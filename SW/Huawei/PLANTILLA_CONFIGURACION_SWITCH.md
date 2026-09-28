# HUAWEI (VRP) - PLANTILLA ULTRA-HARDENED DE PRODUCCION (SEGURIDAD MAXIMA)


---

Descripcion: Configuracion corporativa de maxima seguridad (Hardening Enterprise).
Incluye:
- Usuarios nivel 15 y cifrado irreversible en base AAA.
- Seguridad en consola y lineas VTY blindadas mediante ACL de gestion.
- Sincronizacion horaria NTP y Banner de advertencia legal.
- VLAN 1 de gestion (192.168.1.1/24) con Default Gateway (192.168.1.254).
- Puertos de acceso (1-23): BPDU Protection, Port Security (max 2 MACs) y Storm Control.
- Autorrecuperacion de puertos bloqueados (Error-Down Auto-Recovery en 300 seg).
- DHCP Snooping contra servidores DHCP piratas.
- Puerto troncal (24) marcado como Confiable (Trusted).

## - Servidor Syslog centralizado (11.39.41.200) con auditoria de logins y enlaces.


# -----------------------------------------------------------------------------
# PASO 1: VISTA DEL SISTEMA (MODO CONFIGURACION GLOBAL)
# -----------------------------------------------------------------------------
```text
system-view

# -----------------------------------------------------------------------------
# PASO 2: ASIGNACION DE NOMBRE Y BANNER LEGAL
# -----------------------------------------------------------------------------
sysname SW-HUAWEI-PRODUCCION

header login information "
*******************************************************************************
*                        SISTEMA PRIVADO Y RESTRINGIDO                        *
*  El acceso no autorizado a este conmutador esta estrictamente prohibido.    *
*  Todas las actividades son monitoreadas y registradas para accion legal.    *
*******************************************************************************
"

# -----------------------------------------------------------------------------
# PASO 3: SINCRONIZACION HORARIA (NTP) - CRITICO PARA LOGS AUDITABLES
# -----------------------------------------------------------------------------
clock timezone UTC-6 minus 06:00:00
ntp-service enable
ntp-service unicast-server 11.39.41.200

# -----------------------------------------------------------------------------
# PASO 4: CREACION DE USUARIO ADMINISTRADOR EN BASE AAA
# -----------------------------------------------------------------------------
aaa
 local-user admin password irreversible-cipher CONTRASEÑA_MASTER
 local-user admin privilege level 15
 local-user admin service-type terminal ssh telnet
quit

# -----------------------------------------------------------------------------
# PASO 5: SEGURIDAD DEL PUERTO DE CONSOLA
# -----------------------------------------------------------------------------
user-interface con 0
 authentication-mode aaa
 idle-timeout 10 0
quit

# -----------------------------------------------------------------------------
# PASO 6: LISTA DE CONTROL DE ACCESO (ACL) PARA RESTRINGIR ACCESO A VTY
# Solo permite el ingreso a la administracion desde subredes autorizadas
# -----------------------------------------------------------------------------
acl number 2001
 rule 5 permit source 11.39.41.0 0.0.0.255
 rule 10 permit source 192.168.1.0 0.0.0.255
 rule 15 deny
quit

# -----------------------------------------------------------------------------
# PASO 7: ACCESO REMOTO SEGURO (SSH / TELNET) EN LINEAS VTY
# -----------------------------------------------------------------------------
rsa local-key-pair create
 (Aceptar 2048 bits cuando sea solicitado)

stelnet server enable
telnet server enable

ssh user admin authentication-type password
ssh user admin service-type stelnet

user-interface vty 0 4
 authentication-mode aaa
 protocol inbound all
 acl 2001 inbound
 idle-timeout 10 0
quit

# Desactivar servidor web HTTP plano
undo http server enable

# -----------------------------------------------------------------------------
# PASO 8: CONFIGURACION DE VLAN 1 Y DIRECCION IP DE GESTION
# -----------------------------------------------------------------------------
vlan 1
 description Administracion_Gestion
quit

interface Vlanif 1
 description IP_Gestion_Switch
 ip address 192.168.1.1 255.255.255.0
 undo shutdown
quit

ip route-static 0.0.0.0 0.0.0.0 192.168.1.254

# -----------------------------------------------------------------------------
# PASO 9: AUTORRECUPERACION DE PUERTOS BLOQUEADOS (ERROR-DOWN AUTO-RECOVERY)
# Reactiva automaticamente puertos caidos tras 300 segundos si ceso el problema
# -----------------------------------------------------------------------------
error-down auto-recovery cause bpdu-protection interval 300
error-down auto-recovery cause port-security interval 300
error-down auto-recovery cause storm-control interval 300

# -----------------------------------------------------------------------------
# PASO 10: ACTIVACION DE DHCP SNOOPING (PROTECCION CONTRA ROUTERS PIRATAS)
# -----------------------------------------------------------------------------
dhcp enable
dhcp snooping enable
vlan 1
 dhcp snooping enable
quit

# -----------------------------------------------------------------------------
# PASO 11: PUERTOS DE ACCESO (PUERTOS 0/0/1 AL 0/0/23)
# Con VLAN 1, Edged-port, BPDU Protection, Port Security (2 MACs) y Storm Control
# -----------------------------------------------------------------------------
stp mode rstp
stp enable
stp bpdu-protection

port-group PG_PUERTOS_ACCESO
 group-member GigabitEthernet 0/0/1 to GigabitEthernet 0/0/23
 port link-type access
 port default vlan 1
 
 # Spanning Tree de borde
 stp edged-port enable
 
 # Seguridad de Puerto: permite solo 2 MACs y apaga el puerto si hay violacion
 port-security enable
 port-security max-mac-num 2
 port-security protect-type shutdown
 
 # Control de tormentas: limita trafico broadcast y multicast al 5%
 storm-control broadcast percent 5
 storm-control multicast percent 5
 storm-control action error-down
 
 undo shutdown
quit

# -----------------------------------------------------------------------------
# PASO 12: PUERTO TRONCAL (PUERTO 0/0/24)
# Enlace de confianza hacia el Core / Router
# -----------------------------------------------------------------------------
interface GigabitEthernet 0/0/24
 description UPLINK_TRONCAL_HACIA_CORE
 port link-type trunk
 port trunk allow-pass vlan all
 
 # Definir como puerto de confianza para DHCP
 dhcp snooping trusted
 
 undo shutdown
quit

# -----------------------------------------------------------------------------
# PASO 13: CONFIGURACION DEL SERVIDOR SYSLOG (11.39.41.200) Y AUDITORIA
# Monitoreo centralizado de logins, bloqueos por seguridad y cambios de enlace
# -----------------------------------------------------------------------------
info-center enable
info-center loghost 11.39.41.200 facility local0
info-center source default channel loghost log level informational

# -----------------------------------------------------------------------------
# PASO 14: GUARDAR LA CONFIGURACION EN FLASH
# -----------------------------------------------------------------------------
return
save
 (Confirmar con 'y' y presionar Enter)

# =============================================================================
# FIN DE LA CONFIGURACION - SWITCH HUAWEI EN MAXIMA SEGURIDAD (ULTRA-HARDENED)
# =============================================================================
```
