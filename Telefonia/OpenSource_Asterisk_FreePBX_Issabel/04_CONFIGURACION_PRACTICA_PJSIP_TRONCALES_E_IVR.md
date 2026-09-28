# ASTERISK, FREEPBX E ISSABEL

> **TELEFONIA DE CODIGO ABIERTO (OPEN SOURCE VOIP)**

> *04. TALLER PRACTICO: EXTENSIONES PJSIP, SOFTPHONES, TRONCALES E IVR*


---


Escenario del Laboratorio:
- IP de la Central Asterisk / Issabel: `192.168.1.200`
- Extension 101: `Juan Perez` (Registrada en la laptop con el softphone MicroSIP)
- Extension 102: `Maria Gomez` (Registrada en el celular con el softphone Zoiper)
- IVR de Bienvenida interactivo para atender llamadas entrantes



## PASO 1: CREACION DE EXTENSIONES PJSIP EN LA INTERFAZ WEB

1. En el menu de la interfaz web de FreePBX / Issabel, ve a:
   `PBX -> PBX Configuration -> Extensions`.
2. En el menu desplegable de la derecha, selecciona:
   `Generic PJSIP Device` y haz clic en `Submit`.
3. Completa los campos clave de la Extension 101:
   - User Extension  : `101`
   - Display Name    : `Juan Perez`
   - Outbound CID    : `"Juan Perez" <101>`
   - Secret          : `ClaveFuerte101!` (La contrasena que usara el telefono)
4. Habilitar Buzon de Voz (Voicemail):
   - Desplazate a la seccion "Voicemail":
   - Status          : `Enabled`
   - Voicemail Password: `1234`
   - Email Address   : `juan.perez@empresa.com`
5. Haz clic en `Submit` al final de la pagina.
6. Repite el proceso para crear la Extension 102:
   - User Extension  : `102`
   - Display Name    : `Maria Gomez`
   - Secret          : `ClaveFuerte102!`
7. ¡PASO OBLIGATORIO!: Haz clic en el boton rojo superior:
   `Apply Config` (Aplicar Cambios).



## PASO 2: INSTALACION Y REGISTRO DE SOFTPHONES GRATUITOS



## A) EN TU LAPTOP CON WINDOWS: INSTALACION DE MICROSIP:

1. Descarga el programa gratuito y de codigo abierto MicroSIP (`microsip.org`).
2. Abre MicroSIP, haz clic en la flecha de la esquina superior derecha y selecciona
   `Add Account` (Agregar Cuenta).
3. Rellena los datos de la Extension 101:
   - Account Name : `Oficina Juan 101`
   - SIP Server   : `192.168.1.200`
   - SIP Proxy    : (Dejar vacio)
   - User         : `101`
   - Domain       : `192.168.1.200`
   - Login        : `101`
   - Password     : `ClaveFuerte101!`
4. Haz clic en `Save`.
5. En la esquina inferior izquierda, el estado debe cambiar a:
   `Online` (En color verde brillante).


## B) EN TU CELULAR (ANDROID / IPHONE): INSTALACION DE ZOIPER:

1. Conecta tu celular a la misma red Wi-Fi de tu casa/oficina.
2. Instala la aplicacion gratuita "Zoiper Lite" desde Google Play o App Store.
3. Abre Zoiper y selecciona `Manual Configuration` -> `SIP`:
   - Account Name : `Maria 102`
   - Host / Domain: `192.168.1.200`
   - Username     : `102`
   - Password     : `ClaveFuerte102!`
4. Guarda los cambios. El indicador de Zoiper cambiara a color verde.

¡PRIMERA PRUEBA DE LLAMADA!:
- En MicroSIP (tu laptop), marca `102` y presiona el boton verde de llamar.
- ¡Tu celular timbrara al instante con el nombre "Juan Perez <101>"!
- Descuelga y habla: el audio bidireccional se escucha nitido y sin retardo.



## PASO 3: CONFIGURACION DE UNA TRONCAL SIP (SIP TRUNK)

Para conectar tu conmutador al mundo exterior con un proveedor ITSP:
1. Ve a: `Connectivity -> Trunks -> Add Trunk -> Add SIP (chan_pjsip) Trunk`.
2. Pestana "General":
   - Trunk Name: `TRONCAL_PROVEEDOR`
   - Outbound CallerID: `5512345600`
3. Pestana "pjsip Settings":
   - Username        : `UsuarioAsignadoPorCarrier`
   - Secret          : `PasswordAsignadoPorCarrier`
   - Authentication  : `Outbound`
   - SIP Server      : `sip.proveedor.com` (o la IP publica del carrier)
   - SIP Server Port : `5060`
4. Guarda con `Submit` y `Apply Config`.



## PASO 4: CREACION DEL MENU DE OPERADORA AUTOMATICA (IVR)


Subpaso 4.1: Cargar la Grabacion de Voz:
1. Graba tu voz en formato WAV con las siguientes especificaciones tecnicas
   exigidas por Asterisk:
   - Formato: WAV PCM sin comprimir.
   - Frecuencia de Muestreo: 8,000 Hz (8 kHz).
   - Canales: Mono (1 canal).
   - Resolucion: 16 bits.
   (Audio de ejemplo: "Gracias por llamar a Empresa ABC. Para Ventas marque 1. Para Soporte marque 2").
2. Ve a: `PBX -> System Recordings -> Add Recording`.
3. Sube el archivo y nombralo: `audio_bienvenida`.

Subpaso 4.2: Crear el Objeto IVR:
1. Ve a: `Applications -> IVR -> Add IVR`.
2. Parametros:
   - IVR Name     : `IVR_GENERAL`
   - Announcement : `audio_bienvenida`
   - Direct Dial  : `Enabled` (Permite marcar una extension directamente)
3. Seccion "IVR Entries" (Opciones numericas):
   - Ext: `1` -> Destination: `Extensions -> 101 (Juan Perez - Ventas)`
   - Ext: `2` -> Destination: `Extensions -> 102 (Maria Gomez - Soporte)`
   - Ext: `t` (Timeout) -> Destination: `Extensions -> 101` (Si no marca nada)
   - Ext: `i` (Invalido) -> Destination: `IVR -> IVR_GENERAL` (Repite el menu si se equivoca)
4. Guarda con `Submit` y `Apply Config`.



## PASO 5: RUTA ENTRANTE (INBOUND ROUTE)

Para conectar las llamadas externas entrantes directamente con el IVR:
1. Ve a: `Connectivity -> Inbound Routes -> Add Inbound Route`.
2. Description: `ENTRADA_LINEA_PRINCIPAL`.
3. DID Number : (Dejar en blanco para cualquier llamada o escribir `5512345600`).
4. Set Destination (Al final de la pagina):
   - Seleccionar: `IVR` -> `IVR_GENERAL`.
5. Guarda con `Submit` y `Apply Config`.

¡Ahora, cualquier llamada que entre por la troncal externa sera contestada

inmediatamente por la operadora automatica interactiva!
