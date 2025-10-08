#!/usr/bin/env python3
"""
ANALYZER DATA VIEWER
View captured SPI data from Saleae Logic Analyzer
"""

import os
import glob
import csv
from datetime import datetime

def view_latest_capture():
    """Display the latest analyzer capture data"""
    
    capture_dir = "analyzer_captures"
    
    if not os.path.exists(capture_dir):
        print("❌ No analyzer_captures directory found")
        print("   Create captures first using the Saleae Logic software")
        return
    
    # Find all CSV files
    csv_files = glob.glob(f"{capture_dir}/*.csv")
    
    if not csv_files:
        print("❌ No capture files found in analyzer_captures/")
        print("   Export your Saleae captures as CSV files to this directory")
        return
    
    # Get the most recent file
    latest_file = max(csv_files, key=os.path.getmtime)
    mod_time = datetime.fromtimestamp(os.path.getmtime(latest_file))
    file_size = os.path.getsize(latest_file)
    
    print("🔍 LATEST SPI CAPTURE ANALYSIS")
    print("=" * 50)
    print(f"📄 File: {os.path.basename(latest_file)}")
    print(f"📏 Size: {file_size:,} bytes")
    print(f"🕐 Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    try:
        with open(latest_file, 'r') as f:
            # Read first few lines to understand format
            lines = f.readlines()
            
        print(f"📝 Total Lines: {len(lines):,}")
        print("")
        
        # Show header
        if lines:
            print("📋 CAPTURE HEADER:")
            for i, line in enumerate(lines[:5]):
                print(f"  {i+1}: {line.strip()}")
            
            if len(lines) > 10:
                print("  ...")
                print(f"  {len(lines)}: {lines[-1].strip()}")
        
        print("")
        print("🎯 SPI SIGNAL ANALYSIS:")
        
        # Try to parse as CSV and analyze SPI signals
        try:
            with open(latest_file, 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                
                print(f"📊 Channels: {header}")
                
                # Count data rows
                data_rows = list(reader)
                print(f"📈 Data Points: {len(data_rows):,}")
                
                if len(data_rows) > 0:
                    print("\n🔍 SAMPLE DATA (first 10 rows):")
                    for i, row in enumerate(data_rows[:10]):
                        print(f"  {i+1}: {row}")
                    
                    if len(data_rows) > 10:
                        print("  ...")
                
        except Exception as e:
            print(f"⚠️ CSV parsing error: {e}")
            print("   Raw file content shown above")
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")

def list_all_captures():
    """List all available capture files"""
    
    capture_dir = "analyzer_captures"
    
    if not os.path.exists(capture_dir):
        print("❌ No analyzer_captures directory found")
        return
    
    csv_files = glob.glob(f"{capture_dir}/*.csv")
    
    if not csv_files:
        print("❌ No capture files found")
        return
    
    print("📁 ALL CAPTURE FILES:")
    print("=" * 50)
    
    # Sort by modification time (newest first)
    csv_files.sort(key=os.path.getmtime, reverse=True)
    
    for i, file in enumerate(csv_files):
        mod_time = datetime.fromtimestamp(os.path.getmtime(file))
        file_size = os.path.getsize(file)
        
        print(f"{i+1}. {os.path.basename(file)}")
        print(f"   📏 Size: {file_size:,} bytes")
        print(f"   🕐 Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("")

def main():
    print("🔍 SALEAE ANALYZER DATA VIEWER")
    print("=" * 40)
    print("")
    print("1. View latest capture")
    print("2. List all captures")
    print("")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        view_latest_capture()
    elif choice == "2":
        list_all_captures()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()