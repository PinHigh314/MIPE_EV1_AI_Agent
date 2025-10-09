@echo off
setlocal

echo ========================================
echo MIPE_EV2 Build and Flash
echo ========================================

call build_mipe_ev2.bat

if %errorlevel% neq 0 (
    echo Build failed - cannot flash
    exit /b 1
)

echo Flashing...
nrfjprog --program build\zephyr\zephyr.hex --sectorerase --verify --reset

if %errorlevel% neq 0 (
    echo Flash failed!
    exit /b 1
)

echo MIPE_EV2 flashed successfully!
echo Expected: 23ms toggle on P1.05/P1.06