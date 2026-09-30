<#
.SYNOPSIS
    Diagnostico de Capa 1 (Fisica y Cableado) en Adaptadores de Red Windows.
.DESCRIPTION
    Inspecciona el estado del cable de cobre/fibra (MediaConnectionState),
    velocidad negociada de enlace (LinkSpeed en Mbps/Gbps), modo Duplex (Full/Half),
    paquetes transmitidos/recibidos, errores de recepcion (CRC) y paquetes descartados.
.NOTES
    Modulo: Cableado_y_Fibra_Optica / Troubleshooting
    Autor: Cru9 - BC Compendium
#>

Clear-Host
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       BC NETWORK - DIAGNOSTICO DE CAPA 1 FISICA Y HARDWARE DE RED" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$adaptadores = Get-NetAdapter -ErrorAction Stop

Write-Host "--- RESUMEN DE ADAPTADORES DETECTADOS ---" -ForegroundColor Yellow
$adaptadores | Select-Object Name, InterfaceDescription, Status, LinkSpeed, FullDuplex, MacAddress | Format-Table -AutoSize

Write-Host "`n--- ESTADISTICAS DE TRAFICO Y ERRORES FISICOS ---" -ForegroundColor Yellow

foreach ($nic in $adaptadores | Where-Object { $_.Status -eq 'Up' }) {
    $stats = Get-NetAdapterStatistics -Name $nic.Name -ErrorAction SilentlyContinue

    Write-Host "Adaptador: $($nic.Name) [$($nic.InterfaceDescription)]" -ForegroundColor Green
    Write-Host "  Estado del Enlace:     $($nic.Status) (Cable conectado: $($nic.MediaConnectionState))" -ForegroundColor Gray
    Write-Host "  Velocidad Negociada:   $($nic.LinkSpeed)" -ForegroundColor Cyan
    Write-Host "  Modo de Transmision:   $(if ($nic.FullDuplex) { 'Full-Duplex (Bidireccional Simultaneo)' } else { 'Half-Duplex (Riesgo de colisiones)' })" -ForegroundColor $(if ($nic.FullDuplex) { 'Green' } else { 'Red' })
    
    if ($stats) {
        $rxMB = [math]::Round($stats.ReceivedBytes / 1MB, 2)
        $txMB = [math]::Round($stats.SentBytes / 1MB, 2)
        $rxErrors = $stats.ReceivedPacketErrors
        $txErrors = $stats.OutboundPacketErrors
        $rxDiscards = $stats.ReceivedPacketDiscards
        $txDiscards = $stats.OutboundPacketDiscards

        Write-Host "  Bytes Recibidos (Rx):  $rxMB MB (Paquetes: $($stats.ReceivedUnicastPackets))" -ForegroundColor Gray
        Write-Host "  Bytes Enviados (Tx):   $txMB MB (Paquetes: $($stats.SentUnicastPackets))" -ForegroundColor Gray

        # Analisis de calidad de cableado
        if ($rxErrors -gt 0 -or $txErrors -gt 0) {
            Write-Host "  [ALERTA L1] Errores de Paquete Detectados: Rx=$rxErrors, Tx=$txErrors" -ForegroundColor Red
            Write-Host "              Causa probable: Cable UTP defectuoso, crimpado deficiente, conector sucio o interferencia EMI." -ForegroundColor Yellow
        } else {
            Write-Host "  [OK L1] Errores de Transmision/CRC: 0 (Calidad de enlace optima)" -ForegroundColor Green
        }

        if ($rxDiscards -gt 0 -or $txDiscards -gt 0) {
            Write-Host "  [AVISO] Paquetes Descartados: Rx=$rxDiscards, Tx=$txDiscards (Posible saturacion de buffer)" -ForegroundColor Yellow
        }
    }
    Write-Host ""
}

Write-Host "Presione una tecla para continuar..." -ForegroundColor Gray
[System.Console]::ReadKey() | Out-Null
