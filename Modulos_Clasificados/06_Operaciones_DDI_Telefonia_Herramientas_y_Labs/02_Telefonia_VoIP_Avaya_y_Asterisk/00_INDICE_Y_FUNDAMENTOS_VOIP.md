# 00. INDICE GENERAL, FUNDAMENTOS DE VOIP Y PROTOCOLOS DE COMUNICACION

> **TELEFONIA EMPRESARIAL Y VOZ SOBRE IP (VOIP)**


---



## 1. DE LA RED TELEFONICA CONMUTADA (PSTN/TDM) A LA VOZ SOBRE IP (VOIP)

Durante decadas, la telefonia clasica opero bajo conmutacion de circuitos dedicados:
- La senal analogica de la voz humana (rango de 300 Hz a 3400 Hz) se digitalizaba
  segun el teorema de muestreo de Nyquist a 8,000 muestras por segundo con 8 bits
  por muestra, generando el canal digital estandar DS0 de 64 Kbps (G.711).
- En la tecnologia TDM (Time-Division Multiplexing), los canales se agrupaban en
  tramas E1 (30 canales en Europa/Latinoamerica = 2.048 Mbps) o T1 (24 canales en EE.UU. = 1.544 Mbps).
- Desventaja historica: Desperdicio masivo de recursos (el canal de 64 Kbps permanecia
  ocupado y reservado incluso cuando ninguna de las dos personas estaba hablando).

La Revolucion de Voz sobre IP (VoIP):
- La voz digitalizada se comprime y se empaqueta en tramas IP/UDP ordinarias.
- Comparte la misma red fisica Ethernet que los datos de las computadoras.
- Permite funciones como VAD (Voice Activity Detection) para dejar de transmitir
  paquetes durante los silencios, ahorrando mas del 40% del ancho de banda.



## 2. LA ARQUITECTURA DE PROTOCOLOS DE VOIP (SENALIZACION vs MEDIOS)

En VoIP existe una division estricta entre el control de la llamada y el audio:

  [Telefono A]                                                  [Telefono B]
       |                                                             |
       | ====== 1. Senalizacion y Control (SIP / H.323) ===========> |
       |    (Establecimiento, timbre, negociacion SDP y corte)       |
       |                                                             |
       | <===== 2. Flujo de Audio en Tiempo Real (RTP) =============> |
       |    (Voz digitalizada en paquetes UDP directos cada 20 ms)    |
       |                                                             |
       | <..... 3. Estadisticas de Calidad (RTCP) ..................> |
       |    (Reporte periodico de Jitter, perdida y latencia)        |


### a) Senalizacion (SIP - Session Initiation Protocol / RFC 3261):

   - Protocolo en texto plano (similar a HTTP) que opera en puerto UDP/TCP 5060
     (o TCP 5061 con TLS cifrado).
   - Administra el registro de extensiones (SIP REGISTER), inicio de llamada (INVITE),
     respuesta (200 OK) y finalizacion (BYE).


### b) Descripcion de la Sesion (SDP - Session Description Protocol / RFC 4566):

   - Va embebido dentro del cuerpo de los mensajes SIP.
   - Negocia la direccion IP donde se enviara la voz, el puerto UDP efimero y el
     codec de compresion acordado entre ambos telefonos.


### c) Transporte de Medios (RTP - Real-time Transport Protocol / RFC 3550):

   - Transporta la voz en paquetes UDP de baja sobrecarga (puertos dinamicos 10000 a 32767).
   - Incluye marcas de tiempo (Timestamps) y numeros de secuencia para reconstruir
     el flujo de audio en orden.



## 3. CODECS DE COMPRESION DE VOZ Y ANCHO DE BANDA


| Codec | Estandar | Tasa de Bits | Muestreo | MOS Score | Ancho de Banda con IP/UDP |
| :--- | :--- | :--- | :--- | :--- | :--- |
| G.711u/a | PCM Estandar 64 Kbps | 8 kHz | 4.1 / 5.0 | ~87.2 Kbps (Sin compresion) |  |
| G.729 / A | CS-ACELP | 8 Kbps | 8 kHz | 3.9 / 5.0 | ~31.2 Kbps (Alta compresion) |
| G.722 | HD Voice | 64 Kbps | 16 kHz | 4.3 / 5.0 | ~87.2 Kbps (Alta definicion) |
| Opus | IETF | 6 a 510 Kbps | 48 kHz | 4.5 / 5.0 | Dinamico / Adaptable |
| T.38 | Fax Relay | N/A | N/A | N/A | Protocolo para transmision de Fax |

- MOS (Mean Opinion Score): Metrica estandar humana de 1 a 5 para calificar la calidad de voz.
  Un MOS superior a 4.0 representa calidad cristalina comparable a llamada fija.
- Tiempo de Paquetizacion (ptime): Estandar de 20 milisegundos (50 paquetes por segundo).



## 4. EL DILEMA DE NAT Y EL PROBLEMA DEL SIP ALG


### a) El Problema de Travesia de NAT (NAT Traversal):

   - SIP incluye direcciones IP privadas dentro del cuerpo SDP (`c=IN IP4 192.168.1.50`).
   - Cuando el paquete cruza un router con NAT hacia Internet, la IP privada queda atrapada.
   - El telefono remoto intenta enviar el audio RTP a una IP privada inalcanzable,
     generando el problema de "Audio de una sola via" (One-Way Audio).
   - Mecanismos de solucion: STUN (RFC 5389), TURN (RFC 5766) o un SBC (Session Border Controller).


### b) SIP ALG (Application Layer Gateway) - EL ENEMIGO DE LA TELEFONIA:

   - Los routers domesticos o comerciales suelen traer habilitada la funcion "SIP ALG".
   - En teoria busca corregir las IPs de NAT; en la practica corrompe los puertos UDP,
     altera las sumas de verificacion y corta llamadas a los 30 segundos.
   - REGLA DE ORO DE VOIP: ¡DESHABILITAR SIEMPRE SIP ALG EN TODOS LOS ROUTERS Y FIREWALLS!



## 5. INDICE DE ARCHIVOS DE LA CARPETA TELEFONIA

[00_INDICE_Y_FUNDAMENTOS_VOIP.md](./00_INDICE_Y_FUNDAMENTOS_VOIP.md)
    - Principios de telefonia, SIP, SDP, RTP, codecs de audio y resolucion de problemas de NAT.

[01_ARQUITECTURA_PBX_Y_COMPONENTES.md](./01_ARQUITECTURA_PBX_Y_COMPONENTES.md)
    - Arquitectura de un PBX/Conmutador: Extensiones, Troncales SIP vs E1/PRI vs FXO/FXS,
      Grupos de Timbrado (Hunt Groups), IVR / Operadora Automatica, Voicemail y CDR.

[02_AVAYA_IP_OFFICE_500V2_HARDWARE_Y_LICENCIAMIENTO.md](./02_AVAYA_IP_OFFICE_500V2_HARDWARE_Y_LICENCIAMIENTO.md)
    - Chasis Avaya IP500v2, ranuras base, tarjetas VCM (DSP), Combo Card, tarjetas PRI,
      modulos de expansion externos, tarjeta SD del sistema y esquema de licencias.

[03_AVAYA_MANAGER_CONFIGURACION_PASO_A_PASO.md](./03_AVAYA_MANAGER_CONFIGURACION_PASO_A_PASO.md)
    - Guia practica en software Avaya IP Office Manager: Extensiones H.323/SIP/Digitales,
      Troncales SIP con ITSP, Codigos Cortos (Short Codes), ARS, Rutas Entrantes (ICR) y Hunt Groups.

[04_PROVISIONAMIENTO_TELEFONOS_DHCP_Y_46XXSETTINGS.md](./04_PROVISIONAMIENTO_TELEFONOS_DHCP_Y_46XXSETTINGS.md)
    - Despliegue masivo de telefonos Avaya: Opcion DHCP 242 con salto a VLAN de voz,
      servidor HTTP embebido y edicion del archivo maestro 46xxsettings.txt.

[05_DIAGNOSTICO_MANTENIMIENTO_Y_RECUPERACION_AVAYA.md](./05_DIAGNOSTICO_MANTENIMIENTO_Y_RECUPERACION_AVAYA.md)
    - Herramientas de soporte oficial: System Status Application (SSA), SysMonitor (trazas SIP),
      recuperacion por puerto de consola serial DTE y comandos de reseteo a fabrica (AT-X).

[06_AVAYA_INTERCONEXION_SCN_MULTI_SITIO.md](./06_AVAYA_INTERCONEXION_SCN_MULTI_SITIO.md)
    - Interconexion multi-sitio Small Community Network (SCN): Lineas IP H.323 entre conmutadores,
      marcacion transparente entre sedes, buzon de voz centralizado, Hot Desking distribuido y fallbacks.


## SUBCARPETAS INCLUIDAS:

OpenSource_Asterisk_FreePBX_Issabel/
    - Suite completa de telefonia de codigo abierto: Motor Asterisk, Dialplan, GUI FreePBX

e Issabel, laboratorio virtual en VMware/VirtualBox, softphones, IVR y Fail2Ban.
