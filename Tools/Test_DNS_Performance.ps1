<#
.SYNOPSIS
    Prueba Comparativa de Rendimiento y Latencia de Servidores DNS.
.DESCRIPTION
    Realiza multiples consultas de resolucion de nombres contra el DNS local corporativo
    y los principales proveedores publicos mundiales (Google, Cloudflare, Quad9, OpenDNS).
    Mide los milisegundos de respuesta exactos e identifica cual ofrece la navegacion mas rapida.
#>

param(
    [string[]]$DomainsToTest = @("google.com", "microsoft.com", "cloudflare.com", "amazon.com"),
    [int]$Iterations = 2
)

Clear-Host
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "         BENCHMARK Y COMPARATIVA DE RENDIMIENTO DNS             " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

# Obtener DNS local configurado
$LocalDns = (Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object { $_.ServerAddresses.Count -gt 0 }).ServerAddresses | Select-Object -First 1
if (-not $LocalDns) { $LocalDns = "127.0.0.1" }

$DnsProviders = [ordered]@{
    "DNS Local / Gateway" = $LocalDns
    "Cloudflare (1.1.1.1)" = "1.1.1.1"
    "Google DNS (8.8.8.8)"  = "8.8.8.8"
    "Quad9 Seguro (9.9.9.9)"= "9.9.9.9"
    "OpenDNS (208.67.222.222)" = "208.67.222.222"
}

Write-Host "Dominios de prueba : $($DomainsToTest -join ', ')" -ForegroundColor White
Write-Host "Iteraciones por DNS: $Iterations consultas por dominio`n" -ForegroundColor DarkGray

$Results = [System.Collections.Generic.List[PSCustomObject]]::new()

foreach ($Name in $DnsProviders.Keys) {
    $ServerIp = $DnsProviders[$Name]
    Write-Host "Evaluando proveedor: $Name [$ServerIp]... " -NoNewline -ForegroundColor White

    $Latencies = [System.Collections.Generic.List[double]]::new()
    $SuccessCount = 0
    $FailCount = 0

    foreach ($Domain in $DomainsToTest) {
        for ($i = 0; $i -lt $Iterations; $i++) {
            $Stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
            try {
                $Resolution = Resolve-DnsName -Name $Domain -Server $ServerIp -Type A -DnsOnly -QuickTimeout -ErrorAction Stop
                $Stopwatch.Stop()
                if ($Resolution) {
                    $SuccessCount++
                    $Latencies.Add($Stopwatch.Elapsed.TotalMilliseconds)
                }
            } catch {
                $Stopwatch.Stop()
                $FailCount++
            }
        }
    }

    if ($Latencies.Count -gt 0) {
        $Avg = [math]::Round(($Latencies | Measure-Object -Average).Average, 2)
        $Min = [math]::Round(($Latencies | Measure-Object -Minimum).Minimum, 2)
        $Max = [math]::Round(($Latencies | Measure-Object -Maximum).Maximum, 2)

        Write-Host "COMPLETADO (Promedio: ${Avg}ms)" -ForegroundColor Green

        $Results.Add([PSCustomObject]@{
            "Proveedor_DNS" = $Name
            "IP_Servidor"   = $ServerIp
            "Latencia_Prom" = $Avg
            "Latencia_Min"  = $Min
            "Latencia_Max"  = $Max
            "Exito"         = "$SuccessCount / $($SuccessCount + $FailCount)"
        })
    } else {
        Write-Host "FALLO TOTAL (Timeout o Inalcanzable)" -ForegroundColor Red
        $Results.Add([PSCustomObject]@{
            "Proveedor_DNS" = $Name
            "IP_Servidor"   = $ServerIp
            "Latencia_Prom" = 9999
            "Latencia_Min"  = 9999
            "Latencia_Max"  = 9999
            "Exito"         = "0 / $($SuccessCount + $FailCount) [OFFLINE]"
        })
    }
}

Write-Host "`n=================================================================" -ForegroundColor Cyan
Write-Host "                 RANKING DE VELOCIDAD DNS                       " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

$Sorted = $Results | Sort-Object -Property Latencia_Prom
$Sorted | Format-Table -Property Proveedor_DNS, IP_Servidor, @{Label="Promedio (ms)"; Expression={$_.Latencia_Prom}}, @{Label="Minimo (ms)"; Expression={$_.Latencia_Min}}, @{Label="Maximo (ms)"; Expression={$_.Latencia_Max}}, Exito -AutoSize

$Fastest = $Sorted[0]
if ($Fastest.Latencia_Prom -lt 9999) {
    Write-Host "EL SERVIDOR MAS RAPIDO ES : $($Fastest.Proveedor_DNS) ($($Fastest.IP_Servidor)) con $($Fastest.Latencia_Prom) ms!" -ForegroundColor Green
    Write-Host "Configurar este servidor reducira significativamente el tiempo de carga de paginas web y APIs." -ForegroundColor White
}
Write-Host "=================================================================`n" -ForegroundColor Cyan
