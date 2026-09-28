# 03. MIKROTIK ROUTEROS V7: NUEVO MOTOR BGP, OSPF, COLAS PCQ Y WIREGUARD

> **SISTEMAS OPERATIVOS DE RED ABIERTOS (OPEN NETWORKING & WHITE-BOX)**


---



## 1. ROUTEROS V7: LA EVOLUCION GENERACIONAL DE MIKROTIK

MikroTik es el fabricante europeo lider en routers de bajo costo y alto rendimiento
para WISPs (Wireless ISPs), PyMEs, carriers medianos y laboratorios de red.
La version RouterOS v7 represento una reescritura total frente a la version 6:
- Kernel de Linux actualizado (v5.6.x+).
- Soporte para Hardware L3 Offloading (L3HW) en switches CRS3xx (enrutamiento por ASIC).
- Soporte nativo para WireGuard VPN de ultra alto rendimiento.
- Nuevo motor de ruteo dinamico con soporte multicore (SMP) real y nueva sintaxis
  de filtros de enrutamiento (Routing Filters).



## 2. CONFIGURACION DE INTERFACES Y DIRECCIONAMIENTO EN CLI

# 1. Crear un Bridge unificado con filtrado VLAN por hardware
/interface bridge
add name=bridge-lan vlan-filtering=yes

# 2. Agregar puertos al Bridge
/interface bridge port
add bridge=bridge-lan interface=ether2
add bridge=bridge-lan interface=ether3

# 3. Asignar direcciones IP a las interfaces
/ip address
add address=10.10.10.1/24 interface=bridge-lan comment="GATEWAY_LAN_CORP"
add address=200.50.10.2/30 interface=ether1 comment="WAN_ENLACE_ISP"



## 3. ENRUTAMIENTO OSPF EN ROUTEROS V7

En v7, OSPF se configura mediante Instancias, Templates y Areas:

# 1. Crear la Instancia OSPF
/routing ospf instance
add name=ospf-instance-1 router-id=10.10.10.1

# 2. Definir el Area Backbone (Area 0)
/routing ospf area
add instance=ospf-instance-1 name=backbone area-id=0.0.0.0

# 3. Habilitar OSPF en la interfaz LAN mediante Interface Template
/routing ospf interface-template
add area=backbone networks=10.10.10.0/24 type=ptp



## 4. BGP MULTI-HOMING Y FILTROS DE ENRUTAMIENTO EN ROUTEROS V7

La sintaxis de filtros de enrutamiento en v7 abandona el formato antiguo y adopta
un lenguaje declarativo con bloques condicionales {}:

# 1. Definir los Routing Filters para BGP de salida hacia el ISP
/routing filter rule
add chain=BGP_OUT_ISP rule="if (dst in 10.10.0.0/16) { set bgp-local-pref 150; accept } else { reject }"

# 2. Configurar la Plantilla de BGP (Template)
/routing bgp template
add name=TMPL_BGP_ISP as=65001 router-id=10.10.10.1 output.filter-chain=BGP_OUT_ISP

# 3. Levantar la Conexion BGP con el ISP
/routing bgp connection
add name=PEER_ISP_PRINCIPAL remote.address=200.50.10.1 .as=64500 template=TMPL_BGP_ISP \
    connect=yes listen=yes local.role=ebgp



## 5. CONTROL DE ANCHO DE BANDA INTELIGENTE CON COLAS PCQ (PER CONNECTION QUEUE)

El algoritmo PCQ (Per Connection Queue) es una de las joyas de RouterOS:
Reparte equitativamente el ancho de banda contratado entre todos los usuarios
activos de la red, sin importar si hay 5 o 500 personas conectadas, evitando que
un solo usuario descargando videos sature la conexion de los demas:

# 1. Definir los tipos de colas PCQ para descarga y subida
/queue type
add kind=pcq name=PCQ_DOWN pcq-classifier=dst-address pcq-rate=0
add kind=pcq name=PCQ_UP pcq-classifier=src-address pcq-rate=0

# 2. Crear la Cola Simple (Simple Queue) aplicada a la subred de usuarios
/queue simple
add name="BALANCEO_EQUITATIVO_EMPLEADOS" target=10.10.10.0/24 \
    max-limit=100M/100M queue=PCQ_UP/PCQ_DOWN comment="100 Mbps simetricos repartidos por igual"



## 6. WIREGUARD VPN SITE-TO-SITE EN ROUTEROS V7

WireGuard es el protocolo VPN moderno mas veloz y ligero, incluido de forma nativa en v7:

# 1. Crear la interfaz WireGuard (genera clave publica y privada automaticamente)
/interface wireguard
add name=wg-sucursal listen-port=13231 comment="TUNEL_WIREGUARD_SUCURSAL"

# 2. Asignar direccion IP punto a punto al tunel
/ip address
add address=172.16.50.1/30 interface=wg-sucursal

# 3. Configurar el extremo remoto (Peer)
/interface wireguard peers
add interface=wg-sucursal public-key="xT9478sfljsf0293jslkfd98234jsk=" \
    endpoint-address=190.20.10.5 endpoint-port=13231 \
    allowed-address=172.16.50.2/32,10.20.0.0/16 persistent-keepalive=25s



## 7. COMANDOS DE MONITOREO Y VERIFICACION

1. Ver el estado de las sesiones BGP:
   /routing bgp connection print
   ! Muestra: Flags (A: active, E: established), Local AS, Remote AS, Uptime.

2. Ver la tabla de enrutamiento activa:
   /ip route print
   ! Rutas con banderas: D (Dynamic), A (Active), c (Connected), b (BGP), o (OSPF).

3. Monitorear el consumo de CPU por proceso en tiempo real:
   /tool profile
   ! Permite ver si el consumo es por firewall, routing, bfd o criptografia.

4. Ver el flujo de trafico en vivo en las colas:

## /queue simple print stats
