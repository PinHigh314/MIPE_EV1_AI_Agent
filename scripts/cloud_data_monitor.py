#!/usr/bin/env python3
"""
Cloud Data Monitor - Shows what data is being sent to the cloud
"""

import subprocess
import os
import time
from datetime import datetime

def show_git_log():
    """Show recent commits that trigger cloud analysis"""
    print("📡 RECENT COMMITS SENT TO CLOUD AI:")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            'git', 'log', '--oneline', '-10'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for i, line in enumerate(lines):
                print(f"{i+1:2d}. {line}")
        else:
            print("❌ Could not read git log")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def show_current_code_status():
    """Show what code is currently being analyzed"""
    print("\n🔍 CURRENT CODE BEING ANALYZED:")
    print("=" * 50)
    
    # Show main.c status
    if os.path.exists('src/main.c'):
        with open('src/main.c', 'r') as f:
            lines = f.readlines()
        
        print(f"📄 src/main.c: {len(lines)} lines")
        
        # Look for key SPI functions
        spi_functions = []
        for i, line in enumerate(lines):
            if 'lsm6dso32' in line.lower() or 'spi_' in line.lower():
                spi_functions.append(f"  Line {i+1}: {line.strip()}")
        
        if spi_functions:
            print("🎯 SPI-related code:")
            for func in spi_functions[:5]:  # Show first 5
                print(func)
            if len(spi_functions) > 5:
                print(f"  ... and {len(spi_functions) - 5} more lines")
    
    # Show device tree status
    dts_file = 'boards/nordic/mipe_ev1/mipe_ev1_nrf54l15_cpuapp.dts'
    if os.path.exists(dts_file):
        with open(dts_file, 'r') as f:
            content = f.read()
        
        print(f"\n📄 Device Tree: {len(content.split())} words")
        if 'spi00' in content:
            print("  ✅ SPI configuration found")
        if 'lsm6dso32' in content:
            print("  ✅ LSM6DSO32 sensor defined")

def show_capture_status():
    """Show analyzer capture status"""
    print("\n📊 ANALYZER CAPTURE STATUS:")
    print("=" * 50)
    
    capture_dir = "analyzer_captures"
    
    if os.path.exists(capture_dir):
        files = [f for f in os.listdir(capture_dir) if f.endswith('.csv')]
        
        if files:
            print(f"📁 {len(files)} capture files found:")
            
            # Sort by modification time
            files_with_time = []
            for f in files:
                filepath = os.path.join(capture_dir, f)
                mod_time = os.path.getmtime(filepath)
                files_with_time.append((f, mod_time))
            
            files_with_time.sort(key=lambda x: x[1], reverse=True)
            
            for i, (f, mod_time) in enumerate(files_with_time[:3]):
                time_str = datetime.fromtimestamp(mod_time).strftime('%H:%M:%S')
                filepath = os.path.join(capture_dir, f)
                size = os.path.getsize(filepath)
                print(f"  {i+1}. {f} ({size:,} bytes, {time_str})")
                
                # Quick peek at the file
                try:
                    with open(filepath, 'r') as file:
                        first_line = file.readline().strip()
                        print(f"     Header: {first_line[:60]}...")
                except:
                    pass
        else:
            print("📁 No capture files found")
            print("   Export Saleae captures as CSV to analyzer_captures/")
    else:
        print("📁 analyzer_captures/ directory not found")

def show_cloud_links():
    """Show direct links to cloud resources"""
    print("\n🌐 CLOUD MONITORING LINKS:")
    print("=" * 50)
    print("🔗 GitHub Actions: https://github.com/PinHigh314/MIPE_EV1_AI_Agent/actions")
    print("🔗 Repository: https://github.com/PinHigh314/MIPE_EV1_AI_Agent")
    print("🔗 Latest Commits: https://github.com/PinHigh314/MIPE_EV1_AI_Agent/commits/main")

def main():
    """Main monitoring function"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("☁️ CLOUD DATA MONITOR")
    print("What data is being sent to the AI agent")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    show_git_log()
    show_current_code_status()
    show_capture_status()
    show_cloud_links()
    
    print("\n" + "=" * 60)
    print("💡 Every git push triggers cloud AI analysis!")
    print("💡 The AI analyzes your code and generates reports")
    print("💡 Check GitHub Actions to see AI agent activity")

if __name__ == "__main__":
    main()