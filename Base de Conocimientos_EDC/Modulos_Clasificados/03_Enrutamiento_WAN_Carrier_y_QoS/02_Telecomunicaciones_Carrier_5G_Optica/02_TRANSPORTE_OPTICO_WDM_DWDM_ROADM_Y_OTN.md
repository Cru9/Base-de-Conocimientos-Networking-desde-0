# 02. TRANSPORTE OPTICO DE ALTA CAPACIDAD: WDM, DWDM, ROADM Y OTN (G.709)

> **TELECOMUNICACIONES AVANZADAS, REDES DE CARRIER E INFRAESTRUCTURA GLOBAL**


---



## 1. FUNDAMENTOS DE FISICA OPTICA PARA TELECOMUNICACIONES

La transmision por fibra optica es la columna vertebral de todas las telecomunicaciones
modernas. El envio de luz guiada se rige por la reflexion interna total en el nucleo
de silice (vidrio dopado con germanio) rodeado por una cubierta (cladding).

VENTANAS OPTICAS DE TRANSMISION:
1. Primera Ventana (850 nm):
   - Utilizada en cables Multimodo (OM3, OM4, OM5) con emisores VCSEL.
   - Alta atenuacion (~2.5 dB/km). Limitada a distancias de 100 a 500 metros en Datacenters.
2. Segunda Ventana (1310 nm - Banda O):
   - Atenuacion moderada (~0.35 dB/km). Dispersion cromatica CERO en fibras estandar.
   - Muy utilizada en enlaces metropolitanos de 10 km a 40 km (transceptores 100G-LR4 / 400G-DR4).
3. Tercera Ventana (1550 nm - Banda C / Conventional Band: 1530 nm a 1565 nm):
   - LA VENTANA REINA DE LAS TELECOMUNICACIONES. Minima atenuacion fisica del silicio (~0.18 a 0.20 dB/km).
   - Coincide con la longitud de onda amplificable por el elemento quimico Erbio (EDFA).
4. Cuarta Ventana (1625 nm - Banda L / Long Band: 1565 nm a 1625 nm):
   - Utilizada para expandir la capacidad cuando la Banda C se satura y para monitoreo OTDR en vivo.

TIPOS DE FIBRA OPTICA MONOMODO SEGUN ITU-T:
- ITU-T G.652.D: Fibra monomodo estandar con pico de agua eliminado (Low Water Peak).
  Es la fibra mas desplegada del planeta en redes terrestres metropolitanas y troncales.
- ITU-T G.654.E: Fibra de silice pura con area efectiva ultra-grande (130 um2) y atenuacion
  ultra-baja (~0.15 dB/km). Estandar obligatorio para enlaces terrestres y cables submarinos
  de 400G, 800G y 1.2 Terabits por longitud de onda.
- ITU-T G.655: Fibra con dispersion desplazada no nula (NZD-DSF). Disenada para mitigar
  el fenomeno de mezcla de cuatro ondas (FWM) en sistemas DWDM densos.
- ITU-T G.657.A1 / A2: Fibra insensible a dobleces bruscos (radio de curvatura de 7.5 mm).
  Estandar mandatorio para acometidas finales de FTTH dentro de edificios y hogares.



## 2. DEGRADACIONES FISICAS DE LA LUZ EN LA FIBRA

1. Atenuacion (Perdida de Potencia en dB):
   Causada por dispersion de Rayleigh (imperfecciones microscopicas del vidrio) y absorcion
   quimica de iones hidroxilo (OH-).
2. Dispersion Cromatica (CD - Chromatic Dispersion):
   Las diferentes frecuencias de luz viajan a velocidades ligeramente distintas dentro
   del vidrio. Con la distancia, el pulso digital se ensancha temporalmente hasta
   traslaparse con el bit vecino (Inter-Symbol Interference - ISI).
3. Dispersion por Modo de Polarizacion (PMD):
   La fibra optica real no es perfectamente cilindrica. Los dos modos ortogonales de
   polarizacion de la luz viajan a velocidades distintas (Retardo Diferencial de Grupo - DGD).
4. Efectos No Lineales (a altas potencias opticas):
   - FWM (Four-Wave Mixing): Intermodulacion entre canales DWDM vecinos que genera senales fantasma.
   - SPM (Self-Phase Modulation) y XPM (Cross-Phase Modulation): El indice de refraccion
     del vidrio cambia con la intensidad de la luz, deformando la fase de la onda.



## 3. MULTIPLEXACION POR DIVISION DE LONGITUD DE ONDA (WDM)

Permite transmitir decenas de canales de datos independientes y bidireccionales
a traves de un UNICO hilo de fibra optica, asignando a cada flujo un color (longitud de onda / lambda):

```text
           [ Switch 100G ] -> Lambda 1 (1550.12 nm) \
           [ Switch 100G ] -> Lambda 2 (1550.92 nm)  \  +--------------+               +--------------+
           [ Router 400G ] -> Lambda 3 (1551.72 nm) == | MULTIPLEXOR  | === FIBRA === | DESMULTIPLEX.|
           [ Video Carrier]-> Lambda 4 (1552.52 nm)  /  | MUX OPTICO  | (1 HILO)      | DEMUX OPTICO |
           [ San Storage ] -> Lambda 96 (1560.61 nm)/   +--------------+               +--------------+
```

COMPARATIVA: CWDM VS DWDM

| Caracteristica | CWDM (Coarse WDM) | DWDM (Dense WDM) |
| :--- | :--- | :--- |
| Estandar | ITU-T G.694.2 | ITU-T G.694.1 |
| Espaciado de Canales | 20 nm (Muy amplio) | 0.8 nm (100 GHz) / 0.4 nm (50 GHz) / Flex-Grid |
| Capacidad Maxima | Hasta 18 longitudes de onda | 96 canales (Banda C) / 192 canales (C+L) |
| Rango de Espectro | 1271 nm a 1611 nm | 1528 nm a 1568 nm (Banda C) |
| Control Termico (TEC) | NO requiere (Laseres no refrigerados) | OBLIGATORIO (Control de temperatura Peltier) |
| Amplificacion Optica | NO es amplificable en todo su espectro | AMPLIFICABLE al 100% con EDFA |
| Distancia Tipica | Hasta 40 - 70 km (Redes Metropolitanas) Miles de kilometros (Cables Submarinos/Troncal) |  |




## 4. TECNOLOGIA ROADM (RECONFIGURABLE OPTICAL ADD-DROP MULTIPLEXER)

En las redes opticas de primera generacion, para cambiar una ruta de una longitud
de onda entre dos ciudades, un tecnico debia viajar a la estacion repetidora y
reconectar manualmente cables de parcheo (Patch Cords).

Los ROADM modernos de arquitectura CDC (Colorless, Directionless, Contentionless):
- Emplean conmutadores de seleccion de longitud de onda (WSS - Wavelength Selective Switch)
  basados en microespejos de silicio (LCoS - Liquid Crystal on Silicon).
- Permiten que el software de control desvie, agregue (Add) o extraiga (Drop) cualquier
  longitud de onda hacia cualquier direccion geografica en milisegundos sin cortar el servicio.
- Flex-Grid (Rejilla Flexible): Divide el espectro en rebanadas configurables de 6.25 GHz
  o 12.5 GHz para alojar portadoras super-densas de 400G, 800G y 1.2 Terabits por segundo.



## 5. AMPLIFICADORES OPTICOS: EDFA Y RAMAN

Los amplificadores opticos amplifican la luz DIRECTAMENTE en el dominio fotonico,
sin necesidad de convertir la luz en senal electrica:

1. EDFA (Erbium-Doped Fiber Amplifier):
   - Una fibra dopada con iones de Erbio (Er3+) es estimulada con un laser de bombeo
     (Pump Laser) a 980 nm o 1480 nm.
   - Cuando las senales de la Banda C (1550 nm) atraviesan el Erbio, se produce emision
     estimulada, amplificando todos los 96 canales DWDM simultaneamente con una ganancia de 20 a 35 dB.
   - Introduce ruido de Emision Espontanea Amplificada (ASE).
   - Roles de EDFA: Booster (a la salida del MUX), ILA (In-Line Amplifier cada 80 km), Pre-Amp (al receptor).

2. Amplificacion Raman Distribuida:
   - Se inyecta un laser de bombeo de ultra-alta potencia (~1 Watt) en sentido contrario
     a la senal (contra-direccional) en la propia fibra del tendido.
   - Aprovecha el efecto de dispersion estimulada de Raman (SRS) del silicio para amplificar
     la senal a lo largo de los ultimos 20-30 kilometros antes de llegar a la estacion.
   - Proporciona una mejora de 6 a 10 dB en la relacion senal a ruido (OSNR) frente a un EDFA puro.



## 6. RED DE TRANSPORTE OPTICO (OTN - ITU-T G.709)

OTN es el "contenedor digital universal" que reemplazo a las antiguas redes SDH/SONET:

JERARQUIA DE ENCAPSULACION DIGITAL OTN:
1. OPUk (Optical Payload Unit):
   - Mapea el trafico cliente (Ethernet 10GE/100GE/400GE, Fiber Channel o video SDI).
2. ODUk (Optical Data Unit):
   - Anade cabeceras de gestion, monitoreo de rendimiento (BIP-8) y conmutacion en
     sub-longitud de onda (ODU0=1.25G, ODU2=10G, ODU4=100G, ODUflex).
3. OTUk (Optical Transport Unit):
   - Anade sincronizacion de trama y el bloque de correccion de errores hacia adelante (FEC).

FORWARD ERROR CORRECTION (FEC):
El avance matematico mas crucial de las telecomunicaciones opticas:
- Permite al receptor corregir millones de errores de bits provocados por la degradacion
  del enlace, sin necesidad de retransmitir los paquetes.
- Soft-Decision FEC (SD-FEC con 20-25% de overhead): Permite operar con tasas de error
  antes de correccion (Pre-FEC BER) de 10^-2 y entregar una salida perfecta libre de errores (Post-FEC BER < 10^-15).



## 7. CALCULO MATEMATICO DE ENLACE OPTICO (POWER BUDGET & OSNR)

Formulacion para diseno de vanos opticos:

A. Presupuesto de Perdidas de Potencia (Span Loss Budget):
   Perdida_Total (dB) = (Distancia_km * Atenuacion_fibra) + (N_empalmes * 0.05 dB) + (N_conectores * 0.25 dB) + Margen_Seguridad

   Ejemplo de Calculo para enlace de 80 km con fibra G.652.D en 1550 nm:
   - Atenuacion fibra: 80 km * 0.20 dB/km = 16.0 dB
   - 16 empalmes de fusion por tramo: 16 * 0.05 dB = 0.8 dB
   - 2 conectores de parcheo en ODF: 2 * 0.25 dB = 0.5 dB
   - Margen de envejecimiento y reparacion futura de cable: 3.0 dB
   - Perdida Total del Vano = 16.0 + 0.8 + 0.5 + 3.0 = 20.3 dB

B. Relacion Senal a Ruido Optica (OSNR - Optical Signal-to-Noise Ratio):
   - Mide la pureza de la senal respecto al piso de ruido ASE introducido por los amplificadores EDFA.
   - Se mide con un Analizador de Espectro Optico (OSA) en un ancho de banda de referencia de 0.1 nm.
   - Una transmision coherente 100G QPSK requiere un OSNR minimo de ~13 dB.

## - Una transmision coherente 400G 16-QAM requiere un OSNR minimo de ~22 dB.
