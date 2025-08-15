# Compile the Inno Setup installer
$innoCompiler = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
$scriptPath = "$PSScriptRoot\installer.iss"

if (-not (Test-Path $innoCompiler)) {
    Write-Host "Inno Setup compiler not found at $innoCompiler" -ForegroundColor Red
    $innoCompiler = Read-Host "Please enter the full path to ISCC.exe"
}

if (Test-Path $innoCompiler) {
    Write-Host "Compiling installer..." -ForegroundColor Cyan
    & "$innoCompiler" "$scriptPath"
    
    if ($LASTEXITCODE -eq 0) {
        $outputPath = "$PSScriptRoot\installer\AI-DJ-Setup.exe"
        if (Test-Path $outputPath) {
            Write-Host "✅ Installer created successfully at:" -ForegroundColor Green
            Write-Host $outputPath -ForegroundColor Cyan
            
            # Open the installer location in File Explorer
            explorer "/select,$outputPath"
        } else {
            Write-Host "❌ Error: Installer not found at expected location" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Error compiling installer (Exit code: $LASTEXITCODE)" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Inno Setup compiler not found. Please install Inno Setup first." -ForegroundColor Red
}

# Keep the window open
Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
