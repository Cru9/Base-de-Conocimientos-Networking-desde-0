# 06. MANUAL DE FUNDAMENTOS DE RUTEO, METRICAS, AD Y RUTAS ESTATICAS

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---



## 1. ¿QUE ES EL ENRUTAMIENTO Y COMO FUNCIONA EL REENVIO DE PAQUETES?

El enrutamiento (Routing) es el proceso mediante el cual un dispositivo de Capa 3
(Router, Switch Layer 3 o Firewall) determina la ruta optima para transportar
paquetes IP desde una red de origen hacia una red de destino desconocida localmente.

El router divide su operacion en dos planos fundamentales:


### a) Plano de Control (Control Plane):

   - Es el "cerebro" del router.
   - Ejecuta los protocolos de enrutamiento (OSPF, BGP, EIGRP, RIP).
   - Procesa los paquetes Hello, actualizaciones de estado de enlace y acuerdos de vecindad.
   - Construye la Base de Informacion de Enrutamiento (RIB - Routing Information Base),
     comunmente conocida como la "Tabla de Enrutamiento".


### b) Plano de Datos / Reenvio (Data Plane / Forwarding Plane):

   - Es el motor de alta velocidad que conmuta los paquetes de un puerto a otro.
   - En equipos modernos (Cisco, Huawei, Juniper, Arista), el plano de datos NO consulta
     la tabla de enrutamiento CPU tradicional para cada paquete porque seria lentisimo.
   - Utiliza CEF (Cisco Express Forwarding) o estructuras de hardware basadas en ASIC/TCAM:
     * FIB (Forwarding Information Base): Espejo directo de la RIB optimizado para busquedas
       rapidas de prefijos IP sin resolver dependencias recursivas.
     * Adjacency Table (Tabla de Adyacencias): Contiene las cabeceras de Capa 2 (direcciones
       MAC de destino ya resueltas por ARP) para encapsular el paquete de inmediato.



## 2. EL PRINCIPIO DEL PREFIJO MAS LARGO (LONGEST PREFIX MATCH)

Cuando un router recibe un paquete destinado a la IP `192.168.1.35`, busca en su tabla
todas las rutas que coincidan con esa IP. Si existen multiples coincidencias, el router
SIEMPRE elegira la ruta con la mascara de subred mas especifica (con mas bits en 1).

Ejemplo de decision en la tabla de enrutamiento:
  Ruta A: 192.168.0.0/16       (Coincidencia de 16 bits)
  Ruta B: 192.168.1.0/24       (Coincidencia de 24 bits)
  Ruta C: 192.168.1.32/28      (Coincidencia de 28 bits)  <--- GANA (Prefijo mas largo)
  Ruta D: 0.0.0.0/0            (Ruta por defecto: 0 bits)

REGLA DE ORO:
El prefijo mas largo (Longest Prefix Match) tiene prioridad absoluta por encima de
la Distancia Administrativa y por encima de cualquier metrica.



## 3. DISTANCIA ADMINISTRATIVA (AD) vs METRICA

Es comun confundir la Distancia Administrativa con la Metrica:


### a) Distancia Administrativa (AD - Administrative Distance):

   - Mide la CONFIABILIDAD de la fuente de la ruta.
   - Se utiliza unicamente cuando DOS PROTOCOLOS DIFERENTES ofrecen una ruta hacia
     EXACTAMENTE LA MISMA RED con la MISMA MASCARA (ejemplo: OSPF y RIP anuncian `10.5.0.0/24`).
   - A MENOR valor de AD, MAS confiable es la ruta.


## Tabla Estandar de Distancias Administrativas (Cisco):


| Fuente de la Ruta | Distancia Administrativa |
| :--- | :--- |
| Interfaz Conectada Directamente | 0 |
| Ruta Estatica | 1 |
| eBGP (External BGP) | 20 |
| EIGRP Interno | 90 |
| IGRP (Historico Cisco) | 100 |
| OSPF | 110 |
| IS-IS | 115 |
| RIP (v1, v2) | 120 |
| EIGRP Externo | 170 |
| iBGP (Internal BGP) | 200 |
| Inalcanzable / Desconocida | 255 (El router descarta la ruta) |



### b) Metrica:

   - Mide el COSTO o CALIDAD de una ruta dentro de UN MISMO PROTOCOLO.
   - Cada protocolo calcula la metrica de forma distinta:
     * RIP:   Conteo de saltos (Hop Count, 1 a 15).
     * OSPF:  Costo basado en el ancho de banda (Reference Bandwidth / Interface Bandwidth).
     * EIGRP: Metrica compuesta (Ancho de banda minimo + Suma de retardos).
     * BGP:   Conjunto de atributos de politicas (Weight, Local-Pref, AS-Path, MED).



## 4. CLASIFICACION DE LOS PROTOCOLOS DE ENRUTAMIENTO DINAMICO

Los protocolos se clasifican segun su alcance y su algoritmo matematico:

                                  PROTOCOLOS DE ENRUTAMIENTO
                                               |
```text
                     +-------------------------+-------------------------+
                     |                                                   |
            IGP (Interior Gateway)                              EGP (Exterior Gateway)
       (Dentro de un Sistema Autonomo)                     (Entre Sistemas Autonomos)
                     |                                                   |
         +-----------+-----------+                                       |
         |                       |                                       |
   Vector Distancia         Estado de Enlace                       Vector de Ruta
   (Distance Vector)          (Link-State)                         (Path Vector)
         |                       |                                       |
    - RIPv1 / RIPv2            - OSPFv2 / OSPFv3                       - BGP-4
    - IGRP (Obsoleto)          - IS-IS
    - EIGRP (Avanzado)
```


## 5. TIPOS DE RUTAS ESTATICAS Y SU APLICACION EN LA VIDA REAL

A pesar de la existencia de protocolos dinamicos, las rutas estaticas son esenciales:


### a) Ruta Estatica Directa:

   `ip route 172.16.20.0 255.255.255.0 10.0.0.2`
   - Envia trafico hacia un siguiente salto IP especifico.


### b) Ruta por Defecto (Default Route / Gateway of Last Resort):

   `ip route 0.0.0.0 0.0.0.0 203.0.113.1`
   - Atrapa cualquier paquete cuyo destino no coincida con ninguna entrada de la tabla.
   - Se utiliza para la salida general hacia Internet o hacia el router Core.


### c) Ruta Estatica Flotante (Floating Static Route):

   `ip route 0.0.0.0 0.0.0.0 198.51.100.1 200`
   - Se le asigna una Distancia Administrativa deliberadamente mayor (ej. 200) que la
     ruta primaria (AD 1 o AD 110 de OSPF).
   - La ruta flotante permanece OCULTA e inactiva. Solo se instala en la tabla de
     enrutamiento cuando el enlace primario falla y su ruta desaparece.


### d) Ruta de Host (/32):

   `ip route 10.10.10.50 255.255.255.255 10.0.0.2`
   - Apunta a un unico servidor o servicio critico. Prevalece sobre cualquier resumen.


### e) Ruta de Descarte (Null0 / Blackhole):

   `ip route 10.0.0.0 255.0.0.0 Null0`
   - Descarta el trafico inmediatamente en hardware.
   - Se utiliza para prevenir bucles de enrutamiento al sumarizar y para mitigar ataques DDoS.

IMPORTANTE - Next-Hop IP vs Interfaz de Salida:
- En enlaces punto a punto (Serial, GRE, p2p Ethernet), usar la interfaz de salida es valido:
  `ip route 192.168.2.0 255.255.255.0 GigabitEthernet0/1`
- En redes multiacceso Ethernet (LAN o WAN MetroEthernet), NUNCA use solo la interfaz de salida:
  El router asumira que cada IP de destino es un vecino conectado directamente y enviara
  una peticion ARP broadcast por cada paquete ("Proxy ARP"), saturando la tabla ARP y la CPU.
  SIEMPRE especifique la direccion IP del siguiente salto (Next-Hop IP).



## 6. ESCENARIO PRACTICO DE LA VIDA REAL: CONEXION EMPRESARIAL REDUNDANTE CON IP SLA



#### 🎯 OBJETIVO DEL ESCENARIO:

Una empresa financiera cuenta con una sede remota conectada a dos enlaces de Internet:
1. Enlace Primario: Fibra Optica Dedicada de 500 Mbps con ISP-A (Next-Hop: 203.0.113.1).
2. Enlace Respaldo: Conexion Celular 5G / Microondas de 50 Mbps con ISP-B (Next-Hop: 198.51.100.1).

EL PROBLEMA REAL DE PRODUCCION:
Si la fibra del ISP-A se rompe 3 kilometros mas adelante (en la calle), la interfaz local
GigabitEthernet 0/0/1 del router SIGUE ENCENDIDA (Link UP).
Una ruta estatica clasica nunca caeria, enviando los datos a un agujero negro (Black Hole).

SOLUCION:
Implementar IP SLA (Service Level Agreement) para hacer "ping" continuo (ICMP Echo)
a una IP publica confiable (como 8.8.8.8 o el gateway del ISP). Si el ping falla 3 veces,
el objeto TRACK se desactiva y el router conmuta automaticamente hacia la ruta flotante del ISP-B.


#### 🌐 DIAGRAMA DE LA TOPOLOGIA:

```text
                        +-------------------+
                        |   ISP-A (Primario)|
                        |   203.0.113.1     |
                     +--+  (Fibra 500 Mbps) +--+
                     |  +-------------------+  |
     +------------+  |                         |  +---------------+
     |  ROUTER    +--+                         +--+   INTERNET    |
     |  SUCURSAL  |  Gi0/0/1             Gi0/0/2  | (8.8.8.8 DNS) |
     |  (R1)      +--+                         +--+               |
     +-----+------+  |  +-------------------+  |  +---------------+
           |         |  |   ISP-B (Respaldo)|  |
   Red LAN |         +--+   198.51.100.1    +--+
192.168.1.0/24          |    (5G 50 Mbps)   |
                        +-------------------+
```


#### 📋 TABLA DE DIRECCIONAMIENTO:


| Dispositivo | Interfaz | Direccion IP | Mascara | Descripcion |
| :--- | :--- | :--- | :--- | :--- |
| R1 | Gi0/0/0 | 192.168.1.1 | 255.255.255.0 | Gateway LAN Sucursal |
| R1 | Gi0/0/1 | 203.0.113.2 | 255.255.255.252 | WAN Primaria hacia ISP-A |
| R1 | Gi0/0/2 | 198.51.100.2 | 255.255.255.252 | WAN Respaldo hacia ISP-B |
| ISP-A | Gi0/0/1 | 203.0.113.1 | 255.255.255.252 | Gateway ISP-A |
| ISP-B | Gi0/0/2 | 198.51.100.1 | 255.255.255.252 | Gateway ISP-B |




## PASO A PASO: CONFIGURACION COMPLETA EN CISCO IOS / IOS-XE


! 1. Configuracion de Interfaces
```text
interface GigabitEthernet0/0/0
 description RED_LOCAL_LAN
 ip address 192.168.1.1 255.255.255.0
 no shutdown
exit

interface GigabitEthernet0/0/1
 description WAN_PRIMARIA_ISP_A_FIBRA
 ip address 203.0.113.2 255.255.255.252
 no shutdown
exit

interface GigabitEthernet0/0/2
 description WAN_RESPALDO_ISP_B_5G
 ip address 198.51.100.2 255.255.255.252
 no shutdown
exit

! 2. Configuracion de la sonda IP SLA (Sondeo cada 5 segundos hacia el Gateway ISP-A)
ip sla 1
 icmp-echo 203.0.113.1 source-interface GigabitEthernet0/0/1
 threshold 1000
 timeout 2000
 frequency 5
exit

! 3. Iniciar la sonda IP SLA de inmediato y de forma indefinida
ip sla schedule 1 life forever start-time now

! 4. Vincular el objeto TRACK al estado de la sonda IP SLA
track 10 ip sla 1 reachability
 delay down 10 up 5
exit

! 5. Enrutamiento Estatico con Conmutacion por Falla (Failover)
! - Ruta Primaria: Asociada al track 10 (AD = 1). Solo activa si el ping responde.
ip route 0.0.0.0 0.0.0.0 203.0.113.1 track 10

! - Ruta Flotante de Respaldo: AD = 50. Entra de inmediato si el track 10 cae.
ip route 0.0.0.0 0.0.0.0 198.51.100.1 50
```


## COMANDOS DE VALIDACION Y DIAGNOSTICO EN VIVO

1. Verificar estado de la sonda SLA (debe decir OK):
```cisco
   R1# show ip sla summary
```


| ID | Type | Destination | Stats | ReturnCode |
| :--- | :--- | :--- | :--- | :--- |
| 1 | ICMP-echo | 203.0.113.1 | RTT=4ms | OK |


2. Verificar estado del Track (debe decir UP):
```cisco
   R1# show track 10
   Track 10
     IP SLA 1 reachability
     Reachability is Up
     1 change, last change 00:05:22
     Latest operation return code: OK

3. Verificar tabla de enrutamiento activa:
   R1# show ip route 0.0.0.0
   Routing entry for 0.0.0.0/0, supernet
     Known via "static", distance 1, metric 0
     Routing Descriptor Blocks:
     * 203.0.113.1, via GigabitEthernet0/0/1   <--- Ruta Primaria activa


PRUEBA DE ESTRES / SIMULACION DE FALLA EN PRODUCCION:
1. En el router ISP-A apagamos la interfaz o simulamos caida en la nube del carrier:
   ISP-A(config)# interface GigabitEthernet0/0/1
   ISP-A(config-if)# shutdown

2. En R1 observamos los logs automaticos del sistema:
   %TRACK-6-STATE: 10 ip sla 1 reachability Up -> Down

3. Comprobamos la tabla de enrutamiento en R1:
   R1# show ip route 0.0.0.0
   Routing entry for 0.0.0.0/0, supernet
     Known via "static", distance 50, metric 0
     Routing Descriptor Blocks:
     * 198.51.100.1, via GigabitEthernet0/0/2  <--- ¡Conmutacion automatica a 5G!

4. Al restablecer el servicio en ISP-A, el track 10 regresa a UP tras 5 segundos
```


y R1 restablece el trafico principal por fibra optica de forma transparente.
