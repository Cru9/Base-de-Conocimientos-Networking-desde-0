# 14. MANUAL DE ALTA DISPONIBILIDAD WAN: BALANCEO DE CARGA (ECMP),

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**

> *DUAL-HUB REDUNDANTE Y CONMUTACION SUBSEGUNDO CON BFD (CISCO Y HUAWEI)*


---



## 1. ¿POR QUE EL MODELO SINGLE-HUB / SINGLE-ISP ES UN RIESGO CATASTROFICO?

En entornos corporativos criticos (banca, logistica, salud, retail de alto volumen),
el costo de inactividad (Downtime) de la red WAN puede costar decenas de miles de
dolares por minuto.
Si una arquitectura WAN depende de:
- Un unico router central (Single Hub) en el Datacenter.
- O un unico proveedor de Internet (Single ISP) en cada sitio.

Cualquier contingencia fisica en la calle (un camion que rompe postes de fibra optica,
mantenimiento no programado del carrier, falla de la fuente de poder del router central)
dejara a TODA la organizacion completamente aislada.

LA SOLUCION EMPRESARIAL INTEGRAL:
Disenar una arquitectura WAN de Alta Disponibilidad (HA - High Availability) que combine:
1. Redundancia de Hardware y Sitio: Dos routers Hub en la Sede Central (Hub 1 y Hub 2)
   operando en modo Activo/Activo o Activo/Pasivo con VRRP/HSRP en el lado LAN.
2. Redundancia de Transporte WAN (Dual-ISP): Cada sucursal dispone de dos proveedores
   diferentes (ej. ISP-1 Fibra Optica dedicado + ISP-2 Microondas o Celular 5G).
3. Balanceo de Carga de Capa 3 (ECMP - Equal-Cost Multi-Path): Aprovechar ambos enlaces
   simultaneamente para duplicar el rendimiento agregado en condiciones normales.
4. Deteccion de Fallas en Subsegundo con BFD (Bidirectional Forwarding Detection):
   Conmutar el trafico de una ruta caida en menos de 150 a 300 milisegundos sin cortar
   llamadas telefonicas de VoIP ni sesiones de bases de datos.



## 2. PRINCIPIOS DE BALANCEO DE CARGA (LOAD BALANCING) EN REDES IPSEC

En una red con enlaces redundantes, existen dos estrategias de diseno:


### A) ACTIVO / PASIVO (FAILOVER CLASICO CON RUTAS FLOTANTES O LOCAL-PREF):

   - Todo el trafico viaja por el Enlace Primario (Fibra 500 Mbps).
   - El Enlace Secundario (5G 100 Mbps) permanece ocioso al 0% de uso.
   - Desventaja financiera: La empresa paga mensualmente por un enlace de respaldo
     que solo se utiliza cuando el principal falla.


### B) ACTIVO / ACTIVO CON ECMP (EQUAL-COST MULTI-PATH - ESTANDAR MODERNO):

   - Ambos enlaces estan activos y transmiten paquetes simultaneamente.
   - El router distribuye el trafico a traves de dos o mas interfaces de tunel
     que tienen exactamente la misma metrica de enrutamiento.

¿Como reparte el router el trafico sin desordenar los paquetes?
- Hashing por Flujo (Per-Flow Load Balancing):
  * El router calcula un algoritmo hash matematico basado en la 5-Tupla del paquete:
    [IP Origen, IP Destino, Protocolo Capa 4, Puerto Origen, Puerto Destino].
  * Todos los paquetes pertenecientes a una misma sesion (ej. una descarga de archivo
    o una llamada VoIP especifica) viajan SIEMPRE por el mismo enlace.
  * Esto GARANTIZA que no haya entrega de paquetes desordenados (Packet Reordering),
    lo cual danaria el rendimiento de las conexiones TCP.
  * Diferentes empleados o aplicaciones se distribuyen equitativamente entre los enlaces.

EL PROBLEMA DEL ENRUTAMIENTO ASIMETRICO (ASYMMETRIC ROUTING):
- Si el paquete de ida sale por ISP-1 (Tunel 1) y el paquete de regreso entra por ISP-2 (Tunel 2),
  en routers de routing puro no hay problema.
- Sin embargo, si en el trayecto hay Firewalls con inspeccion de estado (Stateful Inspection),
  el firewall del Tunel 2 no vera el paquete inicial SYN y descartara la conexion con TCP RST.
- REGLA DE DISENO: En topologias Activo/Activo con firewalls, se debe asegurar retorno
  simetrico o permitir balanceo mediante sesiones coordinadas (Cluster HA / ASR).



## 3. DETECCION ULTRA-RAPIDA DE CAIDAS CON BFD (BIDIRECTIONAL FORWARDING DETECTION)

¿Por que los temporizadores estandar de BGP u OSPF son inaceptables en alta disponibilidad?
- BGP por defecto: Keepalive de 60 segundos, Hold-Time de 180 segundos.
  ¡Si un enlace de fibra se corta a nivel logico, BGP puede tardar hasta 3 MINUTOS en enterarse!
- OSPF por defecto: Hello de 10 seg, Dead Timer de 40 segundos (40 segundos de caida total).
- IPsec DPD: Suele tardar de 15 a 30 segundos.

LA SOLUCION: BFD (RFC 5880)
- BFD es un protocolo ultra-ligero que se ejecuta en el hardware / plano de datos.
- Envia micro-paquetes de sondeo cada 50 o 100 milisegundos.
- Se vincula directamente a BGP, OSPF o rutas estaticas.
- Formula de Deteccion de Caida:
  `Tiempo de Deteccion = Intervalo de Transmision (min_tx) * Multiplicador`
  Ejemplo: `interval 100 min_rx 100 multiplier 3`
  `100 ms * 3 = ¡300 MILISEGUNDOS!`
- Si un cable se rompe, a los 300 ms BFD le avisa a BGP/OSPF, y la tabla de enrutamiento
  conmuta todo el trafico a la ruta de respaldo de forma totalmente imperceptible.



## 4. ARQUITECTURA DE LA TOPOLOGIA: DUAL-HUB DUAL-ISP CON BALANCEO Y FAILOVER


DISENO DE LA TOPOLOGIA EMPRESARIAL:
- Sede Central (Datacenter): Cuenta con dos routers de borde independientes:
  * R_HUB_1 (Router Principal Sede Maestra - IP WAN: 203.0.113.10)
  * R_HUB_2 (Router Secundario Sede Maestra - IP WAN: 203.0.113.20)
  * Ambos comparten una direccion IP Virtual de Gateway en la LAN Core mediante VRRP/HSRP.
- Sucursal Remota (Branch Office): Cuenta con un router de borde con dos conexiones a Internet:
  * Enlace 1: ISP-A Fibra Optica (IP WAN: 198.51.100.2)
  * Enlace 2: ISP-B Microondas / Radio (IP WAN: 198.18.50.2)
- Modelo de Malla de Tuneles (Dual-Tunnel Active/Active):
  * Tunel 1: Sucursal (via ISP-A) <====== IPsec ======> R_HUB_1
  * Tunel 2: Sucursal (via ISP-B) <====== IPsec ======> R_HUB_2
  * Ambos tuneles activos simultaneamente con sesiones BGP y BFD activado.
  * Balanceo de carga de salida y entrada mediante BGP Multipath (`maximum-paths 2`).

DIAGRAMA VISUAL DE LA TOPOLOGIA:

```text
             +-----------------------------------------------------------+
             |               SEDE CENTRAL (DATACENTER CORE)              |
             |                   LAN Core: 10.0.0.0/16                   |
             |       VRRP Gateway Virtual: 10.0.0.1 (Hub1-Master/Hub2)   |
             +-------------+-------------------------------+-------------+
                           |                               |
             +-------------+-------------+   +-------------+-------------+
             |         R_HUB_1           |   |         R_HUB_2           |
             |       (CISCO CORE)        |   |       (CISCO CORE)        |
             | WAN: 203.0.113.10 (Gi0/1) |   | WAN: 203.0.113.20 (Gi0/1) |
             | IP Tunel 1: 172.16.1.1/30 |   | IP Tunel 2: 172.16.2.1/30 |
             | BGP AS 65000 (Hub 1)      |   | BGP AS 65000 (Hub 2)      |
             +-------------+-------------+   +-------------+-------------+
                           |                               |
                           +---------------+---------------+
                                           |
                                           v
                         +-----------------------------------+
                         |       RED DE INTERNET (ISPs)      |
                         |   (Nube de Transporte Publico)    |
                         +-----------------+-----------------+
                                           |
                           +---------------+---------------+
                           |                               |
          Uplink ISP-A (Fibra)                             Uplink ISP-B (Radio)
          198.51.100.2 (Gi0/1)                             198.18.50.2 (Gi0/2)
                           |                               |
             +-------------+-------------------------------+-------------+
             |               SUCURSAL REMOTA (R_SUCURSAL)                |
             |               (CISCO IOS-XE / HUAWEI AR)                  |
             | IP Tunel 1: 172.16.1.2/30  |  IP Tunel 2: 172.16.2.2/30   |
             | BGP AS 65000 (Multipath 2 - Balanceo ECMP)               |
             | LAN Sucursal: 192.168.10.0/24                             |
             +-----------------------------------------------------------+
```

TABLA DE DIRECCIONAMIENTO COMPLETO:

| Dispositivo | Interfaz | Direccion IP | Mascara | Rol / Descripcion |
| :--- | :--- | :--- | :--- | :--- |
| R_HUB_1 | Gi0/0 | 10.0.0.2 | 255.255.0.0 | LAN Datacenter (VRRP Master .1) |
| R_HUB_1 | Gi0/1 | 203.0.113.10 | 255.255.255.248 | WAN Publica hacia ISP Hub 1 |
| R_HUB_1 | Tunnel1 | 172.16.1.1 | 255.255.255.252 | Tunel IPsec VTI hacia Sucursal (A) |
| R_HUB_2 | Gi0/0 | 10.0.0.3 | 255.255.0.0 | LAN Datacenter (VRRP Backup .1) |
| R_HUB_2 | Gi0/1 | 203.0.113.20 | 255.255.255.248 | WAN Publica hacia ISP Hub 2 |
| R_HUB_2 | Tunnel2 | 172.16.2.1 | 255.255.255.252 | Tunel IPsec VTI hacia Sucursal (B) |
| R_SUCURSAL | Gi0/0 | 192.168.10.1 | 255.255.255.0 | LAN Usuarios Sucursal |
| R_SUCURSAL | Gi0/1 | 198.51.100.2 | 255.255.255.252 | WAN ISP-A Fibra Primaria |
| R_SUCURSAL | Gi0/2 | 198.18.50.2 | 255.255.255.252 | WAN ISP-B Radio Respaldo |
| R_SUCURSAL | Tunnel1 | 172.16.1.2 | 255.255.255.252 | Tunel IPsec VTI hacia Hub 1 |
| R_SUCURSAL | Tunnel2 | 172.16.2.2 | 255.255.255.252 | Tunel IPsec VTI hacia Hub 2 |




## 5. IMPLEMENTACION PASO A PASO EN CISCO (IOS-XE)



## A) CONFIGURACION EN HUB 1 DE LA SEDE CENTRAL (R_HUB_1 - CISCO):

! 1. Interfaces y Redundancia LAN con HSRP / VRRP
```text
interface GigabitEthernet0/0
 description LAN_DATACENTER_CORE
 ip address 10.0.0.2 255.255.0.0
 vrrp 1 ip 10.0.0.1
 vrrp 1 priority 120   ! Master
 vrrp 1 preempt
 no shutdown
exit

interface GigabitEthernet0/1
 description WAN_INTERNET_ISP_HUB1
 ip address 203.0.113.10 255.255.255.248
 no shutdown
exit
ip route 0.0.0.0 0.0.0.0 203.0.113.14

! 2. Criptografia IKEv2 y IPsec
crypto ikev2 proposal PROP_IKEV2
 encryption aes-cbc-256
 integrity sha256
 group 14
exit

crypto ikev2 policy POL_IKEV2
 proposal PROP_IKEV2
exit

crypto ikev2 keyring KR_HUB1
 peer SUCURSAL_FIBRA
  address 198.51.100.2
  pre-shared-key ClaveCorporativaHA2026!
exit

crypto ikev2 profile PROF_IKEV2_HUB1
 match identity remote address 198.51.100.2 255.255.255.255
 authentication remote pre-share
 authentication local pre-share
 keyring local KR_HUB1
 dpd 10 3 on-demand
exit

crypto ipsec transform-set TS_IPSEC esp-aes 256 esp-sha256-hmac
 mode tunnel
exit

crypto ipsec profile PROF_IPSEC_VTI
 set transform-set TS_IPSEC
 set ikev2-profile PROF_IKEV2_HUB1
 set pfs group14
exit

! 3. Interfaz de Tunel VTI con soporte BFD
interface Tunnel1
 description TUNEL_VTI_HACIA_SUCURSAL_ISPA
 ip address 172.16.1.1 255.255.255.252
 tunnel source GigabitEthernet0/1
 tunnel destination 198.51.100.2
 tunnel mode ipsec ipv4
 tunnel protection ipsec profile PROF_IPSEC_VTI
 ip mtu 1400
 ip tcp adjust-mss 1360
 bfd interval 100 min_rx 100 multiplier 3  ! Deteccion de caida en 300 ms
 no shutdown
exit

! 4. Sesion BGP con aceleracion BFD
router bgp 65000
 bgp router-id 172.16.1.1
 neighbor 172.16.1.2 remote-as 65000
 neighbor 172.16.1.2 description ENLACE_SUCURSAL_A
 neighbor 172.16.1.2 fall-over bfd        ! Conmutacion instantanea al caer BFD
 address-family ipv4
  network 10.0.0.0 mask 255.255.0.0
  neighbor 172.16.1.2 activate
  neighbor 172.16.1.2 next-hop-self
 exit-address-family
exit
```


## B) CONFIGURACION EN HUB 2 DE LA SEDE CENTRAL (R_HUB_2 - CISCO):

```text
interface GigabitEthernet0/0
 description LAN_DATACENTER_CORE
 ip address 10.0.0.3 255.255.0.0
 vrrp 1 ip 10.0.0.1
 vrrp 1 priority 100   ! Backup
 vrrp 1 preempt
 no shutdown
exit

interface GigabitEthernet0/1
 description WAN_INTERNET_ISP_HUB2
 ip address 203.0.113.20 255.255.255.248
 no shutdown
exit
ip route 0.0.0.0 0.0.0.0 203.0.113.24

crypto ikev2 proposal PROP_IKEV2
 encryption aes-cbc-256
 integrity sha256
 group 14
exit

crypto ikev2 policy POL_IKEV2
 proposal PROP_IKEV2
exit

crypto ikev2 keyring KR_HUB2
 peer SUCURSAL_RADIO
  address 198.18.50.2
  pre-shared-key ClaveCorporativaHA2026!
exit

crypto ikev2 profile PROF_IKEV2_HUB2
 match identity remote address 198.18.50.2 255.255.255.255
 authentication remote pre-share
 authentication local pre-share
 keyring local KR_HUB2
 dpd 10 3 on-demand
exit

crypto ipsec transform-set TS_IPSEC esp-aes 256 esp-sha256-hmac
 mode tunnel
exit

crypto ipsec profile PROF_IPSEC_VTI
 set transform-set TS_IPSEC
 set ikev2-profile PROF_IKEV2_HUB2
 set pfs group14
exit

interface Tunnel2
 description TUNEL_VTI_HACIA_SUCURSAL_ISPB
 ip address 172.16.2.1 255.255.255.252
 tunnel source GigabitEthernet0/1
 tunnel destination 198.18.50.2
 tunnel mode ipsec ipv4
 tunnel protection ipsec profile PROF_IPSEC_VTI
 ip mtu 1400
 ip tcp adjust-mss 1360
 bfd interval 100 min_rx 100 multiplier 3
 no shutdown
exit

router bgp 65000
 bgp router-id 172.16.2.1
 neighbor 172.16.2.2 remote-as 65000
 neighbor 172.16.2.2 description ENLACE_SUCURSAL_B
 neighbor 172.16.2.2 fall-over bfd
 address-family ipv4
  network 10.0.0.0 mask 255.255.0.0
  neighbor 172.16.2.2 activate
  neighbor 172.16.2.2 next-hop-self
 exit-address-family
exit
```


## C) CONFIGURACION EN LA SUCURSAL REMOTA (R_SUCURSAL - CISCO):

! 1. Interfaces Fisicas hacia ambos ISPs
```text
interface GigabitEthernet0/0
 description LAN_USUARIOS_SUCURSAL
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit

interface GigabitEthernet0/1
 description WAN_ISP_A_FIBRA
 ip address 198.51.100.2 255.255.255.252
 no shutdown
exit

interface GigabitEthernet0/2
 description WAN_ISP_B_RADIO
 ip address 198.18.50.2 255.255.255.252
 no shutdown
exit

! Rutas estaticas especificas para alcanzar cada Hub por su respectivo ISP
ip route 203.0.113.10 255.255.255.255 198.51.100.1  ! Hub 1 por ISP-A
ip route 203.0.113.20 255.255.255.255 198.18.50.1   ! Hub 2 por ISP-B

! 2. IKEv2 y IPsec
crypto ikev2 proposal PROP_IKEV2
 encryption aes-cbc-256
 integrity sha256
 group 14
exit

crypto ikev2 policy POL_IKEV2
 proposal PROP_IKEV2
exit

crypto ikev2 keyring KR_SPOKE
 peer HUBS_CENTRALES
  address 0.0.0.0 0.0.0.0
  pre-shared-key ClaveCorporativaHA2026!
exit

crypto ikev2 profile PROF_IKEV2_SPOKE
 match identity remote address 0.0.0.0 0.0.0.0
 authentication remote pre-share
 authentication local pre-share
 keyring local KR_SPOKE
 dpd 10 3 on-demand
exit

crypto ipsec transform-set TS_IPSEC esp-aes 256 esp-sha256-hmac
 mode tunnel
exit

crypto ipsec profile PROF_IPSEC_VTI
 set transform-set TS_IPSEC
 set ikev2-profile PROF_IKEV2_SPOKE
 set pfs group14
exit

! 3. Interfaces de Tunel Hacia Hub 1 y Hub 2
interface Tunnel1
 description TUNEL_HACIA_HUB1_FIBRA
 ip address 172.16.1.2 255.255.255.252
 tunnel source GigabitEthernet0/1
 tunnel destination 203.0.113.10
 tunnel mode ipsec ipv4
 tunnel protection ipsec profile PROF_IPSEC_VTI
 ip mtu 1400
 ip tcp adjust-mss 1360
 bfd interval 100 min_rx 100 multiplier 3
 no shutdown
exit

interface Tunnel2
 description TUNEL_HACIA_HUB2_RADIO
 ip address 172.16.2.2 255.255.255.252
 tunnel source GigabitEthernet0/2
 tunnel destination 203.0.113.20
 tunnel mode ipsec ipv4
 tunnel protection ipsec profile PROF_IPSEC_VTI
 ip mtu 1400
 ip tcp adjust-mss 1360
 bfd interval 100 min_rx 100 multiplier 3
 no shutdown
exit

! 4. BGP MULTIPATH: ACTIVACION DEL BALANCEO DE CARGA ECMP
router bgp 65000
 bgp router-id 192.168.10.1
 ! Vecino Hub 1
 neighbor 172.16.1.1 remote-as 65000
 neighbor 172.16.1.1 description UPLINK_HUB1
 neighbor 172.16.1.1 fall-over bfd
 ! Vecino Hub 2
 neighbor 172.16.2.1 remote-as 65000
 neighbor 172.16.2.1 description UPLINK_HUB2
 neighbor 172.16.2.1 fall-over bfd
 !
 address-family ipv4
  network 192.168.10.0
  neighbor 172.16.1.1 activate
  neighbor 172.16.2.1 activate
  ! COMANDO MAESTRO DE BALANCEO ECMP:
  maximum-paths ibgp 2    ! Permite instalar hasta 2 rutas paralelas en la tabla FIB
 exit-address-family
exit
```



## 6. IMPLEMENTACION PASO A PASO EN ROUTERS HUAWEI (VRP)


CASO: LA SUCURSAL CUENTA CON UN ROUTER HUAWEI AR (SERIE AR600 / AR1000 / AR6000)
CONECTADO A AMBOS HUBS CON BFD Y BALANCEO DE CARGA


## A) CONFIGURACION EN ROUTER SUCURSAL (R_SUCURSAL - HUAWEI VRP):

# 1. Interfaces WAN hacia ISP-A e ISP-B
```text
interface GigabitEthernet0/0/0
 description LAN_USUARIOS_SUCURSAL
 ip address 192.168.10.1 255.255.255.0
#
interface GigabitEthernet0/0/1
 description WAN_ISP_A_FIBRA
 ip address 198.51.100.2 255.255.255.252
#
interface GigabitEthernet0/0/2
 description WAN_ISP_B_RADIO
 ip address 198.18.50.2 255.255.255.252
#
# Rutas estaticas fijas hacia los Hubs por su respectivo ISP
ip route-static 203.0.113.10 255.255.255.255 198.51.100.1
ip route-static 203.0.113.20 255.255.255.255 198.18.50.1

# 2. Criptografia IKEv2 y IPsec
ike proposal 10
 encryption-algorithm aes-cbc-256
 dh group14
 authentication-algorithm sha2-256
 authentication-method pre-share
#
ike peer PEER_HUB1
 version 2
 ike-proposal 10
 pre-shared-key cipher ClaveCorporativaHA2026!
 remote-address 203.0.113.10
 dpd type periodic interval 10 retry 3
#
ike peer PEER_HUB2
 version 2
 ike-proposal 10
 pre-shared-key cipher ClaveCorporativaHA2026!
 remote-address 203.0.113.20
 dpd type periodic interval 10 retry 3
#
ipsec proposal PROP_IPSEC
 transform esp
 esp encryption-algorithm aes-256
 esp authentication-algorithm sha2-256
#
ipsec profile PROF_VTI_HUB1
 ike-peer PEER_HUB1
 proposal PROP_IPSEC
 pfs dh-group14
#
ipsec profile PROF_VTI_HUB2
 ike-peer PEER_HUB2
 proposal PROP_IPSEC
 pfs dh-group14
#

# 3. Creacion de Interfaces de Tunel IPsec
interface Tunnel0/0/1
 description TUNEL_HACIA_HUB1
 ip address 172.16.1.2 255.255.255.252
 tunnel-protocol ipsec
 source GigabitEthernet0/0/1
 destination 203.0.113.10
 ipsec profile PROF_VTI_HUB1
 mtu 1400
 tcp adjust-mss 1360
#
interface Tunnel0/0/2
 description TUNEL_HACIA_HUB2
 ip address 172.16.2.2 255.255.255.252
 tunnel-protocol ipsec
 source GigabitEthernet0/0/2
 destination 203.0.113.20
 ipsec profile PROF_VTI_HUB2
 mtu 1400
 tcp adjust-mss 1360
#

# 4. Habilitar y Configurar BFD para Deteccion Rapida (300 ms)
bfd
 quit
#
bfd BFD_HUB1 bind peer-ip 172.16.1.1 interface Tunnel0/0/1
 discriminator local 10
 discriminator remote 11
 min-tx-interval 100
 min-rx-interval 100
 detect-multiplier 3
 commit
#
bfd BFD_HUB2 bind peer-ip 172.16.2.1 interface Tunnel0/0/2
 discriminator local 20
 discriminator remote 21
 min-tx-interval 100
 min-rx-interval 100
 detect-multiplier 3
 commit
#

# 5. BGP CON BALANCEO DE CARGA MULTIPATH EN HUAWEI
bgp 65000
 router-id 192.168.10.1
 peer 172.16.1.1 as-number 65000
 peer 172.16.1.1 connect-interface Tunnel0/0/1
 peer 172.16.1.1 bfd min-tx-interval 100 min-rx-interval 100 detect-multiplier 3
 #
 peer 172.16.2.1 as-number 65000
 peer 172.16.2.1 connect-interface Tunnel0/0/2
 peer 172.16.2.1 bfd min-tx-interval 100 min-rx-interval 100 detect-multiplier 3
 #
 ipv4-family unicast
  undo synchronization
  network 192.168.10.0 255.255.255.0
  peer 172.16.1.1 enable
  peer 172.16.2.1 enable
  # Habilitar balanceo de carga para rutas iBGP (ECMP)
  maximum load-balancing ibgp 2
quit
```



## 7. VALIDACION EN VIVO DEL BALANCEO Y SIMULACION DE FALLA (FAILOVER)


1. COMPROBAR EL BALANCEO DE CARGA ECMP ACTIVO:
   En el router de la sucursal inspeccionamos como llegar a la red del Datacenter (`10.0.0.0/16`):
   
   R_SUCURSAL# show ip route 10.0.0.0
   Routing entry for 10.0.0.0/16
     Known via "bgp 65000", distance 200, metric 0
     Tag 65000, type internal
     Redistributing via bgp 65000
     Advertised by bgp 65000
     Routing Descriptor Blocks:
     * 172.16.1.1, from 172.16.1.1, via Tunnel1
         Route metric is 0, share count 1
     * 172.16.2.1, from 172.16.2.1, via Tunnel2
         Route metric is 0, share count 1

   ¡EVIDENCIA CLAVE!:
   Existen DOS descriptores de ruteo con el asterisco `*` simultaneamente instalados
   en la tabla de enrutamiento (FIB).
   Por cada paquete de un flujo que sale por Tunnel1 hacia Hub 1, el router envia
   otro flujo de datos por Tunnel2 hacia Hub 2, utilizando el 100% de la capacidad de ambos enlaces.

2. VERIFICACION DE SESIONES BFD (KEEP-ALIVES POR HARDWARE):
   R_SUCURSAL# show bfd neighbors
   IPv4 Sessions
   NeighAddr       LD/RD         RH/RS     State     Int
   172.16.1.1      10/11         Up        Up        Tunnel1
   172.16.2.1      20/21         Up        Up        Tunnel2
   (Ambas sesiones en estado UP enviando sondeos cada 100 ms).

3. PRUEBA DE ESTRES Y FALLA CRITICA EN TIEMPO REAL:
   Simulamos la rotura fisica del cable de fibra de ISP-A en la calle:
   R_SUCURSAL(config)# interface GigabitEthernet0/1
   R_SUCURSAL(config-if)# shutdown

   CRONOMETRIA DEL EVENTO:
   - T = 0 ms: Se corta la senal optica.
   - T = 300 ms: BFD detecta la perdida de 3 paquetes de sondeo consecutivos:
     `%BFD-6-BFD_SESS_DOWN: BFD-SYSLOG: bfd_sess_down: Neighbor 172.16.1.1 on Tunnel1 has gone DOWN`
   - T = 310 ms: BGP retira inmediatamente el Next-Hop `172.16.1.1` de la tabla FIB:
     `%BGP-5-ADJCHANGE: neighbor 172.16.1.1 Down BFD session down`
   - T = 320 ms: El 100% del trafico de la sucursal conmuta inmediatamente al Tunnel 2 (Radio).

## - Resultado: CERO llamadas de VoIP desconectadas, CERO sesiones de terminal interrumpidas.
