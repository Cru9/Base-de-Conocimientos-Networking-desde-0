@echo off
chcp 65001 >nul
title BC NETWORK - DIAGNOSTICO VELOZ DE CONECTIVIDAD
color 0E

cls
echo ===============================================================================
echo            BC NETWORK TOOLKIT - DIAGNOSTICO RAPIDO DE CONECTIVIDAD
echo ===============================================================================
echo.
echo [*] Obteniendo resumen de adaptadores activos e IP local...
powershell -Command "Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notmatch 'Loopback' -and $_.IPAddress -ne '127.0.0.1' } | Select-Object InterfaceAlias, IPAddress, PrefixLength | Format-Table -AutoSize"

echo [*] Identificando Gateway Predeterminado...
powershell -Command "$gw = (Get-NetRoute -DestinationPrefix '0.0.0.0/0').NextHop; Write-Host 'Gateway IPv4 detectado:' $gw -ForegroundColor Cyan; if ($gw) { Test-Connection -ComputerName $gw -Count 2 -Quiet | ForEach-Object { if ($_) { Write-Host '[OK] Gateway responde a ICMP' -ForegroundColor Green } else { Write-Host '[ALERTA] Gateway NO responde a ICMP' -ForegroundColor Red } } }"

echo.
echo [*] Probando resolucion de nombres DNS (Google y Cloudflare)...
powershell -Command "$sw = [System.Diagnostics.Stopwatch]::StartNew(); try { [System.Net.Dns]::GetHostAddresses('one.one.one.one') | Out-Null; $sw.Stop(); Write-Host ('[OK] DNS Resolvio en {0} ms' -f $sw.ElapsedMilliseconds) -ForegroundColor Green } catch { Write-Host '[ERROR] Fallo en la resolucion DNS' -ForegroundColor Red }"

echo.
echo [*] Verificando salida a Internet e IP Publica...
powershell -Command "try { $ip = (Invoke-RestMethod -Uri 'https://api.ipify.org' -TimeoutSec 3); Write-Host '[OK] IP Publica WAN:' $ip -ForegroundColor Green } catch { Write-Host '[ALERTA] No se pudo obtener IP publica (sin conexion WAN o bloqueo)' -ForegroundColor Yellow }"

echo.
echo ===============================================================================
echo Diagnostico concluido.
echo ===============================================================================
echo.
pause
