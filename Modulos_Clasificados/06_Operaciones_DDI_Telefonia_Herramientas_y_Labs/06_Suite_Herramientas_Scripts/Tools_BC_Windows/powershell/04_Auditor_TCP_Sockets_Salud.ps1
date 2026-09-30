<#
.SYNOPSIS
    Auditor de Salud de Capa 4 (Transporte TCP/UDP) y Fugas de Sockets.
.DESCRIPTION
    Inspecciona todos los sockets TCP del sistema, clasifica por estados (Established,
    Listen, TimeWait, CloseWait), detecta procesos que consumen excesivas conexiones
    y alerta sobre fugas de sockets (CloseWait excesivos) que pueden agotar el pool de puertos efimeros.
.NOTES
    Modulo: Troubleshooting / Ciberseguridad_OSI
    Autor: Cru9 - BC Compendium
#>

Clear-Host
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       BC NETWORK - AUDITOR DE SALUD DE CAPA 4 (SOCKETS Y PILA TCP/UDP)" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[*] Muestreando sockets TCP del sistema operativo..." -ForegroundColor Gray
$conexiones = Get-NetTCPConnection -ErrorAction SilentlyContinue

if (-not $conexiones) {
    Write-Host "[ERROR] No se pudo consultar la tabla de sockets TCP." -ForegroundColor Red
    return
}

# Conteo por Estado
$estados = $conexiones | Group-Object State | Select-Object Name, Count

Write-Host "--- DISTRIBUCION DE SOCKETS POR ESTADO TCP ---" -ForegroundColor Yellow
$estados | Format-Table Name, Count -AutoSize

# Deteccion de anomalias en estados de conexion
$closeWaitCount = ($conexiones | Where-Object { $_.State -eq 'CloseWait' }).Count
$timeWaitCount  = ($conexiones | Where-Object { $_.State -eq 'TimeWait' }).Count

if ($closeWaitCount -gt 50) {
    Write-Host "[ALERTA] Se detectaron $closeWaitCount conexiones en estado 'CloseWait'!" -ForegroundColor Red
    Write-Host "         Significado: La aplicacion local no cerro correctamente el socket tras recibir FIN remoto." -ForegroundColor Yellow
    Write-Host "         Riesgo: Posible fuga de descriptores de socket (Socket Leak)." -ForegroundColor Yellow
} else {
    Write-Host "[OK] Conexiones CloseWait en rango saludable ($closeWaitCount)." -ForegroundColor Green
}

Write-Host "`n--- TOP 5 PROCESOS CON MAYOR NUMERO DE SOCKETS TCP ACTIVOS ---" -ForegroundColor Yellow
$procesosTop = $conexiones | Group-Object OwningProcess | Sort-Object Count -Descending | Select-Object -First 5

$reporteProc = foreach ($p in $procesosTop) {
    $procObj = Get-Process -Id $p.Name -ErrorAction SilentlyContinue
    $nombre = if ($procObj) { $procObj.ProcessName } else { "Sistema / Terminado" }
    $memoriaMB = if ($procObj) { [math]::Round($procObj.WorkingSet64 / 1MB, 1) } else { 0 }

    [PSCustomObject]@{
        PID              = $p.Name
        Nombre_Proceso   = $nombre
        Sockets_Abiertos = $p.Count
        Memoria_MB       = $memoriaMB
    }
}
$reporteProc | Format-Table -AutoSize

Write-Host "--- PUERTOS LOCALES EN ESCUCHA (SERVICIOS LISTEN ACTIVOS) ---" -ForegroundColor Yellow
$listenSockets = $conexiones | Where-Object { $_.State -eq 'Listen' } | Select-Object -First 10

$reporteListen = foreach ($l in $listenSockets) {
    $procObj = Get-Process -Id $l.OwningProcess -ErrorAction SilentlyContinue
    $nombre = if ($procObj) { $procObj.ProcessName } else { "PID $($l.OwningProcess)" }

    [PSCustomObject]@{
        Puerto_Local = $l.LocalPort
        Direccion_IP = $l.LocalAddress
        Proceso      = $nombre
        PID          = $l.OwningProcess
    }
}
$reporteListen | Format-Table -AutoSize

Write-Host "Presione una tecla para continuar..." -ForegroundColor Gray
[System.Console]::ReadKey() | Out-Null
