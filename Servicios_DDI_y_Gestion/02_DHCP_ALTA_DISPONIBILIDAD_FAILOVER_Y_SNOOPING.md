# 02. DHCP ALTA DISPONIBILIDAD, OPCIONES AVANZADAS Y DHCP SNOOPING

> **SERVICIOS DE RED CORE (DDI: DNS, DHCP, IPAM) Y GESTION EMPRESARIAL**


---



## 1. CICLO DORA Y EL ROL DEL RELAY AGENT (IP HELPER-ADDRESS)

Los clientes obtienen su direccion IP mediante el intercambio DORA (Capa 2):
1. Discover (Broadcast 255.255.255.255: UDP 67 -> 68)
2. Offer    (El servidor ofrece una IP con sus opciones)
3. Request  (El cliente solicita formalmente la IP ofrecida)
4. Ack      (El servidor confirma la concesion / Lease)

Como los broadcasts NO cruzan los routers, se configura el DHCP Relay Agent en
la interfaz gateway (SVI / Subinterfaz):
- El switch/router intercepta el broadcast.
- Inserta su propia IP de interfaz en el campo "giaddr" (Gateway IP Address).
- Reenvia la peticion como UNICAST al servidor DHCP central en el Datacenter.
- Gracias al "giaddr", el servidor DHCP sabe exactamente de que subred entregar la IP.



## 2. OPCIONES DHCP CRITICAS EN REDES CORPORATIVAS


| Opcion | Nombre | Uso Practico en la Empresa |
| :--- | :--- | :--- |
| Option 3 | Router (Default Gateway) | Puerta de enlace predeterminada para los hosts. |
| Option 6 | DNS Servers | Direcciones IP de los servidores DNS resolutores. |
| Option 15 | Domain Name | Sufijo DNS de busqueda (ej. "corp.local"). |
| Option 43 | Vendor-Specific | Le indica a los Access Points (APs) de Cisco o Huawei |

                                        la IP del controlador Wi-Fi (WLC) para auto-unirse.
Option 60   Vendor Class Identifier     Identifica la marca/modelo del cliente (ej. "Cisco AP c3802").
Option 66/67 TFTP Server / Bootfile     Arranque por red PXE para instalacion masiva de SO.
Option 82   Relay Agent Information     Inserta el ID del switch y numero de puerto exacto.
Option 150  TFTP Server (Cisco)         Lista de IPs de Cisco Unified Communications Manager (CUCM)
                                        para que los telefonos IP descarguen su firmware y linea.



## 3. ALTA DISPONIBILIDAD EN DHCP (FAILOVER ACTIVO-ACTIVO Y HOT-STANDBY)

En Windows Server DHCP o ISC-Kea en Linux, se despliega el protocolo de Failover
(RFC 3074) mediante una sesion TCP (puerto 647):
- Esquema Load Balance (50/50): Ambos servidores entregan direcciones simultaneamente
  distribuidas por un algoritmo de hash. Si un servidor se apaga, el sobreviviente
  toma el control del 100% del rango.
- Esquema Hot-Standby: El servidor Primario asigna todas las IPs. El Secundario solo
  actua si el Primario deja de responder tras expirar el MCLT (Maximum Client Lead Time).



## 4. LA TRINIDAD DE SEGURIDAD CAPA 2: DHCP SNOOPING + DAI + IP SOURCE GUARD

Los ataques mas destructivos en redes de acceso son:
1. Rogue DHCP Server: Un atacante conecta un router casero que entrega IPs falsas
   con su propia maquina como gateway, capturando todo el trafico.
2. DHCP Starvation: El atacante envia millones de peticiones con MACs falsas para
   agotar el pool de IPs en segundos.
3. ARP Spoofing / Poisoning: El atacante suplanta la MAC de la puerta de enlace.

Solucion Integrada en Cisco Catalyst (IOS-XE):

! 1. Activar DHCP Snooping globalmente y en las VLANs de usuarios
ip dhcp snooping
ip dhcp snooping vlan 10,20,30
no ip dhcp snooping information option   ! Evita problemas si el switch no es router

! 2. Configurar puertos de confianza (Uplinks hacia el Core / Servidor DHCP)
```text
interface GigabitEthernet1/0/24
 description UPLINK_HACIA_CORE_DHCP
 ip dhcp snooping trust

! 3. Configurar puertos de acceso de usuarios (Untrusted con Rate-Limit)
interface range GigabitEthernet1/0/1 - 20
 description PUERTOS_USUARIOS_FINALES
 switchport mode access
 switchport access vlan 20
 ! Limitar peticiones DHCP a 15 por segundo (mitiga DHCP Starvation)
 ip dhcp snooping limit rate 15

! 4. Habilitar Dynamic ARP Inspection (DAI) - Valida ARP contra la tabla de Snooping
ip arp inspection vlan 10,20,30
interface GigabitEthernet1/0/24
 ip arp inspection trust

! 5. Habilitar IP Source Guard (IPSG) - Impide que un usuario se ponga IP estatica manual
interface range GigabitEthernet1/0/1 - 20
 ip verify source
```


## 5. CONFIGURACION DE DHCP RELAY EN CISCO Y HUAWEI

Cisco IOS-XE (Configuracion en la SVI Gateway):
interface Vlan20
 description GATEWAY_LAN_FINANZAS
```text
 ip address 10.10.20.1 255.255.255.0
 ip helper-address 10.50.0.10     ! Servidor DHCP Primario
 ip helper-address 10.50.0.11     ! Servidor DHCP Secundario

Huawei VRP (Configuracion en la VLANIF Gateway):
dhcp enable
interface Vlanif20
 description GATEWAY_LAN_FINANZAS
 ip address 10.10.20.1 255.255.255.0
 dhcp select relay
 dhcp relay server-ip 10.50.0.10
 dhcp relay server-ip 10.50.0.11
```


## 6. COMANDOS DE VERIFICACION Y MONITOREO

1. Ver la base de datos de vinculacion de DHCP Snooping:
```text
   show ip dhcp snooping binding
   ! Muestra: MAC, IP asignada, tiempo restante de Lease, VLAN e interfaz fisica.

2. Ver estadisticas y paquetes descartados por DHCP Snooping:
   show ip dhcp snooping

3. Ver estadisticas de paquetes ARP fraudulentos bloqueados por DAI:
   show ip arp inspection statistics vlan 20

4. Limpiar una entrada especifica de la tabla de Snooping:
```


`cisco
clear ip dhcp snooping binding 10.10.20.105
`
