# 01. CAPA 1: CAPA FISICA (PHYSICAL LAYER) - MEDIOS, SENALES Y HARDWARE

> **MODELO OSI (OPEN SYSTEMS INTERCONNECTION) - GUIA MAESTRA PARA CERTIFICACIONES**  
> *Guía de referencia técnica y preparación para certificaciones Cisco CCNA 200-301, CompTIA Network+ y Huawei HCIA.*

---


## 1. FUNCION Y ALCANCE DE LA CAPA FISICA

La Capa Fisica es la base fundamental del modelo OSI. Su unico proposito es
transportar la secuencia de bits sin procesar (0s y 1s) a traves de un medio de
transmision fisico (cobre, fibra optica o aire/ondas de radio).

La Capa 1 NO interpreta el significado de los datos, NO sabe que es una direccion IP,
NO entiende direcciones MAC ni nombres de archivo. Solo maneja pulsos electricos,
destellos de luz y ondas electromagneticas.

Funciones clave de la Capa 1:
- Codificacion de senales: Convertir los datos digitales en senales comprensibles
  para el medio (Manchester, NRZ, 4B/5B, PAM4).
- Señalizacion y sincronizacion: Definir que voltaje o intensidad representa un '1'
  o un '0', y sincronizar los relojes del emisor y receptor (Bit Timing).
- Especificaciones mecanicas y electricas: Forma de los conectores (RJ45, LC, SC),
  voltajes, calibres de cable (AWG), frecuencias y pinouts.


## 2. MEDIOS DE TRANSMISION GUIADOS: COBRE (UTP / STP)

El cable de par trenzado de cobre es el medio mas utilizado en redes LAN de oficina.
¿Por que estan trenzados los pares de hilos?
- Efecto de Cancelacion: Cuando la corriente viaja por dos cables trenzados en
  direcciones opuestas, sus campos magneticos se anulan mutuamente, eliminando
  la interferencia electromagnetica externa (EMI) y la diafonia (Crosstalk)
  entre pares adyacentes.

### a) Tipos de cable de par trenzado:

   - UTP (Unshielded Twisted Pair): Sin blindaje metalico. Economico, flexible y estandar.
   - STP / FTP (Shielded / Foiled): Con malla metalica o papel de aluminio. Protege
     contra entornos industriales de alto ruido electromagnetico. Requiere puesta a tierra.

### b) Categorias de cable UTP (Concepto indispensable de certificacion):

| Categoria | Frecuencia | Velocidad Maxima | Distancia Maxima | Uso Principal |
| :--- | :--- | :--- | :--- | :--- |
| Cat 5e | 100 MHz | 1 Gbps (Gigabit) | 100 metros | Redes LAN basicas |
| Cat 6 | 250 MHz | 1 Gbps | 100 metros | Estandar corporativo actual |
| 10 Gbps (10GBASE-T) 37 a 55 metros | (depende de diafonia) |  |  |  |
| Cat 6a | 500 MHz | 10 Gbps | 100 metros | Datacenters y Wi-Fi 6/7 |
| Cat 7 | 600 MHz | 10 Gbps | 100 metros | Industrial (blindado) |
| Cat 8 | 2000 MHz | 25 / 40 Gbps | 30 metros | Interconexion Top-of-Rack |


### c) Estandares de Ponchado TIA/EIA-568A vs TIA/EIA-568B:

| Pin | TIA/EIA-568A (Residencial / Gobierno) | TIA/EIA-568B (Estandar Comercial) |
| :--- | :--- | :--- |
| 1 | Blanco / Verde | Blanco / Naranja |
| 2 | Verde | Naranja |
| 3 | Blanco / Naranja | Blanco / Verde |
| 4 | Azul | Azul |
| 5 | Blanco / Azul | Blanco / Azul |
| 6 | Naranja | Verde |
| 7 | Blanco / Marron | Blanco / Marron |
| 8 | Marron | Marron |


### d) Tipos de cables segun sus extremos:

   - Cable Directo (Straight-Through): Mismo estandar en ambos lados (568B en ambos).
     Se usa para conectar dispositivos de DIFERENTE capa: PC a Switch, Router a Switch.
   - Cable Cruzado (Crossover): Un extremo 568A y el otro 568B (cruza pines 1-3 y 2-6).
     Se usaba historicamente para conectar dispositivos de la MISMA capa: Switch a Switch,
     PC a PC, Router a PC.
     *Nota moderna de examen: Hoy en dia casi todos los puertos implementan Auto-MDIX,
      tecnologia que detecta y cruza los pines electronicamente de forma automatica.
   - Cable de Consola (Rollover): Pines 1-8 invertidos. Conecta el puerto de consola
     del switch o router al puerto serie/USB de la laptop del ingeniero.


## 3. MEDIOS DE TRANSMISION GUIADOS: FIBRA OPTICA

La fibra optica transmite datos mediante pulsos de luz dentro de un hilo de vidrio
o plastico purificado, basandose en el principio de Reflexion Interna Total.
Ventajas sobre el cobre:
- Totalmente inmune a interferencias electromagneticas y descargas electricas.
- Distancias de conexion enormes (kilometros) con minima atenuacion.
- Ancho de banda casi ilimitado (10G, 40G, 100G, 400G, 800G).

## Comparativa de Examen: Fibra Monomodo (SMF) vs Multimodo (MMF)

| Caracteristica | Fibra Monomodo (SMF) | Fibra Multimodo (MMF) |
| :--- | :--- | :--- |
| Diametro del Nucleo | Pequeno: 9 micrometros (µm) | Grande: 50 o 62.5 µm |
| Fuente de Luz | Laser de alta potencia | LED o VCSEL |
| Longitudes de Onda | 1310 nm / 1550 nm | 850 nm / 1300 nm |
| Distancias Maximas | 10 km a 40 km (hasta 100 km) | 300 a 550 metros |
| Dispersion | Cero dispersion modal | Sufre dispersion modal |
| Color de la Chaqueta | Amarillo | Naranja (OM1/OM2) / Aqua (OM3/OM4) |
| Costo de Equipos | Transceptores caros | Transceptores economicos |
| Uso Principal | Backbones Campus, WAN, ISP | Datacenters, cableado de edificio |


Tipos de Conectores de Fibra Optica:
- LC (Lucent Connector): Conector pequeño de ajuste por clic (estandar en transceptores SFP).
- SC (Subscriber Connector): Cuadrado tipo "push-pull" (utilizado en telecomunicaciones).
- ST (Straight Tip): Redondo con bayoneta de giro (equipos legados).
- MPO / MTP: Conector multifibra de 12 o 24 hilos (utilizado en troncales 40G/100G QSFP).


## 4. MEDIOS NO GUIADOS: REDES INALAMBRICAS (RADIOFRECUENCIA)

Transportan senales electromagneticas utilizando el espectro radioelectrico:
- Banda de 2.4 GHz: Gran alcance y penetracion de muros, pero propensa a interferencias
  (microondas, bluetooth) y solo cuenta con 3 canales que no se solapan: 1, 6 y 11.
- Banda de 5 GHz: Mayor velocidad y menor saturacion (24 canales no solapados), pero
  menor alcance y dificultad para atravesar paredes de concreto.
- Banda de 6 GHz (Wi-Fi 6E y Wi-Fi 7): Maxima velocidad, latencia minima y espectro
  limpio sin colisiones de dispositivos heredados.


## 5. DISPOSITIVOS Y HARDWARE DE CAPA 1

- Repetidor (Repeater): Dispositivo de 2 puertos que regenera y amplifica la senal
  atenuada para extender el alcance maximo del medio.
- Hub (Concentrador): Repetidor multipuerto. Cuando recibe un bit por un puerto,
  lo retransmite por TODOS los demas puertos sin mirar direcciones.
  *Regla de Examen: Todos los puertos de un Hub pertenecen al MISMO dominio de colision
   y operan en Half-Duplex. Hoy en dia son piezas de museo reemplazadas por Switches.
- Transceptores Modulares (SFP / SFP+ / QSFP): Convierten senales opticas en electricas.
- Cables DAC (Direct Attach Copper) y AOC (Active Optical Cable): Cables gemelos con
  conectores SFP integrados de fabrica para enlaces cortos de rack (1 a 5 metros).


## 6. METRICAS CRITICAS Y PROBLEMAS DE CAPA FISICA

- Ancho de Banda (Bandwidth): Capacidad teorica maxima del medio (ej. 1 Gbps).
- Throughput (Rendimiento Real): Cantidad real de datos transferidos por segundo
  (siempre menor al ancho de banda debido a encabezados de protocolos).
- Goodput: Cantidad de datos utiles de usuario libres de sobrecarga de red (Goodput = Throughput - Headers).
- Atenuacion: Perdida progresiva de potencia de la senal a medida que viaja por el cable.
- Diafonia (Crosstalk): Interferencia causada por campos electromagneticos de cables vecinos
  (NEXT: Near-End Crosstalk, FEXT: Far-End Crosstalk).
- Latencia: Tiempo que tarda un bit en viajar desde el origen hasta el destino.
- Jitter: Variacion en el tiempo de llegada de los paquetes (critico en VoIP y streaming).


## 7. BANCO DE PREGUNTAS DE EXAMEN (TIPO CCNA / NETWORK+)

### ❓ Pregunta 1
> **¿Cual de los siguientes medios sufre de dispersion modal?**

A) Fibra Monomodo (SMF)
B) Fibra Multimodo (MMF) [CORRECTA: Debido a su nucleo ancho, la luz viaja en multiples rayos/modos reflejados a diferentes velocidades]
C) Cable UTP Categoria 6a
D) Cable Coaxial

### ❓ Pregunta 2
> **¿Cual es el estandar de ponchado TIA/EIA-568B para los pines 1, 2, 3 y 6?**

Respuesta: Pin 1: Blanco/Naranja, Pin 2: Naranja, Pin 3: Blanco/Verde, Pin 6: Verde.
## (Recuerde: los pares de transmision y recepcion en 10/100 Mbps usan los pines 1, 2, 3 y 6).

