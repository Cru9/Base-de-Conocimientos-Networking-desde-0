# 02. AVAYA IP OFFICE 500 V2 (IP500v2): ARQUITECTURA DE HARDWARE Y LICENCIAS

> **TELEFONIA EMPRESARIAL Y VOZ SOBRE IP (VOIP)**


---



## 1. EL CHASIS AVAYA IP OFFICE 500 V2 (IP500v2)

La unidad de control Avaya IP500v2 es un conmutador hibrido modular de 19 pulgadas
(2U de rack) disenado para soportar desde 4 hasta 384 extensiones por sistema.
Combina telefonia IP nativa, extensiones digitales, telefonos analogicos y troncales SIP/E1.


## ANATOMIA DEL PANEL FRONTAL Y TRASERO:

- LAN 1 (Local): Puerto RJ-45 de red interna.
  * Direccion IP de fabrica por defecto: 192.168.42.1 / Mascara 255.255.255.0
  * Actua como servidor DHCP interno entregando IPs en el rango 192.168.42.2 a .254.
- LAN 2 / WAN: Puerto RJ-45 secundario / WAN.
  * Direccion IP de fabrica por defecto: 192.168.43.1 / Mascara 255.255.255.0
- Ranura System SD (OBLIGATORIA):
  * Aloja la tarjeta SD del sistema de Avaya.
- Ranura Optional SD:
  * Segunda ranura utilizada para respaldos automaticos de configuracion y mensajes.
- Puerto DTE (RS-232 Serial de 9 pines):
  * Puerto de consola para rescate a bajo nivel y recuperacion de contrasenas de fabrica.
- Entrada de Audio (Audio In - Jack 3.5 mm):
  * Entrada analogica para fuentes externas de Musica en Espera (Music-on-Hold).
- Puertos de Expansion (Expansion 1 al 8):
  * Puertos RJ-45 posteriores que conectan modulos de expansion externos mediante
    cables azules propietarios de expansion.



## 2. LA TARJETA SYSTEM SD: EL CORAZON Y LLAVE DEL SISTEMA

¡ADVERTENCIA CRITICA!: El chasis IP500v2 NO puede arrancar sin su tarjeta System SD oficial.
- Marca de Agua de Hardware (Feature Key ID - FkID):
  * Cada tarjeta SD de Avaya posee un numero de serie de hardware unico de fabrica
    (ej. `10-12345678`).
  * ¡TODAS LAS LICENCIAS adquiridas a Avaya se compilan y amarran criptograficamente
    a este numero FkID exacto!
  * Si la tarjeta SD se dana o se extravia, las licencias del conmutador quedan invalidas.
- Almacenamiento Interno:
  * Almacena el sistema operativo del conmutador (firmware .bin), los audios de la
    operadora automatica embebida y el archivo maestro de configuracion `config.cfg`.
- Nota: NO se pueden utilizar tarjetas SD comerciales convencionales (SanDisk, Kingston, etc.).
  El firmware de Avaya verifica la firma de fabricante de la tarjeta en el arranque.



## 3. LAS 4 RANURAS BASE Y TIPOS DE TARJETAS (BASE CARDS)

El chasis IP500v2 cuenta con 4 bahias frontales donde se insertan tarjetas base:


### a) Tarjetas VCM (Voice Compression Module - VCM 32 v2 / VCM 64 v2):

   - ¡INDISPENSABLES PARA VOIP!
   - Contienen chips DSP (Digital Signal Processors) dedicados por hardware.
   - Funciones del DSP:
     * Transcodificacion de codecs (ej. convertir de G.711 a G.729 en llamadas externas).
     * Soporte de puentes de audio para conferencias telefonicas.
     * Canales de compresion requeridos para Troncales SIP y Extensiones IP.
   - Cada tarjeta VCM incluye de fabrica 4 licencias gratuitas de Avaya IP Endpoints.


### b) Tarjeta Combo (Combo Card ATM / V2) - La Solucion Todo-en-Uno:

   - Diseñada para sucursales medianas. Integra en una sola tarjeta:
     * 4 Puertos de Troncal Analogica FXO (Lineas de la calle).
     * 6 Puertos de Extension Digital (para telefonos Avaya serie 1400 / 9500).
     * 2 Puertos de Extension Analogica FXS (para aparatos de Fax o telefonos simples).
     * 10 Canales VCM DSP integrados por hardware.


### c) Tarjeta Digital Station (DS 8):

   - Provee 8 puertos para extensiones digitales de dos hilos (DCP).


### d) Tarjeta Phone (Phone 2 / Phone 8):

   - Provee 2 u 8 puertos analogicos FXS para terminales POTS o faxes.


### e) Tarjetas Hijas (Daughter Cards - Troncales):

   - Se montan directamente sobre las tarjetas base DS8 o Phone8:
     * Universal PRI Card (1 o 2 puertos E1/PRI digitales de 30 canales).
     * Analog Trunk Daughter Card (4 puertos FXO analogicos adicionales).



## 4. MODULOS DE EXPANSION EXTERNOS

Si se superan las capacidades del chasis principal, se apilan modulos externos
conectados por los puertos de expansion traseros:
- IP500 Digital Station 16 / 30: Agrega 16 o 30 extensiones digitales adicionales.
- IP500 Phone 16 / 30: Agrega 16 o 30 extensiones analogicas FXS adicionales.



## 5. MODELO DE LICENCIAMIENTO DE AVAYA IP OFFICE

Las licencias son cadenas alfanumericas de 32 caracteres que se cargan en el sistema:


### A) Licencias de Edicion del Sistema (System Edition):

   - IP Office Essential Edition: Licencia base obligatoria para habilitar el conmutador,
     correo de voz embebido y operadora automatica básica.
   - IP Office Preferred Edition (Voicemail Pro): Habilita el servidor avanzado de voz
     en Linux/Windows, IVR multi-nivel, grabacion de llamadas y distribucion avanzada.


### B) Licencias de Canales y Terminales:

   - SIP Trunk Channels: Se adquieren en paquetes (ej. 5, 10, 20 o 50 canales concurrentes).
   - Avaya IP Endpoints: Licencia requerida por cada telefono IP de marca Avaya
     (series 9600, 1600, J100 como J129, J139, J179).
   - 3rd Party IP Endpoints: Licencia requerida si deseas registrar telefonos SIP genericos

## (marcas Grandstream, Yealink, Cisco, Polycom o Softphones como Zoiper / Linphone).
