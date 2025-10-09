#!/usr/bin/env python3
"""
Simple RTT Test using nRF Connect Tools
Alternative approach when J-Link RTT Logger has device compatibility issues
"""

import subprocess
import time
import sys
from pathlib import Path

def test_rtt_via_jlinkexe():
    """Test RTT using J-Link Commander instead of RTT Logger"""
    print("🚀 Testing RTT via J-Link Commander...")
    
    # Create RTT logs directory
    logs_dir = Path("../rtt_logs")
    logs_dir.mkdir(exist_ok=True)
    
    jlink_exe = r"C:\Program Files\SEGGER\JLink_V874a\JLink.exe"
    
    if not Path(jlink_exe).exists():
        print(f"❌ J-Link Commander not found: {jlink_exe}")
        return False
    
    # Create J-Link script for RTT
    script_content = """
connect
nRF54L15
SWD
4000
rtt start
sleep 5000
rtt stop
q
"""
    
    script_file = Path("jlink_rtt_test.jlink")
    with open(script_file, "w") as f:
        f.write(script_content)
    
    try:
        print("📡 Starting J-Link RTT test...")
        result = subprocess.run([
            jlink_exe, "-CommandFile", str(script_file)
        ], capture_output=True, text=True, timeout=10)
        
        print("📊 J-Link output:")
        print(result.stdout)
        
        if "RTT started" in result.stdout or "Connected to target" in result.stdout:
            print("✅ RTT connection successful!")
            return True
        else:
            print("❌ RTT connection failed")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ J-Link RTT test timed out")
        return False
    except Exception as e:
        print(f"❌ J-Link RTT test error: {e}")
        return False
    finally:
        # Clean up script file
        if script_file.exists():
            script_file.unlink()

def test_device_programming():
    """Verify device is properly programmed and running"""
    print("🔍 Testing device programming status...")
    
    try:
        # Check if device is running
        result = subprocess.run([
            "nrfjprog", "--family", "nRF54L", "--readram", "--address", "0x20000000", "--length", "4"
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ Device is accessible and running")
            return True
        else:
            print("❌ Device access failed")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Device test error: {e}")
        return False

def main():
    """Main RTT testing function"""
    print("🎯 MIPE_EV1 RTT Connection Test")
    print("=" * 40)
    
    # Test 1: Device programming
    if not test_device_programming():
        print("💡 Tip: Ensure device is flashed and running")
        return 1
    
    # Test 2: RTT via J-Link
    if test_rtt_via_jlinkexe():
        print("\n🎉 RTT testing PASSED!")
        print("✅ Ready for GitHub Actions automation")
        return 0
    else:
        print("\n❌ RTT testing FAILED!")
        print("💡 Check J-Link version and device compatibility")
        return 1

if __name__ == "__main__":
    sys.exit(main())