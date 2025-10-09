# Project: MIPE_EV1

## 1. Introduction

This document provides a comprehensive overview of the MIPE_EV1 project, a custom-designed embedded system. It details the hardware architecture, the development environment, and the objectives for the initial test code. The project is centered around the nRF54L15 microcontroller (MCU) and is intended for applications requiring Bluetooth Low Energy (BLE) connectivity.

## 2. Hardware Architecture

The MIPE_EV1 hardware is a custom-built Printed Circuit Board Assembly (PCBA) designed specifically for this application. The key components and their configurations are outlined below.

| Component | Details |
|---|---|
| **MCU** | nRF54L15 (or specified SoC) |
| **Peripheral** | LSM6 (Note: Present on board, but not to be initialized or used in the initial test code) |
| **BLE** | Fully functional BLE RF output stage |
| **LEDs** | LED0 (P0.00), LED1 (P0.01) |
| **Test GPIOs** | TestPin05 (P1.05), TestPin06 (P1.06) |
| **Programming** | SWD Interface (SWDIO, SWDCLK, VDD, GND) |

### 2.1. Microcontroller (MCU)

The core of the MIPE_EV1 is the nRF54L15, a powerful and efficient MCU that provides the necessary processing capabilities for the intended application. Its selection is driven by the need for a robust BLE solution and flexible GPIO mapping.

### 2.2. Peripherals

The board includes an LSM6, a high-performance inertial measurement unit (IMU). However, for the initial test code, there should be **no interaction with this peripheral**. The LSM6 is connected to the MCU via the following pins:

*   **SCK:** P2.01
*   **MOSI:** P2.02
*   **MISO:** P2.04
*   **CS:** P2.05

### 2.3. Connectivity

The MIPE_EV1 is equipped with a fully functional BLE RF output stage, enabling wireless communication. The board does **not** have a UART interface.

### 2.4. User Interface

The user interface is minimal, consisting of two LEDs for visual feedback:

*   **LED0:** Connected to pin P0.00
*   **LED1:** Connected to pin P0.01

## 3. Development Environment

The project's source code is located in the following directory:

```
C:\Development\MIPE_EV1
```

Firmware is flashed and debugged using a SEGGER J-Link EDU mini via the Serial Wire Debug (SWD) interface. The required connections are SWDIO, SWDCLK, VDD, and GND.

## 4. Initial Test Code Objective

The primary goal of the initial test code is to verify the basic functionality of the hardware after a reset or power-up event. The code must execute the following sequence of operations:

1.  **Wait:** A 1-second delay to allow for system stabilization.
2.  **Flash LED0:** Turn on LED0 for 200ms, then turn it off.
3.  **Flash LED1:** Turn on LED1 for 200ms, then turn it off.
4.  **Toggle TestPin05:** Set TestPin05 high for 200ms, then set it low.
5.  **Toggle TestPin06:** Set TestPin06 high for 200ms, then set it low.
6.  **Indicate Completion:** Light up LED1 to signify that the test sequence has finished successfully.

It is **strictly prohibited** to initialize or use the SPI or UART interfaces in this test code. The focus is solely on GPIO manipulation and basic timing.



nRF54l15 pinning: 

3:P1.02 Available on PCB
4:P1.03 Available
5:P1.04 Available : D7
6:P1.05 Available : D5
7:P1.06 Available : D6
8:P1.07
9:P1.08
10:VDD : D5
11: P2.00
12:P2.01 Available : D1
13:P2.02 Available : D4
14:P2.03
15:P2.04 Available : D3
16:P2.05 Available : D0
17:P2.06
18:P2.07 Available
19:P2.08 Available
20:P2.09 Available
21:P2.10 Available
22:VDD
23:P0.00
24:P0.01
25:swdio Available
26:swdclk Available