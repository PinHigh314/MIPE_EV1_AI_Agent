#!/usr/bin/env python3
"""
AI Code Generator for MIPE_EV1 SPI Development
Analyzes hardware test results and generates corrective code automatically
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
import re

class AICodeGenerator:
    def __init__(self):
        self.project_root = Path("C:/Development/MIPE_EV1")
        self.captures_dir = self.project_root / "analyzer_captures"
        self.src_dir = self.project_root / "src"
        
        # AI Knowledge Base for SPI Development
        self.spi_fixes = {
            "no_clock": self._generate_clock_fix,
            "no_cs": self._generate_cs_fix,
            "no_data": self._generate_data_fix,
            "wrong_polarity": self._generate_polarity_fix,
            "timing_issues": self._generate_timing_fix,
            "lsm6_not_responding": self._generate_lsm6_init_fix
        }
        
    def analyze_test_results(self):
        """Analyze latest test results and determine what needs fixing"""
        print("🤖 AI analyzing test results...")
        
        # Find latest test results
        result_files = list(self.captures_dir.glob("test_results_*.json"))
        if not result_files:
            return {"error": "No test results found"}
            
        latest_result = max(result_files, key=lambda x: x.stat().st_mtime)
        
        with open(latest_result, 'r') as f:
            results = json.load(f)
            
        # AI Analysis Logic
        analysis = {
            "iteration": self._get_iteration_count() + 1,
            "timestamp": datetime.now().isoformat(),
            "issues_detected": [],
            "success": results.get('spi_activity', False) and results.get('who_am_i_found', False),
            "raw_results": results
        }
        
        # Detect specific issues
        if not results.get('spi_activity', False):
            analysis["issues_detected"].append("no_spi_activity")
            
        if results.get('spi_activity', False) and not results.get('who_am_i_found', False):
            analysis["issues_detected"].append("lsm6_not_responding")
            
        if results.get('valid_responses', 0) == 0:
            analysis["issues_detected"].append("no_valid_responses")
            
        # Save analysis
        analysis_file = self.captures_dir / f"ai_analysis_{self._timestamp()}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
            
        print(f"📊 Analysis complete. Issues: {analysis['issues_detected']}")
        return analysis
        
    def generate_code_fix(self, analysis):
        """Generate code fixes based on analysis"""
        if analysis.get("success", False):
            print("🎉 No fixes needed - SPI communication successful!")
            return True
            
        print("🔧 AI generating code fixes...")
        
        for issue in analysis.get("issues_detected", []):
            if issue in self.spi_fixes:
                print(f"   Fixing: {issue}")
                self.spi_fixes[issue](analysis)
            else:
                print(f"   Unknown issue: {issue}")
                
        # Update configuration if needed
        self._update_configurations(analysis)
        
        print("✅ AI code generation complete")
        return False  # More iterations needed
        
    def _generate_clock_fix(self, analysis):
        """Generate SPI clock configuration"""
        # This would modify device tree and main.c to add SPI clock
        print("   🔧 Generating SPI clock configuration...")
        # Implementation would go here
        
    def _generate_cs_fix(self, analysis):
        """Generate chip select fixes"""
        print("   🔧 Generating chip select fixes...")
        # Implementation would go here
        
    def _generate_data_fix(self, analysis):
        """Generate data transmission fixes"""
        print("   🔧 Generating data transmission fixes...")
        # Implementation would go here
        
    def _generate_polarity_fix(self, analysis):
        """Fix SPI polarity/phase issues"""
        print("   🔧 Fixing SPI polarity/phase...")
        # Implementation would go here
        
    def _generate_timing_fix(self, analysis):
        """Fix SPI timing issues"""
        print("   🔧 Adjusting SPI timing...")
        # Implementation would go here
        
    def _generate_lsm6_init_fix(self, analysis):
        """Generate LSM6DSO32 initialization sequence"""
        print("   🔧 Generating LSM6DSO32 init sequence...")
        
        # Generate basic SPI + LSM6 test code
        spi_test_code = '''/**
 * MIPE_EV1 - SPI + LSM6DSO32 Test
 * AI Generated Code - Iteration {iteration}
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/spi.h>

/* LSM6DSO32 Registers */
#define LSM6_WHO_AM_I_REG    0x0F
#define LSM6_WHO_AM_I_VALUE  0x6C

/* SPI Configuration */
static const struct device *spi_dev = DEVICE_DT_GET(DT_NODELABEL(spi0));

static struct spi_config spi_cfg = {{
    .frequency = 1000000,  /* 1MHz */
    .operation = SPI_WORD_SET(8) | SPI_TRANSFER_MSB,
    .slave = 0,
    .cs = NULL,
}};

/* GPIO for manual CS control */
static const struct gpio_dt_spec cs_pin = GPIO_DT_SPEC_GET(DT_ALIAS(spi_cs), gpios);

int lsm6_read_who_am_i(void)
{{
    uint8_t tx_buf[2] = {{LSM6_WHO_AM_I_REG | 0x80, 0x00}};  /* Read bit set */
    uint8_t rx_buf[2] = {{0}};
    
    struct spi_buf tx_spi_buf = {{.buf = tx_buf, .len = 2}};
    struct spi_buf rx_spi_buf = {{.buf = rx_buf, .len = 2}};
    
    struct spi_buf_set tx_set = {{.buffers = &tx_spi_buf, .count = 1}};
    struct spi_buf_set rx_set = {{.buffers = &rx_spi_buf, .count = 1}};
    
    /* Manual CS control */
    gpio_pin_set_dt(&cs_pin, 0);  /* CS active low */
    
    int ret = spi_transceive(spi_dev, &spi_cfg, &tx_set, &rx_set);
    
    gpio_pin_set_dt(&cs_pin, 1);  /* CS inactive */
    
    if (ret == 0) {{
        return rx_buf[1];  /* WHO_AM_I value */
    }}
    
    return -1;
}}

int main(void)
{{
    /* Configure CS pin */
    gpio_pin_configure_dt(&cs_pin, GPIO_OUTPUT_HIGH);
    
    /* Test SPI communication */
    while (1) {{
        int who_am_i = lsm6_read_who_am_i();
        
        if (who_am_i == LSM6_WHO_AM_I_VALUE) {{
            /* Success - toggle LED */
            // LED indication code here
        }}
        
        k_msleep(1000);  /* Test every second */
    }}
    
    return 0;
}}'''.format(iteration=analysis.get('iteration', 1))

        # Write generated code
        main_c_path = self.src_dir / "main.c"
        with open(main_c_path, 'w') as f:
            f.write(spi_test_code)
            
        print(f"   ✅ Generated SPI test code: {main_c_path}")
        
    def _update_configurations(self, analysis):
        """Update configuration files based on analysis"""
        print("   🔧 Updating configurations...")
        
        # Update prj.conf to enable SPI
        prj_conf = self.project_root / "prj.conf"
        if prj_conf.exists():
            with open(prj_conf, 'r') as f:
                content = f.read()
                
            if "CONFIG_SPI=y" not in content:
                content += "\n# AI Added: Enable SPI\nCONFIG_SPI=y\n"
                
                with open(prj_conf, 'w') as f:
                    f.write(content)
                    
                print("   ✅ Added SPI config to prj.conf")
        
    def _get_iteration_count(self):
        """Get current iteration number"""
        analysis_files = list(self.captures_dir.glob("ai_analysis_*.json"))
        return len(analysis_files)
        
    def _timestamp(self):
        """Generate timestamp for file naming"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

def main():
    parser = argparse.ArgumentParser(description="AI Code Generator for SPI Development")
    parser.add_argument("--analyze-results", action="store_true", 
                       help="Analyze test results")
    parser.add_argument("--generate-fix", action="store_true",
                       help="Generate code fixes")
    
    args = parser.parse_args()
    
    ai = AICodeGenerator()
    
    if args.analyze_results:
        analysis = ai.analyze_test_results()
        
        # Output for GitHub Actions
        success = analysis.get("success", False)
        print(f"::set-output name=success::{str(success).lower()}")
        print(f"::set-output name=iteration_description::AI Iteration {analysis.get('iteration', 1)}: {', '.join(analysis.get('issues_detected', ['analysis']))}")
        
        if not success:
            sys.exit(1)  # Trigger next iteration
            
    elif args.generate_fix:
        # Load latest analysis
        analysis_files = list(ai.captures_dir.glob("ai_analysis_*.json"))
        if analysis_files:
            latest_analysis = max(analysis_files, key=lambda x: x.stat().st_mtime)
            with open(latest_analysis, 'r') as f:
                analysis = json.load(f)
                
            ai.generate_code_fix(analysis)
        else:
            print("❌ No analysis found to generate fixes from")
            sys.exit(1)
    else:
        print("Please specify --analyze-results or --generate-fix")
        sys.exit(1)

if __name__ == "__main__":
    main()