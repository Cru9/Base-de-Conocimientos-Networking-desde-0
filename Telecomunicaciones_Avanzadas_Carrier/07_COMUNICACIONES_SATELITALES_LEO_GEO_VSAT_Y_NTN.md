# 07. COMUNICACIONES SATELITALES, MEGACONSTELACIONES LEO, VSAT Y REDES NTN (3GPP)

> **TELECOMUNICACIONES AVANZADAS, REDES DE CARRIER E INFRAESTRUCTURA GLOBAL**


---



## 1. LA REVOLUCION ESPACIAL: DE SATELITES FIJOS A MEGACONSTELACIONES

Las telecomunicaciones satelitales han vivido la mayor disrupcion de su historia:
el transito de satelites geoestacionarios distantes y lentos hacia constelaciones
de miles de satelites en orbita baja (LEO) interconectados por laseres opticos.

COMPARATIVA ORBITAL: GEO VS MEO VS LEO

| Parametro | GEO (Geostacionario) | MEO (Orbita Media) | LEO (Orbita Baja) |
| :--- | :--- | :--- | :--- |
| Altitud de Orbita | 35,786 km sobre ecuador 2,000 a 20,000 km | 500 a 1,500 km |  |
| Ejemplos Reales | Intelsat, Eutelsat, SES SES O3b mPOWER, GPS | Starlink (SpaceX), OneWeb, Kuiper |  |
| Numero de Satelites | 3 cubren la Tierra | 10 a 20 satelites | Miles (Starlink opera > 6,000) |
| Latencia RTT Fisica | ~550 ms a 650 ms | ~120 ms a 150 ms | 25 ms a 45 ms (Nivel Fibra Optica) |
| Velocidad Orbital | Sincrona con la Tierra | Media | ~27,000 km/h (Pasa en 10 min) |
| Tipo de Antena Cliente | Parabolica Fija | Rastreo Motorizado | Matriz en Fase (Phased Array) |
| Perdida de Espacio Libre Extrema (> 205 dB) | Media (~180 dB) | Baja (~150 a 160 dB) |  |


ENLACES INTER-SATELITALES POR LASER (ISL - OPTICAL INTER-SATELLITE LINKS):
- Los satelites LEO modernos se comunican entre si mediante rayos laser en el vacio del espacio.
- Como la luz viaja un 47% mas rapido en el vacio (300,000 km/s) que dentro del vidrio de una
  fibra optica terrestre (204,000 km/s), una conexion satelital LEO por laser entre Londres
  y Singapur puede tener MENOR latencia que el cable submarino de fibra optica mas rapido.



## 2. REDES NO TERRESTRES (NTN - NON-TERRESTRIAL NETWORKS EN 3GPP)

Los estandares de telefonia celular 3GPP Release 17 y 18 definieron la convergencia
nativa entre las redes 5G terrestres y los satelites espaciales:

1. Direct-to-Cell (Conexion Directa al Telefono Celular):
   - El satelite en el espacio actua como una estacion base 5G (gNodeB) o repetidor transparente.
   - Un smartphone convencional sin antenas voluminosas puede enviar mensajes de texto,
     llamadas de emergencia o datos de baja velocidad directamente al espacio.
2. Desafios Fisicos Resueltos por el Algoritmo NTN:
   - Corrimiento Doppler Masivo: Debido a que el satelite vuela a 7.5 km/s respecto al suelo,
     la frecuencia recibida cambia continuamente; el modem celular compensa el Doppler en tiempo real.
   - Timing Advance (TA) Dinamico: Compensa el retardo variable de milisegundos conforme
     el satelite se acerca o se aleja en el horizonte.



## 3. ARQUITECTURA DE UNA ESTACION TERRENA VSAT

Una terminal VSAT (Very Small Aperture Terminal) se compone de:

              [ REFLECTOR PARABOLICO ]
                         |
                    (Feedhorn)
                         |
```text
           +-----------------------------+
           | OMT (Orthomode Transducer)  | <--- Separa recepcion y transmision por polarizacion
           +-----------------------------+
               /                     \
              /                       \
   +-----------------------+     +-----------------------+
   |   LNB (Downconverter) |     |  BUC (Upconverter/PA) |
   | - Recibe 12 GHz (Ku)  |     | - Transmite 14 GHz    |
   | - Convierte a Banda L |     | - Potencia 2W a 40W   |
   |   (950 - 2150 MHz)    |     | - Amplificador GaN    |
   +-----------------------+     +-----------------------+
              |                              ^
          (Coaxial)                      (Coaxial)
              v                              |
   +-----------------------------------------------------+
   |           MODEM SATELITAL (DVB-S2X / TDMA)          |
   +-----------------------------------------------------+
                             |
                   (Ethernet / IP LAN)

Funciones de los Componentes de RF:
1. LNB (Low Noise Blockdownconverter):
   - La senal que llega del espacio despues de cruzar la atmosfera es debilisima (-90 a -120 dBm).
   - El LNB amplifica la senal introduciendo un ruido microscopico (Figura de Ruido NF < 0.7 dB)
     y la traslada a frecuencias de Banda L (950 a 2150 MHz) que pueden viajar por cable coaxial.
2. BUC (Block Upconverter):
   - Toma la senal en Banda L generada por el modem, la eleva a la frecuencia satelital de subida
     (Uplink) y la amplifica en potencia mediante transistores de Nitruro de Galio (GaN).
3. Antenas Planas Phased Array (AESA):
   - En las constelaciones LEO (Starlink/OneWeb), se eliminan los platos parabolicos.
   - Se utiliza una antena plana con miles de pequenos parches de antena independientes.
   - Modificando la fase electrica de cada elemento en microsegundos, el haz de radio
     apunta hacia el cielo y salta de un satelite a otro sin ningun movimiento mecanico.
```


## 4. BANDAS DE FRECUENCIA SATELITALES


| Banda | Frecuencia Bajada | Frecuencia Subida | Ventajas / Desventajas |
| :--- | :--- | :--- | :--- |
| Banda C | 3.7 a 4.2 GHz | 5.9 a 6.4 GHz | Inmune a la lluvia. Requiere antenas enormes (2.4 a 3.8m). |
| Banda Ku | 10.7 a 12.75 GHz | 13.75 a 14.5 GHz | Antenas pequenas (0.9 a 1.2m). Moderada perdida por lluvia. |
| Banda Ka | 17.7 a 21.2 GHz | 27.5 a 31.0 GHz | Anchos de banda gigantescos (Gbps). Muy sensible a tormentas. |
| Banda Q/V | 37.5 a 52.4 GHz | 47.2 a 51.4 GHz | Utilizada para los Gateways troncales de las megaconstelaciones. |




## 5. METODOS DE ACCESO AL CANAL: SCPC VS MF-TDMA

1. SCPC (Single Channel Per Carrier):
   - Enlace dedicado punto a punto con ancho de banda 100% garantizado (CIR = 100%).
   - Se asigna una frecuencia exclusiva al modem de subida.
   - Ideal para troncales de telefonica celular, plataformas petroleras y bases militares.

2. MF-TDMA (Multi-Frequency Time Division Multiple Access):
   - Acceso compartido por demanda (BoD - Bandwidth on Demand).
   - Miles de estaciones remotas (ej. cajeros automaticos, gasolineras) comparten un pool
     de frecuencias y ranuras de tiempo asignadas dinamicamente por la estacion maestra (Hub).



## 6. EL ESTANDAR DVB-S2X Y MODULACION ADAPTATIVA (ACM)

DVB-S2X es el estandar mundial lider de transmision digital por satelite:
- Modulaciones avanzadas: QPSK, 8PSK, 16-APSK, 32-APSK, 64-APSK, 128-APSK y 256-APSK.
- Factores de Roll-Off ultra estrechos (5%, 10%, 15%) que exprimen cada kilohercio del transpondedor.
- ACM (Adaptive Coding and Modulation): Si una tormenta nubla la antena de una estacion remota,
  el satelite conmuta unicamente el flujo de esa terminal a una modulacion mas robusta (QPSK),
  mientras continua transmitiendo a 64-APSK al resto de las ciudades despejadas.



## 7. ACELERACION TCP (PEP) Y REDES TOLERANTES A DEMORAS (DTN)

1. El Problema de TCP sobre Satelites GEO (600 ms de latencia):
   - El protocolo TCP asume que cualquier retraso en recibir un ACK significa congestion,
     reduciendo la ventana de congestion (CWND) y estrangulando el ancho de banda a 1 o 2 Mbps
     aunque el cliente haya contratado un enlace de 50 Mbps.
2. Proxies de Mejora de Rendimiento (PEP - RFC 3135):
   - El modem satelital actua como un proxy intermedio: genera un ACK local inmediato
     hacia el servidor emisor (TCP Spoofing) y transporta los datos sobre el enlace satelital
     utilizando un protocolo optimizado para alto retardo (BDP - Bandwidth Delay Product).
3. Redes Tolerantes a Demoras (DTN - RFC 5050 / Bundle Protocol):
   - Arquitectura basada en almacenamiento y reenvio ("Store-and-Forward").
   - Los datos se guardan en el satelite o estacion terrena de forma segura hasta que

el siguiente nodo orbital este a la vista, garantizando entrega confiable en comunicaciones espaciales.
