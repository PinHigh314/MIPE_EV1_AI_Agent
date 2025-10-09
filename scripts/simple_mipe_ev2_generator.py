#!/usr/bin/env python3
"""
Simple MIPE_EV2 Project Generator
Creates MIPE_EV2 project with proven MIPE_EV1 patterns (ASCII only)
"""

import os
from pathlib import Path

def create_mipe_ev2():
    """Create MIPE_EV2 project structure"""
    base_path = Path("C:/Development/MIPE_EV2")
    
    print("Creating MIPE_EV2 project...")
    
    # Create directories
    base_path.mkdir(exist_ok=True)
    (base_path / "src").mkdir(exist_ok=True)
    (base_path / "boards" / "nordic" / "mipe_ev2").mkdir(parents=True, exist_ok=True)
    
    # Create main.c with proven 23ms timing
    main_c = '''/**
 * MIPE_EV2 - GPIO Test
 * Based on proven MIPE_EV1 patterns (23ms timing)
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>

/* LEDs on P0.00 and P0.01 */
static const struct gpio_dt_spec led0 = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios);
static const struct gpio_dt_spec led1 = GPIO_DT_SPEC_GET(DT_ALIAS(led1), gpios);

/* Test pins on P1.05 and P1.06 */
static const struct gpio_dt_spec test_pin05 = GPIO_DT_SPEC_GET(DT_ALIAS(testpin05), gpios);
static const struct gpio_dt_spec test_pin06 = GPIO_DT_SPEC_GET(DT_ALIAS(testpin06), gpios);

int main(void)
{
    /* Configure pin directions */
    gpio_pin_configure_dt(&led0, GPIO_OUTPUT);
    gpio_pin_configure_dt(&led1, GPIO_OUTPUT);
    gpio_pin_configure_dt(&test_pin05, GPIO_OUTPUT);
    gpio_pin_configure_dt(&test_pin06, GPIO_OUTPUT);

    /* Set initial states */
    gpio_pin_set_dt(&led0, 0);
    gpio_pin_set_dt(&led1, 0);
    gpio_pin_set_dt(&test_pin05, 0);
    gpio_pin_set_dt(&test_pin06, 0);

    bool led_state = false;
    uint32_t counter = 0;
    const uint32_t toggle_threshold = 1000000;  /* Proven 23ms timing */
    
    while (1) {
        counter++;
        
        if (counter >= toggle_threshold) {
            led_state = !led_state;
            gpio_pin_set_dt(&led0, led_state ? 1 : 0);
            gpio_pin_set_dt(&led1, led_state ? 0 : 1);
            gpio_pin_set_dt(&test_pin05, led_state ? 1 : 0);
            gpio_pin_set_dt(&test_pin06, led_state ? 0 : 1);
            counter = 0;
        }
    }

    return 0;
}
'''
    
    with open(base_path / "src" / "main.c", "w") as f:
        f.write(main_c)
    
    # Create prj.conf with proven config
    prj_conf = '''# MIPE_EV2 - Proven Configuration
CONFIG_BUILD_WITH_TFM=n
CONFIG_NRF_SECURITY=n
CONFIG_GPIO=y
CONFIG_SYS_CLOCK_EXISTS=y
CONFIG_TICKLESS_KERNEL=y
CONFIG_NRF_GRTC_TIMER=y
CONFIG_WATCHDOG=n
CONFIG_WDT_DISABLE_AT_BOOT=y
CONFIG_WDT_NRFX=n
CONFIG_PM=n
CONFIG_PM_DEVICE=n
CONFIG_KERNEL_INIT_PRIORITY_DEFAULT=50
'''
    
    with open(base_path / "prj.conf", "w") as f:
        f.write(prj_conf)
    
    # Create CMakeLists.txt
    cmake_content = '''cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(mipe_ev2)

target_sources(app PRIVATE src/main.c)
'''
    
    with open(base_path / "CMakeLists.txt", "w") as f:
        f.write(cmake_content)
    
    # Create device tree with CRITICAL GRTC fix
    dts_content = '''/*
 * MIPE_EV2 Device Tree
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

/* Enable GPIO ports */
&gpio0 {
    status = "okay";
};

&gpio1 {
    status = "okay";
};

/* Enable GPIOTE instances */
&gpiote20 {
    status = "okay";
};

&gpiote30 {
    status = "okay";
};

/* CRITICAL: Enable GRTC timer */
&grtc {
    owned-channels = <0>;
    status = "okay";
};

/* Include partition configuration */
#include <nordic/nrf54l15_partition.dtsi>
'''
    
    board_path = base_path / "boards" / "nordic" / "mipe_ev2"
    with open(board_path / "mipe_ev2_nrf54l15_cpuapp.dts", "w") as f:
        f.write(dts_content)
    
    # Create board files
    with open(board_path / "Kconfig.board", "w") as f:
        f.write('''config BOARD_MIPE_EV2_NRF54L15_CPUAPP
	bool "MIPE_EV2 nRF54L15 Application MCU"
	depends on SOC_NRF54L15_CPUAPP
''')
    
    with open(board_path / "Kconfig.defconfig", "w") as f:
        f.write('''if BOARD_MIPE_EV2_NRF54L15_CPUAPP

config BOARD
	default "mipe_ev2_nrf54l15_cpuapp"

endif # BOARD_MIPE_EV2_NRF54L15_CPUAPP
''')
    
    with open(board_path / "board.cmake", "w") as f:
        f.write('''board_runner_args(nrfjprog "--nrf-family=NRF54L")
board_runner_args(jlink "--device=nrf54l15_xxaa" "--speed=4000")

include(${ZEPHYR_BASE}/boards/common/nrfjprog.board.cmake)
include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
''')
    
    with open(board_path / "mipe_ev2_nrf54l15_cpuapp.yaml", "w") as f:
        f.write('''identifier: mipe_ev2_nrf54l15_cpuapp
name: MIPE_EV2_nRF54L15_CPUAPP
type: mcu
arch: arm
toolchain:
  - zephyr
  - gnuarmemb
  - xtools
ram: 256
flash: 1536
supported:
  - gpio
  - i2c
  - spi
  - watchdog
  - counter
''')
    
    # Create build script
    build_script = '''@echo off
setlocal

echo ========================================
echo MIPE_EV2 Build Script
echo ========================================

set ZEPHYR_BASE=C:\\ncs\\v3.1.0\\zephyr
set ZEPHYR_SDK_INSTALL_DIR=C:\\ncs\\toolchains\\b8b84efebd\\opt\\zephyr-sdk
set ZEPHYR_TOOLCHAIN_VARIANT=zephyr
set PATH=C:\\ncs\\toolchains\\b8b84efebd\\opt\\bin;C:\\ncs\\toolchains\\b8b84efebd\\opt\\bin\\Scripts;%PATH%

cd /d "%~dp0"

if exist build rmdir /s /q build

cmake -B build -G Ninja -DBOARD=mipe_ev2/nrf54l15/cpuapp
ninja -C build

if %errorlevel% neq 0 (
    echo Build failed!
    exit /b 1
)

echo Build successful!
'''
    
    with open(base_path / "build_mipe_ev2.bat", "w") as f:
        f.write(build_script)
    
    # Create build and flash script
    flash_script = '''@echo off
setlocal

echo ========================================
echo MIPE_EV2 Build and Flash
echo ========================================

call build_mipe_ev2.bat

if %errorlevel% neq 0 (
    echo Build failed - cannot flash
    exit /b 1
)

echo Flashing...
nrfjprog --program build\\zephyr\\zephyr.hex --sectorerase --verify --reset

if %errorlevel% neq 0 (
    echo Flash failed!
    exit /b 1
)

echo MIPE_EV2 flashed successfully!
echo Expected: 23ms toggle on P1.05/P1.06
'''
    
    with open(base_path / "build_and_flash_ev2.bat", "w") as f:
        f.write(flash_script)
    
    print(f"MIPE_EV2 project created at: {base_path}")
    print("Ready to build and flash!")

if __name__ == "__main__":
    create_mipe_ev2()