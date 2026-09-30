# 🧱 Arquitectura de Firewalls Perimetrales y Tecnologías VPN

<p align="center">
  <img src="https://img.shields.io/badge/VPN-IPsec%20IKEv2%20Site--to--Site-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/VPN-DMVPN%20Phases%201%2F2%2F3-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Remote%20Access-SSL%20%7C%20WireGuard-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/NAT-Static%20%7C%20Dynamic%20%7C%20PAT-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Documentación-Markdown%20100%25-blue?style=for-the-badge&logo=markdown&logoColor=white" />
</p>

---

## 📌 Visión General del Módulo

Diseño e implementación de políticas de seguridad en bordes perimetrales corporativos. Cubre la teoría y práctica de inspección con estado (Stateful Inspection), tablas de traducción de direcciones de red (NAT estático, dinámico y PAT por sobrecarga), túneles IPsec IKEv2 robustos, DMVPN multipunto y VPNs modernas de acceso remoto (SSL y WireGuard).

---

## 📚 Temario y Capítulos de Estudio

| Capítulo | Documento Técnico | Temas Principales |
| :---: | :--- | :--- |
| **00** | [00. INDICE GENERAL, ARQUITECTURA DE CORTAFUEGOS Y ZONAS DE SEGURIDAD](./00_INDICE_Y_ARQUITECTURA_FIREWALLS.md) | Guía técnica y sintaxis de producción |
| **01** | [01. POLITICAS DE SEGURIDAD, TIPOS DE NAT/PAT Y DESCIFRADO SSL/TLS](./01_POLITICAS_DE_SEGURIDAD_NAT_Y_PAT.md) | Guía técnica y sintaxis de producción |
| **02** | [02. VPN IPSEC SITE-TO-SITE AVANZADO (IKEv1 vs IKEv2, FASES Y TUNEL VTI)](./02_VPN_IPSEC_SITE_TO_SITE_AVANZADO.md) | Guía técnica y sintaxis de producción |
| **03** | [03. DMVPN (DYNAMIC MULTIPOINT VPN) - ARQUITECTURA mGRE, NHRP Y FASES 1, 2 Y 3](./03_DMVPN_DYNAMIC_MULTIPOINT_VPN.md) | Guía técnica y sintaxis de producción |
| **04** | [04. VPN DE ACCESO REMOTO: SSL/TLS VPN vs WIREGUARD Y AUTENTICACION MFA](./04_VPN_ACCESO_REMOTO_SSL_Y_WIREGUARD.md) | Guía técnica y sintaxis de producción |
| **05** | [05. CONFIGURACIONES REALES EN CORTAFUEGOS: FORTINET FORTIGATE Y PALO ALTO](./05_CONFIGURACIONES_PRACTICAS_FIREWALLS.md) | Guía técnica y sintaxis de producción |

---

## 🚀 Cómo Utilizar este Módulo

1. **Secuencia Recomendada:** Se sugiere revisar los documentos en orden numérico progresivo, ya que cada capítulo profundiza y construye sobre los conceptos del anterior.
2. **Sintaxis de Producción:** Todos los bloques de comandos están validados y optimizados para entornos operativos reales y laboratorios de certificación.
3. **Navegación:** Puedes volver al menú principal en cualquier momento a través del [README General del Repositorio](../README.md).

---

**Autor:** Ezequiel ([@Cru9](https://github.com/Cru9))  
**Licencia:** [MIT License](../LICENSE)
