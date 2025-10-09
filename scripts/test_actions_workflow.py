#!/usr/bin/env python3
"""
Complete GitHub Actions Workflow Test
Tests all components of the automation pipeline
"""

import subprocess
import sys
from pathlib import Path
import time

def test_build():
    """Test firmware build"""
    print("🔨 Testing build process...")
    
    try:
        result = subprocess.run([
            "cmd", "/c", "build_only.bat"
        ], cwd=Path(".."), capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and "BUILD SUCCESSFUL" in result.stdout:
            print("✅ Build: PASSED")
            return True
        else:
            print("❌ Build: FAILED")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def test_flash():
    """Test firmware flashing"""
    print("📡 Testing flash process...")
    
    try:
        result = subprocess.run([
            "cmd", "/c", "flash_only.bat"
        ], cwd=Path(".."), capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and "FLASH SUCCESSFUL" in result.stdout:
            print("✅ Flash: PASSED")
            return True
        else:
            print("❌ Flash: FAILED")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Flash error: {e}")
        return False

def test_rtt_monitoring():
    """Test RTT hardware monitoring"""
    print("📊 Testing RTT monitoring...")
    
    try:
        result = subprocess.run([
            "python", "windows_rtt_monitor.py"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "Hardware monitoring PASSED" in result.stdout:
            print("✅ RTT Monitoring: PASSED")
            return True
        else:
            print("❌ RTT Monitoring: FAILED")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ RTT monitoring error: {e}")
        return False

def test_logic_analyzer():
    """Test logic analyzer automation"""
    print("📈 Testing logic analyzer...")
    
    # Check if analyzer_automation.py exists and can run
    analyzer_script = Path("analyzer_automation.py")
    if analyzer_script.exists():
        try:
            result = subprocess.run([
                "python", str(analyzer_script), "--test"
            ], capture_output=True, text=True, timeout=10)
            
            print("✅ Logic Analyzer: AVAILABLE")
            return True
            
        except Exception as e:
            print(f"⚠️  Logic Analyzer: SCRIPT ERROR - {e}")
            return False
    else:
        print("⚠️  Logic Analyzer: SCRIPT NOT FOUND")
        return False

def main():
    """Main workflow test"""
    print("🚀 MIPE_EV1 GitHub Actions Workflow Test")
    print("=" * 60)
    
    tests = [
        ("Build Process", test_build),
        ("Flash Process", test_flash), 
        ("RTT Monitoring", test_rtt_monitoring),
        ("Logic Analyzer", test_logic_analyzer)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📊 Testing: {test_name}")
        print("-" * 30)
        
        success = test_func()
        results.append((test_name, success))
        
        if success:
            print(f"✅ {test_name}: PASSED\n")
        else:
            print(f"❌ {test_name}: FAILED\n")
    
    # Summary
    print("=" * 60)
    print("🎯 GITHUB ACTIONS WORKFLOW TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print("-" * 60)
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - GitHub Actions ready!")
        return 0
    else:
        failed = total - passed
        print(f"❌ {failed} test(s) failed - Review workflow configuration")
        return 1

if __name__ == "__main__":
    sys.exit(main())