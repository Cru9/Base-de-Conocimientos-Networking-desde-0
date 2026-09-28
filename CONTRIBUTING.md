# 🤝 Guía de Contribución al Repositorio

¡Gracias por tu interés en colaborar con el **Network Engineering & Cybersecurity Master Compendium**! Este proyecto es un esfuerzo colaborativo y de código abierto para construir la documentación de redes y ciberseguridad más completa, rigurosa y práctica en idioma español.

Para mantener los más altos estándares de calidad técnica, legibilidad y coherencia, solicitamos seguir las siguientes directrices.

---

## 📋 Código de Conducta

- Mantener siempre una comunicación profesional, respetuosa y constructiva.
- Fomentar el aprendizaje mutuo y la colaboración técnica.
- Respetar el trabajo y tiempo de los revisores y autores.

---

## 🛠️ Cómo Proponer Cambios o Aportes

1. **Haz un Fork** del repositorio en tu cuenta de GitHub.
2. **Clona tu fork** localmente:
   ```bash
   git clone https://github.com/TU-USUARIO/BC.git
   cd BC
   ```
3. **Crea una nueva rama** descriptiva:
   ```bash
   git checkout -b feature/nuevo-laboratorio-bgp
   # o
   git checkout -b fix/corregir-sintaxis-huawei
   ```
4. **Realiza tus cambios** siguiendo las reglas de formato que se detallan a continuación.
5. **Realiza un commit** con un mensaje claro siguiendo la convención [Conventional Commits](https://www.conventionalcommits.org/):
   ```bash
   git commit -m "docs(routing): agregar caso de BGP MED y community no-export"
   ```
6. **Sube tus cambios** a tu fork:
   ```bash
   git push origin feature/nuevo-laboratorio-bgp
   ```
7. **Abre un Pull Request (PR)** hacia la rama `main` del repositorio oficial.

---

## ✍️ Estándares de Documentación y Formato Markdown

### 1. Formato de Archivo
- Todos los documentos deben estar en **Markdown estándar (.md)** codificados en **UTF-8 sin BOM**.
- Se prohíbe el uso de extensiones `.txt` para guías o manuales.

### 2. Bloques de Código y Sintaxis CLI
- Todo comando de terminal o configuración de conmutador debe estar delimitado por bloques de código con el resaltador de sintaxis apropiado:
  - Para Cisco IOS / IOS-XE / NX-OS: ````cisco`
  - Para scripts en Linux / BASH / CLI genérico: ````bash`
  - Para scripts de automatización: ````python`
  - Para diagramas de topología ASCII y diagramas de flujo: ````text` o ````mermaid`
- Incluye comentarios descriptivos en los scripts precedidos por `!` (en Cisco/Huawei) o `#` (en Linux/Python).

### 3. Estructura de un Laboratorio o Guía
Cada nuevo escenario técnico debe incluir:
1. **Título y Contexto:** Descripción clara del objetivo de ingeniería.
2. **Escenario Real:** Caso de negocio o requerimiento operativo corporativo.
3. **Diagrama de Red:** Topología en formato ASCII o Mermaid.
4. **Configuración por Equipo:** Bloques de código reproducibles y listos para producción.
5. **Comandos de Verificación:** Salidas esperadas de comandos `show` o `display`.
6. **Explicación Técnica:** Análisis de por qué funciona y posibles advertencias.

---

## 🔍 Proceso de Revisión

Todos los Pull Requests son revisados para verificar:
- Precisión técnica de los comandos y configuraciones.
- Cumplimiento de estándares de nombrado de archivos (`NUM_NOMBRE_DESCRIPTIVO.md`).
- Ausencia de enlaces rotos o caracteres corruptos de codificación.

¡Gracias por ayudar a conectar el mundo y elevar el estándar de la ingeniería de redes!
