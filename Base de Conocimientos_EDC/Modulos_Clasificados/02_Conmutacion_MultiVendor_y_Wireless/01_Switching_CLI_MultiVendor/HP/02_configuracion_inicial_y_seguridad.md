# GUIA HP PROCURVE / ARUBA - PARTE 2: CONFIGURACION INICIAL Y ACCESO SEGURO (SSH / CONSOLA)


---



## 1. CAMBIAR EL NOMBRE DEL SWITCH (HOSTNAME)

HP-Switch# configure terminal
HP-Switch(config)# hostname SW-HP-PISO1
```cisco
SW-HP-PISO1(config)#
```


## 2. AJUSTE DE HORA, ZONA HORARIA Y SINCRONIZACION SNTP

Nota: En switches HP ProCurve, la zona horaria se especifica en MINUTOS respecto a UTC:
- UTC-6 (Mexico / Centroamerica) = -360 minutos (-6 horas * 60 min).
- UTC-5 (Colombia / Peru / Este EE.UU.) = -300 minutos.

```cisco
SW-HP-PISO1(config)# time timezone -360
SW-HP-PISO1(config)# time daylight-time-rule none

-- Sincronizacion automatica con Servidor NTP/SNTP:
SW-HP-PISO1(config)# sntp server priority 1 192.168.1.100
SW-HP-PISO1(config)# sntp unicast
SW-HP-PISO1(config)# timesync sntp
```


## 3. MENSAJE DE ADVERTENCIA LEGAL (BANNER MOTD)


## SW-HP-PISO1(config)# banner motd #

 ACCESO EXCLUSIVO PARA PERSONAL AUTORIZADO DE REDES.

## PROHIBIDO EL ACCESO NO AUTORIZADO A ESTE DISPOSITIVO.

#



## 4. ADMINISTRACION DE USUARIOS Y CONTRASENAS (MANAGER Y OPERATOR)

En HP ProCurve existen dos roles de usuario nativos:
- Operator: Solo puede consultar y ejecutar pruebas (lectura).
- Manager: Tiene control total para configurar el equipo (administrador).

Paso 1: Asignar contrasena al usuario Manager (Administrador):
```cisco
SW-HP-PISO1(config)# password manager user-name admin plaintext MiClaveAdmin2026!

Paso 2: (Opcional) Asignar contrasena al usuario Operator (Solo consulta):
SW-HP-PISO1(config)# password operator user-name operario plaintext ClaveConsulta2026!

Paso 3: Tiempo de espera por inactividad en la consola (10 minutos):
SW-HP-PISO1(config)# console inactivity-timer 10
```


## 5. CONFIGURACION COMPLETA DE ACCESO REMOTO SEGURO POR SSH

Telnet envia las credenciales en texto plano sin cifrar. En produccion se debe usar SSH.

Paso 1: Generar las llaves criptograficas RSA:
```cisco
SW-HP-PISO1(config)# crypto key generate ssh rsa
  -> El switch generara las llaves locales en la memoria flash.

Paso 2: Activar el servidor SSH:
SW-HP-PISO1(config)# ip ssh

Paso 3: Desactivar el protocolo inseguro Telnet:
SW-HP-PISO1(config)# no telnet
```


## 6. SEGURIDAD DE LA INTERFAZ WEB (HTTPS / SSL)

Los switches HP traen una interfaz web grafica muy util. Por seguridad, debes apagar
el trafico web plano (HTTP) y habilitar conexion cifrada (HTTPS):

```cisco
SW-HP-PISO1(config)# crypto key generate web-management rsa
SW-HP-PISO1(config)# web-management ssl
SW-HP-PISO1(config)# no web-management plaintext
```


## 7. VERIFICACION

- Comprobar que SSH esta activo y que Telnet esta deshabilitado:
```cisco
    SW-HP-PISO1# show ip ssh
    SW-HP-PISO1# show telnet

- Ver hora sincronizada y estado del servidor SNTP:
    SW-HP-PISO1# show time
    SW-HP-PISO1# show sntp
```
