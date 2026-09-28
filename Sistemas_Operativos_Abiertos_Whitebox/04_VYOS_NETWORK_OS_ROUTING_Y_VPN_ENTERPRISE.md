# 04. VYOS NETWORK OS: ROUTER DECLARATIVO, BGP, IPSEC VTI Y FIREWALL

> **SISTEMAS OPERATIVOS DE RED ABIERTOS (OPEN NETWORKING & WHITE-BOX)**


---



## 1. ¿QUE ES VYOS Y POR QUE ES EL PREFERIDO EN ARQUITECTURAS HIBRIDAS?

VyOS es un sistema operativo de red empresarial de codigo abierto basado en Debian GNU/Linux.
Nacio como un fork comunitario tras la adquisicion de Vyatta por parte de Brocade.

VyOS combina la estabilidad del Kernel de Linux con una interfaz de linea de comandos
(CLI) jerarquica y declarativa inspirada en Juniper JUNOS:
- Toda la configuracion del sistema se almacena en un unico archivo estructurado
  en arbol (/config/config.boot).
- Cuenta con un mecanismo de confirmacion atomica de cambios (commit / rollback).
- Incluye la funcion salvavidas 'commit-confirm': si cometes un error en una regla de
  firewall o IP remota que te desconecte de SSH, el router revierte automaticamente
  la configuracion tras 10 minutos.
- Muy utilizado como Router Virtual (NVA) en AWS, Azure, GCP y servidores Proxmox/VMware.



## 2. MODOS DE OPERACION Y FLUJO DE CAMBIOS EN VYOS

- Modo Operativo (Prompt '$'):
  Para visualizar estados, tablas y diagnostico:
  vyos@vyos:~$ show interfaces
  vyos@vyos:~$ show ip route
  vyos@vyos:~$ configure

- Modo de Configuracion (Prompt '#'):
  Para editar los parametros de red:
  vyos@vyos# set ...
  vyos@vyos# delete ...

COMANDOS DE GOBERNANZA DE CAMBIOS EN VYOS:
  compare        -> Muestra exactamente que lineas van a agregarse (+) o eliminarse (-).
  commit         -> Valida la sintaxis y aplica los cambios en memoria activa.
  commit-confirm -> Aplica el cambio con un temporizador de seguridad de rescate.
  save           -> Guarda la configuracion en el disco para el siguiente reinicio.
  rollback       -> Descarta los cambios no confirmados o regresa a una version anterior.



## 3. CONFIGURACION DE INTERFACES Y ENRUTAMIENTO OSPF/BGP

vyos@vyos# configure

! 1. Interfaces de Red
set interfaces ethernet eth0 description "WAN_CONEXION_ISP"
set interfaces ethernet eth0 address "200.50.10.2/30"

set interfaces ethernet eth1 description "LAN_DATACENTER"
set interfaces ethernet eth1 address "10.10.10.1/24"

! 2. Enrutamiento OSPFv2 para la red interna
set protocols ospf router-id "10.10.10.1"
set protocols ospf area 0 network "10.10.10.0/24"
set protocols ospf passive-interface "eth1"

! 3. Enrutamiento BGP Dinamico con Upstream ISP
set protocols bgp system-as 65001
set protocols bgp parameters router-id 10.10.10.1
set protocols bgp neighbor 200.50.10.1 remote-as 64500
set protocols bgp neighbor 200.50.10.1 description "ISP_TRANSIT_PRIMARY"
set protocols bgp neighbor 200.50.10.1 address-family ipv4-unicast soft-reconfiguration inbound
set protocols bgp address-family ipv4-unicast network "10.10.0.0/16"



## 4. TUNEL VPN IPSEC BASADO EN RUTA (VTI - VIRTUAL TUNNEL INTERFACE)

! 1. Definir Fase 1 IKEv2
set vpn ipsec ike-group IKE-SUCURSAL-01 proposal 1 encryption aes256gcm
set vpn ipsec ike-group IKE-SUCURSAL-01 proposal 1 prf sha384
set vpn ipsec ike-group IKE-SUCURSAL-01 proposal 1 dh-group 19
set vpn ipsec ike-group IKE-SUCURSAL-01 key-exchange ikev2

! 2. Definir Fase 2 ESP
set vpn ipsec esp-group ESP-SUCURSAL-01 proposal 1 encryption aes256gcm
set vpn ipsec esp-group ESP-SUCURSAL-01 proposal 1 dh-group 19
set vpn ipsec esp-group ESP-SUCURSAL-01 lifetime 3600

! 3. Crear la interfaz virtual VTI
set interfaces vti vti0 description "TUNEL_IPSEC_SUCURSAL_NORTE"
set interfaces vti vti0 address "172.16.100.1/30"
set interfaces vti vti0 ip mtu 1400

! 4. Vincular el tunel IPsec a la interfaz VTI
set vpn ipsec site-to-site peer 190.20.10.5 authentication mode pre-shared-secret
set vpn ipsec site-to-site peer 190.20.10.5 authentication pre-shared-secret "VyosSuperIpsecKey2026!"
set vpn ipsec site-to-site peer 190.20.10.5 default-esp-group ESP-SUCURSAL-01
set vpn ipsec site-to-site peer 190.20.10.5 ike-group IKE-SUCURSAL-01
set vpn ipsec site-to-site peer 190.20.10.5 local-address 200.50.10.2
set vpn ipsec site-to-site peer 190.20.10.5 vti bind vti0



## 5. CORTAFUEGOS BASADO EN ZONAS (ZONE-BASED FIREWALL)

En VyOS, el firewall se gestiona por Zonas de Seguridad con seguimiento de estado (Stateful):

! 1. Crear conjuntos de reglas para trafico que entra a la LAN desde la WAN
set firewall name WAN-A-LAN default-action drop
set firewall name WAN-A-LAN rule 10 description "Permitir conexiones establecidas y relacionadas"
set firewall name WAN-A-LAN rule 10 action accept
set firewall name WAN-A-LAN rule 10 state established enable
set firewall name WAN-A-LAN rule 10 state related enable

set firewall name WAN-A-LAN rule 20 description "Descartar paquetes invalidos"
set firewall name WAN-A-LAN rule 20 action drop
set firewall name WAN-A-LAN rule 20 state invalid enable

! 2. Asignar politicas de zona
set zone-policy zone LAN interface eth1
set zone-policy zone WAN interface eth0
set zone-policy zone WAN from LAN firewall name LAN-A-WAN
set zone-policy zone LAN from WAN firewall name WAN-A-LAN

! 3. Aplicar los cambios con seguridad
commit-confirm 5
save



## 6. COMANDOS DE MONITOREO Y VERIFICACION

1. Ver el estado de los tuneles IPsec:
```text
   show vpn ipsec sa
   ! Debe mostrar: State: up, Bytes In/Out, Algoritmo AES-GCM-256

2. Ver el estado de las sesiones BGP:
   show ip bgp summary

3. Analizador de paquetes en vivo en la interfaz de red (Packet Sniffer integrado):
   monitor traffic interface eth0 filter "tcp port 443"
   ! Muestra el flujo en tiempo real exactamente como tcpdump sin salir de la CLI.

4. Ver el archivo de configuracion completo en formato jerarquico:
```


`cisco
show configuration
`
