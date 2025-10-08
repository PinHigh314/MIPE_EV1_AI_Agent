@echo off
setlocal

:: Non-interactive build script for CI/CD and autonomous development
:: No pause commands - runs completely automatically

echo ========================================
echo MIPE_EV1 - Non-Interactive Build
echo ========================================

:: Set NCS environment variables
set ZEPHYR_BASE=C:\ncs\v3.1.0\zephyr
set ZEPHYR_SDK_INSTALL_DIR=C:\ncs\toolchains\b8b84efebd\opt\zephyr-sdk
set ZEPHYR_TOOLCHAIN_VARIANT=zephyr
set PATH=C:\ncs\toolchains\b8b84efebd\opt\bin;C:\ncs\toolchains\b8b84efebd\opt\bin\Scripts;%PATH%

:: Navigate to project directory
cd /d "%~dp0"

echo [1/2] Configuring with CMake...
cmake -B build -G Ninja -DBOARD=mipe_ev1/nrf54l15/cpuapp

if %errorlevel% neq 0 (
    echo ERROR: CMake configuration failed!
    exit /b 1
)

echo [2/2] Building with Ninja...
ninja -C build

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo BUILD SUCCESS - NO PAUSES!
    echo ========================================
    echo Output: build\zephyr\zephyr.hex
    echo Ready for autonomous development!
    exit /b 0
) else (
    echo ERROR: Build failed!
    exit /b 1
)