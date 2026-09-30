# PARTE 6: DATACENTER, SPINE-LEAF, VXLAN Y BGP EVPN (EJEMPLOS 101 AL 120)

> **ENRUTAMIENTO AVANZADO Y REDES WAN - GUIA PRACTICA DEFINITIVA**


---



## EJEMPLO 101: ARQUITECTURA DATACENTER SPINE-LEAF (CLOS TOPOLOGY) CON eBGP


> 🏢 **ESCENARIO REAL:**
En centros de datos modernos, el modelo tradicional de 3 capas con Spanning Tree
(STP) esta obsoleto porque bloquea el 50% de los enlaces. Se implementa una topologia
Spine-Leaf de 2 niveles (red Clos) donde cada Leaf se conecta a todos los Spines
usando eBGP Underlay con ASNs independientes para balanceo ECMP masivo sin bucles.


#### 🌐 DIAGRAMA:

```text
             [SPINE 1 - AS 65001]              [SPINE 2 - AS 65002]
                      \        \                /        /
                       \        \              /        /
                        \        \            /        /
                         \        +----+----+         /
                          \            |             /
                           \           |            /
                   +--------+----------+-----------+--------+
                   |                                        |
          [LEAF 1 - AS 65011]                      [LEAF 2 - AS 65012]
         (Top of Rack - Rack 1)                   (Top of Rack - Rack 2)
                   |                                        |
               [SERVIDORES]                             [SERVIDORES]
```


#### 💻 CONFIGURACION CISCO NX-OS / IOS-XE (LEAF 1):

```cisco
interface Ethernet1/1
 description UPLINK_HACIA_SPINE1
 no switchport
 ip address 10.0.1.2 255.255.255.252
 mtu 9216                           ! Jumbo Frames obligatorio en Datacenter
 no shutdown
exit

interface Ethernet1/2
 description UPLINK_HACIA_SPINE2
 no switchport
 ip address 10.0.2.2 255.255.255.252
 mtu 9216
 no shutdown
exit

router bgp 65011
 router-id 10.255.1.1
 neighbor 10.0.1.1 remote-as 65001  ! Spine 1
 neighbor 10.0.2.1 remote-as 65002  ! Spine 2
 address-family ipv4 unicast
  maximum-paths 64                  ! ECMP masivo sobre todos los Spines
  network 10.255.1.1/32
exit
```


#### 🔍 Verificación:

```cisco
LEAF1# show ip route bgp
(Muestra rutas con multiples saltos paralelos hacia los otros racks).
```



## EJEMPLO 102: ENCAPSULACION VXLAN Y ASIGNACION DE VNI (VXLAN NETWORK IDENTIFIER)


> 🏢 **ESCENARIO REAL:**
Superar el limite de 4096 VLANs de la norma 802.1Q en un Datacenter multi-inquilino
(Multi-Tenant). VXLAN encapsula tramas Ethernet de Capa 2 dentro de paquetes UDP
(puerto 4789) en Capa 3, permitiendo mas de 16 millones de segmentos (VNIs de 24 bits).


#### 🌐 DIAGRAMA:

```text
  [VLAN 100 en Rack 1] ===> [VTEP LEAF 1] === Paquete UDP 4789 (VNI 10100) ===> [VTEP LEAF 2] ===> [VLAN 100 en Rack 2]
```


#### 💻 CONFIGURACION CISCO NX-OS:

```cisco
feature nv overlay
feature vn-segment-vlan-based

vlan 100
 vn-segment 10100                   ! Mapeo de VLAN local a VNI global
exit
```


#### 🔍 Verificación:

```cisco
LEAF1# show vxlan
```



## EJEMPLO 103: CONFIGURACION DE INTERFAZ NVE (NETWORK VIRTUALIZATION EDGE - VTEP)


> 🏢 **ESCENARIO REAL:**
Habilitar la interfaz logica NVE1 que actua como punto final del tunel VXLAN (VTEP)
para empaquetar y desempaquetar las tramas de los servidores del rack.


#### 💻 CONFIGURACION CISCO NX-OS:

```cisco
interface nve1
 no shutdown
 source-interface loopback1         ! IP del VTEP anunciada por el Underlay
 host-reachability protocol bgp     ! Aprendizaje por plano de control EVPN
 member vni 10100
  ingress-replication protocol bgp
exit
```


#### 🔍 Verificación:

```cisco
LEAF1# show nve interface nve1 detail
```



## EJEMPLO 104: BGP EVPN (ETHERNET VPN) COMO PLANO DE CONTROL PARA VXLAN


> 🏢 **ESCENARIO REAL:**
En lugar de inundar la red con broadcast para aprender direcciones MAC (Flood and Learn),
BGP EVPN (RFC 7432) distribuye las direcciones MAC e IP de los servidores como
rutas de enrutamiento Type-2, eliminando el trafico de tormenta en el Datacenter.


#### 💻 CONFIGURACION CISCO (LEAF):

```cisco
router bgp 65011
 address-family l2vpn evpn
  neighbor 10.255.0.1 activate      ! Peering EVPN hacia el Spine (Route Server)
  neighbor 10.255.0.1 send-community both
exit

evpn
 vni 10100 l2
  rd auto
  route-target import auto
  route-target export auto
exit
```


#### 🔍 Verificación:

```cisco
LEAF1# show bgp l2vpn evpn
```



## EJEMPLO 105: DISTRIBUTED ANYCAST GATEWAY EN DATACENTER CON VXLAN


> 🏢 **ESCENARIO REAL:**
Una maquina virtual (VM) se migra en vivo (vMotion) del Rack 1 al Rack 20.
Para que su Gateway por defecto no cambie ni agregue latencia cruzando el Datacenter,
TODOS los switches Leaf tienen exactamente la MISMA direccion IP y la MISMA direccion
MAC virtual configurada en la SVI (Distributed Anycast Gateway).


#### 🌐 DIAGRAMA:

```text
  [LEAF 1: SVI 100 IP 10.100.1.1 / MAC: 0000.2222.3333] <--- Mismo Gateway en todo el DC ---> [LEAF 2: SVI 100 IP 10.100.1.1 / MAC: 0000.2222.3333]
```


#### 💻 CONFIGURACION CISCO NX-OS:

```cisco
fabric forwarding anycast-gateway-mac 0000.2222.3333

interface Vlan100
 no shutdown
 vrf member TENANT_PRODUCCION
 ip address 10.100.1.1/24
 fabric forwarding mode anycast-gateway
exit
```


#### 🔍 Verificación:

```cisco
LEAF1# show fabric forwarding detail
```



## EJEMPLO 106: ENRUTAMIENTO SIMETRICO INTER-VNI (SYMMETRIC IRB CON L3VNI)


> 🏢 **ESCENARIO REAL:**
El Servidor Web (VNI 10100) necesita comunicarse con la Base de Datos (VNI 10200).
El enrutamiento simetrico utiliza una VNI de Capa 3 dedicada (`VNI 50001`) y una VRF
para enrutar directamente en el Leaf de origen y conmutar en el Leaf de destino.


#### 💻 CONFIGURACION CISCO:

```cisco
vlan 500
 vn-segment 50001                   ! VLAN y VNI de transito Layer 3

vrf definition TENANT_PRODUCCION
 vni 50001
 address-family ipv4
 exit-address-family
exit

interface Vlan500
 vrf forwarding TENANT_PRODUCCION
 ip forward
 no shutdown
exit

interface nve1
 member vni 50001 associate-vrf    ! Asocia la L3VNI al VTEP
exit
```



## EJEMPLO 107: MULTI-CHASSIS ETHERCHANNEL (vPC EN CISCO NX-OS)


> 🏢 **ESCENARIO REAL:**
Un servidor critico con dos tarjetas de red (NIC Teaming) se conecta a dos switches
Leaf fisicamente independientes (Leaf-A y Leaf-B). Mediante vPC (Virtual Port-Channel),
ambos switches actuan como una sola entidad logica de Capa 2 hacia el servidor.


#### 🌐 DIAGRAMA:

```text
  +---------------+               +---------------+
  |  LEAF A (vPC) +===============+  LEAF B (vPC) |
  +-------+-------+  Peer-Link    +-------+-------+
           \                             /
            \                           /  Port-Channel 10 (LACP Activo)
             +------------+------------+
                          |
                  [SERVIDOR BLADE]
```


#### 💻 CONFIGURACION CISCO NX-OS:

```cisco
! 1. Dominio vPC:
vpc domain 1
 peer-switch
 role priority 1000
 peer-keepalive destination 172.16.1.2 source 172.16.1.1 vrf management
exit

! 2. Enlace Peer-Link entre ambos switches:
interface Port-channel 1
 description VPC_PEER_LINK
 switchport mode trunk
 vpc peer-link
 no shutdown
exit

! 3. Puerto hacia el Servidor:
interface Port-channel 10
 description ENLACE_DUAL_HACIA_SERVIDOR
 switchport mode access
 switchport access vlan 100
 vpc 10
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
LEAF_A# show vpc brief
```



## EJEMPLO 108: M-LAG (MULTICHASSIS LINK AGGREGATION) EN SWITCHES HUAWEI


> 🏢 **ESCENARIO REAL:**
Implementar agregacion multichasis equivalente a vPC en switches Huawei CloudEngine
(CE6800 / CE12800) para redundancia de servidores en Datacenter.


#### 💻 CONFIGURACION HUAWEI VRP:

```text
# 1. Configuracion de DFS Group (M-LAG)
dfs-group 1
 source ip 172.16.1.1
 priority 150
#
# 2. Peer-link entre switches
interface Eth-Trunk 1
 description PEER_LINK_MLAG
 mode lacp-static
 peer-link 1
#
# 3. Enlace hacia el Servidor
interface Eth-Trunk 10
 description CONEXION_HACIA_SERVIDOR
 mode lacp-static
 port default vlan 100
 dfs-group 1 m-lag 10
#
```


#### 🔍 Verificación:

```cisco
<LEAF_HUAWEI> display dfs-group 1 m-lag
```



## EJEMPLO 109: DATA CENTER INTERCONNECT (DCI) CON VXLAN EVPN MULTI-SITE


> 🏢 **ESCENARIO REAL:**
Interconectar dos Datacenters distantes (DC Guadalajara y DC Monterrey) a traves de
una red WAN. Los Border Gateways (BGWs) extienden las VNIs de Capa 2 y Capa 3 entre sitios.


#### 🌐 DIAGRAMA:

```text
  [DC GUADALAJARA]                                           [DC MONTERREY]
   (Leafs / Spines)                                         (Leafs / Spines)
          |                                                        |
    [BORDER GW 1] <========== WAN / DCI (BGP EVPN) ==========> [BORDER GW 2]
```


#### 💻 CONFIGURACION CISCO (BORDER GATEWAY):

```cisco
evpn multisite border-gateway 1
 delay-restore time 60
exit

interface nve1
 multisite border-gateway interface loopback100
 member vni 10100
 exit
exit

router bgp 65000
 neighbor 198.51.100.2 remote-as 65500  ! Peering DCI con el otro sitio
  address-family l2vpn evpn
   send-community both
   rewrite-evpn-rt-asn                  ! Cruce de politicas multi-sitio
  exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
BGW1# show evpn multisite summary
```



## EJEMPLO 110: RoCEv2 (RDMA OVER CONVERGED ETHERNET) Y LOSSLESS ETHERNET


> 🏢 **ESCENARIO REAL:**
Para aplicaciones de Inteligencia Artificial (IA) y Storage NVMe-over-Fabrics, la
perdida de un solo paquete destruye el rendimiento. Se configura Ethernet sin perdidas
mediante PFC (Priority Flow Control) y ECN (Explicit Congestion Notification).


#### 💻 CONFIGURACION CISCO NX-OS:

```cisco
priority-flow-control mode on
class-map type qos match-any CLASE_ROCE
 match cos 3
exit

policy-map type network-qos POLITICA_LOSSLESS
 class type network-qos CLASE_ROCE
  pause no-drop                     ! Desactiva descarte de paquetes mediante Pause Frames
  congestion-control random-detect  ! ECN
exit

system qos
 service-policy type network-qos POLITICA_LOSSLESS
exit
```


#### 🔍 Verificación:

```cisco
LEAF1# show interface priority-flow-control
```



## EJEMPLO 111: BGP UNNUMBERED EN FABRIC DE DATACENTER


> 🏢 **ESCENARIO REAL:**
En fabrics gigantes con 100 Spines y 500 Leafs, asignar direcciones IP `/30` o `/31`
a cada cable inter-switch desperdicia miles de IPs y horas de diseno.
BGP Unnumbered utiliza IPv6 Link-Local (RFC 5549) para establecer sesiones eBGP
automaticas en cada puerto sin asignar ninguna IP IPv4 al enlace fisico.


#### 🌐 DIAGRAMA:

```text
  [SPINE: Gi0/1 (No IP)] <===== BGP Unnumbered (IPv6 Link-Local FE80::) =====> [LEAF: Gi0/1 (No IP)]
```


#### 💻 CONFIGURACION CISCO IOS-XE / NX-OS:

```cisco
interface GigabitEthernet0/0/1
 description ENLACE_HACIA_SPINE
 no ip address
 ipv6 enable
 no shutdown
exit

router bgp 65011
 neighbor GigabitEthernet0/0/1 interface remote-as external
 address-family ipv4 unicast
  neighbor GigabitEthernet0/0/1 activate
  neighbor GigabitEthernet0/0/1 extended-nexthop
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
LEAF1# show ip bgp summary
```



## EJEMPLO 112: MICROSEGMENTACION CON GRUPOS DE SEGURIDAD (SECURITY GROUPS)


> 🏢 **ESCENARIO REAL:**
Dos maquinas virtuales en la misma subred (ej. Servidor Web 1 y Servidor Web 2 en
`10.100.1.0/24`) no deben comunicarse entre si para evitar movimiento lateral en caso
de hackeo. Se aplica aislamiento de Capa 2 local sin cambiar de VLAN.


#### 💻 CONFIGURACION CISCO:

```cisco
interface GigabitEthernet1/0/1
 description PUERTO_VM_1
 switchport protected              ! Bloquea comunicacion con otros puertos protegidos
exit

interface GigabitEthernet1/0/2
 description PUERTO_VM_2
 switchport protected
exit
```


#### 🔍 Verificación:

```cisco
LEAF# show interfaces switchport | include Protected
```



## EJEMPLO 113: BALANCEO DE CARGA DE SERVIDORES CON BGP ANYCAST


> 🏢 **ESCENARIO REAL:**
Varios servidores web de alto rendimiento (Nginx) anuncian la misma IP publica
(`198.51.100.50/32`) mediante sesiones BGP locales hacia los switches Leaf.
Los switches reparten el trafico web mundial entre los servidores usando ECMP.


#### 🌐 DIAGRAMA:

```text
                   [SWITCH LEAF - ECMP]
```

                    IP VIP: 198.51.100.50
                             |
```text
         +-------------------+-------------------+
         |                                       |
  [SERVIDOR NGINX 1]                      [SERVIDOR NGINX 2]
  Anuncia 198.51.100.50                   Anuncia 198.51.100.50
```


#### 💻 CONFIGURACION EN SWITCH LEAF:

```text
router bgp 65011
 neighbor 10.100.1.50 remote-as 65099   ! Servidor Nginx 1
 neighbor 10.100.1.51 remote-as 65099   ! Servidor Nginx 2
 address-family ipv4
  maximum-paths 16
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
LEAF# show ip route 198.51.100.50
(Muestra dos saltos de salida simultaneos repartiendo carga).
```



## EJEMPLO 114: SUPRESION DE ARP EN FABRIC VXLAN EVPN


> 🏢 **ESCENARIO REAL:**
En redes tradicionales, las peticiones ARP broadcast inundan todos los racks.
Al activar ARP Suppression en el VTEP, el switch local intercepta la peticion ARP,
consulta su tabla BGP EVPN y responde el ARP de inmediato en hardware localmente.


#### 💻 CONFIGURACION CISCO NX-OS:

```cisco
interface nve1
 member vni 10100
  suppress-arp                      ! Elimina el flooding de broadcast ARP
 exit
exit
```


#### 🔍 Verificación:

```cisco
LEAF1# show ip arp suppression-cache
```



## EJEMPLO 115: EVPN TYPE-5 PREFIX ROUTES PARA SALIDA A INTERNET


> 🏢 **ESCENARIO REAL:**
Los Border Leafs del Datacenter aprenden la ruta por defecto de Internet desde los
routers de borde WAN y la inyectan hacia todos los Leafs como una ruta EVPN Type-5.


#### 💻 CONFIGURACION CISCO (BORDER LEAF):

```cisco
router bgp 65000
 vrf TENANT_PRODUCCION
  address-family ipv4 unicast
   default-information originate
   advertise l2vpn evpn             ! Genera el anuncio Type-5 Prefix Route
  exit-address-family
 exit
exit
```


#### 🔍 Verificación:

```cisco
LEAF_INTERNO# show bgp l2vpn evpn route-type 5
```



## EJEMPLO 116: VXLAN BRIDGING L2 EN SWITCHES HUAWEI CLOUDENGINE


> 🏢 **ESCENARIO REAL:**
Implementar el equivalente de encapsulacion VXLAN en switches de Datacenter Huawei.


#### 💻 CONFIGURACION HUAWEI VRP:

```text
# 1. Habilitar puente VXLAN
bridge-domain 10
 vxlan vni 10100
#
# 2. Interfaz VTEP (Nve)
interface Nve1
 source-ip 10.255.1.1
 vni 10100 head-end peer-list 10.255.2.2
#
# 3. Mapeo de subinterfaz en el puerto hacia el servidor
interface 10GE1/0/1.10 mode l2
 encapsulation dot1q vid 100
 bridge-domain 10
#
```


#### 🔍 Verificación:

```cisco
<LEAF_HW> display vxlan vni 10100 verbose
```



## EJEMPLO 117: REDIRECCION DE TRAFICO A APPLIANCE DE SEGURIDAD (SERVICE CHAINING)


> 🏢 **ESCENARIO REAL:**
Todo el trafico entre la VLAN Web y la VLAN de Base de Datos en el Datacenter
debe forzarse a pasar por un Firewall de Proxima Generacion (Palo Alto / Fortinet).


#### 💻 CONFIGURACION CISCO:

```cisco
route-map REVIZAR_FW permit 10
 match ip address ACL_WEB_A_BD
 set ip next-hop 10.100.50.254      ! IP del Firewall NGFW
exit

interface Vlan100
 ip policy route-map REVIZAR_FW
exit
```



## EJEMPLO 118: MONITORIZACION DE LATENCIA CON TELEMETRIA EN TIEMPO REAL (ERSPAN)


> 🏢 **ESCENARIO REAL:**
Capturar trafico de un puerto de servidor en el Rack 1 y enviarlo encapsulado en GRE
por la red IP hacia el servidor analizador de Wireshark en el Rack 15.


#### 💻 CONFIGURACION CISCO:

```cisco
monitor session 1 type erspan-source
 source interface Ethernet1/1 both
 destination
  erspan-id 101
  ip address 10.200.1.50            ! IP del Servidor Wireshark
  origin ip 10.255.1.1
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
LEAF1# show monitor session 1
```



## EJEMPLO 119: SEGMENTACION DE FABRIC MEDIANTE EVPN TENANT VRFs


> 🏢 **ESCENARIO REAL:**
Aislar completamente el ambiente de Desarrollo del ambiente de Produccion en el Datacenter.
Cada ambiente cuenta con su propia VRF y su propio identificador L3VNI.


#### 💻 CONFIGURACION CISCO:

```cisco
vrf definition DEV
 vni 50002
 address-family ipv4
 exit-address-family
exit

vrf definition PROD
 vni 50001
 address-family ipv4
 exit-address-family
exit
```



## EJEMPLO 120: AUTOMATIZACION DE FABRIC CON ZERO-TOUCH PROVISIONING (ZTP)


> 🏢 **ESCENARIO REAL:**
Cuando un nuevo switch Leaf se saca de su caja y se conecta a la red sin configuracion,
solicita una IP por DHCP (Opcion 67), descarga su imagen de software y su archivo
de configuracion de inicio desde un servidor TFTP/HTTP automaticamente.


#### 💻 CONFIGURACION DE SERVIDOR DHCP (OPCION 67):

```text
ip dhcp pool ZTP_DATACENTER
 network 172.16.1.0 255.255.255.0
 bootfile-name http://172.16.1.10/configs/leaf-rack4.cfg
 default-router 172.16.1.1
```


`cisco
exit
`
