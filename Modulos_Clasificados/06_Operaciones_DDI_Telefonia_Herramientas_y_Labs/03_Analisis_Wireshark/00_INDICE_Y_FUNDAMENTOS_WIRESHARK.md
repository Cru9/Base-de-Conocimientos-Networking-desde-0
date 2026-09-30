# 00. INDICE GENERAL, FUNDAMENTOS DE CAPTURA Y METODOLOGIA FORENSE

> **ANALISIS FORENSE DE PAQUETES CON WIRESHARK (WIRESHARK_ANALYSIS)**


---



## 1. INTRODUCCION AL ANALISIS PROFUNDO DE PAQUETES (PACKET INSPECTION)

En la resolucion de incidentes de red y ciberseguridad existe un principio absoluto:
"LOS PAQUETES NUNCA MIENTEN". Los registros de eventos (logs) pueden ser alterados,
pero el flujo de tramas binarias que viajo fisicamente a traves del cable o el aire
contiene la verdad irrefutable de lo que sucedio en la comunicacion.

Wireshark es el analizador de protocolos de red mas utilizado del planeta. Permite
inspeccionar tramas a nivel de bit, decodificar mas de 3,000 protocolos y medir
tiempos con precision de microsegundos o nanosegundos.



## 2. METODOS DE OBTENCION DEL TRAFICO (PUNTOS DE CAPTURA)

Un conmutador moderno solo envia a un puerto las tramas destinadas a la direccion MAC
de dicho puerto. Por tanto, para capturar trafico de terceros se requiere una técnica
especifica:


### a) SPAN (Switch Port Analyzer / Port Mirroring):

   - El conmutador copia en tiempo real todo el trafico que entra o sale de uno
     o varios puertos origen (ej. puerto del Servidor Web) y lo replica hacia un
     puerto de monitoreo donde esta conectada la laptop con Wireshark.
   - RSPAN (Remote SPAN): Transporta el trafico duplicado a traves de una VLAN especial
     entre multiples switches de la red local.
   - ERSPAN (Encapsulated Remote SPAN): Encapsula el trafico duplicado en paquetes
     GRE/IP y permite enviar la captura a traves de routers de Capa 3 e Internet hacia
     un recolector centralizado.


### b) Network TAPs (Test Access Points):

   - Dispositivos de hardware fisico intercalados directamente en el cableado
     (fibra optica mediante prismas pasivos o cobre activo).
   - Ventaja: No consumen CPU del switch, no alteran las tramas ni descartan paquetes
     defectuosos (CRC errors), garantizando evidencia forense 100% integra.


### c) Captura en Linea de Comandos (CLI) Directa en Produccion:

   En servidores remotos o firewalls sin entorno grafico, se genera el archivo de
   captura (.pcap / .pcapng) mediante CLI y luego se descarga para abrir en Wireshark:

   * En Linux (mediante `tcpdump` con Buffer Circular):
     `tcpdump -i eth0 -s 0 -w captura.pcap -C 100 -W 5`
     (-s 0 = paquete completo; -C 100 = archivos de 100 MB; -W 5 = maximo 5 archivos rotativos).

   * En Cisco IOS-XE (Embedded Packet Capture - EPC):
     `monitor capture MI_CAP buffer size 50`
     `monitor capture MI_CAP interface GigabitEthernet0/0/1 both`
     `monitor capture MI_CAP start`
     `monitor capture MI_CAP stop`
     `monitor capture MI_CAP export tftp://10.1.1.50/cisco_capture.pcap`

   * En Fortinet FortiOS:
     `diagnose sniffer packet any 'port 443' 6 0 l`



## 3. FILTROS DE CAPTURA vs FILTROS DE VISUALIZACION (DIFERENCIA CRITICA)

REGLA BASICA DE EXAMEN Y OPERACION:


### a) Filtros de Captura (Capture Filters / BPF - Berkeley Packet Filter):

   - Se configuran ANTES de iniciar la grabacion.
   - Son ejecutados directamente por el Kernel del sistema operativo o tarjeta de red.
   - Su objetivo es ahorrar espacio en disco descartando lo que no interesa.
   - Sintaxis BPF (simple y sin puntos):
     `host 192.168.1.100 and port 80`
     `net 10.0.0.0/8 and not broadcast`


### b) Filtros de Visualizacion (Display Filters):

   - Se aplican DESPUES de haber capturado los paquetes.
   - No eliminan informacion; solo ocultan lo irrelevante en la pantalla.
   - Sintaxis Wireshark rica y granular (con puntos y operadores logicos):
     `ip.addr == 192.168.1.100 && tcp.port == 80`
     `http.response.code >= 500`



## 4. INDICE DE ARCHIVOS DE LA CARPETA WIRESHARK_ANALYSIS

[00_INDICE_Y_FUNDAMENTOS_WIRESHARK.md](./00_INDICE_Y_FUNDAMENTOS_WIRESHARK.md)
    - Principios forenses, metodos de captura (SPAN, TAP, tcpdump) y conceptos clave.

[01_FILTROS_DE_VISUALIZACION_INDISPENSABLES.md](./01_FILTROS_DE_VISUALIZACION_INDISPENSABLES.md)
    - Cheat Sheet maestro de Display Filters para administradores y analistas de ciberseguridad
      (ARP, IP, ICMP, DNS, DHCP, HTTP, TLS y TCP flags).

[02_DIAGNOSTICO_Y_RESOLUCION_FALLAS_TCP.md](./02_DIAGNOSTICO_Y_RESOLUCION_FALLAS_TCP.md)
    - El motor de analisis TCP Expert: Retransmisiones, Dup ACKs, Zero Window, Window Full,
      paquetes desordenados y aislamiento de latencia de red vs latencia de aplicacion.

[03_ANALISIS_VOIP_Y_STREAMING.md](./03_ANALISIS_VOIP_Y_STREAMING.md)
    - Diagnostico de telefonia IP: Senalizacion SIP, audio RTP, medicion de Jitter,
      perdida de paquetes, codecs y resolucion de problemas de audio de una sola via.

[04_CASOS_PRACTICOS_FORENSE_DE_RED.md](./04_CASOS_PRACTICOS_FORENSE_DE_RED.md)
    - Investigacion de incidentes reales: Ataques de fuerza bruta / SYN flood,

exfiltracion por tunel DNS, caida de base de datos y descifrado legal SSL/TLS.
