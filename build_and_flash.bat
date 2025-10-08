@echo off
setlocal

echo ========================================
echo MIPE_EV1 GPIO Test - Build and Flash
echo ========================================
echo.

:: Set NCS environment variables (SAME AS OLD WORKING SCRIPT)
echo Setting up NCS environment...
set ZEPHYR_BASE=C:\ncs\v3.1.0\zephyr
set ZEPHYR_SDK_INSTALL_DIR=C:\ncs\toolchains\b8b84efebd\opt\zephyr-sdk
set ZEPHYR_TOOLCHAIN_VARIANT=zephyr

:: Add toolchain to PATH (SAME AS OLD WORKING SCRIPT)
set PATH=C:\ncs\toolchains\b8b84efebd\opt\bin;C:\ncs\toolchains\b8b84efebd\opt\bin\Scripts;%PATH%

echo Environment configured:
echo   ZEPHYR_BASE: %ZEPHYR_BASE%
echo.

:: Navigate to project directory
cd /d "%~dp0"
echo Working directory: %CD%
echo.

:: Check if CMakeLists.txt exists
if not exist CMakeLists.txt (
    echo ERROR: CMakeLists.txt not found
    pause
    exit /b 1
)

:: Check if custom board directory exists
if not exist boards\nordic\mipe_ev1 (
    echo ERROR: Custom board directory not found!
    pause
    exit /b 1
)

:: Clean build directory
echo Step 1: Cleaning previous build...
if exist build (
    echo Removing existing build directory...
    rmdir /s /q build
)
echo.

:: Configure with CMake
echo Step 2: Configuring project with CMake...
echo Board: mipe_ev1/nrf54l15/cpuapp
echo.

cmake -B build -G Ninja -DBOARD=mipe_ev1/nrf54l15/cpuapp

if %errorlevel% neq 0 (
    echo.
    echo CMake configuration failed!
    pause
    exit /b 1
)

echo.
echo CMake configuration successful!
echo.

:: Build with Ninja
echo Step 3: Building project with Ninja...
ninja -C build

if %errorlevel% neq 0 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build Completed Successfully!
echo ========================================
echo.

:: Display build artifacts
if exist build\zephyr\zephyr.hex (
    echo Build artifacts:
    echo   HEX file: %CD%\build\zephyr\zephyr.hex
    for %%F in (build\zephyr\zephyr.hex) do echo   Size: %%~zF bytes
)

if exist build\zephyr\zephyr.elf (
    echo   ELF file: %CD%\build\zephyr\zephyr.elf
    for %%F in (build\zephyr\zephyr.elf) do echo   Size: %%~zF bytes
)

echo.

:: Flash to board
echo Step 4: Flashing device...
nrfjprog --program build\zephyr\zephyr.hex --chiperase --verify -r

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Device flashed successfully!
    echo ========================================
    echo.
    echo Expected behavior:
    echo - All pins (P0.00, P0.01, P1.05, P1.06) start LOW
    echo - After 1 second, all pins go HIGH
    echo - Pins stay HIGH forever
    echo.
    echo Test with oscilloscope or multimeter.
) else (
    echo.
    echo ========================================
    echo Flash failed! Please check:
    echo ========================================
    echo   - J-Link is connected (SWDIO, SWDCLK, VDD, GND)
    echo   - Board is powered
    echo   - nrfjprog is in your PATH
    echo.
    echo To manually flash later:
    echo   nrfjprog --program build\zephyr\zephyr.hex --chiperase --verify -r
)

echo.
pause
