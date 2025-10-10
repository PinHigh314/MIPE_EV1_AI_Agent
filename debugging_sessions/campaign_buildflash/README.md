# BuildFlash Campaign - Development Iteration

This campaign is for rapid build/flash/test cycles during firmware development.

## Objective
- Adjust code as required
- Build it
- Flash it
- Repeat until the code builds and flashes successfully

## How to Use
1. Make code changes as needed
2. Run the build and flash process (locally or via GitHub Actions)
3. If the build or flash fails, fix the code and repeat
4. When successful, document the result in this iteration

## Automation
- The `.github/workflows/build-flash.yml` workflow will build the code on every push/PR
- If the build fails, the workflow fails
- Artifacts (hex files) are uploaded for reference
- Flashing is simulated in CI (real flashing requires hardware)

## Folder Structure
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

---

_Use this campaign for all development cycles where the goal is to get a successful build and flash. Add new iterations as needed for each major change or test._
