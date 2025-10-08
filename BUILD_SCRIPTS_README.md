# Build Scripts Guide

## Available Scripts

### 1. `build_and_flash.bat` (Recommended)
Complete build and flash in one step.

**Usage**:
```batch
build_and_flash.bat
```

**What it does**:
1. Checks for west environment
2. Cleans previous build
3. Builds the project
4. Flashes to board

---

### 2. `build_only.bat`
Build without flashing (useful for checking compilation).

**Usage**:
```batch
build_only.bat
```

**Output**: `build\zephyr\zephyr.hex`

---

### 3. `flash_only.bat`
Flash an existing build (no rebuild).

**Usage**:
```batch
flash_only.bat
```

**Requires**: Previous successful build

---

## Important: Run from nRF Connect SDK Environment

All scripts **MUST** be run from the **nRF Connect SDK Command Prompt**.

### How to Open nRF Connect SDK Command Prompt

#### Method 1: Toolchain Manager
1. Open nRF Connect for Desktop
2. Open Toolchain Manager
3. Click the dropdown next to your SDK version
4. Select "Open command prompt"

#### Method 2: VS Code Terminal
1. Open project in VS Code with nRF Connect extension
2. Use the integrated terminal (it's pre-configured)

#### Method 3: Start Menu
1. Search for "nRF Connect SDK Command Prompt" in Windows Start Menu
2. Navigate to your project directory

---

## Common Issues

### "west: unknown command"
**Problem**: Not running from nRF Connect SDK environment

**Solution**: Open nRF Connect SDK Command Prompt (see above)

---

### "Board not found"
**Problem**: Board definition not in the right location

**Solution**: Verify `boards/nordic/mipe_ev1/` exists in project

---

### "Flash failed"
**Problem**: J-Link connection or board power issue

**Solutions**:
1. Check J-Link USB connection
2. Verify board is powered (VDD present)
3. Try recovery: `nrfjprog --recover`
4. Reinstall J-Link drivers

---

## Manual Build Commands

If you prefer manual control:

### Clean Build
```bash
west build -b mipe_ev1/nrf54l15/cpuapp -p
```

### Incremental Build
```bash
west build
```

### Flash
```bash
west flash
```

### Flash with nrfjprog
```bash
nrfjprog --program build/zephyr/zephyr.hex --chiperase --verify --reset
```

---

## Build Output

After successful build, find outputs in:
- `build/zephyr/zephyr.hex` - Flash image
- `build/zephyr/zephyr.elf` - ELF with debug symbols
- `build/zephyr/zephyr.bin` - Raw binary

---

## First Time Setup

If this is your first build:

1. **Install nRF Connect SDK** (v3.1.0 or later)
2. **Open nRF Connect SDK Command Prompt**
3. **Navigate to project**:
   ```batch
   cd C:\path\to\mipe_ev1_project
   ```
4. **Run build script**:
   ```batch
   build_and_flash.bat
   ```

That's it! The scripts handle everything else.
