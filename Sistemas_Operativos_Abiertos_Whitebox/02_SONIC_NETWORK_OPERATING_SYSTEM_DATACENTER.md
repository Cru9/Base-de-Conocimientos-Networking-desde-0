# 02. SONIC (SOFTWARE FOR OPEN NETWORKING IN THE CLOUD): DATACENTER Y SAI

> **SISTEMAS OPERATIVOS DE RED ABIERTOS (OPEN NETWORKING & WHITE-BOX)**


---



## 1. ¿QUE ES SONIC Y POR QUE REVOLUCIONO LOS CENTROS DE DATOS?

SONiC (Software for Open Networking in the Cloud) fue desarrollado originalmente por
Microsoft para alimentar la red global de hiper-escala de Microsoft Azure.
Posteriormente fue donado a la Linux Foundation y Open Compute Project (OCP).

Hoy en dia es el estandar "de facto" en centros de datos de Google, Alibaba, Microsoft,
eBay y grandes operadores financieros debido a:
- Independencia total de hardware (corre en switches Edgecore, Dell EMC, Celestica,
  Arista, Cisco 8000 con chips Broadcom, Nvidia Spectrum o Innovium).
- Arquitectura 100% modular basada en contenedores Docker y base de datos Redis.
- Capacidad de actualizar protocolos de enrutamiento o telemetria SIN tirar el trafico
  de red que fluye por el chip ASIC de silicio (Hitless container restart).



## 2. ARQUITECTURA DE MICROSERVICIOS BASADA EN DOCKER Y REDIS

A diferencia de los sistemas operativos monoliticos de red, SONiC desacopla cada
servicio en un contenedor Docker independiente comunicado a traves de una base
de datos Redis en memoria (StateDB / ConfigDB / ApplDB / AsicDB):

```text
              +--------------------------------------------------+
              |           SONIC MANAGEMENT (CLI / gNMI)          |
              +--------------------------------------------------+
                                       |
                   (JSON Configs / Redis Pub-Sub API)
                                       v
         +-------------------------------------------------------------+
         |               REDIS IN-MEMORY DATABASE ENGINE               |
         |  [ ConfigDB ]    [ ApplDB ]    [ StateDB ]    [ AsicDB ]    |
         +-------------------------------------------------------------+
               ^                 ^              ^             ^
               |                 |              |             |
        +---------------+ +--------------+ +---------+ +-------------+
        | Container BGP | | Container    | | Cont.   | | Container   |
        |  (FRRouting)  | |     SWSS     | | TEAM    | |    SYNCD    |
        |  BGP-EVPN L3  | | (Switch State| | (LACP)  | | (SAI Bridge)|
        +---------------+ |   Service)   | +---------+ +-------------+
                          +--------------+                    |
                                                              v
                                                +----------------------------+
                                                | SAI (Switch Abstr. Interf.)|
                                                +----------------------------+
                                                              |
                                                              v
                                                +----------------------------+
                                                | MERCHANT SILICON ASIC      |
                                                | (Broadcom / Nvidia / Intel)|
                                                +----------------------------+
```


## 3. CONTENEDORES FUNDAMENTALES EN SONIC

1. 'bgp':
   - Ejecuta la suite FRRouting (FRR) para negociar eBGP entre Spines y Leafs
     y senalizar tuneles VXLAN EVPN en el Datacenter.
2. 'swss' (Switch State Service):
   - Motor logico que orquesta VLANs, tablas FDB MAC, ACLs y politicas de ruteo.
3. 'syncd':
   - Es el componente critico de hardware. Escucha los cambios en la AsicDB y
     llama a las funciones C de la API SAI para programar las tablas TCAM y FIB
     fisicas del chip ASIC.
4. 'pmon' (Platform Monitor):
   - Monitorea sensores termicos, fuentes de poder redundantes (PSU), ventiladores
     y transceptores opticos SFP+/QSFP28.



## 4. TOPOLOGIA DE DATACENTER SPINE-LEAF CON BGP UNNUMBERED EN SONIC

En arquitecturas modernas Leaf-Spine (T0/T1), SONiC utiliza BGP Unnumbered (RFC 5549):
- Permite levantar sesiones eBGP entre Leafs y Spines utilizando unicamente las
  direcciones IPv6 Link-Local descubiertas automaticamente por Router Advertisements.
- Elimina la necesidad de calcular y configurar cientos de subredes /30 o /31 IPv4
  en los cables de interconexion.

Configuracion en /etc/sonic/config_db.json (o mediante el comando 'config'):
{
    "BGP_NEIGHBOR": {
        "Ethernet0": {
            "asn": "65100",
            "name": "SPINE-01",
            "peer_addr": "fe80::1"
        }
    },
    "DEVICE_METADATA": {
        "localhost": {
            "bgp_asn": "65001",
            "hostname": "LEAF-01",
            "type": "LeafRouter"
        }
    }
}



## 5. COMANDOS DE OPERACION Y VERIFICACION EN CLI DE SONIC

SONiC incluye herramientas CLI optimizadas para ingenieros de red:

1. Ver estado fisico de todos los puertos y transceptores opticos:
```text
   show interfaces status
   ! Muestra: Puerto (Ethernet0), Velocidad (100G), Estado (up), FEC (rs), Alias.

2. Ver estado de los transceptores opticos (potencia laser dBm y temperatura):
   show interfaces transceiver status

3. Entrar a la consola de enrutamiento FRR dentro del contenedor:
   vtysh
   show ip bgp summary

4. Ver el estado de todos los contenedores Docker en ejecucion:
   docker ps

5. Reiniciar unicamente el contenedor BGP sin afectar el trafico de hardware:
   docker restart bgp
   ! El trafico sigue fluyendo por el ASIC a velocidad de linea mientras FRR reinicia.

6. Recargar configuracion desde el archivo ConfigDB:
```


`cisco
config reload -y
`
