#!/usr/bin/env python3
"""
REAL-TIME AUTONOMOUS DEVELOPMENT MONITOR
Shows analyzer data, cloud AI activity, and hardware status
"""

import subprocess
import time
import os
import json
import requests
from datetime import datetime
import glob

class AutonomousDevMonitor:
    def __init__(self):
        self.github_repo = "PinHigh314/MIPE_EV1_AI_Agent"
        self.capture_dir = "analyzer_captures"
        
    def check_hardware_status(self):
        """Check MIPE_EV1 hardware status"""
        try:
            result = subprocess.run(['nrfjprog', '--ids'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0 and result.stdout.strip():
                device_id = result.stdout.strip()
                
                # Get current PC register
                pc_result = subprocess.run(['nrfjprog', '--readregs'], 
                                         capture_output=True, text=True, timeout=5)
                
                pc_value = "Unknown"
                if 'PC' in pc_result.stdout:
                    pc_lines = [line for line in pc_result.stdout.split('\n') if 'PC' in line]
                    if pc_lines:
                        pc_value = pc_lines[0].strip()
                
                return {
                    'status': 'connected',
                    'device_id': device_id,
                    'pc_register': pc_value,
                    'firmware_running': True
                }
            else:
                return {'status': 'disconnected'}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def check_analyzer_status(self):
        """Check logic analyzer and look for capture files"""
        
        # Check if Saleae is connected
        analyzer_connected = False
        try:
            result = subprocess.run([
                'powershell', 
                'Get-PnpDevice | Where-Object {$_.FriendlyName -like "*Saleae*"} | Select-Object FriendlyName'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and 'Saleae' in result.stdout:
                analyzer_connected = True
        except:
            pass
        
        # Look for capture files
        capture_files = []
        if os.path.exists(self.capture_dir):
            csv_files = glob.glob(f"{self.capture_dir}/*.csv")
            capture_files = sorted(csv_files, key=os.path.getmtime, reverse=True)
        
        return {
            'analyzer_connected': analyzer_connected,
            'capture_files': capture_files[:5],  # Show latest 5 files
            'total_captures': len(capture_files)
        }
    
    def check_github_actions(self):
        """Check GitHub Actions workflow runs"""
        try:
            # Get latest workflow runs
            url = f"https://api.github.com/repos/{self.github_repo}/actions/runs"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                runs = data.get('workflow_runs', [])[:5]  # Latest 5 runs
                
                latest_runs = []
                for run in runs:
                    latest_runs.append({
                        'id': run['id'],
                        'status': run['status'],
                        'conclusion': run['conclusion'],
                        'created_at': run['created_at'],
                        'head_commit_message': run['head_commit']['message'][:60],
                        'html_url': run['html_url']
                    })
                
                return {
                    'status': 'success',
                    'runs': latest_runs,
                    'total_runs': data.get('total_count', 0)
                }
            else:
                return {'status': 'api_error', 'code': response.status_code}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def analyze_latest_capture(self):
        """Analyze the most recent capture file"""
        if not os.path.exists(self.capture_dir):
            return {'status': 'no_captures'}
        
        csv_files = glob.glob(f"{self.capture_dir}/*.csv")
        if not csv_files:
            return {'status': 'no_files'}
        
        latest_file = max(csv_files, key=os.path.getmtime)
        
        try:
            # Basic analysis of the CSV file
            with open(latest_file, 'r') as f:
                lines = f.readlines()
            
            return {
                'status': 'analyzed',
                'file': latest_file,
                'size': os.path.getsize(latest_file),
                'lines': len(lines),
                'modified': datetime.fromtimestamp(os.path.getmtime(latest_file))
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def display_status(self):
        """Display comprehensive status dashboard"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print("🤖 AUTONOMOUS EMBEDDED DEVELOPMENT - REAL-TIME MONITOR")
        print("=" * 80)
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        
        # Hardware Status
        print("💻 HARDWARE STATUS:")
        hw_status = self.check_hardware_status()
        if hw_status['status'] == 'connected':
            print(f"  ✅ MIPE_EV1 Connected: {hw_status['device_id']}")
            print(f"  ✅ Firmware Running: {hw_status['pc_register']}")
        else:
            print(f"  ❌ Hardware: {hw_status['status']}")
        print("")
        
        # Analyzer Status
        print("🔍 LOGIC ANALYZER STATUS:")
        analyzer_status = self.check_analyzer_status()
        if analyzer_status['analyzer_connected']:
            print("  ✅ Saleae Logic Analyzer Connected")
        else:
            print("  ❌ Logic Analyzer Not Detected")
        
        print(f"  📁 Total Captures: {analyzer_status['total_captures']}")
        if analyzer_status['capture_files']:
            print("  📋 Recent Captures:")
            for file in analyzer_status['capture_files']:
                mod_time = datetime.fromtimestamp(os.path.getmtime(file))
                print(f"    - {os.path.basename(file)} ({mod_time.strftime('%H:%M:%S')})")
        print("")
        
        # Latest Capture Analysis
        print("📊 LATEST CAPTURE ANALYSIS:")
        capture_analysis = self.analyze_latest_capture()
        if capture_analysis['status'] == 'analyzed':
            print(f"  📄 File: {os.path.basename(capture_analysis['file'])}")
            print(f"  📏 Size: {capture_analysis['size']} bytes")
            print(f"  📝 Lines: {capture_analysis['lines']}")
            print(f"  🕐 Modified: {capture_analysis['modified'].strftime('%H:%M:%S')}")
        else:
            print(f"  ⚠️ Status: {capture_analysis['status']}")
        print("")
        
        # GitHub Actions Status
        print("🌐 CLOUD AI AGENT STATUS:")
        gh_status = self.check_github_actions()
        if gh_status['status'] == 'success':
            print(f"  ✅ GitHub Actions API Connected")
            print(f"  📊 Total Workflow Runs: {gh_status['total_runs']}")
            print("  📋 Recent Runs:")
            for run in gh_status['runs']:
                status_icon = "✅" if run['conclusion'] == 'success' else "❌" if run['conclusion'] == 'failure' else "🔄"
                time_str = run['created_at'][:19].replace('T', ' ')
                print(f"    {status_icon} {run['head_commit_message']} ({time_str})")
        else:
            print(f"  ❌ GitHub API: {gh_status['status']}")
        print("")
        
        # Direct Links
        print("🔗 DIRECT MONITORING LINKS:")
        print(f"  🌐 GitHub Actions: https://github.com/{self.github_repo}/actions")
        print(f"  📁 Local Captures: {os.path.abspath(self.capture_dir)}")
        print("")
        
        print("Press Ctrl+C to stop monitoring...")
    
    def run_monitor(self):
        """Run continuous monitoring"""
        print("🚀 Starting Autonomous Development Monitor...")
        try:
            while True:
                self.display_status()
                time.sleep(5)  # Update every 5 seconds
        except KeyboardInterrupt:
            print("\n🛑 Monitor stopped by user")

if __name__ == "__main__":
    monitor = AutonomousDevMonitor()
    monitor.run_monitor()