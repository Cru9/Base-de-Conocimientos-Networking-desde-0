@echo off
chcp 65001 >nul
title BC CYBERSECURITY - HARDENING DE RED WINDOWS (CIERRE DE PROTOCOLOS LEGADOS)
color 0C

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [i] Solicitando elevacion de permisos para aplicar politicas de seguridad...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

:MENU_HARDENING
cls
echo ===============================================================================
echo            BC CYBERSECURITY - HARDENING DE PROTOCOLOS DE RED (WINDOWS)
echo ===============================================================================
echo.
echo  Este modulo mitiga vectores criticos de ataque en redes LAN corporativas:
echo   - SMBv1: Vector de propagacion de Ransomware (WannaCry, EternalBlue).
echo   - LLMNR: Vector de envenenamiento y robo de hashes NTLM (Responder / MITM).
echo   - NetBIOS: Difusion innecesaria de nombres en capa de difusion.
echo   - WPAD: Deteccion automatica de proxy vulnerable a secuestro.
echo.
echo  --- ACCIONES DISPONIBLES ---
echo   [1] Auditar estado actual de los protocolos inseguros
echo   [2] Aplicar HARDENING COMPLETO (Deshabilitar SMBv1, LLMNR, NetBIOS y WPAD)
echo   [3] Deshabilitar solo SMBv1
echo   [4] Deshabilitar solo LLMNR (Mitigacion de Responder)
echo   [5] Deshabilitar solo NetBIOS sobre TCP/IP en todos los adaptadores
echo   [6] Revertir cambios a valores predeterminados de Windows
echo.
echo   [0] Salir
echo ===============================================================================
set /p OPT="Seleccione una opcion [0-6]: "

if "%OPT%"=="1" goto AUDITAR
if "%OPT%"=="2" goto APLICAR_TODO
if "%OPT%"=="3" goto DES_SMB
if "%OPT%"=="4" goto DES_LLMNR
if "%OPT%"=="5" goto DES_NETBIOS
if "%OPT%"=="6" goto REVERTIR
if "%OPT%"=="0" exit /b

echo [!] Opcion invalida.
timeout /t 2 >nul
goto MENU_HARDENING

:AUDITAR
cls
echo --- AUDITORIA DE PROTOCOLOS LEGADOS ---
echo.
echo [*] Estado de SMBv1:
powershell -Command "try { $smb = (Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -ErrorAction SilentlyContinue).State; Write-Host 'SMB1 Feature:' $smb } catch { Write-Host 'No disponible' }"

echo.
echo [*] Estado de LLMNR en Registro:
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" /v EnableMulticast 2>nul
if %errorLevel% neq 0 (
    echo [ALERTA] LLMNR esta HABILITADO por defecto (Vulnerable a envenenamiento NTLM).
) else (
    echo [OK] LLMNR tiene directiva configurada.
)

echo.
echo [*] Estado de NetBIOS sobre TCP/IP en adaptadores:
powershell -Command "Get-CimInstance Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled } | Select-Object Description, TcpipNetbiosOptions | Format-Table -AutoSize"
echo (0 = Predeterminado por DHCP, 1 = Habilitado, 2 = Deshabilitado)
echo.
pause
goto MENU_HARDENING

:APLICAR_TODO
cls
echo [*] 1/4 Deshabilitando protocolo SMBv1...
powershell -Command "Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart -ErrorAction SilentlyContinue | Out-Null; Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force -ErrorAction SilentlyContinue"
echo [OK] SMBv1 desactivado.

echo [*] 2/4 Deshabilitando LLMNR (Mitigacion de robo de credenciales)...
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" /v EnableMulticast /t REG_DWORD /d 0 /f >nul
echo [OK] LLMNR desactivado en directiva de DNS Client.

echo [*] 3/4 Deshabilitando NetBIOS sobre TCP/IP en adaptadores activos...
powershell -Command "Get-CimInstance Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled } | ForEach-Object { $_.SetTcpipNetbios(2) | Out-Null }"
echo [OK] NetBIOS sobre TCP/IP desactivado (Opcion 2).

echo [*] 4/4 Desactivando WPAD (Web Proxy Auto-Discovery)...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v AutoDetect /t REG_DWORD /d 0 /f >nul
echo [OK] WPAD desactivado.

echo.
echo ===============================================================================
echo [EXITO] Hardening de red aplicado. Su equipo ahora es mucho mas resistente a
echo         ataques de broadcast, envenenamiento y propagacion de malware lateral.
echo ===============================================================================
echo.
pause
goto MENU_HARDENING

:DES_SMB
powershell -Command "Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force"
echo [OK] SMBv1 deshabilitado.
pause
goto MENU_HARDENING

:DES_LLMNR
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" /v EnableMulticast /t REG_DWORD /d 0 /f >nul
echo [OK] LLMNR deshabilitado.
pause
goto MENU_HARDENING

:DES_NETBIOS
powershell -Command "Get-CimInstance Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled } | ForEach-Object { $_.SetTcpipNetbios(2) | Out-Null }"
echo [OK] NetBIOS desactivado en adaptadores.
pause
goto MENU_HARDENING

:REVERTIR
cls
echo [*] Re-habilitando politicas estandar...
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" /v EnableMulticast /f >nul 2>&1
powershell -Command "Get-CimInstance Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled } | ForEach-Object { $_.SetTcpipNetbios(0) | Out-Null }"
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v AutoDetect /t REG_DWORD /d 1 /f >nul 2>&1
echo [OK] Politicas revertidas a valores estandar.
pause
goto MENU_HARDENING
