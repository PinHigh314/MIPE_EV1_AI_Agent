#!/usr/bin/env python3
"""
Simple Log Viewer for MIPE_EV1 Hardware Monitoring
One objective: Show what the firmware is doing
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def show_log_locations():
    """Display all log file locations and their purposes"""
    print("MIPE_EV1 Log File Locations & Access Guide")
    print("=" * 60)
    
    project_dir = Path(r"C:\Development\MIPE_EV1")
    
    locations = [
        {
            "name": "RTT Hardware Logs",
            "path": project_dir / "rtt_logs",
            "description": "Real-time GPIO monitoring and timing validation",
            "files": "rtt_capture_YYYYMMDD_HHMMSS.txt",
            "content": "Timestamped hardware activity logs"
        },
        {
            "name": "Logic Analyzer Captures", 
            "path": project_dir / "analyzer_captures",
            "description": "Signal captures from Logic 2 software",
            "files": "spi_capture_YYYYMMDD_HHMMSS.sr, *.csv",
            "content": "Digital signal captures and decoded protocols"
        },
        {
            "name": "Build System Logs",
            "path": project_dir / "build",
            "description": "Zephyr/NCS build output and configuration",
            "files": "CMakeCache.txt, .config, compile_commands.json",
            "content": "Build configuration and compilation details"
        },
        {
            "name": "GitHub Actions Artifacts",
            "path": "Downloaded from Actions tab",
            "description": "Artifacts uploaded by GitHub Actions",
            "files": "hardware-monitoring-logs.zip, firmware-build-*.zip",
            "content": "Complete test results and build artifacts"
        }
    ]
    
    for loc in locations:
        print(f"\n{loc['name']}:")
        print(f"  Location: {loc['path']}")
        print(f"  Purpose: {loc['description']}")
        print(f"  File Format: {loc['files']}")
        print(f"  Contains: {loc['content']}")
        
        # Check if directory exists and show file count
        if isinstance(loc['path'], Path) and loc['path'].exists():
            files = list(loc['path'].glob("*.*"))
            print(f"  Current Files: {len(files)} files")
            if files:
                latest = max(files, key=lambda f: f.stat().st_mtime)
                print(f"  Latest: {latest.name}")
        else:
            print(f"  Status: Directory not created yet")

def show_rtt_logs():
    """Display RTT log files with analysis"""
    print("\nRTT Hardware Monitoring Logs")
    print("=" * 40)
    
    rtt_dir = Path(r"C:\Development\MIPE_EV1\rtt_logs")
    
    if not rtt_dir.exists():
        print("No RTT logs directory found")
        return
    
    log_files = sorted(rtt_dir.glob("*.txt"), key=lambda f: f.stat().st_mtime, reverse=True)
    
    if not log_files:
        print("No RTT log files found")
        return
    
    print(f"Found {len(log_files)} RTT log files:")
    print(f"{'Filename':<35} {'Size':<8} {'GPIO Cycles':<12} {'Age'}")
    print("-" * 70)
    
    for log_file in log_files[:10]:  # Show latest 10
        size = log_file.stat().st_size
        
        # Quick analysis
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                cycle_count = len([line for line in content.split('\n') if 'Cycle' in line and 'Toggling pins' in line])
        except:
            cycle_count = 0
        
        # File age
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        age = datetime.now() - mtime
        age_str = f"{age.seconds}s ago" if age.days == 0 else f"{age.days}d ago"
        
        print(f"{log_file.name:<35} {size:<8} {cycle_count:<12} {age_str}")

def show_latest_rtt_log():
    """Show content of the latest RTT log"""
    print("\nLatest RTT Log Content")
    print("=" * 30)
    
    rtt_dir = Path(r"C:\Development\MIPE_EV1\rtt_logs")
    
    if not rtt_dir.exists():
        print("No RTT logs directory found")
        return
    
    log_files = sorted(rtt_dir.glob("*.txt"), key=lambda f: f.stat().st_mtime, reverse=True)
    
    if not log_files:
        print("No RTT log files found")
        return
    
    latest_log = log_files[0]
    print(f"File: {latest_log.name}")
    print(f"Size: {latest_log.stat().st_size} bytes")
    print(f"Modified: {datetime.fromtimestamp(latest_log.stat().st_mtime)}")
    print("-" * 50)
    
    try:
        with open(latest_log, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"Error reading log file: {e}")

def show_github_actions_access():
    """Show how to access GitHub Actions logs"""
    print("\nGitHub Actions Log Access")
    print("=" * 30)
    
    print("1. LIVE WORKFLOW LOGS:")
    print("   URL: https://github.com/PinHigh314/MIPE_EV1_AI_Agent/actions")
    print("   - Click on any workflow run")
    print("   - Expand job steps to see real-time logs")
    print("   - View build, flash, RTT, and analyzer outputs")
    
    print("\n2. DOWNLOADABLE ARTIFACTS:")
    print("   - hardware-monitoring-logs.zip")
    print("     * RTT capture files")
    print("     * Logic analyzer data") 
    print("     * Analysis results JSON")
    print("   - firmware-build-<run#>.zip")
    print("     * zephyr.hex firmware")
    print("     * zephyr.map memory layout")
    print("     * build.ninja configuration")
    
    print("\n3. ARTIFACT RETENTION:")
    print("   - Hardware logs: 30 days")
    print("   - Build artifacts: 90 days")
    print("   - Logs in UI: Indefinite")

def main():
    """Main log viewer function"""
    print("MIPE_EV1 Automation Log Viewer")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Show all log locations")
        print("2. Show RTT log summary") 
        print("3. Show latest RTT log content")
        print("4. Show GitHub Actions access guide")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            show_log_locations()
        elif choice == "2":
            show_rtt_logs()
        elif choice == "3":
            show_latest_rtt_log()
        elif choice == "4":
            show_github_actions_access()
        elif choice == "5":
            print("Exiting log viewer...")
            break
        else:
            print("Invalid option. Please select 1-5.")

if __name__ == "__main__":
    main()