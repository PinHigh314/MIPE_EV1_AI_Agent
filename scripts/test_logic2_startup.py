#!/usr/bin/env python3
"""
Test Logic 2 Auto-Startup Functionality
Verifies that Logic 2 can be detected and started automatically
"""

import sys
import time
from analyzer_automation import AnalyzerAutomation

def test_logic2_detection():
    """Test Logic 2 detection functionality"""
    print("Testing Logic 2 Detection and Auto-Startup")
    print("=" * 50)
    
    analyzer = AnalyzerAutomation()
    
    # Test 1: Check current status
    print("1. Checking current Logic 2 status...")
    is_running = analyzer.check_logic2_running()
    print(f"   Logic 2 running: {is_running}")
    
    # Test 2: Ensure Logic 2 is available
    print("\n2. Ensuring Logic 2 is available...")
    success = analyzer.start_logic2()
    print(f"   Logic 2 startup success: {success}")
    
    # Test 3: Verify it's running after startup
    print("\n3. Verifying Logic 2 is running...")
    final_status = analyzer.check_logic2_running()
    print(f"   Final Logic 2 status: {final_status}")
    
    # Test 4: Test device scanning
    print("\n4. Testing device scanning...")
    devices_found = analyzer.scan_devices()
    print(f"   Devices detected: {devices_found}")
    
    print("\n" + "=" * 50)
    print("Logic 2 Auto-Startup Test Results:")
    print(f"  Detection: {'PASS' if analyzer.check_logic2_running() else 'FAIL'}")
    print(f"  Startup: {'PASS' if success else 'WARN'}")
    print(f"  Scanning: {'PASS' if devices_found else 'WARN'}")
    
    if analyzer.check_logic2_running():
        print("\nLogic 2 is ready for GitHub Actions automation!")
        return 0
    else:
        print("\nLogic 2 auto-startup needs manual verification")
        return 1

if __name__ == "__main__":
    sys.exit(test_logic2_detection())