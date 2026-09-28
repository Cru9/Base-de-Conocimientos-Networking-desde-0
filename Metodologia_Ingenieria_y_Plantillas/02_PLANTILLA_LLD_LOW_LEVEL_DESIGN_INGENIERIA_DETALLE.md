# 02. PLANTILLA PROFESIONAL: DISENO DE BAJO NIVEL (LLD - LOW-LEVEL DESIGN)

> **METODOLOGIA DE INGENIERIA, PLANTILLAS Y DOCUMENTACION PROFESIONAL**


---


-------------------------------------------------------------------------------
DOCUMENTO DE ESPECIFICACIONES TECNICAS DE INGENIERIA DETALLADA
TITULO DEL PROYECTO: [Modernizacion de Conectividad y Switching Campus/DC]
REFERENCIA HLD:      [HLD-NET-2026-v1.1]
CLIENTE / SEDE:      [Sede Central - Campus Norte]
INGENIERO RESPONSABLE:[Nombre del Especialista / CCNP / CCIE]

## FECHA DE VALIDACION: [AAAA-MM-DD]



## 1. LISTA DE MATERIALES DE HARDWARE (BILL OF MATERIALS - BOM)


| Item | Cant. Fabricante | Numero de Parte (SKU) | Descripcion del Equipo |
| :--- | :--- | :--- | :--- |
| 1 | 2 | Cisco | C8300-1N1S-4T2X Router Edge WAN Modular con 2x 10GE y 4x 1GE |
| 2 | 2 | Cisco | C9500-24Y4C-A Switch Core L3 24x 1/10/25G + 4x 40/100G |
| 3 | 4 | Cisco | C9300-48P-E Switch Acceso 48 Puertos PoE+ con mGig |
| 4 | 8 | Cisco | SFP-10G-SR Transceptor Optico 10G Multimodo 850nm LC |
| 5 | 4 | Cisco | QSFP-40G-SR4 Transceptor Optico 40G MPO Datacenter |
| 6 | 8 | Panduit | NK6PC3MBUY Patch Cord UTP Categoria 6A Azul 3 metros |
| 7 | 4 | Panduit | F92ERLNSNSNM003 Patch Cord Fibra Optica Monomodo LC-LC 3m |




## 2. ELEVACION DE RACK FISICO (RACK ELEVATION DIAGRAM - RACK 42U)

Rack ID: RCK-DC-01 (Datacenter Sala Blanca - Fila A)

   [ Unidad U ]  [ Equipo Montado ]                         [ Funcion / Rol ]
```text
   +-----------+------------------------------------------+-----------------------+
   |  U41-U42  | Organizador Horizontal de Fibra Optica   | Gestion de Patch Cords|
   |    U40    | Cisco Catalyst 9500 (SW-CORE-01)         | Switch Core Primario  |
   |    U39    | Organizador Horizontal de Cableado       | Cable Management      |
   |    U38    | Cisco Catalyst 9500 (SW-CORE-02)         | Switch Core Secundario|
   |  U36-U37  | Patch Panel de Fibra Optica LC (ODF)     | Troncal Distribucion  |
   |    U35    | Espacio Libre (Panel Ciego de Flujo)     | Aislamiento Termico   |
   |    U34    | Cisco Catalyst 8300 (RT-WAN-01)          | Router Borde WAN ISP1 |
   |    U33    | Cisco Catalyst 8300 (RT-WAN-02)          | Router Borde WAN ISP2 |
   |  U20-U32  | Bahias para Servidores y Almacenamiento  | Cargas de Computo     |
   |  U01-U04  | UPS APC Smart-UPS Online 3000VA          | Respaldo Energetico   |
   +-----------+------------------------------------------+-----------------------+
```


## 3. MATRIZ DE CONECTIVIDAD PUERTO A PUERTO (PORT-TO-PORT MAPPING)


| Equipo Origen | Puerto Origen | Tipo Cable | Equipo Destino | Puerto Destino | Velocidad/VLAN |
| :--- | :--- | :--- | :--- | :--- | :--- |
| RT-WAN-01 | TenGig0/0/1 | Fibra OS2 | SW-CORE-01 | TenGig1/0/1 | 10G / Routed P2P |
| RT-WAN-01 | Gigabit0/0/0 | UTP Cat6A | Módem ISP 1 | Port 1 LAN | 1 Gbps / WAN |
| RT-WAN-02 | TenGig0/0/1 | Fibra OS2 | SW-CORE-02 | TenGig1/0/1 | 10G / Routed P2P |
| RT-WAN-02 | Gigabit0/0/0 | UTP Cat6A | Módem ISP 2 | Port 1 LAN | 1 Gbps / WAN |
| SW-CORE-01 | FortyGig1/0/25 | Fibra OM4 | SW-CORE-02 | FortyGig1/0/25 | 40G / Port-Channel 1 (Trunk) |
| SW-CORE-01 | FortyGig1/0/26 | Fibra OM4 | SW-CORE-02 | FortyGig1/0/26 | 40G / Port-Channel 1 (Trunk) |
| SW-CORE-01 | TenGig1/0/2 | Fibra OM4 | SW-ACC-01 | TenGig1/1/1 | 10G / Trunk (VLANs 10,20,30) |




## 4. MATRIZ DE SEGMENTACION L2 (VLANS) Y VRFS


| VLAN ID | Nombre de la VLAN | Subred IPv4 | Gateway (SVI) | VRF Asociada | DHCP Server |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 10 | VLAN_SERVIDORES | 10.10.10.0/24 | 10.10.10.1 | VRF_DATACENTER Estatico / IPAM |  |
| 20 | VLAN_USUARIOS_LAN | 10.10.20.0/23 | 10.10.20.1 | VRF_CAMPUS | 10.50.0.10 (DHCP) |
| 30 | VLAN_TELEFONIA_VOIP | 10.10.30.0/24 | 10.10.30.1 | VRF_VOIP | 10.50.0.10 (Option 150) |
| 40 | VLAN_CAMARAS_CCTV | 10.10.40.0/24 | 10.10.40.1 | VRF_SEGURIDAD | 10.50.0.10 (MAB) |
| 99 | VLAN_GESTION_IN-BAND 10.10.99.0/24 | 10.10.99.1 | default | Estatico (TACACS+) |  |
| 999 | VLAN_CUARENTENA | 10.10.99.0/24 | 10.10.99.1 | default | Aislada (802.1X Auth-Fail) |




## 5. PLAN DE DIRECCIONAMIENTO IP PUNTO A PUNTO (ROUTED LINKS)


| Segmento /30 | Uso / Descripcion | IP Equipo A | IP Equipo B |
| :--- | :--- | :--- | :--- |
| 10.255.0.0/30 | Enlace P2P Core 1 a WAN 1 | 10.255.0.1 (CORE-01) 10.255.0.2 (WAN-01) |  |
| 10.255.0.4/30 | Enlace P2P Core 2 a WAN 2 | 10.255.0.5 (CORE-02) 10.255.0.6 (WAN-02) |  |
| 10.255.0.8/30 | Enlace P2P Core 1 a Core 2 | 10.255.0.9 (CORE-01) 10.255.0.10 (CORE-02) |  |
| 10.255.255.1/32 | Loopback 0 Router WAN 1 | 10.255.255.1 | N/A (Router ID) |
| 10.255.255.2/32 | Loopback 0 Router WAN 2 | 10.255.255.2 | N/A (Router ID) |




## 6. CONFIGURACION BASE ESTANDARIZADA (SNIPPET LISTO PARA APLICAR)

Plantilla para el Switch Core Primario (SW-CORE-01):

hostname SW-CORE-01
!
ip routing
service timestamps log datetime msec localtime show-timezone
service password-encryption
!
vrf definition VRF_CAMPUS
 rd 65001:20
 address-family ipv4
 exit-address-family
!
interface Port-channel1
 description ENLACE_TRUNK_HACIA_CORE_02
```text
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,99
 no shutdown
!
interface TenGigabitEthernet1/0/1
 description ENLACE_ROUTED_A_ROUTER_WAN_01
 no switchport
 ip address 10.255.0.1 255.255.255.252
 ip ospf 1 area 0
 ip ospf network point-to-point
 bfd interval 300 min_rx 300 multiplier 3
 ip ospf bfd
 no shutdown
!
router ospf 1
 router-id 10.255.255.11
 log-adjacency-changes
 passive-interface default
 no passive-interface TenGigabitEthernet1/0/1
!
line con 0
 exec-timeout 15 0
 stopbits 1
line vty 0 4
 transport input ssh
 exec-timeout 15 0
!
end
```


`cisco
write memory
`
