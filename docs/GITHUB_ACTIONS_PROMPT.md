# GitHub Actions Automated Code-Build-Flash-Test Prompt

You are an expert DevOps engineer specializing in embedded systems CI/CD pipelines. Your task is to create a comprehensive GitHub Actions workflow for automated iterative embedded development.

## Project Context

**Project Location**: `C:\Development\MIPE_EV1_2`
**Hardware Platform**: MIPE_EV1 development board (nRF54L15 SoC)
**Development Environment**: Nordic nRF Connect SDK (NCS) v3.1.0
**Logic Analyzer**: Saleae Logic 2 (already installed locally)
**Target**: Automated code → build → flash → hardware test → feedback loop

## Requirements

### 1. Self-Hosted Windows Runner Setup
Create GitHub Actions workflow that runs on a self-hosted Windows runner with:
- Nordic nRF Connect SDK v3.1.0 installed
- J-Link tools for flashing nRF54L15
- Logic 2 software with command-line automation
- Python environment with automation libraries

### 2. Automated Build Pipeline
- **Trigger**: On push to main branch or pull request
- **Build System**: West/CMake build system for Zephyr/NCS
- **Target Board**: `mipe_ev1/nrf54l15/cpuapp`
- **Artifact Management**: Store build artifacts (hex, elf, map files)
- **Build Validation**: Check for compilation errors and warnings

### 3. Automated Flash Process
- **Hardware Connection**: Automatically detect J-Link debugger
- **Flash Verification**: Ensure successful programming
- **Device Reset**: Reset target after flashing
- **Connection Validation**: Verify device is responsive post-flash

### 4. Logic Analyzer Integration
- **Automated Capture**: Use Logic 2 command-line tools to capture GPIO signals
- **Capture Configuration**: 
  - Channels: D0-D7 (8 channels)
  - Sample Rate: 1 MHz
  - Duration: 10 seconds
  - Trigger: Rising edge on specified channel
- **Data Export**: Export capture data in CSV/VCD format for analysis

### 5. Hardware-in-the-Loop Testing
- **GPIO Validation**: Verify expected pin behavior matches firmware
- **Timing Analysis**: Check signal timing against expected values
- **Signal Quality**: Detect signal integrity issues
- **Automated Pass/Fail**: Determine if hardware behavior meets requirements

### 6. Iterative Feedback Loop
- **Test Results**: Generate detailed test reports with pass/fail status
- **Issue Detection**: Automatically identify common hardware issues:
  - Clock/timing problems
  - Pin mapping errors
  - Signal integrity issues
  - Initialization failures
- **Automated Fixes**: Suggest or implement common fixes
- **Retry Logic**: Automatically retry with configuration changes

### 7. Reporting and Artifacts
- **Test Reports**: Generate HTML reports with:
  - Build status and metrics
  - Flash verification results
  - Logic analyzer captures (screenshots)
  - Timing analysis graphs
  - Pass/fail summary
- **Artifact Storage**: Store all test data for historical analysis
- **Notifications**: Send status updates via GitHub status checks

## Implementation Specifications

### GitHub Actions Workflow Structure
```yaml
name: Automated Embedded Development Loop
on: [push, pull_request]
jobs:
  build-flash-test:
    runs-on: [self-hosted, windows, embedded-lab]
    steps:
      - name: Checkout Code
      - name: Setup NCS Environment  
      - name: Build Firmware
      - name: Flash Device
      - name: Hardware Validation
      - name: Logic Analyzer Capture
      - name: Signal Analysis
      - name: Generate Reports
      - name: Upload Artifacts
```

### Required Tools Integration
- **nrfjprog**: Device programming and control
- **Logic 2 CLI**: Automated logic analyzer control
- **Python Scripts**: Custom analysis and reporting
- **CMake/West**: Build system integration

### Expected Deliverables
1. Complete `.github/workflows/embedded-ci.yml` file
2. Python automation scripts for:
   - Logic analyzer control
   - Signal analysis
   - Test result generation
3. PowerShell/Batch scripts for Windows runner setup
4. Documentation for runner configuration and troubleshooting
5. Example test configurations and expected signal patterns

## Success Criteria
- Fully automated code → hardware validation cycle
- Zero manual intervention required
- Comprehensive test reporting with visual feedback
- Robust error handling and retry mechanisms
- Integration with existing MIPE_EV1_2 project structure
- Scalable to multiple hardware configurations

Create a production-ready CI/CD pipeline that enables continuous hardware validation for embedded development.