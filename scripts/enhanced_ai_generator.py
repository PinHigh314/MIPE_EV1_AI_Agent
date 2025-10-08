#!/usr/bin/env python3
"""
Enhanced AI Code Generator for Autonomous SPI Development
Provides specific code generation and modification capabilities
"""

import os
import re
import json
import subprocess
from datetime import datetime
from pathlib import Path

class SpiCodeGenerator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.iteration_count = 0
        self.log_file = self.project_root / "ai_development.log"
        
    def log(self, message):
        """Log AI decision process"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"AI: {message}")
    
    def analyze_capture_results(self, capture_file):
        """Analyze logic analyzer capture for SPI issues"""
        self.log(f"Analyzing capture file: {capture_file}")
        
        if not os.path.exists(capture_file):
            return {"error": "Capture file not found", "fix_needed": True}
        
        # Read capture results (assuming CSV format)
        issues = []
        try:
            with open(capture_file, 'r') as f:
                content = f.read()
                
            # Analyze common SPI issues
            if "MISO high" in content and "MOSI low" in content:
                issues.append("No response from sensor - possible CS/clock issue")
            
            if "clock_too_fast" in content:
                issues.append("SPI clock too fast for sensor")
                
            if "no_clock_signal" in content:
                issues.append("SPI clock not generated")
                
            if "wrong_cs_polarity" in content:
                issues.append("Chip select polarity incorrect")
                
        except Exception as e:
            self.log(f"Error reading capture: {e}")
            return {"error": str(e), "fix_needed": True}
        
        return {
            "issues": issues,
            "fix_needed": len(issues) > 0,
            "iteration": self.iteration_count
        }
    
    def generate_device_tree_fix(self, issues):
        """Generate device tree modifications based on issues"""
        dts_file = self.project_root / "boards/nordic/mipe_ev1/mipe_ev1_nrf54l15_cpuapp.dts"
        
        if not dts_file.exists():
            self.log("Device tree file not found")
            return False
        
        # Read current device tree
        with open(dts_file, 'r') as f:
            content = f.read()
        
        modifications = []
        
        # Check if SPI node exists
        if "&spi130" not in content:
            modifications.append(self._add_spi_node())
        
        # Fix clock speed if too fast
        if any("clock" in issue.lower() for issue in issues):
            modifications.append(self._fix_spi_clock())
        
        # Fix CS polarity
        if any("cs" in issue.lower() or "select" in issue.lower() for issue in issues):
            modifications.append(self._fix_cs_polarity())
        
        if modifications:
            new_content = self._apply_dts_modifications(content, modifications)
            with open(dts_file, 'w') as f:
                f.write(new_content)
            self.log(f"Applied {len(modifications)} device tree fixes")
            return True
        
        return False
    
    def _add_spi_node(self):
        """Generate SPI node for LSM6DSO32"""
        return """
&spi130 {
    status = "okay";
    cs-gpios = <&gpio2 10 GPIO_ACTIVE_LOW>;
    pinctrl-0 = <&spi130_default>;
    pinctrl-names = "default";

    lsm6dso32: lsm6dso32@0 {
        compatible = "st,lsm6dso32";
        reg = <0>;
        spi-max-frequency = <1000000>; // Start conservative at 1MHz
        label = "LSM6DSO32";
        
        // Pin configuration
        int1-gpios = <&gpio1 11 GPIO_ACTIVE_HIGH>;
        int2-gpios = <&gpio1 12 GPIO_ACTIVE_HIGH>;
    };
};"""
    
    def _fix_spi_clock(self):
        """Reduce SPI clock speed"""
        return {
            "pattern": r"spi-max-frequency = <(\d+)>",
            "replacement": "spi-max-frequency = <500000>" # Reduce to 500kHz
        }
    
    def _fix_cs_polarity(self):
        """Fix chip select polarity"""
        return {
            "pattern": r"cs-gpios = <&gpio2 10 GPIO_ACTIVE_HIGH>",
            "replacement": "cs-gpios = <&gpio2 10 GPIO_ACTIVE_LOW>"
        }
    
    def _apply_dts_modifications(self, content, modifications):
        """Apply modifications to device tree content"""
        for mod in modifications:
            if isinstance(mod, str):
                # Simple addition - append before closing brace
                content = content.replace("};", mod + "\n};")
            elif isinstance(mod, dict):
                # Regex replacement
                content = re.sub(mod["pattern"], mod["replacement"], content)
        return content
    
    def generate_main_c_fix(self, issues):
        """Generate main.c modifications for SPI communication"""
        main_file = self.project_root / "src/main.c"
        
        if not main_file.exists():
            self.log("main.c not found")
            return False
        
        with open(main_file, 'r') as f:
            content = f.read()
        
        # Check if SPI code already exists
        if "lsm6dso32" in content.lower():
            self.log("SPI code already present, modifying...")
            new_content = self._modify_existing_spi_code(content, issues)
        else:
            self.log("Adding new SPI implementation...")
            new_content = self._add_spi_implementation(content)
        
        with open(main_file, 'w') as f:
            f.write(new_content)
        
        self.log("Updated main.c with SPI implementation")
        return True
    
    def _add_spi_implementation(self, content):
        """Add complete SPI implementation to main.c"""
        spi_code = '''
#include <zephyr/device.h>
#include <zephyr/drivers/spi.h>
#include <zephyr/drivers/gpio.h>

#define LSM6DSO32_WHO_AM_I_REG 0x0F
#define LSM6DSO32_WHO_AM_I_VAL 0x6C

static const struct device *spi_dev;
static struct spi_config spi_cfg;

static int lsm6dso32_read_reg(uint8_t reg, uint8_t *data) {
    uint8_t tx_buffer[2] = {reg | 0x80, 0x00}; // Read bit set
    uint8_t rx_buffer[2] = {0};
    
    struct spi_buf tx_buf = {.buf = tx_buffer, .len = 2};
    struct spi_buf_set tx_bufs = {.buffers = &tx_buf, .count = 1};
    
    struct spi_buf rx_buf = {.buf = rx_buffer, .len = 2};
    struct spi_buf_set rx_bufs = {.buffers = &rx_buf, .count = 1};
    
    int ret = spi_transceive(spi_dev, &spi_cfg, &tx_bufs, &rx_bufs);
    if (ret == 0) {
        *data = rx_buffer[1];
    }
    return ret;
}

static int init_lsm6dso32(void) {
    spi_dev = DEVICE_DT_GET(DT_NODELABEL(spi130));
    if (!device_is_ready(spi_dev)) {
        printk("SPI device not ready\\n");
        return -1;
    }
    
    spi_cfg.frequency = 1000000; // 1MHz
    spi_cfg.operation = SPI_WORD_SET(8) | SPI_TRANSFER_MSB;
    spi_cfg.slave = 0;
    spi_cfg.cs = NULL; // Use GPIO CS
    
    // Test WHO_AM_I register
    uint8_t who_am_i;
    int ret = lsm6dso32_read_reg(LSM6DSO32_WHO_AM_I_REG, &who_am_i);
    if (ret == 0) {
        printk("LSM6DSO32 WHO_AM_I: 0x%02X (expected 0x%02X)\\n", 
               who_am_i, LSM6DSO32_WHO_AM_I_VAL);
        if (who_am_i == LSM6DSO32_WHO_AM_I_VAL) {
            printk("LSM6DSO32 sensor detected successfully!\\n");
            return 0;
        }
    }
    
    printk("LSM6DSO32 communication failed\\n");
    return -1;
}
'''
        
        # Insert before main function
        main_pos = content.find("int main(void)")
        if main_pos > 0:
            # Add SPI code before main
            new_content = content[:main_pos] + spi_code + "\n" + content[main_pos:]
            
            # Add init call to main
            main_brace = new_content.find("{", main_pos + len(spi_code))
            if main_brace > 0:
                init_call = "\n\t// Initialize LSM6DSO32 sensor\n\tinit_lsm6dso32();\n"
                new_content = new_content[:main_brace+1] + init_call + new_content[main_brace+1:]
        else:
            new_content = content + spi_code
        
        return new_content
    
    def _modify_existing_spi_code(self, content, issues):
        """Modify existing SPI code based on issues"""
        
        # Reduce SPI frequency if clock issues
        if any("clock" in issue.lower() for issue in issues):
            content = re.sub(r"spi_cfg\.frequency = \d+", 
                           "spi_cfg.frequency = 500000", content)
        
        # Add delays if timing issues
        if any("timing" in issue.lower() for issue in issues):
            content = content.replace("spi_transceive(", 
                                    "k_msleep(1);\n\tspi_transceive(")
        
        return content
    
    def run_build_test_cycle(self):
        """Execute complete build and test cycle"""
        self.iteration_count += 1
        self.log(f"Starting AI iteration #{self.iteration_count}")
        
        # 1. Build firmware
        build_result = subprocess.run(
            ["west", "build", "-b", "mipe_ev1_nrf54l15_cpuapp"],
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        
        if build_result.returncode != 0:
            self.log(f"Build failed: {build_result.stderr}")
            return False
        
        # 2. Flash firmware
        flash_result = subprocess.run(
            ["west", "flash"],
            cwd=self.project_root,
            capture_output=True,
            text=True
        )
        
        if flash_result.returncode != 0:
            self.log(f"Flash failed: {flash_result.stderr}")
            return False
        
        # 3. Capture signals
        capture_file = self.project_root / "analyzer_captures" / f"spi_test_iter_{self.iteration_count}.csv"
        capture_result = subprocess.run([
            "python", 
            str(self.project_root / "scripts/analyzer_automation.py"),
            str(capture_file)
        ], capture_output=True, text=True)
        
        if capture_result.returncode != 0:
            self.log(f"Capture failed: {capture_result.stderr}")
            return False
        
        # 4. Analyze results
        analysis = self.analyze_capture_results(capture_file)
        
        if analysis["fix_needed"]:
            self.log(f"Issues found: {analysis['issues']}")
            
            # 5. Generate fixes
            self.generate_device_tree_fix(analysis["issues"])
            self.generate_main_c_fix(analysis["issues"])
            
            # 6. Commit changes
            subprocess.run([
                "git", "add", "-A"
            ], cwd=self.project_root)
            
            subprocess.run([
                "git", "commit", "-m", 
                f"AI Fix Iteration #{self.iteration_count}: {', '.join(analysis['issues'])}"
            ], cwd=self.project_root)
            
            return self.run_build_test_cycle()  # Recursive iteration
        else:
            self.log("✅ SPI communication successful! AI development complete.")
            return True

def main():
    generator = SpiCodeGenerator("C:/Development/MIPE_EV1")
    
    # Run autonomous development cycle
    success = generator.run_build_test_cycle()
    
    if success:
        print("🎉 AI Agent successfully implemented SPI communication!")
    else:
        print("❌ AI Agent development cycle incomplete")

if __name__ == "__main__":
    main()