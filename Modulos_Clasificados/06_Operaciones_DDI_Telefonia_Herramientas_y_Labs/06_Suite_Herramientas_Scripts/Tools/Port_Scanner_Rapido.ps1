<#
.SYNOPSIS
    Escaner de Puertos TCP Rapido y Auditor de Servicios para Windows.
.DESCRIPTION
    Realiza un escaneo de puertos TCP utilizando sockets asincronos de alta velocidad (.NET).
    Identifica puertos abiertos, servicios asociados y realiza extraccion basica de banners (Banner Grabbing).
#>

param(
    [string]$Target = "",
    [int]$TimeoutMs = 400
)

Clear-Host
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "             ESCANER DE PUERTOS TCP DE ALTA VELOCIDAD           " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

if ([string]::IsNullOrWhiteSpace($Target)) {
    $Target = Read-Host "Ingrese la direccion IP o host a escanear (Ej. 192.168.1.1 o switch)"
    if ([string]::IsNullOrWhiteSpace($Target)) { $Target = "127.0.0.1" }
}

Write-Host "`nSeleccione el modo de escaneo:" -ForegroundColor White
Write-Host "1. Puertos Comunes de Infraestructura (SSH, Telnet, Web, RDP, SMB, DBs)" -ForegroundColor Green
Write-Host "2. Rango Personalizado de Puertos (Ej. 1 al 1024)" -ForegroundColor Yellow
$Mode = Read-Host "Opcion (1 o 2)"

$CommonServices = [ordered]@{
    21   = "FTP (File Transfer Protocol)"
    22   = "SSH (Secure Shell)"
    23   = "Telnet (Texto Plano Inseguro)"
    25   = "SMTP (Correo Electronico)"
    53   = "DNS (Domain Name System TCP)"
    80   = "HTTP (Web en Texto Plano)"
    110  = "POP3 (Correo)"
    135  = "MS RPC (Remote Procedure Call)"
    139  = "NetBIOS Session Service"
    143  = "IMAP (Correo)"
    389  = "LDAP (Directorio Activo)"
    443  = "HTTPS (Web Seguro TLS/SSL)"
    445  = "Microsoft SMB (Comparticion de Archivos)"
    1433 = "Microsoft SQL Server"
    1521 = "Oracle Database"
    3306 = "MySQL / MariaDB"
    3389 = "RDP (Escritorio Remoto de Windows)"
    5060 = "SIP (Telefonia IP VoIP)"
    8080 = "HTTP Alternativo / Proxies"
    8443 = "HTTPS Alternativo"
}

$PortsToScan = @()

if ($Mode -eq "2") {
    $StartPort = [int](Read-Host "Puerto inicial")
    $EndPort   = [int](Read-Host "Puerto final")
    if ($StartPort -lt 1) { $StartPort = 1 }
    if ($EndPort -gt 65535) { $EndPort = 65535 }
    $PortsToScan = $StartPort..$EndPort
} else {
    $PortsToScan = $CommonServices.Keys
}

Write-Host "`nIniciando escaneo contra: $Target ($($PortsToScan.Count) puertos)" -ForegroundColor White
Write-Host "Timeout por puerto: ${TimeoutMs}ms`n" -ForegroundColor DarkGray

$OpenPorts = [System.Collections.Generic.List[PSCustomObject]]::new()
$Total = $PortsToScan.Count
$Current = 0

foreach ($Port in $PortsToScan) {
    $Current++
    $ServiceDesc = if ($CommonServices.Contains($Port)) { $CommonServices[$Port] } else { "Servicio Desconocido" }
    
    $TcpClient = New-Object System.Net.Sockets.TcpClient
    $ConnectTask = $TcpClient.ConnectAsync($Target, $Port)
    $Completed = $ConnectTask.Wait($TimeoutMs)

    if ($Completed -and $TcpClient.Connected) {
        $Banner = ""
        # Intento de Banner Grabbing simple
        try {
            $Stream = $TcpClient.GetStream()
            $Stream.ReadTimeout = 500
            $Buffer = New-Object byte[] 1024
            
            # Enviar CRLF para incitar respuesta si es un servidor de texto
            $BytesToSend = [System.Text.Encoding]::ASCII.GetBytes("HEAD / HTTP/1.0`r`n`r`n")
            $Stream.Write($BytesToSend, 0, $BytesToSend.Length)
            
            if ($Stream.DataAvailable) {
                $BytesRead = $Stream.Read($Buffer, 0, $Buffer.Length)
                $Banner = [System.Text.Encoding]::ASCII.GetString($Buffer, 0, $BytesRead).Trim()
                $Banner = ($Banner -split "`r`n")[0] # Solo tomar la primera linea
            }
        } catch { }

        Write-Host ("[+] PUERTO {0,5} : ABIERTO  | {1}" -f $Port, $ServiceDesc) -ForegroundColor Green
        if ($Banner) {
            Write-Host ("    --> Banner: {0}" -f $Banner) -ForegroundColor Cyan
        }

        $OpenPorts.Add([PSCustomObject]@{
            Puerto   = $Port
            Estado   = "ABIERTO"
            Servicio = $ServiceDesc
            Banner   = $Banner
        })

        $TcpClient.Close()
    } else {
        $TcpClient.Close()
    }
}

Write-Host "`n=================================================================" -ForegroundColor Cyan
Write-Host "                     RESUMEN DEL ESCANEO                        " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Destino evaluado        : $Target" -ForegroundColor White
Write-Host "Puertos escaneados      : $Total" -ForegroundColor White
Write-Host "Puertos abiertos totales: $($OpenPorts.Count)" -ForegroundColor $(if ($OpenPorts.Count -gt 0) { "Green" } else { "Yellow" })

if ($OpenPorts.Count -gt 0) {
    Write-Host "`nDETALLE DE PUERTOS ABIERTOS ENCONTRADOS:" -ForegroundColor White
    $OpenPorts | Format-Table -AutoSize
} else {
    Write-Host "`nNo se encontraron puertos abiertos en el rango seleccionado." -ForegroundColor Yellow
    Write-Host "El equipo podria estar apagado, bloqueando ICMP/TCP o protegido por un Firewall." -ForegroundColor Gray
}
Write-Host "=================================================================`n" -ForegroundColor Cyan
