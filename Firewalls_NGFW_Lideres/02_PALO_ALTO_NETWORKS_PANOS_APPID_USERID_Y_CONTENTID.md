# 02. PALO ALTO NETWORKS (PAN-OS): APP-ID, USER-ID, CONTENT-ID Y PANORAMA

> **FIREWALLS DE PROXIMA GENERACION (NGFW) POR MARCA LIDER**


---



## 1. LA REVOLUCION DE PALO ALTO: LOS TRES PILARES DE PAN-OS

Palo Alto Networks invento el termino NGFW fundamentandose en tres tecnologias
de inspeccion concurrentes en su arquitectura de software PAN-OS:

1. App-ID (Identificacion de Aplicaciones):
   - No clasifica por numero de puerto; examina el trafico a nivel de aplicacion.
   - Detecta evasion (tuneles SSH, SSL con puertos anomalos, evasion por proxy).
   - Mas de 3,800 aplicaciones clasificadas de forma granular (por ejemplo: distingue
     entre navegar en 'facebook-base', transferir archivos en 'facebook-file-upload'
     o mandar mensajes en 'facebook-chat').

2. User-ID (Identificacion de Usuarios y Grupos):
   - Mapea de forma transparente la direccion IP origen al nombre de usuario
     y grupos de seguridad del Active Directory (sin obligar a autenticarse en el firewall).
   - Se alimenta mediante:
     * Lectura de Event Logs de Windows Server (Event ID 4624 - Logon).
     * Agentes User-ID dedicados o lectura WMI sin agente.
     * Syslog listeners de servidores RADIUS / Cisco ISE / VPN.
     * GlobalProtect (cliente de VPN / Zero Trust).

3. Content-ID (Inspeccion de Contenido y Prevencion de Amenazas):
   - Escanea el trafico en busca de amenazas mediante 4 perfiles esenciales:
     * Antivirus: Bloquea troyanos, virus, gusanos y ransomware en tiempo real.
     * Anti-Spyware: Detecta balizas (beacons) y comandos de servidores C2 (Command & Control).
       Incluye DNS Sinkholing para redirigir consultas maliciosas a una IP trampa.
     * Vulnerability Protection: Escudo contra exploits que atacan vulnerabilidades
       en sistemas operativos y navegadores (CVEs, Log4j, desbordamientos de bufer).
     * WildFire: Analisis dinamico de archivos en Sandboxing. Si un archivo es desconocido,
       se sube a la nube de Palo Alto, se detona en una maquina virtual y en menos
       de 5 minutos se distribuye una firma de proteccion a nivel global.



## 2. CONFIGURACION EN CLI DE PAN-OS (ESTRUCTURA JERARQUICA 'SET')

! 1. Definir Zonas de Seguridad
set zone trust network layer3 ethernet1/2
set zone untrust network layer3 ethernet1/1
set zone dmz network layer3 ethernet1/3

! 2. Crear objetos de direccion y grupos
set address HOST_DC_01 ip-netmask 10.10.10.10/32
set address NET_USUARIOS_CORP ip-netmask 10.10.20.0/24

! 3. Crear Regla NAT de Salida (Dynamic IP and Port - Hide NAT)
set rulebase nat rules NAT_SALIDA_INTERNET from trust
set rulebase nat rules NAT_SALIDA_INTERNET to untrust
set rulebase nat rules NAT_SALIDA_INTERNET source NET_USUARIOS_CORP
set rulebase nat rules NAT_SALIDA_INTERNET destination any
set rulebase nat rules NAT_SALIDA_INTERNET service any
set rulebase nat rules NAT_SALIDA_INTERNET source-translation dynamic-ip-and-port interface-address interface ethernet1/1

! 4. Crear Perfil de Grupo de Seguridad (Security Profile Group)
set profiles security-profile-group SEC_PROFILE_STANDARD
set profiles security-profile-group SEC_PROFILE_STANDARD virus default
set profiles security-profile-group SEC_PROFILE_STANDARD spyware strict
set profiles security-profile-group SEC_PROFILE_STANDARD vulnerability strict
set profiles security-profile-group SEC_PROFILE_STANDARD wildfire-analysis default
set profiles security-profile-group SEC_PROFILE_STANDARD url-filtering default

! 5. Crear Regla de Seguridad NGFW con App-ID, User-ID y Content-ID
set rulebase security rules REGLA_USUARIOS_CORP_INTERNET from trust
set rulebase security rules REGLA_USUARIOS_CORP_INTERNET to untrust
set rulebase security rules REGLA_USUARIOS_CORP_INTERNET source NET_USUARIOS_CORP
set rulebase security rules REGLA_USUARIOS_CORP_INTERNET source-user "CORP\Domain Users"
set rulebase security rules REGLA_USUARIOS_CORP_INTERNET destination any
set rulebase security rules REGLA_USUARIOS_CORP_INTERNET application [ web-browsing ssl ms-office365-base dns ping ]
set rulebase security rules REGLA_USUARIOS_CORP_INTERNET service application-default
set rulebase security rules REGLA_USUARIOS_CORP_INTERNET action allow
set rulebase security rules REGLA_USUARIOS_CORP_INTERNET profile-setting group SEC_PROFILE_STANDARD
set rulebase security rules REGLA_USUARIOS_CORP_INTERNET log-start no
set rulebase security rules REGLA_USUARIOS_CORP_INTERNET log-end yes

! 6. Regla de Bloqueo Explicito de Alto Riesgo (Peer-to-Peer y Anonimizadores)
set rulebase security rules REGLA_BLOQUEAR_RIESGO from trust
set rulebase security rules REGLA_BLOQUEAR_RIESGO to untrust
set rulebase security rules REGLA_BLOQUEAR_RIESGO source any
set rulebase security rules REGLA_BLOQUEAR_RIESGO destination any
set rulebase security rules REGLA_BLOQUEAR_RIESGO application [ bittorrent tor ultrasurf crypto-mining ]
set rulebase security rules REGLA_BLOQUEAR_RIESGO action drop
set rulebase security rules REGLA_BLOQUEAR_RIESGO log-end yes

! 7. IMPORTANTE: En Palo Alto los cambios no se aplican hasta confirmar con commit
commit



## 3. ALTA DISPONIBILIDAD (HA) EN PAN-OS: ACTIVE/PASSIVE

Palo Alto utiliza dos enlaces dedicados para su cluster de Alta Disponibilidad:
- HA1 (Control Link): Sincroniza configuraciones, estado de nodos y keepalives (TCP 28769).
  Posee un enlace de respaldo llamado HA1-Backup para evitar Split-Brain.
- HA2 (Data Link): Sincroniza en tiempo real las tablas de sesiones y tablas ARP (EtherType 0x7261).

Configuracion en el Nodo Primario:
set deviceconfig high-availability group 1 mode active-passive
set deviceconfig high-availability group 1 election-option priority 50   ! Menor numero = Mas prioridad
set deviceconfig high-availability group 1 election-option preempt yes  ! Retoma liderazgo al recuperarse
set deviceconfig high-availability interface ha1 ip-address 10.0.0.1 netmask 255.255.255.252
set deviceconfig high-availability interface ha2 ip-address 10.0.1.1 netmask 255.255.255.252
set deviceconfig high-availability enabled yes
commit



## 4. GESTION CENTRALIZADA CON PANORAMA

En empresas con decenas o cientos de firewalls Palo Alto, la administracion se realiza
mediante la plataforma centralizada Panorama:
- Device Groups: Jerarquia de politicas de seguridad heredables (Shared -> Regional -> Local).
- Templates & Template Stacks: Estandarizacion de configuracion de red, interfaces y ruteo.
- Centralized Logging: Todos los firewalls envian sus logs a Panorama para analisis
  y busquedas forenses unificadas.



## 5. COMANDOS DE MONITOREO Y VERIFICACION EN CLI

1. Verificar estado de Alta Disponibilidad:
```text
   show high-availability state
   ! Debe mostrar: Local: active, Peer: passive, Synchronization: synchronized

2. Comprobar que regla de seguridad hara match para un paquete simulado:
   test security-policy-match from trust to untrust source 10.10.20.50 destination 8.8.8.8 protocol 6 destination-port 443 application ssl
   ! Muestra de inmediato cual regla aceptara o descartara el paquete sin generar trafico real.

3. Monitorear sesiones activas en el motor de hardware:
   show session all filter source 10.10.20.50
```


`cisco
show session id 142058
`
