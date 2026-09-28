# 00. Índice General, Fundamentos, Historia y Proceso de Encapsulamiento

> **MODELO OSI (OPEN SYSTEMS INTERCONNECTION) — GUÍA MAESTRA PARA CERTIFICACIONES**  
> *Referencia técnica para ingenieros de redes y preparación para Cisco CCNA 200-301, CompTIA Network+ y Huawei HCIA.*

---

## 1. ¿Qué es el Modelo OSI y por qué fue creado?

El Modelo de Referencia OSI (*Open Systems Interconnection*) fue desarrollado en 1984 por la Organización Internacional de Normalización (**ISO** - Estándar ISO/IEC 7498).

### Antecedentes históricos:
- Cada fabricante de computadoras (**IBM con SNA**, **DEC con DECnet**, **Xerox**, **Apple con AppleTalk**) utilizaba arquitecturas de red cerradas y propietarias.
- Una computadora IBM no podía comunicarse con una computadora DEC sin costosos y complejos conversores de hardware.
- Si una empresa compraba equipos de una marca, quedaba atrapada (*Vendor Lock-in*).

### Objetivo de la creación de OSI:
- Crear un estándar abierto, universal e interoperable que permitiera a computadoras de cualquier fabricante, sistema operativo y arquitectura comunicarse sin fricción.
- Dividir la inmensa complejidad de las telecomunicaciones en **7 capas independientes y modulares** (arquitectura en capas).

---

## 2. El Concepto de Arquitectura en Capas y Modularidad

Cada capa tiene un propósito único y bien definido:

- **Principio de Abstracción**: Una capa solo se comunica con su capa directamente superior y su capa directamente inferior.
- **Principio de Independencia**: Si una tecnología cambia en una capa (por ejemplo, cambiar un cable de cobre por fibra óptica en la Capa 1, o cambiar Wi-Fi por 5G), las capas superiores (Capa 3 IP, Capa 4 TCP, Capa 7 Web) **NO** necesitan modificarse ni se enteran del cambio.

---

## 3. Las 7 Capas del Modelo OSI

| Nivel | Nombre de la Capa | Nombre en Inglés | PDU (Unidad de Datos) | Función Clave |
| :---: | :--- | :--- | :--- | :--- |
| **Capa 7** | **Aplicación** | Application | **Datos** (*Data*) | Servicios de red para aplicaciones de usuario final |
| **Capa 6** | **Presentación** | Presentation | **Datos** (*Data*) | Formato, codificación, cifrado y compresión |
| **Capa 5** | **Sesión** | Session | **Datos** (*Data*) | Establecimiento, sincronización y diálogo |
| **Capa 4** | **Transporte** | Transport | **Segmento** (TCP) / **Datagrama** (UDP) | Conexión extremo a extremo, confiabilidad y puertos |
| **Capa 3** | **Red** | Network | **Paquete** (*Packet*) | Direccionamiento lógico (IP) y enrutamiento global |
| **Capa 2** | **Enlace de Datos** | Data Link | **Trama** (*Frame*) | Direccionamiento físico (MAC), conmutación y CRC |
| **Capa 1** | **Física** | Physical | **Bits** (0s y 1s) | Señales eléctricas, lumínicas y medios físicos |

### 💡 Reglas Mnemotécnicas para Certificación
- **De Capa 7 a Capa 1 (Inglés):**
  > *"**A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing"*  
  *(Application, Presentation, Session, Transport, Network, Data Link, Physical)*
- **De Capa 1 a Capa 7 (Español):**
  > *"**P**or **F**avor **E**nseña **R**edes **T**odos **S**ábados **P**ara **A**probar"*  
  *(Física, Enlace, Red, Transporte, Sesión, Presentación, Aplicación)*

---

## 4. El Proceso de Encapsulamiento y Desencapsulamiento

Cuando una aplicación envía información a través de la red, los datos descienden por la pila OSI agregando encabezados (*Headers*) y al final un pie (*Trailer*).

### Diagrama Visual del Encapsulamiento (Emisor)

```text
Capa 7 [ Datos de Usuario (HTTP / Email) ]
   |
Capa 6 [ Encabezado L6 | Datos ] (Cifrado / Compresión)
   |
Capa 5 [ Encabezado L5 | L6 | Datos ] (ID de Sesión)
   |
Capa 4 [ Encabezado L4 (Puertos TCP/UDP) | Datos L5-L7 ]               ==> SEGMENTO
   |
Capa 3 [ Encabezado L3 (IP Origen / IP Destino) | Segmento L4 ]         ==> PAQUETE
   |
Capa 2 [ Encabezado L2 (MAC Origen / MAC Destino) | Paquete L3 | FCS ] ==> TRAMA
   |
Capa 1 [ 0 1 1 0 1 0 0 1 1 0 0 1 0 1 1 1 0 0 1 0 1 1 0 1 ]            ==> BITS (Pulsos)
```

### Proceso de Desencapsulamiento (Receptor)
1. El receptor recibe **bits** en Capa 1.
2. Valida la integridad de la **trama** y el FCS en Capa 2; retira el encabezado L2.
3. Valida la dirección **IP** en Capa 3; retira el encabezado L3.
4. Ensambla los **segmentos** TCP/UDP en Capa 4 y valida números de puerto.
5. Entrega los datos puros a las capas superiores hasta la **aplicación** en Capa 7.

---

## 5. Índice de Capítulos de esta Guía

- 📖 [**00. Fundamentos e Historia del Modelo OSI**](00_INDICE_Y_FUNDAMENTOS_MODELO_OSI.md)
- 🔌 [**01. Capa 1: Física (Physical Layer)**](01_CAPA_1_FISICA_PHYSICAL_LAYER.md)
- 🖧 [**02. Capa 2: Enlace de Datos (Data Link Layer)**](02_CAPA_2_ENLACE_DE_DATOS_DATA_LINK_LAYER.md)
- 🌐 [**03. Capa 3: Red (Network Layer)**](03_CAPA_3_RED_NETWORK_LAYER.md)
- 🚀 [**04. Capa 4: Transporte (Transport Layer)**](04_CAPA_4_TRANSPORTE_TRANSPORT_LAYER.md)
- 🔄 [**05. Capa 5: Sesión (Session Layer)**](05_CAPA_5_SESION_SESSION_LAYER.md)
- 🎨 [**06. Capa 6: Presentación (Presentation Layer)**](06_CAPA_6_PRESENTACION_PRESENTATION_LAYER.md)
- 💻 [**07. Capa 7: Aplicación (Application Layer)**](07_CAPA_7_APLICACION_APPLICATION_LAYER.md)
- ⚖️ [**08. Comparativa OSI vs TCP/IP y El Viaje de un Paquete**](08_COMPARATIVA_OSI_VS_TCPIP_Y_ENCAPSULAMIENTO.md)
- 🎯 [**09. Banco de 30 Preguntas y Simulador de Examen**](09_BANCO_DE_PREGUNTAS_Y_CASOS_TIPO_CERTIFICACION.md)
