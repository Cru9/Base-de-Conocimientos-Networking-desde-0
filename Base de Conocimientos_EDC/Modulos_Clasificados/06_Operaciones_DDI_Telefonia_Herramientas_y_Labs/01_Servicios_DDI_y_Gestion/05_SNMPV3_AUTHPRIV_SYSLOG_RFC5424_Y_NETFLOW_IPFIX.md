# 05. TELEMETRIA, SNMPV3 (AUTHPRIV), SYSLOG (RFC 5424) Y NETFLOW/IPFIX

> **SERVICIOS DE RED CORE (DDI: DNS, DHCP, IPAM) Y GESTION EMPRESARIAL**


---



## 1. LOS TRES PILARES DE LA OBSERVABILIDAD DE RED

Para operar una red corporativa con nivel de servicio 99.999%, se requieren tres
fuentes de telemetria complementarias:
1. SNMPv3 (Metricas de Salud): Consulta periodica (Polling cada 1 a 5 min) de CPU,
   memoria RAM, temperatura, errores CRC en puertos y volumen agregado de trafico.
2. Syslog (Notificaciones de Eventos): Mensajes en tiempo real que emite el equipo
   cuando ocurre un cambio de estado (ej. caida de enlace, inicio de sesion SSH, flap de OSPF).
3. NetFlow / IPFIX (Analisis de Conversaciones y Ancho de Banda): Detalle forense de
   cada flujo de comunicacion (IP origen, IP destino, puerto, aplicacion y bytes).



## 2. POR QUE SNMPV1 Y SNMPV2C ESTAN TERMINANTEMENTE PROHIBIDOS

Las versiones 1 y 2c de SNMP transmiten la palabra clave ("Community String", como
el clasico 'public' o 'private') en texto plano sin cifrar.
Cualquier persona con Wireshark en la red puede capturar la clave y:
- Mapear toda la topologia y direccionamiento interno de la empresa.
- Si la comunidad tiene permisos de escritura (RW), alterar tablas de ruteo o reiniciar switches.

SNMPV3 Y EL MODELO DE SEGURIDAD BASADO EN USUARIO (USM):
SNMPv3 introduce tres niveles de seguridad:
1. noAuthNoPriv: Sin autenticacion y sin cifrado (inseguro).
2. authNoPriv:   Autenticado con hash criptografico (SHA), pero trafico sin cifrar.
3. authPriv:     MAXIMA SEGURIDAD. Autenticacion con SHA-256 Y CIFRADO del paquete
                 completo con AES-128 o AES-256.



## 3. CONFIGURACION DE SNMPV3 (AUTHPRIV) EN CISCO IOS-XE

! 1. Definir una Vista SNMP para limitar a que ramas OID tiene acceso el NMS
snmp-server view VISTA_MONITOREO iso included

! 2. Crear el Grupo SNMPv3 con nivel authPriv y vincularlo a la vista
snmp-server group GRP_MONITOREO_NOC v3 priv read VISTA_MONITOREO

! 3. Crear el Usuario SNMPv3 con autenticacion SHA y cifrado AES-128
snmp-server user usr_noc GRP_MONITOREO_NOC v3 auth sha ClaveAutenticacionSha2026! priv aes 128 ClaveCifradoAes2026!

! 4. Restringir mediante ACL que solo la IP del servidor de monitoreo (PRTG/Zabbix) consulte
access-list 15 permit 10.50.0.100
snmp-server group GRP_MONITOREO_NOC v3 priv access 15

! 5. Enviar alertas asincronas (SNMP Traps) al NMS ante fallas de hardware
snmp-server enable traps
snmp-server host 10.50.0.100 version 3 priv usr_noc



## 4. CONFIGURACION DE SYSLOG CENTRALIZADO (RFC 5424)

Niveles de Severidad Syslog (0 es el mas critico, 7 es el mas detallado):
0 = Emergency, 1 = Alert, 2 = Critical, 3 = Error, 4 = Warning, 5 = Notice, 6 = Info, 7 = Debug.

Configuracion en Cisco IOS-XE:
! 1. Habilitar marcas de tiempo precisas con fecha, hora y milisegundos
service timestamps log datetime msec localtime show-timezone
service timestamps debug datetime msec localtime show-timezone
service sequence-numbers

! 2. Apuntar al servidor colector de logs central (Graylog / Splunk / ELK)
logging host 10.50.0.120 transport udp port 514
logging source-interface Loopback0
logging trap warnings             ! Enviar mensajes de severidad 4 o mas critica
logging buffered 64000 debugging  ! Guardar historial local en bufer de memoria



## 5. CONFIGURACION DE NETFLOW FLEXIBLE (FNF) / IPFIX

NetFlow permite saber con exactitud matematica que empleado o servidor esta
saturando el enlace a Internet o la WAN:

! 1. Definir el Registro de Flujo (Flow Record) - Que informacion capturar
flow record REC_TRAFICO_CORP
 match ipv4 tos
 match ipv4 protocol
 match ipv4 source address
 match ipv4 destination address
 match transport source-port
 match transport destination-port
 match interface input
 collect transport tcp flags
 collect counter bytes long
 collect counter packets long
 collect timestamp sys-uptime first
 collect timestamp sys-uptime last

! 2. Definir el Exportador de Flujo (Flow Exporter) - A que colector enviar los datos
flow exporter EXP_A_NETFLOW_ANALYZER
 destination 10.50.0.130
 transport udp 2055
 source Loopback0
 template data timeout 60

! 3. Crear el Monitor de Flujo (Flow Monitor) - Une el registro con el exportador
flow monitor MON_TRAFICO_WAN
 record REC_TRAFICO_CORP
 exporter EXP_A_NETFLOW_ANALYZER
 cache timeout active 60
 cache timeout inactive 15

! 4. Aplicar el monitor a la interfaz WAN de enlace
```text
interface GigabitEthernet0/0/1
 description ENLACE_WAN_A_INTERNET
 ip flow monitor MON_TRAFICO_WAN input
 ip flow monitor MON_TRAFICO_WAN output
```


## 6. VERIFICACION Y COMANDOS DE DIAGNOSTICO

1. Verificar estado y estadisticas de SNMPv3:
```text
   show snmp user
   show snmp group

2. Ver el historial de eventos de Syslog en la memoria local:
   show logging

3. Ver el flujo de trafico activo en memoria de NetFlow:
   show flow monitor MON_TRAFICO_WAN cache format table
   ! Muestra las conexiones en vivo con IP origen/destino, puertos y bytes transferidos.

4. Verificar que el exportador de NetFlow este enviando paquetes UDP al colector:
```


`cisco
show flow exporter EXP_A_NETFLOW_ANALYZER statistics
`
