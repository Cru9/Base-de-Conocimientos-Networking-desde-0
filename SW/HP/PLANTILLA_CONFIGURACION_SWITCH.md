# HP (PROCURVE / PROVISION / ARUBAOS-S) - PLANTILLA ULTRA-HARDENED (SEGURIDAD MAXIMA)


---

Descripcion: Configuracion corporativa de maxima seguridad (Hardening Enterprise).
Incluye:
- Usuario Manager con clave maestra y autenticacion local estricta.
- Bloqueo de acceso administrativo mediante IP Authorized-Managers.
- Sincronizacion horaria SNTP y Banner de advertencia legal.
- VLAN 1 de gestion (192.168.1.1/24) con Default Gateway (192.168.1.254).
- Puertos de acceso (1-23): BPDU Protection, Port Security (max 2 MACs) y Rate-Limit.
- Autorrecuperacion de puertos por BPDU Protection en 300 segundos.
- DHCP Snooping contra servidores DHCP piratas.
- Puerto troncal (24) marcado como Confiable (Trust).

## - Servidor Syslog centralizado (11.39.41.200) con auditoria de red.


! -----------------------------------------------------------------------------
! PASO 1: MODO CONFIGURACION GLOBAL
! -----------------------------------------------------------------------------
configure

! -----------------------------------------------------------------------------
! PASO 2: ASIGNACION DE NOMBRE Y BANNER LEGAL
! -----------------------------------------------------------------------------
hostname "SW-HP-PRODUCCION"

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
time timezone -360
sntp server priority 1 11.39.41.200
sntp unicast
timesync sntp

! -----------------------------------------------------------------------------
! PASO 4: CREACION DE USUARIO DE MAXIMO NIVEL (MANAGER) Y CONTRASENA
! -----------------------------------------------------------------------------
password manager user-name admin plaintext CONTRASEÑA_MASTER

aaa authentication login privilege-mode
aaa authentication console login local
aaa authentication ssh login local
aaa authentication telnet login local

! -----------------------------------------------------------------------------
! PASO 5: RESTRICCION DE GESTION ADMINISTRATIVA (IP AUTHORIZED-MANAGERS)
! Solo las IPs autorizadas podran abrir sesiones SSH/Telnet/Web/SNMP
! -----------------------------------------------------------------------------
ip authorized-managers 11.39.41.0 255.255.255.0 access manager
ip authorized-managers 192.168.1.0 255.255.255.0 access manager

! -----------------------------------------------------------------------------
! PASO 6: ACCESO REMOTO SEGURO (SSH / TELNET)
! -----------------------------------------------------------------------------
crypto key generate ssh rsa bits 2048
ip ssh
telnet-server

! Desactivar servidores web inseguros
no web-management plaintext

! -----------------------------------------------------------------------------
! PASO 7: CONFIGURACION DE VLAN 1 Y DIRECCION IP DE GESTION
! -----------------------------------------------------------------------------
```text
vlan 1
   name "DEFAULT_VLAN"
   untagged 1-23
   tagged 24
   ip address 192.168.1.1 255.255.255.0
   exit

ip default-gateway 192.168.1.254

! -----------------------------------------------------------------------------
! PASO 8: AUTORRECUPERACION DE PUERTOS BLOQUEADOS POR BPDU
! Reactiva automaticamente el puerto apagado por BPDU Protection tras 300 seg
! -----------------------------------------------------------------------------
spanning-tree bpdu-protection-timeout 300

! -----------------------------------------------------------------------------
! PASO 9: ACTIVACION DE DHCP SNOOPING (PROTECCION CONTRA ROUTERS PIRATAS)
! -----------------------------------------------------------------------------
dhcp-snooping
dhcp-snooping vlan 1
dhcp-snooping trust 24

! -----------------------------------------------------------------------------
! PASO 10: PUERTOS DE ACCESO (PUERTOS 1 AL 23)
! Con Admin-Edge, BPDU Protection, Port Security (2 MACs) y Rate-Limit de Tormentas
! -----------------------------------------------------------------------------
spanning-tree
spanning-tree 1-23 admin-edge-port
spanning-tree 1-23 bpdu-protection

! Seguridad de Puerto: maximo 2 MACs persistentes; si hay violacion apaga el puerto
port-security 1-23 learn-mode limited-continuous address-limit 2 action send-disable

! Control de tormentas: limita trafico broadcast entrante al 5%
rate-limit bcast in 1-23 percent 5

! -----------------------------------------------------------------------------
! PASO 11: PUERTO TRONCAL (PUERTO 24)
! Transporta las VLANs etiquetadas (tagged) hacia el Core / Router
! -----------------------------------------------------------------------------
vlan 1
   tagged 24
   exit

! -----------------------------------------------------------------------------
! PASO 12: CONFIGURACION DEL SERVIDOR SYSLOG (11.39.41.200) Y AUDITORIA
! Monitoreo de inicios de sesion, bloqueos por seguridad y cambios de enlace
! -----------------------------------------------------------------------------
logging 11.39.41.200
logging severity informational
logging facility local0

! -----------------------------------------------------------------------------
! PASO 13: GUARDAR LA CONFIGURACION EN FLASH
! -----------------------------------------------------------------------------
write memory

! =============================================================================
! FIN DE LA CONFIGURACION - SWITCH HP EN MAXIMA SEGURIDAD (ULTRA-HARDENED)
! =============================================================================
```
