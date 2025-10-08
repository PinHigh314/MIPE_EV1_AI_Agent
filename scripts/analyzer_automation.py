#!/usr/bin/env python3
"""
MIPE_EV1 SPI Analyzer Automation Script
Captures and analyzes SPI signals for automated development
"""

import subprocess
import csv
import json
import os
from pathlib import Path

# Configuration
SIGROK_CLI = r"C:\Program Files\sigrok\sigrok-cli\sigrok-cli.exe"
SAMPLE_RATE = "25M"
CAPTURE_DURATION = "2s"  # 2 seconds of capture

class AnalyzerAutomation:
    def __init__(self):
        self.project_dir = Path(r"C:\Development\MIPE_EV1")
        self.captures_dir = self.project_dir / "analyzer_captures"
        self.captures_dir.mkdir(exist_ok=True)
        
    def scan_devices(self):
        """Scan for available logic analyzers"""
        print("🔍 Scanning for logic analyzers...")
        try:
            result = subprocess.run([SIGROK_CLI, "--scan"],
                                    capture_output=True, text=True, check=True)
            print(result.stdout)
            # Look for fx2lafw device (your Cypress FX2 analyzer)
            has_fx2lafw = "fx2lafw" in result.stdout
            has_saleae = "Saleae Logic" in result.stdout
            return has_fx2lafw or has_saleae
        except subprocess.CalledProcessError as e:
            print(f"❌ Error scanning devices: {e}")
            return False
    
    def capture_spi_signals(self, channel_map=None):
        """
        Capture SPI signals using the logic analyzer
        Default MIPE_EV1 SPI mapping:
        - CH0: SPI_SCLK  (Clock)
        - CH1: SPI_MOSI  (Master Out)
        - CH2: SPI_MISO  (Slave In)
        - CH3: SPI_CS    (Chip Select)
        """
        if channel_map is None:
            channel_map = {"clk": 0, "mosi": 1, "miso": 2, "cs": 3}
        
        print(f"📡 Capturing SPI signals for {CAPTURE_DURATION}...")
        
        capture_file = self.captures_dir / f"spi_capture_{self._timestamp()}.sr"
        
        # Basic signal capture with specific device selection
        cmd = [
            SIGROK_CLI,
            "-d", "fx2lafw:conn=3.22",  # Specify your exact device
            "-c", f"samplerate={SAMPLE_RATE}",
            "-t", f"time={CAPTURE_DURATION}",
            "-o", str(capture_file)
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Capture saved to: {capture_file}")
            return capture_file
        except subprocess.CalledProcessError as e:
            print(f"❌ Capture failed: {e}")
            return None
    
    def decode_spi_capture(self, capture_file, channel_map=None):
        """Decode SPI protocol from captured signals"""
        if channel_map is None:
            channel_map = {"clk": 0, "mosi": 1, "miso": 2, "cs": 3}
        
        print("🔍 Decoding SPI protocol...")
        
        csv_file = capture_file.with_suffix('.csv')
        
        # Protocol decode command
        protocol_def = f"spi:clk={channel_map['clk']}:mosi={channel_map['mosi']}:miso={channel_map['miso']}:cs={channel_map['cs']}"
        
        cmd = [
            SIGROK_CLI,
            "-i", str(capture_file),
            "-P", protocol_def,
            "-A", "spi",  # Just use 'spi' instead of specific annotations
            "-o", str(csv_file)
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ SPI decode saved to: {csv_file}")
            return self._parse_spi_csv(csv_file)
        except subprocess.CalledProcessError as e:
            print(f"❌ SPI decode failed: {e}")
            return None
    
    def _parse_spi_csv(self, csv_file):
        """Parse decoded SPI CSV file"""
        spi_data = []
        try:
            with open(csv_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3:  # Time, Decoder, Data
                        spi_data.append({
                            'time': row[0],
                            'type': row[1], 
                            'data': row[2]
                        })
            return spi_data
        except Exception as e:
            print(f"❌ Error parsing CSV: {e}")
            return []
    
    def validate_lsm6_communication(self, spi_data):
        """
        Validate LSM6DSO32 sensor communication
        Look for WHO_AM_I register response (0x6C)
        """
        print("🔍 Validating LSM6DSO32 communication...")
        
        validation_results = {
            'spi_activity': len(spi_data) > 0,
            'who_am_i_found': False,
            'valid_responses': 0,
            'raw_data': spi_data
        }
        
        for entry in spi_data:
            if 'miso' in entry['type'].lower():
                # Look for WHO_AM_I response (0x6C = 108 decimal)
                data = entry['data'].replace('0x', '').replace(' ', '')
                if '6C' in data.upper() or '108' in data:
                    validation_results['who_am_i_found'] = True
                validation_results['valid_responses'] += 1
        
        return validation_results
    
    def _timestamp(self):
        """Generate timestamp for file naming"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def run_automated_test(self):
        """Run complete automated SPI test sequence"""
        print("🚀 Starting MIPE_EV1 SPI Automation Test")
        print("=" * 50)
        
        # Step 1: Verify analyzer connection
        if not self.scan_devices():
            print("❌ No supported analyzer found!")
            return False
        
        # Step 2: Capture SPI signals
        capture_file = self.capture_spi_signals()
        if not capture_file:
            print("❌ Signal capture failed!")
            return False
        
        # Step 3: Decode SPI protocol
        spi_data = self.decode_spi_capture(capture_file)
        if spi_data is None:
            print("❌ SPI decode failed!")
            return False
        
        # Step 4: Validate communication
        results = self.validate_lsm6_communication(spi_data)
        
        # Step 5: Report results
        print("\n📊 Test Results:")
        print(f"   SPI Activity Detected: {'✅' if results['spi_activity'] else '❌'}")
        print(f"   LSM6 WHO_AM_I Found: {'✅' if results['who_am_i_found'] else '❌'}")
        print(f"   Valid Responses: {results['valid_responses']}")
        
        # Save results for CI/CD
        results_file = self.captures_dir / f"test_results_{self._timestamp()}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📄 Results saved to: {results_file}")
        
        return results['spi_activity'] and results['who_am_i_found']

if __name__ == "__main__":
    automation = AnalyzerAutomation()
    success = automation.run_automated_test()
    
    if success:
        print("\n🎉 Automated SPI test PASSED!")
        exit(0)
    else:
        print("\n❌ Automated SPI test FAILED!")
        exit(1)