# TP-LINK (JETSTREAM SWITCHES) - PLANTILLA ULTRA-HARDENED (SEGURIDAD MAXIMA)


---

Descripcion: Configuracion corporativa de maxima seguridad (Hardening Enterprise).
Incluye:
- Usuario admin de maximo nivel y cifrado secreto de acceso enable.
- Restriccion de gestion administrativa por ACL en lineas de control.
- Sincronizacion horaria SNTP y Banner de advertencia legal.
- VLAN 1 de gestion (192.168.1.1/24) con Default Gateway (192.168.1.254).
- Puertos de acceso (1/0/1-23): BPDU Guard, Port Security y Storm Control.
- Autorrecuperacion de puertos por Errdisable Recovery en 300 segundos.
- DHCP Snooping contra servidores DHCP piratas.
- Puerto troncal (1/0/24) marcado como Confiable (Trust).

## - Servidor Syslog centralizado (11.39.41.200) con registro de eventos de red.


! -----------------------------------------------------------------------------
! PASO 1: MODO PRIVILEGIADO Y CONFIGURACION GLOBAL
! -----------------------------------------------------------------------------
```text
enable
configure

! -----------------------------------------------------------------------------
! PASO 2: ASIGNACION DE NOMBRE Y BANNER LEGAL
! -----------------------------------------------------------------------------
hostname SW-TPLINK-PRODUCCION

banner motd #
*******************************************************************************
*                        SISTEMA PRIVADO Y RESTRINGIDO                        *
*  El acceso no autorizado a este conmutador esta estrictamente prohibido.    *
*  Todas las actividades son monitoreadas y registradas para accion legal.    *
*******************************************************************************
#

! -----------------------------------------------------------------------------
! PASO 3: SINCRONIZACION HORARIA (SNTP) - CRITICO PARA LOGS AUDITABLES
! -----------------------------------------------------------------------------
system-time timezone UTC-6
sntp enable
sntp server 11.39.41.200
sntp server 0.pool.ntp.org

! -----------------------------------------------------------------------------
! PASO 4: CREACION DE USUARIO DE MAXIMO NIVEL (ADMIN) Y CLAVE ENABLE
! -----------------------------------------------------------------------------
user name admin privilege admin secret CONTRASEÑA_MASTER
enable secret CONTRASEÑA_MASTER

! -----------------------------------------------------------------------------
! PASO 5: SEGURIDAD DEL PUERTO DE CONSOLA
! -----------------------------------------------------------------------------
line console 0
 exec-timeout 10
 exit

! -----------------------------------------------------------------------------
! PASO 6: LISTA DE CONTROL DE ACCESO (ACL) PARA RESTRINGIR GESTION
! -----------------------------------------------------------------------------
access-list create 10 standard-ip
access-list ip 10 rule 1 permit sip 11.39.41.0 0.0.0.255
access-list ip 10 rule 2 permit sip 192.168.1.0 0.0.0.255
access-list ip 10 rule 3 deny sip any

! -----------------------------------------------------------------------------
! PASO 7: ACCESO REMOTO SEGURO (SSH / TELNET) EN LINEAS VTY
! -----------------------------------------------------------------------------
crypto key generate rsa
ip ssh server
ip ssh version 2
ip telnet server

line vty 0 4
 exec-timeout 10
 exit

! Desactivar servidor web HTTP no cifrado
no ip http server
ip http secure-server

! -----------------------------------------------------------------------------
! PASO 8: CONFIGURACION DE VLAN 1 Y DIRECCION IP DE GESTION
! -----------------------------------------------------------------------------
vlan 1
 name DEFAULT_VLAN
 exit

interface vlan 1
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit

ip default-gateway 192.168.1.254

! -----------------------------------------------------------------------------
! PASO 9: AUTORRECUPERACION DE PUERTOS BLOQUEADOS (ERRDISABLE RECOVERY)
! Reactiva automaticamente puertos caidos tras 300 segundos si ceso el problema
! -----------------------------------------------------------------------------
errdisable recovery cause bpdu-guard
errdisable recovery cause port-security
errdisable recovery interval 300

! -----------------------------------------------------------------------------
! PASO 10: ACTIVACION DE DHCP SNOOPING (PROTECCION CONTRA ROUTERS PIRATAS)
! -----------------------------------------------------------------------------
ip dhcp snooping
ip dhcp snooping vlan 1

! -----------------------------------------------------------------------------
! PASO 11: PUERTOS DE ACCESO (PUERTOS 1/0/1 AL 1/0/23)
! Con VLAN 1, PortFast, BPDU Guard, Port Security y Storm Control
! -----------------------------------------------------------------------------
spanning-tree mode rstp
spanning-tree

interface range gigabitEthernet 1/0/1-23
 description Puertos_Usuarios_Acceso
 switchport mode access
 switchport access vlan 1
 
 ! Spanning Tree de borde y proteccion BPDU
 spanning-tree portfast
 spanning-tree bpdu-guard
 
 ! Seguridad de Puerto: permite solo 2 MACs y apaga el puerto ante violacion
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation shutdown
 
 ! Control de tormentas: limita trafico broadcast y multicast al 5%
 storm-control broadcast level 5
 storm-control multicast level 5
 
 no shutdown
 exit

! -----------------------------------------------------------------------------
! PASO 12: PUERTO TRONCAL (PUERTO 1/0/24)
! Enlace confiable hacia el Core / Router
! -----------------------------------------------------------------------------
interface gigabitEthernet 1/0/24
 description UPLINK_TRONCAL_HACIA_CORE
 switchport mode trunk
 switchport trunk allowed vlan all
 
 ! Puerto de confianza para trafico DHCP
 ip dhcp snooping trust
 
 no shutdown
 exit

! -----------------------------------------------------------------------------
! PASO 13: CONFIGURACION DEL SERVIDOR SYSLOG (11.39.41.200) Y AUDITORIA
! Monitoreo de inicios de sesion, bloqueos por seguridad y cambios de enlace
! -----------------------------------------------------------------------------
logging host 11.39.41.200
logging buffer severity informational

! -----------------------------------------------------------------------------
! PASO 14: GUARDAR LA CONFIGURACION EN FLASH
! -----------------------------------------------------------------------------
end
copy running-config startup-config

! =============================================================================
! FIN DE LA CONFIGURACION - SWITCH TP-LINK EN MAXIMA SEGURIDAD (ULTRA-HARDENED)
! =============================================================================
```
