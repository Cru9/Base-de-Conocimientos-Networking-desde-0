# 00. INDICE GENERAL, DESAGREGACION DE HARDWARE, ONIE Y SAI

> **SISTEMAS OPERATIVOS DE RED ABIERTOS (OPEN NETWORKING & WHITE-BOX)**


---



## 1. LA REVOLUCION DEL "OPEN NETWORKING" Y SWITCHING WHITE-BOX

Durante decadas, el mercado de redes estuvo dominado por sistemas propietarios
integrados: si comprabas hardware Cisco, Arista o Juniper, estabas obligado a usar
su software y pagar licencias anuales recurrentes.

Open Networking introduce la DESAGREGACION, separando el hardware del software
exactamente como sucedio en el mundo de los servidores PC x86 hace 30 anos:
- Hardware "White-Box" / "Bare-Metal": Switches fabricados por ensambladores como
  Edgecore Networks, Quanta, Celestica o Delta, con chips ASIC de silicio comercial
  (Merchant Silicon) de maxima velocidad (Broadcom Tomahawk/Trident, Nvidia Spectrum).
- Software Libre / Abierto (NOS - Network Operating System): El cliente es dueno
  absoluto de la caja e instala el sistema operativo de red que prefiera.



## 2. COMPONENTES CLAVE DE LA ARQUITECTURA WHITE-BOX

1. ONIE (Open Network Install Environment):
   - Es un gestor de arranque (Bootloader L2) de codigo abierto integrado en la memoria
     flash de la placa base del switch.
   - Funciona exactamente como el instalador BIOS/UEFI de una computadora: arranca el
     switch, busca una IP por DHCP e instala automaticamente por TFTP/HTTP la imagen
     del sistema operativo que elijas (SONiC, Cumulus Linux, VyOS, Open Network Linux).

2. Silicio Comercial (Merchant Silicon ASICs):
   - Chips de conmutacion ultra-rapidos que superan a menudo a los ASICs propietarios:
     * Broadcom Trident 3 / 4 (Switches Top-of-Rack empresariales).
     * Broadcom Tomahawk 3 / 4 / 5 (Datacenters Spine-Leaf de 100G, 400G y 800 Gbps).
     * Nvidia / Mellanox Spectrum 2 / 3 / 4 (Baja latencia e hiperconvergencia RoCEv2).

3. SAI (Switch Abstraction Interface):
   - Proyecto estandarizado por la Open Compute Project (OCP).
   - Proporciona una API C/C++ universal para programar las tablas de hardware de los ASICs
     (rutas IPv4, VLANs, ACLs, tuneles VXLAN, colas QoS).
   - Gracias a SAI, un mismo sistema operativo (como SONiC) puede ejecutarse sin
     cambiar una sola linea de codigo en un switch con chip Broadcom o Nvidia Mellanox.



## 3. INDICE DE ARCHIVOS DE LA CARPETA SISTEMAS_OPERATIVOS_ABIERTOS_WHITEBOX

[00_INDICE_Y_ARQUITECTURA_OPEN_NETWORKING.md](./00_INDICE_Y_ARQUITECTURA_OPEN_NETWORKING.md)
    - Fundamentos de redes abiertas, desagregacion, ONIE, Merchant Silicon y la API SAI.

[01_FRROUTING_FRR_LINUX_BGP_OSPF_Y_BFD.md](./01_FRROUTING_FRR_LINUX_BGP_OSPF_Y_BFD.md)
    - Suite FRRouting (FRR) en Linux (Ubuntu/Debian): arquitectura de daemons (zebra, bgpd, ospfd),
      consola unificada 'vtysh', integracion con tablas de ruteo del kernel y peers BGP/OSPF.

[02_SONIC_NETWORK_OPERATING_SYSTEM_DATACENTER.md](./02_SONIC_NETWORK_OPERATING_SYSTEM_DATACENTER.md)
    - SONiC (Software for Open Networking in the Cloud) liderado por Microsoft y OCP.
      Arquitectura de microservicios contenerizados (Docker, Redis-DB, SWSS, Syncd)
      y configuracion de Topologias Spine-Leaf L3 en Datacenters.

[03_MIKROTIK_ROUTEROS_V7_BGP_OSPF_Y_COLAS.md](./03_MIKROTIK_ROUTEROS_V7_BGP_OSPF_Y_COLAS.md)
    - MikroTik RouterOS v7: Nuevo motor de enrutamiento, sintaxis moderna de Routing Filters,
      configuracion de BGP multi-homing, OSPFv3, tuneles WireGuard y control de ancho de banda (Queues).

[04_VYOS_NETWORK_OS_ROUTING_Y_VPN_ENTERPRISE.md](./04_VYOS_NETWORK_OS_ROUTING_Y_VPN_ENTERPRISE.md)
    - VyOS Network OS: Sistema operativo declarativo basado en Debian para appliances bare-metal y nubes.

## Modo operativo y de configuracion (set / commit / save), BGP, VRRP, IPsec VTI y Firewalls Zone-Based.
