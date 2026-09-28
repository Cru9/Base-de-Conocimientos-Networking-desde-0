# PARTE 5: CASOS AVANZADOS, VPNs, HA Y PRODUCCION REAL (EJEMPLOS 081 AL 100)

> **ENRUTAMIENTO AVANZADO Y REDES WAN - GUIA PRACTICA DEFINITIVA**


---



## EJEMPLO 081: VRF LITE PARA AISLAMIENTO LOGICO CORPORATIVO vs INVITADOS


> 🏢 **ESCENARIO REAL:**
En una empresa financiera, los visitantes en la red Wi-Fi de Invitados y los cajeros
bancarios corporativos comparten el mismo router fisico. Para garantizar cumplimiento
PCI-DSS, se crean dos tablas de enrutamiento virtuales (VRFs) 100% aisladas.


#### 🌐 DIAGRAMA:

```text
                   [ROUTER FISICO R1]
            +------------------------------+
            |  VRF CORPORATIVO (LAN .10)   | ---> Hacia Datacenter Bancario
            +------------------------------+
            |  VRF INVITADOS   (LAN .99)   | ---> Salida directa a Internet
            +------------------------------+
```


#### 💻 CONFIGURACION CISCO IOS-XE:

```cisco
! 1. Definicion de VRFs
vrf definition CORP
 rd 65000:10
 address-family ipv4
 exit-address-family
exit

vrf definition INVITADOS
 rd 65000:99
 address-family ipv4
 exit-address-family
exit

! 2. Asignacion a Interfaces
interface GigabitEthernet0/0/1
 description LAN_CAJEROS_BANCARIOS
 vrf forwarding CORP
 ip address 10.10.10.1 255.255.255.0
 no shutdown
exit

interface GigabitEthernet0/0/2
 description LAN_WIFI_INVITADOS
 vrf forwarding INVITADOS
 ip address 192.168.99.1 255.255.255.0
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip route vrf CORP
R1# show ip route vrf INVITADOS
(Cada VRF tiene su propia tabla de enrutamiento independiente).
```



## EJEMPLO 082: ENRUTAMIENTO INTER-VRF MEDIANTE RUTAS ESTATICAS


> 🏢 **ESCENARIO REAL:**
Los usuarios en la VRF INVITADOS necesitan acceder a un servidor DNS compartido
que reside en la VRF CORP (`10.10.10.53`). Se crea una ruta estatica cruzada.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
ip route vrf INVITADOS 10.10.10.53 255.255.255.255 GigabitEthernet0/0/1 10.10.10.53
```


#### 🔍 Verificación:

```cisco
R1# show ip route vrf INVITADOS 10.10.10.53
```



## EJEMPLO 083: TUNEL GRE BASICO PUNTO A PUNTO SIN CIFRAR SOBRE INTERNET


> 🏢 **ESCENARIO REAL:**
Interconectar dos sedes a traves de Internet para transportar paquetes IP con
encabezados encapsulados mediante protocolo IP 47 (Generic Routing Encapsulation).


#### 🌐 DIAGRAMA:

```text
  [R1: 203.0.113.2] <======= Tunel GRE (172.16.0.1 <-> 172.16.0.2) =======> [R2: 198.51.100.2]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En R1:
interface Tunnel0
 ip address 172.16.0.1 255.255.255.252
 tunnel source GigabitEthernet0/1
 tunnel destination 198.51.100.2
 no shutdown
exit

! En R2:
interface Tunnel0
 ip address 172.16.0.2 255.255.255.252
 tunnel source GigabitEthernet0/1
 tunnel destination 203.0.113.2
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# ping 172.16.0.2
```



## EJEMPLO 084: TUNEL GRE SOBRE IPSEC (GRE OVER IPSEC) CON OSPF


> 🏢 **ESCENARIO REAL:**
Como IPsec puro clasico no transporta Multicast, no puede correr OSPF. Se encapsula
el trafico OSPF dentro de un tunel GRE y luego se cifra con un perfil IPsec.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
crypto ipsec profile PROF_IPSEC
 set transform-set TS_IPSEC
exit

interface Tunnel0
 ip address 172.16.0.1 255.255.255.252
 tunnel source GigabitEthernet0/1
 tunnel destination 198.51.100.2
 tunnel protection ipsec profile PROF_IPSEC   ! Cifra el GRE automaticamente
 ip ospf 1 area 0
exit
```


#### 🔍 Verificación:

```cisco
R1# show crypto session
R1# show ip ospf neighbor
```



## EJEMPLO 085: VPN IPSEC VTI (VIRTUAL TUNNEL INTERFACE) CON IKEv2


> 🏢 **ESCENARIO REAL:**
El estandar corporativo moderno: Tunel Route-Based directo sin necesidad de GRE.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
interface Tunnel1
 description TUNEL_IPSEC_VTI
 ip address 10.255.1.1 255.255.255.252
 tunnel source GigabitEthernet0/1
 tunnel destination 198.51.100.2
 tunnel mode ipsec ipv4                  ! Modo VTI nativo
 tunnel protection ipsec profile IPSEC_VTI_PROFILE
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show crypto ikev2 sa
R1# show crypto ipsec sa
```



## EJEMPLO 086: AJUSTE DE MTU Y TCP MSS CLAMPING EN TUNELES VPN


> 🏢 **ESCENARIO REAL:**
Resolver la clasica falla donde el `ping` funciona a traves del tunel VPN, pero las
paginas web de la empresa y ERP se congelan debido al overhead de cifrado ESP.


#### 💻 CONFIGURACION CISCO IOS (EN INTERFAZ DE TUNEL):

```cisco
interface Tunnel1
 ip mtu 1400
 ip tcp adjust-mss 1360
exit
```


#### 🔍 Verificación:

```cisco
R1# show interfaces Tunnel1 | include MTU
```



## EJEMPLO 087: REDUNDANCIA DE GATEWAY LAN CON HSRP EN ROUTERS CISCO


> 🏢 **ESCENARIO REAL:**
Dos routers comparten una direccion IP de Gateway Virtual (`192.168.1.1`). Si R1 falla,
R2 toma el control del Gateway en 3 segundos sin intervencion humana.


#### 🌐 DIAGRAMA:

```text
  [ROUTER 1: 192.168.1.2 (Active)]      [ROUTER 2: 192.168.1.3 (Standby)]
                 \                              /
                  \                            /
```

             IP VIRTUAL GATEWAY HSRP: 192.168.1.1 (VIP)
                                |
                     [SWITCH ACCESO / PCs]


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En R1 (Router Principal):
interface GigabitEthernet0/0
 ip address 192.168.1.2 255.255.255.0
 standby 1 ip 192.168.1.1
 standby 1 priority 110    ! Mayor prioridad = Active
 standby 1 preempt         ! Recuperar liderazgo al revivir
 no shutdown
exit

! En R2 (Router Secundario):
interface GigabitEthernet0/0
 ip address 192.168.1.3 255.255.255.0
 standby 1 ip 192.168.1.1
 standby 1 priority 100    ! Standby
 standby 1 preempt
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show standby brief
(R1 debe decir 'Active' y R2 debe decir 'Standby').
```



## EJEMPLO 088: REDUNDANCIA CON VRRP v2/v3 Y TRACKING DE INTERFAZ WAN


> 🏢 **ESCENARIO REAL:**
Utilizar el protocolo abierto VRRP con reduccion automatica de prioridad si el enlace
hacia el ISP se desconecta, forzando la conmutacion al router de respaldo.


#### 💻 CONFIGURACION CISCO IOS (EN R1):

```cisco
track 1 interface GigabitEthernet0/1 line-protocol

interface GigabitEthernet0/0
 ip address 192.168.1.2 255.255.255.0
 vrrp 1 ip 192.168.1.1
 vrrp 1 priority 120
 vrrp 1 preempt
 vrrp 1 track 1 decrement 30   ! Si cae la WAN, prioridad baja de 120 a 90
exit
```


#### 🔍 Verificación:

```cisco
R1# show vrrp brief
```



## EJEMPLO 089: BALANCEO DE CARGA EN GATEWAY LAN CON GLBP


> 🏢 **ESCENARIO REAL:**
A diferencia de HSRP/VRRP donde un router esta dormido, GLBP (Gateway Load Balancing
Protocol) entrega diferentes direcciones MAC virtuales a las PCs por round-robin,
permitiendo que ambos routers procesen trafico LAN simultaneamente.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
interface GigabitEthernet0/0
 ip address 192.168.1.2 255.255.255.0
 glbp 1 ip 192.168.1.1
 glbp 1 load-balancing round-robin
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show glbp brief
```



## EJEMPLO 090: CONMUTACION AUTOMATICA FIBRA A 5G CON IP SLA Y TRACK


> 🏢 **ESCENARIO REAL:**
Si el carrier de fibra sufre un corte en la calle pero el puerto local sigue encendido,
un ping continuo (ICMP Echo) hacia `8.8.8.8` detecta la caida y conmuta al enlace 5G.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
ip sla 1
 icmp-echo 8.8.8.8 source-interface GigabitEthernet0/1
 frequency 5
 timeout 1000
exit
ip sla schedule 1 life forever start-time now

track 10 ip sla 1 reachability
exit

ip route 0.0.0.0 0.0.0.0 203.0.113.1 track 10  ! Ruta Primaria monitoreada (AD 1)
ip route 0.0.0.0 0.0.0.0 198.18.1.1 50         ! Ruta Flotante 5G (AD 50)
```


#### 🔍 Verificación:

```cisco
R1# show track 10
```



## EJEMPLO 091: DMVPN FASE 1 (HUB-AND-SPOKE CON mGRE Y NHRP)


> 🏢 **ESCENARIO REAL:**
Conectar 50 sucursales a un Hub central mediante una unica interfaz mGRE. Todo el
trafico de las sucursales viaja hacia el Hub.


#### 💻 CONFIGURACION CISCO IOS (EN EL HUB):

```cisco
interface Tunnel0
 ip address 172.16.100.1 255.255.255.0
 ip nhrp network-id 1
 tunnel source GigabitEthernet0/1
 tunnel mode gre multipoint
 tunnel protection ipsec profile PROF_DMVPN
exit
```



## EJEMPLO 092: DMVPN FASE 2 CON ATAJOS SPOKE-TO-SPOKE DIRECTOS


> 🏢 **ESCENARIO REAL:**
Permitir que la Sucursal A hable directamente con la Sucursal B a traves de Internet
sin que los paquetes de datos atraviesen el Hub Central.


#### 💻 CONFIGURACION CISCO IOS (EN LOS SPOKES):

```cisco
interface Tunnel0
 ip address 172.16.100.10 255.255.255.0
 ip nhrp network-id 1
 ip nhrp map 172.16.100.1 203.0.113.1
 ip nhrp nhs 172.16.100.1
 tunnel source GigabitEthernet0/1
 tunnel mode gre multipoint          ! Modo multipunto en los spokes activa Fase 2
 tunnel protection ipsec profile PROF_DMVPN
exit
```



## EJEMPLO 093: DMVPN FASE 3 CON NHRP REDIRECT Y SHORTCUT


> 🏢 **ESCENARIO REAL:**
En redes de cientos de sucursales, la Fase 3 utiliza `ip nhrp redirect` en el Hub e
`ip nhrp shortcut` en los Spokes para instalar rutas CEF dinamicas en hardware.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En el Hub:
interface Tunnel0
 ip nhrp redirect
exit

! En los Spokes:
interface Tunnel0
 ip nhrp shortcut
exit
```


#### 🔍 Verificación:

```cisco
SPOKE# show ip route | include %
(Las rutas Spoke-to-Spoke dinamicas aparecen marcadas con el simbolo '%').
```



## EJEMPLO 094: REDUNDANCIA DUAL-HUB EN DATACENTER CON BGP


> 🏢 **ESCENARIO REAL:**
Dos routers Hub en el Datacenter (Hub 1 y Hub 2). Cada sucursal levanta dos tuneles
simultaneos y corre BGP con el comando `maximum-paths 2` para balanceo y redundancia.


#### 💻 CONFIGURACION CISCO IOS (EN SPOKE):

```cisco
router bgp 65000
 neighbor 172.16.1.1 remote-as 65000   ! Hub 1
 neighbor 172.16.2.1 remote-as 65000   ! Hub 2
 maximum-paths ibgp 2
exit
```



## EJEMPLO 095: SUCURSAL CON IP DINAMICA CONECTANDOSE CON IKEv2 WILDCARD


> 🏢 **ESCENARIO REAL:**
El Hub Central tiene IP publica fija. La sucursal tiene un modem 4G con IP dinamica.
El Hub valida la conexion mediante autenticacion basada en FQDN.


#### 💻 CONFIGURACION CISCO IOS (EN EL HUB):

```cisco
crypto ikev2 keyring KR_GLOBAL
 peer SUCURSAL_TIENDA
  fqdn tienda45.empresa.com
  pre-shared-key ClaveTiendaSegura2026!
exit
```



## EJEMPLO 096: INTEROPERABILIDAD CISCO (CORE) <-> HUAWEI (SUCURSAL)


> 🏢 **ESCENARIO REAL:**
Conectar un Router Cisco Catalyst 8000 en el corporativo con un Router Huawei AR650
en la sucursal mediante un tunel IPsec VTI estandarizado.

PARAMETROS COMUNES OBLIGATORIOS:
- IKEv2, AES-256, SHA-256, DH Group 14, PSK: ClaveInteroperable2026!, MTU 1400.

VERIFICACION CRUZADA:
CISCO# show crypto ikev2 sa (Status: READY)
HUAWEI> display ike sa (Flags: RD|ST)



## EJEMPLO 097: POLICY-BASED ROUTING (PBR) PARA DESVIO DE TRAFICO


> 🏢 **ESCENARIO REAL:**
Desviar las llamadas telefonicas de VoIP (puertos UDP 5060 y RTP) por el enlace WAN
de fibra dedicado, y enviar la navegacion web por el enlace barato de banda ancha.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
access-list 150 permit udp any any range 16384 32767 ! Trafico de Voz RTP

route-map MAPA_PBR permit 10
 match ip address 150
 set ip next-hop 10.1.1.2     ! Salir por Fibra VIP
exit

interface GigabitEthernet0/0
 description LAN_INTERNA
 ip policy route-map MAPA_PBR
exit
```


#### 🔍 Verificación:

```cisco
R1# show route-map MAPA_PBR
```



## EJEMPLO 098: CALIDAD DE SERVICIO (QoS): COLA PRIORITARIA LLQ PARA VOIP


> 🏢 **ESCENARIO REAL:**
Garantizar 20 Mbps con cero latencia y cero jitter para voz sobre IP en un enlace
WAN de 100 Mbps, shapeando el resto del trafico de datos.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
class-map match-any CLASE_VOZ
 match ip dscp ef
exit

policy-map POLITICA_WAN_QOS
 class CLASE_VOZ
  priority 20000      ! 20 Mbps de Low Latency Queueing (LLQ)
 class class-default
  fair-queue
exit

interface GigabitEthernet0/1
 service-policy output POLITICA_WAN_QOS
exit
```


#### 🔍 Verificación:

```cisco
R1# show policy-map interface GigabitEthernet0/1
```



## EJEMPLO 099: MITIGACION DE INESTABILIDAD WAN CON IP EVENT DAMPENING


> 🏢 **ESCENARIO REAL:**
Un cablemodem sufre 30 desconexiones por minuto (flapping), volviendo locas las
tablas de enrutamiento OSPF y BGP. `dampening` suprime la interfaz temporalmente.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
interface GigabitEthernet0/0/1
 dampening 10 750 2000 40   ! Suprime la interfaz tras caidas repetitivas
exit
```


#### 🔍 Verificación:

```cisco
R1# show dampening interface GigabitEthernet0/0/1
```



## EJEMPLO 100: ARQUITECTURA INTEGRAL DE RED CORPORATIVA MULTI-SITIO


> 🏢 **ESCENARIO REAL:**
Integracion de fin de curso de un Datacenter Empresarial completo:
1. Switches Core L3 en Stack con enrutamiento OSPF interno.
2. Routers Edge WAN redundantes con sesiones BGP Multihoming (AS 65000 a dos ISPs).
3. Redundancia de Gateway LAN mediante VRRP y BFD.
4. Conectividad hacia 50 sucursales mediante DMVPN Fase 3 con cifrado IPsec IKEv2.
5. Control de trafico con BGP Communities y Calidad de Servicio (QoS).

DIAGRAMA INTEGRAL:
```text
                  +-----------------------+
                  |   INTERNET GLOBAL     |
                  +---+---------------+---+
                      |               |
             (ISP-1)  |               | (ISP-2)
                      v               v
                +-----+----+     +----+-----+
                | EDGE R1  |=====| EDGE R2  | (BGP AS 65000 + BFD + Multihoming)
                +-----+----+     +----+-----+
                      |               |
                      +-------+-------+
                              | (IPsec DMVPN Hub 1 & Hub 2)
                              v
                  +-----------+-----------+
                  |  SWITCH CORE STACK L3 | (OSPF Area 0 Backbone)
                  +-----------+-----------+
                              |
               +--------------+--------------+
               |                             |
               v                             v
       [DATACENTER SERVIDORES]     [50 SUCURSALES REMOTAS]
       (VLAN 10, 20, 30 en SVIs)   (Spokes con OSPF Stub y BGP)

RESUMEN DE COMANDOS DE DIAGNOSTICO DE RED GENERAL:
# show ip route summary
# show ip ospf neighbor
# show ip bgp summary
# show crypto session detail
# show dmvpn
```


## # show bfd neighbors
