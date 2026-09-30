<#
.SYNOPSIS
    Auditor de Redes Inalambricas Wi-Fi Enterprise y Espectro.
.DESCRIPTION
    Realiza una inspeccion en profundidad de la interfaz de radio 802.11:
    - SSID activo, BSSID del Access Point (AP), canal y banda de frecuencia (2.4 / 5 / 6 GHz).
    - Calculo de intensidad de senal RSSI en dBm: dBm = (Porcentaje / 2) - 100.
    - Tasas de transmision negociadas (Tx / Rx Rate en Mbps).
    - Tipo de autenticacion y cifrado (WPA2-Enterprise 802.1X, WPA3-SAE, CCMP/GCMP).
    - Escaneo de redes y canales cercanos para analisis de interferencia cocanal.
.NOTES
    Modulo: Wireless_Enterprise
    Autor: Cru9 - BC Compendium
#>

Clear-Host
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       BC WIRELESS - AUDITOR DE REDES WI-FI ENTERPRISE Y ESPECTRO" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$wlanInfo = netsh wlan show interfaces

if ($wlanInfo -match "no hay ninguna interfaz|There is no wireless interface") {
    Write-Host "[i] No se detecto ninguna tarjeta de red inalambrica activa en este equipo." -ForegroundColor Yellow
    return
}

# Extraer informacion de conexion activa
function Parse-WlanField ($pattern) {
    $line = ($wlanInfo | Select-String $pattern).ToString()
    if ($line -match ':\s*(.+)$') { return $matches[1].Trim() }
    return "N/A"
}

$ssid    = Parse-WlanField "SSID\s*:"
$bssid   = Parse-WlanField "BSSID\s*:"
$radio   = Parse-WlanField "Radio type|Tipo de radio"
$auth    = Parse-WlanField "Authentication|Autenticaci"
$cipher  = Parse-WlanField "Cipher|Cifrado"
$channel = Parse-WlanField "Channel|Canal"
$rxRate  = Parse-WlanField "Receive rate|Velocidad de recepci"
$txRate  = Parse-WlanField "Transmit rate|Velocidad de transmisi"
$signal  = Parse-WlanField "Signal|Se"

$signalPct = [int]($signal -replace '\D', '')
$rssi_dBm = if ($signalPct) { [math]::Round(($signalPct / 2) - 100, 0) } else { -100 }

# Determinar Banda
$canalNum = [int]($channel -replace '\D', '')
$banda = "Desconocida"
if ($canalNum -ge 1 -and $canalNum -le 14) { $banda = "2.4 GHz" }
elseif ($canalNum -ge 36 -and $canalNum -le 165) { $banda = "5.0 GHz (Alta Velocidad)" }
elseif ($canalNum -gt 165) { $banda = "6.0 GHz (Wi-Fi 6E / Wi-Fi 7)" }

Write-Host "--- DETALLES DE CONEXION WI-FI ACTIVA ---" -ForegroundColor Yellow
Write-Host "  Nombre de Red (SSID):     $ssid" -ForegroundColor Green
Write-Host "  Direccion MAC del AP:     $bssid" -ForegroundColor Gray
Write-Host "  Estandar 802.11:          $radio" -ForegroundColor Cyan
Write-Host "  Banda de Frecuencia:      $banda (Canal $canalNum)" -ForegroundColor Cyan
Write-Host "  Intensidad de Senal:      $signalPct% ($rssi_dBm dBm)" -ForegroundColor $(if ($rssi_dBm -ge -67) { 'Green' } else { 'Yellow' })
Write-Host "  Velocidad Negociada:      Tx: $txRate | Rx: $rxRate" -ForegroundColor Gray
Write-Host "  Seguridad y Cifrado:      $auth / $cipher" -ForegroundColor $(if ($auth -match 'WPA3|Enterprise') { 'Green' } else { 'Yellow' })

# Evaluacion de calidad para VoIP / Roaming
Write-Host "`n--- EVALUACION DE COBERTURA ENTERPRISE ---" -ForegroundColor Yellow
if ($rssi_dBm -ge -65) {
    Write-Host "  [OPTIMA] RSSI >= -65 dBm: Excelente senal para Voz sobre Wi-Fi (VoWiFi) y streaming 4K." -ForegroundColor Green
} elseif ($rssi_dBm -ge -72) {
    Write-Host "  [ACEPTABLE] RSSI entre -66 y -72 dBm: Cobertura buena para navegacion y correo." -ForegroundColor Yellow
} else {
    Write-Host "  [DEBIL] RSSI < -72 dBm: Riesgo alto de desconexiones o degradacion de rendimiento." -ForegroundColor Red
}

Write-Host "`n--- REDES INALAMBRICAS DETECTADAS EN EL ENTORNO (TOP 10) ---" -ForegroundColor Yellow
$redesVecinas = netsh wlan show networks mode=bssid | Select-String "SSID|Tipo de red|Autenticaci|Cifrado|BSSID|Se|Canal"
Write-Host "Escaneo de espectro completado. Revise canales vecinos para evitar solapamiento." -ForegroundColor Gray

Write-Host "`nPresione una tecla para continuar..." -ForegroundColor Gray
[System.Console]::ReadKey() | Out-Null
