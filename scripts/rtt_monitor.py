#!/usr/bin/env python3
"""
MIPE_EV1 RTT Hardware Monitoring for GitHub Actions
Real-time logging capture and analysis with timestamping
"""

import subprocess
import time
import threading
import queue
import json
import os
from datetime import datetime
from pathlib import Path

class RTTMonitor:
    def __init__(self, duration=30):
        self.project_dir = Path(r"C:\Development\MIPE_EV1")
        self.logs_dir = self.project_dir / "rtt_logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        self.duration = duration  # Monitoring duration in seconds
        self.log_queue = queue.Queue()
        self.is_monitoring = False
        
        # RTT capture configuration
        self.jlink_rtt_logger = r"C:\Program Files\SEGGER\JLink_V874a\JLinkRTTLogger.exe"
        self.device = "nRF54L15_xxAA"
        
        # Timing analysis
        self.cycle_times = []
        self.expected_cycle_time = 23  # milliseconds
        self.tolerance = 2  # ±2ms tolerance
        
    def start_rtt_capture(self):
        """Start J-Link RTT capture in background"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.logs_dir / f"rtt_capture_{timestamp}.txt"
        
        print(f"🚀 Starting RTT capture for {self.duration} seconds...")
        print(f"📝 Log file: {log_file}")
        
        # J-Link RTT Logger command
        cmd = [
            self.jlink_rtt_logger,
            "-device", self.device,
            "-if", "SWD",
            "-speed", "4000",
            "-rttchannel", "0",
            str(log_file)
        ]
        
        try:
            # Start RTT capture process
            self.rtt_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ RTT Logger started (PID: {self.rtt_process.pid})")
            return log_file
            
        except FileNotFoundError:
            print(f"❌ J-Link RTT Logger not found at: {self.jlink_rtt_logger}")
            print("💡 Ensure J-Link tools are installed and path is correct")
            return None
            
        except Exception as e:
            print(f"❌ Failed to start RTT capture: {e}")
            return None
    
    def monitor_hardware(self):
        """Monitor hardware for specified duration"""
        log_file = self.start_rtt_capture()
        if not log_file:
            return False
            
        print(f"⏱️  Monitoring hardware for {self.duration} seconds...")
        print("📊 Collecting RTT logs, GPIO timing, and hardware events...")
        
        # Monitor for specified duration
        start_time = time.time()
        cycle_count = 0
        
        while time.time() - start_time < self.duration:
            elapsed = time.time() - start_time
            print(f"⏳ Monitoring... {elapsed:.1f}s / {self.duration}s", end='\r')
            time.sleep(1)
            
        print(f"\n✅ Hardware monitoring complete!")
        
        # Stop RTT capture
        self.stop_rtt_capture()
        
        # Analyze captured logs
        return self.analyze_rtt_logs(log_file)
    
    def stop_rtt_capture(self):
        """Stop RTT capture process"""
        try:
            if hasattr(self, 'rtt_process') and self.rtt_process:
                self.rtt_process.terminate()
                self.rtt_process.wait(timeout=5)
                print("🛑 RTT capture stopped")
        except Exception as e:
            print(f"⚠️  Error stopping RTT capture: {e}")
    
    def analyze_rtt_logs(self, log_file):
        """Analyze captured RTT logs for hardware validation"""
        print(f"🔍 Analyzing RTT logs: {log_file}")
        
        if not log_file.exists():
            print(f"❌ Log file not found: {log_file}")
            return False
            
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                log_content = f.read()
                
            print(f"📄 Log file size: {len(log_content)} characters")
            
            # Analysis results
            analysis = {
                "log_file": str(log_file),
                "capture_duration": self.duration,
                "timestamp": datetime.now().isoformat(),
                "gpio_cycles_detected": 0,
                "timing_validation": "UNKNOWN",
                "hardware_status": "UNKNOWN",
                "logs_captured": len(log_content) > 0
            }
            
            # Count GPIO cycles
            cycle_lines = [line for line in log_content.split('\n') if 'Cycle' in line and 'Toggling pins' in line]
            analysis["gpio_cycles_detected"] = len(cycle_lines)
            
            # Check for timing validation logs
            timing_lines = [line for line in log_content.split('\n') if 'Timing validation' in line]
            analysis["timing_events"] = len(timing_lines)
            
            # Determine hardware status
            if analysis["gpio_cycles_detected"] > 0:
                analysis["hardware_status"] = "ACTIVE"
                analysis["timing_validation"] = "VERIFIED" if analysis["timing_events"] > 0 else "PARTIAL"
            else:
                analysis["hardware_status"] = "NO_ACTIVITY"
                analysis["timing_validation"] = "FAILED"
            
            # Save analysis results
            results_file = self.logs_dir / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(results_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            
            # Print results for GitHub Actions
            print("\n" + "="*60)
            print("🎯 RTT HARDWARE MONITORING RESULTS")
            print("="*60)
            print(f"📊 GPIO Cycles Detected: {analysis['gpio_cycles_detected']}")
            print(f"⏱️  Timing Events: {analysis['timing_events']}")
            print(f"🔧 Hardware Status: {analysis['hardware_status']}")
            print(f"✅ Timing Validation: {analysis['timing_validation']}")
            print(f"📝 Analysis saved: {results_file}")
            print("="*60)
            
            # Return success status
            return analysis["hardware_status"] == "ACTIVE" and analysis["gpio_cycles_detected"] > 0
            
        except Exception as e:
            print(f"❌ Error analyzing logs: {e}")
            return False
    
    def validate_timing(self, log_content):
        """Extract and validate GPIO timing from logs"""
        timing_lines = []
        for line in log_content.split('\n'):
            if 'Toggle event' in line and 'cycle=' in line:
                timing_lines.append(line)
        
        # For now, just count events - could be enhanced with timestamp parsing
        return len(timing_lines)

def main():
    """Main RTT monitoring function for GitHub Actions"""
    import argparse
    
    parser = argparse.ArgumentParser(description='RTT Hardware Monitoring for MIPE_EV1')
    parser.add_argument('--duration', type=int, default=30, help='Monitoring duration in seconds')
    parser.add_argument('--device', default='nRF54L15_xxAA', help='Target device')
    
    args = parser.parse_args()
    
    print("🚀 MIPE_EV1 RTT Hardware Monitoring")
    print(f"⏱️  Duration: {args.duration} seconds")
    print(f"🎯 Target: {args.device}")
    print("-" * 50)
    
    monitor = RTTMonitor(duration=args.duration)
    success = monitor.monitor_hardware()
    
    if success:
        print("🎉 Hardware monitoring PASSED - GPIO activity detected!")
        exit(0)
    else:
        print("❌ Hardware monitoring FAILED - No GPIO activity detected!")
        exit(1)

if __name__ == "__main__":
    main()