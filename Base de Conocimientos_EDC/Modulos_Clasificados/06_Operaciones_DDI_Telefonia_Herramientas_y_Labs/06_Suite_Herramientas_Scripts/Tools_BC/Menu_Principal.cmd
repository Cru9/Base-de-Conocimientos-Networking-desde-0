@echo off
chcp 65001 >nul
title BC NETWORK TOOLKIT - MASTER LAUNCHER (CMD / POWERSHELL / PYTHON)
color 0B

:MENU
cls
echo ===============================================================================
echo       BC NETWORK & CYBERSECURITY MASTER TOOLKIT (CMD / POWERSHELL / PYTHON)
echo                      Compendio Maestro - Cru9
echo ===============================================================================
echo.
echo  --- HERRAMIENTAS CMD (Mantenimiento y Recuperacion Rapida) ---
echo   [1] Reinicio y Limpieza Profunda de Red (Flush DNS, ARP, Winsock, TCP/IP)
echo   [2] Administrador de Rutas Estaticas IPv4 (route add/del, persistentes)
echo   [3] Diagnostico Veloz de Conectividad (IP, Gateway, DNS e IP Publica)
echo.
echo  --- HERRAMIENTAS POWERSHELL (Seguridad, Monitoreo y DDI) ---
echo   [4] Detector de Servidores Rogue DHCP en LAN (Defensa L2 contra MITM)
echo   [5] Monitor en Vivo de Conexiones Activas / SOC (Deteccion de Puertos C2)
echo   [6] Auditor de Reglas de Entrada de Windows Firewall (Hardening)
echo   [7] Benchmark y Comparativa de Velocidad DNS (Local vs Cloudflare/Google)
echo.
echo  --- HERRAMIENTAS PYTHON (Automatizacion, Forense y Ciberseguridad) ---
echo   [8] Menu Grafico Interactivo Python (Panel Completo Rich CLI)
echo   [9] Calculadora VLSM y Generador de Configuraciones (Cisco / Huawei)
echo   [10] Respaldo y Diff de Configuraciones Multi-Vendor con Netmiko
echo   [11] Analizador Forense de Archivos PCAP con Scapy (Wireshark Automata)
echo   [12] Detector en Vivo de Envenenamiento ARP / Man-In-The-Middle
echo   [13] Auditor de Certificados SSL/TLS, Ciphers y Caducidad
echo   [14] Servidor Colector Syslog UDP en Vivo (RFC 5424)
echo   [15] Auditor y Escaner de Redes Industriales OT / SCADA (Purdue)
echo   [16] Escaner Multihilo TCP con Banner Grabbing de Servicios
echo.
echo  --- MANTENIMIENTO Y GUIA ---
echo   [P] Instalar / Verificar Dependencias de Python (pip install)
echo   [H] Abrir Documentacion y Guia de Uso (README.md)
echo   [0] Salir
echo ===============================================================================
set /p OPCION="Seleccione una opcion [0-16, P, H]: "

if "%OPCION%"=="1" goto CMD_RESET
if "%OPCION%"=="2" goto CMD_RUTAS
if "%OPCION%"=="3" goto CMD_DIAG
if "%OPCION%"=="4" goto PS_DHCP
if "%OPCION%"=="5" goto PS_SOC
if "%OPCION%"=="6" goto PS_FW
if "%OPCION%"=="7" goto PS_DNS
if "%OPCION%"=="8" goto PY_MENU
if "%OPCION%"=="9" goto PY_VLSM
if "%OPCION%"=="10" goto PY_BACKUP
if "%OPCION%"=="11" goto PY_PCAP
if "%OPCION%"=="12" goto PY_ARP
if "%OPCION%"=="13" goto PY_TLS
if "%OPCION%"=="14" goto PY_SYSLOG
if "%OPCION%"=="15" goto PY_OT
if "%OPCION%"=="16" goto PY_SCANNER
if /I "%OPCION%"=="P" goto PY_PIP
if /I "%OPCION%"=="H" goto VER_GUIA
if "%OPCION%"=="0" goto SALIR

echo.
echo [!] Opcion invalida.
timeout /t 2 >nul
goto MENU

:CMD_RESET
cls
call "%~dp0cmd\01_Reset_Pila_Red.cmd"
goto MENU

:CMD_RUTAS
cls
call "%~dp0cmd\02_Rutas_Estaticas_Mgr.cmd"
goto MENU

:CMD_DIAG
cls
call "%~dp0cmd\03_Diagnostico_Rapido.cmd"
goto MENU

:PS_DHCP
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\Detect_Rogue_DHCP.ps1"
goto MENU

:PS_SOC
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\Monitor_Conexiones_SOC.ps1"
goto MENU

:PS_FW
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\Auditor_Firewall_Reglas.ps1"
goto MENU

:PS_DNS
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\Test_DNS_Benchmark.ps1"
goto MENU

:PY_MENU
cls
python "%~dp0python\menu_tools.py"
goto MENU

:PY_VLSM
cls
python "%~dp0python\vlsm_calculator.py"
echo.
pause
goto MENU

:PY_BACKUP
cls
python "%~dp0python\multivendor_backup.py"
echo.
pause
goto MENU

:PY_PCAP
cls
python "%~dp0python\pcap_analyzer.py"
echo.
pause
goto MENU

:PY_ARP
cls
python "%~dp0python\arp_spoof_detector.py"
echo.
pause
goto MENU

:PY_TLS
cls
python "%~dp0python\tls_cert_inspector.py"
echo.
pause
goto MENU

:PY_SYSLOG
cls
python "%~dp0python\syslog_collector.py"
echo.
pause
goto MENU

:PY_OT
cls
python "%~dp0python\ot_industrial_scanner.py"
echo.
pause
goto MENU

:PY_SCANNER
cls
python "%~dp0python\port_banner_grabber.py"
echo.
pause
goto MENU

:PY_PIP
cls
echo [*] Instalando y verificando dependencias Python...
python -m pip install -r "%~dp0requirements.txt"
echo.
pause
goto MENU

:VER_GUIA
cls
start "" notepad "%~dp0README.md"
goto MENU

:SALIR
echo.
echo Gracias por utilizar BC Network Toolkit. Hasta pronto.
timeout /t 1 >nul
exit /b
