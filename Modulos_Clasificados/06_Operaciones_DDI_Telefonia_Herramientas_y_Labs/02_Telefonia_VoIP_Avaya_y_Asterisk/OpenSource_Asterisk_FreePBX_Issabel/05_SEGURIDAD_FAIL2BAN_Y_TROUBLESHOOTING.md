# ASTERISK, FREEPBX E ISSABEL

> **TELEFONIA DE CODIGO ABIERTO (OPEN SOURCE VOIP)**

> *05. SEGURIDAD Y HARDENING: FAIL2BAN, ANTI-FRAUDE Y RESOLUCION DE FALLAS*


---



## 1. LA AMENAZA DEL ESCANEO MASIVO Y FRAUDE TELEFONICO (SIPVICIOUS)

En cuanto conectas un servidor Asterisk con una IP publica a Internet, recibira
miles de paquetes SIP automatizados por hora generados por herramientas como
`SIPVicious` (herramientas `svmap` y `svcrack`).

El Objetivo de los Cibercriminales:
1. Escanear el puerto UDP 5060 buscando conmutadores Asterisk en linea.
2. Probar ataques de fuerza bruta contra extensiones comunes (101, 102, 200, 1000)
   utilizando contrasenas faciles (`1234`, `101`, `admin`).
3. Registrarse como una extension interna legitima.
4. Enrutar cientos de llamadas simultaneas a traves de tus troncales hacia numeros
   satelitales o internacionales de cobro revertido de tarificacion especial ($30 a $60
   dolares por minuto) en paises sin tratado de extradicion.
5. Dejar a la empresa una factura telefonica de mas de $50,000 dolares durante el fin de semana.



## 2. LAS 5 REGLAS DE ORO DE HARDENING EN ASTERISK

REGLA 1: Contrasenas Robustas Generadas Aleatoriamente (Secrets):
- NUNCA uses como password el mismo numero de extension ni secuencias obvias.
- Utiliza contrasenas alfanumericas de minimo 16 caracteres generadas al azar
  (ej. `kX9#mP2$vL8@qR4!`).

REGLA 2: Ocultar si la Extension Existe (alwaysauthreject):
- Por defecto, si un atacante prueba la extension 101 y existe, Asterisk responde "Password incorrecto".
  Si la extension 102 no existe, Asterisk responde "Usuario no encontrado".
- Esto le permite al atacante enumerar la lista completa de extensiones de la empresa.
- SOLUCION: En la configuracion SIP, fijar:
  `alwaysauthreject = yes`
- Ahora Asterisk responde con el IDENTICO mensaje `SIP 401 Unauthorized` sin importar
  si la extension existe o no, dejando a ciegas al atacante.

REGLA 3: Deshabilitar Llamadas de Invitados (allowguest):
- Evita que cualquier paquete SIP anonimo en Internet pueda hacer sonar los telefonos
  o ejecutar el IVR:
  `allowguest = no`

REGLA 4: Cambiar el Puerto SIP Predeterminado o Migrar a TLS:
- El 99% de los bots atacan exclusivamente el puerto estandar UDP 5060.
- Cambiar el puerto SIP a uno no estandar (ej. UDP 5082 o 5160) o forzar el registro
  exclusivo mediante SIP-TLS cifrado (puerto TCP 5061) elimina el 99.9% de los ataques.

REGLA 5: Bloqueo de Prefijos Internacionales con PIN Sets:
- En las Rutas Salientes (Outbound Routes), restringe los patrones de marcacion
  internacional (`00`, `011`) exigiendo un codigo PIN de 6 digitos autorizado
  unicamente para los directores que viajan.



## 3. FAIL2BAN: EL GUARDIAN AUTOMATIZADO CONTRA FUERZA BRUTA

Fail2Ban es un servicio de seguridad en Linux indispensable para Asterisk:
- Monitorea continuamente el archivo de registros `/var/log/asterisk/full`.
- Detecta intentos fallidos de autenticacion SIP.
- Si una direccion IP falla 3 o 5 contrasenas en menos de 10 minutos:
  ¡Fail2Ban inyecta automaticamente una regla en el Firewall de Linux (iptables / nftables)
  descartando (DROP) el 100% de los paquetes provenientes de esa IP por 24 horas o permanentemente!


## COMANDOS ESENCIALES DE FAIL2BAN EN CONSOLA LINUX:

- `systemctl status fail2ban`          -> Verifica que el servicio de proteccion este activo.
- `fail2ban-client status asterisk`    -> Muestra la lista de IPs atacantes bloqueadas en este momento.
- `fail2ban-client set asterisk unbanip 192.168.1.55`
                                       -> Desbloquea la IP de un empleado legitimo que se equivoco de clave.



## 4. RESOLUCION DE FALLAS COMUNES EN ASTERISK (TROUBLESHOOTING)



### A) PROBLEMA DE AUDIO EN UNA SOLA VIA (ONE-WAY AUDIO EN NAT):

- Sintoma: La llamada conecta, pero una de las dos personas no escucha nada.
- Causa: Asterisk envia su IP privada local (192.168.1.200) en el paquete SDP hacia
  un cliente que esta en Internet.
- Solucion: En la configuracion del transporte PJSIP (`pjsip.conf` o GUI de FreePBX):
  * `external_media_address = TU_IP_PUBLICA` (ej. 200.10.20.30)
  * `local_net = 192.168.1.0/24`
  * Abrir y reenviar en el router el rango UDP de puertos RTP:
    Puertos UDP `10000 a 20000` hacia la IP interna de Asterisk.


### B) DECODIFICACION DE ERRORES EN EL ARCHIVO DE LOG (/var/log/asterisk/full):

- En Linux ejecuta: `tail -f /var/log/asterisk/full | grep -i error`

Errores Tipicos:
1. `Registration from '<sip:101@...>' failed for '192.168.1.50' - Wrong password`:
   -> La contrasena escrita en el softphone no coincide con el `Secret` de la extension.
2. `No matching endpoint found`:
   -> El softphone escribio mal el nombre de usuario o Asterisk no tiene configurado
      el endpoint PJSIP para esa cuenta.
3. `Everyone is busy/congested at this time`:
   -> La llamada hacia la calle fallo. O la troncal SIP esta caida con el proveedor,
      o el patron de marcacion en la Ruta Saliente no coincide con el numero digitado.
4. `Unable to create channel of type 'PJSIP' (cause 20 - Subscriber absent)`:

## -> La extension de destino esta apagada o desregistrada de la red.
