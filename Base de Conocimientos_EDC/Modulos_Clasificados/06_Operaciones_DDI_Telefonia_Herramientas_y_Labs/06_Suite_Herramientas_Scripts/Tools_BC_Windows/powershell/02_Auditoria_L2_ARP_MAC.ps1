<#
.SYNOPSIS
    Auditoria de Capa 2 (Enlace de Datos): Mapeo ARP, MACs y Deteccion de Conflictos.
.DESCRIPTION
    Inspecciona la tabla de vecinos de Capa 2 (ARP Table), identifica el Default Gateway,
    detecta posibles colisiones de direcciones IP, analiza prefijos OUI de fabricantes
    y alerta si existen anomalias en la resolucion de direcciones fisicas.
.NOTES
    Modulo: OSI / SW (Switching) / Ciberseguridad_OSI
    Autor: Cru9 - BC Compendium
#>

Clear-Host
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       BC NETWORK - AUDITORIA DE CAPA 2 (TABLA ARP Y DIRECCIONES MAC)" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$vecinos = Get-NetNeighbor -AddressFamily IPv4 | Where-Object { $_.LinkLayerAddress -and $_.State -notin @('Unreachable') }

if (-not $vecinos) {
    Write-Host "[i] No se encontraron entradas activas en la tabla ARP." -ForegroundColor Yellow
    return
}

# Obtener Default Gateway
$gwIP = (Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue).NextHop

$OUI_Conocidos = @{
    "00:50:56" = "VMware ESXi / Workstation"
    "00:0C:29" = "VMware Virtual NIC"
    "00:15:5D" = "Microsoft Hyper-V"
    "00:1A:A0" = "Dell Networking"
    "00:00:0C" = "Cisco Systems"
    "00:01:42" = "Cisco Systems"
    "00:18:BA" = "Cisco Systems"
    "F4:BD:9E" = "Cisco Systems"
    "00:E0:FC" = "Huawei Technologies"
    "70:7B:E8" = "Huawei Technologies"
    "AC:75:1D" = "Huawei Technologies"
    "00:04:0D" = "Avaya Telephony"
    "F0:9F:C2" = "Ubiquiti UniFi"
    "00:1A:79" = "Alcatel-Lucent"
    "B8:27:EB" = "Raspberry Pi Foundation"
    "DC:A6:32" = "Raspberry Pi Foundation"
    "AC:DE:48" = "Apple Device"
    "F8:FF:C2" = "Apple Device"
    "3C:D9:2B" = "Hewlett Packard Enterprise"
    "28:6F:7F" = "TP-Link Technologies"
    "50:C7:BF" = "TP-Link Technologies"
}

function Obtener-Fabricante ([string]$mac) {
    if ([string]::IsNullOrWhiteSpace($mac)) { return "Desconocido" }
    $prefijo = $mac.Substring(0, [math]::Min(8, $mac.Length)).ToUpper().Replace("-", ":")
    if ($OUI_Conocidos.ContainsKey($prefijo)) {
        return $OUI_Conocidos[$prefijo]
    }
    return "Generico / Privado"
}

Write-Host "[*] Default Gateway Detectado: $gwIP" -ForegroundColor Cyan
Write-Host "[*] Entradas ARP Analizadas:   $($vecinos.Count)`n" -ForegroundColor Gray

$tablaReporte = foreach ($v in $vecinos) {
    $ip = $v.IPAddress
    $mac = $v.LinkLayerAddress.ToUpper().Replace("-", ":")
    $esGW = ($ip -eq $gwIP)
    $fabricante = Obtener-Fabricante $mac

    $rol = if ($esGW) { "[GATEWAY PRINCIPAL]" } else { "Host / Endpoint" }
    if ($ip -eq "255.255.255.255" -or $ip -match '^224\.') { $rol = "Broadcast / Multicast" }

    [PSCustomObject]@{
        IP_Destino  = $ip
        MAC_Address = $mac
        Rol_Red     = $rol
        Fabricante  = $fabricante
        Estado_ARP  = $v.State
        Interfaz    = $v.InterfaceAlias
    }
}

$tablaReporte | Sort-Object Rol_Red -Descending | Format-Table IP_Destino, MAC_Address, Rol_Red, Fabricante, Estado_ARP, Interfaz -AutoSize

# Deteccion de anomalias (Multiples IPs con la misma MAC o viceversa)
$ipsDuplicadas = $tablaReporte | Where-Object { $_.Rol_Red -notmatch "Broadcast" } | Group-Object MAC_Address | Where-Object { $_.Count -gt 3 }
if ($ipsDuplicadas) {
    Write-Host "`n[AVISO] Se detectaron direcciones MAC que responden por multiples direcciones IP (>3):" -ForegroundColor Yellow
    foreach ($dup in $ipsDuplicadas) {
        Write-Host "  MAC: $($dup.Name) responde por: $($dup.Group.IP_Destino -join ', ')" -ForegroundColor Gray
    }
    Write-Host "  (Normal en routers o gateways haciendo Proxy ARP / Subinterfaces trunk)." -ForegroundColor DarkGray
}

Write-Host "`nPresione una tecla para continuar..." -ForegroundColor Gray
[System.Console]::ReadKey() | Out-Null
