<#
.SYNOPSIS
    SuperPing Continuo: Monitor avanzado de latencia, jitter y disponibilidad con marcas de tiempo.
.DESCRIPTION
    Realiza pings continuos a un host o IP objetivo, coloreando la salida segun los milisegundos
    de latencia, emitiendo alertas sonoras ante perdida de paquetes y registrando todo en un log CSV.
#>

param(
    [string]$Target = "",
    [int]$IntervalMs = 1000,
    [int]$TimeoutMs = 1500,
    [switch]$NoBeep,
    [switch]$LogToFile
)

Clear-Host
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "               SUPERPING CONTINUO PARA WINDOWS                  " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

if ([string]::IsNullOrWhiteSpace($Target)) {
    $Target = Read-Host "Ingrese la direccion IP o nombre de host a monitorear (Ej. 8.8.8.8 o gateway)"
    if ([string]::IsNullOrWhiteSpace($Target)) { $Target = "8.8.8.8" }
}

$LogPath = ""
if ($LogToFile -or (Read-Host "Desea guardar la salida en un archivo de log CSV? (s/n)") -eq "s") {
    $DateStr = Get-Date -Format "yyyyMMdd_HHmmss"
    $CleanTarget = $Target -replace "[:/\\]", "_"
    $LogPath = Join-Path -Path $PSScriptRoot -ChildPath "PingLog_${CleanTarget}_${DateStr}.csv"
    "Timestamp,Sequence,Target,IP,Status,Latency_ms,TTL" | Out-File -FilePath $LogPath -Encoding utf8
    Write-Host "[INFO] Registrando eventos en: $LogPath" -ForegroundColor Green
}

Write-Host "Monitoreando destino: $Target" -ForegroundColor White
Write-Host "Intervalo: ${IntervalMs}ms | Timeout: ${TimeoutMs}ms" -ForegroundColor DarkGray
Write-Host "Presione [Ctrl + C] en cualquier momento para detener y ver resumen estadistico.`n" -ForegroundColor DarkYellow

$Pinger = New-Object System.Net.NetworkInformation.Ping
$Seq = 0
$Sent = 0
$Received = 0
$Lost = 0
$Latencies = [System.Collections.Generic.List[int]]::new()

try {
    while ($true) {
        $Seq++
        $Sent++
        $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
        
        try {
            $Reply = $Pinger.Send($Target, $TimeoutMs)
            
            if ($Reply.Status -eq [System.Net.NetworkInformation.IPStatus]::Success) {
                $Received++
                $Ms = $Reply.RoundtripTime
                $Latencies.Add($Ms)
                $Ttl = $Reply.Options.Ttl
                $ResolvedIp = $Reply.Address.ToString()

                # Codigo de colores por severidad
                if ($Ms -lt 30) {
                    $Color = "Green"
                    $StatusTag = "[EXCELENTE]"
                } elseif ($Ms -le 80) {
                    $Color = "Yellow"
                    $StatusTag = "[ACEPTABLE]"
                } else {
                    $Color = "Magenta"
                    $StatusTag = "[LATENCIA ALTA]"
                }

                $Line = "[$Timestamp] #$Seq | Destino: $Target ($ResolvedIp) | Tiempo: ${Ms}ms | TTL: $Ttl | $StatusTag"
                Write-Host $Line -ForegroundColor $Color

                if ($LogPath) {
                    "$Timestamp,$Seq,$Target,$ResolvedIp,Success,$Ms,$Ttl" | Out-File -FilePath $LogPath -Append -Encoding utf8
                }
            } else {
                $Lost++
                Write-Host "[$Timestamp] #$Seq | Destino: $Target | ERROR: $($Reply.Status) [PAQUETE PERDIDO]" -ForegroundColor Red
                if (-not $NoBeep) { [Console]::Beep(1200, 200) }

                if ($LogPath) {
                    "$Timestamp,$Seq,$Target,Unknown,$($Reply.Status),0,0" | Out-File -FilePath $LogPath -Append -Encoding utf8
                }
            }
        } catch {
            $Lost++
            Write-Host "[$Timestamp] #$Seq | Destino: $Target | EXCEPCION: $($_.Exception.Message) [FALLO DE RED]" -ForegroundColor Red
            if (-not $NoBeep) { [Console]::Beep(800, 300) }

            if ($LogPath) {
                "$Timestamp,$Seq,$Target,Unknown,Exception,0,0" | Out-File -FilePath $LogPath -Append -Encoding utf8
            }
        }

        Start-Sleep -Milliseconds $IntervalMs
    }
} finally {
    Write-Host "`n=================================================================" -ForegroundColor Cyan
    Write-Host "                    RESUMEN ESTADISTICO                         " -ForegroundColor Yellow
    Write-Host "=================================================================" -ForegroundColor Cyan
    $LossPercent = if ($Sent -gt 0) { [math]::Round(($Lost / $Sent) * 100, 2) } else { 0 }
    
    Write-Host "Paquetes transmitidos : $Sent" -ForegroundColor White
    Write-Host "Paquetes recibidos    : $Received" -ForegroundColor Green
    Write-Host "Paquetes perdidos     : $Lost ($LossPercent%)" -ForegroundColor $(if ($Lost -gt 0) { "Red" } else { "Green" })

    if ($Latencies.Count -gt 0) {
        $Min = ($Latencies | Measure-Object -Minimum).Minimum
        $Max = ($Latencies | Measure-Object -Maximum).Maximum
        $Avg = [math]::Round(($Latencies | Measure-Object -Average).Average, 2)

        # Calculo de Jitter promedio (variacion sucesiva de latencias)
        $JitterSum = 0
        for ($i = 1; $i -lt $Latencies.Count; $i++) {
            $JitterSum += [math]::Abs($Latencies[$i] - $Latencies[$i - 1])
        }
        $AvgJitter = if ($Latencies.Count -gt 1) { [math]::Round($JitterSum / ($Latencies.Count - 1), 2) } else { 0 }

        Write-Host "Latencia Minima       : ${Min}ms" -ForegroundColor Cyan
        Write-Host "Latencia Maxima       : ${Max}ms" -ForegroundColor Cyan
        Write-Host "Latencia Promedio     : ${Avg}ms" -ForegroundColor Yellow
        Write-Host "Jitter Estimado       : ${AvgJitter}ms" -ForegroundColor $(if ($AvgJitter -lt 20) { "Green" } else { "Yellow" })
    }

    if ($LogPath) {
        Write-Host "`nInforme detallado guardado exitosamente en: $LogPath" -ForegroundColor Green
    }
    Write-Host "=================================================================`n" -ForegroundColor Cyan
}
