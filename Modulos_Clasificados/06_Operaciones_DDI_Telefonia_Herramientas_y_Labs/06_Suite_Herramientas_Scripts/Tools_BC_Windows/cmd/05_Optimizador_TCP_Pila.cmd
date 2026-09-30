@echo off
chcp 65001 >nul
title BC NETWORK - OPTIMIZADOR DE PILA TCP/IP DE WINDOWS
color 0B

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [i] Solicitando permisos administrativos para configurar parametros de la pila TCP...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

:MENU_TCP
cls
echo ===============================================================================
echo            BC NETWORK TOOLKIT - OPTIMIZACION DE PILA TCP (WINDOWS)
echo ===============================================================================
echo.
echo Parametros TCP globales actuales:
netsh int tcp show global
echo.
echo  --- OPCIONES DE OPTIMIZACION ---
echo   [1] Ver estado detallado de metricas TCP
echo   [2] Aplicar perfil de ALTO RENDIMIENTO (Auto-Tuning Normal, RSS Habilitado, CUBIC)
echo   [3] Habilitar ECN (Explicit Congestion Notification - Notificacion de Congestion)
echo   [4] Habilitar Timestamps TCP (RFC 1323)
echo   [5] Restablecer pila TCP a valores originales predeterminados de Windows
echo.
echo   [0] Salir
echo ===============================================================================
set /p OPT="Seleccione una opcion [0-5]: "

if "%OPT%"=="1" goto VER_TCP
if "%OPT%"=="2" goto OPTIMIZAR_ALTO
if "%OPT%"=="3" goto SET_ECN
if "%OPT%"=="4" goto SET_TIMESTAMPS
if "%OPT%"=="5" goto RESET_DEFAULTS
if "%OPT%"=="0" exit /b

echo [!] Opcion invalida.
timeout /t 2 >nul
goto MENU_TCP

:VER_TCP
cls
netsh int tcp show global
echo.
pause
goto MENU_TCP

:OPTIMIZAR_ALTO
cls
echo [*] Configurando nivel de ajuste automatico de ventana de recepcion a 'normal'...
netsh int tcp set global autotuninglevel=normal

echo [*] Habilitando escalabilidad del lado de recepcion (Receive-Side Scaling - RSS)...
netsh int tcp set global rss=enabled

echo [*] Configurando algoritmo de control de congestion a CUBIC (o CTCP)...
powershell -Command "try { Set-NetTCPSetting -SettingName InternetCustom -CongestionProvider CUBIC -ErrorAction SilentlyContinue } catch {}"

echo.
echo [OK] Perfil de alto rendimiento aplicado.
echo.
pause
goto MENU_TCP

:SET_ECN
netsh int tcp set global ecncapability=enabled
echo [OK] ECN habilitado (RFC 3168).
pause
goto MENU_TCP

:SET_TIMESTAMPS
netsh int tcp set global timestamps=enabled
echo [OK] Marcas de tiempo TCP habilitadas.
pause
goto MENU_TCP

:RESET_DEFAULTS
cls
netsh int tcp set global autotuninglevel=normal
netsh int tcp set global rss=enabled
netsh int tcp set global ecncapability=disabled
netsh int tcp set global timestamps=disabled
echo [OK] Pila TCP restablecida a valores por defecto de Windows.
pause
goto MENU_TCP
