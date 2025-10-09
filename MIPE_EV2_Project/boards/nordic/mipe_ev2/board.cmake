board_runner_args(nrfjprog "--nrf-family=NRF54L")
board_runner_args(jlink "--device=nrf54l15_xxaa" "--speed=4000")

include(${ZEPHYR_BASE}/boards/common/nrfjprog.board.cmake)
include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)