@echo off
chcp 65001 >nul
title PyEDC - Enterprise Data & Connectivity Suite

echo =====================================================================
echo  🏛️ PyEDC - Instalador y Lanzador Automatico
echo =====================================================================
echo.

:: 1. Verificar si Python esta instalado en el sistema
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] No se encontro Python instalado en este equipo.
    echo Por favor descarga e instala Python 3.10 o superior desde:
    echo https://www.python.org/downloads/
    echo.
    echo Asegurate de marcar la casilla "Add python.exe to PATH" durante la instalacion.
    echo =====================================================================
    pause
    exit /b 1
)

:: 2. Verificar o crear el entorno virtual (.venv)
if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creando entorno virtual aislado (.venv)...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado con exito.
    echo.
    echo [2/3] Instalando todas las librerias necesarias (Rich, Pydantic, Jinja2, etc.)...
    .venv\Scripts\python.exe -m pip install --upgrade pip --quiet
    .venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
    if %errorlevel% neq 0 (
        echo [ERROR] Hubo un problema instalando las dependencias.
        pause
        exit /b 1
    )
    echo [OK] Todas las dependencias se instalaron correctamente.
    echo.
) else (
    echo [OK] Entorno virtual (.venv) detectado.
)

:: 3. Ejecutar PyEDC dentro del entorno virtual
echo [3/3] Iniciando PyEDC...
echo =====================================================================
echo.

.venv\Scripts\python.exe run.py

if %errorlevel% neq 0 (
    echo.
    echo [AVISO] La aplicacion finalizo con codigo de salida %errorlevel%.
    pause
)
