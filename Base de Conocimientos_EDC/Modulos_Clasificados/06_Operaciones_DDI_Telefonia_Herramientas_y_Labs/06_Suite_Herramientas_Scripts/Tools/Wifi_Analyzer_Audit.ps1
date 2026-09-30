<#
.SYNOPSIS
    Wifi Analyzer & Auditor: Escaneo y auditoria de radiofrecuencia y seguridad Wi-Fi en Windows.
.DESCRIPTION
    Extrae informacion en tiempo real de todos los puntos de acceso y redes al alcance
    usando la API nativa de Windows (netsh wlan). Calcula dBm, canal, banda, tipo de radio
    y nivel de seguridad criptografica.
#>

Clear-Host
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "             AUDITOR Y ANALIZADOR WI-FI PARA WINDOWS            " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

Write-Host "Escaneando el espectro electromagnetico... Espere un momento.`n" -ForegroundColor DarkGray

$RawOutput = netsh wlan show networks mode=bssid

if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($RawOutput)) {
    Write-Host "[ERROR] No se pudo obtener informacion del adaptador inalambrico." -ForegroundColor Red
    Write-Host "Asegurese de tener un adaptador Wi-Fi encendido y habilitado." -ForegroundColor Yellow
    return
}

$Networks = [System.Collections.Generic.List[PSCustomObject]]::new()

$CurrentSSID = ""
$CurrentAuth = ""
$CurrentCipher = ""
$CurrentBSSID = ""
$CurrentSignal = 0
$CurrentRadio = ""
$CurrentChannel = 0

foreach ($Line in $RawOutput) {
    $Trimmed = $Line.Trim()

    if ($Trimmed -match "^SSID\s+\d+\s+:\s*(.*)$") {
        $CurrentSSID = $Matches[1]
        if ([string]::IsNullOrWhiteSpace($CurrentSSID)) { $CurrentSSID = "[SSID OCULTO / HIDDEN]" }
    }
    elseif ($Trimmed -match "^Autenticaci[oó]n\s+:\s*(.*)$" -or $Trimmed -match "^Authentication\s+:\s*(.*)$") {
        $CurrentAuth = $Matches[1].Trim()
    }
    elseif ($Trimmed -match "^Cifrado\s+:\s*(.*)$" -or $Trimmed -match "^Encryption\s+:\s*(.*)$") {
        $CurrentCipher = $Matches[1].Trim()
    }
    elseif ($Trimmed -match "^BSSID\s+\d+\s+:\s*(.*)$") {
        $CurrentBSSID = $Matches[1].Trim()
    }
    elseif ($Trimmed -match "^Se[nñ]al\s+:\s*(\d+)%$" -or $Trimmed -match "^Signal\s+:\s*(\d+)%$") {
        $CurrentSignal = [int]$Matches[1]
    }
    elseif ($Trimmed -match "^Tipo de radio\s+:\s*(.*)$" -or $Trimmed -match "^Radio type\s+:\s*(.*)$") {
        $CurrentRadio = $Matches[1].Trim()
    }
    elseif ($Trimmed -match "^Canal\s+:\s*(\d+)$" -or $Trimmed -match "^Channel\s+:\s*(\d+)$") {
        $CurrentChannel = [int]$Matches[1]

        # Calcular dBm aproximado a partir del porcentaje de Windows
        # Formula estandar: dBm = (Porcentaje / 2) - 100
        $Dbm = [math]::Round(($CurrentSignal / 2) - 100)

        # Determinar banda de frecuencia
        $Band = "Desconocida"
        if ($CurrentChannel -ge 1 -and $CurrentChannel -le 14) {
            $Band = "2.4 GHz"
        } elseif ($CurrentChannel -ge 36 -and $CurrentChannel -le 177) {
            $Band = "5 GHz"
        } elseif ($CurrentChannel -gt 177) {
            $Band = "6 GHz (Wi-Fi 6E/7)"
        }

        # Evaluar calificacion de seguridad
        $RiskLevel = "SEGURO"
        if ($CurrentAuth -match "Open" -or $CurrentAuth -match "Abierta" -or $CurrentCipher -match "None") {
            $RiskLevel = "CRITICO (Sin Cifrado)"
        } elseif ($CurrentAuth -match "WEP" -or $CurrentCipher -match "TKIP") {
            $RiskLevel = "ALTO (Algoritmo Obsoleto)"
        } elseif ($CurrentAuth -match "WPA3") {
            $RiskLevel = "OPTIMO (WPA3 SAE)"
        }

        $Networks.Add([PSCustomObject]@{
            SSID        = $CurrentSSID
            BSSID       = $CurrentBSSID
            Canal       = $CurrentChannel
            Banda       = $Band
            Radio       = $CurrentRadio
            SenalPct    = "$CurrentSignal%"
            RSSI_dBm    = "${Dbm} dBm"
            Seguridad   = $CurrentAuth
            Cifrado     = $CurrentCipher
            Riesgo      = $RiskLevel
        })
    }
}

Write-Host "TOTAL DE PUNTOS DE ACCESO (BSSIDs) DETECTADOS: $($Networks.Count)`n" -ForegroundColor White

# Mostrar tabla formateada
$Networks | Sort-Object -Property @{Expression={[int]($_.RSSI_dBm -replace '[^\d-]', '')}; Descending=$true} | Format-Table -Property SSID, Canal, Banda, RSSI_dBm, SenalPct, Radio, Seguridad, Riesgo -AutoSize

Write-Host "`nANALISIS DE SATURACION DEL ESPECTRO (CANALES MAS UTILIZADOS):" -ForegroundColor Cyan
Write-Host "-----------------------------------------------------------------" -ForegroundColor DarkGray

$ChannelGroups = $Networks | Group-Object -Property Canal | Sort-Object Count -Descending
foreach ($Grp in $ChannelGroups) {
    $ChNum = [int]$Grp.Name
    $Count = $Grp.Count
    $Bar = "█" * $Count
    $Color = "Green"
    if ($Count -ge 5) { $Color = "Red" }
    elseif ($Count -ge 3) { $Color = "Yellow" }

    Write-Host ("Canal {0,3} [{1} redes] : {2}" -f $ChNum, $Count, $Bar) -ForegroundColor $Color
}

Write-Host "`nRECOMENDACIONES DE OPTIMIZACION DE RF:" -ForegroundColor Yellow
Write-Host "- En 2.4 GHz, asegurese de utilizar UNICAMENTE los canales 1, 6 u 11." -ForegroundColor White
Write-Host "- Para entornos de alta densidad, migre los clientes al espectro de 5 GHz / 6 GHz." -ForegroundColor White
Write-Host "- Un valor de RSSI inferior a -70 dBm provocara lentitud y caidas de conexion." -ForegroundColor White
Write-Host "=================================================================`n" -ForegroundColor Cyan
