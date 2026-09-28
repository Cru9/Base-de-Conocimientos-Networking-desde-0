# 03. TRANSCEPTORES OPTICOS (SFP/QSFP), PRESUPUESTO DE POTENCIA Y OTDR

> **CABLEADO ESTRUCTURADO, FIBRA OPTICA Y CAPA FISICA**


---



## 1. FACTORES DE FORMA DE TRANSCEPTORES EN CONMUTADORES MODERNOS

Un transceptor optico (Transceiver) es un modulo intercambiable en caliente (Hot-Swappable)
que convierte las senales electricas del switch en pulsos de luz optica:


| Formato | Velocidad Maxima | Canales de Datos | Conector Tipico |
| :--- | :--- | :--- | :--- |
| SFP | 1 Gbps (1.25 Gbps) | 1 canal (1x 1G) | LC Duplex |
| SFP+ | 10 Gbps | 1 canal (1x 10G) | LC Duplex |
| SFP28 | 25 Gbps | 1 canal (1x 25G) | LC Duplex |
| QSFP+ | 40 Gbps | 4 canales (4x 10G) | MPO/MTP-12 o LC Duplex |
| QSFP28 | 100 Gbps | 4 canales (4x 25G) | MPO/MTP-12 o LC Duplex |
| QSFP-DD / OSFP 400G / 800 Gbps | 8 canales (8x 50G PAM4) MPO-16 / MPO-24 |  |  |


Cables de Conexion Directa para Centro de Datos (ToR a Servidor):

### a) DAC (Direct Attach Copper / Twinax):

   - Cable de cobre pasivo con conectores SFP+ o QSFP28 integrados en fábrica.
   - Longitud: 1 a 5 metros.
   - Ventajas: Latencia de nanosegundos, costo 80% menor que opticos y consumo
     electrico casi nulo (< 0.5 Watts por puerto).

### b) AOC (Active Optical Cable):

   - Fibra optica integrada con conectores sellados. Para distancias de 5 a 30 metros.



## 2. CODIGOS DE ALCANCE OPTICO (-SR, -LR, -ER, -ZR, BiDi)


| Sufijo Optico | Nombre | Tipo de Fibra | Longitud de Onda | Distancia Tipica |
| :--- | :--- | :--- | :--- | :--- |
| -SR / -SX | Short Reach | Multimodo MMF | 850 nm | Hasta 300 - 400 m |
| -LR / -LX | Long Reach | Monomodo SMF | 1310 nm | Hasta 10 km |
| -ER | Extended Reach | Monomodo SMF | 1550 nm | Hasta 40 km |
| -ZR | Zealous Reach | Monomodo SMF | 1550 nm | Hasta 80 km |
| -BiDi | Bidirectional | Monomodo SMF | 1310/1490 nm | Hasta 10 - 40 km |
| (1 solo hilo) | o 1270/1330 nm |  |  |  |

¿Que es la tecnologia BiDi (Bidireccional)?
- Tradicionalmente, la fibra optica requiere 2 hilos (un hilo para Tx y un hilo para Rx).
- Los transceptores BiDi incorporan un prisma WDM interno que transmite en una longitud
  de onda (ej. 1310 nm) y recibe en otra (ej. 1490 nm) sobre UN SOLO HILO de fibra.
- ¡Ahorra el 50% de los costos de renta de fibra oscura entre sedes!



## 3. TELEMETRIA DDM / DOM (DIGITAL DIAGNOSTIC MONITORING)

Permite consultar desde la linea de comandos del switch el estado fisico del laser:
- Comando Cisco: `show interfaces GigabitEthernet0/0/1 transceiver detail`
- Comando Huawei: `display transceiver verbose interface GigabitEthernet0/0/1`

Variables Monitoreadas:
- Temperatura del modulo (°C).
- Voltaje de alimentacion (V).
- Corriente de polarizacion del laser (Laser Bias Current en mA).
- Potencia Optica de Transmision (Tx Power en dBm).
- Potencia Optica de Recepcion (Rx Power en dBm).



## 4. CALCULO DEL PRESUPUESTO DE POTENCIA OPTICA (OPTICAL POWER BUDGET)

Antes de conectar un enlace de fibra de varios kilometros, el ingeniero debe calcular
matematicamente si la senal llegara con la intensidad suficiente o si quemara el receptor.

PASO 1: Obtener las especificaciones del transceptor (Datasheet):
- Potencia de Transmision Minima (Tx Min) : -9 dBm
- Sensibilidad del Receptor (Rx Min)      : -20 dBm (Por debajo de esto hay perdida de paquetes)
- Potencia de Saturacion (Rx Max)         : -3 dBm (Por encima de esto se dana el fotodiodo)

PASO 2: Calcular el Presupuesto de Perdida Disponible (Loss Budget):
  Presupuesto Disponible = Tx Min - Rx Min
  Presupuesto Disponible = -9 dBm - (-20 dBm) = 11.0 dB

PASO 3: Calcular la Atenuacion Total del Enlace Fisico:
- Distancia del enlace: 15 km de fibra monomodo a 1310 nm (atenuacion tipica: 0.35 dB/km).
  Perdida por Fibra = 15 km * 0.35 dB/km = 5.25 dB
- Conectores LC (2 pares en Patch Panels, 0.5 dB por par):
  Perdida por Conectores = 2 * 0.5 dB = 1.00 dB
- Empalmes por fusion (4 empalmes en el trayecto, 0.1 dB por fusion):
  Perdida por Empalmes = 4 * 0.1 dB = 0.40 dB
- Margen de Seguridad de Diseno (envejecimiento y futuras reparaciones): 3.00 dB

Atenuacion Total Estimada = 5.25 + 1.00 + 0.40 + 3.00 = 9.65 dB


#### 📌 CONCLUSION:

- Como la Atenuacion Total (9.65 dB) es MENOR que el Presupuesto (11.0 dB):
  ¡EL ENLACE ES 100% VIABLE Y OPERARA DE FORMA PERFECTA Y CONFIABLE!



## 5. INTERPRETACION DE GRAFICAS OTDR (REFLECTOMETRIA OPTICA)

El reflectometro optico en el dominio del tiempo (OTDR) es el instrumento de diagnostico
forense definitivo para fibra optica. Inyecta pulsos de luz laser de alta energia
y grafica la potencia de retorno en decibeles (Eje Y) contra la distancia en metros (Eje X).

  Potencia (dB)
    ^
    |   [Pico 1: Zona Muerta / Conector Inicial]
    |    /\
    |   /  \
    |  /    \____________________  (Pendiente de Atenuacion Rayleigh dB/km)
    |                            \
    |                             \____ [Escalon hacia abajo: Empalme por Fusion (0.05 dB)]
    |                                  \
    |                                   \      [Pico 2: Conector Intermedio]
    |                                    \      /\
    |                                     \____/  \_______
    |                                                     \      [Pico Final]
    |                                                      \      /\
    |                                                       \____/  \____ (Piso de Ruido)
```text
    +------------------------------------------------------------------------> Distancia (km)
```

EVENTOS CLAVE EN LA GRAFICA OTDR:
1. Picos Reflectivos Hacia Arriba (Reflexion de Fresnel):
   - Producidos por un cambio en el indice de refraccion (conector desalineado,
     cara de fibra sucia o rotura completa de la fibra).
2. Caidas No Reflectivas (Escalones Hacia Abajo):
   - Producidos por atenuacion pura sin rebote (empalmes por fusion o curvaturas excesivas / macrobending).
3. Pendiente Descendente Continua:

## - Dispersion de Rayleigh natural del vidrio. Una pendiente abrupta indica fibra defectuosa.
