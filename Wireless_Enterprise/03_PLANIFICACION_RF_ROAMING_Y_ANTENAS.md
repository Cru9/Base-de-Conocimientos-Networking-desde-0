# 03. PLANIFICACION DE RADIOFRECUENCIA (RF), ANTENAS Y ROAMING RAPIDO (802.11k/v/r)

> **REDES INALAMBRICAS EMPRESARIALES (WIRELESS ENTERPRISE NETWORKING)**


---



## 1. METRICAS FUNDAMENTALES DE RADIOFRECUENCIA (RF)


### a) Potencia y la Escala Logaritmica (dBm y mW):

   - La potencia de transmision de radio no se mide linealmente en miliwatts (mW)
     porque la atenuacion en el aire es exponencial.
   - Formula: dBm = 10 * log10(Potencia en mW)
   - Regla de los 3s y los 10s:
     * +3 dB = Se duplica la potencia (ej. 20 dBm = 100 mW -> 23 dBm = 200 mW).
     * -3 dB = Se reduce la potencia a la mitad.
     * +10 dB = Se multiplica por 10 la potencia (ej. 10 dBm = 10 mW -> 20 dBm = 100 mW).


### b) RSSI (Received Signal Strength Indicator):

   - Nivel de intensidad con el que el cliente recibe la senal del AP (en -dBm):
     * -30 a -50 dBm : Excelente senal (cliente justo debajo del punto de acceso).
     * -65 a -67 dBm : UMBRAL DE DISENO EMPRESARIAL (Requerido para voz y video).
     * -75 dBm       : Senal regular; reduccion de tasas de modulacion (MCS) y lentitud.
     * -85 dBm       : Desconexion inminente; perdida severa de paquetes.


### c) Piso de Ruido (Noise Floor) y SNR (Signal-to-Noise Ratio):

   - Ruido de fondo en oficinas: tipicamente entre -90 dBm y -95 dBm.
   - SNR = Nivel de Senal (RSSI) - Piso de Ruido.
   - Ejemplo: Senal = -65 dBm, Ruido = -92 dBm -> SNR = 27 dB.
   - Regla: Para alcanzar las tasas maximas de modulacion Wi-Fi se requiere un SNR > 25 dB.



## 2. PLANIFICACION DE CANALES (EL DILEMA DE 2.4 GHz vs 5 GHz)


### a) Banda de 2.4 GHz (Propagacion Lejana, Espectro Estrecho):

   - Posee 11 canales en America, pero cada canal tiene 20 MHz de ancho y sus centros
     estan separados por solo 5 MHz.
   - ¡SOLO EXISTEN 3 CANALES QUE NO SE SUPERPONEN: CANAL 1, CANAL 6 Y CANAL 11!
   - ERROR CRITICO COMUN: Configurar canales como el 2, 3, 4 o 9 provoca
     Interferencia de Canal Adyacente (ACI - Adjacent Channel Interference), la cual
     actua como ruido electromagnetico destructivo que corrompe las tramas.


### b) Banda de 5 GHz (Alta Capacidad y Densidad):

   - Ofrece mas de 25 canales no superpuestos de 20 MHz.
   - Canales UNII-1 (36 al 48): Uso en interiores, baja potencia, sin restricciones.
   - Canales UNII-2 (52 al 144) - REGLA DFS (Dynamic Frequency Selection):
     * Estos canales comparten frecuencias con radares meteorologicos y militares.
     * Si un AP detecta un pulso de radar en su canal DFS, DEBE silenciarse de inmediato
       y cambiar de canal en segundos para no interferir con la aviacion o el ejercito.
   - Ancho de Canales y Agrupamiento (Channel Bonding):
     * Se pueden unir canales para lograr 40 MHz, 80 MHz o 160 MHz.
     * ¡REGLA DE EXPERTO EN EMPRESAS!: En entornos corporativos de alta densidad,
       se debe disenar con canales de 20 MHz o maximo 40 MHz. Utilizar canales de 80
       o 160 MHz agota el espectro y genera Interferencia Co-Canal (CCI).



## 3. TIPOS DE ANTENAS Y PATRONES DE RADIACION


### a) Antenas Omnidireccionales:

   - Patron de radiacion toroidal (en forma de dona de 360 grados en el plano horizontal).
   - Uso: Puntos de acceso montados en el techo en oficinas estandar, pasillos y salas
     de juntas con alturas convencionales (2.5 a 4 metros).


### b) Antenas Direccionales (Patch / Panel / Sectoriales):

   - Concentran la energia de radiofrecuencia en un cono enfocado y estrecho (ej. apertura de 30 o 60 grados).
   - Uso: Naves industriales, almacenes con techos altos (8 a 15 metros), estadios
     y enlaces inalambricos punto a punto de larga distancia entre edificios.



## 4. ROAMING TRANSPARENTE: ESTANDARES IEEE 802.11k, 802.11v Y 802.11r

En las redes Wi-Fi, la decision de desconectarse de un AP y conectarse a otro es
tomada EXCLUSIVAMENTE por el dispositivo cliente (laptop o telefono), no por el AP.

Sin estandares de asistencia, el roaming tradicional tardaba hasta 1,500 ms (1.5 segundos),
cortando llamadas de Zoom o Teams y congelando aplicaciones web.


### a) IEEE 802.11k (Neighbor Reports - Reporte de Vecinos):

   - El AP le entrega al cliente una lista optimizada de los APs vecinos cercanos
     y sus canales.
   - El cliente ya no necesita escanear los 40 canales del espectro; salta directamente
     al canal del AP vecino mas cercano, ahorrando bateria y tiempo de escaneo.


### b) IEEE 802.11v (BSS Transition Management):

   - La red (WLC) monitorea la carga de los APs y le "sugiere" formalmente al cliente
     que se mueva a un AP menos congestionado o lo orienta hacia la banda de 5 GHz
     (Band Steering asistido).


### c) IEEE 802.11r (Fast BSS Transition - FT):

   - El estandar mas critico para telefonia y movilidad.
   - En una red empresarial 802.1X normal, cambiar de AP requiere negociar de nuevo
     el tunel EAP completo contra el servidor RADIUS (decenas de paquetes y > 1 segundo).
   - Con 802.11r, la controladora WLC pre-calcula y pre-distribuye las claves criptograficas
     (PMK-R1) a los APs vecinos antes de que el usuario camine hacia ellos.
   - TIEMPO DE TRANSICION CON 802.11r: ¡Menos de 20 milisegundos!
   - Cero paquetes perdidos: La voz y el video no sufren ni una sola interrupcion

mientras el usuario camina por todo el edificio.
