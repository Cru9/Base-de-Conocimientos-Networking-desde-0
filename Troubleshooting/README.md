# 🔍 Base de Conocimientos de Resolución de Fallas (Troubleshooting de Switches)

<p align="center">
  <img src="https://img.shields.io/badge/Metodología-OSI%20Layer%20Diagnostic-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Fallas-Errdisable%20%7C%20Loops%20%7C%20LACP-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Multi--Vendor-Cisco%20%7C%20Huawei%20%7C%20HP%20%7C%20Aruba-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Diagnóstico-Show%20%26%20Display%20Commands-darkgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Documentación-Markdown%20100%25-blue?style=for-the-badge&logo=markdown&logoColor=white" />
</p>

---

## 📌 Visión General del Módulo

Guía práctica de triaje, aislamiento y resolución de incidentes críticos en conmutadores multi-fabricante. Documenta causas raíz, síntomas físicos (LEDs de estado), comandos de inspección en vivo y procedimientos exactos de solución para puertos en err-disabled, caídas de Spanning Tree, tormentas de broadcast, Native VLAN mismatch, problemas de agregación LACP y fallas de Capa 1 física.

---

## 📚 Temario y Capítulos de Estudio

| Capítulo | Documento Técnico | Temas Principales |
| :---: | :--- | :--- |
| **00** | [00. INDICE MAESTRO, METODOLOGIA DE DIAGNOSTICO Y PROTOCOLO DE TRIAGE](./00_INDICE_Y_METODOLOGIA_DE_DIAGNOSTICO.md) | Guía técnica y sintaxis de producción |
| **01** | [01. PUERTOS BLOQUEADOS (ERR-DISABLED / SHUTDOWN POR SEGURIDAD Y BPDU GUARD)](./01_fallas_puertos_bloqueados_errdisable_y_seguridad.md) | Guía técnica y sintaxis de producción |
| **02** | [02. FALLAS DE VLANS, PUERTOS TRONCALES Y DISCREPANCIA DE VLAN NATIVA](./02_fallas_vlans_troncales_y_vlan_nativa.md) | Guía técnica y sintaxis de producción |
| **03** | [03. FALLAS DE SPANNING TREE, BUCLES DE CAPA 2 Y TORMENTAS DE DIFUSION](./03_fallas_spanning_tree_bucles_y_tormentas.md) | Guía técnica y sintaxis de producción |
| **04** | [04. FALLAS EN ENLACES AGREGADOS (PORT-CHANNEL / LACP / LAG / ETH-TRUNK)](./04_fallas_enlace_agregado_lag_lacp_port_channel.md) | Guía técnica y sintaxis de producción |
| **05** | [05. FALLAS DE ENRUTAMIENTO INTER-VLAN, INTERFACES SVI Y GATEWAYS](./05_fallas_enrutamiento_intervlan_svi_y_gateway.md) | Guía técnica y sintaxis de producción |
| **06** | [06. FALLAS DE CAPA 1 FISICA: SFP, FIBRA OPTICA, DUPLEX Y CABLE DE COBRE](./06_fallas_capa_1_fisica_sfp_fibra_y_cable_utp.md) | Guía técnica y sintaxis de producción |
| **07** | [07. FALLAS DE ACCESO REMOTO (SSH / TELNET), AUTENTICACION Y RECUPERACION DE CLAVES](./07_fallas_acceso_remoto_ssh_telnet_y_autenticacion.md) | Guía técnica y sintaxis de producción |
| **08** | [08. FALLAS DE DHCP SNOOPING, DYNAMIC ARP INSPECTION (DAI) Y TABLAS ARP](./08_fallas_dhcp_snooping_dai_y_arp.md) | Guía técnica y sintaxis de producción |
| **09** | [09. GUIA DE ERRORES FRECUENTES Y PECULIARIDADES ("GOTCHAS") POR MARCA](./09_guia_errores_frecuentes_y_gotchas_por_marca.md) | Guía técnica y sintaxis de producción |

---

## 🚀 Cómo Utilizar este Módulo

1. **Secuencia Recomendada:** Se sugiere revisar los documentos en orden numérico progresivo, ya que cada capítulo profundiza y construye sobre los conceptos del anterior.
2. **Sintaxis de Producción:** Todos los bloques de comandos están validados y optimizados para entornos operativos reales y laboratorios de certificación.
3. **Navegación:** Puedes volver al menú principal en cualquier momento a través del [README General del Repositorio](../README.md).

---

**Autor:** Ezequiel ([@Cru9](https://github.com/Cru9))  
**Licencia:** [MIT License](../LICENSE)
