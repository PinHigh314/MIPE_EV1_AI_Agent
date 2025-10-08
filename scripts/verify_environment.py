#!/usr/bin/env python3
"""
MIPE_EV1 AI Agent Environment Verification
Checks if all components are ready for autonomous development
"""

import subprocess
import os
import sys
from pathlib import Path

def check_command(cmd, description):
    """Check if a command exists and works"""
    print(f"🔍 Checking {description}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"   ✅ {description} - OK")
            return True
        else:
            print(f"   ❌ {description} - Failed")
            print(f"      Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"   ❌ {description} - Error: {e}")
        return False

def check_file_exists(file_path, description):
    """Check if a file exists"""
    print(f"🔍 Checking {description}...")
    if Path(file_path).exists():
        print(f"   ✅ {description} - Found")
        return True
    else:
        print(f"   ❌ {description} - Not found")
        return False

def main():
    print("🤖 MIPE_EV1 AI Agent Environment Verification")
    print("=" * 50)
    
    all_checks = []
    
    # 1. Git Configuration
    print("\n📋 Git Configuration:")
    all_checks.append(check_command("git --version", "Git installed"))
    all_checks.append(check_command("git config --global user.name", "Git user configured"))
    all_checks.append(check_command("git config --global user.email", "Git email configured"))
    
    # 2. Repository Status
    print("\n📋 Repository Status:")
    all_checks.append(check_command("git remote -v", "GitHub remote configured"))
    all_checks.append(check_command("git status", "Git repository working"))
    
    # 3. Nordic nRF Connect SDK
    print("\n📋 Nordic nRF Connect SDK:")
    all_checks.append(check_command("west --version", "West build tool"))
    all_checks.append(check_command("west list", "West workspace configured"))
    
    # 4. Python Environment
    print("\n📋 Python Environment:")
    all_checks.append(check_command("python --version", "Python installed"))
    all_checks.append(check_command("python -c \"import subprocess, pathlib, datetime, re, os\"", "Required Python modules"))
    
    # 5. Logic Analyzer
    print("\n📋 Logic Analyzer:")
    sigrok_path = "C:\\Program Files\\sigrok\\sigrok-cli\\sigrok-cli.exe"
    if check_file_exists(sigrok_path, "sigrok-cli executable"):
        all_checks.append(check_command(f'"{sigrok_path}" --version', "sigrok-cli working"))
        # Try to scan for devices
        print("🔍 Scanning for logic analyzer devices...")
        try:
            result = subprocess.run([sigrok_path, "--scan"], capture_output=True, text=True)
            if "fx2lafw" in result.stdout:
                print("   ✅ Logic analyzer detected (fx2lafw)")
                all_checks.append(True)
            else:
                print("   ⚠️  No fx2lafw device detected")
                print("      Make sure logic analyzer is connected")
                all_checks.append(False)
        except Exception as e:
            print(f"   ❌ Device scan failed: {e}")
            all_checks.append(False)
    else:
        all_checks.append(False)
    
    # 6. Hardware Files
    print("\n📋 Project Files:")
    project_files = [
        ("src/main.c", "Main application"),
        ("boards/nordic/mipe_ev1/mipe_ev1_nrf54l15_cpuapp.dts", "Device tree"),
        ("scripts/enhanced_ai_generator.py", "AI code generator"),
        ("scripts/analyzer_automation.py", "Logic analyzer automation"),
        (".github/workflows/spi-development.yml", "GitHub Actions workflow")
    ]
    
    for file_path, description in project_files:
        all_checks.append(check_file_exists(file_path, description))
    
    # 7. Build Test
    print("\n📋 Build System Test:")
    print("🔍 Testing firmware build...")
    try:
        build_cmd = ["west", "build", "-b", "mipe_ev1_nrf54l15_cpuapp", "--build-dir", "build_test"]
        result = subprocess.run(build_cmd, capture_output=True, text=True, cwd="C:/Development/MIPE_EV1")
        if result.returncode == 0:
            print("   ✅ Test build successful")
            all_checks.append(True)
            # Clean up test build
            try:
                import shutil
                test_build_path = Path("C:/Development/MIPE_EV1/build_test")
                if test_build_path.exists():
                    shutil.rmtree(test_build_path)
                    print("   🧹 Test build cleaned up")
            except:
                pass
        else:
            print("   ❌ Test build failed")
            print(f"      Error: {result.stderr.strip()}")
            all_checks.append(False)
    except Exception as e:
        print(f"   ❌ Build test error: {e}")
        all_checks.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total) * 100
    
    print(f"✅ Passed: {passed}/{total} checks ({percentage:.1f}%)")
    
    if percentage >= 90:
        print("\n🎉 EXCELLENT! Your environment is ready for AI agent development!")
        print("🚀 You can now:")
        print("   • Run: python scripts/enhanced_ai_generator.py")
        print("   • Set up GitHub Actions runner for 24/7 automation")
        print("   • Push changes to trigger autonomous development")
    elif percentage >= 70:
        print("\n⚠️  GOOD! Most components ready, but some issues need attention.")
        print("🔧 Fix the failed checks above before running the AI agent.")
    else:
        print("\n❌ NEEDS WORK! Several components need setup before AI agent can run.")
        print("📖 See docs/GITHUB_RUNNER_SETUP.md for detailed instructions.")
    
    print(f"\n📖 For detailed setup instructions:")
    print("   • docs/GITHUB_RUNNER_SETUP.md")
    print("   • https://github.com/PinHigh314/MIPE_EV1_AI_Agent")
    
    return percentage >= 90

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)