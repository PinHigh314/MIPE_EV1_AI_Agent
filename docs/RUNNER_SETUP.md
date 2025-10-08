# MIPE_EV1 Self-Hosted Runner Setup

## Prerequisites
1. GitHub repository created for MIPE_EV1
2. Hardware connected (MIPE_EV1 + Logic Analyzer)
3. Development environment working

## Setup Instructions

### 1. Create GitHub Repository
```bash
# In your MIPE_EV1 directory
git add .
git commit -m "Initial MIPE_EV1 project with AI automation"
git remote add origin https://github.com/YOUR_USERNAME/MIPE_EV1.git
git push -u origin main
```

### 2. Install GitHub Actions Runner
1. Go to your GitHub repo → Settings → Actions → Runners
2. Click "New self-hosted runner"
3. Select Windows x64
4. Follow download/configure instructions
5. Install as Windows Service

### 3. Label Your Runner
Add these labels to your runner:
- `self-hosted`
- `windows` 
- `mipe-ev1-rig`

### 4. Environment Setup
Ensure your runner can access:
- West build tools
- Nordic nRF Connect SDK
- Logic analyzer (PulseView/sigrok)
- Python environment

### 5. Test the Setup
Push a change to trigger the workflow:
```bash
git add .
git commit -m "Test AI development loop"
git push
```

## Automation Flow
1. **Code Change** → GitHub detects push
2. **Build** → Firmware compiled
3. **Flash** → Hardware updated
4. **Capture** → Logic analyzer records SPI signals
5. **Analyze** → AI examines results
6. **Generate** → AI creates fixes if needed
7. **Repeat** → Until SPI communication works

## Manual Trigger
You can also manually trigger development:
```bash
# Go to GitHub Actions tab
# Click "Automated SPI Development"
# Click "Run workflow"
# Specify target feature (e.g., "WHO_AM_I")
```