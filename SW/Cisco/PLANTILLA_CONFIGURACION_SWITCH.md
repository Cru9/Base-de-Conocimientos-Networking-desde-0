# CISCO (IOS / IOS-XE) - PLANTILLA ULTRA-HARDENED DE PRODUCCION (SEGURIDAD MAXIMA)


---

Descripcion: Configuracion corporativa de maxima seguridad (Hardening Enterprise).
Incluye:
- Usuarios nivel 15 y cifrado maestro.
- Seguridad estricta en consola y lineas VTY restringidas por ACL de gestion.
- Sincronizacion de reloj NTP y Banner legal disuasorio (MOTD).
- VLAN 1 de gestion (192.168.1.1/24) con Default Gateway (192.168.1.254).
- Puertos de acceso (1-23): BPDU Guard, Port Security (max 2 MACs) y Storm Control.
- Autorecuperacion de puertos caidos (Errdisable Recovery en 300 seg).
- DHCP Snooping contra servidores DHCP piratas.
- Puerto troncal (24) confiable (Trusted).

## - Servidor Syslog centralizado (11.39.41.200) con auditoria de logins y enlaces.


! -----------------------------------------------------------------------------
! PASO 1: MODO PRIVILEGIADO Y CONFIGURACION GLOBAL
! -----------------------------------------------------------------------------
```text
enable
configure terminal

! -----------------------------------------------------------------------------
! PASO 2: IDENTIFICACION, BANNER LEGAL Y SERVICIOS BASE
! -----------------------------------------------------------------------------
hostname SW-CISCO-PRODUCCION

! Evitar congelamientos molestos de la consola al cometer errores tipograficos
no ip domain-lookup

! Banner legal de advertencia (obligatorio para auditorias de seguridad)
banner motd #
*******************************************************************************
*                        SISTEMA PRIVADO Y RESTRINGIDO                        *
*  El acceso no autorizado a este conmutador esta estrictamente prohibido.    *
*  Todas las actividades son monitoreadas y registradas para accion legal.    *
*******************************************************************************
#

! Cifrado general de contrasenas en el archivo de texto
service password-encryption

! -----------------------------------------------------------------------------
! PASO 3: SINCRONIZACION HORARIA (NTP) - CRITICO PARA LOGS AUDITABLES
! -----------------------------------------------------------------------------
clock timezone UTC-6 -6 0
ntp server 11.39.41.200
ntp server 0.pool.ntp.org

! -----------------------------------------------------------------------------
! PASO 4: CREACION DE USUARIO ADMINISTRADOR Y CLAVE ENABLE
! -----------------------------------------------------------------------------
username admin privilege 15 secret CONTRASEÑA_MASTER
enable secret CONTRASEÑA_MASTER

! -----------------------------------------------------------------------------
! PASO 5: SEGURIDAD DEL PUERTO DE CONSOLA
! -----------------------------------------------------------------------------
line con 0
 password CONTRASEÑA_MASTER
 login local
 exec-timeout 10 0
 logging synchronous
 exit

! -----------------------------------------------------------------------------
! PASO 6: LISTA DE CONTROL DE ACCESO (ACL) PARA GESTION VTY (SSH / TELNET)
! Solo las IPs de administracion autorizadas podran conectarse al switch
! -----------------------------------------------------------------------------
ip access-list standard ACL_GESTION_PERMITIDA
 remark Permitir servidor Syslog y subred de TI
 permit 11.39.41.0 0.0.0.255
 remark Permitir red de administracion local
 permit 192.168.1.0 0.0.0.255
 remark Bloquear y registrar cualquier intento de intrusion
 deny any log
 exit

! -----------------------------------------------------------------------------
! PASO 7: ACCESO REMOTO SEGURO (SSH / TELNET) EN LINEAS VTY
! -----------------------------------------------------------------------------
ip domain-name empresa.local
crypto key generate rsa modulus 2048
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3

line vty 0 15
 login local
 transport input ssh telnet
 access-class ACL_GESTION_PERMITIDA in
 exec-timeout 10 0
 logging synchronous
 exit

! Desactivar interfaz web en texto plano insegura
no ip http server
ip http secure-server

! -----------------------------------------------------------------------------
! PASO 8: CONFIGURACION DE VLAN 1 Y DIRECCION IP DE GESTION
! -----------------------------------------------------------------------------
vlan 1
 name Administracion_Gestion
 exit

interface vlan 1
 description IP_Gestion_Switch
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit

ip default-gateway 192.168.1.254

! -----------------------------------------------------------------------------
! PASO 9: AUTORRECUPERACION DE PUERTOS BLOQUEADOS (ERRDISABLE RECOVERY)
! Si un puerto se apaga por BPDU Guard o Port Security, se reactiva en 5 min
! -----------------------------------------------------------------------------
errdisable recovery cause bpduguard
errdisable recovery cause psecure-violation
errdisable recovery cause storm-control
errdisable recovery interval 300

! -----------------------------------------------------------------------------
! PASO 10: SEGURIDAD DHCP SNOOPING (PREVENCION DE ROUTERS PIRATAS)
! -----------------------------------------------------------------------------
ip dhcp snooping
ip dhcp snooping vlan 1
no ip dhcp snooping information option

! -----------------------------------------------------------------------------
! PASO 11: PUERTOS DE ACCESO (PUERTOS 1 AL 23)
! Con VLAN 1, PortFast, BPDU Guard, Port Security (2 MACs) y Storm Control
! -----------------------------------------------------------------------------
spanning-tree mode rapid-pvst
spanning-tree portfast bpduguard default

interface range GigabitEthernet 0/1 - 23
 description Puertos_Usuarios_Acceso
 switchport mode access
 switchport access vlan 1
 
 ! Spanning Tree de Borde y proteccion contra switches externos
 spanning-tree portfast
 spanning-tree bpduguard enable
 
 ! Seguridad de Puerto: maximo 2 MACs persistentes
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 
 ! Control de tormentas: limita trafico broadcast y multicast al 5%
 storm-control broadcast level 5.0
 storm-control multicast level 5.0
 storm-control action trap
 
 no shutdown
 exit

! -----------------------------------------------------------------------------
! PASO 12: PUERTO TRONCAL (PUERTO 24)
! Enlace confiable hacia el Core / Router
! -----------------------------------------------------------------------------
interface GigabitEthernet 0/24
 description UPLINK_TRONCAL_HACIA_CORE
 switchport mode trunk
 switchport trunk allowed vlan all
 
 ! Puerto de confianza para trafico DHCP del servidor oficial
 ip dhcp snooping trust
 
 no shutdown
 exit

! -----------------------------------------------------------------------------
! PASO 13: CONFIGURACION DEL SERVIDOR SYSLOG (11.39.41.200) Y AUDITORIA
! Monitoreo de inicios de sesion, bloqueos por seguridad y cambios de enlace
! -----------------------------------------------------------------------------
service timestamps log datetime msec localtime show-timezone
service timestamps debug datetime msec localtime show-timezone

logging host 11.39.41.200
logging trap informational
logging source-interface vlan 1

! Registrar accesos y fallos de login en consola, SSH y telnet
login on-success log
login on-failure log

! Registrar cambios de estado operacional de interfaces
logging event link-status

! -----------------------------------------------------------------------------
! PASO 14: GUARDAR LA CONFIGURACION EN FLASH
! -----------------------------------------------------------------------------
end
write memory

! =============================================================================
! FIN DE LA CONFIGURACION - SWITCH CISCO EN MAXIMA SEGURIDAD (ULTRA-HARDENED)
! =============================================================================
```
