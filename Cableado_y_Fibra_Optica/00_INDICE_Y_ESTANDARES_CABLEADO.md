# 00. INDICE GENERAL, ESTANDARES INTERNACIONALES Y SUBSISTEMAS

> **CABLEADO ESTRUCTURADO, FIBRA OPTICA Y CAPA FISICA**


---



## 1. LA IMPORTANCIA CRITICA DE LA CAPA FISICA (CAPA 1 DEL MODELO OSI)

Los estudios de la asociacion BICSI (Building Industry Consulting Service International)
demuestran de manera consistente que mas del 70% de las fallas intermitentes, lentitud
inexplicable y caidas de paquetes en redes corporativas tienen su origen en una
instalacion deficiente de la Capa Fisica:
- Conectores mal ponchados o sin el destrenzado adecuado.
- Radios de curvatura excesivos que quiebran fibras o estrangulan cables de cobre.
- Uso de cables de categorias inadecuadas o fuentes de alimentacion PoE saturadas.
- Tendidos paralelos a cables de alta tension que inducen interferencia electromagnetica (EMI).

Mientras que los switches y routers se renuevan cada 3 a 7 anos, el sistema de
cableado estructurado debe tener una vida util garantizada de 15 a 25 anos.



## 2. ESTANDARES Y NORMAS INTERNACIONALES DE DISENO


### a) ANSI/TIA-568 (Estandar Norteamericano de Cableado para Edificios Comerciales):

   - TIA-568.0-D: Cableado de Telecomunicaciones Generico para el Cliente.
   - TIA-568.1-D: Infraestructura de Cableado de Edificios Comerciales.
   - TIA-568.2-D: Estandar para Cableado y Componentes de Cobre de Par Trenzado Balanceado.
   - TIA-568.3-D: Componentes de Cableado de Fibra Optica.


### b) ISO/IEC 11801 (Estandar Global Internacional):

   - Equivalente internacional de la TIA, clasifica los cables de cobre por "Clases"
     (Clase D = Cat5e, Clase E = Cat6, Clase EA = Cat6A, Clase F = Cat7, Clase I/II = Cat8).


### c) ANSI/TIA-569-D (Rutas y Espacios de Telecomunicaciones):

   - Define las dimensiones, ductos, escalerillas y cuartos tecnicos (MDF / IDF).


### d) ANSI/TIA-606-C (Administracion y Etiquetado de Infraestructura):

   - Reglas estrictas para el etiquetado y codificacion de puertos, cables y racks.


### e) ANSI/TIA-607-C (Puesta a Tierra y Aterrizaje para Telecomunicaciones):

   - Malla de tierra, barras TGB / TMGB y proteccion contra descargas electrostaticas.



## 3. LOS 6 SUBSISTEMAS DEL CABLEADO ESTRUCTURADO

   [Acometida / Proveedor ISP]
                |
                v
```text
   +-----------------------------------------------------------------------+
   | 1. Facilidad de Entrada (Entrance Facility - EF)                      |
   +-----------------------------------------------------------------------+
                |
                v
   +-----------------------------------------------------------------------+
   | 2. Cuarto de Equipos Principal (Equipment Room - ER / MDF)            |
   |    (Switches Core, Servidores, Routers WAN)                           |
   +-----------------------------------------------------------------------+
                |
                | ===== [3. Cableado Vertebral / Backbone / Vertical] =====
                |       (Enlaces de Fibra Optica entre pisos)
                v
   +-----------------------------------------------------------------------+
   | 4. Cuarto de Telecomunicaciones (Telecommunications Room - TR / IDF)  |
   |    (Switches de Acceso PoE por piso o edificio)                       |
   +-----------------------------------------------------------------------+
                |
                | ----- [5. Cableado Horizontal (Cobre Cat6/6A max 90m)] ---
                v
   +-----------------------------------------------------------------------+
   | 6. Area de Trabajo (Work Area - WA)                                   |
   |    (Placa de pared Faceplate, Jack RJ-45, Patch Cord y Computadora)  |
   +-----------------------------------------------------------------------+

REGLA DE DISTANCIA DEL CABLEADO HORIZONTAL:
- Distancia maxima del enlace permanente (del Patch Panel al Jack): 90 metros.
- Longitud maxima de cables de parcheo (Patch Cords en ambos extremos): 10 metros.
- Distancia total del canal de cobre de punta a punta: ¡MAXIMO 100 METROS!
```


## 4. INDICE DE ARCHIVOS DE LA CARPETA CABLEADO_Y_FIBRA_OPTICA

[00_INDICE_Y_ESTANDARES_CABLEADO.md](./00_INDICE_Y_ESTANDARES_CABLEADO.md)
    - Principios fisicos, normas internacionales TIA/ISO y los 6 subsistemas de cableado.

[01_CABLEADO_DE_COBRE_UTP_STP_CATEGORIAS.md](./01_CABLEADO_DE_COBRE_UTP_STP_CATEGORIAS.md)
    - Par trenzado balanceado, tipos de apantallamiento (UTP, FTP, STP, SFTP), categorias
      Cat5e a Cat8, pinout T568A vs T568B, y estandares PoE (802.3af, 802.3at, 802.3bt 90W).

[02_FIBRA_OPTICA_SMF_MMF_Y_CONECTORES.md](./02_FIBRA_OPTICA_SMF_MMF_Y_CONECTORES.md)
    - Fisica optica y dispersion, Monomodo (OS1/OS2) vs Multimodo (OM1 a OM5),
      conectores (LC, SC, MPO/MTP) y tipos de pulido de conector (UPC Azul vs APC Verde).

[03_TRANSCEPTORES_SFP_Y_PRESUPUESTO_OPTICO.md](./03_TRANSCEPTORES_SFP_Y_PRESUPUESTO_OPTICO.md)
    - Modulos SFP, SFP+, SFP28, QSFP28, QSFP-DD, calculo del presupuesto de potencia

optica (Power Budget en dBm), atenuacion por km y lectura de graficas OTDR.
