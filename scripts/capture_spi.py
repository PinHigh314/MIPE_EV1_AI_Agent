#!/usr/bin/env python3
"""
SALEAE LOGIC ANALYZER CAPTURE SCRIPT
Captures SPI signals from MIPE_EV1 → LSM6DSO32 communication
"""

import subprocess
import time
import os
from datetime import datetime

def capture_spi_signals():
    """Capture SPI signals using Saleae Logic Analyzer"""
    
    print("🔍 SALEAE LOGIC ANALYZER - SPI CAPTURE")
    print("=" * 50)
    
    # SPI Pin assignments for MIPE_EV1
    print("📌 EXPECTED SPI PIN CONNECTIONS:")
    print("  D0 → MOSI (P2.2)  - Data from MIPE_EV1 to LSM6DSO32")
    print("  D1 → MISO (P2.4)  - Data from LSM6DSO32 to MIPE_EV1") 
    print("  D2 → SCK  (P2.1)  - Clock signal")
    print("  D3 → CS   (P2.5)  - Chip select (active low)")
    print("")
    
    # Create captures directory
    capture_dir = "analyzer_captures"
    os.makedirs(capture_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Try multiple approaches for capture
    
    # Method 1: Try with sigrok (might work with some settings)
    print("🔄 METHOD 1: Attempting sigrok capture...")
    try:
        # Basic sigrok capture command for Saleae
        cmd = [
            "C:\\Program Files\\sigrok\\sigrok-cli\\sigrok-cli.exe",
            "--driver", "saleae-logic16",
            "--time", "5s",  # 5 second capture
            "--channels", "D0,D1,D2,D3",  # SPI channels
            "--triggers", "D2=r",  # Trigger on rising edge of clock
            "--output-format", "csv", 
            "--output-file", f"{capture_dir}/spi_capture_{timestamp}.csv"
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Sigrok capture successful!")
            print(f"📁 Saved to: {capture_dir}/spi_capture_{timestamp}.csv")
            return True
        else:
            print(f"❌ Sigrok failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Sigrok method failed: {e}")
    
    # Method 2: Instructions for Saleae Logic software
    print("\n🔄 METHOD 2: Manual Saleae Logic Software")
    print("Since sigrok may not work perfectly with Saleae devices,")
    print("use the official Saleae Logic software:")
    print("")
    print("SETUP INSTRUCTIONS:")
    print("1. 📱 Open Saleae Logic software")
    print("2. 🔌 Connect analyzer channels to MIPE_EV1:")
    print("   - Channel 0 → P2.2  (MOSI)")
    print("   - Channel 1 → P2.4  (MISO)")
    print("   - Channel 2 → P2.1  (SCK)")
    print("   - Channel 3 → P2.5  (CS)")
    print("3. ⚙️  Set sample rate: 10 MHz or higher")
    print("4. ⏱️  Set capture time: 5-10 seconds")
    print("5. 🎯 Set trigger: Rising edge on Channel 2 (SCK)")
    print("6. ▶️  Start capture")
    print("7. 💾 Export as CSV to:", f"{capture_dir}/")
    print("")
    
    # Method 3: Create a monitoring script
    print("🔄 METHOD 3: Creating monitoring script...")
    
    monitor_script = f"""
import time
import subprocess

print("🤖 SPI COMMUNICATION MONITOR")
print("Monitoring MIPE_EV1 SPI communication...")
print("Press Ctrl+C to stop")

try:
    while True:
        # Check if board is still running
        result = subprocess.run([
            'nrfjprog', '--readregs'
        ], capture_output=True, text=True)
        
        if 'PC' in result.stdout:
            pc_line = [line for line in result.stdout.split('\\n') if 'PC' in line]
            if pc_line:
                print(f"⚡ MIPE_EV1 running: {{pc_line[0].strip()}}")
        
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\\n🛑 Monitoring stopped")
"""
    
    with open(f"{capture_dir}/spi_monitor.py", 'w') as f:
        f.write(monitor_script)
    
    print(f"✅ Created SPI monitor script: {capture_dir}/spi_monitor.py")
    print("")
    print("🎯 NEXT STEPS:")
    print("1. Connect your Saleae analyzer to the SPI pins")
    print("2. Use Saleae Logic software for capture (most reliable)")
    print("3. Monitor with: python analyzer_captures/spi_monitor.py")
    print("4. Share the captured CSV files for AI analysis!")
    
    return False

if __name__ == "__main__":
    capture_spi_signals()