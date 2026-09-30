@echo off
chcp 65001 >nul
title BC NETWORK - ADMINISTRADOR DE RUTAS ESTATICAS (WINDOWS)
color 0A

:MENU_RUTAS
cls
echo ===============================================================================
echo            BC NETWORK TOOLKIT - GESTION DE RUTAS ESTATICAS (IPv4)
echo ===============================================================================
echo.
echo   [1] Ver tabla de enrutamiento IPv4 activa (route print -4)
echo   [2] Ver solo rutas persistentes (estaticas guardadas)
echo   [3] Agregar nueva ruta estatica temporal
echo   [4] Agregar nueva ruta estatica PERSISTENTE (sobrevive al reinicio)
echo   [5] Eliminar una ruta estatica existente
echo   [6] Probar conectividad hacia un Gateway / Next-Hop (Ping)
echo   [0] Salir al menu principal
echo.
echo ===============================================================================
set /p OPT="Seleccione una opcion [0-6]: "

if "%OPT%"=="1" goto VER_TABLA
if "%OPT%"=="2" goto VER_PERSISTENTES
if "%OPT%"=="3" goto AGREGAR_TEMP
if "%OPT%"=="4" goto AGREGAR_PERM
if "%OPT%"=="5" goto ELIMINAR_RUTA
if "%OPT%"=="6" goto TEST_GATEWAY
if "%OPT%"=="0" exit /b

echo [!] Opcion invalida.
timeout /t 2 >nul
goto MENU_RUTAS

:VER_TABLA
cls
echo --- TABLA DE ENRUTAMIENTO IPv4 COMPLETA ---
echo.
route print -4
echo.
pause
goto MENU_RUTAS

:VER_PERSISTENTES
cls
echo --- RUTAS PERSISTENTES CONFIGURADAS EN WINDOWS ---
echo.
powershell -Command "Get-NetRoute -PolicyStore PersistentStore -AddressFamily IPv4 | Format-Table DestinationPrefix, NextHop, RouteMetric, IfIndex -AutoSize"
echo.
pause
goto MENU_RUTAS

:AGREGAR_TEMP
cls
echo --- AGREGAR RUTA ESTATICA TEMPORAL ---
echo Formato de ejemplo: Red: 10.50.0.0  Mascara: 255.255.0.0  Gateway: 192.168.1.254
echo.
set /p RED="Direccion de Red Destino (ej. 172.16.0.0): "
set /p MASCARA="Mascara de Subred (ej. 255.255.255.0): "
set /p GW="Siguiente Salto / Gateway (ej. 192.168.1.1): "

echo.
echo Ejecutando: route add %RED% mask %MASCARA% %GW%
route add %RED% mask %MASCARA% %GW%
if %ERRORLEVEL% EQU 0 (
    echo [OK] Ruta temporal agregada correctamente.
) else (
    echo [ERROR] No se pudo agregar la ruta. Asegurese de ejecutar la consola como Administrador.
)
echo.
pause
goto MENU_RUTAS

:AGREGAR_PERM
cls
echo --- AGREGAR RUTA ESTATICA PERSISTENTE (-p) ---
echo NOTA: Esta ruta permanecera configurada incluso despues de reiniciar Windows.
echo.
set /p RED="Direccion de Red Destino (ej. 10.0.0.0): "
set /p MASCARA="Mascara de Subred (ej. 255.0.0.0): "
set /p GW="Siguiente Salto / Gateway (ej. 192.168.1.1): "

echo.
echo Ejecutando: route -p add %RED% mask %MASCARA% %GW%
route -p add %RED% mask %MASCARA% %GW%
if %ERRORLEVEL% EQU 0 (
    echo [OK] Ruta persistente registrada en el registro de Windows.
) else (
    echo [ERROR] No se pudo agregar la ruta persistente. Requiere privilegios de Administrador.
)
echo.
pause
goto MENU_RUTAS

:ELIMINAR_RUTA
cls
echo --- ELIMINAR RUTA ESTATICA ---
set /p RED="Ingrese la Red Destino a eliminar (ej. 10.0.0.0): "
echo.
echo Ejecutando: route delete %RED%
route delete %RED%
if %ERRORLEVEL% EQU 0 (
    echo [OK] Ruta eliminada exitosamente.
) else (
    echo [ERROR] Fallo al eliminar la ruta o la ruta no existia.
)
echo.
pause
goto MENU_RUTAS

:TEST_GATEWAY
cls
echo --- PROBAR CONECTIVIDAD HACIA GATEWAY / NEXT-HOP ---
set /p GW_TEST="Ingrese la direccion IP del Gateway o Host: "
echo.
ping -n 4 %GW_TEST%
echo.
pause
goto MENU_RUTAS
