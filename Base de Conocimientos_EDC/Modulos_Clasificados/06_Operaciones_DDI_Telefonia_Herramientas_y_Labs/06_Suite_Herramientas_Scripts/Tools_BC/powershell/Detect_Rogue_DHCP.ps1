<#
.SYNOPSIS
    Detector de Servidores DHCP No Autorizados (Rogue DHCP) en la Red Local (LAN).
.DESCRIPTION
    Herramienta defensiva de Ciberseguridad Capa 2 (Modelo OSI).
    Envia un paquete DHCP Discover en broadcast hacia el puerto UDP 67 y escucha
    las respuestas DHCP Offer en el puerto UDP 68. Si detecta multiples servidores
    ofreciendo direccionamiento o una IP de servidor desconocida, genera una alerta
    de posible ataque Man-In-The-Middle / Servidor DHCP Rogue.
.NOTES
    Modulo: Ciberseguridad_OSI / Servicios_DDI_y_Gestion
    Autor: Cru9 - BC Compendium
#>

[CmdletBinding()]
param(
    [int]$TimeoutSegundos = 5,
    [string]$ServidorAutorizadoIP = ""
)

Clear-Host
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       BC CYBERSECURITY - DETECTOR DE SERVIDORES ROGUE DHCP (LAN L2)" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

# Obtener MAC de la interfaz de red activa
$activeAdapter = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' -and $_.Virtual -ne $true } | Select-Object -First 1
if (-not $activeAdapter) {
    $activeAdapter = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | Select-Object -First 1
}

if (-not $activeAdapter) {
    Write-Host "[ERROR] No se encontro ninguna tarjeta de red activa en el sistema." -ForegroundColor Red
    return
}

$macBytes = ($activeAdapter.MacAddress -split "[:-]" | ForEach-Object { [Convert]::ToByte($_, 16) })
Write-Host "[*] Interfaz seleccionada: $($activeAdapter.Name) (MAC: $($activeAdapter.MacAddress))" -ForegroundColor Gray

# Construir paquete DHCP Discover (RFC 2131)
$packet = New-Object byte[] 300
$packet[0] = 1   # op: BOOTREQUEST
$packet[1] = 1   # htype: Ethernet
$packet[2] = 6   # hlen: 6 bytes
$packet[3] = 0   # hops

# Generar Transaction ID (xid) aleatorio
$rand = New-Object System.Random
$xid = New-Object byte[] 4
$rand.NextBytes($xid)
[Array]::Copy($xid, 0, $packet, 4, 4)

# Flags: 0x8000 (Broadcast)
$packet[10] = 0x80
$packet[11] = 0x00

# Client MAC Address (chaddr)
[Array]::Copy($macBytes, 0, $packet, 28, 6)

# Magic Cookie: 0x63, 0x82, 0x53, 0x63
$packet[236] = 0x63
$packet[237] = 0x82
$packet[238] = 0x53
$packet[239] = 0x63

# Opcion 53: DHCP Message Type = DHCPDISCOVER (1)
$packet[240] = 53
$packet[241] = 1
$packet[242] = 1

# Opcion 55: Parameter Request List (1=Subnet, 3=Router, 6=DNS, 15=Domain)
$packet[243] = 55
$packet[244] = 4
$packet[245] = 1
$packet[246] = 3
$packet[247] = 6
$packet[248] = 15

# Opcion 255: End
$packet[249] = 255

Write-Host "[*] Preparando socket UDP para sondeo broadcast..." -ForegroundColor Yellow

$udpClient = New-Object System.Net.Sockets.UdpClient
$udpClient.Client.SetSocketOption([System.Net.Sockets.SocketOptionLevel]::Socket, [System.Net.Sockets.SocketOptionName]::ReuseAddress, $true)
$udpClient.EnableBroadcast = $true

try {
    # Vincular al puerto DHCP Client 68
    $localEp = New-Object System.Net.IPEndPoint([System.Net.IPAddress]::Any, 68)
    $udpClient.Client.Bind($localEp)
} catch {
    Write-Host "[!] Nota: El puerto 68 esta en uso por el cliente DHCP de Windows. Utilizando modo alternativo..." -ForegroundColor DarkYellow
    $udpClient = New-Object System.Net.Sockets.UdpClient
    $udpClient.EnableBroadcast = $true
}

$destEp = New-Object System.Net.IPEndPoint([System.Net.IPAddress]::Broadcast, 67)
Write-Host "[*] Enviando paquete DHCP Discover a 255.255.255.255:67..." -ForegroundColor Cyan

try {
    $bytesSent = $udpClient.Send($packet, 250, $destEp)
} catch {
    Write-Host "[ERROR] No se pudo enviar el paquete UDP: $($_.Exception.Message)" -ForegroundColor Red
    $udpClient.Close()
    return
}

Write-Host "[*] Escuchando respuestas DHCP Offer (Timeout: $TimeoutSegundos s)..." -ForegroundColor Gray
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$offersReceived = @()

$udpClient.Client.ReceiveTimeout = 1000

while ($stopwatch.Elapsed.TotalSeconds -lt $TimeoutSegundos) {
    try {
        $senderEp = New-Object System.Net.IPEndPoint([System.Net.IPAddress]::Any, 0)
        $receivedBytes = $udpClient.Receive([ref]$senderEp)

        if ($receivedBytes.Length -ge 240) {
            # Verificar Magic Cookie
            if ($receivedBytes[236] -eq 0x63 -and $receivedBytes[237] -eq 0x82) {
                $offeredIP = "$($receivedBytes[16]).$($receivedBytes[17]).$($receivedBytes[18]).$($receivedBytes[19])"
                $serverIP = $senderEp.Address.ToString()
                
                $offersReceived += [PSCustomObject]@{
                    Servidor_DHCP = $serverIP
                    IP_Ofrecida   = $offeredIP
                    Tamano_Bytes  = $receivedBytes.Length
                    Tiempo_Resp   = "$([math]::Round($stopwatch.Elapsed.TotalMilliseconds, 0)) ms"
                }
            }
        }
    } catch [System.Net.Sockets.SocketException] {
        # Timeout normal de recepcion
    }
}

$udpClient.Close()

Write-Host ""
Write-Host "========================== RESULTADOS DEL ANALISIS ==========================" -ForegroundColor Cyan

if ($offersReceived.Count -eq 0) {
    Write-Host "[i] No se recibieron respuestas DHCP Offer dentro de la ventana de tiempo." -ForegroundColor Yellow
    Write-Host "    Causas posibles:" -ForegroundColor Gray
    Write-Host "    1. El segmento de red no posee servidor DHCP activo." -ForegroundColor Gray
    Write-Host "    2. Un switch intermediario tiene DHCP Snooping bloqueando puertos no confiables (Untrusted)." -ForegroundColor Green
    Write-Host "    3. El firewall local bloqueo la respuesta UDP." -ForegroundColor Gray
} elseif ($offersReceived.Count -eq 1) {
    $srv = $offersReceived[0]
    Write-Host "[OK] Se detecto exactamente 1 servidor DHCP en la red:" -ForegroundColor Green
    $offersReceived | Format-Table -AutoSize
    
    if ($ServidorAutorizadoIP -and $srv.Servidor_DHCP -ne $ServidorAutorizadoIP) {
        [System.Console]::Beep(1000, 400)
        Write-Host "[ALERTA CRITICA] El servidor detectado ($($srv.Servidor_DHCP)) NO coincide con el autorizado ($ServidorAutorizadoIP)!" -ForegroundColor Red
    } else {
        Write-Host "[ESTADO] Comportamiento normal. No hay evidencias de Rogue DHCP." -ForegroundColor Green
    }
} else {
    [System.Console]::Beep(1500, 500)
    [System.Console]::Beep(1500, 500)
    Write-Host "[ALERTA DE SEGURIDAD] Se detectaron MULTIPLES servidores DHCP ($($offersReceived.Count))!" -ForegroundColor Red
    Write-Host "Riesgo: Posible ataque Man-In-The-Middle, DHCP Spoofing o servidor configurado por error." -ForegroundColor Yellow
    Write-Host ""
    $offersReceived | Format-Table -AutoSize
    Write-Host "Accion recomendada: Activar 'ip dhcp snooping' y 'ip dhcp snooping trust' en el switch de acceso." -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Presione una tecla para continuar..." -ForegroundColor Gray
[System.Console]::ReadKey() | Out-Null
