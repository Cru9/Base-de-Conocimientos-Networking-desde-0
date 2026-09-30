# ==============================================================================
# PyEDC - Lanzador y Configuración Automática para PowerShell
# ==============================================================================

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host " 🏛️ PyEDC - Instalador y Lanzador Automático (PowerShell)" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[ERROR] Python no está instalado o no se encuentra en el PATH." -ForegroundColor Red
    Write-Host "Descárgalo e instálalo desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host 'Recuerda marcar "Add python.exe to PATH" en el instalador.' -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir..."
    exit 1
}

# 2. Verificar o crear el entorno virtual
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "[1/3] Creando entorno virtual (.venv)..." -ForegroundColor Yellow
    python -m venv .venv

    if (-not (Test-Path $venvPython)) {
        Write-Host "[ERROR] Falló la creación del entorno virtual." -ForegroundColor Red
        Read-Host "Presiona Enter para salir..."
        exit 1
    }
    Write-Host "[OK] Entorno virtual creado exitosamente." -ForegroundColor Green

    Write-Host "[2/3] Instalando dependencias desde requirements.txt..." -ForegroundColor Yellow
    & $venvPython -m pip install --upgrade pip --quiet
    & $venvPython -m pip install -r requirements.txt

    Write-Host "[OK] Todas las librerías se instalaron correctamente." -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[OK] Entorno virtual (.venv) listo." -ForegroundColor Green
}

# 3. Ejecutar PyEDC
Write-Host "[3/3] Iniciando la suite PyEDC..." -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

& $venvPython run.py
