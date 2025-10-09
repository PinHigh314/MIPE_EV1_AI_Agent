# 🔧 MIPE_EV2 Board Bring-Up Guide
## Critical Knowledge Transfer from MIPE_EV1

> **⚠️ CRITICAL:** This document contains hard-won knowledge from MIPE_EV1 board bring-up challenges. Follow these patterns exactly to avoid repeating the same debugging cycles.

---

## 🏆 **Working Foundation - Proven Components**

### **1. Device Tree Structure (CRITICAL)**

#### **Base DTS File:** `boards/nordic/mipe_ev2/mipe_ev2_nrf54l15_cpuapp.dts`
```dts
/*
 * Copyright (c) 2025 MIPE_EV2 Project
 * SPDX-License-Identifier: Apache-2.0
 */

/dts-v1/;

#include <nordic/nrf54l15_cpuapp.dtsi>

/ {
	model = "MIPE_EV2 Custom Board";
	compatible = "mipe,mipe-ev2";

	chosen {
		zephyr,sram = &cpuapp_sram;
		zephyr,flash = &cpuapp_rram;
		zephyr,code-partition = &slot0_partition;
	};

	leds {
		compatible = "gpio-leds";
		led0: led_0 {
			gpios = <&gpio0 0 GPIO_ACTIVE_HIGH>;
			label = "LED 0";
		};
		led1: led_1 {
			gpios = <&gpio0 1 GPIO_ACTIVE_HIGH>;
			label = "LED 1";
		};
	};

	test_pins {
		compatible = "gpio-leds";
		testpin05: test_pin_05 {
			gpios = <&gpio1 5 GPIO_ACTIVE_HIGH>;
			label = "Test Pin 05";
		};
		testpin06: test_pin_06 {
			gpios = <&gpio1 6 GPIO_ACTIVE_HIGH>;
		};
	};

	aliases {
		led0 = &led0;
		led1 = &led1;
		testpin05 = &testpin05;
		testpin06 = &testpin06;
	};
};

/* Enable GPIO ports - REQUIRED */
&gpio0 {
	status = "okay";
};

&gpio1 {
	status = "okay";
};

/* Enable GPIOTE instances - REQUIRED for GPIO operations */
&gpiote20 {
	status = "okay";
};

&gpiote30 {
	status = "okay";
};

/* ⚠️ CRITICAL FIX: Enable GRTC timer for system timing */
&grtc {
	owned-channels = <0>;
	status = "okay";
};

/* Include partition configuration */
#include <nordic/nrf54l15_partition.dtsi>
```

#### **🔥 CRITICAL LESSON #1: GRTC Timer**
**Problem**: Nordic nRF54L15 has GRTC disabled by default in device tree.
**Impact**: Without GRTC enabled, `k_msleep()` and ALL timing functions fail silently.
**Symptoms**: Code compiles, flashes, but appears not to run (pins stuck HIGH/LOW).
**Solution**: MUST enable GRTC in device tree as shown above.

### **2. Project Configuration (PROVEN)**

#### **prj.conf - Working Timer Configuration**
```properties
# MIPE_EV2 - Minimal GPIO Configuration
# Based on MIPE_EV1 proven working setup

# Disable crypto/security for development
CONFIG_BUILD_WITH_TFM=n
CONFIG_NRF_SECURITY=n

# Enable GPIO driver
CONFIG_GPIO=y

# System Timer - CRITICAL for k_msleep() functionality
CONFIG_SYS_CLOCK_EXISTS=y
CONFIG_TICKLESS_KERNEL=y
CONFIG_NRF_GRTC_TIMER=y

# Disable watchdogs for development stability
CONFIG_WATCHDOG=n
CONFIG_WDT_DISABLE_AT_BOOT=y
CONFIG_WDT_NRFX=n

# Disable power management for development
CONFIG_PM=n
CONFIG_PM_DEVICE=n

# System initialization
CONFIG_KERNEL_INIT_PRIORITY_DEFAULT=50
```

#### **🔥 CRITICAL LESSON #2: Timer Configuration**
These three config lines are ESSENTIAL for timing to work:
- `CONFIG_SYS_CLOCK_EXISTS=y`
- `CONFIG_TICKLESS_KERNEL=y` 
- `CONFIG_NRF_GRTC_TIMER=y`

### **3. GPIO Code Patterns (PROVEN)**

#### **Correct GPIO Initialization**
```c
#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>

/* GPIO pin definitions using device tree aliases */
static const struct gpio_dt_spec led0 = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios);
static const struct gpio_dt_spec led1 = GPIO_DT_SPEC_GET(DT_ALIAS(led1), gpios);
static const struct gpio_dt_spec test_pin05 = GPIO_DT_SPEC_GET(DT_ALIAS(testpin05), gpios);
static const struct gpio_dt_spec test_pin06 = GPIO_DT_SPEC_GET(DT_ALIAS(testpin06), gpios);

int main(void)
{
	/* ⚠️ CRITICAL: Correct GPIO configuration pattern */
	/* Step 1: Configure pin direction only */
	gpio_pin_configure_dt(&led0, GPIO_OUTPUT);
	gpio_pin_configure_dt(&led1, GPIO_OUTPUT);
	gpio_pin_configure_dt(&test_pin05, GPIO_OUTPUT);
	gpio_pin_configure_dt(&test_pin06, GPIO_OUTPUT);
	
	/* Step 2: Explicitly set initial pin states */
	gpio_pin_set_dt(&led0, 0);         /* Start LOW */
	gpio_pin_set_dt(&led1, 0);         /* Start LOW */
	gpio_pin_set_dt(&test_pin05, 0);   /* Start LOW */
	gpio_pin_set_dt(&test_pin06, 0);   /* Start LOW */

	bool led_state = false;

	/* Main loop with timing */
	while (1) {
		led_state = !led_state;
		gpio_pin_set_dt(&led0, led_state ? 1 : 0);
		gpio_pin_set_dt(&led1, led_state ? 0 : 1);  /* Opposite phase */
		gpio_pin_set_dt(&test_pin05, led_state ? 1 : 0);
		gpio_pin_set_dt(&test_pin06, led_state ? 0 : 1);
		
		k_msleep(200);  /* Now works because GRTC is enabled! */
	}

	return 0;
}
```

#### **🔥 CRITICAL LESSON #3: GPIO Configuration vs State**
**WRONG Pattern (Causes Failures):**
```c
gpio_pin_configure_dt(&led0, GPIO_OUTPUT_ACTIVE);   // DON'T DO THIS
gpio_pin_configure_dt(&led1, GPIO_OUTPUT_INACTIVE); // DON'T DO THIS
```

**CORRECT Pattern:**
```c
gpio_pin_configure_dt(&led0, GPIO_OUTPUT);  // Configure direction only
gpio_pin_set_dt(&led0, 1);                 // Set state separately
```

### **4. Build System (PROVEN)**

#### **CMakeLists.txt**
```cmake
cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(mipe_ev2)

target_sources(app PRIVATE src/main.c)
```

#### **Board Directory Structure**
```
boards/
└── nordic/
    └── mipe_ev2/
        ├── Kconfig.board
        ├── Kconfig.defconfig
        ├── board.cmake
        ├── mipe_ev2_nrf54l15_cpuapp.dts
        └── mipe_ev2_nrf54l15_cpuapp.yaml
```

#### **Build Script Pattern (PROVEN)**
```bat
@echo off
setlocal

echo Setting up NCS environment...
set ZEPHYR_BASE=C:\ncs\v3.1.0\zephyr
set ZEPHYR_SDK_INSTALL_DIR=C:\ncs\toolchains\b8b84efebd\opt\zephyr-sdk
set ZEPHYR_TOOLCHAIN_VARIANT=zephyr
set PATH=C:\ncs\toolchains\b8b84efebd\opt\bin;C:\ncs\toolchains\b8b84efebd\opt\bin\Scripts;%PATH%

echo Cleaning build directory...
if exist build rmdir /s /q build

echo Configuring with CMake...
cmake -B build -G Ninja -DBOARD=mipe_ev2/nrf54l15/cpuapp

echo Building...
ninja -C build

echo Flashing...
nrfjprog --program build/zephyr/zephyr.hex --sectorerase --verify --reset
```

---

## 🚨 **Common Failure Patterns to AVOID**

### **1. Device Tree Peripheral Enablement**
- **Never assume peripherals are enabled by default**
- **Always explicitly enable in your board DTS:**
  - `&grtc { status = "okay"; }`
  - `&gpio0 { status = "okay"; }`
  - `&gpiote20 { status = "okay"; }`

### **2. GPIO Configuration Mixing**
- **Never mix configuration and state setting**
- **Always configure direction first, then set state**

### **3. Timer Dependencies**
- **GRTC hardware MUST be enabled in device tree**
- **Kconfig timer settings are meaningless without hardware enablement**

### **4. Build Environment**
- **Use exact NCS v3.1.0 paths in build scripts**
- **Clean build directory between major changes**
- **Verify board directory structure matches exactly**

---

## 🎯 **Testing & Validation Pattern**

### **1. First Boot Test**
```c
// Minimal test - just set one pin HIGH
gpio_pin_configure_dt(&test_pin05, GPIO_OUTPUT);
gpio_pin_set_dt(&test_pin05, 1);
// No timing, no loops - just verify basic GPIO works
```

### **2. Timing Test**
```c
// Add timing after basic GPIO confirmed
while (1) {
    gpio_pin_set_dt(&test_pin05, 1);
    k_msleep(500);
    gpio_pin_set_dt(&test_pin05, 0);
    k_msleep(500);
}
```

### **3. Multi-Pin Test**
```c
// Add multiple pins after timing confirmed working
// Test pattern from MIPE_EV1 main.c
```

---

## 📋 **Pre-Flight Checklist for MIPE_EV2**

- [ ] **Device Tree**: GRTC enabled with `status = "okay"`
- [ ] **Device Tree**: GPIO ports enabled
- [ ] **Device Tree**: GPIOTE instances enabled  
- [ ] **prj.conf**: All three timer configs present
- [ ] **main.c**: GPIO configure/set pattern used correctly
- [ ] **Build**: Board directory structure matches MIPE_EV1
- [ ] **Build**: CMakeLists.txt matches proven pattern
- [ ] **Test**: Start with minimal single-pin test
- [ ] **Test**: Add timing after basic GPIO confirmed
- [ ] **Test**: Verify with logic analyzer capture

---

**🎉 Follow this guide exactly and MIPE_EV2 will work on first boot!**