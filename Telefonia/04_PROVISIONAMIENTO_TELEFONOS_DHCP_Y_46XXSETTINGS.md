# 04. APROVISIONAMIENTO MASIVO DE TELEFONOS IP: DHCP OPCION 242 Y 46xxsettings.txt

> **TELEFONIA EMPRESARIAL Y VOZ SOBRE IP (VOIP)**


---



## 1. EL FLUJO DE ARRANQUE AUTOMATIZADO (ZERO TOUCH PROVISIONING)

En una empresa con 300 telefonos IP Avaya, configurar manualmente la IP, VLAN,
servidor y mascara a traves de la pantalla diminuta de cada telefono es impensable.

Avaya utiliza un flujo automatizado de arranque mediante DHCP y servidores HTTP:

  [Telefono IP Avaya]                                   [Servidor DHCP]       [Avaya IP500v2]
           |                                                   |                     |
           | -- 1. DHCP Discover (VLAN 1 Datos sin etiquetar) -> |                     |
           | < - 2. DHCP Offer con Opcion 242: L2QVLAN=20 ----- |                     |
           |                                                   |                     |
   (El telefono libera la IP, activa 802.1Q VLAN 20 y se reinicia)                    |
           |                                                   |                     |
           | == 3. DHCP Discover (VLAN 20 de Voz etiquetada) => |                     |
           | <= 4. DHCP Offer con Opcion 242 Completa ========= |                     |
           |       (MCIPADD=192.168.42.1, HTTPSRVR=192.168.42.1)                     |
           |                                                                         |
           | == 5. Descarga de Firmware (J100upgrade.txt / 96x1Hupgrade.txt) =======> |
           | == 6. Descarga del archivo de configuracion maestro (46xxsettings.txt) => |
           | == 7. Registro H.323 (UDP 1719) o SIP (UDP 5060) al conmutador =======> |
           v                                                                         v
   [Telefono Operativo: Solicita Extension y Password en pantalla]



## 2. LA OPCION DHCP 242 (EL MOTOR DE DESCUBRIMIENTO AVAYA)

La Opcion DHCP 242 (Tipo String / Cadena de Texto) es el estandar que le indica
a los telefonos Avaya a que red saltar y que servidores consultar.


## A) En el Servidor DHCP de la VLAN de Datos (VLAN 1):

El objetivo es forzar al telefono a abandonar la red de computadoras y saltar
a la red de voz aislada:
- En Servidor Windows DHCP (Opcion 242 de ambito):
  `L2Q=1,L2QVLAN=20`
- En Switch Cisco (DHCP Pool de Datos):
  `option 242 ascii "L2Q=1,L2QVLAN=20"`


## B) En el Servidor DHCP de la VLAN de Voz (VLAN 20):

Entrega todos los parametros de conexion al conmutador Avaya:
- En Servidor Windows DHCP:
  `MCIPADD=192.168.42.1,MCPORT=1719,HTTPSRVR=192.168.42.1,HTTPDIR=/,TLSSRVR=192.168.42.1`
- En Switch Cisco:
  `option 242 ascii "MCIPADD=192.168.42.1,MCPORT=1719,HTTPSRVR=192.168.42.1,HTTPDIR=/,TLSSRVR=192.168.42.1"`

SIGNIFICADO DE LOS PARAMETROS:
- `L2Q=1`        : Habilita el etiquetado 802.1Q en el telefono.
- `L2QVLAN=20`   : ID de la VLAN de Voz donde debe operar el telefono.
- `MCIPADD`      : IP del Call Server (Avaya IP Office 500v2).
- `MCPORT=1719`  : Puerto de registro H.323 Gatekeeper (o 5060 para SIP).
- `HTTPSRVR`     : IP del servidor de archivos HTTP/HTTPS que aloja el firmware y settings.
- `HTTPDIR=/`    : Directorio raiz de descarga de archivos.



## 3. EL ARCHIVO MAESTRO DE CONFIGURACION: 46xxsettings.txt

El archivo `46xxsettings.txt` reside dentro de la tarjeta System SD de Avaya IP Office
y es servido automaticamente por el servidor web HTTP embebido del conmutador.

Permite controlar de forma masiva el comportamiento de todos los telefonos de la empresa:


## LINEAS MAESTRAS RECOMENDADAS EN UN ARCHIVO 46xxsettings.txt:

## 1. SINCRONIZACION HORARIA Y ZONA
SET TIMEZONE "America/Mexico_City"
SET SNTPSRVR "192.168.42.1"
SET DSTOFFSET "1"

## 2. SERVIDOR DE ARCHIVOS Y FIRMWARE
SET TRUSTCERTS "CA_Empresarial.crt"
SET HTTPSRVR "192.168.42.1"
SET HTTPDIR "/"

## 3. IDIOMA Y PARAMETROS DE INTERFAZ
SET SYSTEM_LANGUAGE "spanish.xml"
SET RESTRICT_LOGOFF "1"              ## Impide que usuarios curiosos desregistren el telefono

## 4. INTEGRACION CON DIRECTORIO CORPORATIVO (LDAP / ACTIVE DIRECTORY)
## Permite buscar extensiones corporativas directamente desde la pantalla del telefono
SET WMLHOME "http://192.168.42.1/directory.wml"
SET DIRSRVR "10.100.1.10"
SET DIRBASE "DC=empresa,DC=local"
SET DIRNAME "CN=admin,CN=Users,DC=empresa,DC=local"
SET DRPWD "PasswordLDAP2026!"

## 5. PERSONALIZACION DE PANTALLA
SET SCREENSAVER "logo_corporativo.jpg"
SET SCREENSAVERON "30"              ## Activar protector a los 30 minutos de inactividad



## 4. COMO EDITAR Y SUBIR ARCHIVOS PERSONALIZADOS A LA TARJETA SD

1. Abre Avaya IP Office Manager.
2. Ve a: `File -> Advanced -> Embedded File Management`.
3. Introduce el usuario y password de Administrador.
4. Navega hasta la carpeta `System -> Primary`.
5. Aqui se encuentran los archivos `46xxsettings.txt`, `46xxupgrade.txt` y audios `.wav`.
6. Puedes descargar el archivo, editarlo en Notepad, y volver a subirlo con clic derecho `Upload`.

## 7. La proxima vez que un telefono se reinicie, leera automaticamente la nueva configuracion.
