# Deploy trained model to Seldon Core
# Run after training the model with train.py

Write-Host "🚀 Deploying model to Seldon Core" -ForegroundColor Green

# Check if model_path.txt exists
if (-not (Test-Path "model_path.txt")) {
    Write-Host "❌ model_path.txt not found. Please run 'python train.py' first." -ForegroundColor Red
    exit 1
}

# Read model path
$modelPath = Get-Content "model_path.txt" -Raw
$modelPath = $modelPath.Trim()

Write-Host "📦 Using model path: $modelPath" -ForegroundColor Yellow

# Create deployment YAML from template
$template = Get-Content "seldon-deployment-template.yaml" -Raw
$deployment = $template -replace "{MODEL_PATH}", $modelPath

# Save the final deployment file
$deployment | Out-File -FilePath "seldon-deployment-final.yaml" -Encoding UTF8

Write-Host "📝 Created deployment file: seldon-deployment-final.yaml" -ForegroundColor Yellow

# Apply the deployment
Write-Host "🚀 Applying Seldon deployment..." -ForegroundColor Yellow
kubectl apply -f seldon-deployment-final.yaml

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to apply Seldon deployment" -ForegroundColor Red
    exit 1
}

# Wait for deployment to be ready
Write-Host "⏳ Waiting for deployment to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l seldon-deployment-id=simple-ml-model --timeout=300s

# Check deployment status
Write-Host "🔍 Checking deployment status..." -ForegroundColor Yellow
kubectl get seldondeployments
kubectl get pods -l seldon-deployment-id=simple-ml-model

Write-Host ""
Write-Host "✅ Model deployment completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Port forward to access the model: kubectl port-forward svc/simple-ml-model-default 8003:8000" -ForegroundColor White
Write-Host "2. Test predictions: .\test-predictions.ps1" -ForegroundColor White
Write-Host ""
Write-Host "🔍 Monitor with:" -ForegroundColor Cyan
Write-Host "   kubectl get seldondeployments" -ForegroundColor White
Write-Host "   kubectl logs -l seldon-deployment-id=simple-ml-model" -ForegroundColor White