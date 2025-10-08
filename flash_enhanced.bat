@echo off
setlocal

:: ENHANCED FLASH - Sectorerase + verify + reset
echo ========================================
echo MIPE_EV1 - ENHANCED FLASH & RESET
echo ========================================

if not exist "build\zephyr\zephyr.hex" (
    echo ERROR: No firmware file found!
    echo Run build_pristine.bat first
    exit /b 1
)

echo [1/3] Checking device connection...
nrfjprog --ids
if %errorlevel% neq 0 (
    echo ERROR: No device found! Check USB connection.
    exit /b 1
)

echo [2/3] Flashing with sectorerase + verify...
nrfjprog --program build\zephyr\zephyr.hex --sectorerase --verify

if %errorlevel% neq 0 (
    echo ERROR: Flash failed!
    echo Try: nrfjprog --recover
    exit /b 1
)

echo [3/3] Resetting device...
nrfjprog --reset

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo FLASH & RESET SUCCESS!
    echo ========================================
    echo Device is now running new firmware
    echo SPI WHO_AM_I should start immediately
    exit /b 0
) else (
    echo ERROR: Reset failed!
    exit /b 1
)