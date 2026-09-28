# 3COM / H3C (COMWARE) - PLANTILLA ULTRA-HARDENED DE PRODUCCION (SEGURIDAD MAXIMA)


---

Descripcion: Configuracion corporativa de maxima seguridad (Hardening Enterprise).
Incluye:
- Usuarios nivel 3 (maximo) con contrasena cifrada y super password.
- Seguridad en consola y lineas VTY blindadas mediante ACL de gestion.
- Sincronizacion de reloj NTP y Banner legal de acceso.
- VLAN 1 de gestion (192.168.1.1/24) con Default Gateway (192.168.1.254).
- Puertos de acceso (1-23): BPDU Protection, Port Security (max 2 MACs) y Storm Suppression.
- Autorrecuperacion temporal de puertos bloqueados (temporizador 300 seg).
- DHCP Snooping contra servidores DHCP no autorizados.
- Puerto troncal (24) marcado como Confiable (Trust).

## - Servidor Syslog centralizado (11.39.41.200) con auditoria de red.


# -----------------------------------------------------------------------------
# PASO 1: VISTA DEL SISTEMA (MODO CONFIGURACION GLOBAL)
# -----------------------------------------------------------------------------
```text
system-view

# -----------------------------------------------------------------------------
# PASO 2: ASIGNACION DE NOMBRE Y BANNER LEGAL
# -----------------------------------------------------------------------------
sysname SW-3COM-PRODUCCION

header login "
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
# PASO 4: CREACION DE USUARIO DE MAXIMO NIVEL (NIVEL 3) Y SUPER PASSWORD
# -----------------------------------------------------------------------------
local-user admin
 password cipher CONTRASEÑA_MASTER
 authorization-attribute level 3
 service-type ssh telnet terminal
quit

super password level 3 cipher CONTRASEÑA_MASTER

# -----------------------------------------------------------------------------
# PASO 5: SEGURIDAD DEL PUERTO DE CONSOLA (AUX 0)
# -----------------------------------------------------------------------------
user-interface aux 0
 authentication-mode scheme
 idle-timeout 10 0
quit

# -----------------------------------------------------------------------------
# PASO 6: LISTA DE CONTROL DE ACCESO (ACL) PARA RESTRINGIR ACCESO A VTY
# Solo permite el ingreso a administracion desde subredes autorizadas
# -----------------------------------------------------------------------------
acl number 2001
 rule 5 permit source 11.39.41.0 0.0.0.255
 rule 10 permit source 192.168.1.0 0.0.0.255
 rule 15 deny
quit

# -----------------------------------------------------------------------------
# PASO 7: ACCESO REMOTO SEGURO (SSH / TELNET) EN LINEAS VTY
# -----------------------------------------------------------------------------
public-key local create rsa
 (Aceptar 2048 bits cuando sea solicitado)

ssh server enable
telnet server enable

ssh user admin service-type stelnet authentication-type password

user-interface vty 0 4
 authentication-mode scheme
 protocol inbound all
 acl 2001 inbound
 idle-timeout 10 0
quit

# -----------------------------------------------------------------------------
# PASO 8: CONFIGURACION DE VLAN 1 Y DIRECCION IP DE GESTION
# -----------------------------------------------------------------------------
vlan 1
 description Administracion_Gestion
quit

interface Vlan-interface 1
 description IP_Gestion_Switch
 ip address 192.168.1.1 255.255.255.0
 undo shutdown
quit

ip route-static 0.0.0.0 0.0.0.0 192.168.1.254

# -----------------------------------------------------------------------------
# PASO 9: ACTIVACION DE DHCP SNOOPING (PROTECCION CONTRA ROUTERS PIRATAS)
# -----------------------------------------------------------------------------
dhcp-snooping

# -----------------------------------------------------------------------------
# PASO 10: PUERTOS DE ACCESO (PUERTOS 1/0/1 AL 1/0/23)
# Con VLAN 1, Edged-port, BPDU Protection, Port Security (2 MACs) y Supresion
# -----------------------------------------------------------------------------
stp mode rstp
stp enable
stp bpdu-protection

# Temporizador para rehabilitar puertos bloqueados por seguridad tras 300 segundos
port-security timer disableport 300

port-group manual PG_PUERTOS_ACCESO
 group-member GigabitEthernet 1/0/1 to GigabitEthernet 1/0/23
 port link-type access
 port access vlan 1
 
 # Spanning Tree de borde
 stp edged-port enable
 
 # Seguridad de Puerto: maximo 2 MACs autologeadas; apaga el puerto temporalmente por 300s
 port-security enable
 port-security max-mac-count 2
 port-security mode autolearn
 port-security intrusion-mode disableport-temporarily
 
 # Supresion de tormentas: limita trafico broadcast y multicast al 5%
 broadcast-suppression 5
 multicast-suppression 5
 
 undo shutdown
quit

# -----------------------------------------------------------------------------
# PASO 11: PUERTO TRONCAL (PUERTO 1/0/24)
# Enlace confiable hacia el Core / Router
# -----------------------------------------------------------------------------
interface GigabitEthernet 1/0/24
 description UPLINK_TRONCAL_HACIA_CORE
 port link-type trunk
 port trunk permit vlan all
 
 # Definir como puerto de confianza para DHCP
 dhcp-snooping trust
 
 undo shutdown
quit

# -----------------------------------------------------------------------------
# PASO 12: CONFIGURACION DEL SERVIDOR SYSLOG (11.39.41.200) Y AUDITORIA
# Monitoreo centralizado de logins, bloqueos por seguridad y cambios de enlace
# -----------------------------------------------------------------------------
info-center enable
info-center loghost 11.39.41.200

# -----------------------------------------------------------------------------
# PASO 13: GUARDAR LA CONFIGURACION EN FLASH
# -----------------------------------------------------------------------------
return
save
 (Confirmar con 'y' y presionar Enter)

# =============================================================================
# FIN DE LA CONFIGURACION - SWITCH 3COM EN MAXIMA SEGURIDAD (ULTRA-HARDENED)
# =============================================================================
```
