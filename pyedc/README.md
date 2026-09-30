# 🏛️ PyEDC - Enterprise Data & Connectivity Python Suite

**PyEDC** es un framework modular en Python construido sobre la **Base de Conocimientos EDC**. Convierte la documentación técnica, matrices multi-fabricante, fórmulas de ingeniería y bancos de preguntas en una plataforma activa de software para ingenieros de redes y ciberseguridad.

---

## 📦 Estructura de Módulos

```text
pyedc/
├── cli.py                     # CLI Maestro interactivo y parseador de subcomandos
├── config.py                  # Rutas maestras y constantes de red
├── modules/
│   ├── calculator/            # Módulo 1: Calculadora & Diseñador de Red
│   │   ├── subnetting.py      #   - IPv4/IPv6, VLSM, Supernetting y Árbol de IPs
│   │   ├── mtu_mss.py         #   - Cálculo de Overhead (IPsec/GRE/VXLAN) y TCP MSS
│   │   ├── optics.py          #   - Presupuesto Óptico (TIA-568-D / ISO 11801)
│   │   └── fabric_design.py   #   - Sobresuscripción y Spine-Leaf Clos para Datacenter
│   │
│   ├── automator/             # Módulo 2: Automatización Multi-Vendor
│   │   ├── matrix_parser.py   #   - Parseador de tablas Markdown y catálogo IANA
│   │   ├── transpiler.py      #   - Transpilador CLI (Cisco, Huawei, Aruba, etc.)
│   │   └── generator.py       #   - Generador de plantillas (VLANs, Acceso, Troncales)
│   │
│   ├── glossary/              # Módulo 3: Diccionario Enciclopédico (+200 Términos A-Z)
│   │   └── glossary_engine.py #   - Búsqueda por acrónimo, letra y flashcards técnicas
│   │
│   ├── troubleshooter/        # Módulo 4: Diagnóstico y Troubleshooting Guiado
│   │   └── troubleshooter.py  #   - Patologías L2-L7, filtros Wireshark y comandos Cisco/Huawei
│   │
│   ├── standards/             # Módulo 5: Catálogo Oficial de RFCs y Estándares IETF
│   │   └── rfc_catalog.py     #   - Consulta de RFCs con enlaces oficiales y categorías
│   │
│   ├── labs/                  # Módulo 6: Banco de 200 Laboratorios y Emulación
│   │   └── lab_catalog.py     #   - Bloques temáticos mapeados a certificaciones y emuladores
│   │
│   ├── examiner/              # Módulo 7: Simulador de Certificaciones
│   │   ├── parser.py          #   - Extractor de preguntas de certificación Markdown
│   │   └── engine.py          #   - Motor interactivo de examen (Práctica / Simulación)
│   │
│   └── copilot/               # Módulo 8: Asistente Técnico y RAG
│       ├── indexer.py         #   - Indexador semántico con extracción de RFCs
│       ├── retriever.py       #   - Buscador de alta precisión (BM25 / Scoring ponderado)
│       └── chat.py            #   - Chat interactivo de preguntas técnicas
```

---

## 🚀 Inicio Rápido

### 1. Activar Entorno Virtual
```powershell
# En Windows:
.venv\Scripts\activate
```

### 2. Ejecutar el Menú Interactivo Visual
Si no pasas argumentos, se abrirá un menú guiado en la consola:
```powershell
python run.py
# o también:
python -m pyedc
```

---

## 💻 Ejemplos de Uso por Línea de Comandos

### 🧮 1. Calculadora y Diseñador de Red
```powershell
# Análisis detallado de subred
python -m pyedc calc subnet --cidr 10.50.0.0/22

# Cálculo VLSM con requerimientos por departamento
python -m pyedc calc vlsm --cidr 192.168.1.0/24 --hosts "Ventas:50,Ingenieria:20,DMZ:10,WAN:2"

# Cálculo de MTU de ruta y TCP MSS con túnel IPsec ESP y VLAN 802.1Q
python -m pyedc calc mss --mtu 1500 --encaps ipsec_esp,vlan_8021q

# Presupuesto óptico de enlace de 10 km con fibra monomodo OS2 y 10GBASE-LR
python -m pyedc calc optics --distance 10 --fiber OS2_1310 --transceiver 10GBASE-LR

# Dimensionamiento de Datacenter Spine-Leaf Clos
python -m pyedc calc fabric --leafs 4 --downlinks 48 --uplinks 4
```

### ⚙️ 2. Automatización y Transpilador Multi-Vendor
```powershell
# Traducir comando de Cisco IOS a Huawei VRP
python -m pyedc automator translate --cmd "switchport mode trunk" --from-vendor cisco --to-vendor huawei

# Buscar en la matriz comparativa de todos los fabricantes
python -m pyedc automator matrix --query "rstp"

# Generar plantilla de configuración para VLAN
python -m pyedc automator generate --task vlan --vendor aruba

# Consultar catálogo IANA, riesgo y mitigación
python -m pyedc automator ports --query "445"
```

### 🎓 3. Simulador de Certificaciones
```powershell
# Iniciar sesión de estudio en Modo Práctica (5 preguntas)
python -m pyedc exam --mode practice --count 5

# Iniciar Simulación Oficial de Examen cronometrada (10 preguntas)
python -m pyedc exam --mode simulation --count 10
```

### 🧠 4. Asistente Técnico y Copilot EDC
```powershell
# Pregunta directa con citas exactas a la base y estándares RFC
python -m pyedc copilot ask -q "RFC 7348 VXLAN"

# Iniciar sesión de chat interactiva
python -m pyedc copilot chat
```

---

## 🧪 Pruebas Unitarias
El proyecto cuenta con un suite completa de tests unitarios:
```powershell
python -m unittest tests/test_pyedc.py
```
