<#
.SYNOPSIS
    Gestor y Auditor de Perfiles de Windows Defender Firewall.
.DESCRIPTION
    Inspecciona y audita la postura de seguridad de los tres perfiles de red:
    Domain (Dominio), Private (Privada) y Public (Publica).
    Permite verificar acciones predeterminadas (Block/Allow) y activar proteccion estricta.
.NOTES
    Modulo: Firewalls_y_VPN / Ciberseguridad_OSI
    Autor: Cru9 - BC Compendium
#>

Clear-Host
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       BC FIREWALL SECURITY - GESTOR DE PERFILES DE WINDOWS DEFENDER" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$perfiles = Get-NetFirewallProfile -ErrorAction Stop

Write-Host "--- ESTADO DE LOS PERFILES DE FIREWALL ---" -ForegroundColor Yellow
$perfiles | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction, AllowInboundRules | Format-Table -AutoSize

# Auditoria de riesgo
$riesgos = @()
foreach ($p in $perfiles) {
    if (-not $p.Enabled) {
        $riesgos += "El perfil '$($p.Name)' esta DESACTIVADO (Riesgo Alto de intrusion)."
    }
    if ($p.DefaultInboundAction -eq 'Allow') {
        $riesgos += "El perfil '$($p.Name)' permite conexiones de entrada por defecto (Accion Inbound: Allow)."
    }
}

if ($riesgos) {
    Write-Host "[!] ADVERTENCIAS DE POSTURA DE SEGURIDAD:" -ForegroundColor Red
    foreach ($r in $riesgos) {
        Write-Host "  - $r" -ForegroundColor Yellow
    }
} else {
    Write-Host "[OK] Todos los perfiles de firewall estan activos y bloquean trafico de entrada no solicitado." -ForegroundColor Green
}

Write-Host "`n--- REGLAS DE ENTRADA BLOQUEADAS EXPLICITAMENTE (MUESTRA) ---" -ForegroundColor Yellow
Get-NetFirewallRule -Direction Inbound -Action Block -Enabled True -ErrorAction SilentlyContinue | Select-Object -First 5 | Format-Table DisplayName, Profile -AutoSize

Write-Host "Presione una tecla para continuar..." -ForegroundColor Gray
[System.Console]::ReadKey() | Out-Null
