# 02. FIBRA OPTICA: MONOMODO (SMF) vs MULTIMODO (MMF), CONECTORES Y PULIDOS

> **CABLEADO ESTRUCTURADO, FIBRA OPTICA Y CAPA FISICA**


---



## 1. ANATOMIA Y PRINCIPIO FISICO DE LA FIBRA OPTICA

La fibra optica es una guia de ondas de vidrio de silice ultrapuro que transporta
pulsos de luz (fotones).

Estructura Concentrica:
1. Nucleo (Core): Zona central de silice por donde viaja la senal de luz.
2. Revestimiento (Cladding): Capa de silice que rodea el nucleo con un indice de
   refraccion menor. Diametro estandar universal: 125 micrometros (µm).
3. Recubrimiento Primario (Buffer / Coating): Capa de acrilato de 250 o 900 µm
   que aporta proteccion mecanica contra humedad y raspaduras.

Principio de Reflexion Interna Total (Ley de Snell):
- Como el nucleo tiene un indice de refraccion mayor que el cladding, si la luz
  golpea la pared con un angulo superior al angulo critico, el 100% de la luz rebota
  hacia adentro sin escapar al exterior.



## 2. FIBRA MONOMODO (SMF - SINGLE-MODE FIBER)


### a) Caracteristicas Fisicas:

   - Diametro del nucleo diminuto: 9 µm (del grosor de un globulo rojo o cabello fino).
   - Solo permite el paso de un UNICO rayo de luz (modo fundamental) que viaja en linea recta.
   - CERO Dispersion Modal (no hay rebotes en angulos dispersos).
   - Fuentes de Emision: Laseres semiconductores de alta potencia (Fabry-Perot / DFB).
   - Longitudes de Onda: 1310 nm y 1550 nm (en la ventana de absorcion minima del silice).
   - Color estandar del forro exterior: Amarillo brillante.


### b) Categorias Oficiales:

   - OS1: Disenada para interiores (campus corto, atenuacion ~1.0 dB/km a 1310 nm).
   - OS2: Fibra con pico de agua cero (Low Water Peak) para exteriores y largas
     distancias (atenuacion ultra-baja de 0.4 dB/km a 1310 nm y 0.25 dB/km a 1550 nm).
   - Alcance: 10 km, 40 km y hasta mas de 80 km sin necesidad de repetidores.



## 3. FIBRA MULTIMODO (MMF - MULTI-MODE FIBER)


### a) Caracteristicas Fisicas:

   - Diametro del nucleo amplio: 50 µm o 62.5 µm.
   - La luz rebota en cientos de angulos (modos de propagacion) simultaneamente.
   - Fenomeno de Dispersion Modal: Los rayos que rebotan en angulos agudos recorren
     una distancia mayor y llegan mas tarde que los rayos centrales.
     Esto distorsiona los pulsos de datos a altas velocidades y limita la distancia maxima.
   - Fuentes de Emision: Laseres economicos VCSEL (Vertical-Cavity Surface-Emitting Laser).
   - Longitudes de Onda: 850 nm y 1300 nm.


b) Categorias de Fibra Multimodo:


| Estandar | Nucleo | Color de Forro | 10 Gbps | 40G / 100 Gbps | Tecnologia Laser |
| :--- | :--- | :--- | :--- | :--- | :--- |
| OM1 | 62.5 µm | Naranja | 33 metros | No soportado | LED (Obsoleto) |
| OM2 | 50 µm | Naranja | 82 metros | No soportado | LED |
| OM3 | 50 µm | Aqua (Turquesa) | 300 metros | 100 metros | Laser VCSEL 850nm |
| OM4 | 50 µm | Violeta Erika/Aqua 400 metros | 150 metros | VCSEL Optimizado |  |
| OM5 | 50 µm | Verde Lima | 400 metros | 150 metros | SWDM (4 Long. Onda) |




## 4. TIPOS DE CONECTORES DE FIBRA OPTICA


### a) Conector LC (Lucent Connector) - EL ESTANDAR CORPORATIVO:

   - Conector miniatura (SFF - Small Form Factor) con ferula de ceramica de 1.25 mm.
   - Mecanismo de fijacion por trinquete (similar a un RJ-45).
   - Es el conector indiscutible en conmutadores modernos, transceptores SFP/SFP+
     y bandejas de distribucion optica (ODF).


### b) Conector SC (Subscriber Connector):

   - Conector cuadrado con sistema "Push-Pull" y ferula de 2.5 mm.
   - Muy utilizado historicamente en telecomunicaciones y acometidas de fibra.


### c) Conector MPO / MTP (Multi-fiber Push-On):

   - Conector multifibra de alta densidad que alberga 8, 12, 16 o 24 hilos de fibra
     en una sola ferula rectangular.
   - Obligatorio en centros de datos modernos para transceptores QSFP de 40G, 100G y 400G
     (ej. conexion QSFP-SR4 utilizando 4 fibras para transmitir y 4 fibras para recibir).



## 5. TIPOS DE PULIDO DE FERULA: UPC (AZUL) vs APC (VERDE)

La superficie de la punta de la ferula de ceramica donde se unen dos fibras debe
pulirse microscopicamente para minimizar el reflejo de retorno (Optical Return Loss - ORL).


| Caracteristica | UPC (Ultra Physical Contact) | APC (Angled Physical Contact) |
| :--- | :--- | :--- |
| Color del Conector | AZUL | VERDE |
| Forma del Pulido | Domo ligeramente redondeado | PULIDO CON ANGULO DE 8 GRADOS |
| Perdida de Retorno (ORL) -50 dB | -60 dB (Minima reflexion) |  |
| Hacia donde rebota la luz Rebota de regreso al emisor | Rebota en angulo hacia el cladding |  |
| Uso Principal | Redes LAN empresariales y datos | Redes GPON / FTTH, Video RF y DWDM |


¡ADVERTENCIA CRITICA DE CAMPO!:
NUNCA conectes un conector VERDE (APC) en un puerto AZUL (UPC).
El choque del plano inclinado de 8° contra la punta plana rayara permanentemente

ambas caras de vidrio, arruinando la fibra y provocando una caida total de senal.
