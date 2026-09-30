<#
.SYNOPSIS
    Inspector de Rutas y Traza WAN Avanzada (Traceroute Capa 3).
.DESCRIPTION
    Realiza una traza de paquetes hop-by-hop incrementando el campo TTL (Time-To-Live).
    Mide los tiempos de respuesta (RTT) en milisegundos, resuelve el nombre PTR inverso
    de cada router intermedio y clasifica los saltos entre LAN, Carrier/ISP e Internet.
.NOTES
    Modulo: Routing_y_WAN / Telecomunicaciones_Avanzadas_Carrier
    Autor: Cru9 - BC Compendium
#>

[CmdletBinding()]
param(
    [string]$Destino = "1.1.1.1",
    [int]$MaxSaltos = 25,
    [int]$TimeoutMs = 1500
)

Clear-Host
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       BC ROUTING & WAN - INSPECTOR DE RUTAS Y TRAZA WAN (TTL PROBING)" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$inputDest = Read-Host "Ingrese la direccion IP o nombre de destino [$Destino]"
if (-not [string]::IsNullOrWhiteSpace($inputDest)) {
    $Destino = $inputDest.Trim()
}

Write-Host "`n[*] Iniciando traza hacia $Destino (Max saltos: $MaxSaltos, Timeout: $TimeoutMs ms)..." -ForegroundColor Yellow
Write-Host "=====================================================================================================" -ForegroundColor DarkGray
Write-Host ("{0,-5} {1,-18} {2,-30} {3,-10} {4,-10} {5,-10} {6}" -f "Salto", "Direccion IP", "Nombre DNS / PTR", "RTT 1", "RTT 2", "RTT 3", "Tipo de Red") -ForegroundColor Cyan
Write-Host "=====================================================================================================" -ForegroundColor DarkGray

$ping = New-Object System.Net.NetworkInformation.Ping
$buffer = New-Object byte[] 32
(New-Object System.Random).NextBytes($buffer)

for ($ttl = 1; $ttl -le $MaxSaltos; $ttl++) {
    $options = New-Object System.Net.NetworkInformation.PingOptions($ttl, $true)
    $rtts = @()
    $hopIP = "*"

    for ($p = 0; $p -lt 3; $p++) {
        try {
            $reply = $ping.Send($Destino, $TimeoutMs, $buffer, $options)
            if ($reply.Status -in @('Success', 'TtlExpired')) {
                $hopIP = $reply.Address.ToString()
                $rtts += "$($reply.RoundtripTime) ms"
            } else {
                $rtts += "*"
            }
        } catch {
            $rtts += "*"
        }
    }

    $ptrName = "-"
    $tipoRed = "Sin respuesta"

    if ($hopIP -ne "*") {
        try {
            $entry = [System.Net.Dns]::GetHostEntry($hopIP)
            $ptrName = $entry.HostName
            if ($ptrName.Length -gt 28) { $ptrName = $ptrName.Substring(0, 25) + "..." }
        } catch {
            $ptrName = "(Sin registro PTR)"
        }

        if ($hopIP -match '^10\.' -or $hopIP -match '^172\.(1[6-9]|2[0-9]|3[0-1])\.' -or $hopIP -match '^192\.168\.') {
            $tipoRed = "LAN / Privada"
        } elseif ($hopIP -match '^100\.(6[4-9]|[7-9][0-9]|1[0-1][0-9]|12[0-7])\.') {
            $tipoRed = "Carrier-Grade NAT"
        } else {
            $tipoRed = "ISP / Internet WAN"
        }
    }

    $rtt1 = if ($rtts.Count -gt 0) { $rtts[0] } else { "*" }
    $rtt2 = if ($rtts.Count -gt 1) { $rtts[1] } else { "*" }
    $rtt3 = if ($rtts.Count -gt 2) { $rtts[2] } else { "*" }

    $color = if ($hopIP -eq "*") { "DarkGray" } elseif ($tipoRed -match "LAN") { "Green" } else { "White" }

    Write-Host ("{0,-5} {1,-18} {2,-30} {3,-10} {4,-10} {5,-10} {6}" -f $ttl, $hopIP, $ptrName, $rtt1, $rtt2, $rtt3, $tipoRed) -ForegroundColor $color

    if ($hopIP -eq $Destino) {
        Write-Host "`n[OK] Destino alcanzado con exito en $ttl saltos." -ForegroundColor Green
        break
    }
}

Write-Host ""
Write-Host "Presione una tecla para continuar..." -ForegroundColor Gray
[System.Console]::ReadKey() | Out-Null
