# 03. ANALISIS DE TELEFONIA IP (VOIP), PROTOCOLOS SIP Y FLUJOS RTP

> **ANALISIS FORENSE DE PAQUETES CON WIRESHARK (WIRESHARK_ANALYSIS)**


---



## 1. ARQUITECTURA DE PROTOCOLOS VOIP

La telefonia IP sobre redes de datos separa estrictamente el control de la llamada
de la transmision de la voz:


### a) Senalizacion y Control (SIP - Session Initiation Protocol / RFC 3261):

   - Establece, modifica y finaliza las llamadas telefonicas.
   - Puertos: UDP o TCP 5060 (texto plano) y TCP 5061 (SIP-TLS cifrado).
   - Utiliza una sintaxis similar a HTTP (INVITE, 200 OK, ACK, BYE).


### b) Descripcion de la Sesion Multimedia (SDP - Session Description Protocol):

   - Va embebido dentro del cuerpo de los mensajes SIP.
   - Negocia la direccion IP donde se enviara la voz, el puerto UDP efimero y el
     codec de compresion acordado.


### c) Transporte de la Voz en Tiempo Real (RTP - Real-time Transport Protocol / RFC 3550):

   - Transporta la voz digitalizada en paquetes UDP de baja latencia.
   - Puertos dinamicos efimeros (rango tipico 10000 a 32767 UDP).
   - Acompanado por RTCP (puerto impar contiguo) para reportar estadisticas de calidad.



## 2. FLUJO DE SENALIZACION SIP (DIAGRAMA DE ESCALERA - LADDER DIAGRAM)

En Wireshark, ir a: `Telephony -> VoIP Calls -> Seleccionar la llamada -> Flow Sequence`.

  Telefono Origen (Alice)                   PBX / Centralita / Telefono Destino (Bob)
           |                                                    |
           | ---------------- INVITE (SDP: IP/Port) ----------> |
           | <--------------- 100 Trying ---------------------- |
           | <--------------- 180 Ringing (Timbrando) --------- |
           |                                                    | (Bob contesta)
           | <--------------- 200 OK (SDP: IP/Port) ----------- |
           | ---------------- ACK ----------------------------> |
           |                                                    |
           | <================ BIDIRECCIONAL =================> |
           |                  FLUJO DE AUDIO RTP                |
           |                 (Paquetes cada 20 ms)              |
           |                                                    | (Alice cuelga)
           | ---------------- BYE ----------------------------> |
           | <--------------- 200 OK -------------------------- |
           v                                                    v

Codigos de Estado SIP Comunes:
- 1xx (Informativos): 100 Trying, 180 Ringing, 183 Session Progress.
- 2xx (Exito): 200 OK.
- 4xx (Errores del Cliente):
  * 401 Unauthorized / 407 Proxy Authentication Required (Desafio digest normal).
  * 404 Not Found (Numero no asignado o inexistente).
  * 486 Busy Here (Usuario ocupado).
  * 488 Not Acceptable Here (Incompatibilidad de Codecs).
- 5xx / 6xx: 500 Server Internal Error, 503 Service Unavailable, 603 Decline.



## 3. ANALISIS DE FLUJOS RTP Y METRICAS DE CALIDAD DE VOZ

En Wireshark, ir a: `Telephony -> RTP -> RTP Streams`.
Seleccionar un flujo y hacer clic en `Analyze`.

Metricas Criticas de Calidad:

### a) Jitter (Variacion de Retardo de Paquetes):

   - En una llamada normal, los paquetes de voz se transmiten exactamente cada 20 ms.
   - El Jitter mide la dispersion o irregularidad con la que llegan los paquetes.
   - Umbral Maximo Tolerable: < 30 milisegundos.
   - Si el jitter supera los 30-50 ms, el buffer de jitter del telefono IP se agota
     y el audio suena metalico, robotico o entrecortado.


### b) Perdida de Paquetes (Packet Loss):

   - Porcentaje de paquetes RTP que se descartaron en el trayecto.
   - Umbral Maximo Tolerable: < 1% de perdida.
   - Si la perdida supera el 2%, se pierden silabas completas y la conversacion
     se vuelve ininteligible.


### c) Latencia Unidireccional (One-Way Delay):

   - Tiempo que tarda la voz en viajar desde la boca del emisor hasta el oido del receptor.
   - Segun la norma ITU-T G.114:
     * 0 a 150 ms: Excelente (Conversacion fluida y natural).
     * 150 a 300 ms: Aceptable para enlaces satelitales pero con sensacion de retardo.
     * > 400 ms: Inaceptable (Ambas personas se interrumpen al hablar).


### d) Codecs de Voz:

   - G.711 (PCMU / PCMA - 64 Kbps): Voz sin comprimir. Calidad maxima (MOS 4.1).
   - G.729 (8 Kbps): Voz altamente comprimida para enlaces WAN estrechos (MOS 3.9).
   - Opus: Codec moderno adaptable utilizado por WebRTC, Zoom y Microsoft Teams.



## 4. RESOLUCION DEL PROBLEMA NUMERO 1: "AUDIO DE UNA SOLA VIA" (ONE-WAY AUDIO)

Sintoma: El usuario A escucha perfectamente al usuario B, pero el usuario B no
escucha absolutamente nada del usuario A.

Causa Raiz 1: Problema de NAT en la Carga Util SDP (Direccion IP Privada Filtrada):
- El telefono IP se encuentra detras de un router con NAT (IP Privada 192.168.1.50).
- En el cuerpo del paquete SIP `INVITE`, la linea de conexion SDP contiene:
  `c=IN IP4 192.168.1.50`
- El telefono remoto en Internet intenta enviar sus paquetes RTP a la IP 192.168.1.50,
  la cual es inalcanzable sobre la red publica Internet.
- Solucion: Habilitar STUN (Session Traversal Utilities for NAT) o un SBC (Session
  Border Controller) para sustituir la IP privada por la IP publica externa.

Causa Raiz 2: SIP ALG (Application Layer Gateway) Defectuoso en Routers:
- Muchos routers domesticos o empresariales tienen habilitada la funcion "SIP ALG".
- En teoria fue creada para ayudar reescribiendo IPs privadas a publicas.
- En la practica, corrompe las cabeceras SDP, altera puertos y destruye las asociaciones
  de puertos de los conmutadores VoIP.
- REGLA DE ORO DE INGENIERIA VOIP: ¡DESHABILITAR SIEMPRE SIP ALG EN TODOS LOS ROUTERS
  Y FIREWALLS INTERMEDIOS!

Causa Raiz 3: Reglas de Firewall Bloqueando Puertos UDP Efimeros:
- Un firewall permite la senalizacion en el puerto UDP 5060, pero bloquea el rango

dinamico de puertos UDP de datos (10000 a 20000 UDP) en una de las dos direcciones.
