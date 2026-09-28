# ASTERISK, FREEPBX E ISSABEL

> **TELEFONIA DE CODIGO ABIERTO (OPEN SOURCE VOIP)**

> *03. GUIA DE INSTALACION Y LABORATORIO VIRTUAL EN WINDOWS*


---



## 1. PREPARACION DEL LABORATORIO VIRTUAL EN TU COMPUTADORA

Para practicar y dominar la telefonia IP sin gastar en hardware fisico, puedes
desplegar un conmutador completo en tu computadora con Windows utilizando:
- VMware Workstation Pro (Gratuito para uso personal) o
- Oracle VM VirtualBox (Gratuito y de codigo abierto).

DESCARGA DE LA IMAGEN ISO OFICIAL:
- Para Issabel (Recomendado por su facilidad e instalador todo-en-uno):
  Descargar la ISO oficial desde el sitio oficial `issabel.org` (o SourceForge).
- Para FreePBX Distro:
  Descargar la ISO oficial desde `freepbx.org`.



## 2. CREACION DE LA MAQUINA VIRTUAL (SPECS RECOMENDADAS)

Al crear la Maquina Virtual en VMware o VirtualBox, asigna los siguientes recursos:
- Tipo de Sistema Operativo : Linux -> Red Hat (64-bit) o CentOS (64-bit).
- Procesador (vCPU)         : 2 Cores.
- Memoria RAM               : 2 GB minimo (4 GB recomendado para Call Center).
- Disco Duro Virtual        : 20 GB a 30 GB (Thin Provision / Asignacion dinamica).
- Unidad Optica (CD/DVD)    : Montar el archivo `.iso` descargado.


## ¡EL PARAMETRO MAS IMPORTANTE DE RED (NETWORK ADAPTER)!:

- Configura la tarjeta de red de la Maquina Virtual en modo:
  `BRIDGED` (Adaptador Puente) conectado a tu tarjeta fisica de Ethernet o Wi-Fi.
- ¿Por que NO usar NAT?:
  * En modo NAT, la maquina virtual queda oculta detras de tu computadora.
  * En modo BRIDGED, la maquina virtual recibe una direccion IP real de tu modem
    de casa u oficina (ej. `192.168.1.150`).
  * ¡Esto permite que tu telefono celular con Wi-Fi, tu laptop y cualquier telefono
    IP fisico de escritorio puedan registrarse y hablar directamente con tu conmutador!



## 3. PROCEDIMIENTO DE INSTALACION PASO A PASO (ISSABEL / FREEPBX)

Paso 1: Iniciar la Maquina Virtual:
- Enciende la VM y presiona Enter en la primera opcion: `Install`.

Paso 2: Configuracion Regional:
- Idioma del instalador : Espanol (Spanish).
- Distribucion de teclado: Espanol / Latinoamericano.
- Fecha y Hora           : Selecciona tu zona horaria (ej. `America/Mexico_City`).

Paso 3: Destino de la Instalacion (Particionamiento de Disco):
- Haz clic en "Destino de la instalacion".
- Selecciona el disco virtual de 20 GB y elige "Configuracion automatica".

Paso 4: Red y Nombre de Host (Network & Hostname):
- Activa el interruptor de la tarjeta de red (debe pasar a estado "Conectado").
- Haz clic en "Configurar" -> pestana "Ajustes de IPv4":
  * Metodo: Manual
  * Direccion IP : 192.168.1.200 (o una IP libre en el segmento de tu red)
  * Mascara      : 255.255.255.0 (o prefijo 24)
  * Puerta enlace: 192.168.1.254 (la IP de tu modem o router)
  * Servidores DNS: 8.8.8.8, 1.1.1.1
- Guarda los cambios.

Paso 5: Definicion de Credenciales de Seguridad:
- Durante la instalacion, el asistente te solicitara crear:
  1. Contrasena del usuario `root` de Linux: (ej. `ClaveRootLinux2026!`).
  2. Contrasena de la Base de Datos MariaDB/MySQL: (ej. `ClaveBaseDatos2026!`).
  3. Contrasena del Administrador Web de Issabel (`admin`): (ej. `ClaveAdminWeb2026!`).

Paso 6: Finalizacion y Reinicio:
- Al terminar la instalacion de paquetes, la maquina se reiniciara automaticamente.
- Desmonta la imagen ISO para que arranque desde el disco duro virtual.



## 4. PRIMER ACCESO A LA INTERFAZ WEB

1. Abre tu navegador web favorito en tu computadora (Google Chrome, Microsoft Edge).
2. Escribe en la barra de direcciones la IP que le asignaste al conmutador:
   `https://192.168.1.200`
3. Advertencia de Certificado SSL:
   - El navegador mostrara una advertencia indicando que el certificado es autofirmado.
   - Haz clic en `Configuracion Avanzada` -> `Continuar a 192.168.1.200 (no seguro)`.
4. Pantalla de Inicio de Sesion:
   - Usuario     : `admin`
   - Contrasena  : La clave que definiste en el Paso 5.
5. ¡Bienvenido al Dashboard de Control de tu conmutador IP empresarial!
   Podras ver el uso de CPU, memoria RAM, estado del servicio de Asterisk (en verde)

y llamadas activas.
