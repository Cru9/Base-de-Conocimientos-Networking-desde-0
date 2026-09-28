# 01. ARQUITECTURA CENTRALIZADA, CONTROLADORAS WLC Y PROTOCOLO CAPWAP

> **REDES INALAMBRICAS EMPRESARIALES (WIRELESS ENTERPRISE NETWORKING)**


---



## 1. APs AUTONOMOS (FAT) vs APs LIGEROS (LIGHTWEIGHT / FIT)


### a) Puntos de Acceso Autonomos (Standalone / Fat APs):

   - Cada AP almacena su propio archivo de configuracion, define localmente los SSIDs,
     gestiona las VLANs y almacena las contraseñas.
   - Limitacion Empresarial: En una empresa o campus con 300 puntos de acceso, cambiar
     la clave de Wi-Fi o crear una VLAN implicaba conectarse a 300 dispositivos
     individualmente. El roaming era caotico e interrumpia las llamadas.


### b) Puntos de Acceso Ligeros (Lightweight APs - LAP):

   - Los APs no tienen configuracion local permanente.
   - Al encenderse, buscan y se conectan a una Controladora Centralizada de LAN
     Inalambrica (WLC - Wireless LAN Controller).
   - El WLC gestiona centralizadamente la seguridad, las politicas de usuario, la
     potencia de emision de radio y la conmutacion de trafico.



## 2. EL MODELO "SPLIT-MAC" (DIVISION DE LA CAPA MAC)

Para que la arquitectura centralizada funcione sin colapsar por latencia, las
responsabilidades de la capa 802.11 se dividen estrictamente en dos partes:


### a) Tareas en Tiempo Real (Procesadas en el Hardware del AP):

   - Transmision y recepcion de senales fisicas de radiofrecuencia (PHY).
   - Generacion y envio periodico de tramas Beacon ("anuncios del SSID").
   - Respuestas inmediatas a tramas de sondeo (Probe Requests / Probe Responses).
   - Envio de tramas de confirmacion ACK por hardware (tolerancia de microsegundos).
   - Cifrado y descifrado de tramas de datos por hardware (AES-CCMP / GCMP).


### b) Tareas que NO son en Tiempo Real (Procesadas en la CPU del WLC):

   - Autenticacion corporativa de usuarios (802.1X / RADIUS / Captive Portal).
   - Gestion de claves de sesion y distribucion de llaves criptograficas maestras.
   - RRM (Radio Resource Management): Algoritmo de optimizacion dinamica de canales
     y regulacion automatica de potencia de radio.
   - Mapeo centralizado de SSIDs hacia VLANs corporativas.
   - Coordinacion de Roaming transparente y sin corte entre pisos y edificios.



## 3. EL PROTOCOLO CAPWAP (RFC 5415 / RFC 5416)

CAPWAP (Control and Provisioning of Wireless Access Points) es el protocolo de
comunicacion estandar entre el AP ligero y la WLC.

Opera a traves de dos tuneles UDP independientes:
1. CAPWAP Control (Puerto UDP 5246):
   - Trafico de gestion y control.
   - SIEMPRE CIFRADO mediante DTLS (Datagram Transport Layer Security).
   - Transporta ordenes de configuracion, actualizaciones de firmware y alarmas.

2. CAPWAP Data (Puerto UDP 5247):
   - Transporta el trafico de datos de los usuarios conectados a la red Wi-Fi.
   - Las tramas Ethernet de los usuarios se encapsulan dentro de paquetes UDP 5247
     y viajan a traves de la red cableada hasta el WLC.


## PROCESO DE DESCUBRIMIENTO Y REGISTRO (JOIN PROCESS) DE UN AP:

Paso 1: El AP se conecta al switch, recibe alimentacion PoE y solicita una IP por DHCP.
Paso 2: Descubrimiento del WLC:
        El AP busca la direccion IP del WLC mediante uno de estos mecanismos:

### a) Opcion DHCP 43 (El servidor DHCP envia la IP del WLC en la concesion).


### b) Resolucion DNS: El AP busca el nombre `cisco-capwap-controller.dominio.local`.


### c) Broadcast local en la subred de administracion.

Paso 3: CAPWAP Discovery Request & Response: El AP y el WLC se reconocen.
Paso 4: Tunel DTLS: Se establece una sesion criptografica mutua verificando los
        certificados digitales instalados de fabrica en el hardware (MIC).
Paso 5: CAPWAP Join Request & Response: El AP se asocia oficialmente al WLC.
Paso 6: Verificacion de Firmware: Si la version del AP no coincide exactamente con
        la del WLC, el AP descarga automaticamente la imagen correcta y se reinicia.
Paso 7: Descarga de Configuracion: El WLC le empuja los SSIDs, canales y potencias.



## 4. MODOS DE OPERACION DE PUNTOS DE ACCESO (LOCAL vs FLEXCONNECT)


### a) Local Mode (Modo Centralizado - Campus Principal):

   - Modo estandar para sedes corporativas con switches de alta velocidad.
   - TODO el trafico de datos de los usuarios se encapsula en el tunel CAPWAP Data
     y viaja hasta la WLC.
   - La WLC desencapsula el trafico y lo inyecta en la VLAN correspondiente del switch Core.


### b) FlexConnect (Cisco) / Bridge Mode (Aruba) - SUCURSALES REMOTAS:

   - Disenado para oficinas remotas, sucursales bancarias o tiendas conectadas al
     corporativo mediante enlaces WAN lentos o conexiones VPN de Internet.
   - El tunel CAPWAP Control (UDP 5246) viaja por la WAN hacia la WLC corporativa.
   - El trafico de datos de los empleados locales NO viaja por la WAN; es conmutado
     LOCALMENTE en el switch de la sucursal (Local Switching).
   - RESILIENCIA TOTAL (Modo Standalone): Si el enlace WAN o la VPN hacia la WLC se
     cae por completo, los APs de la sucursal continuan operando localmente, permitiendo
     a los empleados seguir trabajando e imprimiendo sin interrupciones.


### c) Monitor Mode / WIPS:

   - El AP apaga su capacidad de atender clientes y se dedica el 100% de su tiempo
     a escanear el espectro en busca de puntos de acceso no autorizados (Rogue APs),
     ataques de denegacion de servicio y trampas Evil Twin.


### d) Sniffer Mode:

   - El AP se sintoniza en un canal de radio especifico y reenvia todo el trafico

crudo en tiempo real hacia una maquina ejecutando Wireshark.
