# MIPE_EV1 GPIO Test - Changelog

## Version 3 - Actual Root Cause Fix (Current)

### Problem Identified
The GPIO test code was building successfully but not executing properly:
- All GPIO pins were stuck HIGH
- Code appeared to not be running
- VDD was stable (no flickering)

### Root Cause Analysis - CORRECT

After user feedback, the **actual root causes** were identified:

#### 1. GRTC Timer Disabled in Device Tree ⚠️ **CRITICAL**
**Problem**: The GRTC (Global Real-Time Counter) peripheral was disabled in the device tree.

**Evidence**: In `nrf54l15_cpuapp.dtsi`, the GRTC node has `status = "disabled"` by default.

**Impact**: Without GRTC enabled, `k_msleep()` and all timing functions don't work. The system timer configuration in `prj.conf` is meaningless if the hardware peripheral itself is disabled.

**Fix**: Added to `mipe_ev1_nrf54l15_cpuapp.dts`:
```dts
/* Enable GRTC timer - CRITICAL for system timing */
&grtc {
	status = "okay";
};
```

#### 2. Wrong GPIO Configuration Flags
**Problem**: Using `GPIO_OUTPUT_ACTIVE` or `GPIO_OUTPUT_INACTIVE` in `gpio_pin_configure_dt()`.

**Issue**: These flags are meant for pin configuration, but the correct approach is:
1. Configure pin as `GPIO_OUTPUT`
2. Then explicitly set the pin state with `gpio_pin_set_dt()`

**Fix**: Changed from:
```c
gpio_pin_configure_dt(&led0, GPIO_OUTPUT_INACTIVE);
```

To:
```c
gpio_pin_configure_dt(&led0, GPIO_OUTPUT);
gpio_pin_set_dt(&led0, 0);  /* Set LOW explicitly */
```

### Changes Made

#### 1. Updated `mipe_ev1_nrf54l15_cpuapp.dts`
```diff
+/* Enable GRTC timer - CRITICAL for system timing */
+&grtc {
+	status = "okay";
+};
```

#### 2. Updated `src/main.c`
```diff
-gpio_pin_configure_dt(&led0, GPIO_OUTPUT_INACTIVE);
+gpio_pin_configure_dt(&led0, GPIO_OUTPUT);
+gpio_pin_set_dt(&led0, 0);  /* Set LOW explicitly */
```

Applied to all 4 pins (led0, led1, test_pin05, test_pin06).

### Expected Behavior After Fix
1. **At power-on**: All pins (P0.00, P0.01, P1.05, P1.06) are LOW
2. **After 1 second**: All pins transition to HIGH (k_msleep works now!)
3. **Forever**: Pins remain HIGH

### Key Learnings

#### Device Tree Status is Critical
Peripherals in Nordic device trees default to `status = "disabled"`. You MUST explicitly enable them in your board's DTS file, even if you have the driver configured in Kconfig.

#### GPIO Configuration vs. Pin State
- `gpio_pin_configure_dt()` sets the pin **direction** (input/output)
- `gpio_pin_set_dt()` sets the pin **state** (high/low)
- Don't mix them - configure first, then set state

#### Configuration Location (Previous Misunderstanding)
The location of timer settings (prj.conf vs defconfig) was **not** the issue. The real issue was that GRTC hardware was disabled in device tree.

### Files Modified
- `boards/nordic/mipe_ev1/mipe_ev1_nrf54l15_cpuapp.dts` - Added GRTC enablement
- `src/main.c` - Fixed GPIO configuration flags and added explicit pin state setting

## Version 2 - Configuration Reorganization (Incorrect Fix)

### What Was Changed
- Moved timer settings from defconfig to prj.conf
- Enabled MPU
- Added security disablement

### Why It Didn't Work
These changes addressed symptoms, not root causes:
- Timer settings location doesn't matter if GRTC hardware is disabled
- MPU state is not critical for this simple test
- Security settings were already handled by defaults

### Lesson Learned
Always verify hardware peripheral enablement in device tree before adjusting Kconfig settings.

## Version 1 - Initial Minimal Version

### Initial State
- Ultra minimal GPIO test
- Attempted to set P1.05 HIGH
- GRTC not enabled in device tree
- Wrong GPIO configuration flags

### Issues
- Code built but didn't execute
- Pins stuck HIGH (not responding to code)
- Root causes not identified
