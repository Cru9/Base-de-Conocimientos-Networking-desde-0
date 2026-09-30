# GUIA 3COM COMWARE - PARTE 2: CONFIGURACION INICIAL Y ACCESO SEGURO (SSH / CONSOLA)


---



## 1. CAMBIAR EL NOMBRE DEL SWITCH (SYSNAME)

```text
<3Com> system-view
[3Com] sysname SW-3COM-PISO1
[SW-3COM-PISO1]
```


## 2. CONFIGURACION DE FECHA, HORA Y SERVIDOR NTP

-- Configurar la Zona Horaria (Ejemplo: UTC-6 Mexico/Centroamerica):
```text
<SW-3COM-PISO1> clock timezone CDMX minus 06:00:00

-- Ajuste manual de hora y fecha (Formato: HH:MM:SS AAAA/MM/DD):
<SW-3COM-PISO1> clock datetime 12:00:00 2026/09/25

-- Sincronizacion automatica con servidor NTP:
[SW-3COM-PISO1] ntp-service unicast-server 192.168.1.100
```


## 3. MENSAJE DE ADVERTENCIA LEGAL (BANNER)


## [SW-3COM-PISO1] header shell "

 ACCESO EXCLUSIVO PARA PERSONAL AUTORIZADO DE SISTEMAS.
 PROHIBIDO EL ACCESO NO AUTORIZADO A ESTE DISPOSITIVO.
============================================================"



## 4. SEGURIDAD EN EL PUERTO DE CONSOLA FISICA (AUX / CONSOLE)

Nota: En switches 3Com, el puerto de consola se llama frecuentemente "aux 0" o "console 0":

```text
[SW-3COM-PISO1] user-interface aux 0
[SW-3COM-PISO1-ui-aux0] authentication-mode password
[SW-3COM-PISO1-ui-aux0] set authentication password cipher ClaveConsola3Com2026!
[SW-3COM-PISO1-ui-aux0] idle-timeout 10 0           <- Cierra sesion tras 10 min de inactividad
[SW-3COM-PISO1-ui-aux0] quit
```


## 5. CONFIGURACION COMPLETA DE ACCESO REMOTO SEGURO POR SSH

En Comware, el esquema AAA administra los usuarios locales mediante "scheme".

Paso 1: Habilitar el servicio SSH en el switch:
```text
[SW-3COM-PISO1] ssh server enable

Paso 2: Generar el par de llaves criptograficas RSA locales:
[SW-3COM-PISO1] public-key local create rsa
  -> Te solicitara el tamano de clave. Escribe: 2048 y presiona Enter.

Paso 3: Crear el usuario administrador local:
* Niveles de usuario en 3Com Comware:
```

  - 0: Visit (Solo comandos de red elementales).
  - 1: Monitor (Comandos de visualizacion display).
  - 2: System (Configuracion basica).
  - 3: Manage (Acceso total administrativo equivalente al nivel 15 de Cisco).

```text
[SW-3COM-PISO1] local-user admin
[SW-3COM-PISO1-luser-admin] password cipher AdminClave3Com2026!
[SW-3COM-PISO1-luser-admin] authorization-attribute level 3
[SW-3COM-PISO1-luser-admin] service-type ssh telnet terminal
[SW-3COM-PISO1-luser-admin] quit

Paso 4: Asociar el usuario al servicio SSH con contrasena:
[SW-3COM-PISO1] ssh user admin authentication-type password
[SW-3COM-PISO1] ssh user admin service-type stelnet

Paso 5: Configurar las lineas virtuales de acceso remoto (VTY 0 a 4):
[SW-3COM-PISO1] user-interface vty 0 4
[SW-3COM-PISO1-ui-vty0-4] authentication-mode scheme      <- Usa la base de usuarios locales
[SW-3COM-PISO1-ui-vty0-4] protocol inbound ssh            <- Bloquea Telnet, solo acepta SSH
[SW-3COM-PISO1-ui-vty0-4] idle-timeout 15 0
[SW-3COM-PISO1-ui-vty0-4] quit
```


## 6. VERIFICACION

- Comprobar estado del servidor SSH:
```text
    <SW-3COM-PISO1> display ssh server status

- Ver usuarios conectados en este momento:
    <SW-3COM-PISO1> display users
```
