# 07. FALLAS DE ACCESO REMOTO (SSH / TELNET), AUTENTICACION Y RECUPERACION DE CLAVES

> **RESOLUCION DE FALLAS (TROUBLESHOOTING DE SWITCHES)**


---



## 1. SINTOMAS COMUNES DE FALLA EN ACCESO REMOTO

- Al intentar conectar por SSH: "Connection refused", "Connection timed out" o
  "Server unexpectedly closed network connection".
- El cliente SSH muestra: "No supported authentication methods available (server sent: publickey)".
- Aparece la solicitud de usuario y clave, pero rechaza la contrasena correcta
  ("Login invalid").
- El administrador aplico una ACL en las lineas VTY y accidentalmente se bloqueo
  a si mismo el acceso a todos los switches.
- Se desconoce la contrasena de un switch instalado hace anos por un proveedor anterior.



## 2. PRINCIPALES CAUSAS Y DIAGNOSTICO


### a) Falta de llaves criptograficas RSA (Causa #1 de "Connection Refused" en SSH):

   - El servicio SSH requiere obligatoriamente un par de llaves asimetricas RSA.
   - Si no se ejecuto `crypto key generate rsa`, el puerto 22 permanecera cerrado.


### b) Bloqueo por Lista de Control de Acceso (ACL de Gestion VTY):

   - La ACL en las lineas VTY solo permite las IPs `11.39.41.0/24` y `192.168.1.0/24`.
   - Si el administrador intenta entrar desde una VPN (`10.200.0.50`), la ACL
     descarta los paquetes silenciosamente.


### c) Rechazo de cifrado por clientes OpenSSH modernos (Linux/Mac/Windows Terminal):

   - Switches antiguos usan algoritmos obsoletos (ej. `ssh-rsa` o `diffie-hellman-group1-sha1`).
   - Los clientes SSH actuales bloquean estos algoritmos por seguridad.
   - Solucion desde la terminal del cliente:
     `ssh -oKexAlgorithms=+diffie-hellman-group14-sha1 -oHostKeyAlgorithms=+ssh-rsa admin@192.168.1.1`


### d) Servidor RADIUS / TACACS+ caido sin respaldo local:

   - Se configuro autenticacion centralizada, pero el servidor RADIUS se apago o
     cambio de IP, y el administrador olvido poner `local` al final de la regla.
   - El switch espera respuesta del servidor inexistente y rechaza el login local.



## 3. RESOLUCION RAPIDA DE PROBLEMAS DE SSH

Paso 1: Generar o regenerar llaves criptograficas
  (Cisco)       SW(config)# crypto key generate rsa modulus 2048
  (Huawei)      SW(config)# rsa local-key-pair create
  (3Com)        SW(config)# public-key local create rsa
  (HP)          SW(config)# crypto key generate ssh rsa bits 2048
  (Aruba CX)    SW(config)# crypto key generate rsa bits 2048
  (TP-Link)     SW(config)# crypto key generate rsa

Paso 2: Verificar que el servicio SSH este activo
  (Cisco)       SW# show ip ssh
  (Huawei)      SW> display stelnet server status
  (HP)          SW# show ip ssh
  (Aruba CX)    SW# show ssh server status
  (TP-Link)     SW# show ip ssh

Paso 3: Asegurar siempre respaldo local en AAA
  Regla de oro: NUNCA configure AAA sin fallback local:
```cisco
  SW(config)# aaa authentication login default group radius local
```


## 4. PROCEDIMIENTO DE RECUPERACION DE CONTRASENA POR MARCA (PASSWORD RECOVERY)

Cuando se pierde la contrasena de administrador, cada fabricante cuenta con un
metodo de recuperacion fisica mediante cable de consola sin borrar la configuracion:

CISCO (Modo ROMMON):
  1. Conectar cable de consola a 9600 bps.
  2. Reiniciar el switch fisicamente y presionar el boton 'Mode' en el frontal
     durante 10 segundos hasta que el LED parpadee en ambar y entre al prompt `switch:`.
  3. Ejecutar: `flash_init`
  4. Renombrar archivo de configuracion: `rename flash:config.text flash:config.old`
  5. Iniciar sistema: `boot`
  6. El switch iniciara sin pedir contrasena. En enable:
     `rename flash:config.old flash:config.text`
     `copy flash:config.text system:running-config`
  7. Cambiar contrasena: `username admin privilege 15 secret NuevaClave123`
  8. Guardar: `write memory`

HUAWEI (Menu BootLoader):
  1. Conectar consola a 9600 bps y reiniciar el switch.
  2. Cuando aparezca el mensaje de arranque, presionar `Ctrl + B` repetidamente.
  3. Ingresar la contrasena de BootLoader (por defecto suele ser `Admin@huawei.com` o vacia).
  4. Seleccionar la opcion del menu: "Clear password for console user" o
     "Boot with default configuration".
  5. Modificar la contrasena en AAA y guardar con `save`.

HP PROCURVE (Botones fisicos Clear / Reset):
  1. Localizar los dos pequeños orificios frontales rotulados "Reset" y "Clear".
  2. Con un clip, presione ambos botones simultaneamente.
  3. Suelte el boton "Reset" manteniendo presionado el boton "Clear".
  4. Cuando el LED "Test" comience a parpadear, suelte el boton "Clear".
  5. El switch borrara UNICAMENTE las contrasenas locales, preservando intactas
     todas las VLANs, IPs y puertos configurados.

ARUBA (AOS-CX ServiceOS):
  1. Conectar consola a 115200 bps y reiniciar.
  2. Durante el arranque seleccionar la particion 'ServiceOS' (tecla '0').

## 3. En el menu de ServiceOS seleccionar la opcion para restablecer credenciales.
