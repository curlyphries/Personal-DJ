<#!
.SYNOPSIS
    Guides you through building and running the AI-DJ container with the right ENV vars & volume mount.

.DESCRIPTION
    1. Checks for required services (Docker, Ollama)
    2. Prompts for ELEVEN API key (optional), voice ID, and local music folder.
    3. Builds the Docker image (cached on subsequent runs).
    4. Runs the container with interactive CLI, passing the ENV vars and mounting the music dir read-only.

.NOTES
    Requires Docker Desktop running on Windows / WSL.
    If Ollama is already running on the host, it can be used instead of installing in the container.
#>

param(
    [string]$ImageName = "ai-dj"
)

# ---------------------------
# 0️⃣  Check prerequisites
# ---------------------------
# Check if Docker is running
try {
    $null = docker info 2>&1  # Discard output, just check exit code
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Docker is not running or not installed. Please start Docker Desktop first." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Docker is not installed or not in PATH. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check for Ollama server
$ollamaRunning = $false
$ollamaHost = $null
$ollamaPort = 11434

# Function to test Ollama server connection
function Test-OllamaServer {
    param([string]$server, [int]$port)
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $connect = $tcpClient.BeginConnect($server, $port, $null, $null)
        $success = $connect.AsyncWaitHandle.WaitOne(1000, $false)
        if ($success) {
            $tcpClient.EndConnect($connect) | Out-Null
            $tcpClient.Close()
            return $true
        }
    } catch {
        # Ignore errors, server is not reachable
    }
    return $false
}

# Check if Ollama CLI is available
$ollamaCliAvailable = $false
if (Get-Command -Name ollama -ErrorAction SilentlyContinue) {
    try {
        $ollamaVersion = ollama --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $ollamaCliAvailable = $true
            Write-Host "✅ Found Ollama CLI: $ollamaVersion" -ForegroundColor Green
        }
    } catch {
        # Ollama command exists but failed to run
    }
}

# Check if Ollama server is running locally
$localOllamaRunning = Test-OllamaServer -server "localhost" -port $ollamaPort

if ($localOllamaRunning) {
    Write-Host "✅ Ollama server is running on localhost:$ollamaPort" -ForegroundColor Green
    $useLocalOllama = Read-Host "Use local Ollama server (localhost:$ollamaPort)? [Y/n]"
    if ($useLocalOllama -ne 'n' -and $useLocalOllama -ne 'N') {
        $ollamaRunning = $true
        $ollamaHost = "host.docker.internal"
    }
}

# If not using local Ollama, check for custom server
if (-not $ollamaRunning) {
    Write-Host ""
    Write-Host "Ollama server configuration:" -ForegroundColor Cyan
    Write-Host "1. Use default (install inside container)"
    if ($ollamaCliAvailable) {
        Write-Host "2. Start local Ollama server (if not running)"
    }
    Write-Host "3. Use custom Ollama server (e.g., http://192.168.1.100:11434)"
    
    $choice = Read-Host "Choose an option [1-3]"
    
    switch ($choice) {
        "2" {
            if ($ollamaCliAvailable) {
                Write-Host "🚀 Starting Ollama server..." -ForegroundColor Cyan
                Start-Process -NoNewWindow -FilePath "ollama" -ArgumentList "serve"
                Start-Sleep -Seconds 2  # Give it a moment to start
                
                if (Test-OllamaServer -server "localhost" -port $ollamaPort) {
                    $ollamaRunning = $true
                    $ollamaHost = "host.docker.internal"
                    Write-Host "✅ Ollama server started successfully" -ForegroundColor Green
                } else {
                    Write-Host "❌ Failed to start Ollama server" -ForegroundColor Red
                }
            }
        }
        "3" {
            $customServer = Read-Host "Enter Ollama server URL (e.g., http://192.168.1.100:11434)"
            if ($customServer -match '^(https?://)?([^/:]+)(?::(\d+))?$') {
                $serverHost = $matches[2]
                $serverPort = if ($matches[3]) { [int]$matches[3] } else { 11434 }
                
                if (Test-OllamaServer -server $serverHost -port $serverPort) {
                    $ollamaRunning = $true
                    $ollamaHost = $serverHost
                    if ($serverPort -ne 11434) {
                        $ollamaHost += ":$serverPort"
                    }
                    Write-Host "✅ Connected to Ollama server at $ollamaHost" -ForegroundColor Green
                } else {
                    Write-Host "❌ Could not connect to Ollama server at $serverHost`:$serverPort" -ForegroundColor Red
                }
            } else {
                Write-Host "❌ Invalid server format. Please use format: http(s)://hostname:port" -ForegroundColor Red
            }
        }
    }
}

Write-Host "`n=== AI-DJ Container Setup ===`n" -ForegroundColor Cyan

# ---------------------------
# 1️⃣  Collect config inputs
# ---------------------------
$apiKey = Read-Host "Enter ELEVEN_API_KEY (leave blank to skip TTS)"
$voiceId = Read-Host "ElevenLabs VOICE_ID  [default: eleven_monolingual_v1]"
if ([string]::IsNullOrWhiteSpace($voiceId)) { $voiceId = "eleven_monolingual_v1" }

$musicDir = Read-Host "Absolute path to your local MP3 folder"
if (-not (Test-Path $musicDir)) {
    Write-Host "Directory not found: $musicDir" -ForegroundColor Red
    exit 1
}

# Normalise Windows path to Docker mount (C:\foo → /c/foo)
function Convert-PathForDocker($path) {
    $p = (Resolve-Path $path).ProviderPath
    $p = $p -replace "\\", "/"      # backslashes → slashes
    # C:/Users → /c/Users for Docker Desktop
    if ($p -match "^[A-Za-z]:/") { $p = "/" + $p.Substring(0,1).ToLower() + $p.Substring(2) }
    return $p
}
$dockerMountPath = Convert-PathForDocker $musicDir

# Ensure Docker builds from project root (parent of this script directory)
$projectRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
Push-Location $projectRoot

# ---------------------------
# 2️⃣  Build image (cached)
# ---------------------------
$buildArgs = @()
if (-not $ollamaRunning) {
    Write-Host "ℹ️  Will install Ollama inside container" -ForegroundColor Cyan
} else {
    Write-Host "ℹ️  Using host's Ollama service" -ForegroundColor Cyan
    $buildArgs += @("--build-arg", "INSTALL_OLLAMA=false")
}

Write-Host "`n> docker build -t $ImageName $($buildArgs -join ' ') ." -ForegroundColor Yellow
& docker build -t $ImageName $buildArgs .
if ($LASTEXITCODE -ne 0) { Pop-Location; exit $LASTEXITCODE }

# ---------------------------
# 3️⃣  Run container interactively
# ---------------------------
$envArgs = @("--env", "MUSIC_DIR=/music")
if ($apiKey) { $envArgs += @("--env", "ELEVEN_API_KEY=$apiKey") }
if ($voiceId) { $envArgs += @("--env", "ELEVEN_VOICE_ID=$voiceId") }

# If using host's Ollama, add host networking and OLLAMA_HOST
if ($ollamaRunning) {
    $envArgs += @("--network", "host")
    $envArgs += @("--env", "OLLAMA_HOST=$ollamaHost")
    Write-Host "🔌 Using host's Ollama service at $ollamaHost" -ForegroundColor Cyan
    Write-Host "   (Make sure Ollama is running and accessible from containers)" -ForegroundColor Cyan
}

# Build the Docker run command
$dockerCmd = @("docker", "run", "-it") + $envArgs + @("-v", "${dockerMountPath}:/music:ro", $ImageName)

# Display the command being run
Write-Host ""
Write-Host "> $($dockerCmd -join ' ')" -ForegroundColor Yellow

# Execute the command
& $dockerCmd

Pop-Location
