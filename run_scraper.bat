@echo off
REM ===================================================
REM Script para ejecutar el scraper de precios
REM ===================================================

cd /d "%~dp0"

REM Verifica si existe el entorno virtual
if exist "venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo ADVERTENCIA: No se encontro el entorno virtual en venv\
    echo Usando Python del sistema...
)

REM Ejecuta el scraper
echo Ejecutando scraper...
python scraper.py

REM Pausa opcional (comentar si se ejecuta desde Task Scheduler)
REM pause
