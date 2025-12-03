# Seldon Core setup script
# Run after setup.ps1 completes successfully

Write-Host "🧱 Setting up Seldon Core on Minikube" -ForegroundColor Green

# Create seldon-system namespace
Write-Host "📦 Creating seldon-system namespace..." -ForegroundColor Yellow
kubectl create namespace seldon-system --dry-run=client -o yaml | kubectl apply -f -

# Add Seldon Helm repository
Write-Host "📥 Adding Seldon Helm repository..." -ForegroundColor Yellow
helm repo add seldon https://storage.googleapis.com/seldon-charts
helm repo update

# Install Seldon Core Operator
Write-Host "🚀 Installing Seldon Core Operator..." -ForegroundColor Yellow
helm install seldon-core seldon/seldon-core-operator `
  --namespace seldon-system `
  --set usageMetrics.enabled=true `
  --set istio.enabled=true

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install Seldon Core" -ForegroundColor Red
    exit 1
}

# Wait for Seldon Core to be ready
Write-Host "⏳ Waiting for Seldon Core to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=seldon-core-operator -n seldon-system --timeout=300s

# Create MinIO access secret for Seldon
Write-Host "🔐 Creating MinIO access secret..." -ForegroundColor Yellow
kubectl create secret generic seldon-init-container-secret `
  --from-literal=AWS_ACCESS_KEY_ID=minio `
  --from-literal=AWS_SECRET_ACCESS_KEY=minio123 `
  --dry-run=client -o yaml | kubectl apply -f -

# Enable host.minikube.internal addon
Write-Host "🔗 Enabling host access addon..." -ForegroundColor Yellow
minikube addons enable host-resolver

Write-Host ""
Write-Host "✅ Seldon Core setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Train your model: python train.py" -ForegroundColor White
Write-Host "2. Deploy model: .\deploy-model.ps1" -ForegroundColor White
Write-Host "3. Test predictions: .\test-predictions.ps1" -ForegroundColor White
Write-Host ""
Write-Host "🔍 Monitor with:" -ForegroundColor Cyan
Write-Host "   kubectl get pods -n seldon-system" -ForegroundColor White
Write-Host "   kubectl get seldondeployments" -ForegroundColor White