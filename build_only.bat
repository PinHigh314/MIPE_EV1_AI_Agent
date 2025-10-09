@echo off
setlocal

echo ========================================
echo MIPE_EV1 GPIO Test - Build Only
echo ========================================
echo.

:: Set NCS environment variables
set ZEPHYR_BASE=C:\ncs\v3.1.0\zephyr
set ZEPHYR_SDK_INSTALL_DIR=C:\ncs\toolchains\b8b84efebd\opt\zephyr-sdk
set ZEPHYR_TOOLCHAIN_VARIANT=zephyr
set PATH=C:\ncs\toolchains\b8b84efebd\opt\bin;C:\ncs\toolchains\b8b84efebd\opt\bin\Scripts;%PATH%

:: Navigate to project directory
cd /d "%~dp0"

:: Configure with CMake
echo Configuring project with CMake...
cmake -B build -G Ninja -DBOARD=mipe_ev1/nrf54l15/cpuapp

if %errorlevel% neq 0 (
    echo.
    echo CMake configuration failed!
    exit /b 1
)

:: Build with Ninja
echo Building project with Ninja...
ninja -C build

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Output files:
    echo   build\zephyr\zephyr.hex
    echo   build\zephyr\zephyr.elf
    echo.
    echo To flash: flash_only.bat
    echo.
) else (
    echo.
    echo Build failed!
    echo.
)
