@echo off
REM MIPE_EV1 RTT Hardware Monitoring Script
REM For GitHub Actions integration

echo 🚀 MIPE_EV1 RTT Hardware Monitoring
echo ===================================

REM Set paths (without extra quotes)
set "JLINK_PATH=C:\Program Files\SEGGER\JLink_V874a"
set "RTT_LOGGER=%JLINK_PATH%\JLinkRTTLogger.exe"

REM Create logs directory
if not exist "rtt_logs" mkdir rtt_logs

REM Generate simple timestamp
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do set "datestr=%%a%%b%%c"
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set "timestr=%%a%%b"
set "timestamp=%datestr%_%timestr%"

echo ⏱️  Timestamp: %timestamp%
echo 🎯 Target: nRF54L15_xxAA
echo 📝 Log directory: rtt_logs\

REM Check if J-Link tools exist
if not exist "%RTT_LOGGER%" (
    echo ❌ J-Link RTT Logger not found at: %RTT_LOGGER%
    echo 💡 Please ensure J-Link tools are installed
    exit /b 1
)

echo ✅ J-Link tools found

REM Start RTT logging (5 seconds for fast Actions)
echo 📊 Starting RTT capture for 5 seconds...
set "LOG_FILE=rtt_logs\rtt_capture_%timestamp%.txt"

echo 📡 Starting RTT Logger...
REM Try nRF54L15 first, fallback to auto-detect
"%RTT_LOGGER%" -device nRF54L15 -if SWD -speed 4000 -rttchannel 0 "%LOG_FILE%" > nul 2>&1 &

REM If that fails, try with auto-detect
if errorlevel 1 (
    echo 🔄 Retrying with auto-detect...
    "%RTT_LOGGER%" -if SWD -speed 4000 -rttchannel 0 "%LOG_FILE%" > nul 2>&1 &
)

echo ⏳ Monitoring hardware activity for 5 seconds...

REM Wait 5 seconds
timeout /t 5 /nobreak > nul

REM Stop RTT logging
echo 🛑 Stopping RTT capture...
taskkill /F /IM JLinkRTTLogger.exe > nul 2>&1

REM Wait a moment for file to be written
timeout /t 2 /nobreak > nul

REM Check if log file was created
if exist "%LOG_FILE%" (
    echo ✅ RTT log captured: %LOG_FILE%
    
    REM Show log file size
    for %%A in ("%LOG_FILE%") do (
        echo 📄 Log size: %%~zA bytes
    )
    
    REM Count GPIO activity lines - use findstr instead of find
    findstr /C:"Cycle" "%LOG_FILE%" > temp_cycles.txt 2>nul
    for /f %%C in ('type temp_cycles.txt 2^>nul ^| find /c /v ""') do set cycle_count=%%C
    del temp_cycles.txt > nul 2>&1
    
    echo 🔄 GPIO cycles detected: %cycle_count%
    
    if %cycle_count% GTR 0 (
        echo 🎉 Hardware monitoring PASSED - GPIO activity detected!
        exit /b 0
    ) else (
        echo ❌ Hardware monitoring FAILED - No GPIO activity detected!
        echo 📋 Log content preview:
        type "%LOG_FILE%" 2>nul | head -10
        exit /b 1
    )
) else (
    echo ❌ RTT log file not created - Check hardware connection
    exit /b 1
)