# 06. AVAYA SMALL COMMUNITY NETWORK (SCN): INTERCONEXION MULTI-SITIO Y RESILIENCIA

> **TELEFONIA EMPRESARIAL Y VOZ SOBRE IP (VOIP)**


---



## 1. ¿QUE ES AVAYA SMALL COMMUNITY NETWORK (SCN)?

Small Community Network (SCN) es la tecnologia propietaria de Avaya que permite
interconectar multiples conmutadores IP Office (IP500v2 o Server Edition) a traves
de una red WAN, MPLS o tuneles VPN IPsec corporativos.

A diferencia de una interconexion telefonica basica (donde solo se pasan llamadas),
SCN convierte a multiples conmutadores geograficamente dispersos (ej. Mexico, Bogota,
Madrid y Miami) en UN SOLO SISTEMA TELEFONICO VIRTUAL UNIFICADO.

CAPACIDADES DE ESCALABILIDAD:
- Permite enlazar hasta 32 nodos IP500v2 en malla.
- Soporta hasta 150 sistemas y mas de 10,000 extensiones en arquitecturas Server Edition.



## 2. BENEFICIOS Y TRANSPARENCIA TOTAL DE FUNCIONES (FEATURE TRANSPARENCY)


### a) Plan de Marcacion Unico y Transparente:

   - Los empleados marcan directamente el numero de extension del companero en otra
     ciudad (ej. marcar `305` para hablar con Bogota) exactamente igual que si estuviera
     en el escritorio de al lado.
   - CERO costo telefonico: Todo el trafico viaja como paquetes de datos sobre la red IP privada.


### b) Presencia y Teclas de Estado en Tiempo Real (BLF - Busy Lamp Field):

   - Una recepcionista en la sede central de Mexico puede tener en los botones de su
     telefono Avaya 9608 las extensiones de los directores en Monterrey y Colombia.
   - El boton se ilumina en ROJO si el director en otra ciudad esta hablando por telefono,
     y en VERDE si esta desocupado.


### c) Buzon de Voz Centralizado (Centralized Voicemail):

   - No es necesario comprar ni licenciar un servidor de buzones en cada sucursal.
   - Se instala un unico servidor Voicemail Pro en la sede central; los conmutadores
     remotos envian los mensajes de voz a traves de la SCN.
   - La luz roja de mensaje en espera (MWI) del telefono de cualquier sucursal se enciende
     instantaneamente al recibir un correo de voz.


### d) Grupos de Busqueda Distribuidos (Distributed Hunt Groups):

   - Se crea un grupo unico de Soporte Tecnico (ej. Extension `200`).
   - El grupo incluye agentes fisicos sentados en Mexico, Colombia y Espana.
   - Una llamada entrante timbra de forma rotativa o colectiva entre agentes de
     diferentes paises de forma completamente imperceptible para el cliente.


### e) Hot Desking Distribuido (Movilidad Total de Empleados):

   - Un ejecutivo de la sucursal A viaja a la sucursal B.
   - Se sienta en cualquier telefono IP disponible, teclea su numero de extension
     y su Login Code.
   - El telefono remoto descarga su perfil: su extension, sus contactos personales,
     sus botones programados y su buzon de voz lo acompanan automaticamente.


### f) Desborde de Troncales y Salida de Respaldo (Toll Breakout / Fallback):

   - Si la sucursal B pierde su conexion local con la compania telefonica (corte de fibra):
   - Sus llamadas locales y de emergencia se enrutan automaticamente a traves de la SCN
     hacia el conmutador de la sucursal A y salen a la calle usando las troncales del corporativo.



## 3. REQUISITOS PREVIOS Y PLANIFICACION DE DISENO


### A) Plan de Direccionamiento No Superpuesto (REGLA OBLIGATORIA):

   En una red SCN, ¡NINGUNA EXTENSION NI GRUPO PUEDE REPETIRSE!
   Se debe disenar una numeracion jerarquica por sede:
   - Sede 1 (Mexico)     : Extensiones 200 a 299 | Grupos 290 a 299
   - Sede 2 (Monterrey)  : Extensiones 300 a 399 | Grupos 390 a 399
   - Sede 3 (Bogota)     : Extensiones 400 a 499 | Grupos 490 a 499


### B) Recursos de Hardware y Licenciamiento:

   - Canales DSP VCM: Cada nodo IP500v2 DEBE contar con una tarjeta VCM 32 o VCM 64
     para procesar la compresion y descompresion de codecs entre el chasis y la WAN.
   - Licencias: Licencia de Voice Networking (segun la version de IP Office) para
     habilitar los canales de troncal H.323 entre conmutadores.


### C) Calidad de Servicio (QoS) y Ancho de Banda WAN:

   - Codec Recomendado para la WAN: G.729 (8 Kbps / consume ~32 Kbps por llamada activa con cabeceras).
   - Marcar el trafico de audio con DSCP EF (46) en los routers de borde.
   - Puertos de Red que DEBEN estar abiertos en los Firewalls/VPNs intermedios:
     * Senalizacion H.323 Gatekeeper : UDP 1719
     * Senalizacion H.323 Call Setup  : TCP 1720
     * Audio RTP / RTCP de Avaya     : UDP 4675 a 5075 (o rango configurado)
     * Descubrimiento y Estado SCN   : UDP 50794 a 50799



## 4. CONFIGURACION PASO A PASO EN AVAYA IP OFFICE MANAGER

Escenario Practico:
- Conmutador Sede Central (MEX-IPO): IP LAN1 10.10.0.50 (Extensiones 2xx)
- Conmutador Sucursal (MTY-IPO): IP LAN1 10.20.0.50 (Extensiones 3xx)

PASO 1: Configuracion del Sistema Local (MEX-IPO):
1. Abre Manager y descarga la configuracion de `MEX-IPO`.
2. Ve a: `System -> Telephony -> Pestana VoIP`.
   - Verifica que el campo `Direct Media Path` este habilitado (permite que los
     telefonos envien audio directamente entre si sin triangular por la CPU del conmutador).

PASO 2: Creacion de la Linea H.323 SCN en MEX-IPO:
1. En el arbol de configuracion, haz clic derecho sobre `Line` -> `New` -> `IP Line`.
2. Pestana "IP Line":
   - Line Number: `10`
   - Gateway IP Address: `10.20.0.50` (Direccion IP del conmutador remoto MTY-IPO).
   - Outgoing Group ID: `10`
   - Incoming Group ID: `10`
   - Number of Channels: `8` (Numero de llamadas simultaneas autorizadas entre sedes).
   - CASILLA CLAVE: Marca obligatoriamente `[X] Small Community Network`.
3. Pestana "VoIP":
   - Compression Mode: Seleccionar `G.729(8K CS-ACELP)`.
   - Supplementary Services: `IP Office SCN`.
   - Local TDM To Local IP: Marcado.

PASO 3: Configuracion Espejo en el Conmutador Remoto (MTY-IPO):
1. Abre Manager y descarga la configuracion de `MTY-IPO`.
2. Haz clic derecho sobre `Line` -> `New` -> `IP Line`.
3. Pestana "IP Line":
   - Line Number: `10`
   - Gateway IP Address: `10.10.0.50` (IP de regreso hacia MEX-IPO).
   - Outgoing Group ID: `10`
   - Incoming Group ID: `10`
   - Number of Channels: `8`
   - CASILLA CLAVE: Marca `[X] Small Community Network`.
4. Pestana "VoIP":
   - Compression Mode: `G.729(8K CS-ACELP)`.
   - Supplementary Services: `IP Office SCN`.

PASO 4: Guardar y Sincronizar:
- Guarda la configuracion en ambos sistemas con `File -> Save Configuration` en modo `Merge`.
- En menos de 30 segundos, ambos conmutadores negocian por UDP 1719/1720, intercambian
  sus tablas de extensiones y ¡la red SCN queda completamente activa!



## 5. CONFIGURACION DE BUZON CENTRALIZADO (CENTRALIZED VOICEMAIL)

Para que los usuarios de Monterrey utilicen el servidor Voicemail Pro de Mexico:
1. En el conmutador de Monterrey (MTY-IPO):
   - Ve a: `System -> Pestana Voicemail`.
   - Voicemail Type: `Voicemail Pro / Lite`.
   - Voicemail IP Address: `10.10.0.50` (La IP del conmutador central que aloja el servidor de voz).
2. Guardar con `Merge`.
3. Ahora, cuando un usuario en Monterrey marque `*17`, el conmutador abrira un canal
   SCN en segundo plano y reproducira sus mensajes de voz desde el servidor central.



## 6. DIAGNOSTICO Y RESOLUCION DE FALLAS EN ENLACES SCN


### A) Validacion en System Status Application (SSA):

- Abre SSA y conectate a cualquiera de los dos conmutadores.
- Despliega la seccion: `Small Community Network`.
- Deberas ver la lista de todos los sistemas remotos:
  * Estado: `Connected` (Conectado).
  * Tiempo de Enlace Activo (Uptime).
  * Latencia de Red de Ida y Vuelta (Round Trip Delay en ms).
  * Extensiones remotas descubiertas.


## B) Errores Frecuentes y Soluciones de Campo:

1. Sintoma: "Extension remota no contesta o da tono de ocupado inmediato".
   - Diagnostico: Conflicto de extensiones duplicadas (ej. la extension 205 existe
     en Mexico y tambien en Monterrey).
   - Solucion: En SSA, revisa el registro de alarmas; Avaya marca en amarillo
     "Duplicate Extension Number" y deshabilita la extension remota conflictiva.

2. Sintoma: "La llamada timbra, descuelgan, pero no se escucha nada (Audio Silencioso)".
   - Diagnostico: El firewall intermedio permite la senalizacion H.323 (puerto TCP 1720)
     pero esta bloqueando el rango de puertos UDP de audio RTP (4675 a 5075).
   - Solucion: Abrir el rango de puertos UDP en las politicas del firewall/VPN.

3. Sintoma: "Alarma 'No Channels Available' al intentar marcar a otra sede".
   - Diagnostico: Se saturaron los canales autorizados de la linea IP (ej. pusiste
     4 canales y hay 4 empleados hablando simultaneamente), o se agotaron los
     chips DSP de la tarjeta VCM fisica.
   - Solucion: Incrementar el numero de canales en la configuracion de la linea o

instalar una tarjeta VCM 64 con mayor capacidad de hardware.
