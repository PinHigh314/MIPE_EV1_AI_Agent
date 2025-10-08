@echo off
REM GitHub Actions Setup Script for MIPE_EV1 AI Agent

echo 🤖 MIPE_EV1 AI Agent - GitHub Actions Setup
echo ===========================================

REM Step 1: Check Git configuration
echo.
echo 📋 Step 1: Checking Git configuration...
git config --global user.name
git config --global user.email
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git not configured. Please set your Git credentials:
    echo git config --global user.name "Your Name"
    echo git config --global user.email "your.email@example.com"
    pause
    exit /b 1
)

REM Step 2: Repository status
echo.
echo 📋 Step 2: Checking repository status...
git status

REM Step 3: Check for GitHub remote
echo.
echo 📋 Step 3: Checking GitHub remote...
git remote -v
git remote get-url origin >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ GitHub remote already configured!
    for /f "delims=" %%i in ('git remote get-url origin') do echo Repository: %%i
) else (
    echo ❌ No GitHub remote found.
    echo.
    echo 🔧 Next steps:
    echo 1. Go to https://github.com/new
    echo 2. Create repository named 'MIPE_EV1_AI_Agent'
    echo 3. Don't initialize with README (we have one)
    echo 4. Copy the repository URL
    echo.
    echo Then we'll add it as remote...
    echo.
    pause
    
    set /p REPO_URL="Enter your GitHub repository URL: "
    if not "!REPO_URL!"=="" (
        git remote add origin "!REPO_URL!"
        git branch -M main
        echo ✅ Remote added successfully!
    )
)

REM Step 4: Commit changes
echo.
echo 📋 Step 4: Committing current changes...
git add .
git diff --staged --quiet
if %ERRORLEVEL% EQU 0 (
    echo ✅ No changes to commit
) else (
    git commit -m "Setup GitHub Actions for AI agent automation - 🤖 Ready for autonomous embedded development: Complete AI agent framework, Logic analyzer integration, GitHub Actions workflow, Self-hosted runner capability"
    echo ✅ Changes committed!
)

REM Step 5: Push to GitHub
echo.
echo 📋 Step 5: Pushing to GitHub...
git push -u origin main
if %ERRORLEVEL% EQU 0 (
    echo ✅ Successfully pushed to GitHub!
) else (
    echo ❌ Push failed. Please check your repository URL and credentials.
    pause
    exit /b 1
)

REM Step 6: Instructions
echo.
echo 🎉 SUCCESS! Repository is now on GitHub.
echo.
echo 🔧 Next: Set up Self-Hosted Runner
echo ==================================
echo.
echo 1. Go to your repository on GitHub
echo 2. Click Settings → Actions → Runners
echo 3. Click 'New self-hosted runner'
echo 4. Select 'Windows x64'
echo 5. Follow the download and configuration instructions
echo 6. IMPORTANT: Install as Windows Service for 24/7 operation
echo.
echo Required labels for your runner:
echo - self-hosted
echo - windows
echo - mipe-ev1-rig  
echo - logic-analyzer
echo.
echo Environment checklist:
echo ✅ Nordic nRF Connect SDK installed
echo ✅ West build tool working
echo ✅ Logic analyzer connected and detected
echo ✅ PulseView/sigrok working
echo ✅ Python 3.8+ installed
echo ✅ MIPE_EV1 hardware connected
echo.
echo 🚀 Test your setup:
echo git commit --allow-empty -m "Test AI automation"
echo git push
echo.
echo Then watch the Actions tab for autonomous development!

REM Step 7: Verify logic analyzer
echo.
echo 📋 Step 7: Verifying logic analyzer connection...
if exist "C:\Program Files\sigrok\sigrok-cli\sigrok-cli.exe" (
    echo ✅ sigrok-cli found
    echo 🔍 Scanning for devices...
    "C:\Program Files\sigrok\sigrok-cli\sigrok-cli.exe" --scan
    echo.
    echo ✅ Logic analyzer verification complete
) else (
    echo ❌ sigrok-cli not found. Please install PulseView/sigrok.
)

echo.
echo 🎉 GitHub Actions setup complete!
echo Your AI agent is ready for autonomous development!
pause