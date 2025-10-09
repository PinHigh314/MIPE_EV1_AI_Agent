@echo off
REM MIPE_EV1 GPIO Test - Flash Only

echo ========================================
echo MIPE_EV1 GPIO Test - Flash Only
echo ========================================
echo.

REM Check if build exists
if not exist build\zephyr\zephyr.hex (
    echo ERROR: build\zephyr\zephyr.hex not found
    echo Please run build_mipe.bat first to build the project
    exit /b 1
)

echo Flashing firmware...
nrfjprog --program build\zephyr\zephyr.hex --chiperase --verify -r

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo FLASH SUCCESSFUL!
    echo ========================================
    echo.
) else (
    echo.
    echo FLASH FAILED!
    echo Try: nrfjprog --recover
    echo.
)
