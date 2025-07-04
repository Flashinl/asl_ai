# PowerShell script to deploy ASL-to-Text AI to GitHub
Write-Host "🚀 Deploying ASL-to-Text AI to GitHub..." -ForegroundColor Green

# Set location to project directory
Set-Location "C:\Users\vkris\Documents\augment-projects\asl-to-text-ai"

Write-Host "📁 Current directory: $(Get-Location)" -ForegroundColor Yellow

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "🔧 Initializing Git repository..." -ForegroundColor Yellow
    git init
}

# Configure git user (if not already configured)
Write-Host "👤 Configuring Git user..." -ForegroundColor Yellow
git config user.name "Flashinl"
git config user.email "multiversestupid@gmail.com"

# Add all files
Write-Host "📦 Adding files to Git..." -ForegroundColor Yellow
git add --all

# Check status
Write-Host "📋 Git status:" -ForegroundColor Yellow
git status

# Commit changes
Write-Host "💾 Committing changes..." -ForegroundColor Yellow
git commit -m "Initial commit: ASL-to-Text AI system with real-time translation capabilities"

# Add remote origin (remove if exists)
Write-Host "🔗 Setting up remote repository..." -ForegroundColor Yellow
try {
    git remote remove origin 2>$null
} catch {
    # Remote doesn't exist, that's fine
}
git remote add origin https://github.com/Flashinl/asl_ai.git

# Set main branch
Write-Host "🌿 Setting main branch..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host "⬆️ Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host "✅ Successfully deployed to GitHub!" -ForegroundColor Green
Write-Host "🌐 Repository URL: https://github.com/Flashinl/asl_ai" -ForegroundColor Cyan

# Test the system
Write-Host "🧪 Testing system components..." -ForegroundColor Yellow
python test_system.py

Write-Host "🎉 Deployment complete! Your ASL-to-Text AI is now on GitHub." -ForegroundColor Green
Read-Host "Press Enter to continue..."
