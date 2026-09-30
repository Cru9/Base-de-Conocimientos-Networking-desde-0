<#
.SYNOPSIS
    Reporte Integral de Salud y Auditoria de Red para Windows (HTML + Consola).
.DESCRIPTION
    Extrae la configuracion completa de red del host: adaptadores, direcciones IP/MAC,
    gateways, servidores DNS y DHCP, IP publica externa, latencia al gateway,
    tabla de enrutamiento, cache ARP y puertos TCP en escucha.
    Genera un informe visual profesional en formato HTML y lo abre automaticamente.
#>

Clear-Host
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "         AUDITORIA INTEGRAL DE SALUD DE RED (WINDOWS)            " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

Write-Host "Recopilando telemetria del sistema operativo y adaptadores...`n" -ForegroundColor DarkGray

$ComputerName = $env:COMPUTERNAME
$UserName = $env:USERNAME
$DateStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$DateFile = Get-Date -Format "yyyyMMdd_HHmmss"

# 1. Adaptadores Fisicos y Logicos
Write-Host "[1/7] Extrayendo adaptadores de red y velocidad de enlace..." -ForegroundColor White
$Adapters = Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, LinkSpeed, MacAddress

# 2. Direccionamiento IP
Write-Host "[2/7] Extrayendo direcciones IPv4 e IPv6..." -ForegroundColor White
$IPConfigs = Get-NetIPConfiguration | Where-Object { $_.IPv4Address -ne $null }

# 3. Prueba de Gateway y Latencia
Write-Host "[3/7] Diagnosticando Default Gateway y latencia..." -ForegroundColor White
$GatewayResults = [System.Collections.Generic.List[PSCustomObject]]::new()
$Pinger = New-Object System.Net.NetworkInformation.Ping

foreach ($Config in $IPConfigs) {
    if ($Config.IPv4DefaultGateway) {
        $GwIp = $Config.IPv4DefaultGateway.NextHop
        try {
            $Reply = $Pinger.Send($GwIp, 1000)
            $Status = if ($Reply.Status -eq "Success") { "ALCANZABLE ($($Reply.RoundtripTime)ms)" } else { "FALLO ($($Reply.Status))" }
            $Color = if ($Reply.Status -eq "Success") { "Green" } else { "Red" }
        } catch {
            $Status = "ERROR EXCEPCION"
            $Color = "Red"
        }
        $GatewayResults.Add([PSCustomObject]@{
            Interfaz = $Config.InterfaceAlias
            Gateway  = $GwIp
            Estado   = $Status
        })
    }
}

# 4. Deteccion de IP Publica Externa
Write-Host "[4/7] Consultando direccion IP publica externa..." -ForegroundColor White
$PublicIP = "Desconocida / Sin Acceso a Internet"
try {
    $WebClient = New-Object System.Net.WebClient
    $WebClient.Timeout = 3000
    $PublicIP = $WebClient.DownloadString("https://api.ipify.org").Trim()
} catch {
    try {
        $PublicIP = (Invoke-RestMethod -Uri "https://icanhazip.com" -TimeoutSec 3).Trim()
    } catch {
        $PublicIP = "Sin conexion directa a Internet"
    }
}

# 5. Tabla de Enrutamiento IPv4
Write-Host "[5/7] Obteniendo tabla de rutas activas..." -ForegroundColor White
$Routes = Get-NetRoute -AddressFamily IPv4 | Where-Object { $_.DestinationPrefix -ne "255.255.255.255/32" } | 
          Select-Object DestinationPrefix, NextHop, RouteMetric, InterfaceAlias | Sort-Object RouteMetric

# 6. Cache ARP
Write-Host "[6/7] Obteniendo tabla ARP de vecinos descubiertos..." -ForegroundColor White
$ArpCache = Get-NetNeighbor -AddressFamily IPv4 | Where-Object { $_.State -ne "Unreachable" -and $_.LinkLayerAddress -ne "00-00-00-00-00-00" } |
            Select-Object IPAddress, LinkLayerAddress, State, InterfaceAlias

# 7. Puertos TCP en Escucha (Servicios Locales)
Write-Host "[7/7] Analizando puertos y servicios TCP abiertos..." -ForegroundColor White
$ListeningPorts = Get-NetTCPConnection -State Listen | 
                  Select-Object LocalAddress, LocalPort, OwningProcess | 
                  Sort-Object LocalPort

# Construccion del Reporte HTML Profesional
$HtmlPath = Join-Path -Path $PSScriptRoot -ChildPath "Reporte_Salud_Red_${DateFile}.html"

$Html = @"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Red - $ComputerName</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: auto; }
        h1, h2, h3 { color: #38bdf8; }
        .header-box { background: #1e293b; padding: 20px; border-radius: 10px; border-left: 6px solid #38bdf8; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5); }
        .grid-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 25px; }
        .card { background: #1e293b; padding: 15px; border-radius: 8px; border-top: 4px solid #0284c7; }
        .card h4 { margin: 0 0 10px 0; color: #94a3b8; font-size: 0.9em; text-transform: uppercase; }
        .card p { margin: 0; font-size: 1.3em; font-weight: bold; color: #f1f5f9; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 30px; background: #1e293b; border-radius: 8px; overflow: hidden; }
        th, td { padding: 12px 15px; text-align: left; }
        th { background-color: #0284c7; color: white; font-weight: 600; text-transform: uppercase; font-size: 0.85em; }
        tr:nth-child(even) { background-color: #1e293b; }
        tr:nth-child(odd) { background-color: #162032; }
        tr:hover { background-color: #334155; }
        .badge { padding: 4px 10px; border-radius: 12px; font-size: 0.8em; font-weight: bold; }
        .badge-up { background-color: #15803d; color: #dcfce7; }
        .badge-down { background-color: #b91c1c; color: #fee2e2; }
        .footer { text-align: center; color: #64748b; font-size: 0.85em; margin-top: 40px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header-box">
        <h1>REPORTE DE DIAGNOSTICO Y SALUD DE RED</h1>
        <p>Equipo: <strong>$ComputerName</strong> | Usuario: <strong>$UserName</strong> | Fecha: <strong>$DateStr</strong></p>
    </div>

    <div class="grid-cards">
        <div class="card">
            <h4>IP Publica de Salida</h4>
            <p style="color: #38bdf8;">$PublicIP</p>
        </div>
        <div class="card">
            <h4>Adaptadores Detectados</h4>
            <p>$($Adapters.Count)</p>
        </div>
        <div class="card">
            <h4>Gateways Monitoreados</h4>
            <p>$($GatewayResults.Count)</p>
        </div>
        <div class="card">
            <h4>Puertos TCP en Escucha</h4>
            <p>$($ListeningPorts.Count)</p>
        </div>
    </div>

    <h2>1. Adaptadores de Red y Estado de Enlace</h2>
    <table>
        <thead><tr><th>Nombre</th><th>Descripcion</th><th>Estado</th><th>Velocidad</th><th>Direccion MAC</th></tr></thead>
        <tbody>
"@

foreach ($A in $Adapters) {
    $Badge = if ($A.Status -eq "Up") { "<span class='badge badge-up'>UP / ACTIVO</span>" } else { "<span class='badge badge-down'>DOWN</span>" }
    $Html += "<tr><td>$($A.Name)</td><td>$($A.InterfaceDescription)</td><td>$Badge</td><td>$($A.LinkSpeed)</td><td>$($A.MacAddress)</td></tr>"
}

$Html += @"
        </tbody>
    </table>

    <h2>2. Direccionamiento IP y Gateway</h2>
    <table>
        <thead><tr><th>Interfaz</th><th>Direccion IPv4</th><th>Mascara / Prefijo</th><th>Default Gateway</th><th>Servidores DNS</th></tr></thead>
        <tbody>
"@

foreach ($C in $IPConfigs) {
    $Gw = if ($C.IPv4DefaultGateway) { $C.IPv4DefaultGateway.NextHop } else { "Ninguno" }
    $Dns = ($C.DnsServer.ServerAddresses) -join ", "
    $Html += "<tr><td>$($C.InterfaceAlias)</td><td><strong>$($C.IPv4Address.IPAddress)</strong></td><td>$($C.IPv4Address.PrefixLength)</td><td>$Gw</td><td>$Dns</td></tr>"
}

$Html += @"
        </tbody>
    </table>

    <h2>3. Estado de Conectividad con Gateway</h2>
    <table>
        <thead><tr><th>Interfaz</th><th>Direccion Gateway</th><th>Resultado de Prueba</th></tr></thead>
        <tbody>
"@

foreach ($G in $GatewayResults) {
    $Html += "<tr><td>$($G.Interfaz)</td><td>$($G.Gateway)</td><td><strong>$($G.Estado)</strong></td></tr>"
}

$Html += @"
        </tbody>
    </table>

    <h2>4. Tabla ARP (Dispositivos Vecinos Descubiertos en L2)</h2>
    <table>
        <thead><tr><th>Direccion IP</th><th>Direccion MAC (Fisica)</th><th>Estado ARP</th><th>Interfaz</th></tr></thead>
        <tbody>
"@

foreach ($Arp in $ArpCache | Select-Object -First 25) {
    $Html += "<tr><td>$($Arp.IPAddress)</td><td>$($Arp.LinkLayerAddress)</td><td>$($Arp.State)</td><td>$($Arp.InterfaceAlias)</td></tr>"
}

$Html += @"
        </tbody>
    </table>

    <h2>5. Puertos TCP Locales en Escucha (Servicios Activos)</h2>
    <table>
        <thead><tr><th>Direccion Local</th><th>Puerto TCP</th><th>PID del Proceso</th></tr></thead>
        <tbody>
"@

foreach ($P in $ListeningPorts | Select-Object -First 30) {
    $Html += "<tr><td>$($P.LocalAddress)</td><td><strong>$($P.LocalPort)</strong></td><td>$($P.OwningProcess)</td></tr>"
}

$Html += @"
        </tbody>
    </table>

    <div class="footer">
        Generado automaticamente por la Suite de Redes BC - Antigravity Toolkit para Windows
    </div>
</div>
</body>
</html>
"@

$Html | Out-File -FilePath $HtmlPath -Encoding utf8

Write-Host "`n=================================================================" -ForegroundColor Cyan
Write-Host "                REPORTE GENERADO CON EXITO                       " -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Archivo HTML guardado en: $HtmlPath" -ForegroundColor White
Write-Host "Abriendo reporte en su navegador predeterminado..." -ForegroundColor Yellow

Start-Process $HtmlPath
Write-Host "=================================================================`n" -ForegroundColor Cyan
