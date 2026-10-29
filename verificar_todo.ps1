$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$Python = Join-Path $Root ".venv\\Scripts\\python.exe"

if (-not (Test-Path $Python)) {
    Write-Host "No se encontro el Python del entorno .venv." -ForegroundColor Red
    Write-Host "Ejecuta: python -m venv .venv" -ForegroundColor Blue
    Write-Host "Luego: .\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt" -ForegroundColor Blue
    exit 1
}

Set-Location $Root
Write-Host "`n1. CARGA DE CSV" -ForegroundColor Blue
& $Python "cargar_csv.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n2. ESCENARIOS E01-E15" -ForegroundColor Blue
& $Python "ejecutar_escenarios.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n3. PRUEBAS AUTOMATIZADAS" -ForegroundColor Blue
& $Python -m pytest -q --color=yes
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nVerificacion completa: todas las comprobaciones terminaron correctamente." -ForegroundColor Green
