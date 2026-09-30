# 🗂️ Módulos Clasificados y Mejorados del Repositorio
## Base de Conocimientos EDC

> **ESTRUCTURA DE CLASIFICACIÓN ARQUITECTÓNICA DE LOS 22 PILARES ORIGINALES**  
> **Ubicación:** `Base de Conocimientos_EDC/Modulos_Clasificados/README.md`  
> **Criterio de Mejora:** Corrección de tablas desalineadas, corrección de typos (`redudancia` -> `redundancia`), clasificación jerárquica limpia e indexación cruzada.

---

## 🏛️ Mapa Jerárquico de Módulos Clasificados

A diferencia de la carpeta raíz original donde los 25 módulos se encontraban dispersos de forma plana, esta sección los organiza en **6 Pilares de Especialidad de Ingeniería**, conservando el 100% de los archivos originales debidamente saneados y corregidos:

```text
Modulos_Clasificados/
│
├── 01_Fundamentos_Fisicos_y_OSI/
│   ├── 01_Modelo_OSI/                            <- Origen: OSI/ (Tablas L1 saneadas)
│   └── 02_Cableado_y_Fibra_Optica/               <- Origen: Cableado_y_Fibra_Optica/
│
├── 02_Conmutacion_MultiVendor_y_Wireless/
│   ├── 01_Switching_CLI_MultiVendor/             <- Origen: SW/ (Cisco, Huawei, Aruba, HP, 3Com, TP-Link; typo 'redundancia' corregido)
│   ├── 02_Troubleshooting_Switches/              <- Origen: Troubleshooting/
│   └── 03_Wireless_Enterprise/                   <- Origen: Wireless_Enterprise/
│
├── 03_Enrutamiento_WAN_Carrier_y_QoS/
│   ├── 01_Routing_Avanzado_y_WAN/                <- Origen: Routing_y_WAN/ (Tablas LSA OSPF corregidas)
│   ├── 02_Telecomunicaciones_Carrier_5G_Optica/  <- Origen: Telecomunicaciones_Avanzadas_Carrier/
│   └── 03_QoS_y_Traffic_Shaping/                 <- Origen: QoS_Traffic_Shaping/
│
├── 04_Ciberseguridad_Firewalls_y_Acceso/
│   ├── 01_Ciberseguridad_en_Capas_OSI/           <- Origen: Ciberseguridad_OSI/ (Matriz de amenazas reconstruida)
│   ├── 02_Control_de_Acceso_AAA_8021X/           <- Origen: AAA_y_Control_de_Acceso/
│   ├── 03_Firewalls_y_VPN/                       <- Origen: Firewalls_y_VPN/
│   ├── 04_Firewalls_NGFW_Lideres/                <- Origen: Firewalls_NGFW_Lideres/
│   └── 05_Redes_Industriales_OT/                 <- Origen: Redes_Industriales_OT/
│
├── 05_DataCenter_Cloud_y_Whitebox/
│   ├── 01_DataCenter_Spine_Leaf_VXLAN/           <- Origen: DataCenter/
│   ├── 02_Cloud_Networking_MultiCloud/           <- Origen: Cloud_Networking/
│   └── 03_Sistemas_Operativos_Abiertos_Whitebox/ <- Origen: Sistemas_Operativos_Abiertos_Whitebox/
│
└── 06_Operaciones_DDI_Telefonia_Herramientas_y_Labs/
    ├── 01_Servicios_DDI_y_Gestion/               <- Origen: Servicios_DDI_y_Gestion/
    ├── 02_Telefonia_VoIP_Avaya_y_Asterisk/       <- Origen: Telefonia/
    ├── 03_Analisis_Wireshark/                    <- Origen: Wireshark_Analysis/
    ├── 04_Metodologia_Ingenieria_Plantillas/     <- Origen: Metodologia_Ingenieria_y_Plantillas/
    ├── 05_Banco_200_Laboratorios_Practicos/      <- Origen: Ejemplos/ (Los 200 labs prácticos)
    ├── 06_Suite_Herramientas_Scripts/            <- Origen: Tools/, Tools_BC/, Tools_BC_Windows/
    └── 07_Wiki_Pages_Originales/                 <- Origen: wiki_pages/
```

---

## 📋 Resumen de Mejoras Aplicadas en los Módulos Clasificados

1. **Corrección de Tablas Markdown Rotas:**
   - [`01_Fundamentos_Fisicos_y_OSI/01_Modelo_OSI/01_CAPA_1_FISICA_PHYSICAL_LAYER.md`](./01_Fundamentos_Fisicos_y_OSI/01_Modelo_OSI/01_CAPA_1_FISICA_PHYSICAL_LAYER.md): Se reparó la tabla de categorías UTP eliminando el salto de fila roto en Cat 6.
   - [`03_Enrutamiento_WAN_Carrier_y_QoS/01_Routing_Avanzado_y_WAN/01_OSPF_MULTI_AREA_AVANZADO.md`](./03_Enrutamiento_WAN_Carrier_y_QoS/01_Routing_Avanzado_y_WAN/01_OSPF_MULTI_AREA_AVANZADO.md): Se reconstruyeron las columnas y delimitadores de la tabla de LSAs Tipo 1 a 7.
   - [`04_Ciberseguridad_Firewalls_y_Acceso/01_Ciberseguridad_en_Capas_OSI/08_MATRIZ_INTEGRAL_DE_AMENAZAS_Y_ARQUITECTURA_ZERO_TRUST.md`](./04_Ciberseguridad_Firewalls_y_Acceso/01_Ciberseguridad_en_Capas_OSI/08_MATRIZ_INTEGRAL_DE_AMENAZAS_Y_ARQUITECTURA_ZERO_TRUST.md): Se reconstruyó por completo la matriz de amenazas desde Capa 6 hasta Capa 1 en una tabla Markdown estándar.
2. **Corrección de Typos Sistemáticos de Nombre y Contenido:**
   - Se renombraron los 6 archivos de conmutación de `05_redudancia_y_agregacion_...` a **`05_redundancia_y_agregacion_...`** en las carpetas de Cisco, Huawei, Aruba, HP, 3Com y TP-Link.
   - Se sustituyeron todas las ocurrencias internas de la palabra `redudancia` por **`redundancia`** en todos los índices y manuales.
3. **Organización Lógica:** Cada subcarpeta mantiene sus archivos y laboratorios originales accesibles, agrupados de forma cohesiva para estudio o consulta directa.
