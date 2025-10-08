# Copyright (c) 2025 MIPE_EV1 Project
# SPDX-License-Identifier: Apache-2.0

# Configure J-Link for nRF54L15 CPUAPP
if(CONFIG_SOC_NRF54L15_CPUAPP)
	board_runner_args(jlink "--device=nRF54L15_M33" "--speed=4000")
endif()

include(${ZEPHYR_BASE}/boards/common/nrfjprog.board.cmake)
include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
