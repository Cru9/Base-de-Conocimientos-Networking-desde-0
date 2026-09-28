<#
.SYNOPSIS
    Descubridor de MTU de Ruta (Path MTU Discovery) y Calculador de TCP MSS.
.DESCRIPTION
    Realiza pruebas de paquetes con la bandera Don't Fragment (DF) activa para determinar
    el tamano maximo de paquete que puede cruzar la red sin fragmentarse. Ideal para
    resolver problemas de navegacion lenta, congelamiento de sesiones SSH y tuneles VPN.
#>

param(
    [string]$Target = "",
    [int]$MinPayload = 1200,
    [int]$MaxPayload = 1472
)

Clear-Host
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "         DESCUBRIDOR DE MTU DE RUTA Y CALCULADOR DE TCP MSS     " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

if ([string]::IsNullOrWhiteSpace($Target)) {
    $Target = Read-Host "Ingrese la direccion IP o host destino a evaluar (Ej. 8.8.8.8 o IP remota de VPN)"
    if ([string]::IsNullOrWhiteSpace($Target)) { $Target = "8.8.8.8" }
}

Write-Host "`nIniciando busqueda binaria de MTU hacia: $Target" -ForegroundColor White
Write-Host "Rango de prueba de carga util ICMP: $MinPayload a $MaxPayload bytes`n" -ForegroundColor DarkGray

$Pinger = New-Object System.Net.NetworkInformation.Ping
$PingOptions = New-Object System.Net.NetworkInformation.PingOptions
$PingOptions.DontFragment = $true
$Timeout = 1200

# Primero validar si el destino responde
try {
    $TestReply = $Pinger.Send($Target, $Timeout)
    if ($TestReply.Status -ne [System.Net.NetworkInformation.IPStatus]::Success) {
        Write-Host "[ADVERTENCIA] El destino no respondio al ping inicial ($($TestReply.Status)). Es posible que bloquee ICMP." -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ERROR] Imposible alcanzar el destino: $($_.Exception.Message)" -ForegroundColor Red
    return
}

# Busqueda Binaria para encontrar la carga util maxima exacta
$Low = $MinPayload
$High = $MaxPayload
$OptimalPayload = -1

while ($Low -le $High) {
    $Mid = [math]::Floor(($Low + $High) / 2)
    $Buffer = New-Object byte[] $Mid

    Write-Host "Probando tamano de carga util: $Mid bytes (Paquete total: $($Mid + 28) bytes)... " -NoNewline -ForegroundColor Gray

    try {
        $Reply = $Pinger.Send($Target, $Timeout, $Buffer, $PingOptions)

        if ($Reply.Status -eq [System.Net.NetworkInformation.IPStatus]::Success) {
            Write-Host "EXITO (Sin fragmentar)" -ForegroundColor Green
            $OptimalPayload = $Mid
            $Low = $Mid + 1 # Probar tamano mas grande
        } else {
            Write-Host "FALLO ($($Reply.Status))" -ForegroundColor Red
            $High = $Mid - 1 # Reducir tamano
        }
    } catch {
        Write-Host "ERROR ($($_.Exception.Message))" -ForegroundColor Red
        $High = $Mid - 1
    }
}

if ($OptimalPayload -eq -1) {
    Write-Host "`n[ERROR] No se pudo determinar el MTU. Verifique conectividad o politicas de firewall." -ForegroundColor Red
    return
}

# Calculo de parametros de red
$OptimalMTU = $OptimalPayload + 28   # 20 bytes IPv4 Header + 8 bytes ICMP Header
$OptimalMSS = $OptimalMTU - 40       # 20 bytes IP + 20 bytes TCP Header

Write-Host "`n=================================================================" -ForegroundColor Cyan
Write-Host "                   RESULTADOS DEL ANALISIS                      " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Carga util ICMP maxima sin fragmentar : $OptimalPayload bytes" -ForegroundColor White
Write-Host "MTU Maximo de la Ruta (PMTU)          : $OptimalMTU bytes" -ForegroundColor Green
Write-Host "TCP MSS Recomendado (MTU - 40)        : $OptimalMSS bytes" -ForegroundColor Yellow

if ($OptimalMTU -lt 1500) {
    $PerdidaBytes = 1500 - $OptimalMTU
    Write-Host "`n[DIAGNOSTICO] Se detectaron tuneles o encapsulados en la ruta!" -ForegroundColor Magenta
    Write-Host "La ruta pierde $PerdidaBytes bytes respecto al estandar Ethernet (1500 bytes)." -ForegroundColor Gray
    Write-Host "Causas comunes: Tuneles IPsec, GRE, PPPoE (ADSL/Fibra), MPLS o VXLAN." -ForegroundColor Gray
} else {
    Write-Host "`n[DIAGNOSTICO] Ruta estandar limpia (Ethernet 1500 bytes sin overhead visible)." -ForegroundColor Green
}

Write-Host "`nCOMANDOS DE AJUSTE RECOMENDADOS:" -ForegroundColor White
Write-Host "-----------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "# En Windows (Ajustar interfaz local en PowerShell como Administrador):" -ForegroundColor Cyan
Write-Host "netsh interface ipv4 set subinterface `"Ethernet`" mtu=$OptimalMTU store=persistent`n" -ForegroundColor Gray

Write-Host "# En Routers Cisco (MSS Clamping en la interfaz del tunel o WAN):" -ForegroundColor Cyan
Write-Host "interface GigabitEthernet0/0/1" -ForegroundColor Gray
Write-Host " ip mtu $OptimalMTU" -ForegroundColor Gray
Write-Host " ip tcp adjust-mss $OptimalMSS`n" -ForegroundColor Gray

Write-Host "# En Firewalls Fortinet (FortiOS):" -ForegroundColor Cyan
Write-Host "config system interface" -ForegroundColor Gray
Write-Host "  edit `"wan1`"" -ForegroundColor Gray
Write-Host "    set tcp-mss $OptimalMSS" -ForegroundColor Gray
Write-Host "  next" -ForegroundColor Gray
Write-Host "end`n" -ForegroundColor Gray
Write-Host "=================================================================`n" -ForegroundColor Cyan
