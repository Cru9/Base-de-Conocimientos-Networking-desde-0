# 02. CONFIGURACION INICIAL, IDENTIFICACION Y SEGURIDAD DE ACCESO

> **TP-LINK (JETSTREAM SWITCHES) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. ASIGNACION DEL NOMBRE DEL DISPOSITIVO (HOSTNAME)

El nombre del switch facilita su identificacion en la consola y en la red:

  TP-LINK# configure
  TP-LINK(config)# hostname SW-DISTRIB-TPLINK-01
```cisco
  SW-DISTRIB-TPLINK-01(config)#
```


## 2. MENSAJE DE ADVERTENCIA LEGAL (BANNER MOTD)

Configura una advertencia disuasoria antes de solicitar credenciales de acceso:


## SW-DISTRIB-TPLINK-01(config)# banner motd #

  ATENCION: Acceso restringido exclusivamente a personal de TI.

## Cualquier ingreso no autorizado sera reportado y sancionado.

  #



## 3. CONFIGURACION DE HORA, ZONA HORARIA Y CLIENTE NTP / SNTP

Tener el reloj sincronizado garantiza que los registros (logs) sean confiables.


### a) Configurar zona horaria:

```cisco
  SW-DISTRIB-TPLINK-01(config)# system-time timezone UTC-6

b) Habilitar sincronizacion por SNTP/NTP y definir servidores:
  SW-DISTRIB-TPLINK-01(config)# sntp enable
  SW-DISTRIB-TPLINK-01(config)# sntp server 192.168.1.50
  SW-DISTRIB-TPLINK-01(config)# sntp server 0.pool.ntp.org
  SW-DISTRIB-TPLINK-01(config)# sntp poll-interval 3600   (en segundos)

c) Verificacion:
  SW-DISTRIB-TPLINK-01# show system-time
```


## 4. GESTION DE USUARIOS LOCALES Y NIVELES DE PRIVILEGIO

TP-Link maneja usuarios con diferentes niveles de acceso:
- admin (privilegio total, equivalente a nivel 15)
- operator (monitoreo y consultas basicas)
- user (solo lectura basica)


### a) Crear cuenta de administrador:

```cisco
  SW-DISTRIB-TPLINK-01(config)# user name admin privilege admin secret AdminSegura2026!

b) Crear cuenta de operador / soporte nivel 1:
  SW-DISTRIB-TPLINK-01(config)# user name soporte privilege operator secret SoportePass123!

c) Proteger el acceso al modo privilegiado (Enable Secret):
  SW-DISTRIB-TPLINK-01(config)# enable secret EnablePasswordClave99!
```


## 5. HABILITACION DE SSHv2 (ACCESO REMOTO CIFRADO)


### a) Generar las llaves criptograficas RSA para el servidor SSH:

```cisco
  SW-DISTRIB-TPLINK-01(config)# crypto key generate rsa
  (Seleccionar 2048 bits cuando sea solicitado).

b) Habilitar el servidor SSH y forzar version 2:
  SW-DISTRIB-TPLINK-01(config)# ip ssh server
  SW-DISTRIB-TPLINK-01(config)# ip ssh version 2

c) Apagar el servidor Telnet por seguridad (inseguro y texto plano):
  SW-DISTRIB-TPLINK-01(config)# no ip telnet server
```


## 6. SEGURIDAD DE LA INTERFAZ WEB (HTTPS / HTTP)


### a) Habilitar acceso web seguro (HTTPS / SSL):

```cisco
  SW-DISTRIB-TPLINK-01(config)# ip http secure-server

b) Deshabilitar HTTP en texto plano:
  SW-DISTRIB-TPLINK-01(config)# no ip http server
```


## 7. CONFIGURACION DE TIEMPO DE ESPERA (TIMEOUT DE SESION)

Cierra automaticamente las sesiones inactivas de consola y lineas virtuales (VTY):

```cisco
  SW-DISTRIB-TPLINK-01(config)# line console 0
  SW-DISTRIB-TPLINK-01(config-line)# exec-timeout 10   (10 minutos)
  SW-DISTRIB-TPLINK-01(config-line)# exit

  SW-DISTRIB-TPLINK-01(config)# line vty 0 4
  SW-DISTRIB-TPLINK-01(config-line)# exec-timeout 10
  SW-DISTRIB-TPLINK-01(config-line)# exit
```


## 8. AUTENTICACION CENTRALIZADA RADIUS (OPCIONAL)

Para integrar con servidores de autenticacion como FreeRADIUS, NPS o ClearPass:

```cisco
  SW-DISTRIB-TPLINK-01(config)# radius-server host 192.168.10.25 key ClaveRadius123
  SW-DISTRIB-TPLINK-01(config)# aaa authentication login default radius local
```


## 9. VERIFICACION Y COMANDOS DE DIAGNOSTICO

Visualizar usuarios creados en el sistema:
```cisco
  SW-DISTRIB-TPLINK-01# show user-account

Visualizar estado del servicio SSH:
  SW-DISTRIB-TPLINK-01# show ip ssh

Visualizar estado de los servicios web (HTTP / HTTPS):
```


## SW-DISTRIB-TPLINK-01# show ip http
