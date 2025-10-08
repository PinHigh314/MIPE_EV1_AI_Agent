#!/usr/bin/env python3
"""
Quick SPI Activity Test
Check if the LEDs are working (indicates firmware is running)
Then check hardware status
"""

import subprocess
import time

def check_status():
    print("🔍 QUICK SPI ACTIVITY CHECK")
    print("=" * 40)
    
    # Check hardware connection
    try:
        result = subprocess.run(['nrfjprog', '--ids'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            print(f"✅ MIPE_EV1 Connected: {result.stdout.strip()}")
        else:
            print("❌ MIPE_EV1 not detected")
            return
    except Exception as e:
        print(f"❌ Connection check failed: {e}")
        return
    
    # Check if firmware is running
    try:
        result = subprocess.run(['nrfjprog', '--readregs'], 
                              capture_output=True, text=True, timeout=5)
        if 'PC:' in result.stdout:
            pc_lines = [line for line in result.stdout.split('\n') if 'PC:' in line]
            if pc_lines:
                pc = pc_lines[0].strip()
                print(f"✅ Firmware Running: {pc}")
            else:
                print("❌ Cannot read PC register")
                return
        else:
            print("❌ No PC register found")
            return
    except Exception as e:
        print(f"❌ Firmware check failed: {e}")
        return
    
    print("")
    print("🎯 WHAT TO LOOK FOR ON SALEAE:")
    print("Connected as: D0=CS(P2.5), D1=CLK(P2.1), D2=MOSI(P2.2), D3=MISO(P2.4)")
    print("")
    print("1. 📱 D5/D6 should show LED patterns (200ms toggle)")
    print("   - This confirms the board is running")
    print("")
    print("2. 🔄 Every ~2 seconds on SPI channels:")
    print("   - D0 (CS): Goes LOW for transaction")
    print("   - D1 (CLK): Should show 16 clock pulses")
    print("   - D2 (MOSI): Should show 0x8F 0x00")
    print("   - D3 (MISO): Should show response (0x00 0x6C if sensor connected)")
    print("")
    print("3. ⚙️ Saleae Settings:")
    print("   - Trigger: D1 (CLK) falling edge")
    print("   - Sample rate: 10MHz+") 
    print("   - Duration: 10 seconds")
    print("")
    
    if input("Start 30-second monitoring? (y/n): ").lower() == 'y':
        print("\n🔄 Monitoring for 30 seconds...")
        print("Watch your Saleae for SPI activity!")
        
        for i in range(30):
            print(f"⏱️  {30-i:2d} seconds remaining", end='\r')
            time.sleep(1)
        
        print("\n✅ Monitoring complete!")
        print("Did you see SPI activity on D0-D3?")
        print("LED patterns on D5-D6?")

if __name__ == "__main__":
    check_status()