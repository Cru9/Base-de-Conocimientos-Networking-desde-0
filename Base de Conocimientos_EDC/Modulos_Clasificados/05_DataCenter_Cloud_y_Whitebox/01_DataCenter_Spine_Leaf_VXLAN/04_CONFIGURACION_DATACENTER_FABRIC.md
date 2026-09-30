# 04. GUIA DE CONFIGURACION: DATA CENTER FABRIC (CISCO NEXUS Y ARISTA EOS)

> **REDES DE CENTROS DE DATOS (DATA CENTER & CLOUD NETWORKING)**


---


Escenario de Referencia:
- Topologia Spine-Leaf con VXLAN y MP-BGP EVPN.
- Spines actuan como Route Reflectors (RR) BGP EVPN en el ASN 65000.
- Leaves actuan como VTEPs con Anycast Gateway distribuido para la VLAN 10 (VNI 10010).
- Red de la VLAN 10: 10.1.1.0/24 (Gateway Virtual Anycast: 10.1.1.254/24).
- MTU en todos los enlaces de Fabric: 9216 bytes (Jumbo Frames).



## 1. CONFIGURACION EN CONMUTADORES CISCO NEXUS (NX-OS)



## A) Activacion de Funcionalidades Requeridas (Features):

install feature-set fabric
feature-set fabric
feature bgp
feature ospf
feature interface-vlan
feature vn-segment-vlan-based
feature nv overlay
nv overlay evpn


## B) Politica Global de MTU Jumbo (9216 bytes):

system qos
  service-policy type network-qos default-nq-policy

policy-map type network-qos JUMBO-MTU-POLICY
  class type network-qos c-8q-nq-default
    mtu 9216

system qos
  service-policy type network-qos JUMBO-MTU-POLICY


## C) Configuracion de Interfaces Fisicas Underlay (Hacia Spines):

interface Ethernet1/1
  description UPLINK-HACIA-SPINE-01
  no switchport
  mtu 9216
```text
  ip address 10.0.0.1/30
  ip ospf network point-to-point
  ip router ospf 1 area 0.0.0.0
  no shutdown

interface Loopback0
  description UNDERLAY-ROUTER-ID-Y-OSPF
  ip address 10.255.0.1/32
  ip router ospf 1 area 0.0.0.0

interface Loopback1
  description VTEP-SOURCE-IP-OVERLAY
  ip address 10.255.1.1/32
  ip router ospf 1 area 0.0.0.0
```


## D) Configuracion de VNI y Anycast Gateway en el Leaf:

! Creacion de la VLAN y asociacion al VNI de Capa 2
```text
vlan 10
  name PRODUCCION-SERVIDORES
  vn-segment 10010

! Direccion MAC virtual Anycast identica en todos los Leaves del Datacenter
fabric forwarding anycast-gateway-mac 0000.5e00.0101

! SVI con Gateway Distribuido
interface Vlan10
  no shutdown
  vrf member default
  ip address 10.1.1.254/24
  fabric forwarding mode anycast-gateway
```


## E) Configuracion de la Interfaz NVE (Network Virtualization Endpoint - VTEP):

interface nve1
```text
  no shutdown
  source-interface loopback1
  host-reachability protocol bgp
  member vni 10010
    ingress-replication protocol bgp
```


## F) Configuracion de MP-BGP EVPN (Plano de Control):

router bgp 65001
  router-id 10.255.0.1

  ! Vecindad BGP EVPN hacia Spine 1 (10.255.0.100)
  neighbor 10.255.0.100
    remote-as 65000
    update-source loopback0
    address-family l2vpn evpn
      send-community
      send-community extended

  ! Habilitacion del VNI 10010 en el plano EVPN
  evpn
    vni 10010 l2
      rd auto
      route-target import auto
      route-target export auto



## 2. CONFIGURACION EN CONMUTADORES ARISTA EOS



## A) Configuracion de Interfaces Fisicas y MTU:

interface Ethernet1
  description UPLINK-HACIA-SPINE-01
  no switchport
  mtu 9214
```text
  ip address 10.0.0.2/30
  ip ospf network point-to-point
  ip ospf area 0.0.0.0

interface Loopback0
  description ROUTER-ID-UNDERLAY
  ip address 10.255.0.2/32
  ip ospf area 0.0.0.0

interface Loopback1
  description VTEP-IP-VXLAN
  ip address 10.255.1.2/32
  ip ospf area 0.0.0.0
```


## B) Configuracion del Tunel VXLAN (Vxlan1):

interface Vxlan1
  vxlan source-interface Loopback1
  vxlan udp-port 4789
  vxlan vlan 10 vni 10010


## C) Anycast Gateway con VARP (Virtual ARP) en Arista:

ip virtual-router mac-address 00:1c:73:00:00:99

```text
vlan 10
  name PRODUCCION-WEB

interface Vlan10
  ip address virtual 10.1.1.254/24
```


## D) Configuracion de MP-BGP EVPN en Arista EOS:

router bgp 65002
  router-id 10.255.0.2
  neighbor EVPN-SPINES peer group
  neighbor EVPN-SPINES remote-as 65000
  neighbor EVPN-SPINES update-source Loopback0
  neighbor EVPN-SPINES send-community
  neighbor 10.255.0.100 peer group EVPN-SPINES

  address-family evpn
    neighbor EVPN-SPINES activate

```text
  vlan 10
    rd 10.255.0.2:10
    route-target both 10010:10010
    redistribute learned
```



## 3. COMANDOS ESENCIALES DE VALIDACION Y VERIFICACION EN PRODUCCION


En Cisco Nexus (NX-OS):
- `show nve interface nve1`          -> Verifica que el VTEP este UP y con su IP correcta.
- `show nve peers`                   -> Lista todos los demas Leaves remotos descubiertos.
- `show bgp l2vpn evpn summary`      -> Estado de las sesiones BGP EVPN con los Spines.
- `show bgp l2vpn evpn`              -> Tabla de rutas EVPN (Rutas Type 2 MAC/IP aprendidas).
- `show ip route`                    -> Verifica las rutas de Underlay (OSPF/eBGP).

En Arista EOS:
- `show vxlan vtep`                  -> Lista de tuneles VTEP activos hacia otros conmutadores.
- `show vxlan address-table`         -> Mapeo de direcciones MAC aprendidas sobre la red VXLAN.
- `show bgp evpn summary`            -> Estado de los peers BGP EVPN.

## - `show bgp evpn route-type mac-ip`  -> Detalle de las direcciones MAC y su VTEP origen.
