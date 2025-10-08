@echo off
setlocal

:: ULTIMATE AUTONOMOUS DEPLOYMENT
:: Pristine build + Enhanced flash + Reset - NO PAUSES!
echo ========================================
echo MIPE_EV1 - ULTIMATE AUTONOMOUS DEPLOY
echo ========================================

echo Starting complete autonomous deployment...
echo.

:: Step 1: Pristine build
echo ======== STEP 1: PRISTINE BUILD ========
call build_pristine.bat
if %errorlevel% neq 0 (
    echo DEPLOYMENT FAILED at build stage
    exit /b 1
)

echo.
echo ======== STEP 2: ENHANCED FLASH ========
call flash_enhanced.bat
if %errorlevel% neq 0 (
    echo DEPLOYMENT FAILED at flash stage
    exit /b 1
)

echo.
echo ========================================
echo ULTIMATE DEPLOYMENT COMPLETE!
echo ========================================
echo ✅ Pristine build completed
echo ✅ Enhanced flash with sectorerase
echo ✅ Device reset and running
echo ✅ SPI WHO_AM_I active
echo.
echo 🎯 Check your Saleae for SPI activity!
echo    D0=CS, D1=CLK, D2=MOSI, D3=MISO
echo    Expected: WHO_AM_I reads every 2 seconds