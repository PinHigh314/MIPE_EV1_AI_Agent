#!/usr/bin/env python3
"""
Quick GitHub Actions status checker
"""

import requests
import json
from datetime import datetime

def check_github_status():
    """Check latest GitHub Actions runs"""
    
    repo = "PinHigh314/MIPE_EV1_AI_Agent"
    url = f"https://api.github.com/repos/{repo}/actions/runs"
    
    print("🌐 CHECKING GITHUB ACTIONS STATUS...")
    print("=" * 50)
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            runs = data.get('workflow_runs', [])[:10]  # Latest 10 runs
            
            print(f"✅ Connected to GitHub API")
            print(f"📊 Total Runs: {data.get('total_count', 0)}")
            print("")
            print("📋 RECENT WORKFLOW RUNS:")
            print("")
            
            for i, run in enumerate(runs):
                status_icon = {
                    'success': '✅',
                    'failure': '❌', 
                    'cancelled': '⚪',
                    'in_progress': '🔄'
                }.get(run.get('conclusion', run.get('status', 'unknown')), '❓')
                
                created = datetime.fromisoformat(run['created_at'].replace('Z', '+00:00'))
                time_str = created.strftime('%m-%d %H:%M')
                
                commit_msg = run['head_commit']['message'][:50]
                if len(run['head_commit']['message']) > 50:
                    commit_msg += "..."
                
                print(f"{i+1:2d}. {status_icon} {commit_msg}")
                print(f"     🕐 {time_str} | Status: {run.get('conclusion', run.get('status'))}")
                print(f"     🔗 {run['html_url']}")
                print("")
            
        elif response.status_code == 403:
            print("❌ GitHub API rate limit exceeded")
            print("   Try again in a few minutes")
        else:
            print(f"❌ GitHub API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error connecting to GitHub: {e}")

if __name__ == "__main__":
    check_github_status()