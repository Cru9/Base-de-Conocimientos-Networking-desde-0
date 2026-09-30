<#
.SYNOPSIS
    Benchmark y Comparativa de Rendimiento de Servidores DNS.
.DESCRIPTION
    Realiza pruebas de resolucion DNS contra los servidores publicos mas reconocidos
    (Cloudflare, Google, Quad9, OpenDNS) y el DNS local configurado.
    Calcula latencias minimas, maximas y promedio para identificar el mejor proveedor.
.NOTES
    Modulo: Servicios_DDI_y_Gestion
    Autor: Cru9 - BC Compendium
#>

[CmdletBinding()]
param(
    [string[]]$DominiosDePrueba = @("google.com", "microsoft.com", "cloudflare.com", "github.com", "wikipedia.org"),
    [int]$RepeticionesPorDominio = 3
)

Clear-Host
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       BC DDI SERVICES - BENCHMARK Y EVALUACION DE RENDIMIENTO DNS" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$ServidoresDNS = @(
    @{ Nombre = "Cloudflare Primario"; IP = "1.1.1.1" },
    @{ Nombre = "Cloudflare Secundario"; IP = "1.0.0.1" },
    @{ Nombre = "Google Public DNS 1"; IP = "8.8.8.8" },
    @{ Nombre = "Google Public DNS 2"; IP = "8.8.4.4" },
    @{ Nombre = "Quad9 (Seguridad/Filtro)"; IP = "9.9.9.9" },
    @{ Nombre = "OpenDNS (Cisco Umbrella)"; IP = "208.67.222.222" }
)

# Detectar DNS configurado localmente
$dnsLocal = (Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object { $_.ServerAddresses.Count -gt 0 } | Select-Object -ExpandProperty ServerAddresses -First 1)
if ($dnsLocal) {
    $ServidoresDNS = @(@{ Nombre = "DNS Local (Configurado en Windows)"; IP = $dnsLocal }) + $ServidoresDNS
}

Write-Host "[*] Dominios de prueba: $($DominiosDePrueba -join ', ')" -ForegroundColor Gray
Write-Host "[*] Ejecutando $RepeticionesPorDominio consultas por cada dominio..." -ForegroundColor Gray
Write-Host ""

$resultados = @()

foreach ($srv in $ServidoresDNS) {
    Write-Host "Probando $($srv.Nombre) ($($srv.IP))..." -ForegroundColor Yellow -NoNewline
    $tiempos = @()
    $fallos = 0

    foreach ($dominio in $DominiosDePrueba) {
        for ($i = 0; $i -lt $RepeticionesPorDominio; $i++) {
            $sw = [System.Diagnostics.Stopwatch]::StartNew()
            try {
                $null = Resolve-DnsName -Name $dominio -Server $srv.IP -Type A -QuickTimeout -ErrorAction Stop
                $sw.Stop()
                $tiempos += $sw.Elapsed.TotalMilliseconds
            } catch {
                $sw.Stop()
                $fallos++
            }
        }
    }

    if ($tiempos.Count -gt 0) {
        $promedio = [math]::Round(($tiempos | Measure-Object -Average).Average, 1)
        $minimo   = [math]::Round(($tiempos | Measure-Object -Minimum).Minimum, 1)
        $maximo   = [math]::Round(($tiempos | Measure-Object -Maximum).Maximum, 1)
        
        Write-Host " [OK - Promedio: $promedio ms]" -ForegroundColor Green

        $resultados += [PSCustomObject]@{
            Servidor_DNS = $srv.Nombre
            Direccion_IP = $srv.IP
            Promedio_ms  = $promedio
            Minimo_ms    = $minimo
            Maximo_ms    = $maximo
            Consultas    = ($DominiosDePrueba.Count * $RepeticionesPorDominio)
            Fallos       = $fallos
        }
    } else {
        Write-Host " [INACCESIBLE]" -ForegroundColor Red
        $resultados += [PSCustomObject]@{
            Servidor_DNS = $srv.Nombre
            Direccion_IP = $srv.IP
            Promedio_ms  = 9999
            Minimo_ms    = 9999
            Maximo_ms    = 9999
            Consultas    = ($DominiosDePrueba.Count * $RepeticionesPorDominio)
            Fallos       = $fallos
        }
    }
}

Write-Host ""
Write-Host "=========================== CLASIFICACION POR VELOCIDAD ===========================" -ForegroundColor Cyan
$ranking = $resultados | Sort-Object Promedio_ms
$ranking | Format-Table Servidor_DNS, Direccion_IP, Promedio_ms, Minimo_ms, Maximo_ms, Fallos -AutoSize

$ganador = $ranking | Where-Object { $_.Fallos -eq 0 } | Select-Object -First 1
if ($ganador) {
    Write-Host "[RECOMENDACION] El servidor mas rapido y estable es: $($ganador.Servidor_DNS) ($($ganador.Direccion_IP)) con promedio de $($ganador.Promedio_ms) ms.`n" -ForegroundColor Green
}

Write-Host "Presione una tecla para continuar..." -ForegroundColor Gray
[System.Console]::ReadKey() | Out-Null
