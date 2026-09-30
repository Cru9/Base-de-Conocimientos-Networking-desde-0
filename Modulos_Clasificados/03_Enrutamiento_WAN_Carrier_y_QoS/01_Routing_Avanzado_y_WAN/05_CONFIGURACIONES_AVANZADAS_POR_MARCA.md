# 05. CONFIGURACIONES AVANZADAS MULTI-MARCA (CISCO, HUAWEI Y ARUBAOS-CX)

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---


Este laboratorio integra los conceptos mas demandados en redes empresariales:
1. OSPF Multi-Area con Area 10 en modo STUB para aislar la sucursal.
2. Sincronizacion de fallas por hardware mediante BFD (deteccion en 100 ms).
3. Sesion eBGP redundante hacia el Proveedor de Internet (ISP) con politicas
   de trafico (Local Preference y AS-Path Prepend).
4. Segmentacion logica mediante VRF (Virtual Routing and Forwarding).


## 1. CONFIGURACION EN CISCO (IOS / IOS-XE)

! --- PASO 1: CREACION DE VRF PARA SEGMENTAR EL TRAFICO WAN ---
vrf definition EMPRESA_WAN
 rd 65001:100
 address-family ipv4
 exit-address-family
!
```text
interface GigabitEthernet 0/0/1
 description ENLACE_LAN_INTERNA_SUCURSAL
 vrf forwarding EMPRESA_WAN
 ip address 192.168.10.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet 0/0/2
 description UPLINK_HACIA_ISP_A
 vrf forwarding EMPRESA_WAN
 ip address 203.0.113.2 255.255.255.252
 bfd interval 100 min_rx 100 multiplier 3
 no shutdown
!
! --- PASO 2: OSPF MULTI-AREA CON AREA 10 STUB Y BFD ---
router ospf 1 vrf EMPRESA_WAN
 router-id 1.1.1.1
 bfd all-interfaces
 area 10 stub
 network 192.168.10.0 0.0.0.255 area 10
 exit
!
! --- PASO 3: INGENIERIA DE TRAFICO BGP (ROUTE-MAPS) ---
ip prefix-list REDES_PROPIAS permit 198.51.100.0/24
!
! Preferir entrar por el ISP-A (Anunciar normal) y penalizar ISP-B con Prepend
route-map FILTRO_SALIDA_ISP_A permit 10
 match ip address prefix-list REDES_PROPIAS
 set local-preference 200
!
route-map FILTRO_ANUNCIO_ISP_B permit 10
 match ip address prefix-list REDES_PROPIAS
 set as-path prepend 65001 65001 65001
!
! --- PASO 4: SESION eBGP HACIA EL PROVEEDOR DE INTERNET ---
router bgp 65001
 address-family ipv4 vrf EMPRESA_WAN
  neighbor 203.0.113.1 remote-as 64512
  neighbor 203.0.113.1 description PEERING_ISP_TELMEX
  neighbor 203.0.113.1 fall-over bfd
  neighbor 203.0.113.1 route-map FILTRO_SALIDA_ISP_A in
  neighbor 203.0.113.1 route-map FILTRO_ANUNCIO_ISP_B out
  network 198.51.100.0 mask 255.255.255.0
 exit-address-family
```



## 2. CONFIGURACION EN HUAWEI (VRP)

# --- PASO 1: CREACION DE INSTANCIA VPN (VRF) ---
ip vpn-instance EMPRESA_WAN
 ipv4-family
  route-distinguisher 65001:100
  vpn-target 65001:100 both
quit
#
```text
interface GigabitEthernet 0/0/1
 description ENLACE_LAN_INTERNA_SUCURSAL
 ip binding vpn-instance EMPRESA_WAN
 ip address 192.168.10.1 255.255.255.0
#
interface GigabitEthernet 0/0/2
 description UPLINK_HACIA_ISP_A
 ip binding vpn-instance EMPRESA_WAN
 ip address 203.0.113.2 255.255.255.252
#
# --- PASO 2: OSPF MULTI-AREA CON AREA 10 STUB ---
ospf 1 vpn-instance EMPRESA_WAN router-id 1.1.1.1
 bfd all-interfaces enable
 area 0.0.0.10
  stub
  network 192.168.10.0 0.0.0.255
quit
#
# --- PASO 3: POLITICAS DE RUTA Y AS-PATH FILTER ---
ip ip-prefix REDES_PROPIAS permit 198.51.100.0 24
#
route-policy FILTRO_SALIDA_ISP_A permit node 10
 if-match ip-prefix REDES_PROPIAS
 apply local-preference 200
#
route-policy FILTRO_ANUNCIO_ISP_B permit node 10
 if-match ip-prefix REDES_PROPIAS
 apply as-path 65001 65001 additive
#
# --- PASO 4: SESION BGP HACIA EL PROVEEDOR ---
bgp 65001
 ipv4-family vpn-instance EMPRESA_WAN
  peer 203.0.113.1 as-number 64512
  peer 203.0.113.1 bfd min-tx-interval 100 min-rx-interval 100
  peer 203.0.113.1 route-policy FILTRO_SALIDA_ISP_A import
  peer 203.0.113.1 route-policy FILTRO_ANUNCIO_ISP_B export
  network 198.51.100.0 255.255.255.0
quit
```



## 3. CONFIGURACION EN ARUBA (ARUBAOS-CX)

! --- PASO 1: CREACION DE VRF Y ASIGNACION DE PUERTOS ---
vrf EMPRESA_WAN
!
interface 1/1/1
 vrf attach EMPRESA_WAN
 description ENLACE_LAN_INTERNA_SUCURSAL
 routing
```text
 ip address 192.168.10.1/24
 no shutdown
!
interface 1/1/2
 vrf attach EMPRESA_WAN
 description UPLINK_HACIA_ISP_A
 routing
 ip address 203.0.113.2/30
 bfd min-transmit-interval 100
 bfd min-receive-interval 100
 bfd detect-multiplier 3
 bfd enable
 no shutdown
!
! --- PASO 2: OSPF MULTI-AREA STUB EN AOS-CX ---
router ospf 1 vrf EMPRESA_WAN
 router-id 1.1.1.1
 area 0.0.0.10 stub
 bfd enable
!
interface 1/1/1
 ip ospf 1 area 0.0.0.10
!
! --- PASO 3: SESION eBGP CON ROUTE-MAP EN AOS-CX ---
route-map PREFERIR_ISP_A permit seq 10
 set local-preference 200
!
router bgp 65001 vrf EMPRESA_WAN
 neighbor 203.0.113.1 remote-as 64512
 neighbor 203.0.113.1 bfd
 neighbor 203.0.113.1 route-map PREFERIR_ISP_A in
```


network 198.51.100.0/24
