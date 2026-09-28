# 06. RADIOENLACES DE MICROONDAS, PROPAGACION RF, PTP, PTMP Y E-BAND (80 GHZ)

> **TELECOMUNICACIONES AVANZADAS, REDES DE CARRIER E INFRAESTRUCTURA GLOBAL**


---



## 1. EL ROL DE LOS RADIOENLACES EN LA RED DE TRANSPORTE (BACKHAUL)

Aunque la fibra optica ofrece un ancho de banda casi ilimitado, en la geografia real
existen obstaculos insuperables: cadenas montanosas, cruces de rios, desiertos, selvas
o la lentitud burocratica de permisos municipales para abrir zanjas en avenidas.

Los radioenlaces de microondas proporcionan conectividad carrier de alta capacidad
(desde 1 Gbps hasta 20 Gbps) en cuestion de dias:
- Backhaul Celular: Interconectan las torres de antenas 4G/5G con los centros de conmutacion.
- Redes de Transporte Rural y Mineria: Conectan poblaciones aisladas a cientos de kilometros.
- Enlaces de Mision Critica: Respaldo geograficamente disjunto de cables de fibra optica.



## 2. BANDAS DE FRECUENCIA Y ARQUITECTURAS DE HARDWARE


| Rango de Banda | Frecuencias Tipicas | Distancia de Salto | Capacidad Tipica |
| :--- | :--- | :--- | :--- |
| Microondas Bajas | 6 GHz, 7 GHz, 8 GHz, 11 GHz | 20 km a 60+ km | 300 Mbps a 1 Gbps |
| Microondas Medias | 13 GHz, 15 GHz, 18 GHz, 23 GHz 5 km a 20 km | 500 Mbps a 1.5 Gbps |  |
| Microondas Altas | 26 GHz, 32 GHz, 38 GHz | 1 km a 5 km | 1 Gbps a 2.5 Gbps |
| V-Band (No Licenciada) | 60 GHz (Absorcion O2) | 100 m a 800 m | 1 Gbps a 2.5 Gbps |
| E-Band (Ondas Milim.) | 70 GHz / 80 GHz | 1 km a 4 km | 10 Gbps a 20 Gbps Full Duplex |


ARQUITECTURAS FISICAS DE RADIOMIKROONDAS:
1. Full Outdoor (FOD):
   - Todo el sistema (radio, modem y procesador de banda base) va integrado en una caja
     compacta fijada directamente en la parte posterior de la antena parabolica en la torre.
   - Hacia la sala de equipos solo baja un cable de fibra optica y alimentacion DC/PoE.
2. Split-Mount (La mas extendida en carriers):
   - ODU (Outdoor Unit): Transceptor de radiofrecuencia montado en la antena en la torre.
   - IDU (Indoor Unit): Modem modulador/demodulador y switch L2/L3 en el rack de la caseta.
   - Conectados entre si por un cable coaxial que transporta Frecuencia Intermedia (IF).
3. All-Indoor (Larga Distancia y Alta Potencia):
   - Transmisores de radiofrecuencia pesados en la sala climatizada; la senal de microondas
     sube a la torre a traves de Guias de Onda elipticas presurizadas con nitrogeno.



## 3. TEORIA DE PROPAGACION Y LINEA DE VISTA (LINE OF SIGHT - LOS)

Un radioenlace de microondas requiere Linea de Vista Optica y Radioelectrica limpia:

LA PRIMERA ZONA DE FRESNEL:
Es el volumen elipsoidal que rodea al haz directo de radio. Si un obstaculo (la copa
de un arbol, un edificio o una loma) penetra en esta zona, las ondas reflejadas
llegan al receptor desfasadas 180 grados, cancelando la senal (interferencia destructiva).

Formula del Radio de la Primera Zona de Fresnel (R1 en metros):
R1 = 17.32 * sqrt( (d1 * d2) / (f_GHz * D_km) )

Donde:
- d1 y d2: Distancias desde el obstaculo a cada antena (km).
- D_km: Distancia total del enlace (km).
- f_GHz: Frecuencia de operacion (GHz).

CRITERIO DE DISENO OBLIGATORIO:
El obstaculo mas cercano debe dejar libre AL MENOS EL 60% del radio R1 (idealmente el 100%)
mas un margen de seguridad por el crecimiento futuro de los arboles.

CURVATURA DE LA TIERRA Y FACTOR K:
Debido a que la atmosfera terrestre disminuye su densidad con la altura, las ondas
de radio sufren refraccion (se doblan ligeramente hacia el suelo).
- Factor K normal (Atmosfera Estandar): K = 4/3 (~1.33). La Tierra parece mas plana.
- Sub-refraccion (K < 1, ej. niebla matutina densa o inversiones termicas): El haz
  se curva hacia arriba y el terreno geografico parece levantarse, tapando el enlace.



## 4. CALCULO MATEMATICO DEL ENLACE (LINK BUDGET)

La ecuacion fundamental de balance de potencia determina si el enlace funcionara:

Prx (dBm) = Ptx + Gtx + Grx - FSL - Lcables - Lgases - Alluvia

1. Perdida en el Espacio Libre (Free Space Loss - FSL en dB):
   FSL = 92.45 + 20 * log10(f_GHz) + 20 * log10(D_km)

   Ejemplo: Enlace de 15 km en banda de 11 GHz:
   FSL = 92.45 + 20 * log10(11) + 20 * log10(15)
   FSL = 92.45 + 20.83 + 23.52 = 136.8 dB de atenuacion en el aire.

2. Margen de Desvanecimiento (Fade Margin - FM):
   FM = Prx_calculada - Sensibilidad_minima_del_receptor

   Para lograr disponibilidad de Carrier de "Cinco Nueves" (99.999% del ano, equivalente
   a menos de 5 minutos de corte acumulado al ano), el Margen de Desvanecimiento
   debe ser de 30 a 45 dB.



## 5. ATENUACION POR LLUVIA (ITU-R P.530) Y MODULACION ADAPTATIVA (ACM)

Por encima de 10 GHz, el tamano de las gotas de lluvia coincide con la longitud de
onda del haz, absorbiendo y dispersando la energia de radio (Rain Fade).

MODULACION Y CODIFICACION ADAPTATIVA (ACM - ADAPTIVE CODING AND MODULATION):
La tecnologia que erradico las caidas totales de radioenlaces ante tormentas:
- Cielo Despejado: La radio negocia 4096-QAM (12 bits por simbolo), entregando 1.2 Gbps.
- Lluvia Moderada: El procesador detecta caida de senal y conmuta sin perder un solo bit
  a 512-QAM o 256-QAM (800 Mbps).
- Tormenta Torrencial Extrema: La radio degrada dinamicamente a QPSK (2 bits por simbolo).
  El ancho de banda se reduce a 100 Mbps, pero el enlace NUNCA cae, manteniendo vivas
  las llamadas de emergencia, el control de la red y el trafico prioritario.



## 6. ESQUEMAS DE PROTECCION Y DIVERSIDAD

1. 1+0 (Sin Proteccion): Un transmisor y un receptor. Si la ODU se quema, el enlace muere.
2. 1+1 HSB (Hot Standby): Dos ODUs conectadas a la misma antena mediante un acoplador.
   Una radio transmite activamente; la segunda esta encendida en caliente lista para
   asumir la transmision en menos de 50 milisegundos si la principal falla.
3. 1+1 SD (Space Diversity / Diversidad de Espacio):
   - Dos antenas parabólicas separadas verticalmente de 3 a 5 metros en la misma torre.
   - Combate el desvanecimiento por trayectos multiples (Multipath Fading).
4. 2+0 XPIC (Cross-Polarization Interference Cancellation):
   - Duplica la capacidad utilizando EXACTAMENTE LA MISMA frecuencia.
   - Emite simultaneamente un flujo en Polarizacion Vertical (V) y otro en Polarizacion Horizontal (H).
   - Un chip digital en la IDU cancela en tiempo real la interferencia mutua entre ambas polarizaciones.



## 7. PROCEDIMIENTO DE ALINEACION EN CAMPO

Para alinear dos antenas parabolicas de haz estrecho (anchura de haz de 1 a 2 grados):
1. Calcular previamente por software (Pathloss) el angulo de Azimut magnetico y Elevacion.
2. Conectar un multimetro digital en la escala de corriente continua (VDC) al puerto
   de prueba RSSI (BNC / Jack) de la ODU en la torre.
3. El voltaje es directamente proporcional a la potencia recibida en dBm (ej. 1V = -40 dBm).
4. Mover lentamente los tornillos de ajuste fino horizontal y vertical de la antena:
   - CUIDADO CON LOS LOBULOS SECUNDARIOS: Es comun enganchar un lobulo lateral de la antena
     y creer que esta alineada. Se debe seguir barriendo hasta encontrar el lobulo principal

## (pico maximo de voltaje RSSI).
