# 00. GUIA DE USO, REQUISITOS Y EJECUCION DE SCRIPTS

> **TOOLS: SUITE DE HERRAMIENTAS Y SCRIPTS DE RED PARA WINDOWS**


---



## 1. INTRODUCCION A LA SUITE DE HERRAMIENTAS

Esta carpeta contiene herramientas avanzadas desarrolladas en PowerShell (.ps1)
y scripts por lotes (.cmd) disenadas especificamente para ingenieros de redes,
administradores de sistemas y analistas de ciberseguridad que operan en estaciones
de trabajo y servidores Windows (Windows 10, Windows 11, Windows Server 2016/2019/2022).

Las herramientas no requieren software pesado adicional de terceros y aprovechan
el poder nativo de PowerShell, la pila .NET Framework y utilidades nativas de Windows
(Netsh, TCP Sockets, ICMP API).



## 2. COMO EJECUTAR LOS SCRIPTS EN WINDOWS

Por defecto, Windows restringe la ejecucion de scripts de PowerShell por seguridad
(Politica de Ejecucion "Restricted").

OPCION 1: El Menu Maestro (LA FORMA MAS FACIL)
- Simplemente haz doble clic en el archivo:
  `Menu_Principal.cmd`
- Este iniciador abre una consola interactiva, salta automaticamente las restricciones
  de ejecucion de forma segura y te permite elegir cualquier herramienta con un solo numero.

OPCION 2: Ejecucion desde PowerShell
- Abre una ventana de PowerShell y ejecuta:
  `powershell -ExecutionPolicy Bypass -File .\NombreDelScript.ps1`
- O para tu sesion actual de PowerShell:
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
  Y luego ejecuta directamente:
  `.\SuperPing_Continuo.ps1`

OPCION 3: Ejecutar con Permisos de Administrador
- Algunas herramientas (como la captura de paquetes nativa con `netsh trace` o
  la modificacion de adaptadores) requieren ejecutarse con privilegios elevados.
- Haz clic derecho sobre PowerShell y selecciona "Ejecutar como administrador".



## 3. CATALOGO DE HERRAMIENTAS INCLUIDAS

01. Menu_Principal.cmd
    - Lanzador interactivo por lotes con interfaz de menu en consola para ejecutar
      cualquiera de las herramientas de la suite con un solo clic.

02. SuperPing_Continuo.ps1
    - Monitor de ping avanzado con marcas de tiempo (timestamp en milisegundos),
      alertas visuales con codigo de colores (verde <30ms, amarillo 30-80ms, rojo >80ms),
      pitido sonoro ante paquetes perdidos y guardado automatico en archivo CSV/TXT.

03. Descubridor_MTU_Path.ps1
    - Herramienta de descubrimiento automatico del MTU de ruta (PMTU) utilizando
      pings con bandera DF (Don't Fragment). Calcula el MTU maximo sin fragmentar
      y el TCP MSS optimo para tuneles VPN (IPsec, WireGuard, GRE).

04. Wifi_Analyzer_Audit.ps1
    - Escaner y auditor de redes Wi-Fi en tiempo real. Analiza todas las redes
      inalambricas al alcance, calcula RSSI en dBm, canal, banda (2.4/5/6 GHz),
      estandar (802.11ax/ac/n) y tipo de seguridad (WPA2, WPA3, Abierta).

05. Wifi_Password_Extractor.ps1
    - Auditoria y respaldo de perfiles Wi-Fi guardados en la maquina local.
      Recupera nombres de SSID, tipo de cifrado y contrasenas en texto claro.

06. Wifi_Roaming_Live_Monitor.ps1
    - Monitor en vivo para pruebas de movilidad y cobertura. Registra en tiempo real
      el AP (BSSID), canal, RSSI y velocidad negociada mientras el usuario camina,
      emitiendo alertas audibles y visuales cuando ocurre un roaming entre APs.

07. Port_Scanner_Rapido.ps1
    - Escaner de puertos TCP multihilo basado en sockets .NET de alta velocidad.
      Permite auditar puertos comunes de infraestructura (SSH, Telnet, HTTP, HTTPS,
      RDP, SMB, Bases de Datos) o rangos personalizados contra cualquier host.

08. Test_DNS_Performance.ps1
    - Medidor comparativo de rendimiento de servidores DNS. Consulta en paralelo
      el DNS local contra Google (8.8.8.8), Cloudflare (1.1.1.1), Quad9 (9.9.9.9)
      y OpenDNS, mostrando cual ofrece la menor latencia de resolucion.

09. Captura_Paquetes_Nativa.ps1
    - Capturador de paquetes de red 100% nativo de Windows mediante `netsh trace`.
      Permite capturar trafico en servidores de produccion donde no se puede instalar
      Wireshark, con buffer circular para no saturar el disco.

10. Reporte_Salud_Red.ps1
    - Diagnostico integral de la maquina: adaptadores de red, velocidad y duplex,
      IPs, mascara, gateway, servidores DNS/DHCP, tabla ARP, tabla de enrutamiento

y conexiones activas. Genera un reporte profesional en formato HTML.
