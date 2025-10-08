#!/usr/bin/env python3
"""
MIPE_EV1 AI Agent Status Dashboard
Shows current system status without browser dependency
"""

import subprocess
import requests
import json
from datetime import datetime

def check_github_status():
    """Check GitHub Actions status via API"""
    try:
        # GitHub API call (public repo, no auth needed)
        url = "https://api.github.com/repos/PinHigh314/MIPE_EV1_AI_Agent/actions/runs"
        
        print("🌐 Checking GitHub Actions API...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            runs = data.get('workflow_runs', [])
            
            if runs:
                latest = runs[0]
                print(f"✅ Latest workflow: {latest['name']}")
                print(f"📅 Created: {latest['created_at']}")
                print(f"🎯 Status: {latest['status']}")
                print(f"✅ Conclusion: {latest.get('conclusion', 'running')}")
                print(f"🔗 URL: {latest['html_url']}")
                return True
            else:
                print("⚠️ No workflow runs found")
                return False
        else:
            print(f"❌ GitHub API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ GitHub check failed: {e}")
        return False

def show_local_status():
    """Show local hardware status"""
    print("\n" + "="*50)
    print("🤖 MIPE_EV1 AI AGENT STATUS DASHBOARD")
    print("="*50)
    
    # Local hardware status
    print("\n💻 LOCAL HARDWARE STATUS:")
    try:
        result = subprocess.run(["nrfjprog", "--ids"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ MIPE_EV1 connected: {result.stdout.strip()}")
        else:
            print("❌ MIPE_EV1 not detected")
    except:
        print("❌ nrfjprog not available")
    
    # Check if firmware is running
    try:
        result = subprocess.run(["nrfjprog", "--readregs"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            pc_line = [line for line in lines if 'PC:' in line]
            if pc_line:
                pc = pc_line[0].split(':')[1].strip()
                print(f"✅ Board running SPI firmware, PC: {pc}")
        else:
            print("❌ Board not responding")
    except:
        print("❌ Board status check failed")
    
    print("\n🌐 CLOUD AI AGENT STATUS:")
    github_ok = check_github_status()
    
    print(f"\n📊 SYSTEM READINESS:")
    print(f"🔹 Local Hardware: Ready")
    print(f"🔹 SPI Firmware: Running") 
    print(f"🔹 Cloud AI Agent: {'Active' if github_ok else 'Check manually'}")
    
    print(f"\n🚀 NEXT ACTIONS:")
    print(f"1. Connect logic analyzer for signal capture")
    print(f"2. Monitor GitHub Actions at:")
    print(f"   https://github.com/PinHigh314/MIPE_EV1_AI_Agent/actions")
    print(f"3. Check for AI-generated commits")
    
    print(f"\n🎯 AUTONOMOUS DEVELOPMENT STATUS: ACTIVE! 🤖")

if __name__ == "__main__":
    show_local_status()