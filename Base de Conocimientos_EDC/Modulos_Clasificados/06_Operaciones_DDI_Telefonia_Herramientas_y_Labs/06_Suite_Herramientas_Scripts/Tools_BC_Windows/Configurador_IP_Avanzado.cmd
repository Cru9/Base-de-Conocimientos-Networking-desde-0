@echo off
chcp 65001 >nul
title BC NETWORK - CONFIGURADOR MAESTRO DE IP, MASCARA, GATEWAY Y DNS
color 0B

:: ===============================================================================
:: VERIFICACION Y ELEVACION DE PRIVILEGIOS (UAC)
:: Permite ejecutar a administradores y usuarios del grupo 'Operadores de configuracion de red'
:: ===============================================================================
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ===============================================================================
    echo [i] AVISO: La configuracion de adaptadores de red requiere permisos elevados.
    echo     Si usted es Usuario Avanzado / Administrador, confirme el aviso UAC.
    echo ===============================================================================
    echo.
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

:MENU_PRINCIPAL
cls
echo ===============================================================================
echo        BC NETWORK - CONFIGURADOR MAESTRO DE IP / MASCARA / GATEWAY / DNS
echo                           Windows Advanced Toolkit
echo ===============================================================================
echo.
echo   [1] Listar adaptadores de red y configuracion TCP/IP actual
echo   [2] Asignar IP ESTATICA (IP, Mascara/CIDR, Gateway y Servidores DNS)
echo   [3] Restablecer a DHCP (Obtener IP y DNS automaticamente)
echo   [4] Configurar solo Servidores DNS (Cloudflare, Google, Quad9 o Manual)
echo   [5] Agregar IP Secundaria adicional al adaptador (Multihoming L3)
echo   [6] Respaldar configuracion actual del adaptador a archivo
echo   [7] Restaurar configuracion desde un archivo de respaldo
echo   [8] Modificar MTU de la interfaz (ej. 1500, 1400 para VPN, 9000 Jumbo Frame)
echo   [9] Reiniciar adaptador de red (Deshabilitar y Habilitar interfaz)
echo   [10] Diagnostico de conectividad inmediata (Test de IP, Gateway e Internet)
echo.
echo   [0] Salir
echo ===============================================================================
set /p OPCION="Seleccione una opcion [0-10]: "

if "%OPCION%"=="1" goto LISTAR
if "%OPCION%"=="2" goto SET_ESTATICA
if "%OPCION%"=="3" goto SET_DHCP
if "%OPCION%"=="4" goto SET_DNS
if "%OPCION%"=="5" goto ADD_IP_SEC
if "%OPCION%"=="6" goto BACKUP_CFG
if "%OPCION%"=="7" goto RESTORE_CFG
if "%OPCION%"=="8" goto CAMBIAR_MTU
if "%OPCION%"=="9" goto RESTART_IFACE
if "%OPCION%"=="10" goto TEST_CONECTIVIDAD
if "%OPCION%"=="0" exit /b

echo [!] Opcion invalida.
timeout /t 2 >nul
goto MENU_PRINCIPAL

:: ===============================================================================
:: 1. LISTAR ADAPTADORES
:: ===============================================================================
:LISTAR
cls
echo ===============================================================================
echo                       ESTADO ACTUAL DE INTERFACES DE RED
echo ===============================================================================
echo.
powershell -Command "Get-NetIPConfiguration | ForEach-Object { [PSCustomObject]@{ Interfaz = $_.InterfaceAlias; Estado = $_.NetAdapter.Status; IPv4 = ($_.IPv4Address.IPAddress -join ', '); Mascara = ($_.IPv4Address.PrefixLength -join ', '); Gateway = ($_.IPv4DefaultGateway.NextHop -join ', '); DNS = ($_.DNSServer.ServerAddresses -join ', ') } } | Format-Table -AutoSize"
echo.
pause
goto MENU_PRINCIPAL

:: ===============================================================================
:: 2. ASIGNAR IP ESTATICA
:: ===============================================================================
:SET_ESTATICA
cls
echo ===============================================================================
echo                      CONFIGURACION DE DIRECCION IP ESTATICA
echo ===============================================================================
echo.
echo Adaptadores disponibles:
powershell -Command "Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, MacAddress | Format-Table -AutoSize"
echo.
set /p ADAPTADOR="Ingrese el Nombre EXACTO de la interfaz (ej. Ethernet, Wi-Fi): "
if "%ADAPTADOR%"=="" goto MENU_PRINCIPAL

set /p IP_ADDR="Direccion IP estatica (ej. 192.168.1.50): "
if "%IP_ADDR%"=="" goto MENU_PRINCIPAL

set /p MASCARA="Mascara de subred (ej. 255.255.255.0 o prefijo /24): "
if "%MASCARA%"=="" set MASCARA=255.255.255.0

:: Si el usuario escribio /24 o 24, convertir a mascara decimal
if "%MASCARA%"=="/24" set MASCARA=255.255.255.0
if "%MASCARA%"=="24" set MASCARA=255.255.255.0
if "%MASCARA%"=="/16" set MASCARA=255.255.0.0
if "%MASCARA%"=="16" set MASCARA=255.255.0.0
if "%MASCARA%"=="/8" set MASCARA=255.0.0.0
if "%MASCARA%"=="8" set MASCARA=255.0.0.0
if "%MASCARA%"=="/30" set MASCARA=255.255.255.252
if "%MASCARA%"=="30" set MASCARA=255.255.255.252
if "%MASCARA%"=="/29" set MASCARA=255.255.255.248
if "%MASCARA%"=="29" set MASCARA=255.255.255.248
if "%MASCARA%"=="/28" set MASCARA=255.255.255.240
if "%MASCARA%"=="28" set MASCARA=255.255.255.240

set /p GATEWAY="Gateway / Puerta de Enlace (ej. 192.168.1.1 o vacio): "
set /p DNS_PRI="Servidor DNS Primario (ej. 1.1.1.1 o 8.8.8.8): "
set /p DNS_SEC="Servidor DNS Secundario (ej. 1.0.0.1 o 8.8.4.4): "

echo.
echo [*] Aplicando direccion IP, Mascara y Gateway a '%ADAPTADOR%'...
if "%GATEWAY%"=="" (
    netsh interface ipv4 set address name="%ADAPTADOR%" source=static address=%IP_ADDR% mask=%MASCARA%
) else (
    netsh interface ipv4 set address name="%ADAPTADOR%" source=static address=%IP_ADDR% mask=%MASCARA% gateway=%GATEWAY% gwmetric=1
)

if %ERRORLEVEL% EQU 0 (
    echo [OK] Direccion IP y Gateway aplicados exitosamente.
) else (
    echo [ERROR] No se pudo asignar la IP. Verifique permisos y nombre del adaptador.
)

if not "%DNS_PRI%"=="" (
    echo [*] Configurando DNS Primario (%DNS_PRI%)...
    netsh interface ipv4 set dnsservers name="%ADAPTADOR%" source=static address=%DNS_PRI% register=primary validate=no
)

if not "%DNS_SEC%"=="" (
    echo [*] Configurando DNS Secundario (%DNS_SEC%)...
    netsh interface ipv4 add dnsservers name="%ADAPTADOR%" address=%DNS_SEC% index=2 validate=no
)

echo.
echo [EXITO] Parametros actualizados.
echo.
pause
goto MENU_PRINCIPAL

:: ===============================================================================
:: 3. RESTABLECER A DHCP
:: ===============================================================================
:SET_DHCP
cls
echo ===============================================================================
echo                     RESTABLECER ADAPTADOR A DHCP AUTOMATICO
echo ===============================================================================
echo.
powershell -Command "Get-NetAdapter | Select-Object Name, Status | Format-Table -AutoSize"
set /p ADAPTADOR="Ingrese el Nombre del adaptador (ej. Ethernet, Wi-Fi): "
if "%ADAPTADOR%"=="" goto MENU_PRINCIPAL

echo.
echo [*] Configurando direccion IP por DHCP...
netsh interface ipv4 set address name="%ADAPTADOR%" source=dhcp

echo [*] Configurando servidores DNS por DHCP...
netsh interface ipv4 set dnsservers name="%ADAPTADOR%" source=dhcp

echo [*] Renovando concesion de red...
ipconfig /renew "%ADAPTADOR%" >nul 2>&1

echo.
echo [OK] El adaptador '%ADAPTADOR%' ahora obtiene IP y DNS automaticamente por DHCP.
echo.
pause
goto MENU_PRINCIPAL

:: ===============================================================================
:: 4. CONFIGURAR SOLO SERVIDORES DNS
:: ===============================================================================
:SET_DNS
cls
echo ===============================================================================
echo                          CONFIGURACION DE SERVIDORES DNS
echo ===============================================================================
echo.
set /p ADAPTADOR="Ingrese el Nombre del adaptador: "
if "%ADAPTADOR%"=="" goto MENU_PRINCIPAL

echo.
echo Perfiles DNS recomendados:
echo   [1] Cloudflare (1.1.1.1 / 1.0.0.1) - Rapido y Privado
echo   [2] Google Public DNS (8.8.8.8 / 8.8.4.4)
echo   [3] Quad9 (9.9.9.9 / 149.112.112.112) - Filtro contra Malware
echo   [4] DNS Personalizado / Manual
echo   [5] Volver a DNS por DHCP
echo.
set /p OP_DNS="Seleccione una opcion [1-5]: "

if "%OP_DNS%"=="1" (
    netsh interface ipv4 set dnsservers name="%ADAPTADOR%" source=static address=1.1.1.1 register=primary validate=no
    netsh interface ipv4 add dnsservers name="%ADAPTADOR%" address=1.0.0.1 index=2 validate=no
    echo [OK] Cloudflare DNS aplicado.
)
if "%OP_DNS%"=="2" (
    netsh interface ipv4 set dnsservers name="%ADAPTADOR%" source=static address=8.8.8.8 register=primary validate=no
    netsh interface ipv4 add dnsservers name="%ADAPTADOR%" address=8.8.4.4 index=2 validate=no
    echo [OK] Google DNS aplicado.
)
if "%OP_DNS%"=="3" (
    netsh interface ipv4 set dnsservers name="%ADAPTADOR%" source=static address=9.9.9.9 register=primary validate=no
    netsh interface ipv4 add dnsservers name="%ADAPTADOR%" address=149.112.112.112 index=2 validate=no
    echo [OK] Quad9 DNS aplicado.
)
if "%OP_DNS%"=="4" (
    set /p D1="DNS Primario: "
    set /p D2="DNS Secundario: "
    netsh interface ipv4 set dnsservers name="%ADAPTADOR%" source=static address=%D1% register=primary validate=no
    if not "%D2%"=="" netsh interface ipv4 add dnsservers name="%ADAPTADOR%" address=%D2% index=2 validate=no
    echo [OK] DNS Manual aplicado.
)
if "%OP_DNS%"=="5" (
    netsh interface ipv4 set dnsservers name="%ADAPTADOR%" source=dhcp
    echo [OK] DNS por DHCP restablecido.
)

ipconfig /flushdns >nul 2>&1
echo [OK] Cache DNS purgada.
echo.
pause
goto MENU_PRINCIPAL

:: ===============================================================================
:: 5. AGREGAR IP SECUNDARIA
:: ===============================================================================
:ADD_IP_SEC
cls
echo ===============================================================================
echo                 AGREGAR IP SECUNDARIA (MULTIHOMING DE CAPA 3)
echo ===============================================================================
echo.
set /p ADAPTADOR="Nombre del adaptador: "
set /p IP_SEC="Segunda direccion IP a vincular: "
set /p MASC_SEC="Mascara de la segunda IP: "

echo.
echo [*] Agregando direccion secundaria...
netsh interface ipv4 add address name="%ADAPTADOR%" address=%IP_SEC% mask=%MASC_SEC%
if %ERRORLEVEL% EQU 0 (
    echo [OK] IP secundaria agregada con exito.
) else (
    echo [ERROR] No se pudo agregar la IP secundaria.
)
echo.
pause
goto MENU_PRINCIPAL

:: ===============================================================================
:: 6. RESPALDAR CONFIGURACION
:: ===============================================================================
:BACKUP_CFG
cls
echo ===============================================================================
echo                 RESPALDO DE CONFIGURACION ACTUAL DE RED
echo ===============================================================================
echo.
set ARCHIVO_BK="%~dp0backup_red_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%.txt"
set ARCHIVO_BK=%ARCHIVO_BK: =0%

echo [*] Guardando dump de configuracion en: %ARCHIVO_BK%
netsh interface ipv4 dump > %ARCHIVO_BK%
echo [OK] Respaldo guardado exitosamente.
echo.
pause
goto MENU_PRINCIPAL

:: ===============================================================================
:: 7. RESTAURAR CONFIGURACION
:: ===============================================================================
:RESTORE_CFG
cls
echo ===============================================================================
echo                RESTAURAR CONFIGURACION DESDE ARCHIVO DUMP
echo ===============================================================================
echo.
set /p RUTA_BK="Ingrese la ruta al archivo dump .txt de netsh: "
if exist "%RUTA_BK%" (
    echo [*] Restaurando configuracion de red...
    netsh exec "%RUTA_BK%"
    echo [OK] Configuracion restablecida.
) else (
    echo [ERROR] El archivo especificado no existe.
)
echo.
pause
goto MENU_PRINCIPAL

:: ===============================================================================
:: 8. CAMBIAR MTU DE INTERFAZ
:: ===============================================================================
:CAMBIAR_MTU
cls
echo ===============================================================================
echo                       MODIFICACION DE MTU EN INTERFAZ
echo ===============================================================================
echo.
set /p ADAPTADOR="Nombre de la interfaz: "
set /p VALOR_MTU="Nuevo valor MTU (ej. 1500 estandar, 1400/1420 VPN/PPPoE, 9000 Jumbo): "

echo.
echo [*] Aplicando MTU %VALOR_MTU% en '%ADAPTADOR%'...
netsh interface ipv4 set subinterface "%ADAPTADOR%" mtu=%VALOR_MTU% store=persistent
if %ERRORLEVEL% EQU 0 (
    echo [OK] MTU modificado y guardado de forma persistente.
) else (
    echo [ERROR] Fallo al modificar MTU.
)
echo.
pause
goto MENU_PRINCIPAL

:: ===============================================================================
:: 9. REINICIAR ADAPTADOR
:: ===============================================================================
:RESTART_IFACE
cls
echo ===============================================================================
echo                  REINICIAR ADAPTADOR DE RED (CYCLE INTERFACE)
echo ===============================================================================
echo.
set /p ADAPTADOR="Nombre del adaptador a reiniciar: "

echo [*] Deshabilitando '%ADAPTADOR%'...
powershell -Command "Disable-NetAdapter -Name '%ADAPTADOR%' -Confirm:$false"
timeout /t 2 >nul

echo [*] Habilitando '%ADAPTADOR%'...
powershell -Command "Enable-NetAdapter -Name '%ADAPTADOR%' -Confirm:$false"

echo [OK] Adaptador reiniciado.
echo.
pause
goto MENU_PRINCIPAL

:: ===============================================================================
:: 10. DIAGNOSTICO DE CONECTIVIDAD
:: ===============================================================================
:TEST_CONECTIVIDAD
cls
echo ===============================================================================
echo                       TEST DE CONECTIVIDAD INMEDIATO
echo ===============================================================================
echo.
echo [*] 1. Gateway Predeterminado:
powershell -Command "$gw = (Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue).NextHop; if ($gw) { Write-Host 'Gateway:' $gw; Test-Connection $gw -Count 2 } else { Write-Host 'No hay gateway predeterminado activo' -ForegroundColor Red }"

echo.
echo [*] 2. Resolucion DNS y Ping a Internet:
powershell -Command "Test-Connection 1.1.1.1 -Count 2; Test-Connection google.com -Count 2"

echo.
pause
goto MENU_PRINCIPAL
