# ===================================================
# Script de configuracion automatica para Task Scheduler
# Ejecutar como Administrador
# ===================================================

param(
    [string]$Hora = "09:00",
    [string]$Frecuencia = "Diaria"
)

Write-Host "=== Configurador de Tarea Programada - Chile Tech Price Tracker ===" -ForegroundColor Cyan
Write-Host ""

# Obtener la ruta del proyecto
$ProyectoPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptPath = Join-Path $ProyectoPath "run_scraper.bat"

# Verificar que existe el script BAT
if (-not (Test-Path $ScriptPath)) {
    Write-Host "ERROR: No se encontro run_scraper.bat en $ScriptPath" -ForegroundColor Red
    exit 1
}

Write-Host "Ruta del proyecto: $ProyectoPath" -ForegroundColor Green
Write-Host "Script a ejecutar: $ScriptPath" -ForegroundColor Green
Write-Host "Hora de ejecucion: $Hora" -ForegroundColor Green
Write-Host "Frecuencia: $Frecuencia" -ForegroundColor Green
Write-Host ""

# Nombre de la tarea
$TaskName = "ChileTechPriceTracker"

# Verificar si la tarea ya existe
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "La tarea '$TaskName' ya existe. Eliminando..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Crear la accion (ejecutar el BAT)
$Action = New-ScheduledTaskAction -Execute $ScriptPath -WorkingDirectory $ProyectoPath

# Crear el trigger segun la frecuencia
switch ($Frecuencia) {
    "Diaria" {
        $Trigger = New-ScheduledTaskTrigger -Daily -At $Hora
        Write-Host "Configurando ejecucion diaria a las $Hora" -ForegroundColor Cyan
    }
    "Semanal" {
        $Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At $Hora
        Write-Host "Configurando ejecucion semanal los lunes a las $Hora" -ForegroundColor Cyan
    }
    "Cada6Horas" {
        # Ejecutar 4 veces al dia (00:00, 06:00, 12:00, 18:00)
        $Trigger = @(
            New-ScheduledTaskTrigger -Daily -At "00:00"
            New-ScheduledTaskTrigger -Daily -At "06:00"
            New-ScheduledTaskTrigger -Daily -At "12:00"
            New-ScheduledTaskTrigger -Daily -At "18:00"
        )
        Write-Host "Configurando ejecucion cada 6 horas" -ForegroundColor Cyan
    }
    default {
        Write-Host "Frecuencia no valida. Usando 'Diaria' por defecto." -ForegroundColor Yellow
        $Trigger = New-ScheduledTaskTrigger -Daily -At $Hora
    }
}

# Configuracion principal de la tarea
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType S4U

# Configuracion adicional
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Registrar la tarea
try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Description "Rastreo automatico de precios de tecnologia en tiendas chilenas"
    Write-Host ""
    Write-Host "Tarea programada creada exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Puedes verificarla en:" -ForegroundColor Yellow
    Write-Host "  - Abre 'Programador de tareas' (taskschd.msc)" -ForegroundColor White
    Write-Host "  - Busca 'ChileTechPriceTracker'" -ForegroundColor White
    Write-Host ""
    Write-Host "Para ejecutar manualmente ahora:" -ForegroundColor Yellow
    Write-Host "  Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "ERROR al crear la tarea: $_" -ForegroundColor Red
    exit 1
}
