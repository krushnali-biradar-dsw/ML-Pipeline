# Setup script for MLflow + MinIO + Seldon Core Pipeline
# Run this script as Administrator

Write-Host "🚀 Starting MLflow + MinIO + Seldon Core Pipeline Setup" -ForegroundColor Green

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

$prerequisites = @("docker", "kubectl", "helm", "minikube")
$missing = @()

foreach ($cmd in $prerequisites) {
    if (Test-Command $cmd) {
        Write-Host "✅ $cmd is installed" -ForegroundColor Green
    } else {
        Write-Host "❌ $cmd is NOT installed" -ForegroundColor Red
        $missing += $cmd
    }
}

if ($missing.Count -gt 0) {
    Write-Host "❌ Missing prerequisites: $($missing -join ', ')" -ForegroundColor Red
    Write-Host "Please install missing tools and run this script again." -ForegroundColor Red
    exit 1
}

# Start Minikube
Write-Host "🏁 Starting Minikube..." -ForegroundColor Yellow
minikube start --memory=8192 --cpus=4

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start Minikube" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Minikube started successfully" -ForegroundColor Green

# Start Docker Compose services
Write-Host "🐳 Starting MLflow and MinIO services..." -ForegroundColor Yellow
docker compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start Docker Compose services" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker services started successfully" -ForegroundColor Green

# Wait for services to be ready
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check service health
Write-Host "🏥 Checking service health..." -ForegroundColor Yellow

# Check MinIO
try {
    $minio_health = Invoke-WebRequest -Uri "http://localhost:9000/minio/health/live" -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ MinIO is healthy" -ForegroundColor Green
} catch {
    Write-Host "⚠️  MinIO might not be ready yet, check manually at http://localhost:9001" -ForegroundColor Yellow
}

# Check MLflow
try {
    $mlflow_health = Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ MLflow is healthy" -ForegroundColor Green
} catch {
    Write-Host "⚠️  MLflow might not be ready yet, check manually at http://localhost:5000" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Basic setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Access MinIO Console: http://localhost:9001 (user: minio, pass: minio123)" -ForegroundColor White
Write-Host "2. Create bucket 'mlflow-artifacts' in MinIO" -ForegroundColor White
Write-Host "3. Access MLflow UI: http://localhost:5000" -ForegroundColor White
Write-Host "4. Run: .\setup-seldon.ps1 to install Seldon Core" -ForegroundColor White
Write-Host "5. Run: python train.py to train and log your model" -ForegroundColor White