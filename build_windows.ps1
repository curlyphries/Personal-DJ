# Build script to create standalone Windows installer for Personal DJ
# -------------------------------------------------------------------
# 1. Creates/activates a temporary virtual environment under .venv-build
# 2. Installs Windows requirements
# 3. Uses PyInstaller to generate a single-file executable (dist/ai-dj.exe)
# 4. Invokes Inno Setup compiler (ISCC.exe) to package the installer
# -------------------------------------------------------------------

param(
    [string]$PyVersion = "python",
    [string]$InnoCompiler = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
)

$ErrorActionPreference = 'Stop'
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "==> Building Personal DJ Windows installer" -ForegroundColor Cyan

# --- 1. Virtual environment ---
$venvPath = Join-Path $scriptRoot ".venv-build"
if (-Not (Test-Path $venvPath)) {
    & $PyVersion -m venv $venvPath
}

$activate = Join-Path $venvPath "Scripts/Activate.ps1"
. $activate

# --- 2. Dependencies ---
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -r "$scriptRoot/requirements-win.txt"
pip install pyinstaller

# --- 3. PyInstaller build ---
Write-Host "Running PyInstaller..." -ForegroundColor Cyan
pyinstaller --noconfirm --onefile --name ai-dj --add-data "config;config" "$scriptRoot/run.py"

if (-Not (Test-Path "$scriptRoot/dist/ai-dj.exe")) {
    Write-Host "PyInstaller failed – executable not found" -ForegroundColor Red
    exit 1
}

Write-Host "PyInstaller build complete." -ForegroundColor Green

# --- 4. Inno Setup ---
if (-Not (Test-Path $InnoCompiler)) {
    Write-Host "Inno Setup compiler not found at $InnoCompiler" -ForegroundColor Yellow
    $InnoCompiler = Read-Host "Enter full path to ISCC.exe"
}

if (Test-Path $InnoCompiler) {
    Write-Host "Compiling installer with Inno Setup..." -ForegroundColor Cyan
    & "$InnoCompiler" "$scriptRoot/installer.iss"
    if ($LASTEXITCODE -eq 0) {
        $out = "$scriptRoot/installer/AI-DJ-Setup.exe"
        if (Test-Path $out) {
            Write-Host "Installer ready at $out" -ForegroundColor Green
        }
    } else {
        Write-Host "Inno Setup compilation failed ($LASTEXITCODE)" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Inno Setup compiler not found. Install Inno Setup 6 first." -ForegroundColor Red
    exit 1
}
