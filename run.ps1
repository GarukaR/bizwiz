# Run BizWiz locally in one command:  .\run.ps1
#
# Starts the database (Docker), the API (port 8010) and the web app (port 3010), then opens the
# browser. Press Ctrl+C to stop the API and web app. The database keeps running in Docker; stop it
# with `docker compose stop db`. Add -NoBrowser to skip opening the browser.

param([switch]$NoBrowser)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$apiPort = 8010
$webPort = 3010

# 1. Settings: create .env on the first run.
$envFile = Join-Path $root ".env"
if (-not (Test-Path $envFile)) {
    Copy-Item (Join-Path $root ".env.example") $envFile
    Write-Host "Created .env from .env.example." -ForegroundColor Yellow
}
$settings = Get-Content $envFile
$hasKey = $settings | Where-Object { $_ -match '^ANTHROPIC_API_KEY=\S+' }
$isFake = $settings | Where-Object { $_ -match '^ANSWERER=fake' }
if (-not $hasKey -and -not $isFake) {
    # No key yet: answer with the fake answerer instead of failing on every question.
    $env:ANSWERER = "fake"
    Write-Host "No ANTHROPIC_API_KEY in .env, so answers come from the fake answerer." -ForegroundColor Yellow
}

# 2. Stop early if something already holds our ports (usually an earlier run still going).
foreach ($port in $apiPort, $webPort) {
    if (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) {
        Write-Host "Port $port is already in use. Close the other BizWiz window (or whatever holds it) and try again." -ForegroundColor Red
        exit 1
    }
}

# 3. Database.
Write-Host "Starting the database..." -ForegroundColor Cyan
docker compose -f (Join-Path $root "docker-compose.yml") up -d --wait db
if ($LASTEXITCODE -ne 0) {
    Write-Host "The database didn't start. Is Docker Desktop running?" -ForegroundColor Red
    exit 1
}

# 4. Web app packages, only the first time.
$frontend = Join-Path $root "frontend"
if (-not (Test-Path (Join-Path $frontend "node_modules"))) {
    Write-Host "Installing web app packages (first run only)..." -ForegroundColor Cyan
    npm install --prefix $frontend
}

# 5. API and web app, both printing into this window.
Write-Host "Starting the API on port $apiPort and the web app on port $webPort..." -ForegroundColor Cyan
$api = Start-Process uv -ArgumentList "run", "bizwiz-api" -WorkingDirectory (Join-Path $root "backend") -NoNewWindow -PassThru
$web = Start-Process npm.cmd -ArgumentList "run", "dev", "--", "--port", "$webPort" -WorkingDirectory $frontend -NoNewWindow -PassThru

try {
    # Open the browser once the web app answers.
    $url = "http://localhost:$webPort"
    for ($i = 0; $i -lt 120; $i++) {
        try {
            Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 2 | Out-Null
            break
        } catch {
            if ($api.HasExited -or $web.HasExited) { throw "The API or web app stopped. See the errors above." }
            Start-Sleep -Seconds 1
        }
    }
    Write-Host "`nBizWiz is running at $url  (Ctrl+C to stop)`n" -ForegroundColor Green
    if (-not $NoBrowser) { Start-Process $url }
    while (-not ($api.HasExited -or $web.HasExited)) { Start-Sleep -Seconds 1 }
    Write-Host "The API or web app stopped. See the errors above." -ForegroundColor Red
} finally {
    # Stop both, including the processes they started (Python, Node).
    foreach ($p in $api, $web) {
        if (-not $p.HasExited) { try { taskkill /PID $p.Id /T /F 2>&1 | Out-Null } catch {} }
    }
    Write-Host "Stopped the API and web app." -ForegroundColor Cyan
}
