# 04. NTP, ESTRATOS, AUTENTICACION CRIPTOGRAFICA Y PTP (IEEE 1588)

> **SERVICIOS DE RED CORE (DDI: DNS, DHCP, IPAM) Y GESTION EMPRESARIAL**


---



## 1. POR QUE LA SINCRONIZACION HORARIA ES VITAL EN INFRAESTRUCTURA IT

Tener los relojes desincronizados en routers, switches y servidores causa desastres:
1. Caida de Autenticacion Kerberos (Active Directory): Si la diferencia de reloj
   entre un cliente y el Domain Controller supera los 5 minutos (Skew Time), Windows
   rechaza el inicio de sesion de inmediato.
2. Invalidez de Certificados SSL/TLS: Un certificado puede ser marcado como "Aun no valido"
   o "Expirado" si el reloj del firewall o servidor web tiene fecha incorrecta.
3. Imposibilidad de Analisis Forense (SIEM): En una investigacion de seguridad,
   si el firewall marca un ataque a las 14:02 y la base de datos marca la fuga
   a las 13:58, es imposible correlacionar los eventos del ataque.



## 2. JERARQUIA DE ESTRATOS NTP (STRATUM LEVELS)

El protocolo NTP (RFC 5905 - UDP puerto 123) organiza la distribucion del tiempo
en capas jerarquicas llamadas "Estratos":

  [ ESTRATO 0 ]  Relojes Atomicos de Cesio / Rubidio / Receptores GPS Satelitales
        |        (Hardware fisico puro, no conectado directamente a la red IP)
        v
  [ ESTRATO 1 ]  Servidores de Tiempo Primarios conectados fisicamente al GPS por antena.
        |        (Precision de nanosegundos. Ejemplo: Servidores NTP del Observatorio)
        v
  [ ESTRATO 2 ]  Servidores Corporativos de Datacenter sincronizados por red con Estrato 1.
        |        (Ejemplo: Par de Servidores NTP / Chrony de la empresa)
        v
  [ ESTRATO 3 ]  Routers Core, Switches de Distribucion y Firewalls perimetrales.
        |
        v
  [ ESTRATO 4 ]  Switches de Acceso, Servidores Virtuales y Laptops de usuarios.
        ...
  [ ESTRATO 16]  INDICA DESINCRONIZACION TOTAL (Reloj invalido / No confiable).



## 3. SERVIDOR NTP MODERNO EN LINUX (CHRONY)

Chrony ha reemplazado al antiguo daemon 'ntpd' en RHEL, Rocky Linux y Ubuntu por
su capacidad de sincronizar el reloj casi instantaneamente y tolerar redes con jitter.

Instalacion y configuracion en /etc/chrony/chrony.conf:
# 1. Servidores upstream publicos oficiales
server time.google.com iburst prefer
server time.cloudflare.com iburst
server pool.ntp.org iburst

# 2. Permitir que los dispositivos de la red interna consulten la hora a este servidor
allow 10.0.0.0/8
allow 172.16.0.0/12

# 3. Servir tiempo a la red local aun si la conexion a Internet se corta temporalmente
local stratum 10

# Iniciar el servicio y consultar estado:
sudo systemctl restart chronyd
chronyc sources -v
chronyc tracking



## 4. CONFIGURACION DE NTP SEGURO CON AUTENTICACION EN CISCO Y HUAWEI

Para evitar ataques de suplantacion horaria (NTP Spoofing), se firman los paquetes
NTP con llaves criptograficas SHA-1 o MD5.

Configuracion en Cisco Catalyst / Routers IOS-XE:
! 1. Definir la zona horaria y horario de verano
clock timezone CST -6 0

! 2. Habilitar llaves de autenticacion NTP
ntp authenticate
ntp authentication-key 1 md5 ClaveNtpSegura2026!
ntp trusted-key 1

! 3. Apuntar a los servidores de tiempo corporativos
ntp server 10.50.0.50 key 1 prefer
ntp server 10.50.0.51 key 1
ntp source Loopback0

! 4. Proteger el router para que nadie externo manipule el reloj (NTP Access-Groups)
access-list 10 permit 10.50.0.50
access-list 10 permit 10.50.0.51
ntp access-group peer 10         ! Solo estos servidores pueden cambiar la hora del router

Configuracion en Huawei VRP:
ntp-service authentication enable
ntp-service authentication-keyid 1 authentication-mode md5 cipher ClaveNtpSegura2026!
ntp-service reliable authentication-keyid 1
ntp-service unicast-server 10.50.0.50 authentication-keyid 1 preferred
ntp-service unicast-server 10.50.0.51 authentication-keyid 1
ntp-service source-interface LoopBack0



## 5. PTP (PRECISION TIME PROTOCOL - IEEE 1588V2)

¿Cuando NTP no es suficiente?
- NTP proporciona precision en milisegundos (1 a 10 ms).
- PTP (IEEE 1588v2) proporciona precision en SUB-MICROSEGUNDOS (nanosegundos).

Casos de Uso Obligatorios de PTP:
1. Finanzas y Trading de Alta Frecuencia (HFT): Normativas como MiFID II en Europa
   exigen registrar cada orden de compra/venta con precision de microsegundos.
2. Telecomunicaciones Celulares 5G: La sincronizacion de fase y frecuencia entre
   antenas de radio bases (Open RAN) requiere marcas de tiempo exactas por fibra optica.
3. Subestaciones Electricas Inteligentes (Norma IEC 61850).

Roles de Relojes PTP en la Red:
- Grandmaster Clock (GMC): Reloj maestro con receptor satelital GNSS de maxima pureza.
- Boundary Clock (BC): Switches de red que terminan la sesion PTP, recalculan el retardo
  interno de procesamiento de hardware (Hardware Timestamping) y retransmiten.
- Transparent Clock (TC): Switches que miden el tiempo de transito del paquete PTP
  a traves de su chip ASIC y agregan un campo de correccion (Correction Field).



## 6. VERIFICACION Y COMANDOS DE DIAGNOSTICO

1. Verificar estado de asociacion NTP en Cisco:
```text
   show ntp associations
   ! El servidor seleccionado tendra un asterisco (*) a la izquierda.
   ! Ejemplo: *~10.50.0.50  stratum: 2  offset: 0.42 ms  delay: 2.15 ms

2. Ver sincronizacion global del sistema:
   show ntp status
   ! Debe mostrar: "Clock is synchronized, stratum 3, reference is 10.50.0.50"

3. Ver hora y fecha de hardware (RTC) vs reloj del sistema:
```


`cisco
show clock detail
`
