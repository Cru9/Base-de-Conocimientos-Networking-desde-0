# PARTE 8: ENRUTAMIENTO IPv6, DUAL-STACK Y TRANSICION (EJEMPLOS 141 AL 160)

> **ENRUTAMIENTO AVANZADO Y REDES WAN - GUIA PRACTICA DEFINITIVA**


---



## EJEMPLO 141: FUNDAMENTOS DE IPv6: UNICAST-ROUTING Y ASIGNACION ESTATICA /64


> 🏢 **ESCENARIO REAL:**
Habilitar enrutamiento IPv6 en un router Cisco. Por defecto, los routers Cisco
actuan como hosts IPv6 y descartan paquetes de transito hasta habilitar
el comando global obligatorio `ipv6 unicast-routing`.


#### 🌐 DIAGRAMA:

```text
  [PC IPv6: 2001:DB8:ACAD:1::10/64] ===> [ROUTER R1: 2001:DB8:ACAD:1::1/64]
```


#### 💻 CONFIGURACION CISCO IOS-XE:

```cisco
! 1. Comando OBLIGATORIO para habilitar el motor de enrutamiento IPv6
ipv6 unicast-routing

! 2. Configuracion de interfaz con direccion Global Unicast (/64)
interface GigabitEthernet0/0/0
 description LAN_PRODUCCION_IPV6
 ipv6 address 2001:DB8:ACAD:1::1/64
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show ipv6 interface brief
```



## EJEMPLO 142: IPv6 LINK-LOCAL (FE80::) Y GENERACION AUTOMATICA EUI-64


> 🏢 **ESCENARIO REAL:**
Toda interfaz IPv6 requiere una direccion Link-Local (`FE80::/10`) para comunicarse
con vecinos en el mismo cable. Se asigna una Link-Local memorable fija (`fe80::1`)
y se demuestra el uso de EUI-64 (que inserta `FF:FE` en la direccion MAC).


#### 💻 CONFIGURACION CISCO IOS:

```cisco
interface GigabitEthernet0/0/0
 ! Asignacion de Link-Local fija memorable:
 ipv6 address fe80::1 link-local
 ! Asignacion global usando EUI-64 basado en MAC:
 ipv6 address 2001:DB8:ACAD:1::/64 eui-64
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show ipv6 interface GigabitEthernet0/0/0 | include Link-local
```



## EJEMPLO 143: SLAAC (STATELESS ADDRESS AUTOCONFIGURATION) CON NDP (RA y RS)


> 🏢 **ESCENARIO REAL:**
Las computadoras de los empleados se autoconfiguran su direccion IPv6 sin necesidad
de servidor DHCP. El router anuncia periodicamente mensajes Router Advertisement (RA)
conteniendo el prefijo de red mediante el protocolo NDP (Neighbor Discovery Protocol).


#### 💻 CONFIGURACION CISCO IOS:

```cisco
interface GigabitEthernet0/0/0
 description LAN_USUARIOS_SLAAC
 ipv6 address 2001:DB8:10::1/64
 ! Por defecto al poner IP, el router envia RAs con banderas M=0 y O=0 (SLAAC Puro)
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show ipv6 nd interface GigabitEthernet0/0/0
```



## EJEMPLO 144: SERVIDOR DHCPv6 STATELESS (DNS Y DOMINIO PARA SLAAC)


> 🏢 **ESCENARIO REAL:**
SLAAC entrega direccion IP y gateway, pero tradicionalmente no entregaba servidores
DNS. Se configura un DHCPv6 "Stateless" que entrega solo el DNS y el dominio de busqueda.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! 1. Crear Pool DHCPv6 Stateless
ipv6 dhcp pool POOL_DNS_IPV6
 dns-server 2001:4860:4860::8888    ! DNS Publico de Google
 domain-name empresa.com
exit

! 2. Habilitar la bandera 'O' (Other-Configuration) en los mensajes RA
interface GigabitEthernet0/0/0
 ipv6 dhcp server POOL_DNS_IPV6
 ipv6 nd other-config-flag          ! Le dice a las PCs que busquen el DNS por DHCPv6
exit
```


#### 🔍 Verificación:

```cisco
R1# show ipv6 dhcp pool
```



## EJEMPLO 145: SERVIDOR DHCPv6 STATEFUL (ENTREGA Y CONTROL DE DIRECCIONES)


> 🏢 **ESCENARIO REAL:**
En una empresa que requiere auditar que IP exacta tiene cada computadora, se desactiva
SLAAC forzando la bandera 'M' (Managed Address Flag) para que el router entregue IPs completas.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
ipv6 dhcp pool POOL_STATEFUL
 address prefix 2001:DB8:50::/64 lifetime 86400 43200
 dns-server 2001:4860:4860::8888
exit

interface GigabitEthernet0/0/0
 ipv6 dhcp server POOL_STATEFUL
 ipv6 nd managed-config-flag        ! Bandera M=1 (Fuerza uso de DHCPv6)
 ipv6 nd prefix default no-autoconfig ! Desactiva SLAAC
exit
```


#### 🔍 Verificación:

```cisco
R1# show ipv6 dhcp binding
```



## EJEMPLO 146: RUTA ESTATICA IPv6 DIRECTA Y RUTA POR DEFECTO (::/0)


> 🏢 **ESCENARIO REAL:**
Configurar salida a Internet hacia el proveedor IPv6 mediante la ruta por defecto `::/0`.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! Ruta por defecto hacia el siguiente salto del ISP:
ipv6 route ::/0 2001:DB8:WAN:1::1

! Ruta estatica hacia una sucursal remota:
ipv6 route 2001:DB8:SUCURSAL::/64 2001:DB8:WAN:2::2
```


#### 🔍 Verificación:

```cisco
R1# show ipv6 route static
```



## EJEMPLO 147: OSPFv3 BASICO PARA IPv6 CON ACTIVACION POR INTERFAZ


> 🏢 **ESCENARIO REAL:**
OSPFv3 (RFC 5340) se diseno especificamente para IPv6. Una diferencia critica con OSPFv2:
OSPFv3 NO utiliza comandos `network`; se habilita obligatoriamente en cada interfaz fisica.
Requiere asignar manualmente un Router-ID de 32 bits (en formato decimal con puntos).


#### 🌐 DIAGRAMA:

```text
  [R1 (RID 1.1.1.1)] <===== OSPFv3 Area 0 (Link-Local FE80::) =====> [R2 (RID 2.2.2.2)]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En R1:
router ospfv3 1
 router-id 1.1.1.1
exit

interface GigabitEthernet0/0/1
 description ENLACE_OSPFV3
 ipv6 ospf 1 area 0
 no shutdown
exit

! En R2:
router ospfv3 1
 router-id 2.2.2.2
exit

interface GigabitEthernet0/0/1
 description ENLACE_OSPFV3
 ipv6 ospf 1 area 0
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show ipv6 ospf neighbor
(El vecino se identifica por su Router-ID de 32 bits y su IP Link-Local FE80::).
```



## EJEMPLO 148: OSPFv3 MULTI-AREA CON AREA STUB EN IPv6


> 🏢 **ESCENARIO REAL:**
Segmentar la red IPv6 de la empresa en Area 0 (Core) y Area 10 (Sucursal Stub).


#### 💻 CONFIGURACION CISCO (ROUTER ABR):

```cisco
router ospfv3 1
 router-id 10.0.0.1
 area 10 stub
exit

interface GigabitEthernet0/0/1
 ipv6 ospf 1 area 0
exit
interface GigabitEthernet0/0/2
 ipv6 ospf 1 area 10
exit
```


#### 🔍 Verificación:

```cisco
R_SUCURSAL# show ipv6 route ospf
```

OI  ::/0 [110/11] via FE80::1 (Ruta por defecto inyectada por el Stub).



## EJEMPLO 149: AUTENTICACION IPSEC NATIVA EN OSPFv3


> 🏢 **ESCENARIO REAL:**
OSPFv3 elimino los campos antiguos de contrasena de la cabecera OSPF y utiliza la
suite de seguridad nativa de IPv6 (IPsec ESP / AH) directamente en la interfaz.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
interface GigabitEthernet0/0/1
 ipv6 ospf authentication ipsec spi 1000 sha1 ClaveSeguraOSPFv32026
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show ipv6 ospf interface GigabitEthernet0/0/1 | include IPsec
```



## EJEMPLO 150: MP-BGP PARA IPv6: SESION eBGP IPv6 PURA


> 🏢 **ESCENARIO REAL:**
Establecer un enlace eBGP nativo sobre direccionamiento IPv6 con el Proveedor de Internet.


#### 🌐 DIAGRAMA:

```text
  [EMPRESA: 2001:DB8:1::2] (AS 65001) <===== eBGP IPv6 =====> [ISP: 2001:DB8:1::1] (AS 65002)
```


#### 💻 CONFIGURACION CISCO IOS-XE:

```cisco
router bgp 65001
 bgp router-id 1.1.1.1
 neighbor 2001:DB8:1::1 remote-as 65002
 address-family ipv6 unicast
  neighbor 2001:DB8:1::1 activate
  network 2001:DB8:CORP::/48
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
R1# show bgp ipv6 unicast summary
```



## EJEMPLO 151: ANUNCIO DE PREFIJOS IPv6 PUBLICOS (/48 y /32) EN BGP


> 🏢 **ESCENARIO REAL:**
Los Registros Regionales de Internet (RIR) como LACNIC o ARIN entregan bloques
IPv6 corporativos minimos de tamano `/48`. Se anclan con una ruta Null0 y se anuncian.


#### 💻 CONFIGURACION CISCO:

```cisco
ipv6 route 2001:DB8:1234::/48 Null0 254

router bgp 65001
 address-family ipv6 unicast
  network 2001:DB8:1234::/48
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
R1# show bgp ipv6 unicast 2001:DB8:1234::/48
```



## EJEMPLO 152: TRANSPORTE DE PREFIJOS IPv6 SOBRE SESION BGP IPv4 EXISTENTE


> 🏢 **ESCENARIO REAL:**
Dos routers tienen una sesion BGP establecida sobre IPv4 (`10.0.0.1 <-> 10.0.0.2`),
pero necesitan anunciar rutas IPv6 sin crear una segunda sesion TCP independiente.


#### 💻 CONFIGURACION CISCO:

```cisco
router bgp 65000
 neighbor 10.0.0.2 remote-as 65000
 address-family ipv6 unicast
  neighbor 10.0.0.2 activate
  neighbor 10.0.0.2 route-map SET_IPV6_NEXTHOP in
 exit-address-family
exit

route-map SET_IPV6_NEXTHOP permit 10
 set ipv6 next-hop 2001:DB8:CORE::2
exit
```



## EJEMPLO 153: EIGRP PARA IPv6 EN MODO CLASICO


> 🏢 **ESCENARIO REAL:**
Habilitar EIGRP para IPv6 en una red corporativa. Al igual que OSPFv3, requiere
activacion por interfaz y un Router-ID de 32 bits explicito.


#### 💻 CONFIGURACION CISCO:

```cisco
router eigrp CAMPUS_V6
 ! Se activa el proceso:
 ipv6 router eigrp 100
 eigrp router-id 1.1.1.1
 no shutdown                         ! En EIGRP IPv6 clasico, viene apagado por defecto
exit

interface GigabitEthernet0/0/1
 ipv6 eigrp 100
exit
```


#### 🔍 Verificación:

```cisco
R1# show ipv6 eigrp neighbors
```



## EJEMPLO 154: EIGRP NAMED MODE CON ADDRESS-FAMILY IPv6


> 🏢 **ESCENARIO REAL:**
Gestionar IPv4 e IPv6 bajo la misma jerarquia con EIGRP Named Mode moderno.


#### 💻 CONFIGURACION CISCO IOS-XE:

```cisco
router eigrp GLOBAL_CORP
 address-family ipv6 unicast autonomous-system 200
  af-interface default
   passive-interface
  exit-af-interface
  af-interface GigabitEthernet0/0/1
   no passive-interface
  exit-af-interface
  topology base
  exit-af-topology
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
R1# show ipv6 protocols | include Named
```



## EJEMPLO 155: TUNEL DE TRANSICION IPv6 SOBRE IPv4 MANUAL (6in4 / RFC 4213)


> 🏢 **ESCENARIO REAL:**
Dos oficinas con IPv6 nativo necesitan comunicarse a traves de un proveedor de
Internet que solo proporciona transporte IPv4 tradicional (Protocolo IP 41).


#### 🌐 DIAGRAMA:

```text
  [LAN IPv6] ---> [ROUTER 1: IP WAN 203.0.113.2] === Tunel 6in4 (IP 41) ===> [ROUTER 2: 198.51.100.2] ---> [LAN IPv6]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En Router 1:
interface Tunnel10
 description TUNEL_6IN4_HACIA_SEDE2
 no ip address
 ipv6 address 2001:DB8:TUNEL::1/64
 tunnel source GigabitEthernet0/1
 tunnel destination 198.51.100.2
 tunnel mode ipv6ip                  ! Modo 6in4 estandar (Protocolo IP 41)
 no shutdown
exit

ipv6 route 2001:DB8:SEDE2::/64 Tunnel10
```


#### 🔍 Verificación:

```cisco
R1# ping 2001:DB8:TUNEL::2
```



## EJEMPLO 156: TUNEL AUTOMATICO 6to4 (2002::/16)


> 🏢 **ESCENARIO REAL:**
Mapeo automatico de direcciones IPv4 publicas a direcciones IPv6 utilizando el prefijo
estandar especial `2002::/16` sin requerir configuracion de tuneles punto a punto fijos.


#### 💻 CONFIGURACION CISCO:

```cisco
interface Tunnel20
 no ip address
 ipv6 address 2002:CB00:7102::1/48   ! CB00:7102 es la conversion hexa de 203.0.113.2
 tunnel source GigabitEthernet0/1
 tunnel mode ipv6ip 6to4
exit

ipv6 route 2002::/16 Tunnel20
```



## EJEMPLO 157: TUNEL GRE TRANSPORTANDO TRAFICO IPv6 NATIVO


> 🏢 **ESCENARIO REAL:**
Utilizar encapsulacion GRE multiprotocolo para transportar tanto IPv4 como IPv6
simultaneamente en la misma interfaz de tunel (Dual-Stack).


#### 💻 CONFIGURACION CISCO:

```cisco
interface Tunnel0
 ip address 10.255.0.1 255.255.255.252
 ipv6 address 2001:DB8:TUNEL::1/64
 tunnel source GigabitEthernet0/1
 tunnel destination 198.51.100.2
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# ping ipv6 2001:DB8:TUNEL::2
```



## EJEMPLO 158: VPN IPSEC VTI CON DIRECCIONAMIENTO IPv6 PURO


> 🏢 **ESCENARIO REAL:**
Construir un tunel IPsec cifrado punto a punto utilizando direcciones IPv6 de extremo a extremo.


#### 💻 CONFIGURACION CISCO IOS-XE:

```cisco
crypto ikev2 proposal IKEV2_PROP_V6
 encryption aes-cbc-256
 integrity sha256
 group 14
exit

crypto ikev2 profile PROF_V6
 match identity remote address 2001:DB8:WAN::2 128
 authentication remote pre-share
 authentication local pre-share
 keyring local KR_V6
exit

interface Tunnel1
 ipv6 address 2001:DB8:VTI::1/64
 tunnel source GigabitEthernet0/1
 tunnel destination 2001:DB8:WAN::2
 tunnel mode ipsec ipv6
 tunnel protection ipsec profile PROF_IPSEC_V6
 no shutdown
exit
```



## EJEMPLO 159: ENRUTAMIENTO IPv6 EN ROUTERS HUAWEI VRP (OSPFv3 Y BGP4+)


> 🏢 **ESCENARIO REAL:**
Habilitar OSPFv3 y BGP para IPv6 en routers de campus Huawei.


#### 💻 CONFIGURACION HUAWEI VRP:

```text
# 1. Habilitar IPv6 globalmente
ipv6
#
# 2. Interfaz con IPv6
interface GigabitEthernet0/0/1
 ipv6 enable
 ipv6 address 2001:DB8:1::1 64
#
# 3. OSPFv3 en Huawei
ospfv3 1
 router-id 1.1.1.1
#
interface GigabitEthernet0/0/1
 ospfv3 1 area 0
#
# 4. BGP4+ en Huawei
bgp 65001
 router-id 1.1.1.1
 peer 2001:DB8:1::2 as-number 65002
 #
 ipv6-family unicast
  peer 2001:DB8:1::2 enable
  network 2001:DB8:CORP:: 48
quit
```


#### 🔍 Verificación:

```cisco
<ROUTER_HW> display ospfv3 peer
<ROUTER_HW> display bgp ipv6 routing-table
```



## EJEMPLO 160: SEGURIZACION IPv6: ACLS Y PROTECCION RA GUARD


> 🏢 **ESCENARIO REAL:**
Prevenir ataques donde un atacante en la LAN conecta un router falso y envia
anuncios RA falsificados (Rogue RA) para secuestrar el gateway (Man-in-the-Middle).
IPv6 RA Guard en los switches bloquea mensajes RA en los puertos de acceso de usuarios.


#### 💻 CONFIGURACION CISCO (SWITCH):

```cisco
ipv6 nd raguard policy POLITICA_ANTI_ROGUE_RA
 device-role host                   ! Solo permite hosts en estos puertos, no routers
exit

interface FastEthernet0/1
 description PUERTO_USUARIO_PC
 ipv6 nd raguard attach-policy POLITICA_ANTI_ROGUE_RA
 no shutdown
exit
```


#### 🔍 Verificación:


## SWITCH# show ipv6 snooping
