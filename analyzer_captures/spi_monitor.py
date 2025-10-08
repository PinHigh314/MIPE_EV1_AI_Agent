#!/usr/bin/env python3
"""
SPI Monitor for MIPE_EV1 - Simple monitoring without emojis
"""

import time
import subprocess

def monitor_spi():
    print("SPI COMMUNICATION MONITOR")
    print("Monitoring MIPE_EV1 SPI communication...")
    print("Press Ctrl+C to stop")
    print("")

    try:
        while True:
            # Check if board is still running
            result = subprocess.run([
                'nrfjprog', '--readregs'
            ], capture_output=True, text=True)
            
            if 'PC' in result.stdout:
                pc_line = [line for line in result.stdout.split('\n') if 'PC' in line]
                if pc_line:
                    print(f"MIPE_EV1 running: {pc_line[0].strip()}")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped")

if __name__ == "__main__":
    monitor_spi()
