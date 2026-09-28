<#
.SYNOPSIS
    Auditor y Extractor de Perfiles y Claves Wi-Fi Almacenadas en Windows.
.DESCRIPTION
    Recupera todas las redes inalambricas guardadas en el sistema operativo,
    extrayendo el tipo de autenticacion, cifrado y contrasenas en texto claro.
    Herramienta esencial para auditoria de seguridad, migracion de equipos y soporte.
#>

param(
    [switch]$ExportToFile
)

Clear-Host
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "         EXTRACTOR Y AUDITOR DE CLAVES WI-FI EN WINDOWS         " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

Write-Host "Consultando perfiles de red inalambrica almacenados en el sistema...`n" -ForegroundColor DarkGray

$ProfilesRaw = netsh wlan show profiles
$ProfileNames = [System.Collections.Generic.List[string]]::new()

foreach ($Line in $ProfilesRaw) {
    if ($Line -match ":\s*(.+)$") {
        $Name = $Matches[1].Trim()
        if (-not ($Name -match "^<" -or $Name -eq "")) {
            $ProfileNames.Add($Name)
        }
    }
}

if ($ProfileNames.Count -eq 0) {
    Write-Host "[INFO] No se encontraron perfiles de Wi-Fi almacenados en este equipo." -ForegroundColor Yellow
    return
}

$Results = [System.Collections.Generic.List[PSCustomObject]]::new()

foreach ($PName in $ProfileNames) {
    $Detail = netsh wlan show profile name="$PName" key=clear
    $Auth = "Desconocida"
    $Cipher = "Desconocido"
    $Key = "[SIN CLAVE / ABIERTA O 802.1X]"

    foreach ($DLine in $Detail) {
        $Trimmed = $DLine.Trim()
        if ($Trimmed -match "^Autenticaci[oó]n\s+:\s*(.*)$" -or $Trimmed -match "^Authentication\s+:\s*(.*)$") {
            $Auth = $Matches[1].Trim()
        }
        elseif ($Trimmed -match "^Cifrado\s+:\s*(.*)$" -or $Trimmed -match "^Cipher\s+:\s*(.*)$") {
            $Cipher = $Matches[1].Trim()
        }
        elseif ($Trimmed -match "^Contenido de la clave\s+:\s*(.*)$" -or $Trimmed -match "^Key Content\s+:\s*(.*)$") {
            $Key = $Matches[1].Trim()
        }
    }

    $Results.Add([PSCustomObject]@{
        "Perfil_SSID"  = $PName
        "Autenticacion"= $Auth
        "Cifrado"      = $Cipher
        "Contrasena"   = $Key
    })
}

Write-Host "TOTAL DE PERFILES WI-FI RECUPERADOS: $($Results.Count)`n" -ForegroundColor White
$Results | Format-Table -AutoSize

if ($ExportToFile -or (Read-Host "`nDesea exportar estas credenciales a un archivo de texto? (s/n)") -eq "s") {
    $DateStr = Get-Date -Format "yyyyMMdd_HHmmss"
    $OutPath = Join-Path -Path $PSScriptRoot -ChildPath "Wifi_Passwords_Backup_${DateStr}.txt"

    $FileContent = @"
===============================================================================
REPORTE DE AUDITORIA DE PERFILES Y CLAVES WI-FI (WINDOWS)
Generado el: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Equipo     : $env:COMPUTERNAME | Usuario: $env:USERNAME
===============================================================================

"@
    foreach ($Item in $Results) {
        $FileContent += "SSID / Perfil : $($Item.Perfil_SSID)`n"
        $FileContent += "Autenticacion : $($Item.Autenticacion)`n"
        $FileContent += "Cifrado       : $($Item.Cifrado)`n"
        $FileContent += "Contrasena    : $($Item.Contrasena)`n"
        $FileContent += "-------------------------------------------------------------------------------`n"
    }

    $FileContent | Out-File -FilePath $OutPath -Encoding utf8
    Write-Host "[EXITO] Reporte guardado de forma segura en: $OutPath" -ForegroundColor Green
}

Write-Host "=================================================================`n" -ForegroundColor Cyan
