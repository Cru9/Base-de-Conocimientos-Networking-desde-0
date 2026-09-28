@echo off
chcp 65001 >nul
title BC NETWORK TOOLKIT - SUITE DE HERRAMIENTAS DE RED PARA WINDOWS
color 0B

:MENU
cls
echo ===============================================================================
echo            BC NETWORK TOOLKIT - SUITE DE HERRAMIENTAS DE RED
echo ===============================================================================
echo.
echo   [1] SuperPing Continuo (Timestamp, Latencia en ms, Alertas Sonoras y CSV)
echo   [2] Descubridor de MTU de Ruta (Path MTU con DF) y Calculo de TCP MSS
echo   [3] Auditor y Analizador Wi-Fi (dBm, Canales, Bandas y Seguridad)
echo   [4] Extractor y Backup de Claves Wi-Fi Almacenadas en Windows
echo   [5] Monitor en Vivo de Roaming Wi-Fi y Cobertura (Site Survey)
echo   [6] Escaner de Puertos TCP de Alta Velocidad (Servicios y Banner Grabbing)
echo   [7] Benchmark y Comparativa de Velocidad DNS (Local vs Google/Cloudflare)
echo   [8] Capturador Nativo de Paquetes de Red (netsh trace sin software externo)
echo   [9] Reporte Integral de Salud de Red (Generador de Informe HTML)
echo.
echo   [H] Ver Guia y Manual de las Herramientas (README)
echo   [0] Salir
echo.
echo ===============================================================================
set /p OPCION="Seleccione una opcion [0-9, H]: "

if "%OPCION%"=="1" goto OP1
if "%OPCION%"=="2" goto OP2
if "%OPCION%"=="3" goto OP3
if "%OPCION%"=="4" goto OP4
if "%OPCION%"=="5" goto OP5
if "%OPCION%"=="6" goto OP6
if "%OPCION%"=="7" goto OP7
if "%OPCION%"=="8" goto OP8
if "%OPCION%"=="9" goto OP9
if /I "%OPCION%"=="H" goto OPH
if "%OPCION%"=="0" goto SALIR

echo.
echo [!] Opcion invalida. Intente nuevamente.
timeout /t 2 >nul
goto MENU

:OP1
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0SuperPing_Continuo.ps1"
echo.
pause
goto MENU

:OP2
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0Descubridor_MTU_Path.ps1"
echo.
pause
goto MENU

:OP3
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0Wifi_Analyzer_Audit.ps1"
echo.
pause
goto MENU

:OP4
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0Wifi_Password_Extractor.ps1"
echo.
pause
goto MENU

:OP5
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0Wifi_Roaming_Live_Monitor.ps1"
echo.
pause
goto MENU

:OP6
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0Port_Scanner_Rapido.ps1"
echo.
pause
goto MENU

:OP7
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0Test_DNS_Performance.ps1"
echo.
pause
goto MENU

:OP8
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0Captura_Paquetes_Nativa.ps1"
echo.
pause
goto MENU

:OP9
cls
powershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0Reporte_Salud_Red.ps1"
echo.
pause
goto MENU

:OPH
cls
notepad "%~dp000_README_GUIA_HERRAMIENTAS.txt"
goto MENU

:SALIR
echo.
echo Gracias por utilizar BC Network Toolkit. Hasta pronto.
timeout /t 1 >nul
exit /b
