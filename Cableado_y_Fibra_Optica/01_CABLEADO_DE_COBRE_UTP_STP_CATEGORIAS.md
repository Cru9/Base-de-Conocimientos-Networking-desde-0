# 01. CABLEADO DE COBRE: PAR TRENZADO, APANTALLAMIENTO, CATEGORIAS Y POE

> **CABLEADO ESTRUCTURADO, FIBRA OPTICA Y CAPA FISICA**


---



## 1. PRINCIPIO FISICO DEL PAR TRENZADO Y SENALIZACION DIFERENCIAL

¿Por que se trenzan los cables de cobre?
El cable de red utiliza "Senalizacion Diferencial Balanceada":
- Por un conductor del par se envia el voltaje positivo (+V).
- Por el otro conductor del par se envia exactamente el voltaje negativo inverso (-V).
- En el receptor, el chip calcula la diferencia: (+V) - (-V) = 2V.

Cancelacion de Ruido Electromagnetico (EMI):
- Si una fuente de ruido externa (un motor electrico o lampara fluorescente)
  golpea el cable, induce exactamente la misma cantidad de ruido (+Ruido) en ambos hilos.
- El receptor calcula: (+V + Ruido) - (-V + Ruido) = 2V.
- ¡EL RUIDO SE CANCELA MATEMATICAMENTE A CERO!

Paso de Trenzado Diferenciado:
- Para evitar que un par interfiera con el par vecino dentro del mismo forro (Diafonia
  o Crosstalk: NEXT / FEXT), cada uno de los 4 pares tiene un numero DIFERENTE de
  vueltas por pulgada.



## 2. NOMENCLATURA DE APANTALLAMIENTO (ESTANDAR ISO/IEC 11801)

Formato estandar internacional: [XX] / [Y] TP
- XX : Blindaje exterior que envuelve a los 4 pares juntos.
- Y  : Blindaje individual alrededor de CADA par.
- TP : Twisted Pair (Par Trenzado).
- Simbolos: U = Unshielded (Sin blindaje), F = Foil (Lamina de aluminio), S = Braided Shield (Malla metalica tejida).


| Codificacion Oficial | Nombre Comun | Descripcion y Aplicacion |
| :--- | :--- | :--- |
| U/UTP | UTP Estandar | Sin ningun blindaje. Economico y flexible. |

                                         Ideal para oficinas comerciales sin interferencia.
F/UTP                   FTP              Lamina de aluminio global cubriendo los 4 pares.
                                         Protege contra radiofrecuencia moderada.
U/FTP                   STP Individual   Cada par envuelto en su propia lamina de aluminio.
                                         Excelente eliminacion de diafonia interna (NEXT).
S/FTP                   SFTP Industrial  Malla de cobre tejida exterior + laminas en cada par.

## Maxima proteccion para fabricas y plantas industriales.

REGLA CRITICA: Todo cable apantallado (FTP/STP) DEBE estar correctamente conectado
a la tierra de telecomunicaciones en el Patch Panel. Un blindaje sin conexion a tierra
actua como una antena que capta y amplifica el ruido electromagnetico.



## 3. MATRIZ DE CATEGORIAS DE CABLE DE COBRE


| Categoria | Frecuencia | Velocidad Maxima | Distancia Max. | Calibre | Uso Principal |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Cat 5e | 100 MHz | 1 Gbps (1000Base-T) 100 metros | 24 AWG | Obsoleto para obra nueva |  |
| Cat 6 | 250 MHz | 1 Gbps (1000Base-T) 100 metros | 23 AWG | Estaciones de trabajo |  |
| 10 Gbps (10GBase-T) 55 metros | (Oficinas convencionales) |  |  |  |  |
| Cat 6A | 500 MHz | 10 Gbps (10GBase-T) 100 metros | 23 AWG | ESTANDAR RECOMENDADO |  |

                                                                       (Wi-Fi 6/7, Data Centers)
Cat 7       600 MHz      10 Gbps             100 metros      22 AWG    Entornos industriales S/FTP
Cat 7A      1000 MHz     10 Gbps             100 metros      22 AWG    Sistemas de audio/video
Cat 8       2000 MHz     25G / 40 Gbps       30 metros       22 AWG    Interconexion ToR en

| (40GBase-T) | Centros de Datos modernos |
| :--- | :--- |
| ¿Por que Cat6A sobre Cat6? |  |
| Cat6A mitiga totalmente el "Alien Crosstalk" (ANEXT - ruido inducido entre cables vecinos |  |
| amarrados en la misma charola), garantizando 10 Gbps completos a 100 metros. |  |




## 4. NORMAS DE PONCHADO: T568A vs T568B

En ambos estandares los pares Azul y Marron permanecen en las mismas posiciones;
unicamente se intercambian los pares Verde y Naranja.


| Pin | Funcion Ethernet | Norma T568A | Norma T568B (Mas Usada) |
| :--- | :--- | :--- | :--- |
| Pin 1 | Tx+ / Rx+ (Datos) | Blanco - Verde | Blanco - Naranja |
| Pin 2 | Tx- / Rx- (Datos) | Verde | Naranja |
| Pin 3 | Rx+ / Tx+ (Datos) | Blanco - Naranja | Blanco - Verde |
| Pin 4 | PoE / Bidireccional | Azul | Azul |
| Pin 5 | PoE / Bidireccional | Blanco - Azul | Blanco - Azul |
| Pin 6 | Rx- / Tx- (Datos) | Naranja | Verde |
| Pin 7 | PoE / Bidireccional | Blanco - Marron | Blanco - Marron |
| Pin 8 | PoE / Bidireccional | Marron | Marron |


- Cable Directo (Straight-Through): Mismo estandar en ambos extremos (ej. T568B a T568B).
  Conecta dispositivos de distinta capa (PC a Switch, Switch a Router).
- Cable Cruzado (Crossover): Un extremo T568A y el otro T568B.
  Historicamente conectaba dispositivos iguales (Switch a Switch, PC a PC).
  En la actualidad, todos los equipos modernos cuentan con Auto-MDIX por hardware,
  el cual detecta y cruza los pares electronicamente de forma automatica.



## 5. ESTANDARES POWER OVER ETHERNET (PoE - ENERGIA SOBRE ETHERNET)

Permite alimentar telefonos IP, camaras de videovigilancia y puntos de acceso Wi-Fi
directamente a traves del cable de cobre sin enchufes electricos adicionales.


| Estandar | Nombre Comercial | Pares Usados | Potencia en Switch (PSE) | Potencia en Equipo (PD) |
| :--- | :--- | :--- | :--- | :--- |
| 802.3af | PoE Clasico | 2 pares | 15.4 Watts | 12.95 Watts (Telefonos IP) |
| 802.3at | PoE+ | 2 pares | 30.0 Watts | 25.50 Watts (Camaras PTZ) |
| 802.3bt | PoE++ (Tipo 3) | 4 pares | 60.0 Watts | 51.00 Watts (APs Wi-Fi 6) |
| 802.3bt | PoE++ (Tipo 4) | 4 pares | 90.0 a 100.0 Watts | 71.30 Watts (Iluminacion LED / |


## Pantallas Digitales)

ADVERTENCIA TERMICA DE INSTALACION:
El uso masivo de PoE de 90W en manojos apretados de mas de 48 cables genera calor
interno que degrada la atenuacion del cobre. Se debe utilizar cable Cat6A con forro

de disipacion termica y no superar manojos de 24 cables en charolas.
