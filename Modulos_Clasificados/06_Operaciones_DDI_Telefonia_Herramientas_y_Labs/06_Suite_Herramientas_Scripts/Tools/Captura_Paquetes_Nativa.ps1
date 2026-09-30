<#
.SYNOPSIS
    Capturador Nativo de Paquetes de Red para Windows (netsh trace).
.DESCRIPTION
    Permite iniciar y detener grabaciones forenses de paquetes de red en servidores y clientes
    Windows SIN instalar ningun software de terceros (ni WinPcap, ni Npcap, ni Wireshark).
    Genera un archivo .etl con buffer circular seguro que puede convertirse a .pcapng.
    * Requiere privilegios de Administrador.
#>

param(
    [int]$MaxSizeBytes = 250MB
)

Clear-Host
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "         CAPTURADOR NATIVO DE TRAFICO DE RED (NETSH TRACE)       " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

# Validar permisos de Administrador
$IsAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $IsAdmin) {
    Write-Host "[ERROR CRITICO] Este script requiere privilegios elevados de Administrador." -ForegroundColor Red
    Write-Host "Por favor cierre esta ventana, haga clic derecho sobre PowerShell y elija:" -ForegroundColor Yellow
    Write-Host "   'Ejecutar como administrador'`n" -ForegroundColor White
    return
}

Write-Host "Seleccione la accion a realizar:" -ForegroundColor White
Write-Host "1. INICIAR Captura de Paquetes (Buffer Circular)" -ForegroundColor Green
Write-Host "2. DETENER Captura de Paquetes y Finalizar Archivo" -ForegroundColor Red
Write-Host "3. Consultar Estado Actual de Captura" -ForegroundColor Cyan
$Opt = Read-Host "Opcion (1, 2 o 3)"

switch ($Opt) {
    "1" {
        $DateStr = Get-Date -Format "yyyyMMdd_HHmmss"
        $TraceFile = Join-Path -Path $PSScriptRoot -ChildPath "Captura_Windows_${DateStr}.etl"
        $MaxSizeMB = [math]::Round($MaxSizeBytes / 1MB)

        Write-Host "`nIniciando captura de paquetes en: $TraceFile" -ForegroundColor Cyan
        Write-Host "Tamano maximo de buffer circular: ${MaxSizeMB} MB (No saturara el disco duro)..." -ForegroundColor DarkGray

        # Comando netsh nativo
        netsh trace start capture=yes persistent=no maxsize=$MaxSizeMB filemode=circular tracefile="$TraceFile" report=disabled

        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n[EXITO] ¡Captura de red iniciada correctamente!" -ForegroundColor Green
            Write-Host "El sistema esta grabando todas las tramas de todos los adaptadores de red." -ForegroundColor White
            Write-Host "Reproduzca el problema o trafico a investigar." -ForegroundColor Yellow
            Write-Host "Cuando termine, ejecute nuevamente este script y elija la Opcion 2 (DETENER).`n" -ForegroundColor Yellow
        } else {
            Write-Host "`n[ERROR] No se pudo iniciar la captura. Es posible que ya exista una sesion activa." -ForegroundColor Red
        }
    }

    "2" {
        Write-Host "`nDeteniendo sesion de captura de red... Espere a que Windows consolide los buffers..." -ForegroundColor Yellow
        netsh trace stop

        Write-Host "`n[EXITO] Captura detenida y finalizada." -ForegroundColor Green
        Write-Host "Los archivos resultantes (.etl y .cab) se encuentran en la carpeta de este script." -ForegroundColor White
        Write-Host "`nCOMO ABRIR ESTE ARCHIVO EN WIRESHARK:" -ForegroundColor Cyan
        Write-Host "-----------------------------------------------------------------" -ForegroundColor DarkGray
        Write-Host "1. El archivo nativo de Windows tiene extension .etl" -ForegroundColor White
        Write-Host "2. Para convertirlo a .pcapng estandar de Wireshark, puede utilizar la" -ForegroundColor White
        Write-Host "   herramienta gratuita y de codigo abierto de Microsoft 'etl2pcapng':" -ForegroundColor White
        Write-Host "   Comando: etl2pcapng.exe Captura_Windows.etl salida.pcapng" -ForegroundColor Gray
        Write-Host "3. O bien abrirlo directamente en Microsoft Message Analyzer / Event Viewer." -ForegroundColor White
    }

    "3" {
        Write-Host "`nConsultando estado del subsistema de rastreo de red..." -ForegroundColor Cyan
        netsh trace show status
    }

    default {
        Write-Host "[INFO] Opcion cancelada." -ForegroundColor Yellow
    }
}

Write-Host "=================================================================`n" -ForegroundColor Cyan
