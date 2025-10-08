@echo off
setlocal

:: Non-interactive flash script - no pauses
echo ========================================
echo MIPE_EV1 - Non-Interactive Flash
echo ========================================

if not exist "build\zephyr\zephyr.hex" (
    echo ERROR: No firmware file found!
    echo Run build_auto.bat first
    exit /b 1
)

echo Flashing firmware to MIPE_EV1...
nrfjprog --program build\zephyr\zephyr.hex --sectorerase --verify --reset

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo FLASH SUCCESS - NO PAUSES!
    echo ========================================
    echo Firmware running on MIPE_EV1
    echo Ready for SPI communication!
    exit /b 0
) else (
    echo ERROR: Flash failed!
    exit /b 1
)