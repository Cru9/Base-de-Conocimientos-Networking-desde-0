# 00. INDICE GENERAL, RETOS DEL TRAFICO IP Y MODELOS DE QOS

> **CALIDAD DE SERVICIO Y CONFORMACION DE TRAFICO (QOS & TRAFFIC SHAPING)**


---



## 1. LA NECESIDAD DE CALIDAD DE SERVICIO (QOS)

Por naturaleza, las redes IP tradicionales operan bajo el principio de "Best Effort"
(Mejor Esfuerzo): todos los paquetes son tratados con la misma prioridad; no hay
garantias de entrega ni orden de llegada.

Sin embargo, el trafico empresarial moderno tiene requisitos diametralmente opuestos:
- Una llamada de Telefonia IP (VoIP) o videoconferencia requiere latencia minima y
  entrega constante en tiempo real; 1 segundo de retraso arruina la comunicacion.
- Una descarga de archivo por FTP o actualizacion de Windows puede esperar varios
  segundos sin que el usuario note degradacion.


## LOS CUATRO ENEMIGOS DEL RENDIMIENTO DE RED:


### a) Falta de Ancho de Banda (Bandwidth Saturation):

   - Ocurre cuando la demanda de trafico supera la capacidad fisica del enlace.
   - Solucion QoS: Priorizacion selectiva y descarte de trafico no esencial.


### b) Latencia o Retardo (Delay):

   - Tiempo total que tarda un paquete en viajar del origen al destino.
   - Umbral maximo tolerable para voz y video: < 150 milisegundos (unidireccional).


### c) Jitter (Variacion del Retardo):

   - Fluctuacion irregular en los tiempos de llegada de paquetes contiguos.
   - Umbral maximo tolerable para voz: < 30 milisegundos.


### d) Perdida de Paquetes (Packet Loss):

   - Descarte de paquetes en colas saturadas de routers o conmutadores.
   - Umbral maximo tolerable para voz: < 1% de perdida.



## 2. LOS TRES MODELOS ARQUITECTONICOS DE QOS


### a) Best Effort (Sin QoS):

   - El router no clasifica los paquetes. Aplica una cola simple FIFO (First-In,
     First-Out). Quien llega primero se envia primero.


### b) IntServ (Integrated Services - Servicios Integrados / RFC 1633):

   - Modelo de "Reserva Explicita": utiliza el protocolo RSVP (Resource Reservation
     Protocol) para solicitar y reservar ancho de banda en CADA router del trayecto
     antes de iniciar la transmision de datos.
   - Limitacion: No escala en redes corporativas ni en Internet; los routers consumen
     toda su memoria y CPU manteniendo tablas de estado por flujo.


### c) DiffServ (Differentiated Services - Servicios Diferenciados / RFC 2474 / 2475):

   - EL ESTANDAR DE FACTO DE LA INDUSTRIA.
   - Modelo sin estado (Stateless): El trafico se clasifica y se marca en el primer
     salto de la red (en la cabecera IP o Ethernet).
   - Los routers intermedios no mantienen estado por sesion; simplemente leen la
     etiqueta del paquete y aplican un "Comportamiento por Salto" (PHB - Per-Hop Behavior).
   - Es ultra-escalable y procesado directamente por el hardware de los conmutadores.



## 3. LIMITES DE CONFIANZA (TRUST BOUNDARIES)

Un concepto de seguridad fundamental en QoS: "¿En que punto de la red confiamos
en las marcas de prioridad de los paquetes?".

```text
  [PC Usuario] ---- (Sin Confianza) ----> [Switch Acceso] ---- (Confiable) ----> [Core / WAN]
         |                                       ^
         |--- [Telefono IP] (Confiable) ---------|

- Por defecto, una PC de usuario NO es confiable. Un usuario podria alterar su
  sistema operativo para marcar sus descargas de torrent o videojuegos con maxima prioridad.
- El switch de acceso DEBE reescribir a cero (Untrusted) el trafico proveniente de PCs.
- Los telefonos IP empresariales son dispositivos autorizados (Trusted Boundary);
  el switch respeta sus marcas de Voz (CoS 5 / DSCP EF 46).
```


## 4. INDICE DE ARCHIVOS DE LA CARPETA QOS_TRAFFIC_SHAPING

[00_INDICE_Y_ARQUITECTURA_QOS.md](./00_INDICE_Y_ARQUITECTURA_QOS.md)
    - Fundamentos de QoS, los 4 problemas de red, comparativa Best Effort vs IntServ vs DiffServ
      y limites de confianza (Trust Boundaries).

[01_CLASIFICACION_Y_MARCADO_COS_DSCP.md](./01_CLASIFICACION_Y_MARCADO_COS_DSCP.md)
    - Marcado de Capa 2 (802.1p CoS) y Capa 3 (IPv4 ToS / DiffServ DSCP: CS, AF, EF),
      tablas de equivalencia y clasificacion de trafico corporativo.

[02_MECANISMOS_DE_COLAS_Y_CONGESTION.md](./02_MECANISMOS_DE_COLAS_Y_CONGESTION.md)
    - Algoritmos de planificacion por hardware: FIFO, PQ, CBWFQ, LLQ (Low Latency Queuing),
      evitacion de congestion (Tail Drop vs WRED) y sincronizacion global TCP.

[03_TRAFFIC_POLICING_VS_SHAPING.md](./03_TRAFFIC_POLICING_VS_SHAPING.md)
    - Diferencias matematicas entre Policing (descarte/remarcado) y Shaping (buffer/suavizado),
      algoritmo Token Bucket (CIR, Bc, Be, Tc) y marcadores Two-Rate Three-Color.

[04_CONFIGURACIONES_QOS_POR_MARCA.md](./04_CONFIGURACIONES_QOS_POR_MARCA.md)
    - Plantillas de configuracion completas para entornos empresariales en

## Cisco IOS-XE (MQC), Huawei VRP y ArubaOS-CX.
