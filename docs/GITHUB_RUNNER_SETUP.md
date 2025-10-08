# 🚀 GitHub Actions Self-Hosted Runner Setup
**For MIPE_EV1 AI Agent - Windows Environment**

## 📋 **Current Status**
- ✅ Repository created: https://github.com/PinHigh314/MIPE_EV1_AI_Agent
- ✅ Code pushed to GitHub
- ✅ GitHub Actions workflow ready
- 🔄 **Next: Install self-hosted runner**

## 🏗️ **Step-by-Step Runner Installation**

### **1. Access Runner Setup Page**
Go to: https://github.com/PinHigh314/MIPE_EV1_AI_Agent/settings/actions/runners/new

### **2. Download GitHub Actions Runner**
1. Select **"Windows"** as your operating system
2. Select **"x64"** architecture
3. Download the runner package (typically `actions-runner-win-x64-2.x.x.zip`)
4. Extract to a dedicated folder: `C:\actions-runner\`

### **3. Configure the Runner**
Open **PowerShell as Administrator** and run:

```powershell
# Navigate to runner directory
cd C:\actions-runner

# Configure the runner (GitHub will provide the exact command)
.\config.cmd --url https://github.com/PinHigh314/MIPE_EV1_AI_Agent --token YOUR_TOKEN_HERE

# When prompted for runner name, use: MIPE-EV1-AI-Agent
# When prompted for labels, add: self-hosted,windows,mipe-ev1-rig,logic-analyzer
# When prompted for work folder, press Enter for default
```

### **4. Install as Windows Service (Critical!)**
```powershell
# Install as service for 24/7 operation
.\svc.cmd install

# Start the service
.\svc.cmd start

# Verify service is running
.\svc.cmd status
```

### **5. Verify Environment Requirements**

**Check Nordic nRF Connect SDK:**
```bash
west --version
west list  # Should show nRF modules
```

**Check Logic Analyzer:**
```bash
"C:\Program Files\sigrok\sigrok-cli\sigrok-cli.exe" --scan
# Should detect: fx2lafw:conn=3.22 - Saleae Logic
```

**Check Python Environment:**
```bash
python --version  # Should be 3.8+
python -c "import subprocess, pathlib, datetime" # Test required modules
```

**Check Build Environment:**
```bash
cd C:\Development\MIPE_EV1
west build -b mipe_ev1_nrf54l15_cpuapp --build-dir build_test
# Should compile successfully
```

## 🧪 **Test the AI Agent**

### **Option 1: Manual Trigger**
1. Go to: https://github.com/PinHigh314/MIPE_EV1_AI_Agent/actions
2. Click **"Automated SPI Development"**
3. Click **"Run workflow"**
4. Enter **"WHO_AM_I"** as the target feature
5. Click **"Run workflow"**

### **Option 2: Push Trigger**
```bash
cd C:\Development\MIPE_EV1
echo "// Test AI automation" >> src/main.c
git add .
git commit -m "🧪 Test AI development loop"
git push
```

### **Option 3: Local AI Agent**
```bash
cd C:\Development\MIPE_EV1
python scripts/enhanced_ai_generator.py
```

## 📊 **What to Expect**

When the AI agent runs, you'll see:

1. **🔨 Build Phase**: West compiles firmware for MIPE_EV1
2. **📡 Flash Phase**: Firmware uploaded to hardware
3. **📊 Capture Phase**: Logic analyzer records SPI signals  
4. **🧠 Analysis Phase**: AI examines capture for issues
5. **⚡ Fix Phase**: AI generates code modifications
6. **✏️ Modify Phase**: Device tree and driver updates
7. **💾 Commit Phase**: AI commits changes with descriptions
8. **🔄 Repeat**: Until LSM6DSO32 communication succeeds

## 🎯 **Success Indicators**

**✅ Successful Setup:**
- Runner appears as **"Online"** in GitHub Actions
- Test workflow completes without errors
- Logic analyzer detects hardware signals
- AI agent generates meaningful fixes

**❌ Common Issues:**
- **Runner Offline**: Check Windows Service status
- **Build Fails**: Verify Nordic nRF Connect SDK installation
- **No Signals**: Check logic analyzer connection
- **Flash Fails**: Verify MIPE_EV1 hardware connection

## 🔧 **Environment Checklist**

Before running the AI agent, verify:

- [ ] **GitHub Runner**: Installed as Windows Service and **"Online"**
- [ ] **Hardware**: MIPE_EV1 connected via USB and powered
- [ ] **Logic Analyzer**: Connected and detected as `fx2lafw:conn=3.22`
- [ ] **Nordic SDK**: West command working, nRF modules loaded
- [ ] **Python**: Version 3.8+, required modules available
- [ ] **Git**: Configured with your credentials
- [ ] **Repository**: Connected to https://github.com/PinHigh314/MIPE_EV1_AI_Agent

## 🚨 **Troubleshooting**

### **Runner Won't Start**
```powershell
# Check service status
sc query "GitHub Actions Runner (actions-runner.mipe_ev1_ai_agent.MIPE-EV1-AI-Agent)"

# Restart service
.\svc.cmd stop
.\svc.cmd start
```

### **Logic Analyzer Not Detected**
```bash
# Check USB devices
# Install fx2lafw drivers using Zadig if needed
# Verify with PulseView
```

### **Build Failures**
```bash
# Check SDK installation
west config --global zephyr.base
# Should point to nRF Connect SDK Zephyr installation
```

## 🎉 **Ready for Autonomous Development!**

Once everything is verified:

1. **Push any change** to trigger the AI agent
2. **Watch the Actions tab** for real-time progress
3. **Monitor commits** for AI-generated fixes
4. **Celebrate** when LSM6DSO32 communication works!

The AI agent will autonomously:
- ⚡ Detect SPI timing issues
- 🔧 Fix GPIO polarity problems  
- ⏰ Adjust clock speeds
- 📝 Generate device tree configurations
- 🔄 Iterate until success

**Welcome to the future of embedded development! 🤖**