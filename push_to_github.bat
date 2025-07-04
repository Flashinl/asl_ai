@echo off
echo Pushing ASL-to-Text AI to GitHub...

echo Adding all files...
git add .

echo Committing changes...
git commit -m "Initial commit: ASL-to-Text AI system with real-time translation capabilities"

echo Adding remote origin...
git remote add origin https://github.com/Flashinl/asl_ai.git

echo Setting main branch...
git branch -M main

echo Pushing to GitHub...
git push -u origin main

echo Done! Check your repository at: https://github.com/Flashinl/asl_ai
pause
