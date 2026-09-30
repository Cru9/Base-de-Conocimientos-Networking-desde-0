<#
.SYNOPSIS
    Tester Nativo de Conectividad para Redes Industriales OT / SCADA.
.DESCRIPTION
    Herramienta nativa en PowerShell (.NET Sockets) para verificar la disponibilidad
    y latencia de puertos de automatizacion industrial en PLCs, RTUs y HMIs:
    - Modbus TCP (502)
    - Siemens S7 Comm (102)
    - EtherNet/IP CIP (44818)
    - DNP3 Subestaciones (20000)
    - BACnet/IP Automatizacion de Edificios (47808)
    - MQTT / Sparkplug B (1883)
.NOTES
    Modulo: Redes_Industriales_OT (Modelo Purdue)
    Autor: Cru9 - BC Compendium
#>

[CmdletBinding()]
param(
    [string]$TargetIP = "127.0.0.1",
    [int]$TimeoutMs = 1200
)

Clear-Host
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       BC OT SECURITY - TESTER NATIVO DE PUERTOS INDUSTRIALES OT/SCADA" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$inputIP = Read-Host "Ingrese la direccion IP del PLC, RTU o Gateway OT [$TargetIP]"
if (-not [string]::IsNullOrWhiteSpace($inputIP)) {
    $TargetIP = $inputIP.Trim()
}

$puertosOT = @(
    @{ Puerto = 502;   Nombre = "Modbus TCP"; Descripcion = "Control de PLCs / Sensores (Nivel 1/2 Purdue)" },
    @{ Puerto = 102;   Nombre = "Siemens S7"; Descripcion = "Controladores Siemens S7-300/400/1200/1500" },
    @{ Puerto = 44818; Nombre = "EtherNet/IP"; Descripcion = "Rockwell Allen-Bradley / CIP" },
    @{ Puerto = 20000; Nombre = "DNP3"; Descripcion = "Subestaciones Electricas y Plantas de Agua" },
    @{ Puerto = 47808; Nombre = "BACnet/IP"; Descripcion = "Sistemas BMS / Control de Clima HVAC" },
    @{ Puerto = 1883;  Nombre = "MQTT IIoT"; Descripcion = "Telemetria IoT Industrial (Sin cifrar)" },
    @{ Puerto = 8883;  Nombre = "MQTT TLS"; Descripcion = "Telemetria IoT Industrial Cifrada" }
)

Write-Host "`n[*] Iniciando sondeo de sockets en $TargetIP (Timeout: $TimeoutMs ms)...`n" -ForegroundColor Yellow

$resultados = foreach ($p in $puertosOT) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $socket = New-Object System.Net.Sockets.TcpClient
    $abierto = $false

    try {
        $async = $socket.BeginConnect($TargetIP, $p.Puerto, $null, $null)
        $success = $async.AsyncWaitHandle.WaitOne($TimeoutMs, $false)
        if ($success -and $socket.Connected) {
            $socket.EndConnect($async)
            $abierto = $true
        }
    } catch {
        $abierto = $false
    } finally {
        $sw.Stop()
        $socket.Close()
    }

    [PSCustomObject]@{
        Puerto      = $p.Puerto
        Protocolo   = $p.Nombre
        Descripcion = $p.Descripcion
        Estado      = if ($abierto) { "[ABIERTO / ACTIVO]" } else { "Cerrado / Filtrado" }
        Latencia_ms = if ($abierto) { "$([math]::Round($sw.Elapsed.TotalMilliseconds, 1)) ms" } else { "-" }
    }
}

$resultados | Format-Table Puerto, Protocolo, Estado, Latencia_ms, Descripcion -AutoSize

$abiertosCount = ($resultados | Where-Object { $_.Estado -match "ABIERTO" }).Count
if ($abiertosCount -gt 0) {
    Write-Host "[!] ADVERTENCIA OT: Se detectaron $abiertosCount puertos industriales activos en este equipo." -ForegroundColor Yellow
    Write-Host "    Verifique que el dispositivo este aislado en su respectiva celda o zona segun ISA/IEC 62443." -ForegroundColor Gray
} else {
    Write-Host "[OK] Ningun puerto industrial estandar respondio en este host." -ForegroundColor Green
}

Write-Host "`nPresione una tecla para continuar..." -ForegroundColor Gray
[System.Console]::ReadKey() | Out-Null
