# RTT + Logic 2 Integration Guide
## Unified Debugging Session Management

### 🎯 System Overview

This guide provides a **best practice way to structure Logic 2 SAL + RTT logs in iterative steps** as requested. The system enables correlation between hardware signal analysis and firmware state debugging.

```
debugging_sessions/
├── session_template/              # Template for new iterations
├── campaign_spi_timing_tests/     # Named test campaigns
│   ├── campaign_metadata.json    # Campaign configuration
│   ├── iterations/               # Numbered test iterations
│   │   ├── iter_001_20251009_140500/  # Iteration 1: Baseline
│   │   ├── iter_002_20251009_141200/  # Iteration 2: Modified config
│   │   └── iter_003_20251009_142000/  # Iteration 3: Final validation
│   └── campaign_summary/         # Campaign-wide analysis
│       └── campaign_summary_20251009.md
├── campaign_gpio_performance/     # Different test campaign
│   ├── campaign_metadata.json
│   ├── iterations/
│   │   ├── iter_001_20251009_150000/  # GPIO baseline
│   │   └── iter_002_20251009_151500/  # GPIO optimization
│   └── campaign_summary/
└── tools/                        # Management utilities
```

### 🔧 Quick Start - Session Management

#### Method 1: Enhanced Campaign Manager (Recommended)
```bash
cd C:\Development\MIPE_EV1\scripts
python enhanced_session_manager.py

# Create test campaign
manager.create_test_campaign("SPI Timing Tests", "Verify SPI timing compliance")

# Add iterations
manager.add_test_iteration("spi_timing_tests", "Baseline measurement")
manager.add_test_iteration("spi_timing_tests", "Modified configuration test") 
manager.add_test_iteration("spi_timing_tests", "Final validation")
```

#### Method 2: GUI Tool
```bash
python session_gui.py  # Will be updated for campaign support
```

### 📋 Structured Workflow - Iterative Steps

#### Step 1: Session Planning
```json
{
  "hardware_setup": {
    "target_board": "MIPE_EV1",
    "logic_analyzer": "Saleae Logic 2",
    "debug_probe": "J-Link EDU Mini V2 (S/N 802004638)",
    "signal_connections": {
      "GPIO_0_02": "Logic 2 Channel 0",
      "GPIO_0_03": "Logic 2 Channel 1"
    }
  },
  "investigation_focus": {
    "primary_goal": "Debug SPI communication timing",
    "signals_of_interest": ["SCLK", "MOSI", "MISO", "CS"],
    "expected_outcomes": ["Timing verification", "Protocol compliance"]
  }
}
```

#### Step 2: Capture Coordination
```
Simultaneous Capture Strategy:
1. Start RTT logging:    robust_rtt_manager.py
2. Start Logic 2:       Logic 2 software (when drivers working)
3. Trigger test scenario
4. Stop both captures
5. Copy files to session
```

#### Step 3: Campaign-Based File Organization
```
campaign_spi_timing_tests/
├── campaign_metadata.json        # Campaign planning & goals
├── iterations/
│   ├── iter_001_20251009_140500/  # Baseline measurement
│   │   ├── iteration_metadata.json
│   │   ├── logic2_captures/
│   │   │   └── spi_baseline.sal
│   │   ├── rtt_logs/
│   │   │   └── rtt_baseline.txt
│   │   └── correlation_analysis/
│   │       └── baseline_analysis.md
│   ├── iter_002_20251009_141200/  # Configuration change test
│   │   ├── iteration_metadata.json
│   │   ├── logic2_captures/
│   │   │   └── spi_modified_config.sal
│   │   ├── rtt_logs/
│   │   │   └── rtt_modified_config.txt
│   │   └── correlation_analysis/
│   │       └── config_change_analysis.md
│   └── iter_003_20251009_142000/  # Final validation
└── campaign_summary/
    └── spi_timing_final_report.md
```

### 🔍 Current System Status

#### ✅ RTT System - Production Ready
- **Status**: Fully operational, 17,609 lines captured successfully
- **Automation**: `robust_rtt_manager.py` handles all process conflicts
- **Integration**: Ready for session management
- **Verification**: Timing analysis shows 23ms intervals

#### ⚠️ Logic 2 System - Hardware Ready, Drivers Blocked  
- **Hardware**: Saleae Logic 2 connected and detected
- **Software**: Installation attempts failed on Windows
- **Blocker**: Driver conflicts prevent J-Link + Logic 2 cooperation
- **Workaround**: RTT-only sessions functional, Logic 2 integration pending

#### 🔧 Session Management - Framework Complete
- **Templates**: Complete session structure established
- **Tools**: GUI and CLI management available
- **Workflow**: Iterative debugging process defined
- **Example**: `20251009_gpio_timing_investigation/` demonstrates structure

### 📊 Real Data Example

From session `20251009_gpio_timing_investigation/`:

```
RTT Timing Analysis:
- Capture Duration: 9 minutes, 23 seconds
- Data Points: 17,609 lines
- Timing Verification: 23ms intervals confirmed
- State Tracking: GPIO initialization sequences validated
- Performance: ~31 log entries per second average
```

**Key Finding**: RTT data alone sufficient for timing verification in current test scenarios.

### 🛠️ Session Management Tools

#### Available Tools

1. **debugging_session_manager.py**
   - Create/list sessions programmatically
   - Add RTT/Logic 2 files to sessions
   - Generate session summaries
   - Template management

2. **session_gui.py**
   - Visual session management
   - Drag-and-drop file addition
   - One-click folder opening
   - Status tracking

3. **robust_rtt_manager.py**
   - Automated RTT capture
   - Process conflict resolution
   - Failsafe operation
   - Integration ready

#### Tool Integration Example
```python
# Create new debugging session
manager = DebuggingSessionManager()
session_id = manager.create_new_session(
    "spi_protocol_analysis", 
    "Verify SPI timing compliance with sensor specification"
)

# Add RTT capture
manager.add_rtt_capture(session_id, "spi_baseline", "rtt_output.txt")

# Add Logic 2 capture (when available)
manager.add_logic2_capture(session_id, "spi_signals", "spi_capture.sal")

# Generate correlation analysis
manager.generate_session_summary(session_id)
```

### 🎯 Immediate Next Actions

#### Ready Now (RTT-Only Sessions)
1. ✅ Create new session with GUI tool
2. ✅ Add RTT captures for timing analysis  
3. ✅ Generate session summaries
4. ✅ Perform firmware state correlation

#### Pending Logic 2 Integration
1. ⏳ Resolve Logic 2 driver installation on Windows
2. ⏳ Test Logic 2 + J-Link cooperative operation
3. ⏳ Validate SAL file import into sessions
4. ⏳ Develop hardware/firmware correlation algorithms

### 📈 Success Metrics

#### Current Achievement
- ✅ RTT system 100% functional with automation
- ✅ Session management framework complete
- ✅ Comprehensive documentation established
- ✅ Real-world validation (17,609 lines captured)

#### Future Integration
- 🎯 Logic 2 driver resolution
- 🎯 Unified capture coordination
- 🎯 Automated correlation analysis
- 🎯 Full hardware/firmware debugging workflow

### 🔧 Quick Reference Commands

```bash
# Start RTT capture with failsafe
python scripts/robust_rtt_manager.py

# Launch session manager GUI  
python scripts/session_gui.py

# Create session via CLI
python scripts/debugging_session_manager.py

# Open existing session folder
explorer "debugging_sessions/20251009_203306_example/"
```

### 💡 Best Practices

1. **Session Planning**: Always fill out metadata before capture
2. **File Naming**: Use descriptive names (not timestamps)
3. **Correlation**: Link RTT log events to Logic 2 signal changes
4. **Documentation**: Update session_summary.md during investigation
5. **Backup**: Keep original captures unchanged, work on copies

---

## 🚀 BuildFlash Campaign & GitHub Actions Workflow

### BuildFlash Campaign
- Use `campaign_buildflash` for all development cycles where the goal is to get a successful build and flash.
- Each iteration documents a build/flash/test cycle.
- Folder structure:

```
debugging_sessions/
└── campaign_buildflash/
    ├── campaign_metadata.json
    └── iterations/
        └── iter_001_20251010_000000/
            ├── iteration_metadata.json
            ├── logic2_captures/
            ├── rtt_logs/
            └── correlation_analysis/
```

### GitHub Actions: Automated Build/Flash
- Workflow file: `.github/workflows/build-flash.yml`
- Runs on every push/PR to `main`
- Steps:
  1. Checkout code
  2. Set up Python
  3. Install dependencies (if any)
  4. Build firmware (calls `build_mipe.bat` if present)
  5. Simulate flashing (real flashing requires hardware)
  6. Upload build artifacts (hex files)
- If the build fails, the workflow fails

#### How to Use
1. Make code changes and push to GitHub
2. GitHub Actions will build automatically
3. Check the Actions tab for build results and artifacts
4. If build fails, fix code and repeat
5. When build and flash succeed, document in the campaign iteration

---

**Status**: RTT mission accomplished ✅ | Logic 2 integration framework ready ⏳ | Awaiting driver resolution for complete system 🔧