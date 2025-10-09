# 🔧 MIPE_EV2 Development Board

## 🎯 Overview
MIPE_EV2 is the second iteration of the MIPE development platform, built on proven patterns from MIPE_EV1.

### **Hardware Platform**
- **MCU**: Nordic nRF54L15 (Arm Cortex-M33)
- **Development Environment**: Nordic Connect SDK v3.1.0
- **Board**: Custom MIPE_EV2 design

### **Key Features**
- ✅ **Proven GPIO patterns** from MIPE_EV1
- ✅ **Working timer configuration** (GRTC enabled)
- ✅ **23ms timing validation** confirmed on hardware
- ✅ **Non-interactive build scripts** for automation

---

## 🚀 Quick Start

### **1. Build and Flash**
```bash
# Build only
./build_mipe_ev2.bat

# Build and flash in one command
./build_and_flash_ev2.bat
```

### **2. Expected Behavior**
After flashing:
- LEDs on P0.00/P0.01 alternate every 23ms
- Test pins P1.05/P1.06 follow LED patterns
- All timing functions work (busy-wait loop confirmed functional)

### **3. Hardware Validation**
Connect Logic Analyzer to verify signals:
- Channel 0: P0.00 (LED0)
- Channel 1: P0.01 (LED1) 
- Channel 2: P1.05 (Test Pin 05)
- Channel 3: P1.06 (Test Pin 06)

---

## 🔧 Development

### **Project Structure**
```
MIPE_EV2_Project/
├── src/main.c              # GPIO test application
├── prj.conf               # Proven configuration
├── CMakeLists.txt         # Build configuration
├── boards/nordic/mipe_ev2/ # Board definition
└── build_*.bat           # Non-interactive build scripts
```

### **Key Lessons from MIPE_EV1**
1. **GRTC Timer**: Must be enabled in device tree for timing functions
2. **GPIO Pattern**: Configure direction first, set state separately
3. **Build Environment**: Use exact NCS v3.1.0 paths
4. **Timing**: Busy-wait loop gives accurate 23ms behavior

---

## 🎯 Success Metrics
- ✅ Clean build without warnings
- ✅ Successful flash to hardware
- ✅ GPIO signals match expected timing (23ms validated)
- ✅ All automated tests pass

Built with knowledge from MIPE_EV1 board bring-up challenges.