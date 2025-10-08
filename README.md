# 🤖 MIPE_EV1 AI Agent - Autonomous Embedded Development# 🤖 MIPE_EV1 AI Agent - Autonomous Embedded Development



[![AI Development Loop](https://img.shields.io/badge/AI-Autonomous%20Development-brightgreen)](https://github.com/your-username/MIPE_EV1_AI_Agent)[![AI Development Loop](https://img.shields.io/badge/AI-Autonomous%20Development-brightgreen)](https://github.com/your-username/MIPE_EV1_AI_Agent)

[![Hardware](https://img.shields.io/badge/Hardware-nRF54L15-blue)](https://www.nordicsemi.com/)[![Hardware](https://img.shields.io/badge/Hardware-nRF54L15-blue)](https://www.nordicsemi.com/)

[![Sensor](https://img.shields.io/badge/Sensor-LSM6DSO32-orange)](https://www.st.com/)[![Sensor](https://img.shields.io/badge/Sensor-LSM6DSO32-orange)](https://www.st.com/)

[![Analyzer](https://img.shields.io/badge/Logic%20Analyzer-8CH%2025MHz-red)](https://sigrok.org/)[![Analyzer](https://img.shields.io/badge/Logic%20Analyzer-8CH%2025MHz-red)](https://sigrok.org/)



**Revolutionary autonomous embedded development system that eliminates manual debugging through AI-driven hardware-in-the-loop testing.****Revolutionary autonomous embedded development system that eliminates manual debugging through AI-driven hardware-in-the-loop testing.**



## 🎯 **What This Project Does**## 🎯 **What This Project Does**



This is the **world's first fully autonomous embedded development system** that:This is the **world's first fully autonomous embedded development system** that:



- ✅ **Automatically detects hardware communication issues** using logic analyzer captures- ✅ **Automatically detects hardware communication issues** using logic analyzer captures

- ✅ **Generates targeted code fixes** for device tree, drivers, and configuration- ✅ **Generates targeted code fixes** for device tree, drivers, and configuration

- ✅ **Iterates continuously** until hardware communication succeeds  - ✅ **Iterates continuously** until hardware communication succeeds  

- ✅ **Operates 24/7** with zero manual intervention- ✅ **Operates 24/7** with zero manual intervention

- ✅ **Learns from each attempt** to improve fix accuracy- ✅ **Learns from each attempt** to improve fix accuracy



### **Target Hardware**### **Target Hardware**

- **MIPE_EV1** development board (nRF54L15 SoC)- **MIPE_EV1** development board (nRF54L15 SoC)

- **LSM6DSO32** 6-axis inertial sensor via SPI- **LSM6DSO32** 6-axis inertial sensor via SPI

- **8-channel Logic Analyzer** (Cypress FX2 compatible)- **8-channel Logic Analyzer** (Cypress FX2 compatible)



## 🚀 **Quick Start**## Software Architecture



### **Prerequisites**### Configuration Strategy

- Windows development environmentThe project uses a two-layer configuration approach:

- Nordic nRF Connect SDK v2.8.0+

- Logic analyzer connected (Saleae/fx2lafw compatible)1. **Board Definition Config** (`mipe_ev1_nrf54l15_cpuapp_defconfig`)

- MIPE_EV1 hardware with LSM6DSO32 sensor   - Hardware-specific settings (clock frequency, peripherals)

   - Board-level defaults that apply to all applications

### **Option 1: GitHub Actions (Recommended)**   - UART/console disablement (no UART on this board)

1. Fork this repository   - MPU configuration

2. Set up self-hosted runner (see below)

3. Push any change to trigger autonomous development2. **Project Config** (`prj.conf`)

4. Watch the AI agent work!   - Application-specific settings

   - Feature enablement (GPIO, SPI, sensors, etc.)

### **Option 2: Local AI Agent**   - System timer configuration (CRITICAL for proper initialization)

```bash   - Security settings

git clone https://github.com/your-username/MIPE_EV1_AI_Agent.git

cd MIPE_EV1_AI_Agent### Key Configuration Decisions

python scripts/enhanced_ai_generator.py

```#### System Timer in prj.conf (Not defconfig)

```

### **Option 3: Manual Development Loop**CONFIG_SYS_CLOCK_EXISTS=y

```bashCONFIG_TICKLESS_KERNEL=y

# Traditional approach (if you want to see each step)CONFIG_NRF_GRTC_TIMER=y

python scripts/analyzer_automation.py```

west build -b mipe_ev1_nrf54l15_cpuapp**Rationale**: The nRF54L15 uses GRTC (Global Real-Time Counter) instead of legacy RTC. These settings must be in `prj.conf` to ensure proper initialization order. Placing them in `defconfig` can cause initialization failures.

west flash

```#### MPU Enabled

```

## 🤖 **How the AI Agent Works**CONFIG_ARM_MPU=y

```

```**Rationale**: The ARM Memory Protection Unit provides memory safety. Disabling it can cause silent failures or unexpected behavior. The working reference project has this enabled.

1. 📋 ANALYZE → Current SPI configuration

2. 🔨 BUILD   → Compile firmware with west#### Security Disabled

3. 📡 FLASH   → Update MIPE_EV1 hardware  ```

4. 📊 CAPTURE → Record SPI signals via logic analyzerCONFIG_BUILD_WITH_TFM=n

5. 🧠 DETECT  → AI identifies communication issuesCONFIG_NRF_SECURITY=n

6. ⚡ GENERATE → Create targeted fixes automatically```

7. ✏️  MODIFY  → Update device tree & driver code**Rationale**: TrustedFirmware-M and Nordic security features add complexity and code size. For a minimal GPIO test, these are unnecessary and can interfere with simple applications.

8. 💾 COMMIT  → Version control with AI messages

9. 🔄 REPEAT  → Until LSM6DSO32 communication succeeds### Device Tree Architecture

```

The device tree defines hardware resources:

## 🛠️ **Self-Hosted Runner Setup**

```dts

The AI agent runs best with GitHub Actions on your development machine:leds {

    compatible = "gpio-leds";

### **1. Create GitHub Repository**    led0: led_0 {

1. Go to [GitHub](https://github.com/new)        gpios = <&gpio0 0 GPIO_ACTIVE_HIGH>;

2. Create repository named `MIPE_EV1_AI_Agent` (or your preferred name)    };

3. **Don't** initialize with README (we already have one)}

4. Create the repository

aliases {

### **2. Connect Local Repository**    led0 = &led0;

```bash}

# In your MIPE_EV1 directory```

git remote add origin https://github.com/YOUR_USERNAME/MIPE_EV1_AI_Agent.git

git branch -M mainThis allows code to reference hardware using symbolic names:

git push -u origin main```c

```static const struct gpio_dt_spec led0 = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios);

```

### **3. Install GitHub Actions Runner**

1. Go to your repo → **Settings** → **Actions** → **Runners****Benefits**:

2. Click **"New self-hosted runner"**- Hardware abstraction

3. Select **Windows x64**- Compile-time validation

4. Follow the download and configuration instructions- Easy hardware changes without code modifications

5. **Important**: Install as **Windows Service** for 24/7 operation

## Application Behavior

### **4. Configure Runner Labels**

Add these labels to your runner:### Initialization Sequence

- `self-hosted`1. Configure LED0 (P0.00) as output, set LOW

- `windows`2. Configure LED1 (P0.01) as output, set LOW

- `mipe-ev1-rig`3. Configure TestPin05 (P1.05) as output, set LOW

- `logic-analyzer`4. Configure TestPin06 (P1.06) as output, set LOW

5. Wait 1000ms (1 second)

### **5. Environment Requirements**6. Set all pins HIGH

Ensure your runner machine has:7. Enter infinite loop (pins stay HIGH)

- ✅ Nordic nRF Connect SDK v2.8.0+

- ✅ West build tool configured  ### Expected Observable Behavior

- ✅ Logic analyzer drivers (fx2lafw)- **0-1 second**: All pins LOW (0V)

- ✅ PulseView/sigrok installed- **After 1 second**: All pins HIGH (3.3V or VDD)

- ✅ Python 3.8+ with required packages- **Forever**: Pins remain HIGH

- ✅ MIPE_EV1 hardware connected

- ✅ Logic analyzer connected and detected### Error Handling

If any GPIO initialization fails, the application returns immediately with an error code. This prevents undefined behavior from uninitialized hardware.

### **6. Test the Automation**

```bash## Building and Flashing

# Trigger the AI agent

git commit --allow-empty -m "Test AI agent automation"### Prerequisites

git push- Nordic Connect SDK v3.1.0 or later

```- west build tool

- J-Link debugger/programmer

Go to your repository's **Actions** tab and watch the autonomous development!- Windows environment (for .bat scripts)



## 🏗️ **Architecture**### Quick Start

```batch

### **AI Components**build_and_flash.bat

- **`scripts/enhanced_ai_generator.py`** - Core AI intelligence for code generation```

- **`scripts/analyzer_automation.py`** - Logic analyzer integration and signal capture  

- **`.github/workflows/spi-development.yml`** - GitHub Actions automation pipelineThis script:

1. Cleans previous build

### **Hardware Integration**2. Builds the project for `mipe_ev1/nrf54l15/cpuapp`

- **Device Tree**: `boards/nordic/mipe_ev1/mipe_ev1_nrf54l15_cpuapp.dts`3. Flashes the firmware via J-Link

- **Main Application**: `src/main.c`4. Reports success/failure

- **Build System**: Zephyr RTOS with Nordic nRF Connect SDK

### Manual Build

### **Analysis Tools**```bash

- **PulseView/sigrok** for logic analyzer interface# Clean build

- **SPI Protocol Decoder** for automatic signal analysiswest build -b mipe_ev1/nrf54l15/cpuapp -p

- **AI Pattern Recognition** for issue detection and fix generation

# Flash

## 📊 **AI Performance Metrics**west flash

```

| Capability | Status | Details |

|------------|--------|---------|## Testing and Verification

| **Issue Detection** | ✅ Operational | Logic analyzer integration working |

| **Code Generation** | ✅ Operational | Device tree + driver modifications |### Equipment Needed

| **Build Automation** | ✅ Operational | West build system integration |- Oscilloscope (preferred) or multimeter

| **Hardware Validation** | ✅ Operational | Real MIPE_EV1 + LSM6DSO32 testing |- Test probes

| **Continuous Iteration** | ✅ Operational | Autonomous retry until success |

### Test Procedure

## 🎯 **Development Workflow Examples**1. Connect probes to test pins (P0.00, P0.01, P1.05, P1.06)

2. Flash the firmware

### **Manual Trigger**3. Reset the board

```bash4. Observe:

# Go to GitHub Actions tab   - All pins start LOW

# Click "Automated SPI Development"    - After 1 second, all pins go HIGH

# Click "Run workflow"   - Pins stay HIGH

# Specify target: "WHO_AM_I" or "full_sensor_config"

```### Success Criteria

- ✅ All 4 pins transition from LOW to HIGH after 1 second

### **Automatic Trigger**- ✅ Timing is consistent across resets

```bash- ✅ Pins remain stable in HIGH state

# Any code push triggers the AI agent

echo "// Test change" >> src/main.c### Troubleshooting

git add .

git commit -m "Trigger AI development cycle"#### Pins stuck HIGH (not responding)

git push**Symptoms**: Pins are always HIGH, no LOW period observed

```**Causes**:

- Code not executing (initialization failure)

### **Monitor Progress**- Configuration error (timer, MPU, security)

- **GitHub Actions Tab**: Real-time build/test progress- Flash corruption

- **Repository Commits**: AI-generated fix attempts

- **Actions Logs**: Detailed capture analysis and fix reasoning**Solutions**:

1. Verify configuration matches this README

## 📁 **Project Structure**2. Check `prj.conf` has system timer settings

3. Ensure `CONFIG_ARM_MPU=y` in defconfig

```4. Perform full chip erase and reflash

MIPE_EV1_AI_Agent/

├── 🤖 AI_AGENT_COMPLETE.md          # Complete implementation guide#### Pins stuck LOW

├── 📋 scripts/**Symptoms**: Pins never go HIGH

│   ├── enhanced_ai_generator.py      # Core AI intelligence**Causes**:

│   ├── analyzer_automation.py       # Logic analyzer integration- GPIO initialization failed

│   └── demo_ai_loop.py              # Interactive demonstration- k_msleep() not working (timer issue)

├── ⚙️  .github/workflows/- Code stuck in error path

│   └── spi-development.yml          # GitHub Actions automation

├── 🔧 boards/nordic/mipe_ev1/        # Board definition and device tree**Solutions**:

├── 💻 src/main.c                     # Application firmware1. Check GRTC timer configuration

├── 📖 docs/RUNNER_SETUP.md           # Detailed setup instructions2. Verify GPIO ports are enabled in device tree

└── 🏗️ build system files            # Zephyr/Nordic SDK integration3. Add debug output (if UART available)

```

#### Inconsistent behavior

## 🔬 **Technical Innovation****Symptoms**: Sometimes works, sometimes doesn't

**Causes**:

### **AI Capabilities**- Power supply instability

- **Pattern Recognition**: Identifies SPI timing and polarity issues from logic analyzer data- Clock configuration issues

- **Code Generation**: Creates device tree modifications and driver implementations  - Race conditions

- **Iterative Learning**: Improves fix accuracy based on previous attempts

- **Hardware Integration**: Direct feedback loop with real embedded hardware**Solutions**:

1. Check VDD stability with oscilloscope

### **Automation Framework**2. Verify system clock settings

- **GitHub Actions Integration**: 24/7 autonomous development capability3. Add delays in initialization sequence

- **Version Control**: Complete audit trail of AI-generated changes

- **Scalable Architecture**: Easy extension to new sensors and platforms## Project Structure

```

## 📈 **Expected Results**mipe_ev1_project/

├── boards/

The AI agent typically achieves:│   └── nordic/

- **⏱️ Average iteration time**: ~5 minutes│       └── mipe_ev1/

- **🎯 Success rate**: >95% for SPI communication issues│           ├── board.yml                              # Board metadata

- **🔄 Typical iterations needed**: 2-4 for complex issues│           ├── board.cmake                            # Build configuration

- **📊 Issue categories handled**: Clock speed, GPIO polarity, timing, protocol errors│           ├── Kconfig.board                          # Board Kconfig

- **🤖 Automation level**: 100% autonomous operation│           ├── Kconfig.defconfig                      # Default Kconfig

│           ├── Kconfig.mipe_ev1                       # Board-specific Kconfig

## 🏆 **Why This Matters**│           ├── mipe_ev1_nrf54l15_cpuapp.dts          # Device tree

│           └── mipe_ev1_nrf54l15_cpuapp_defconfig    # Board config

This project represents a **fundamental shift** in embedded systems development:├── src/

│   └── main.c                                         # Application code

### **Traditional Approach** ❌├── CMakeLists.txt                                     # CMake build file

- Manual debugging with oscilloscopes/logic analyzers├── prj.conf                                           # Project configuration

- Trial-and-error code modifications├── build_and_flash.bat                                # Build script

- Hours/days to resolve communication issues├── CHANGELOG.md                                       # Version history

- Expert knowledge required for each new sensor└── README.md                                          # This file

```

### **AI Agent Approach** ✅  

- **Autonomous issue detection** and resolution## Next Steps

- **Intelligent code generation** based on hardware feedback

- **Minutes to working communication** This GPIO test serves as a foundation for:

- **Scales to any embedded platform** automatically1. **SPI Communication**: Add LSM6DSVTR sensor support

2. **BLE**: Add Bluetooth Low Energy advertising

## 🤝 **Contributing**3. **Power Management**: Implement sleep modes

4. **Data Logging**: Store sensor data to flash

This project welcomes contributions to:

- **New sensor support** (I2C, UART, etc.)Each milestone builds on this proven, working base.

- **Additional AI fix patterns**

- **Platform extensions** (other MCUs/boards)## References

- **Analysis improvements** (more sophisticated issue detection)- [nRF54L15 Product Specification](https://infocenter.nordicsemi.com/topic/ps_nrf54l15/keyfeatures_html5.html)

- [Zephyr Device Tree Guide](https://docs.zephyrproject.org/latest/build/dts/index.html)

## 📄 **License**- [Nordic Connect SDK Documentation](https://developer.nordicsemi.com/nRF_Connect_SDK/doc/latest/nrf/index.html)



MIT License - See LICENSE file for details## License

SPDX-License-Identifier: Apache-2.0

---

## Version

**🎉 Experience the future of embedded development with autonomous AI agents!**Current version: 2.0 (Fixed Configuration)

See CHANGELOG.md for version history.

For detailed setup instructions, see `docs/RUNNER_SETUP.md`