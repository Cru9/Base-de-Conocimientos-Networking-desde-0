# ⚖️ Calidad de Servicio (QoS) y Modelado de Tráfico

<p align="center">
  <img src="https://img.shields.io/badge/Estándar-RFC%204594%20DiffServ-005073?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Marcado-L2%20CoS%20%7C%20L3%20DSCP-darkgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Mecanismos-Policing%20vs%20Shaping-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Algoritmos-LLQ%20%7C%20CBWFQ%20%7C%20WRED-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Documentación-Markdown%20100%25-blue?style=for-the-badge&logo=markdown&logoColor=white" />
</p>

---

## 📌 Visión General del Módulo

Teoría matemática y configuración práctica de Calidad de Servicio (QoS). Explica cómo clasificar, marcar y priorizar tráfico crítico como Telefonía VoIP (EF / DSCP 46) y Videoconferencias sobre datos recreativos, algoritmos de colas para evitar congestión (LLQ, CBWFQ, WRED) y comparativa técnica entre limitación de tasa (Policing) y suavizado de ráfagas (Traffic Shaping).

---

## 📚 Temario y Capítulos de Estudio

| Capítulo | Documento Técnico | Temas Principales |
| :---: | :--- | :--- |
| **00** | [00. INDICE GENERAL, RETOS DEL TRAFICO IP Y MODELOS DE QOS](./00_INDICE_Y_ARQUITECTURA_QOS.md) | Guía técnica y sintaxis de producción |
| **01** | [01. CLASIFICACION Y MARCADO DE PAQUETES: COS (CAPA 2) Y DSCP (CAPA 3)](./01_CLASIFICACION_Y_MARCADO_COS_DSCP.md) | Guía técnica y sintaxis de producción |
| **02** | [02. MECANISMOS DE PLANIFICACION DE COLAS Y CONTROL DE CONGESTION](./02_MECANISMOS_DE_COLAS_Y_CONGESTION.md) | Guía técnica y sintaxis de producción |
| **03** | [03. CONTROL DE TASA: TRAFFIC POLICING vs TRAFFIC SHAPING](./03_TRAFFIC_POLICING_VS_SHAPING.md) | Guía técnica y sintaxis de producción |
| **04** | [04. GUIA DE CONFIGURACION PRACTICA DE QOS MULTI-MARCA (CISCO, HUAWEI, ARUBA)](./04_CONFIGURACIONES_QOS_POR_MARCA.md) | Guía técnica y sintaxis de producción |

---

## 🚀 Cómo Utilizar este Módulo

1. **Secuencia Recomendada:** Se sugiere revisar los documentos en orden numérico progresivo, ya que cada capítulo profundiza y construye sobre los conceptos del anterior.
2. **Sintaxis de Producción:** Todos los bloques de comandos están validados y optimizados para entornos operativos reales y laboratorios de certificación.
3. **Navegación:** Puedes volver al menú principal en cualquier momento a través del [README General del Repositorio](../README.md).

---

**Autor:** Ezequiel ([@Cru9](https://github.com/Cru9))  
**Licencia:** [MIT License](../LICENSE)
