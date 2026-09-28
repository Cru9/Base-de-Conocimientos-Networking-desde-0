# ARUBA NETWORKS (ARUBAOS-CX) - PLANTILLA ULTRA-HARDENED (SEGURIDAD MAXIMA)


---

Descripcion: Configuracion corporativa de maxima seguridad (Hardening Enterprise).
Incluye:
- Usuario administrators con clave maestra y aislamiento de procesos.
- Proteccion del plano de control (Control-Plane ACL) para restringir gestion SSH.
- Sincronizacion horaria NTP y Banner de advertencia legal.
- VLAN 1 de gestion (192.168.1.1/24) con Default Gateway (192.168.1.254).
- Puertos de acceso (1/1/1-1/1/23): BPDU Guard, Port-Access Security y Storm Control.
- Autorrecuperacion de puertos caidos por violacion de seguridad (300 seg).
- DHCP Snooping contra servidores DHCP piratas.
- Puerto troncal (1/1/24) marcado como Confiable (Trust).

## - Servidor Syslog centralizado (11.39.41.200) con auditoria de red en tiempo real.


! -----------------------------------------------------------------------------
! PASO 1: MODO CONFIGURACION GLOBAL
! -----------------------------------------------------------------------------
```text
configure terminal

! -----------------------------------------------------------------------------
! PASO 2: ASIGNACION DE NOMBRE Y BANNER LEGAL
! -----------------------------------------------------------------------------
hostname SW-ARUBA-PRODUCCION

banner motd #
*******************************************************************************
*                        SISTEMA PRIVADO Y RESTRINGIDO                        *
*  El acceso no autorizado a este conmutador esta estrictamente prohibido.    *
*  Todas las actividades son monitoreadas y registradas para accion legal.    *
*******************************************************************************
#

! -----------------------------------------------------------------------------
! PASO 3: SINCRONIZACION HORARIA (NTP) - CRITICO PARA LOGS AUDITABLES
! -----------------------------------------------------------------------------
clock timezone UTC-6
ntp server 11.39.41.200 minpoll 4 maxpoll 6
ntp server 0.pool.ntp.org
ntp enable

! -----------------------------------------------------------------------------
! PASO 4: CREACION DE USUARIO DE MAXIMO NIVEL (ADMINISTRATORS)
! -----------------------------------------------------------------------------
user admin group administrators password
(El sistema solicitara ingresar 'CONTRASEÑA_MASTER' y confirmarla)

! -----------------------------------------------------------------------------
! PASO 5: SEGURIDAD DEL PUERTO DE CONSOLA
! -----------------------------------------------------------------------------
line console
 session-timeout 10
 exit

! -----------------------------------------------------------------------------
! PASO 6: PROTECCION DEL PLANO DE CONTROL (CONTROL-PLANE ACL)
! Restringe el acceso SSH unicamente a las subredes autorizadas de gestion
! -----------------------------------------------------------------------------
access-list ip ACL_CONTROL_PLANE
 10 comment Permitir servidor Syslog y subred de TI
 10 permit ip 11.39.41.0/24 any
 20 comment Permitir red de gestion local
 20 permit ip 192.168.1.0/24 any
 30 comment Bloquear y contar cualquier otro intento de acceso
 30 deny ip any any count
 exit

apply access-list ip ACL_CONTROL_PLANE control-plane vrf default

! -----------------------------------------------------------------------------
! PASO 7: ACCESO REMOTO SEGURO (SSH)
! -----------------------------------------------------------------------------
crypto key generate rsa bits 2048
ssh server vrf default

! Desactivar servidores web HTTP plano
no http-server

! -----------------------------------------------------------------------------
! PASO 8: CONFIGURACION DE VLAN 1 Y DIRECCION IP DE GESTION
! -----------------------------------------------------------------------------
vlan 1
 name DEFAULT_VLAN
 no shutdown
 exit

interface vlan 1
 description IP_Gestion_Switch
 ip address 192.168.1.1/24
 no shutdown
 exit

ip route 0.0.0.0/0 192.168.1.254

! -----------------------------------------------------------------------------
! PASO 9: ACTIVACION DE DHCP SNOOPING (PROTECCION CONTRA ROUTERS PIRATAS)
! -----------------------------------------------------------------------------
dhcp-snooping
dhcp-snooping vlan 1

! -----------------------------------------------------------------------------
! PASO 10: PUERTOS DE ACCESO (PUERTOS 1/1/1 AL 1/1/23)
! Con VLAN 1, Admin-Edge, BPDU Guard, Port-Access Security y Storm Control
! -----------------------------------------------------------------------------
spanning-tree mode rstp
spanning-tree

interface 1/1/1-1/1/23
 description Puertos_Usuarios_Acceso
 no routing
 vlan access 1
 
 ! Spanning Tree de borde y proteccion BPDU
 spanning-tree port-type admin-edge
 spanning-tree bpdu-guard enable
 
 ! Seguridad de Puerto: permite maximo 2 MACs; apaga el puerto y se reactiva en 300s
 port-access security
 port-access security client-limit 2
 port-access security violation action shutdown
 port-access security violation recovery-timer 300
 
 ! Control de tormentas: limita trafico broadcast y multicast al 5%
 storm-control broadcast 5.0%
 storm-control multicast 5.0%
 storm-control action notify
 
 no shutdown
 exit

! -----------------------------------------------------------------------------
! PASO 11: PUERTO TRONCAL (PUERTO 1/1/24)
! Enlace confiable hacia el Core / Router
! -----------------------------------------------------------------------------
interface 1/1/24
 description UPLINK_TRONCAL_HACIA_CORE
 no routing
 vlan trunk native 1
 vlan trunk allowed all
 
 ! Puerto de confianza para trafico DHCP
 dhcp-snooping trust
 
 no shutdown
 exit

! -----------------------------------------------------------------------------
! PASO 12: CONFIGURACION DEL SERVIDOR SYSLOG (11.39.41.200) Y AUDITORIA
! Monitoreo de inicios de sesion, bloqueos por seguridad y cambios de enlace
! -----------------------------------------------------------------------------
logging 11.39.41.200 severity informational vrf default

! -----------------------------------------------------------------------------
! PASO 13: GUARDAR LA CONFIGURACION EN FLASH
! -----------------------------------------------------------------------------
end
write memory

! =============================================================================
! FIN DE LA CONFIGURACION - SWITCH ARUBA CX EN MAXIMA SEGURIDAD (ULTRA-HARDENED)
! =============================================================================
```
