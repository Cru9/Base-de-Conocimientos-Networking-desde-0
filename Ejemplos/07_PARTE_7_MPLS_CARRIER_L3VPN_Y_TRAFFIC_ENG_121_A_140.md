# PARTE 7: MPLS, CARRIER L3VPN Y TRAFFIC ENGINEERING (EJEMPLOS 121 AL 140)

> **ENRUTAMIENTO AVANZADO Y REDES WAN - GUIA PRACTICA DEFINITIVA**


---



## EJEMPLO 121: FUNDAMENTOS DE CONMUTACION POR ETIQUETAS MPLS CON LDP


> 🏢 **ESCENARIO REAL:**
En el nucleo de un Proveedor de Servicios de Internet (Carrier / ISP), los routers P
(Provider) conmutan paquetes a velocidad de silicio leyendo etiquetas numericas simples
de 32 bits (Label Switching) en lugar de consultar tablas de enrutamiento IP gigantescas.
Se habilita MPLS y LDP (Label Distribution Protocol) en las interfaces del Core.


#### 🌐 DIAGRAMA:

```text
  [ROUTER PE 1] ===== Etiqueta LDP (ej. 1024) =====> [ROUTER P CORE] ===== Etiqueta (2048) =====> [ROUTER PE 2]
```


#### 💻 CONFIGURACION CISCO IOS-XE (CORE PROVIDER):

```cisco
ip cef
mpls ldp router-id Loopback0 force

interface GigabitEthernet0/0/1
 description ENLACE_CORE_MPLS
 mpls ip                             ! Activa MPLS y LDP en el enlace
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R_CORE# show mpls ldp neighbor
R_CORE# show mpls forwarding-table
```



## EJEMPLO 122: PENULTIMATE HOP POPPING (PHP) Y ETIQUETA EXPLICITA NULL


> 🏢 **ESCENARIO REAL:**
Para evitar que el router PE de destino tenga que hacer dos busquedas (desencapsular
la etiqueta MPLS y luego buscar la IP en la tabla), el penultimo router retira la
etiqueta externa antes de entregar el paquete (PHP - RFC 3032). Utiliza la etiqueta
implicita Null (Label 3).


#### 💻 CONFIGURACION Y DIAGNOSTICO:

```text
R_PENULTIMO# show mpls forwarding-table
Local  Outgoing   Prefix            Bytes tag  Outgoing   Next Hop
tag    tag        or VC or Tunnel   switched   interface
105    Pop tag    10.255.0.2/32     145020     Gi0/0/2    10.1.1.2
(Notese la accion 'Pop tag': remueve la etiqueta para aliviar la CPU del PE final).
```



## EJEMPLO 123: DEFINICION DE VRF, RD (ROUTE DISTINGUISHER) Y ROUTE TARGETS (RT)


> 🏢 **ESCENARIO REAL:**
Un Carrier aloja a dos clientes diferentes: Banco Alfa y Tiendas Beta. Ambos clientes
usan la misma direccion privada interna `192.168.1.0/24`. Mediante VRFs y RDs,
el router PE separa y transporta ambas redes sin conflicto alguno.


#### 🌐 DIAGRAMA:

```text
  [BANCO ALFA: 192.168.1.0/24]   ---> [RD 65000:100] ---> VPNv4: 65000:100:192.168.1.0/24 (UNICA!)
  [TIENDAS BETA: 192.168.1.0/24] ---> [RD 65000:200] ---> VPNv4: 65000:200:192.168.1.0/24 (UNICA!)
```


#### 💻 CONFIGURACION CISCO IOS-XE (ROUTER PE):

```cisco
vrf definition CLIENTE_BANCO_ALFA
 rd 65000:100                       ! Convierte IPv4 en direccion VPNv4 unica
 address-family ipv4
  route-target export 65000:100     ! Etiqueta comunitaria BGP de exportacion
  route-target import 65000:100     ! Etiqueta comunitaria BGP de importacion
 exit-address-family
exit

interface GigabitEthernet0/0/2
 description CONEXION_HACIA_SEDE_BANCO
 vrf forwarding CLIENTE_BANCO_ALFA
 ip address 10.1.1.1 255.255.255.252
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
PE1# show vrf detail CLIENTE_BANCO_ALFA
```



## EJEMPLO 124: CONFIGURACION DE MP-BGP (MULTIPROTOCOL BGP) VPNv4


> 🏢 **ESCENARIO REAL:**
Los routers PE de los extremos de la red del Carrier se conectan mediante una sesion
iBGP multiprotocolo para transportar las rutas VPNv4 de los clientes corporativos.


#### 💻 CONFIGURACION CISCO IOS-XE (ROUTER PE):

```cisco
router bgp 65000
 neighbor 10.255.0.2 remote-as 65000     ! Loopback del otro router PE
 neighbor 10.255.0.2 update-source Loopback0
 address-family vpnv4
  neighbor 10.255.0.2 activate
  neighbor 10.255.0.2 send-community extended ! Envia Route-Targets
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
PE1# show bgp vpnv4 unicast all summary
```



## EJEMPLO 125: ENRUTAMIENTO PE-CE CON eBGP ENTRE CLIENTE Y CARRIER


> 🏢 **ESCENARIO REAL:**
El router de la empresa (CE - Customer Edge) intercambia rutas con el router del
Carrier (PE - Provider Edge) mediante una sesion eBGP dedicada dentro de la VRF.


#### 💻 CONFIGURACION CISCO (ROUTER PE):

```cisco
router bgp 65000
 address-family ipv4 vrf CLIENTE_BANCO_ALFA
  neighbor 10.1.1.2 remote-as 65111      ! AS del Banco
  neighbor 10.1.1.2 activate
 exit-address-family
exit

! En el Router del Banco (CE):
router bgp 65111
 neighbor 10.1.1.1 remote-as 65000       ! AS del Carrier
 network 192.168.10.0 mask 255.255.255.0
exit
```


#### 🔍 Verificación:

```cisco
PE# show ip bgp vpnv4 vrf CLIENTE_BANCO_ALFA summary
```



## EJEMPLO 126: ENRUTAMIENTO PE-CE CON OSPF Y DOMAIN-ID


> 🏢 **ESCENARIO REAL:**
El cliente bancario exige correr OSPF entre sus sucursales a traves de la nube MPLS
del Carrier, haciendo que la red MPLS se comporte como un Superbackbone transparente.


#### 💻 CONFIGURACION CISCO (ROUTER PE):

```cisco
router ospf 100 vrf CLIENTE_BANCO_ALFA
 domain-id 0.0.0.100
 network 10.1.1.0 0.0.0.3 area 0
 redistribute bgp 65000 subnets
exit

router bgp 65000
 address-family ipv4 vrf CLIENTE_BANCO_ALFA
  redistribute ospf 100
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
CE# show ip route ospf
(Las rutas de otras sucursales se aprenden como Inter-Area 'O IA').
```



## EJEMPLO 127: ENRUTAMIENTO PE-CE CON RUTAS ESTATICAS HACIA EL CLIENTE


> 🏢 **ESCENARIO REAL:**
Para sucursales pequenas donde el router CE no soporta BGP ni OSPF, el Carrier
agrega una ruta estatica apuntando a la IP del cliente y la inyecta a MP-BGP.


#### 💻 CONFIGURACION CISCO (ROUTER PE):

```cisco
ip route vrf CLIENTE_BANCO_ALFA 192.168.50.0 255.255.255.0 10.1.1.2

router bgp 65000
 address-family ipv4 vrf CLIENTE_BANCO_ALFA
  redistribute static
 exit-address-family
exit
```



## EJEMPLO 128: PREVENCION DE BUCLES CON BGP AS-OVERRIDE EN EL CARRIER


> 🏢 **ESCENARIO REAL:**
Si todas las sucursales del cliente usan el mismo ASN privado (ej. AS 65111):
Cuando el router CE de la Sucursal B recibe una ruta que contiene el AS 65111 en el
AS-Path, la regla de prevencion de bucles de BGP la DESCARTA de inmediato.
`as-override` en el router PE reemplaza el AS del cliente por el AS del Carrier.


#### 🌐 DIAGRAMA:

```text
  [Sucursal A: AS 65111] ---> [PE 1] ---> AS-Path: 65000 65000 (Override!) ---> [Sucursal B: Acepta ruta!]
```


#### 💻 CONFIGURACION CISCO (ROUTER PE):

```cisco
router bgp 65000
 address-family ipv4 vrf CLIENTE_BANCO_ALFA
  neighbor 10.1.1.2 as-override      ! Reemplaza ASN del cliente
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
CE_B# show ip bgp
```



## EJEMPLO 129: BGP ALLOWAS-IN EN EL ROUTER CE DEL CLIENTE


> 🏢 **ESCENARIO REAL:**
Alternativa si el Carrier no soporta `as-override`: Se configura el router CE
del cliente para que acepte su propio ASN en el AS-Path hasta 2 veces.


#### 💻 CONFIGURACION CISCO (ROUTER CE DEL CLIENTE):

```cisco
router bgp 65111
 neighbor 10.1.1.1 allowas-in 2      ! Permite su propio AS hasta 2 veces
exit
```



## EJEMPLO 130: ENLACES DE RESPALDO OSPF SHAM-LINK SOBRE MPLS


> 🏢 **ESCENARIO REAL:**
Dos sedes del cliente tienen un enlace backdoor privado (Fibra oscura) y ademas
estan conectadas por MPLS. OSPF siempre preferiria el backdoor porque lo ve Intra-Area (O)
frente al MPLS que lo ve Inter-Area (O IA). Se crea un Sham-Link logico sobre la nube
MPLS para que MPLS compita como enlace Intra-Area.


#### 💻 CONFIGURACION CISCO (ROUTER PE):

```cisco
interface Loopback100
 description SHAM_LINK_SOURCE
 vrf forwarding CLIENTE_BANCO_ALFA
 ip address 10.255.100.1 255.255.255.255
exit

router ospf 100 vrf CLIENTE_BANCO_ALFA
 area 0 sham-link 10.255.100.1 10.255.100.2 cost 10
exit
```


#### 🔍 Verificación:

```cisco
PE# show ip ospf sham-links
```



## EJEMPLO 131: MPLS L3VPN EN ROUTERS HUAWEI VRP


> 🏢 **ESCENARIO REAL:**
Implementacion de VPN de Capa 3 equivalente en routers de operador Huawei (NetEngine / AR).


#### 💻 CONFIGURACION HUAWEI VRP:

```text
# 1. Habilitar MPLS y LDP global
mpls lsr-id 10.255.0.1
mpls
mpls ldp
#
# 2. Instancia VPN del Cliente
ip vpn-instance EMPRESA_MINERA
 ipv4-family
  route-distinguisher 65000:500
  vpn-target 65000:500 both
#
# 3. Interfaz del Cliente
interface GigabitEthernet0/0/1
 ip binding vpn-instance EMPRESA_MINERA
 ip address 10.5.1.1 255.255.255.252
#
# 4. BGP VPNv4
bgp 65000
 peer 10.255.0.2 as-number 65000
 peer 10.255.0.2 connect-interface LoopBack0
 #
 ipv4-family vpnv4
  peer 10.255.0.2 enable
 #
 ipv4-family vpn-instance EMPRESA_MINERA
  import-route direct
#
```


#### 🔍 Verificación:

```cisco
<PE_HUAWEI> display ip routing-table vpn-instance EMPRESA_MINERA
```



## EJEMPLO 132: MPLS TRAFFIC ENGINEERING (MPLS-TE) CON EXTENSIONES OSPF


> 🏢 **ESCENARIO REAL:**
En lugar de enviar siempre el trafico por el camino mas corto (SPF), MPLS-TE permite
calcular caminos basados en restricciones de ancho de banda disponible (CSPF - Constrained SPF).


#### 💻 CONFIGURACION CISCO IOS-XE:

```cisco
mpls traffic-eng tunnels

router ospf 1
 mpls traffic-eng router-id Loopback0
 mpls traffic-eng area 0
exit

interface GigabitEthernet0/0/1
 mpls traffic-eng tunnels
 ip rsvp bandwidth 100000 100000    ! Reserva 100 Mbps para ingenieria de trafico
exit
```


#### 🔍 Verificación:

```cisco
R1# show mpls traffic-eng topology
```



## EJEMPLO 133: CREACION DE TUNELES MPLS TE EXPLICITOS


> 🏢 **ESCENARIO REAL:**
Crear un tunel virtual de ingenieria de trafico que fuerce a los paquetes de VoIP
a viajar por una ruta especifica reservando 50 Mbps de ancho de banda garantizado.


#### 💻 CONFIGURACION CISCO:

```cisco
ip explicit-path name RUTA_VIP enable
 next-address 10.0.1.2              ! Router P1
 next-address 10.0.2.2              ! Router P3
 next-address 10.255.0.2            ! Router PE Destino
exit

interface Tunnel100
 description TUNEL_MPLS_TE_VOZ
 ip unnumbered Loopback0
 tunnel mode mpls traffic-eng
 tunnel destination 10.255.0.2
 tunnel mpls traffic-eng path-option 1 explicit name RUTA_VIP
 tunnel mpls traffic-eng bandwidth 50000 ! Reserva 50 Mbps
exit
```


#### 🔍 Verificación:

```cisco
R1# show mpls traffic-eng tunnels brief
```



## EJEMPLO 134: FAST REROUTE (FRR) EN MPLS TE CON CONMUTACION EN < 50 MS


> 🏢 **ESCENARIO REAL:**
Proteger un enlace critico del Carrier. Si un cable se corta, el router previo conmuta
al camino de respaldo pre-calculado en hardware en MENOS DE 50 MILISEGUNDOS.


#### 💻 CONFIGURACION CISCO:

```cisco
interface Tunnel100
 tunnel mpls traffic-eng fast-reroute
exit
```


#### 🔍 Verificación:

```cisco
R1# show mpls traffic-eng fast-reroute database
```



## EJEMPLO 135: SEGMENT ROUTING (SR-MPLS) CON PREFIX-SIDs


> 🏢 **ESCENARIO REAL:**
Segment Routing simplifica el plano de control eliminando LDP y RSVP. Las etiquetas
(SIDs - Segment Identifiers) se distribuyen directamente a traves de OSPF o IS-IS.


#### 💻 CONFIGURACION CISCO IOS-XE:

```cisco
segment-routing mpls
 connected-prefix-sid-map
  address-family ipv4
   10.255.0.1/32 index 1 range 1    ! Asigna el Prefix-SID etiqueta 16001
  exit-address-family
exit

router ospf 1
 segment-routing mpls
 segment-routing area 0
exit
```


#### 🔍 Verificación:

```cisco
R1# show segment-routing mpls connected-prefix-sid-map
```



## EJEMPLO 136: SEGMENT ROUTING SRv6 SOBRE IPv6 NATIVO


> 🏢 **ESCENARIO REAL:**
La vanguardia de las telecomunicaciones globales: Transporte de paquetes de extremo
a extremo sobre direcciones IPv6 de 128 bits sin utilizar etiquetas MPLS.


#### 💻 CONFIGURACION CISCO:

```cisco
segment-routing srv6
 encapsulation
  source-address 2001:DB8:CORE::1
 locators
  locator LOC1
   prefix 2001:DB8:AA01::/64
  exit
 exit
exit
```


#### 🔍 Verificación:

```cisco
R1# show segment-routing srv6 locator
```



## EJEMPLO 137: CARRIER SUPPORTING CARRIER (CSC)


> 🏢 **ESCENARIO REAL:**
Un proveedor de Internet regional pequeno contrata transporte a un operador global
mayor (Tier-1) para conectar sus propios routers PoP mediante etiquetas MPLS jerarquicas.


#### 💻 CONFIGURACION CISCO (ROUTER PE DEL TIER-1):

```cisco
interface GigabitEthernet0/0/2
 description CLIENTE_ISP_REGIONAL
 vrf forwarding ISP_REGIONAL
 mpls ip                             ! Habilita MPLS en la interfaz VRF hacia el cliente
 no shutdown
exit
```



## EJEMPLO 138: INTER-AS MPLS VPN OPCION A (BACK-TO-BACK VRF)


> 🏢 **ESCENARIO REAL:**
Conectar las redes MPLS de dos Carriers diferentes (Carrier A en Mexico y Carrier B
en Estados Unidos). En la frontera, ambos routers ASBR se conectan mediante cables
subinterfaz (VLANs 802.1Q) actuando como CE y PE mutuamente.


#### 🌐 DIAGRAMA:

```text
  [CARRIER A: ASBR 1] <=== Subinterfaces 802.1Q (Sin MPLS en el cruce) ===> [CARRIER B: ASBR 2]
```


#### 💻 CONFIGURACION CISCO (ASBR 1):

```cisco
interface GigabitEthernet0/1.100
 description CRUCE_INTER_AS_VRF_CLIENTE1
 encapsulation dot1Q 100
 vrf forwarding CLIENTE1
 ip address 192.168.254.1 255.255.255.252
exit

router bgp 65001
 address-family ipv4 vrf CLIENTE1
  neighbor 192.168.254.2 remote-as 65002
 exit-address-family
exit
```



## EJEMPLO 139: INTER-AS MPLS VPN OPCION B (MP-eBGP DIRECTO ENTRE ASBRs)


> 🏢 **ESCENARIO REAL:**
En lugar de crear cientos de subinterfaces, los dos routers ASBR de frontera
establecen una sesion eBGP VPNv4 directa y se intercambian paquetes con etiquetas MPLS.


#### 💻 CONFIGURACION CISCO (ASBR 1):

```cisco
interface GigabitEthernet0/1
 description ENLACE_ASBR_INTER_CARRIER
 mpls ip
 no shutdown
exit

router bgp 65001
 neighbor 192.168.254.2 remote-as 65002
 address-family vpnv4
  neighbor 192.168.254.2 activate
  neighbor 192.168.254.2 send-community extended
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
ASBR1# show bgp vpnv4 unicast all summary
```



## EJEMPLO 140: INTER-AS MPLS VPN OPCION C (eBGP MULTIHOP ENTRE PEs CON BGP-LU)


> 🏢 **ESCENARIO REAL:**
La solucion mas escalable para operadores globales: Los ASBRs solo intercambian
rutas Loopback de los PEs con BGP-LU (Labeled Unicast - RFC 3107). Los routers PE
establecen la sesion MP-eBGP VPNv4 directamente de extremo a extremo sin que los
ASBRs almacenen rutas de clientes.


#### 💻 CONFIGURACION CISCO (ASBR):

```cisco
router bgp 65001
 address-family ipv4
  neighbor 192.168.254.2 activate
  neighbor 192.168.254.2 send-label  ! BGP Labeled Unicast (RFC 3107)
 exit-address-family
exit
```


#### 🔍 Verificación:


## PE1# show mpls forwarding-table | include BGP
