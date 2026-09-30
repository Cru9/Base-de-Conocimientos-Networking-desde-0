<#
.SYNOPSIS
    Auditor Integral de Servicios DDI (DNS, DHCP) y Sincronizacion Horaria NTP.
.DESCRIPTION
    Inspecciona los tres pilares de gestion de infraestructura:
    1. DNS: Estado de servidores asignados, tiempo de resolucion de registros A y AAAA.
    2. DHCP: Concesion activa, fecha de adquisicion, fecha de expiracion y servidor emisor.
    3. NTP: Sincronizacion de reloj con w32tm, estrato (Stratum), servidor de tiempo y desfase (offset).
.NOTES
    Modulo: Servicios_DDI_y_Gestion
    Autor: Cru9 - BC Compendium
#>

Clear-Host
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       BC DDI SERVICES - AUDITOR DE SERVICIOS DNS, DHCP Y HORARIO NTP" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. AUDITORIA DNS
Write-Host "--- 1. AUDITORIA DE SERVICIOS DNS ---" -ForegroundColor Yellow
$dnsServers = (Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object { $_.ServerAddresses.Count -gt 0 }).ServerAddresses | Select-Object -Unique
Write-Host "Servidores DNS configurados en Windows: $($dnsServers -join ', ')" -ForegroundColor Cyan

$testDomains = @("microsoft.com", "google.com", "cloudflare.com")
$dnsResults = foreach ($dom in $testDomains) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $ipResolved = "-"
    $status = "OK"
    try {
        $entry = [System.Net.Dns]::GetHostAddresses($dom) | Select-Object -First 1
        $sw.Stop()
        $ipResolved = $entry.IPAddressToString
    } catch {
        $sw.Stop()
        $status = "FALLO"
    }

    [PSCustomObject]@{
        Dominio         = $dom
        IP_Resuelta     = $ipResolved
        Latencia_ms     = "$([math]::Round($sw.Elapsed.TotalMilliseconds, 1)) ms"
        Estado          = $status
    }
}
$dnsResults | Format-Table -AutoSize

# 2. AUDITORIA DHCP
Write-Host "`n--- 2. CONCESIONES Y ESTADO DHCP (WMI) ---" -ForegroundColor Yellow
$adaptersWMI = Get-CimInstance Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled -and $_.DHCPEnabled }

if ($adaptersWMI) {
    foreach ($a in $adaptersWMI) {
        Write-Host "Adaptador: $($a.Description)" -ForegroundColor Green
        Write-Host "  Servidor DHCP Emisor: $($a.DHCPServer)" -ForegroundColor Gray
        Write-Host "  Concesion Obtenida:   $($a.DHCPLeaseObtained)" -ForegroundColor Gray
        Write-Host "  Concesion Expira:     $($a.DHCPLeaseExpires)" -ForegroundColor Gray
    }
} else {
    Write-Host "[i] No se encontraron adaptadores configurados con direccionamiento dinamico DHCP (Estan en IP estatica)." -ForegroundColor Gray
}

# 3. AUDITORIA NTP
Write-Host "`n--- 3. SINCRONIZACION HORARIA NTP (W32Time) ---" -ForegroundColor Yellow
try {
    $ntpStatus = w32tm /query /status 2>&1
    if ($LASTEXITCODE -eq 0) {
        $source = ($ntpStatus | Select-String "Source:|Origen:").ToString().Trim()
        $stratum = ($ntpStatus | Select-String "Stratum:|Estrato:").ToString().Trim()
        $pollInterval = ($ntpStatus | Select-String "Poll Interval:|Intervalo de sondeo:").ToString().Trim()
        
        Write-Host "  $source" -ForegroundColor Cyan
        Write-Host "  $stratum" -ForegroundColor Gray
        Write-Host "  $pollInterval" -ForegroundColor Gray
        Write-Host "  [OK] Servicio Windows Time activo y respondiendo." -ForegroundColor Green
    } else {
        Write-Host "[AVISO] El servicio de hora W32Time no esta activo o no esta sincronizado con un servidor NTP externo." -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ERROR] No se pudo consultar w32tm." -ForegroundColor Red
}

Write-Host "`nPresione una tecla para continuar..." -ForegroundColor Gray
[System.Console]::ReadKey() | Out-Null
