# 02. CONFIGURACION INICIAL, IDENTIFICACION Y SEGURIDAD DE ACCESO

> **ARUBA NETWORKS (ARUBAOS-CX) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. ASIGNACION DEL NOMBRE DEL DISPOSITIVO (HOSTNAME)

El hostname permite identificar unicamente el switch en la topologia de red:

  switch# configure terminal
  switch(config)# hostname SW-CORE-ARUBA-01
```cisco
  SW-CORE-ARUBA-01(config)#
```


## 2. MENSAJE DE ADVERTENCIA LEGAL (BANNER MOTD)

Configuracion del mensaje de inicio de sesion (Banner del Dia):

```cisco
  SW-CORE-ARUBA-01(config)# banner motd $
  *****************************************************************
  *                 SISTEMA PRIVADO Y CONFIDENCIAL                *
  * El acceso no autorizado a este conmutador esta estrictamente *
  * prohibido y sera procesado bajo las leyes aplicables.         *
  *****************************************************************
  $
```


## 3. CONFIGURACION DE FECHA, HORA Y CLIENTE NTP

Tener la hora sincronizada es esencial para la correlacion de eventos en logs.


### a) Configurar zona horaria:

```cisco
  SW-CORE-ARUBA-01(config)# clock timezone America/Mexico_City
  (O con desfase UTC: clock timezone UTC-6)

b) Configurar servidores de sincronizacion NTP:
  SW-CORE-ARUBA-01(config)# ntp server 192.168.1.50 minpoll 4 maxpoll 6
  SW-CORE-ARUBA-01(config)# ntp server 0.pool.ntp.org
  SW-CORE-ARUBA-01(config)# ntp enable

c) Verificacion:
  SW-CORE-ARUBA-01# show clock
  SW-CORE-ARUBA-01# show ntp status
  SW-CORE-ARUBA-01# show ntp associations
```


## 4. GESTION DE USUARIOS LOCALES Y ROLES (RBAC)

ArubaOS-CX cuenta con control de acceso basado en roles (administrators y operators).


### a) Cambiar contrasena del usuario administrador por defecto (admin):

```cisco
  SW-CORE-ARUBA-01(config)# user admin password
  (El sistema solicitara ingresar la nueva contrasena y su confirmacion).

b) Crear usuarios con roles especificos:
  - Usuario de solo lectura / monitorizacion (Rol 'operators'):
    SW-CORE-ARUBA-01(config)# user auditor group operators password
    (Ingresar contrasena).

  - Usuario con privilegios totales (Rol 'administrators'):
    SW-CORE-ARUBA-01(config)# user ing_redes group administrators password
    (Ingresar contrasena).

c) Bloqueo de intentos fallidos (Proteccion contra fuerza bruta):
  SW-CORE-ARUBA-01(config)# aaa authentication login lockout-period 300
  SW-CORE-ARUBA-01(config)# aaa authentication login max-retries 3
```


## 5. HABILITACION Y SEGURIDAD DE SSH (ACCESO REMOTO SEGURO)

En ArubaOS-CX, SSH se habilita por VRF (Virtual Routing and Forwarding):


### a) Habilitar el servidor SSH en la VRF default (en banda) y/o VRF mgmt (puerto dedicado):

```cisco
  SW-CORE-ARUBA-01(config)# ssh server vrf default
  SW-CORE-ARUBA-01(config)# ssh server vrf mgmt

b) Generar / regenerar llaves criptograficas RSA (minimo 2048 o 4096 bits):
  SW-CORE-ARUBA-01(config)# crypto key generate rsa bits 4096

c) Restringir algoritmos criptograficos debiles (FIPS / Hardening):
  SW-CORE-ARUBA-01(config)# ssh server ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr

d) Verificacion del servicio SSH:
  SW-CORE-ARUBA-01# show ssh server status
```


## 6. INTERFAZ WEB GRAFICA (HTTPS WEB GUI Y REST API)

ArubaOS-CX incluye una potente interfaz grafica web y soporte API REST sobre HTTPS:


### a) Habilitar el servidor HTTPS seguro:

```cisco
  SW-CORE-ARUBA-01(config)# https-server vrf default
  SW-CORE-ARUBA-01(config)# https-server vrf mgmt

b) Asegurar que HTTP plano este deshabilitado (viene apagado por defecto en CX):
  SW-CORE-ARUBA-01(config)# no http-server
```


## 7. PUERTO DEDICADO DE GESTION FUERA DE BANDA (OOBM - INTERFACE MGMT)

La mayoria de los switches ArubaOS-CX incluyen un puerto fisico rotulado "MGMT"
que pertenece exclusivamente a la 'vrf mgmt' aislada del trafico de datos:

```cisco
  SW-CORE-ARUBA-01(config)# interface mgmt
  SW-CORE-ARUBA-01(config-if-mgmt)# no shutdown
  SW-CORE-ARUBA-01(config-if-mgmt)# ip static 10.254.1.10/24
  SW-CORE-ARUBA-01(config-if-mgmt)# default-gateway 10.254.1.1
  SW-CORE-ARUBA-01(config-if-mgmt)# exit

Verificar conexion de gestion:
  SW-CORE-ARUBA-01# ping 10.254.1.1 vrf mgmt
```


## 8. INTEGRACION DE AUTENTICACION CENTRALIZADA (RADIUS / TACACS+)


### a) Configuracion de servidor RADIUS (ej. Aruba ClearPass / FreeRADIUS):

```cisco
  SW-CORE-ARUBA-01(config)# radius-server host 192.168.10.25 key plaintext SecretoRadius123 vrf default
  SW-CORE-ARUBA-01(config)# aaa authentication login default group radius local

b) Configuracion de servidor TACACS+ (ej. Cisco ISE / Aruba TACACS):
  SW-CORE-ARUBA-01(config)# tacacs-server host 192.168.10.30 key plaintext SecretoTacacs123 vrf default
  SW-CORE-ARUBA-01(config)# aaa authentication login default group tacacs local
  SW-CORE-ARUBA-01(config)# aaa authorization commands default group tacacs local
```


## 9. CONTROL DE TIEMPO DE ESPERA (TIMEOUT DE SESION)

Evita que sesiones de consola o SSH queden abiertas indefinidamente:


## SW-CORE-ARUBA-01(config)# session-timeout 15   (en minutos, 0 para desactivar)
