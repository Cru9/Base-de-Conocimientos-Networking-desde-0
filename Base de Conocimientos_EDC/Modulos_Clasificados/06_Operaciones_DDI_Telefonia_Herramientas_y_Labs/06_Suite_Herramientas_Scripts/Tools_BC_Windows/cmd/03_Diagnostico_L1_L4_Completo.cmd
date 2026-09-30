@echo off
chcp 65001 >nul
title BC NETWORK - DIAGNOSTICO INTEGRAL POR CAPAS OSI (L1 A L4)
color 0A

cls
echo ===============================================================================
echo            BC NETWORK TOOLKIT - DIAGNOSTICO COMPLETO CAPAS OSI (L1-L4)
echo ===============================================================================
echo.

echo [CAPA 1 - FISICA] Estado de Cable, Velocidad de Enlace y Duplex:
powershell -Command "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | Select-Object Name, LinkSpeed, Status, FullDuplex, MediaConnectionState | Format-Table -AutoSize"

echo [CAPA 2 - ENLACE DE DATOS] Direcciones MAC y Tamano MTU:
powershell -Command "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | Select-Object Name, MacAddress, MtuSize | Format-Table -AutoSize"

echo [CAPA 3 - RED] Direccionamiento IPv4, Gateway y Metricas de Ruta:
powershell -Command "Get-NetIPConfiguration | Where-Object { $_.IPv4Address } | ForEach-Object { [PSCustomObject]@{ Interfaz = $_.InterfaceAlias; IPv4 = ($_.IPv4Address.IPAddress -join ', '); Mascara = ($_.IPv4Address.PrefixLength -join ', '); Gateway = ($_.IPv4DefaultGateway.NextHop -join ', ') } } | Format-Table -AutoSize"

echo [CAPA 4 - TRANSPORTE] Resumen de Sockets TCP en Escucha (Listening) y Sockets Activos:
powershell -Command "$escucha = (Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue).Count; $estab = (Get-NetTCPConnection -State Established -ErrorAction SilentlyContinue).Count; Write-Host ('Sockets TCP en Escucha (Listen): {0} | Sockets Establecidos: {1}' -f $escucha, $estab) -ForegroundColor Cyan"

echo.
echo [PRUEBA DE CONECTIVIDAD END-TO-END]
powershell -Command "$gw = (Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue).NextHop; if ($gw) { $p1 = Test-Connection $gw -Count 1 -Quiet; Write-Host ('Salto 1 (Gateway {0}): {1}' -f $gw, ($p1 ? '[OK]' : '[FALLO]')) -ForegroundColor ($p1 ? 'Green' : 'Red') }; $p2 = Test-Connection 8.8.8.8 -Count 1 -Quiet; Write-Host ('Salto 2 (Internet IP 8.8.8.8): {0}' -f ($p2 ? '[OK]' : '[FALLO]')) -ForegroundColor ($p2 ? 'Green' : 'Red'); $p3 = Test-Connection google.com -Count 1 -Quiet; Write-Host ('Salto 3 (Resolucion DNS google.com): {0}' -f ($p3 ? '[OK]' : '[FALLO]')) -ForegroundColor ($p3 ? 'Green' : 'Red')"

echo.
echo ===============================================================================
echo Diagnostico finalizado.
echo ===============================================================================
echo.
pause
