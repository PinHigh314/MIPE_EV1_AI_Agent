#!/usr/bin/env python3
"""
Simple Log Viewer for MIPE_EV1
One objective: Show what the firmware is doing
"""

from pathlib import Path
from datetime import datetime


def show_firmware_logs():
    """Show the latest firmware output"""
    
    print("MIPE_EV1 Firmware Output")
    print("=" * 40)
    
    # Find RTT logs
    rtt_dir = Path("../rtt_logs")
    if not rtt_dir.exists():
        rtt_dir = Path("rtt_logs")
    
    if not rtt_dir.exists():
        print("No logs found. Run monitoring first:")
        print("  python scripts/windows_rtt_monitor.py")
        return
    
    # Get latest log
    log_files = list(rtt_dir.glob("*.txt"))
    if not log_files:
        print("No log files found")
        return
    
    latest = max(log_files, key=lambda f: f.stat().st_mtime)
    
    print(f"Latest: {latest.name}")
    print(f"Time: {datetime.fromtimestamp(latest.stat().st_mtime)}")
    print("-" * 40)
    
    # Show content
    try:
        with open(latest, 'r') as f:
            content = f.read()
        
        if content.strip():
            print("FIRMWARE OUTPUT:")
            print(content)
        else:
            print("No output captured")
            
    except Exception as e:
        print(f"Read error: {e}")
    
    # Simple stats
    lines = content.split('\n') if content else []
    cycles = len([line for line in lines if 'Cycle' in line])
    
    print("-" * 40)
    print(f"GPIO Cycles: {cycles}")
    print(f"Status: {'ACTIVE' if cycles > 0 else 'INACTIVE'}")


if __name__ == "__main__":
    show_firmware_logs()