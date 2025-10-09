@echo off
setlocal

echo ========================================
echo MIPE_EV1 - Milestone 1: GPIO Test
echo Build and Flash Script
echo ========================================
echo.
echo Usage: build_mipe.bat [options]
echo   Options:
echo     --clean or -c : Clean build (removes build directory first)
echo.

:: Set NCS environment variables
echo Setting up NCS environment...
set ZEPHYR_BASE=C:\ncs\v3.1.0\zephyr
set ZEPHYR_SDK_INSTALL_DIR=C:\ncs\toolchains\b8b84efebd\opt\zephyr-sdk
set ZEPHYR_TOOLCHAIN_VARIANT=zephyr

:: Add toolchain to PATH
set PATH=C:\ncs\toolchains\b8b84efebd\opt\bin;C:\ncs\toolchains\b8b84efebd\opt\bin\Scripts;%PATH%

echo Environment configured:
echo   ZEPHYR_BASE: %ZEPHYR_BASE%
echo.

:: Check for clean build flag
set clean_build=0
if "%1"=="--clean" set clean_build=1
if "%1"=="-c" set clean_build=1

:: Navigate to project directory
cd /d "%~dp0"
echo Working directory: %CD%
echo.

:: Check if CMakeLists.txt exists
if not exist CMakeLists.txt (
    echo ERROR: CMakeLists.txt not found
    exit /b 1
)

:: Check if custom board directory exists
if not exist boards\nordic\mipe_ev1 (
    echo ERROR: Custom board directory not found!
    exit /b 1
)

:: Clean build directory if requested
if %clean_build%==1 (
    echo Clean build requested...
    if exist build (
        echo Removing existing build directory...
        rmdir /s /q build
    )
)

:: Configure with CMake
echo Configuring project with CMake...
echo Board: mipe_ev1/nrf54l15/cpuapp
echo.

cmake -B build -G Ninja -DBOARD=mipe_ev1/nrf54l15/cpuapp

if %errorlevel% neq 0 (
    echo.
    echo CMake configuration failed!
    exit /b 1
)

echo.
echo CMake configuration successful!
echo.

:: Build with Ninja
echo Building project with Ninja...
ninja -C build

if %errorlevel% neq 0 (
    echo.
    echo Build failed!
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

:: Use simple output name
set output_name=MIPE_EV1_M1_latest.hex
echo Output filename: %output_name%

:: Copy hex file
echo.
echo Copying hex file to compiled_code directory...
if not exist "compiled_code" (
    echo Creating compiled_code directory...
    mkdir "compiled_code"
)

echo Copying: build\zephyr\zephyr.hex to compiled_code\%output_name%
copy build\zephyr\zephyr.hex "compiled_code\%output_name%"

if %errorlevel% equ 0 (
    echo SUCCESS: Hex file copied to: compiled_code\%output_name%
) else (
    echo WARNING: Failed to copy hex file
)

echo.
echo ========================================
echo Build Completed Successfully!
echo ========================================
echo.
echo Expected behavior after flash:
echo   1. Wait 1 second
echo   2. LED0 flashes once (200ms)
echo   3. LED1 flashes once (200ms)
echo   4. TestPin05 pulses (200ms)
echo   5. TestPin06 pulses (200ms)
echo   6. LED1 stays ON (test complete)
echo.
echo.
echo.
echo Build completed successfully!
echo.
echo To flash manually, run:
echo   nrfjprog --program build\zephyr\zephyr.hex --chiperase --verify -r
echo.
