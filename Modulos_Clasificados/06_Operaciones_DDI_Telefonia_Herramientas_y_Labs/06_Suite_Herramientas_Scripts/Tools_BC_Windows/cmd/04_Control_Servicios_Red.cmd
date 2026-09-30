@echo off
chcp 65001 >nul
title BC NETWORK - CONTROLADOR DE SERVICIOS DE RED DE WINDOWS
color 0E

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [i] Solicitando permisos administrativos para gestionar servicios del sistema...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

:MENU_SERVICIOS
cls
echo ===============================================================================
echo            BC NETWORK TOOLKIT - CONTROL DE SERVICIOS DE RED
echo ===============================================================================
echo.
echo Estado de Servicios Clave de Red:
powershell -Command "Get-Service -Name Dhcp, Dnscache, W32Time, mpssvc, LanmanServer, LanmanWorkstation, NlaSvc | Select-Object Name, DisplayName, Status, StartType | Format-Table -AutoSize"
echo.
echo  --- ACCIONES RAPIDAS ---
echo   [1] Reiniciar Servicio de Cache DNS (Dnscache) y vaciar registros
echo   [2] Reiniciar Servicio de Cliente DHCP (Dhcp)
echo   [3] Forzar Resincronizacion de Hora NTP (W32Time y w32tm /resync)
echo   [4] Reiniciar Servicio de Firewall de Windows (mpssvc)
echo   [5] Reiniciar Servicio de Deteccion de Red (NlaSvc - Network Location Awareness)
echo   [6] Reiniciar TODOS los servicios de red esenciales
echo.
echo   [0] Salir
echo ===============================================================================
set /p OPT="Seleccione una opcion [0-6]: "

if "%OPT%"=="1" goto RESTART_DNS
if "%OPT%"=="2" goto RESTART_DHCP
if "%OPT%"=="3" goto RESYNC_NTP
if "%OPT%"=="4" goto RESTART_FW
if "%OPT%"=="5" goto RESTART_NLA
if "%OPT%"=="6" goto RESTART_ALL
if "%OPT%"=="0" exit /b

echo [!] Opcion invalida.
timeout /t 2 >nul
goto MENU_SERVICIOS

:RESTART_DNS
echo [*] Purgando cache DNS...
ipconfig /flushdns
echo [*] Reiniciando servicio Dnscache...
powershell -Command "Restart-Service -Name Dnscache -Force -ErrorAction SilentlyContinue"
echo [OK] Servicio DNS actualizado.
pause
goto MENU_SERVICIOS

:RESTART_DHCP
echo [*] Reiniciando servicio Cliente DHCP...
net stop Dhcp /y >nul 2>&1
net start Dhcp >nul 2>&1
ipconfig /renew >nul 2>&1
echo [OK] Servicio DHCP reiniciado y direcciones renovadas.
pause
goto MENU_SERVICIOS

:RESYNC_NTP
echo [*] Iniciando y resincronizando hora con servidor NTP...
net start W32Time >nul 2>&1
w32tm /resync /nowait
w32tm /query /status
echo [OK] Peticion de sincronizacion NTP emitida.
pause
goto MENU_SERVICIOS

:RESTART_FW
echo [*] Reiniciando Windows Defender Firewall (mpssvc)...
net stop mpssvc /y >nul 2>&1
net start mpssvc >nul 2>&1
echo [OK] Firewall reiniciado.
pause
goto MENU_SERVICIOS

:RESTART_NLA
echo [*] Reiniciando Network Location Awareness (NlaSvc)...
net stop NlaSvc /y >nul 2>&1
net start NlaSvc >nul 2>&1
echo [OK] Servicio NLA reiniciado.
pause
goto MENU_SERVICIOS

:RESTART_ALL
echo [*] Reiniciando pila completa de servicios de red...
net stop Dhcp /y >nul 2>&1
net start Dhcp >nul 2>&1
net start W32Time >nul 2>&1
net start mpssvc >nul 2>&1
net stop NlaSvc /y >nul 2>&1
net start NlaSvc >nul 2>&1
ipconfig /flushdns >nul 2>&1
echo.
echo [EXITO] Servicios restablecidos.
pause
goto MENU_SERVICIOS
