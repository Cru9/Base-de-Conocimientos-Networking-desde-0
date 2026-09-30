<#
.SYNOPSIS
    Auditor de Reglas de Entrada de Windows Defender Firewall.
.DESCRIPTION
    Herramienta de Hardening y Ciberseguridad. Analiza todas las reglas de entrada activas,
    identificando puertos de alto riesgo expuestos hacia cualquier origen (0.0.0.0/0 o Any),
    tales como RDP (3389), SMB (445), WinRM (5985/5986), Telnet (23) o VNC (5900).
    Genera un informe con recomendaciones de mitigacion.
.NOTES
    Modulo: Firewalls_y_VPN / Ciberseguridad_OSI
    Autor: Cru9 - BC Compendium
#>

[CmdletBinding()]
param(
    [string]$RutaExportacionCSV = "$PSScriptRoot\Auditoria_Firewall_Reporte.csv"
)

Clear-Host
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       BC FIREWALL SECURITY - AUDITOR DE REGLAS DE ENTRADA (WINDOWS)" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$PuertosCriticos = @{
    "21"   = "FTP (Texto claro)"
    "23"   = "Telnet (Inseguro - Credenciales sin cifrar)"
    "445"  = "SMB (Riesgo critico de ransomware / WannaCry / Lateral Movement)"
    "135"  = "RPC Endpoint Mapper (Vulnerable a relay/reconocimiento)"
    "139"  = "NetBIOS Session Service"
    "3389" = "RDP (Escritorio Remoto - Riesgo de fuerza bruta si es publico)"
    "5985" = "WinRM HTTP (Administracion remota sin TLS)"
    "5986" = "WinRM HTTPS"
    "5900" = "VNC Server"
    "1433" = "Microsoft SQL Server"
}

Write-Host "[*] Extrayendo reglas de entrada activas (Inbound Allow)..." -ForegroundColor Yellow
$reglas = Get-NetFirewallRule -Direction Inbound -Enabled True -Action Allow -ErrorAction Stop

Write-Host "[*] Total de reglas de entrada activas encontradas: $($reglas.Count)" -ForegroundColor Gray
Write-Host "[*] Analizando exposicion de puertos criticos...`n" -ForegroundColor Gray

$hallazgos = @()

foreach ($regla in $reglas) {
    $portFilter = $regla | Get-NetFirewallPortFilter -ErrorAction SilentlyContinue
    $addrFilter = $regla | Get-NetFirewallAddressFilter -ErrorAction SilentlyContinue

    if ($portFilter -and $portFilter.LocalPort) {
        $puertos = $portFilter.LocalPort
        $remoto = if ($addrFilter.RemoteAddress) { ($addrFilter.RemoteAddress -join ", ") } else { "Any" }

        foreach ($p in $puertos) {
            if ($PuertosCriticos.ContainsKey($p.ToString())) {
                $descripcionRiesgo = $PuertosCriticos[$p.ToString()]
                $esAny = ($remoto -match "Any" -or $remoto -eq "*" -or $remoto -eq "0.0.0.0/0")

                $nivelAlerta = if ($esAny) { "ALTO (Expuesto a Any)" } else { "MEDIO (Restringido)" }

                $hallazgos += [PSCustomObject]@{
                    Nombre_Regla  = $regla.DisplayName
                    Perfil        = ($regla.Profile -join ", ")
                    Protocolo     = $portFilter.Protocol
                    Puerto_Local  = $p
                    Origen_Remoto = $remoto
                    Servicio      = $descripcionRiesgo
                    Nivel_Riesgo  = $nivelAlerta
                }
            }
        }
    }
}

if ($hallazgos.Count -eq 0) {
    Write-Host "[EXCELENTE] No se encontraron reglas de entrada que expongan puertos criticos predefinidos." -ForegroundColor Green
} else {
    Write-Host "[!] HALLAZGOS DE SEGURIDAD EN REGLAS DE FIREWALL:" -ForegroundColor Red
    $hallazgos | Sort-Object Nivel_Riesgo -Descending | Format-Table Nombre_Regla, Protocolo, Puerto_Local, Origen_Remoto, Nivel_Riesgo, Servicio -AutoSize

    try {
        $hallazgos | Export-Csv -Path $RutaExportacionCSV -NoTypeInformation -Encoding UTF8
        Write-Host "`n[OK] Reporte exportado a: $RutaExportacionCSV" -ForegroundColor Green
    } catch {
        Write-Host "`n[!] No se pudo guardar el archivo CSV: $($_.Exception.Message)" -ForegroundColor Yellow
    }

    Write-Host "`nRecomendaciones de Hardening:" -ForegroundColor Cyan
    Write-Host "  1. Si un puerto como SMB (445) o RDP (3389) debe estar abierto, restringir 'Origen_Remoto' a IPs de gestion exclusivas." -ForegroundColor Gray
    Write-Host "  2. Deshabilitar reglas asociadas al perfil 'Public' en laptops o estaciones móviles." -ForegroundColor Gray
    Write-Host "  3. Reemplazar Telnet (23) o WinRM HTTP (5985) por protocolos cifrados SSH o WinRM HTTPS (5986)." -ForegroundColor Gray
}

Write-Host ""
Write-Host "Presione una tecla para continuar..." -ForegroundColor Gray
[System.Console]::ReadKey() | Out-Null
