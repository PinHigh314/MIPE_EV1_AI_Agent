#!/usr/bin/env python3
"""
Quick RTT Connection Test for MIPE_EV1
Verify J-Link and RTT setup before running full monitoring
"""

import subprocess
import sys
from pathlib import Path

def test_jlink_connection():
    """Test J-Link connection to MIPE_EV1"""
    print("🔍 Testing J-Link connection to MIPE_EV1...")
    
    jlink_exe = r"C:\Program Files\SEGGER\JLink_V874a\JLink.exe"
    
    if not Path(jlink_exe).exists():
        print(f"❌ J-Link not found at: {jlink_exe}")
        return False
    
    # Test J-Link connection with nrfjprog
    try:
        result = subprocess.run([
            "nrfjprog", "--ids"
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0 and result.stdout.strip():
            print(f"✅ J-Link devices found:")
            print(result.stdout.strip())
            return True
        else:
            print("❌ No J-Link devices detected")
            print(f"nrfjprog output: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ J-Link connection test timed out")
        return False
    except FileNotFoundError:
        print("❌ nrfjprog not found - ensure NCS tools are in PATH")
        return False
    except Exception as e:
        print(f"❌ J-Link test failed: {e}")
        return False

def test_rtt_tools():
    """Test RTT tools availability"""
    print("🔍 Testing RTT tools availability...")
    
    rtt_logger = r"C:\Program Files\SEGGER\JLink_V874a\JLinkRTTLogger.exe"
    
    if Path(rtt_logger).exists():
        print(f"✅ RTT Logger found: {rtt_logger}")
        return True
    else:
        print(f"❌ RTT Logger not found: {rtt_logger}")
        return False

def main():
    """Run all RTT setup tests"""
    print("MIPE_EV1 RTT Setup Test")
    print("=" * 40)
    
    tests = [
        ("J-Link Connection", test_jlink_connection),
        ("RTT Tools", test_rtt_tools)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        success = test_func()
        results.append(success)
        print(f"Result: {'PASS' if success else 'FAIL'}")
    
    print("\n" + "=" * 40)
    print("RTT Setup Test Summary:")
    
    all_passed = all(results)
    if all_passed:
        print("All tests PASSED - RTT monitoring ready!")
        return 0
    else:
        failed_count = len([r for r in results if not r])
        print(f"{failed_count} test(s) FAILED - RTT setup incomplete")
        print("\nTroubleshooting:")
        print("   - Ensure MIPE_EV1 is connected via J-Link")
        print("   - Verify J-Link tools are installed")
        print("   - Check USB connections and drivers")
        return 1

if __name__ == "__main__":
    sys.exit(main())