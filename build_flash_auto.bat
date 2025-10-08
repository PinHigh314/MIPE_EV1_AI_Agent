@echo off
setlocal

:: Complete autonomous build and flash - NO PAUSES!
echo ========================================
echo MIPE_EV1 - AUTONOMOUS BUILD & FLASH
echo ========================================

:: Build first
call build_auto.bat
if %errorlevel% neq 0 (
    echo FAILED at build stage
    exit /b 1
)

echo.
echo Build complete, now flashing...

:: Flash automatically
call flash_auto.bat
if %errorlevel% neq 0 (
    echo FAILED at flash stage
    exit /b 1
)

echo.
echo ========================================
echo AUTONOMOUS DEPLOYMENT COMPLETE!
echo ========================================
echo MIPE_EV1 is now running with SPI firmware
echo Check Saleae for WHO_AM_I transactions!