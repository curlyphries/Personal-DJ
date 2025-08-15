<#
.SYNOPSIS
    Simple script to run the AI-DJ container
#>

# Check if Docker is running
try {
    $null = docker info 2>&1
} catch {
    Write-Host "❌ Docker is not running or not installed. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Get inputs
$apiKey = Read-Host "Enter ELEVEN_API_KEY (leave blank to skip TTS)"
$voiceId = Read-Host "ElevenLabs VOICE_ID [default: eleven_monolingual_v1]"
if ([string]::IsNullOrWhiteSpace($voiceId)) { $voiceId = "eleven_monolingual_v1" }

$musicDir = Read-Host "Absolute path to your local MP3 folder"
if (-not (Test-Path $musicDir)) {
    Write-Host "Directory not found: $musicDir" -ForegroundColor Red
    exit 1
}

# Convert Windows path to Docker format
$dockerMountPath = $musicDir -replace '^([A-Z]):', '/$1$1' -replace '\\', '/'

# Build Docker command
$dockerCmd = @(
    "docker", "run", "-it",
    "--env", "MUSIC_DIR=/music",
    "--env", "ELEVEN_VOICE_ID=$voiceId"
)

if (-not [string]::IsNullOrWhiteSpace($apiKey)) {
    $dockerCmd += @("--env", "ELEVEN_API_KEY=$apiKey")
}

# Always use host's Ollama
$dockerCmd += @(
    "--network", "host",
    "--env", "OLLAMA_HOST=host.docker.internal",
    "-v", "${dockerMountPath}:/music:ro",
    "ai-dj"
)

# Display and run
Write-Host "`nRunning: $($dockerCmd -join ' ')" -ForegroundColor Yellow
& $dockerCmd
