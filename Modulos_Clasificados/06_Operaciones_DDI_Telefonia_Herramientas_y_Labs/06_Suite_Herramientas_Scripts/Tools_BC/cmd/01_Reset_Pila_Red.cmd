@echo off
chcp 65001 >nul
title BC NETWORK - REINICIO Y LIMPIEZA DE PILA DE RED TCP/IP
color 0C

echo ===============================================================================
echo            BC NETWORK TOOLKIT - LIMPIEZA Y REINICIO DE RED TCP/IP
echo ===============================================================================
echo.
echo  Este script ejecuta un restablecimiento profundo de los componentes de red:
echo   - Vaciado de cache DNS local (ipconfig /flushdns)
echo   - Limpieza de nombres NetBIOS (nbtstat -R)
echo   - Purga de la tabla ARP local (arp -d *)
echo   - Liberacion y renovacion de concesiones DHCP (release/renew)
echo   - Reinicio del catalogo de sockets Winsock (netsh winsock reset)
echo   - Reinicio de la pila TCP/IP a valores predeterminados (netsh int ip reset)
echo.
echo ===============================================================================
echo [!] ADVERTENCIA: Se recomienda ejecutar esta herramienta como ADMINISTRADOR.
echo ===============================================================================
echo.

set /p CONFIRMAR="¿Desea proceder con la reparacion de red? (S/N): "
if /I not "%CONFIRMAR%"=="S" (
    echo Operación cancelada por el usuario.
    timeout /t 2 >nul
    exit /b
)

echo.
echo [*] 1/6 Vaciando cache de resolucion DNS...
ipconfig /flushdns
echo [OK] Cache DNS limpia.

echo.
echo [*] 2/6 Purgando nombres NetBIOS...
nbtstat -R >nul 2>&1
echo [OK] Nombres NetBIOS actualizados.

echo.
echo [*] 3/6 Limpiando tabla de resolucion ARP...
arp -d * >nul 2>&1
echo [OK] Tabla ARP purgada.

echo.
echo [*] 4/6 Liberando concesion DHCP actual...
ipconfig /release >nul 2>&1
echo [*] Renovando direccion IP desde DHCP...
ipconfig /renew
echo [OK] Direccion IP renovada exitosamente.

echo.
echo [*] 5/6 Restableciendo catalogo Winsock de Windows...
netsh winsock reset
echo [OK] Winsock restablecido.

echo.
echo [*] 6/6 Restableciendo pila TCP/IP de Windows...
netsh int ip reset
echo [OK] Pila IP restablecida.

echo.
echo ===============================================================================
echo [EXITO] Reparacion de red finalizada.
echo NOTA: Para que todos los cambios de Winsock e IP tomen efecto completo,
echo       se recomienda reiniciar el equipo si los problemas persisten.
echo ===============================================================================
echo.
pause
