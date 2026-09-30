<#
.SYNOPSIS
    Verificador de Politicas de QoS (Calidad de Servicio) y Marcado DSCP en Windows.
.DESCRIPTION
    Inspecciona las directivas de QoS configuradas en el sistema (NetQosPolicy),
    el marcado de paquetes DiffServ / DSCP (RFC 4594), la asignacion de prioridad
    para aplicaciones criticas (VoIP, Video, Gestion de Red) y el estado en el Registro
    de Windows para el marcado de campos ToS/DSCP (DisableUserTOSSetting).
.NOTES
    Modulo: QoS_Traffic_Shaping / Telefonia
    Autor: Cru9 - BC Compendium
#>

Clear-Host
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "       BC NETWORK - VERIFICADOR DE POLITICAS QOS Y MARCADO DSCP" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "--- DIRECTIVAS DE CALIDAD DE SERVICIO (QOS) ACTIVAS EN WINDOWS ---" -ForegroundColor Yellow
$politicas = Get-NetQosPolicy -ErrorAction SilentlyContinue

if ($politicas) {
    $politicas | Select-Object Name, DSCPAction, ThrottleRateActionBitsPerSecond, AppPathName, IPProtocol, PriorityValue8021Action | Format-Table -AutoSize
} else {
    Write-Host "[i] No se encontraron directivas de QoS locales configuradas mediante PowerShell." -ForegroundColor Gray
}

# Tabla de Correspondencia DSCP Enterprise
Write-Host "`n--- REFERENCIA RAPIDA DIFFSERV / DSCP (RFC 4594) ---" -ForegroundColor Yellow
$dscpRef = @(
    [PSCustomObject]@{ Valor_DSCP = 46; Nombre = "EF (Expedited Forwarding)"; Aplicacion = "Voz sobre IP (Audio RTP) - Minimo Jitter"; Prioridad = "Critica" },
    [PSCustomObject]@{ Valor_DSCP = 34; Nombre = "AF41 (Assured Forwarding)"; Aplicacion = "Videoconferencia Interactiva (Zoom, Teams)"; Prioridad = "Alta" },
    [PSCustomObject]@{ Valor_DSCP = 26; Nombre = "AF31"; Aplicacion = "Streaming Multimedia"; Prioridad = "Media-Alta" },
    [PSCustomObject]@{ Valor_DSCP = 18; Nombre = "AF21"; Aplicacion = "Datos Transaccionales (ERP, SQL)"; Prioridad = "Media" },
    [PSCustomObject]@{ Valor_DSCP = 48; Nombre = "CS6 (Network Control)"; Aplicacion = "Protocolos de Enrutamiento (OSPF, BGP)"; Prioridad = "Infraestructura" },
    [PSCustomObject]@{ Valor_DSCP = 0;  Nombre = "CS0 / Best Effort"; Aplicacion = "Trafico estandar por defecto"; Prioridad = "Normal" }
)
$dscpRef | Format-Table -AutoSize

# Auditoria de marcado en registro de Windows
Write-Host "--- VERIFICACION DE VALORES EN REGISTRO DE WINDOWS ---" -ForegroundColor Yellow
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters"
$tosVal = (Get-ItemProperty -Path $regPath -Name "DisableUserTOSSetting" -ErrorAction SilentlyContinue).DisableUserTOSSetting

if ($null -eq $tosVal) {
    Write-Host "[INFO] 'DisableUserTOSSetting' no esta presente en el registro (Comportamiento predeterminado)." -ForegroundColor Gray
} elseif ($tosVal -eq 0) {
    Write-Host "[OK] 'DisableUserTOSSetting' = 0: El marcado de paquetes DSCP/TOS esta PERMITIDO para aplicaciones." -ForegroundColor Green
} else {
    Write-Host "[AVISO] 'DisableUserTOSSetting' = 1: Windows ignora el marcado TOS de aplicaciones no privilegiadas." -ForegroundColor Yellow
}

Write-Host "`nPresione una tecla para continuar..." -ForegroundColor Gray
[System.Console]::ReadKey() | Out-Null
