#!/usr/bin/env python3
"""
MIPE_EV1 AI Agent - Non-Interactive Hardware Testing
Runs without prompts, provides complete status reports
"""

import subprocess
import time
import os
from datetime import datetime
from pathlib import Path

class NonInteractiveAI:
    def __init__(self):
        self.project_root = Path("C:/Development/MIPE_EV1")
        self.log_file = self.project_root / "ai_test_results.txt"
        
    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        try:
            with open(self.log_file, "a", encoding='utf-8') as f:
                f.write(log_msg + "\n")
        except:
            # Fallback without emoji
            safe_msg = log_msg.encode('ascii', 'ignore').decode('ascii')
            with open(self.log_file, "a") as f:
                f.write(safe_msg + "\n")
            
    def check_hardware_connection(self):
        """Check if MIPE_EV1 is connected"""
        self.log("🔍 Checking MIPE_EV1 connection...")
        try:
            result = subprocess.run(["nrfjprog", "--ids"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and result.stdout.strip():
                device_id = result.stdout.strip()
                self.log(f"✅ MIPE_EV1 connected: {device_id}")
                return device_id
            else:
                self.log("❌ No Nordic device detected")
                return None
        except Exception as e:
            self.log(f"❌ Hardware check failed: {e}")
            return None
            
    def check_board_status(self):
        """Check if board is running"""
        self.log("📊 Checking board status...")
        try:
            result = subprocess.run(["nrfjprog", "--readregs"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                # Extract PC (Program Counter) to see if running
                lines = result.stdout.split('\n')
                pc_line = [line for line in lines if 'PC:' in line]
                if pc_line:
                    pc_value = pc_line[0].split(':')[1].strip()
                    self.log(f"✅ Board running, PC: {pc_value}")
                    return True
                else:
                    self.log("⚠️ Board connected but status unclear")
                    return False
        except Exception as e:
            self.log(f"❌ Status check failed: {e}")
            return False
            
    def check_logic_analyzer(self):
        """Check logic analyzer without getting stuck"""
        self.log("🔍 Checking logic analyzer...")
        try:
            # Use timeout to avoid hanging
            result = subprocess.run([
                "C:\\Program Files\\sigrok\\sigrok-cli\\sigrok-cli.exe", 
                "--scan"
            ], capture_output=True, text=True, timeout=15)
            
            if "fx2lafw" in result.stdout:
                self.log("✅ Logic analyzer detected (fx2lafw)")
                return True
            else:
                self.log("❌ Logic analyzer not detected")
                self.log(f"Scanner output: {result.stdout}")
                return False
        except subprocess.TimeoutExpired:
            self.log("⚠️ Logic analyzer scan timed out (15s)")
            return False
        except Exception as e:
            self.log(f"❌ Logic analyzer check failed: {e}")
            return False
            
    def capture_quick_sample(self):
        """Capture a quick sample without hanging"""
        self.log("📊 Attempting quick signal capture...")
        try:
            # Very short capture to avoid hanging
            result = subprocess.run([
                "C:\\Program Files\\sigrok\\sigrok-cli\\sigrok-cli.exe",
                "--driver", "fx2lafw:conn=3.22",
                "--config", "samplerate=1000000",  # 1MHz
                "--samples", "10000",  # Small sample
                "--channels", "D0,D1,D2,D3",
                "--output-format", "csv"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.log("✅ Quick capture successful")
                # Save sample
                with open(self.project_root / "quick_capture.csv", "w") as f:
                    f.write(result.stdout)
                return True
            else:
                self.log(f"❌ Capture failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log("⚠️ Capture timed out (10s)")
            return False
        except Exception as e:
            self.log(f"❌ Capture error: {e}")
            return False
            
    def analyze_system_readiness(self):
        """Complete system analysis without hanging"""
        self.log("🤖 MIPE_EV1 AI Agent - Non-Interactive Analysis")
        self.log("=" * 50)
        
        # Clear previous log
        if self.log_file.exists():
            self.log_file.unlink()
            
        # Start fresh log
        self.log("🚀 Starting autonomous hardware analysis...")
        
        # Check all components
        hw_connected = self.check_hardware_connection()
        board_running = self.check_board_status() if hw_connected else False
        analyzer_ready = self.check_logic_analyzer()
        capture_working = self.capture_quick_sample() if analyzer_ready else False
        
        # Summary
        self.log("\n" + "=" * 50)
        self.log("📊 AUTONOMOUS SYSTEM STATUS")
        self.log("=" * 50)
        
        status = {
            "Hardware Connection": "✅" if hw_connected else "❌",
            "Board Running": "✅" if board_running else "❌", 
            "Logic Analyzer": "✅" if analyzer_ready else "❌",
            "Signal Capture": "✅" if capture_working else "❌"
        }
        
        for component, result in status.items():
            self.log(f"{component}: {result}")
            
        ready_count = sum(1 for s in status.values() if s == "✅")
        total_count = len(status)
        readiness = (ready_count / total_count) * 100
        
        self.log(f"\n🎯 System Readiness: {ready_count}/{total_count} ({readiness:.1f}%)")
        
        if readiness >= 75:
            self.log("🎉 SYSTEM READY FOR AUTONOMOUS DEVELOPMENT!")
            self.log("🚀 AI agent can proceed with hardware-in-the-loop testing")
        elif readiness >= 50:
            self.log("⚠️ PARTIAL READINESS - Some components need attention")
        else:
            self.log("❌ SYSTEM NOT READY - Multiple issues need resolution")
            
        # Next steps
        self.log("\n🔧 NEXT STEPS:")
        if not hw_connected:
            self.log("  • Connect MIPE_EV1 via USB")
        if not board_running:
            self.log("  • Flash firmware: nrfjprog --program build/zephyr/zephyr.hex --verify --reset")
        if not analyzer_ready:
            self.log("  • Connect logic analyzer and check drivers")
        if not capture_working:
            self.log("  • Verify logic analyzer probe connections")
            
        self.log(f"\n📄 Full log saved to: {self.log_file}")
        self.log("🤖 Non-interactive analysis complete!")
        
        return readiness >= 75

def main():
    """Run non-interactive AI analysis"""
    ai = NonInteractiveAI()
    success = ai.analyze_system_readiness()
    
    if success:
        print("\n🎉 Ready for cloud-based autonomous development!")
        print("🌐 Push changes to GitHub to trigger AI agent")
    else:
        print("\n🔧 Fix the issues above, then run again")
        
    return success

if __name__ == "__main__":
    main()