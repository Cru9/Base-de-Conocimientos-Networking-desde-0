@echo off
chcp 65001 >nul
title BC NETWORK - SUITE MAESTRA DE REDES Y CIBERSEGURIDAD PARA WINDOWS
color 0B

:MENU
cls
echo ===============================================================================
echo        BC NETWORK & CYBERSECURITY - SUITE MAESTRA PARA WINDOWS (CMD / PS)
echo                     Compendio Tecnico de Ingenieria - Cru9
echo ===============================================================================
echo.
echo  --- GESTION Y CONFIGURACION DE ADAPTADORES ---
echo   [1] CONFIGURADOR MAESTRO DE IP, MASCARA, GATEWAY Y DNS (Auto-Elevacion UAC)
echo.
echo  --- HERRAMIENTAS CMD (Mantenimiento, Servicios y Hardening) ---
echo   [2] Hardening de Protocolos Inseguros de Windows (SMBv1, LLMNR, NetBIOS, WPAD)
echo   [3] Diagnostico Integral por Capas OSI (L1 Fisica a L4 Transporte)
echo   [4] Controlador y Reinicio de Servicios de Red (DHCP, DNS, NTP, Firewall)
echo   [5] Optimizador de Rendimiento de la Pila TCP (Auto-Tuning, RSS, ECN, CUBIC)
echo.
echo  --- HERRAMIENTAS POWERSHELL POR DOMINIOS TECNICOS (CAPAS OSI) ---
echo   [6] Capa 1: Diagnostico Fisico y Hardware (Velocidad, Duplex, Errores CRC)
echo   [7] Capa 2: Auditoria de Tabla ARP, MACs, OUI de Fabricantes y Conflictos
echo   [8] Capa 3: Inspector de Rutas y Traza WAN Avanzada (TTL Probing y PTR)
echo   [9] Capa 4: Auditor de Salud de Sockets TCP/UDP y Fugas de Conexiones
echo   [10] DDI / NTP: Auditor de Servidores DNS, Concesiones DHCP y Reloj NTP
echo   [11] Wireless: Auditor de Redes Wi-Fi Enterprise (dBm, Banda, Canales, WPA3)
echo   [12] Firewall: Gestor y Auditor de Perfiles (Domain, Private, Public)
echo   [13] QoS: Verificador de Calidad de Servicio y Marcado DSCP (RFC 4594)
echo   [14] OT / SCADA: Tester de Sockets Industriales (Modbus, S7, CIP, DNP3)
echo.
echo  --- DOCUMENTACION ---
echo   [H] Ver Manual Tecnico y Guia de Ejecucion (README.md)
echo   [0] Salir
echo ===============================================================================
set /p OPT="Seleccione una opcion [0-14, H]: "

if "%OPT%"=="1" goto OP_CONFIG_IP
if "%OPT%"=="2" goto OP_HARDENING
if "%OPT%"=="3" goto OP_DIAG_OSI
if "%OPT%"=="4" goto OP_SERVICIOS
if "%OPT%"=="5" goto OP_OPT_TCP
if "%OPT%"=="6" goto OP_PS_L1
if "%OPT%"=="7" goto OP_PS_L2
if "%OPT%"=="8" goto OP_PS_L3
if "%OPT%"=="9" goto OP_PS_L4
if "%OPT%"=="10" goto OP_PS_DDI
if "%OPT%"=="11" goto OP_PS_WIFI
if "%OPT%"=="12" goto OP_PS_FW
if "%OPT%"=="13" goto OP_PS_QOS
if "%OPT%"=="14" goto OP_PS_OT
if /I "%OPT%"=="H" goto OP_DOC
if "%OPT%"=="0" goto SALIR

echo.
echo [!] Opcion invalida.
timeout /t 2 >nul
goto MENU

:OP_CONFIG_IP
cls
call "%~dp0Configurador_IP_Avanzado.cmd"
goto MENU

:OP_HARDENING
cls
call "%~dp0cmd\02_Hardening_Red_Insegura.cmd"
goto MENU

:OP_DIAG_OSI
cls
call "%~dp0cmd\03_Diagnostico_L1_L4_Completo.cmd"
goto MENU

:OP_SERVICIOS
cls
call "%~dp0cmd\04_Control_Servicios_Red.cmd"
goto MENU

:OP_OPT_TCP
cls
call "%~dp0cmd\05_Optimizador_TCP_Pila.cmd"
goto MENU

:OP_PS_L1
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\01_Diagnostico_L1_Fisico.ps1"
goto MENU

:OP_PS_L2
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\02_Auditoria_L2_ARP_MAC.ps1"
goto MENU

:OP_PS_L3
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\03_Inspector_Rutas_Traceroute.ps1"
goto MENU

:OP_PS_L4
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\04_Auditor_TCP_Sockets_Salud.ps1"
goto MENU

:OP_PS_DDI
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\05_Auditor_DNS_DHCP_NTP.ps1"
goto MENU

:OP_PS_WIFI
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\06_Auditor_WiFi_Enterprise.ps1"
goto MENU

:OP_PS_FW
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\07_Gestor_Firewall_Perfiles.ps1"
goto MENU

:OP_PS_QOS
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\08_Verificador_QoS_DSCP.ps1"
goto MENU

:OP_PS_OT
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0powershell\09_Tester_Conectividad_OT.ps1"
goto MENU

:OP_DOC
cls
start "" notepad "%~dp0README.md"
goto MENU

:SALIR
echo.
echo Gracias por utilizar BC Network Suite para Windows.
timeout /t 1 >nul
exit /b
