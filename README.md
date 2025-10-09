# 🤖 MIPE_EV1 AI Agent - Autonomous Embedded Development

[![AI Development Loop](https://img.shields.io/badge/AI-Autonomous%20Development-brightgreen)](https://github.com/your-username/MIPE_EV1_AI_Agent)
[![Hardware](https://img.shields.io/badge/Hardware-nRF54L15-blue)](https://www.nordicsemi.com/)
[![Sensor](https://img.shields.io/badge/Sensor-LSM6DSO32-orange)](https://www.st.com/)
[![Analyzer](https://img.shields.io/badge/Logic%20Analyzer-8CH%2025MHz-red)](https://sigrok.org/)

**Revolutionary autonomous embedded development system that eliminates manual debugging through AI-driven hardware-in-the-loop testing.**

## 🎯 **What This Project Does**

This is the **world's first fully autonomous embedded development system** that:

- ✅ **Automatically detects hardware communication issues** using logic analyzer captures
- ✅ **Generates targeted code fixes** for device tree, drivers, and configuration
- ✅ **Iterates continuously** until hardware communication succeeds  
- ✅ **Operates 24/7** with zero manual intervention
- ✅ **Learns from each attempt** to improve fix accuracy

### **Target Hardware**
- **MIPE_EV1** development board (nRF54L15 SoC)
- **LSM6DSO32** 6-axis inertial sensor via SPI
- **8-channel Logic Analyzer** (Cypress FX2 compatible)

## Software Architecture

### Configuration Strategy
The project uses a two-layer configuration approach:

1. **Board Definition Config** (`mipe_ev1_nrf54l15_cpuapp_defconfig`)
   - Hardware-specific settings (clock frequency, peripherals)
   - Board-level defaults that apply to all applications
   - UART/console disablement (no UART on this board)
   - MPU configuration

2. **Project Config** (`prj.conf`)
   - Application-specific settings
   - Feature enablement (GPIO, SPI, sensors, etc.)
   - System timer configuration (CRITICAL for proper initialization)
   - Security settings

### Key Configuration Decisions

#### System Timer in prj.conf (Not defconfig)
```
CONFIG_SYS_CLOCK_EXISTS=y
CONFIG_TICKLESS_KERNEL=y
CONFIG_NRF_GRTC_TIMER=y
```
**Rationale**: The nRF54L15 uses GRTC (Global Real-Time Counter) instead of legacy RTC. These settings must be in `prj.conf` to ensure proper initialization order. Placing them in `defconfig` can cause initialization failures.

#### MPU Enabled
```
CONFIG_ARM_MPU=y
```
**Rationale**: The ARM Memory Protection Unit provides memory safety. Disabling it can cause silent failures or unexpected behavior. The working reference project has this enabled.

#### Security Disabled
```
CONFIG_BUILD_WITH_TFM=n
CONFIG_NRF_SECURITY=n
```
**Rationale**: TrustedFirmware-M and Nordic security features add complexity and code size. For a minimal GPIO test, these are unnecessary and can interfere with simple applications.

### Device Tree Architecture

The device tree defines hardware resources:

```dts
leds {
    compatible = "gpio-leds";
    led0: led_0 {
        gpios = <&gpio0 0 GPIO_ACTIVE_HIGH>;
    };
}

aliases {
    led0 = &led0;
}
```

This allows code to reference hardware using symbolic names:
```c
static const struct gpio_dt_spec led0 = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios);
```

**Benefits**:
- Hardware abstraction
- Compile-time validation
- Easy hardware changes without code modifications

## Application Behavior

### Initialization Sequence
1. Configure LED0 (P0.00) as output, set LOW
2. Configure LED1 (P0.01) as output, set LOW
3. Configure TestPin05 (P1.05) as output, set LOW
4. Configure TestPin06 (P1.06) as output, set LOW
5. Wait 1000ms (1 second)
6. Set all pins HIGH
7. Enter infinite loop (pins stay HIGH)

### Expected Observable Behavior
- **0-1 second**: All pins LOW (0V)
- **After 1 second**: All pins HIGH (3.3V or VDD)
- **Forever**: Pins remain HIGH

### Error Handling
If any GPIO initialization fails, the application returns immediately with an error code. This prevents undefined behavior from uninitialized hardware.

## Building and Flashing

### Prerequisites
- Nordic Connect SDK v3.1.0 or later
- west build tool
- J-Link debugger/programmer
- Windows environment (for .bat scripts)

### Quick Start
```batch
build_and_flash.bat
```

This script:
1. Cleans previous build
2. Builds the project for `mipe_ev1/nrf54l15/cpuapp`
3. Flashes the firmware via J-Link
4. Reports success/failure

### Manual Build
```bash
# Clean build
west build -b mipe_ev1/nrf54l15/cpuapp -p

# Flash
west flash
```

## Testing and Verification

### Equipment Needed
- Oscilloscope (preferred) or multimeter
- Test probes

### Test Procedure
1. Connect probes to test pins (P0.00, P0.01, P1.05, P1.06)
2. Flash the firmware
3. Reset the board
4. Observe:
   - All pins start LOW
   - After 1 second, all pins go HIGH
   - Pins stay HIGH

### Success Criteria
- ✅ All 4 pins transition from LOW to HIGH after 1 second
- ✅ Timing is consistent across resets
- ✅ Pins remain stable in HIGH state

### Troubleshooting

#### Pins stuck HIGH (not responding)
**Symptoms**: Pins are always HIGH, no LOW period observed
**Causes**:
- Code not executing (initialization failure)
- Configuration error (timer, MPU, security)
- Flash corruption

**Solutions**:
1. Verify configuration matches this README
2. Check `prj.conf` has system timer settings
3. Ensure `CONFIG_ARM_MPU=y` in defconfig
4. Perform full chip erase and reflash

#### Pins stuck LOW
**Symptoms**: Pins never go HIGH
**Causes**:
- GPIO initialization failed
- k_msleep() not working (timer issue)
- Code stuck in error path

**Solutions**:
1. Check GRTC timer configuration
2. Verify GPIO ports are enabled in device tree
3. Add debug output (if UART available)

#### Inconsistent behavior
**Symptoms**: Sometimes works, sometimes doesn't
**Causes**:
- Power supply instability
- Clock configuration issues
- Race conditions

**Solutions**:
1. Check VDD stability with oscilloscope
2. Verify system clock settings
3. Add delays in initialization sequence

## Project Structure
```
mipe_ev1_project/
├── boards/
│   └── nordic/
│       └── mipe_ev1/
│           ├── board.yml                              # Board metadata
│           ├── board.cmake                            # Build configuration
│           ├── Kconfig.board                          # Board Kconfig
│           ├── Kconfig.defconfig                      # Default Kconfig
│           ├── Kconfig.mipe_ev1                       # Board-specific Kconfig
│           ├── mipe_ev1_nrf54l15_cpuapp.dts          # Device tree
│           └── mipe_ev1_nrf54l15_cpuapp_defconfig    # Board config
├── src/
│   └── main.c                                         # Application code
├── CMakeLists.txt                                     # CMake build file
├── prj.conf                                           # Project configuration
├── build_and_flash.bat                                # Build script
├── CHANGELOG.md                                       # Version history
└── README.md                                          # This file
```

## Next Steps

This GPIO test serves as a foundation for:
1. **SPI Communication**: Add LSM6DSVTR sensor support
2. **BLE**: Add Bluetooth Low Energy advertising
3. **Power Management**: Implement sleep modes
4. **Data Logging**: Store sensor data to flash

Each milestone builds on this proven, working base.

## References
- [nRF54L15 Product Specification](https://infocenter.nordicsemi.com/topic/ps_nrf54l15/keyfeatures_html5.html)
- [Zephyr Device Tree Guide](https://docs.zephyrproject.org/latest/build/dts/index.html)
- [Nordic Connect SDK Documentation](https://developer.nordicsemi.com/nRF_Connect_SDK/doc/latest/nrf/index.html)

## License
SPDX-License-Identifier: Apache-2.0

## Version
Current version: 2.0 (Fixed Configuration)
See CHANGELOG.md for version history.
