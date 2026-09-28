<#
.SYNOPSIS
    Monitor en Vivo de Roaming Wi-Fi y Calidad de Radiofrecuencia.
.DESCRIPTION
    Monitorea continuamente la conexion del adaptador inalambrico en tiempo real.
    Detecta de inmediato cuando el dispositivo realiza Roaming entre Puntos de Acceso (BSSIDs),
    cambios de canal, fluctuaciones de RSSI en dBm y variacion de velocidades de enlace (Rx/Tx).
    Herramienta indispensable para Site Surveys y pruebas de movilidad (802.11k/v/r).
#>

param(
    [int]$PollingIntervalMs = 1000
)

Clear-Host
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "         MONITOR EN VIVO DE ROAMING WI-FI (SITE SURVEY)          " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

Write-Host "Inicializando monitor de interfaz inalambrica..." -ForegroundColor White
Write-Host "Presione [Ctrl + C] para detener el monitoreo en cualquier momento.`n" -ForegroundColor DarkGray

$PreviousBSSID = ""
$PreviousChannel = 0
$PreviousSSID = ""
$RoamCount = 0

function Get-WifiInterfaceData {
    $Raw = netsh wlan show interfaces
    $Data = @{
        State   = "Desconectado"
        SSID    = "N/A"
        BSSID   = "N/A"
        Radio   = "N/A"
        Channel = 0
        Signal  = 0
        Dbm     = 0
        RxRate  = 0
        TxRate  = 0
    }

    foreach ($Line in $Raw) {
        $T = $Line.Trim()
        if ($T -match "^Estado\s+:\s*(.*)$" -or $T -match "^State\s+:\s*(.*)$") { $Data.State = $Matches[1] }
        elseif ($T -match "^SSID\s+:\s*(.*)$") { $Data.SSID = $Matches[1] }
        elseif ($T -match "^BSSID\s+:\s*(.*)$") { $Data.BSSID = $Matches[1] }
        elseif ($T -match "^Tipo de radio\s+:\s*(.*)$" -or $T -match "^Radio type\s+:\s*(.*)$") { $Data.Radio = $Matches[1] }
        elseif ($T -match "^Canal\s+:\s*(\d+)$" -or $T -match "^Channel\s+:\s*(\d+)$") { $Data.Channel = [int]$Matches[1] }
        elseif ($T -match "^Se[nñ]al\s+:\s*(\d+)%$" -or $T -match "^Signal\s+:\s*(\d+)%$") { 
            $Data.Signal = [int]$Matches[1]
            $Data.Dbm = [math]::Round(($Data.Signal / 2) - 100)
        }
        elseif ($T -match "^Velocidad de recepci[oó]n\s+:\s*(\d+)" -or $T -match "^Receive rate\s+:\s*(\d+)") { $Data.RxRate = [int]$Matches[1] }
        elseif ($T -match "^Velocidad de transmisi[oó]n\s+:\s*(\d+)" -or $T -match "^Transmit rate\s+:\s*(\d+)") { $Data.TxRate = [int]$Matches[1] }
    }
    return $Data
}

try {
    while ($true) {
        $Info = Get-WifiInterfaceData
        $Time = Get-Date -Format "HH:mm:ss"

        if ($Info.State -notmatch "conectado" -and $Info.State -notmatch "connected") {
            Write-Host "[$Time] ADVERTENCIA: Interfaz Wi-Fi desconectada o buscando red..." -ForegroundColor Red
        } else {
            # Verificar si ocurrio un Roaming (cambio de AP BSSID)
            if ($PreviousBSSID -ne "" -and $Info.BSSID -ne "" -and $Info.BSSID -ne $PreviousBSSID) {
                $RoamCount++
                [Console]::Beep(1800, 250)
                Write-Host "`n*****************************************************************" -ForegroundColor Yellow
                Write-Host "[$Time] ¡EVENTO DE ROAMING DETECTADO! (#$RoamCount)" -ForegroundColor Green
                Write-Host "AP Anterior : $PreviousBSSID (Canal $PreviousChannel)" -ForegroundColor Gray
                Write-Host "Nuevo AP    : $($Info.BSSID) (Canal $($Info.Channel))" -ForegroundColor Cyan
                Write-Host "Nueva Senal : $($Info.Dbm) dBm ($($Info.Signal)%) | Estandar: $($Info.Radio)" -ForegroundColor Yellow
                Write-Host "*****************************************************************`n" -ForegroundColor Yellow
            }

            # Actualizar estado previo
            $PreviousBSSID = $Info.BSSID
            $PreviousChannel = $Info.Channel
            $PreviousSSID = $Info.SSID

            # Linea de estado continuo
            $SigColor = "Green"
            if ($Info.Dbm -lt -70) { $SigColor = "Yellow" }
            if ($Info.Dbm -lt -80) { $SigColor = "Red" }

            $StatusLine = "[$Time] SSID: $($Info.SSID) | BSSID: $($Info.BSSID) | Ch: $($Info.Channel) | RSSI: $($Info.Dbm) dBm ($($Info.Signal)%) | Rx/Tx: $($Info.RxRate)/$($Info.TxRate) Mbps"
            Write-Host $StatusLine -ForegroundColor $SigColor
        }

        Start-Sleep -Milliseconds $PollingIntervalMs
    }
} finally {
    Write-Host "`n=================================================================" -ForegroundColor Cyan
    Write-Host "                     FIN DEL MONITOREO                          " -ForegroundColor Yellow
    Write-Host "Total de eventos de Roaming registrados durante la prueba: $RoamCount" -ForegroundColor White
    Write-Host "=================================================================`n" -ForegroundColor Cyan
}
