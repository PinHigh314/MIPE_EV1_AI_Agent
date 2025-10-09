@echo off
setlocal

echo ========================================
echo MIPE_EV2 Build Script
echo ========================================

set ZEPHYR_BASE=C:\ncs\v3.1.0\zephyr
set ZEPHYR_SDK_INSTALL_DIR=C:\ncs\toolchains\b8b84efebd\opt\zephyr-sdk
set ZEPHYR_TOOLCHAIN_VARIANT=zephyr
set PATH=C:\ncs\toolchains\b8b84efebd\opt\bin;C:\ncs\toolchains\b8b84efebd\opt\bin\Scripts;%PATH%

cd /d "%~dp0"

if exist build rmdir /s /q build

cmake -B build -G Ninja -DBOARD=mipe_ev2/nrf54l15/cpuapp
ninja -C build

if %errorlevel% neq 0 (
    echo Build failed!
    exit /b 1
)

echo Build successful!