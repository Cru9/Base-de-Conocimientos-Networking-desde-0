# 🗂️ Servicios Críticos DDI (DNS, DHCP, IPAM) y Gestión de Red

<p align="center">
  <img src="https://img.shields.io/badge/Servicios-DNS%20%7C%20DHCP%20%7C%20IPAM%20(DDI)-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Single%20Source%20of%20Truth-NetBox-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Sincronización-NTP%20%7C%20PTP%20IEEE%201588-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Monitoreo-SNMPv3%20%7C%20NetFlow%20%7C%20IPFIX-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Documentación-Markdown%20100%25-blue?style=for-the-badge&logo=markdown&logoColor=white" />
</p>

---

## 📌 Visión General del Módulo

Diseño e implementación de la tríada de servicios centrales indispensables para la operación de cualquier red corporativa: DNS Empresarial con Anycast BGP y Split-Horizon, DHCP de Alta Disponibilidad con Failover y Option 82, Gestión de Direccionamiento IPAM con NetBox como Fuente Única de Verdad (SSoT), sincronización horaria NTP/PTP y telemetría con SNMPv3 y NetFlow/IPFIX.

---

## 📚 Temario y Capítulos de Estudio

| Capítulo | Documento Técnico | Temas Principales |
| :---: | :--- | :--- |
| **00** | [00. INDICE GENERAL, ARQUITECTURA DDI Y OBSERVABILIDAD DE RED](./00_INDICE_Y_ARQUITECTURA_SERVICIOS_DDI.md) | Guía técnica y sintaxis de producción |
| **01** | [01. DNS EMPRESARIAL, ANYCAST BGP, SPLIT-HORIZON Y DNSSEC](./01_DNS_EMPRESARIAL_ANYCAST_BGP_DNSSEC_Y_SPLIT_HORIZON.md) | Guía técnica y sintaxis de producción |
| **02** | [02. DHCP ALTA DISPONIBILIDAD, OPCIONES AVANZADAS Y DHCP SNOOPING](./02_DHCP_ALTA_DISPONIBILIDAD_FAILOVER_Y_SNOOPING.md) | Guía técnica y sintaxis de producción |
| **03** | [03. IPAM CON NETBOX: FUENTE UNICA DE VERDAD (SINGLE SOURCE OF TRUTH)](./03_IPAM_NETBOX_SINGLE_SOURCE_OF_TRUTH.md) | Guía técnica y sintaxis de producción |
| **04** | [04. NTP, ESTRATOS, AUTENTICACION CRIPTOGRAFICA Y PTP (IEEE 1588)](./04_NTP_ESTRATOS_AUTENTICACION_Y_PTP_IEEE_1588.md) | Guía técnica y sintaxis de producción |
| **05** | [05. TELEMETRIA, SNMPV3 (AUTHPRIV), SYSLOG (RFC 5424) Y NETFLOW/IPFIX](./05_SNMPV3_AUTHPRIV_SYSLOG_RFC5424_Y_NETFLOW_IPFIX.md) | Guía técnica y sintaxis de producción |

---

## 🚀 Cómo Utilizar este Módulo

1. **Secuencia Recomendada:** Se sugiere revisar los documentos en orden numérico progresivo, ya que cada capítulo profundiza y construye sobre los conceptos del anterior.
2. **Sintaxis de Producción:** Todos los bloques de comandos están validados y optimizados para entornos operativos reales y laboratorios de certificación.
3. **Navegación:** Puedes volver al menú principal en cualquier momento a través del [README General del Repositorio](../README.md).

---

**Autor:** Ezequiel ([@Cru9](https://github.com/Cru9))  
**Licencia:** [MIT License](../LICENSE)
