# GUIA HUAWEI VRP - PARTE 2: CONFIGURACION INICIAL Y ACCESO SEGURO (SSH / CONSOLA)


---



## 1. CAMBIAR EL NOMBRE DEL SWITCH (SYSNAME)

Identificar el switch en la red es el primer paso obligatorio.

```text
<HUAWEI> system-view
[HUAWEI] sysname SW-ACCESO-PISO1
[SW-ACCESO-PISO1]
```


## 2. CONFIGURACION DE FECHA, HORA Y ZONA HORARIA

Fundamental para que los registros (logs) tengan la hora correcta:

-- Configurar Zona Horaria (Ejemplo: UTC-6 Mexico/Centroamerica):
```text
<SW-ACCESO-PISO1> clock timezone CDMX minus 06:00:00

-- Ajustar Hora y Fecha manualmente (Formato: HH:MM:SS AAAA-MM-DD):
<SW-ACCESO-PISO1> clock datetime 10:30:00 2026-09-25

-- (Opcional pero recomendado) Configurar servidor NTP sincronizado:
[SW-ACCESO-PISO1] ntp-service unicast-server 192.168.1.100
```


## 3. MENSAJE DE BIENVENIDA / ADVERTENCIA LEGAL (BANNER)


## [SW-ACCESO-PISO1] header shell information "

 ACCESO EXCLUSIVO PARA PERSONAL AUTORIZADO DE REDES.
 TODO ACCESO NO AUTORIZADO SERA REGISTRADO Y SANCIONADO.
============================================================"



## 4. SEGURIDAD EN EL PUERTO DE CONSOLA (CABLE FISICO)

Para evitar que cualquiera conecte un cable de consola y entre directo sin password:

```text
[SW-ACCESO-PISO1] user-interface console 0
[SW-ACCESO-PISO1-ui-console0] authentication-mode password
[SW-ACCESO-PISO1-ui-console0] set authentication password cipher MiClaveConsola2026!
[SW-ACCESO-PISO1-ui-console0] idle-timeout 10 0     <- Cierra sesion tras 10 min de inactividad
[SW-ACCESO-PISO1-ui-console0] quit
```


## 5. CONFIGURACION DE ACCESO REMOTO SEGURO POR SSH (STELNET)

Telnet envia texto plano. En produccion SIEMPRE se debe usar SSH (STelnet en Huawei).

Paso A: Activar el servicio SSH en el switch:
```text
[SW-ACCESO-PISO1] stelnet server enable

Paso B: Generar las llaves criptograficas RSA locales (minimo 2048 bits):
[SW-ACCESO-PISO1] rsa local-key-pair create
  -> Te preguntara el tamano de la clave (512-4096). Escribe: 2048 y pulsa Enter.

Paso C: Crear el usuario administrador con protocolo AAA:
[SW-ACCESO-PISO1] aaa
[SW-ACCESO-PISO1-aaa] local-user admin password cipher AdminPassSegura2026!
[SW-ACCESO-PISO1-aaa] local-user admin privilege level 15    <- Nivel 15 = Permiso total
[SW-ACCESO-PISO1-aaa] local-user admin service-type ssh      <- Solo permitirle entrar por SSH
[SW-ACCESO-PISO1-aaa] quit

Paso D: Habilitar servicio SSH para el usuario especifico:
[SW-ACCESO-PISO1] ssh user admin authentication-type password
[SW-ACCESO-PISO1] ssh user admin service-type stelnet

Paso E: Configurar las lineas virtuales VTY (Sesiones remotas 0 a 4):
[SW-ACCESO-PISO1] user-interface vty 0 4
[SW-ACCESO-PISO1-ui-vty0-4] authentication-mode aaa
[SW-ACCESO-PISO1-ui-vty0-4] protocol inbound ssh             <- Bloquea Telnet, solo acepta SSH
[SW-ACCESO-PISO1-ui-vty0-4] idle-timeout 15 0                <- Desconexion por inactividad
[SW-ACCESO-PISO1-ui-vty0-4] quit
```


## 6. VERIFICACION

- Comprobar que el servidor SSH esta activo:
```text
    <SW-ACCESO-PISO1> display ssh server status

- Ver sesiones conectadas activas:
    <SW-ACCESO-PISO1> display users
```
