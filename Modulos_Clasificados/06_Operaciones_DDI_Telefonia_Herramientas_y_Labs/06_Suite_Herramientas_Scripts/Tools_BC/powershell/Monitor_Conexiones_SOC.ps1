<#
.SYNOPSIS
    Monitor de Conexiones Activas de Red para Analistas SOC y Troubleshooting.
.DESCRIPTION
    Inspecciona en tiempo real las conexiones TCP establecidas (Established/SynSent),
    identifica el proceso que origino la conexion (Nombre, PID, Ruta), clasifica el destino
    (Privado RFC 1918 / Publico Internet) y audita puertos sospechosos frecuentemente
    utilizados en balizas C2, Reverse Shells o exfiltracion.
.NOTES
    Modulo: Ciberseguridad_OSI / Troubleshooting
    Autor: Cru9 - BC Compendium
#>

[CmdletBinding()]
param(
    [int]$IntervaloRefrescoSegundos = 3
)

$PuertosSospechosos = @(4444, 5555, 1337, 31337, 6667, 9001, 8888, 1234, 4443)

function Es-IPPublica ([string]$ip) {
    if ([string]::IsNullOrWhiteSpace($ip)) { return $false }
    if ($ip -match '^127\.' -or $ip -match '^10\.' -or $ip -match '^172\.(1[6-9]|2[0-9]|3[0-1])\.' -or $ip -match '^192\.168\.' -or $ip -eq '::1' -or $ip -eq '0.0.0.0') {
        return $false
    }
    return $true
}

Clear-Host
Write-Host "Iniciando monitor SOC de sockets de red... Presione [Ctrl+C] para detener." -ForegroundColor Cyan
Start-Sleep -Seconds 1

try {
    while ($true) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $conexiones = Get-NetTCPConnection -State Established, SynSent -ErrorAction SilentlyContinue

        $resultados = foreach ($c in $conexiones) {
            $proc = Get-Process -Id $c.OwningProcess -ErrorAction SilentlyContinue
            $procNombre = if ($proc) { $proc.ProcessName } else { "Desconocido (PID: $($c.OwningProcess))" }
            $esPublica = Es-IPPublica $c.RemoteAddress
            $esRiesgoso = $PuertosSospechosos -contains $c.RemotePort

            $alerta = "Normal"
            if ($esRiesgoso) {
                $alerta = "[ALERTA: Puerto C2 / Sospechoso]"
            } elseif ($esPublica -and ($c.RemotePort -notin @(80, 443, 8080, 8443, 53))) {
                $alerta = "[Inusual: Puerto Publico]"
            }

            [PSCustomObject]@{
                Hora          = $timestamp
                Proceso       = $procNombre
                PID           = $c.OwningProcess
                IP_Local      = "$($c.LocalAddress):$($c.LocalPort)"
                IP_Remota     = "$($c.RemoteAddress):$($c.RemotePort)"
                Tipo_Destino  = if ($esPublica) { "Internet WAN" } else { "LAN / Privada" }
                Estado        = $c.State
                Auditoria_SOC = $alerta
            }
        }

        Clear-Host
        Write-Host "===============================================================================" -ForegroundColor Cyan
        Write-Host "       BC CYBERSECURITY - MONITOR EN VIVO DE SOCKETS TCP / SOC ($timestamp)" -ForegroundColor White
        Write-Host "===============================================================================" -ForegroundColor Cyan
        Write-Host "Conexiones activas analizadas: $($resultados.Count)" -ForegroundColor Gray
        Write-Host "Presione [Ctrl+C] para detener el monitoreo continuo.`n" -ForegroundColor DarkGray

        # Separar alertas de las normales
        $alertas = $resultados | Where-Object { $_.Auditoria_SOC -ne "Normal" }
        if ($alertas) {
            Write-Host ">>> ACTIVIDAD SOSPECHOSA O INUSUAL DETECTADA <<<" -ForegroundColor Red
            $alertas | Format-Table Proceso, PID, IP_Remota, Tipo_Destino, Auditoria_SOC -AutoSize
            Write-Host ""
        }

        Write-Host "--- Conexiones Activas Establecidas (Muestra de las ultimas 15) ---" -ForegroundColor Yellow
        $resultados | Select-Object -First 15 | Format-Table Proceso, PID, IP_Local, IP_Remota, Tipo_Destino, Estado -AutoSize

        Start-Sleep -Seconds $IntervaloRefrescoSegundos
    }
} finally {
    Write-Host "`nMonitor finalizado." -ForegroundColor Cyan
}
