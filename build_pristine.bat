@echo off
setlocal

:: PRISTINE BUILD - Always clean, no cache, no pauses
echo ========================================
echo MIPE_EV1 - PRISTINE BUILD (CLEAN)
echo ========================================

:: Set NCS environment variables
set ZEPHYR_BASE=C:\ncs\v3.1.0\zephyr
set ZEPHYR_SDK_INSTALL_DIR=C:\ncs\toolchains\b8b84efebd\opt\zephyr-sdk
set ZEPHYR_TOOLCHAIN_VARIANT=zephyr
set PATH=C:\ncs\toolchains\b8b84efebd\opt\bin;C:\ncs\toolchains\b8b84efebd\opt\bin\Scripts;%PATH%

:: Navigate to project directory
cd /d "%~dp0"

echo [1/3] Cleaning build directory...
if exist build (
    rmdir /s /q build
    echo Build directory removed
)

echo [2/3] Configuring with CMake (pristine)...
cmake -B build -G Ninja -DBOARD=mipe_ev1/nrf54l15/cpuapp

if %errorlevel% neq 0 (
    echo ERROR: CMake configuration failed!
    exit /b 1
)

echo [3/3] Building with Ninja (clean build)...
ninja -C build

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo PRISTINE BUILD SUCCESS!
    echo ========================================
    echo Output: build\zephyr\zephyr.hex
    echo Ready for flashing!
    exit /b 0
) else (
    echo ERROR: Build failed!
    exit /b 1
)