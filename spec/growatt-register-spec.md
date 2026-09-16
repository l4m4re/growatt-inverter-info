# Growatt Register Specification

The JSON specification is authoritative. This document is generated from the same in-memory model and presents the shared register blocks in vendor protocol order.

## Contents

- [Scope / applicability](#scope--applicability)
- [Holding registers](#holding-registers)
  - [First group](#block-cb-holding-p009-first_group-block-01)
  - [Second group](#block-cb-holding-p016-second_group-block-02)
  - [Six group for Storage Power](#block-cb-holding-p027-six_group_for_storage_power-block-03)
  - [Use for TL-X and TL-XH](#block-cb-holding-p035-use_for_tl_x_and_tl_xh-block-04)
  - [US Machine type Time Set](#block-cb-holding-p042-us_machine_type_time_set-block-05)
  - [BDC information (support up to 10 parallel BDC)](#block-cb-holding-p047-bdc_information_support_up_to_10_parallel_bdc-block-06)
- [Input registers](#input-registers)
  - [First group](#block-cb-input-p047-first_group-block-07)
  - [Second group](#block-cb-input-p051-second_group-block-08)
  - [The eighth group for PV9-PV16 information](#block-cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09)
  - [Ninth group for Storage power](#block-cb-input-p059-ninth_group_for_storage_power-block-10)
  - [BMS Infomation](#block-cb-input-p062-bms_infomation-block-11)
  - [Ups information (offline)](#block-cb-input-p062-ups_information_offline-block-12)
  - [Ninth group reserved for storage power](#block-cb-input-p064-ninth_group_reserved_for_storage_power-block-13)
  - [Use for TL-X and TL-XH](#block-cb-input-p070-use_for_tl_x_and_tl_xh-block-14)
  - [BDC and BMS information (support up to 10 PARALLEL BDCS)](#block-cb-input-p084-bdc_and_bms_information_support_up_to_10_parallel_bdcs-block-15)
- [Logical multi-word fields](#logical-multi-word-fields)

## Scope / applicability

The register maps preserve the source-native block layout. Each shared block is defined once; applicability paths connect families and declared ranges to those blocks. A declared family range does not by itself establish semantic rows for every address.

| Family | Models | Protocol group | Shared blocks |
| --- | --- | --- | --- |
| TL-X/TL-XH/TL-XH US (MIN Type) | MIN 6000TL-XH | 120 | 4 |
| MOD TL3-XH | Models not specified | 120 | 3 |
| Storage (MIX Type) | Models not specified | 120 | 6 |
| Storage (SPA Type) | Models not specified | 120 | 6 |
| Storage (SPH Type) | Models not specified | 120 | 7 |
| MAX 1500V/MAX-X LV / TL3-X (MAX, MID, MAC Type) | Models not specified | 120 | 5 |

Block applicability retains the vendor declarations and source/model qualifiers in the JSON `applicability` section.

## Holding registers

<a id="block-cb-holding-p009-first_group-block-01"></a>
### First group

- **Vendor heading:** First group
- **Normalized role:** not normalized (unresolved_ordinal_label)
- **Table / function:** Holding / FC03
- **Address range:** H0–H124
- **Applicable families / models:** MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) (models not specified); TL-X/TL-XH/TL-XH US (MIN Type) (MIN 6000TL-XH); MOD TL3-XH (models not specified); Storage (MIX Type) (models not specified); Storage (SPA Type) (models not specified); Storage (SPH Type) (models not specified)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 9–15; 125 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H0 | Inverter enable flags | Inverter enable flags | read_write | u16 bitfield, unsigned | scale=1, multiplier=1 | — | 0、1、2、 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1 | Safety function enable flags | SPI: system protection interface Bit0~3:forCEI0-21 Bit4~6:forSAA | write | register value, unsigned | — | — | 0         :; 0 = SPIenable Bit1; 2 = LVFRTenable Bit3; 3 = forCEI0-21 Bit4 / forCEI0-21 Bit4~6:forSAA register value None; 4 = Softstartenable Bit5; 6 = PowerVoltFunc Enable Bit7 / forSAA; 8 = ROCOFenable Bit9 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H2 | Persist power-factor commands | Means these settings will be acting or not when next poweron | write | register value, unsigned | scale=1, multiplier=1 | — | 0or1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H3 | Active power limit setpoint | 255:powerisnotbelimited | write | register value | divisor=1, scale=1, multiplier=1 | % | 0-100 or %; 255 = powerisnotbelimited / powerisnotbelimited register value % | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H4 | Reactive power limit setpoint | 255:powerisnotbelimited | write | register value, signed | divisor=1 | % | -100-100 %; 255 = powerisnotbelimited / powerisnotbelimited register value % | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H5 | Power factor target | Inverter output power factor’s10000times | write | register value, unsigned | divisor=10000 | pf | 0-20000, | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H6 | Rated apparent power (high word) | Normal power(high) | read | register value, unsigned | divisor=10 | 0.1VA | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H7 | Rated apparent power (low word) | Normal power(low) | read | register value, unsigned | divisor=10 | 0.1VA | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H8 | Nominal PV voltage | NormalworkPV voltage | read | register value, unsigned | divisor=10 | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H9 | Firmware (high word) | Firmwareversion (high) | read | firmware_version | divisor=10 | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H10 | Firmware (middle word) | Firmwareversion (middle) | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H11 | Firmware (low word) | Firmwareversion(low) | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H12 | Firmware (high word) | ControlFirmware version(high) | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H13 | Firmware (middle word) | ControlFirmware version(middle) | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H14 | Firmware (low word) | ControlFirmware version(low) | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H15 | LCD language selection | 0:Italian; 1:English; 2:German; 3:Spanish; 4:French; 5:Chinese; 6：Polish 7：Portugues 8：Hungary | write | register value, unsigned | — | — | 0-5; 0 = Italian; 1 = English; 2 = German; 3 = Spanish; 4 = French; 5 = Chinese | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H16 | Country profile configured | CountrySelectedor not | write | register value, unsigned | — | — | 0: need | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H17 | PV start voltage threshold | Inputstartvoltage | write | register value, unsigned | divisor=10 | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H18 | Start-up delay | Starttime | write | register value, unsigned | divisor=1 | 1s | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H19 | Restart delay | RestartDelayTime afterfaultback; | write | register value, unsigned | divisor=1 | 1s | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H20 | Active power ramp rate (startup) | Powerstartslope | write | register value, unsigned | divisor=10 | 0.1% | -1000      0.1% | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H21 | Active power ramp rate (restart) | Powerrestartslope | write | register value, unsigned | divisor=10 | 0.1% | -1000      0.1% | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H22 | Modbus RTU baud rate | Select communicationbaudrat e 0:9600bps 1:38400bps | write | register value, unsigned | — | — | -1; 0 = 9600bps; 1 = 38400bps register value None | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H23 | Inverter serial number | Inverter serial number | read | ASCII, 10 characters | — | ASCII | ASCI | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H24 | Serial Number | The Home Assistant integration exposes this as the device serial number and reuses it as the unique identifier. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H25 | Serial Number | The Home Assistant integration exposes this as the device serial number and reuses it as the unique identifier. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H26 | Serial Number | The Home Assistant integration exposes this as the device serial number and reuses it as the unique identifier. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H27 | Serial Number | The Home Assistant integration exposes this as the device serial number and reuses it as the unique identifier. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H28 | Inverter Model (high word) | Home Assistant renders this value as the string A# B# D# T# P# U# M# S# via the integration's model() helper. Vendor spec lists value pattern `&*5`; digits appear to be stored without the leading letter codes, so treat as encoded tokens until verified on hardware. | read | register value | divisor=10 | — | *5 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H29 | Inverter Model (low word) | Home Assistant renders this value as the string A# B# D# T# P# U# M# S# via the integration's model() helper. Vendor spec lists value pattern `&*5`; digits appear to be stored without the leading letter codes, so treat as encoded tokens until verified on hardware. | read | register value | — | — | *5 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H30 | Modbus slave address | Communicate address | write | register value | — | — | -254 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H31 | Firmware update trigger | Updatefirmware | write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H32 | Reset user configuration | Use with caution; the inverter immediately reboots and loses provisioning data. | write | register value | — | — | x0001 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H33 | Factory reset | Equivalent to the front-panel factory reset. Requires re-commissioning afterwards. | write | register value | — | — | x0001 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H34 | Manufacturer information string | The original table lists these words as Manufacturer Info 8-1 (high/middle/low); combine them to read the full string. | read | register value | — | ASCII | ASCI | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H35 | Manufacturer information string | The original table lists these words as Manufacturer Info 8-1 (high/middle/low); combine them to read the full string. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H36 | Manufacturer information string | The original table lists these words as Manufacturer Info 8-1 (high/middle/low); combine them to read the full string. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H37 | Manufacturer information string | The original table lists these words as Manufacturer Info 8-1 (high/middle/low); combine them to read the full string. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H38 | Manufacturer information string | The original table lists these words as Manufacturer Info 8-1 (high/middle/low); combine them to read the full string. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H39 | Manufacturer information string | The original table lists these words as Manufacturer Info 8-1 (high/middle/low); combine them to read the full string. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H40 | Manufacturer information string | The original table lists these words as Manufacturer Info 8-1 (high/middle/low); combine them to read the full string. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H41 | Manufacturer information string | The original table lists these words as Manufacturer Info 8-1 (high/middle/low); combine them to read the full string. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H42 | G100 failsafe enable | EnglishG100failsafeset | write | register value | — | — | nable:1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H43 | Device type code | Device type code | read | vendor encoded | — | — | *6 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H44 | Trackers and phases | Trackers and phases | read | high byte trackers, low byte phases | — | — | Eg:0x020 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H45 | System clock year | Localtime | write | register value | — | — | Year | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H46 | System clock month | Systemtime-Month | write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H47 | System clock day | Systemtime-Day | write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H48 | System clock hour | Systemtime-Hour | write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H49 | System clock minute | Systemtime-Min | write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H50 | System clock second | Systemtime-Second | write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H51 | System clock weekday | SystemWeekly | write | register value | — | — | 0-6 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H52 | Stage 1 undervoltage limit | Gridvoltagelowlimit protect | write | register value | — | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H53 | Stage 1 overvoltage limit | Gridvoltagehighlimit protect | write | register value | — | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H54 | Stage 1 underfrequency limit | Gridfrequencylow limitprotect | write | register value | — | 0.01 Hz | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H55 | Stage 1 overfrequency limit | Gridhigh frequencylimitprotect | write | register value | — | 0.01 Hz | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H56 | Stage 2 undervoltage limit | Gridvoltagelowlimit protect2 | write | register value | — | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H57 | Stage 2 overvoltage limit | Gridvoltagehighlimit protect2 | write | register value | — | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H58 | Stage 2 underfrequency limit | Gridfrequencylow limitprotect2 | write | register value | — | 0.01 Hz | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H59 | Stage 2 overfrequency limit | Gridhighfrequency limitprotect2 | write | register value | — | 0.01 Hz | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H60 | Stage 3 undervoltage limit | Grid voltage low limit protect3 | write | register value | — | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H61 | Stage 3 overvoltage limit | Grid voltage high limit protect3 | write | register value | — | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H62 | Grid frequency | Grid frequency low limitprotect3 | write | register value | — | 0.01Hz | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H63 | Grid frequency | Grid frequency high limitprotect3 | write | register value | — | 0.01Hz | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H64 | Reconnect undervoltage limit | Gridlowvoltagelimit connecttoGrid | write | register value | — | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H65 | Reconnect overvoltage limit | Gridhighvoltagelimit connecttoGrid | write | register value | — | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H66 | Reconnect underfrequency limit | Gridlowfrequency | write | register value | — | 0.01 | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H67 | Reconnect overfrequency limit | Gridhighfrequency limitconnecttoGrid | write | register value | — | 0.01 Hz | 0.01 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H68 | Stage 1 undervoltage trip delay | Grid voltage low limit protecttime 1 | write | register value | — | Cycle | Cycle | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H69 | Stage 1 overvoltage trip delay | Grid voltage high limit protecttime 1 | write | register value | — | Cycle | Cycle | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H70 | Stage 2 undervoltage trip delay | Grid voltage low limit protecttime 2 | write | register value | — | Cycle | Cycle | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H71 | Stage 2 overvoltage trip delay | Grid voltage high limit protecttime 2 | write | register value | — | Cycle | Cycle | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H72 | Grid frequency | Grid frequency low limitprotecttime 1 | write | register value | — | Cycle | Cycle | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H73 | Grid frequency | Grid frequency high limitprotecttime 1 | write | register value | — | Cycle | Cycle | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H74 | Grid frequency | Grid frequency low limitprotecttime 2 | write | register value | — | Cycle | Cycle | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H75 | Grid frequency | Grid frequency high limitprotecttime 2 | write | register value | — | Cycle | Cycle | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H76 | Stage 3 undervoltage trip delay | Grid voltage low limit protecttime 3 | write | register value | — | Cycle | Cycle | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H77 | Stage 3 overvoltage trip delay | Grid voltage high limit protecttime 3 | write | register value | — | Cycle | Cycle | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H78 | Grid frequency | Grid frequency low limitprotecttime 3 | write | register value | — | Cycle | Cycle | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H79 | Grid frequency | Grid frequency high limitprotecttime 3 | write | register value | — | Cycle | Cycle | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H80 | Ten-minute overvoltage limit | Voltprotectionfor10 min | write | register value | — | 0.1V | 0.1V    1.1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H81 | PV input high-voltage fault | PVVoltageHigh Fault | write | register value | — | 0.1V | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H82 | Controller firmware build string | Positions: 0-1 model letters, 2-3 model variant, 4-5 DSP1 build, 6-7 DSP2/M0 build, 8-9 CPLD/AFCI build, 10-11 M3 build. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H83 | Controller firmware build string | Positions: 0-1 model letters, 2-3 model variant, 4-5 DSP1 build, 6-7 DSP2/M0 build, 8-9 CPLD/AFCI build, 10-11 M3 build. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H84 | Controller firmware build string | Positions: 0-1 model letters, 2-3 model variant, 4-5 DSP1 build, 6-7 DSP2/M0 build, 8-9 CPLD/AFCI build, 10-11 M3 build. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H85 | Controller firmware build string | Positions: 0-1 model letters, 2-3 model variant, 4-5 DSP1 build, 6-7 DSP2/M0 build, 8-9 CPLD/AFCI build, 10-11 M3 build. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H86 | Controller firmware build string | Positions: 0-1 model letters, 2-3 model variant, 4-5 DSP1 build, 6-7 DSP2/M0 build, 8-9 CPLD/AFCI build, 10-11 M3 build. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H87 | Controller firmware build string | Positions: 0-1 model letters, 2-3 model variant, 4-5 DSP1 build, 6-7 DSP2/M0 build, 8-9 CPLD/AFCI build, 10-11 M3 build. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H88 | Modbus version | Modbus version | read | u16 / 100, unsigned | divisor=100, scale=0.01 | version | Eg：207 is Int(1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H89 | Power-factor control mode | 0=Unity PF, 1=Fixed PF setpoint, 2=Default PF line, 3=User-defined PF line, 4=Under-excited reactive power, 5=Over-excited reactive power, 6=Q(V) curve, 7=Direct control, 8=Static capacitive QV, 9=Static inductive QV. | write | register value | — | — | 0 = PF / Unity PF; 1 = Fixed PF setpoint / PFbyset 2; 2 = Default PF line; 3 = User-defined PF line / UserPFline 4; 4 = Under-excited reactive power; 5 = Over-excited reactive power / OverExcited; 6 = Q / Q(V) curve; 7 = Direct control; 8 = Static capacitive QV; 9 = Static inductive QV / Static inductive QV. register value None | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H90 | GPRS modem IP/status flags | Bit 0-3: 0=idle, 1=IP read requested, 2=set IP succeeded; Bit 4-7: 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. | write | register value | — | — | Bit0-3:ab; 0 = idle / unknown; 1 = IP read requested / modem OK; 2 = no SIM / set IP succeeded; 3 = 0=idle / no network / read; 4 = TCP connect fail; 5 = TCP connected; 7 = 0=unknown / GPRSstatus Bit 0-3 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H91 | Frequency derating start | Frequencyderating startpoint | write | register value | — | 0.01H Z | 0.0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H92 | Frequency derating slope | Frequency–loadlimit rate | write | register value | — | 10tim es | 0-100       10t | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H93 | CEI 0-21 Q(V) point V1S | CEI021V1SQ(v) | write | register value | — | 0.1V | V1S<V2S 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H94 | CEI 0-21 Q(V) point V2S | CEI021V2SQ(v) | write | register value | — | 0.1V | 0.1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H95 | CEI 0-21 Q(V) point V1L | CEI021V1LQ(v) | write | register value | — | 0.1V | V1L<V1S 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H96 | CEI 0-21 Q(V) point V2L | CEI021V2LQ(v) | write | register value | — | 0.1V | V2L<V1L 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H97 | Q(V) lock-in active power | Q(v)lockinactive powerofCEI021 | write | register value | — | Percen t | 0-100       Per | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H98 | Q(V) lock-out active power | Q(v)lockOutactive powerofCEI021 | write | register value | — | Percen t | 0-100       Per | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H99 | Power-factor curve lock-in voltage | Lockingirdvoltof CEI021PFline | write | register value | — | 0.1V | nVn         0.1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H100 | Power-factor curve lock-out voltage | Lockoutgirdvoltof CEI021PFline | write | register value | — | 0.1V | nVn         0.1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H101 | Power-factor adjust value 1 | PFadjustvalue1 | write | register value | — | — | 4096 is 1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H102 | Power-factor adjust value 2 | PFadjustvalue2 | write | register value | — | — | 4096 is 1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H103 | Power-factor adjust value 3 | PFadjustvalue3 | write | register value | — | — | 4096 is 1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H104 | Power-factor adjust value 4 | PFadjustvalue4 | write | register value | — | — | 4096 is 1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H105 | Power-factor adjust value 5 | PFadjustvalue5 | write | register value | — | — | 4096 is 1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H106 | Power-factor adjust value 6 | PFadjustvalue6 | write | register value | — | — | 4096 is 1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H107 | Q(V) response delay | QV Reactive Power delaytime | write | register value | — | 1S | 0-30 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H108 | Over-frequency derating delay | Overfrequency derati ngdelaytime | write | register value | — | 50ms | 0-20 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H109 | Maximum reactive power magnitude | QmaxforQ(V)curve | write | register value | — | 0.1% | 0-1000 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H110 | PF curve point 1 load | 255meansnothispoint | write | register value | — | percen t | 0-255 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H111 | PF curve point 1 target | PFlimitlinepoint1 powerfactor | write | register value | — | — | 0-20000 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H112 | PF curve point 2 load | 255meansnothispoint | write | register value | — | percen t | 0-255 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H113 | PF curve point 2 target | PFlimitlinepoint 2powerfactor | write | register value | — | — | 0-20000 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H114 | PF curve point 3 load | 255meansnothispoint | write | register value | — | percen t | 0-255 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H115 | PF curve point 3 target | PFlimitlinepoint3 powerfactor | write | register value | — | — | 0-20000 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H116 | PF curve point 4 load | 255meansnothispoint | write | register value | — | percen t | 0-255 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H117 | PF curve point 4 target | PFlimitlinepoint4 powerfactor | write | register value | — | — | 0-20000 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H118 | Module code segments | SxxBxx | read | register value | — | — | &*11 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H119 | Module code segments | DxxTxx | read | register value | — | — | &*11 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H120 | Module code segments | PxxUxx | read | register value | — | — | &*11 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H121 | Module code segments | Mxxxx Power | read | register value | — | — | &*11 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H122 | Export limit enable mode | ExportLimitenable, 0:DisableexportLimit; 1:Enable485exportLimit; 2:Enable232exportLimit; 3:EnableCTexportLimit; | read_write | register value | — | — | /W 1/0; 0 = DisableexportLimit; 1 = Enable485exportLimit; 2 = Enable232exportLimit; 3 = EnableCTexportLimit | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H123 | Export limit power setpoint | ExportLimitPowerRate | read_write | register value | — | 0.1% | /W -1000~+1 0.1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H124 | Tracker coupling mode | 0:Independent 1:DCSource 2:Parallel | write | register value | — | — | 0,1,2; 0 = Independent / Independent 1; 1 = DCSource; 2 = Parallel / Parallel register value None | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH; Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |

#### Enum values

| Address | Source identity | Value | Vendor label | Ambiguous |
| --- | --- | --- | --- | --- |
| H1 | MOD TL3-XH | 0 | SPIenable Bit1 | False |
| H1 | MOD TL3-XH | 2 | LVFRTenable Bit3 | False |
| H1 | MOD TL3-XH | 3 | forCEI0-21 Bit4 / forCEI0-21 Bit4~6:forSAA register value None | True |
| H1 | MOD TL3-XH | 4 | Softstartenable Bit5 | False |
| H1 | MOD TL3-XH | 6 | PowerVoltFunc Enable Bit7 / forSAA | True |
| H1 | MOD TL3-XH | 8 | ROCOFenable Bit9 | False |
| H1 | Storage (MIX Type) | 0 | SPIenable Bit1 | False |
| H1 | Storage (MIX Type) | 2 | LVFRTenable Bit3 | False |
| H1 | Storage (MIX Type) | 3 | forCEI0-21 Bit4 / forCEI0-21 Bit4~6:forSAA register value None | True |
| H1 | Storage (MIX Type) | 4 | Softstartenable Bit5 | False |
| H1 | Storage (MIX Type) | 6 | PowerVoltFunc Enable Bit7 / forSAA | True |
| H1 | Storage (MIX Type) | 8 | ROCOFenable Bit9 | False |
| H1 | Storage (SPA Type) | 0 | SPIenable Bit1 | False |
| H1 | Storage (SPA Type) | 2 | LVFRTenable Bit3 | False |
| H1 | Storage (SPA Type) | 3 | forCEI0-21 Bit4 / forCEI0-21 Bit4~6:forSAA register value None | True |
| H1 | Storage (SPA Type) | 4 | Softstartenable Bit5 | False |
| H1 | Storage (SPA Type) | 6 | PowerVoltFunc Enable Bit7 / forSAA | True |
| H1 | Storage (SPA Type) | 8 | ROCOFenable Bit9 | False |
| H1 | Storage (SPH Type) | 0 | SPIenable Bit1 | False |
| H1 | Storage (SPH Type) | 2 | LVFRTenable Bit3 | False |
| H1 | Storage (SPH Type) | 3 | forCEI0-21 Bit4 / forCEI0-21 Bit4~6:forSAA register value None | True |
| H1 | Storage (SPH Type) | 4 | Softstartenable Bit5 | False |
| H1 | Storage (SPH Type) | 6 | PowerVoltFunc Enable Bit7 / forSAA | True |
| H1 | Storage (SPH Type) | 8 | ROCOFenable Bit9 | False |
| H1 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | SPIenable Bit1 | False |
| H1 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 2 | LVFRTenable Bit3 | False |
| H1 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 3 | forCEI0-21 Bit4 / forCEI0-21 Bit4~6:forSAA register value None | True |
| H1 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 4 | Softstartenable Bit5 | False |
| H1 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 6 | PowerVoltFunc Enable Bit7 / forSAA | True |
| H1 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 8 | ROCOFenable Bit9 | False |
| H3 | TL-X/TL-XH/TL-XH US (MIN Type) | 255 | powerisnotbelimited / powerisnotbelimited register value % | True |
| H3 | MOD TL3-XH | 255 | powerisnotbelimited / powerisnotbelimited register value % | True |
| H3 | Storage (MIX Type) | 255 | powerisnotbelimited / powerisnotbelimited register value % | True |
| H3 | Storage (SPA Type) | 255 | powerisnotbelimited / powerisnotbelimited register value % | True |
| H3 | Storage (SPH Type) | 255 | powerisnotbelimited / powerisnotbelimited register value % | True |
| H3 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 255 | powerisnotbelimited / powerisnotbelimited register value % | True |
| H4 | TL-X/TL-XH/TL-XH US (MIN Type) | 255 | powerisnotbelimited / powerisnotbelimited register value % | True |
| H4 | MOD TL3-XH | 255 | powerisnotbelimited / powerisnotbelimited register value % | True |
| H4 | Storage (MIX Type) | 255 | powerisnotbelimited / powerisnotbelimited register value % | True |
| H4 | Storage (SPA Type) | 255 | powerisnotbelimited / powerisnotbelimited register value % | True |
| H4 | Storage (SPH Type) | 255 | powerisnotbelimited / powerisnotbelimited register value % | True |
| H4 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 255 | powerisnotbelimited / powerisnotbelimited register value % | True |
| H15 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | Italian | False |
| H15 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | English | False |
| H15 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | German | False |
| H15 | TL-X/TL-XH/TL-XH US (MIN Type) | 3 | Spanish | False |
| H15 | TL-X/TL-XH/TL-XH US (MIN Type) | 4 | French | False |
| H15 | TL-X/TL-XH/TL-XH US (MIN Type) | 5 | Chinese | False |
| H15 | MOD TL3-XH | 0 | Italian | False |
| H15 | MOD TL3-XH | 1 | English | False |
| H15 | MOD TL3-XH | 2 | German | False |
| H15 | MOD TL3-XH | 3 | Spanish | False |
| H15 | MOD TL3-XH | 4 | French | False |
| H15 | MOD TL3-XH | 5 | Chinese | False |
| H15 | Storage (MIX Type) | 0 | Italian | False |
| H15 | Storage (MIX Type) | 1 | English | False |
| H15 | Storage (MIX Type) | 2 | German | False |
| H15 | Storage (MIX Type) | 3 | Spanish | False |
| H15 | Storage (MIX Type) | 4 | French | False |
| H15 | Storage (MIX Type) | 5 | Chinese | False |
| H15 | Storage (SPA Type) | 0 | Italian | False |
| H15 | Storage (SPA Type) | 1 | English | False |
| H15 | Storage (SPA Type) | 2 | German | False |
| H15 | Storage (SPA Type) | 3 | Spanish | False |
| H15 | Storage (SPA Type) | 4 | French | False |
| H15 | Storage (SPA Type) | 5 | Chinese | False |
| H15 | Storage (SPH Type) | 0 | Italian | False |
| H15 | Storage (SPH Type) | 1 | English | False |
| H15 | Storage (SPH Type) | 2 | German | False |
| H15 | Storage (SPH Type) | 3 | Spanish | False |
| H15 | Storage (SPH Type) | 4 | French | False |
| H15 | Storage (SPH Type) | 5 | Chinese | False |
| H15 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | Italian | False |
| H15 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 1 | English | False |
| H15 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 2 | German | False |
| H15 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 3 | Spanish | False |
| H15 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 4 | French | False |
| H15 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 5 | Chinese | False |
| H22 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | 9600bps | False |
| H22 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | 38400bps register value None | False |
| H22 | MOD TL3-XH | 0 | 9600bps | False |
| H22 | MOD TL3-XH | 1 | 38400bps register value None | False |
| H22 | Storage (MIX Type) | 0 | 9600bps | False |
| H22 | Storage (MIX Type) | 1 | 38400bps register value None | False |
| H22 | Storage (SPA Type) | 0 | 9600bps | False |
| H22 | Storage (SPA Type) | 1 | 38400bps register value None | False |
| H22 | Storage (SPH Type) | 0 | 9600bps | False |
| H22 | Storage (SPH Type) | 1 | 38400bps register value None | False |
| H22 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | 9600bps | False |
| H22 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 1 | 38400bps register value None | False |
| H89 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | PF / Unity PF | True |
| H89 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | Fixed PF setpoint / PFbyset 2 | True |
| H89 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | Default PF line | False |
| H89 | TL-X/TL-XH/TL-XH US (MIN Type) | 3 | User-defined PF line / UserPFline 4 | True |
| H89 | TL-X/TL-XH/TL-XH US (MIN Type) | 4 | Under-excited reactive power | False |
| H89 | TL-X/TL-XH/TL-XH US (MIN Type) | 5 | Over-excited reactive power / OverExcited | True |
| H89 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | Q / Q(V) curve | True |
| H89 | TL-X/TL-XH/TL-XH US (MIN Type) | 7 | Direct control | False |
| H89 | TL-X/TL-XH/TL-XH US (MIN Type) | 8 | Static capacitive QV | False |
| H89 | TL-X/TL-XH/TL-XH US (MIN Type) | 9 | Static inductive QV / Static inductive QV. register value None | True |
| H89 | MOD TL3-XH | 0 | PF / Unity PF | True |
| H89 | MOD TL3-XH | 1 | Fixed PF setpoint / PFbyset 2 | True |
| H89 | MOD TL3-XH | 2 | Default PF line | False |
| H89 | MOD TL3-XH | 3 | User-defined PF line / UserPFline 4 | True |
| H89 | MOD TL3-XH | 4 | Under-excited reactive power | False |
| H89 | MOD TL3-XH | 5 | Over-excited reactive power / OverExcited | True |
| H89 | MOD TL3-XH | 6 | Q / Q(V) curve | True |
| H89 | MOD TL3-XH | 7 | Direct control | False |
| H89 | MOD TL3-XH | 8 | Static capacitive QV | False |
| H89 | MOD TL3-XH | 9 | Static inductive QV / Static inductive QV. register value None | True |
| H89 | Storage (MIX Type) | 0 | PF / Unity PF | True |
| H89 | Storage (MIX Type) | 1 | Fixed PF setpoint / PFbyset 2 | True |
| H89 | Storage (MIX Type) | 2 | Default PF line | False |
| H89 | Storage (MIX Type) | 3 | User-defined PF line / UserPFline 4 | True |
| H89 | Storage (MIX Type) | 4 | Under-excited reactive power | False |
| H89 | Storage (MIX Type) | 5 | Over-excited reactive power / OverExcited | True |
| H89 | Storage (MIX Type) | 6 | Q / Q(V) curve | True |
| H89 | Storage (MIX Type) | 7 | Direct control | False |
| H89 | Storage (MIX Type) | 8 | Static capacitive QV | False |
| H89 | Storage (MIX Type) | 9 | Static inductive QV / Static inductive QV. register value None | True |
| H89 | Storage (SPA Type) | 0 | PF / Unity PF | True |
| H89 | Storage (SPA Type) | 1 | Fixed PF setpoint / PFbyset 2 | True |
| H89 | Storage (SPA Type) | 2 | Default PF line | False |
| H89 | Storage (SPA Type) | 3 | User-defined PF line / UserPFline 4 | True |
| H89 | Storage (SPA Type) | 4 | Under-excited reactive power | False |
| H89 | Storage (SPA Type) | 5 | Over-excited reactive power / OverExcited | True |
| H89 | Storage (SPA Type) | 6 | Q / Q(V) curve | True |
| H89 | Storage (SPA Type) | 7 | Direct control | False |
| H89 | Storage (SPA Type) | 8 | Static capacitive QV | False |
| H89 | Storage (SPA Type) | 9 | Static inductive QV / Static inductive QV. register value None | True |
| H89 | Storage (SPH Type) | 0 | PF / Unity PF | True |
| H89 | Storage (SPH Type) | 1 | Fixed PF setpoint / PFbyset 2 | True |
| H89 | Storage (SPH Type) | 2 | Default PF line | False |
| H89 | Storage (SPH Type) | 3 | User-defined PF line / UserPFline 4 | True |
| H89 | Storage (SPH Type) | 4 | Under-excited reactive power | False |
| H89 | Storage (SPH Type) | 5 | Over-excited reactive power / OverExcited | True |
| H89 | Storage (SPH Type) | 6 | Q / Q(V) curve | True |
| H89 | Storage (SPH Type) | 7 | Direct control | False |
| H89 | Storage (SPH Type) | 8 | Static capacitive QV | False |
| H89 | Storage (SPH Type) | 9 | Static inductive QV / Static inductive QV. register value None | True |
| H89 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | PF / Unity PF | True |
| H89 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 1 | Fixed PF setpoint / PFbyset 2 | True |
| H89 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 2 | Default PF line | False |
| H89 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 3 | User-defined PF line / UserPFline 4 | True |
| H89 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 4 | Under-excited reactive power | False |
| H89 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 5 | Over-excited reactive power / OverExcited | True |
| H89 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 6 | Q / Q(V) curve | True |
| H89 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 7 | Direct control | False |
| H89 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 8 | Static capacitive QV | False |
| H89 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 9 | Static inductive QV / Static inductive QV. register value None | True |
| H90 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | idle / unknown | True |
| H90 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | IP read requested / modem OK | True |
| H90 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | no SIM / set IP succeeded | True |
| H90 | TL-X/TL-XH/TL-XH US (MIN Type) | 3 | 0=idle / no network / read | True |
| H90 | TL-X/TL-XH/TL-XH US (MIN Type) | 4 | TCP connect fail | False |
| H90 | TL-X/TL-XH/TL-XH US (MIN Type) | 5 | TCP connected | False |
| H90 | TL-X/TL-XH/TL-XH US (MIN Type) | 7 | 0=unknown / GPRSstatus Bit 0-3 | True |
| H90 | MOD TL3-XH | 0 | idle / unknown | True |
| H90 | MOD TL3-XH | 1 | IP read requested / modem OK | True |
| H90 | MOD TL3-XH | 2 | no SIM / set IP succeeded | True |
| H90 | MOD TL3-XH | 3 | 0=idle / no network / read | True |
| H90 | MOD TL3-XH | 4 | TCP connect fail | False |
| H90 | MOD TL3-XH | 5 | TCP connected | False |
| H90 | MOD TL3-XH | 7 | 0=unknown / GPRSstatus Bit 0-3 | True |
| H90 | Storage (MIX Type) | 0 | idle / unknown | True |
| H90 | Storage (MIX Type) | 1 | IP read requested / modem OK | True |
| H90 | Storage (MIX Type) | 2 | no SIM / set IP succeeded | True |
| H90 | Storage (MIX Type) | 3 | 0=idle / no network / read | True |
| H90 | Storage (MIX Type) | 4 | TCP connect fail | False |
| H90 | Storage (MIX Type) | 5 | TCP connected | False |
| H90 | Storage (MIX Type) | 7 | 0=unknown / GPRSstatus Bit 0-3 | True |
| H90 | Storage (SPA Type) | 0 | idle / unknown | True |
| H90 | Storage (SPA Type) | 1 | IP read requested / modem OK | True |
| H90 | Storage (SPA Type) | 2 | no SIM / set IP succeeded | True |
| H90 | Storage (SPA Type) | 3 | 0=idle / no network / read | True |
| H90 | Storage (SPA Type) | 4 | TCP connect fail | False |
| H90 | Storage (SPA Type) | 5 | TCP connected | False |
| H90 | Storage (SPA Type) | 7 | 0=unknown / GPRSstatus Bit 0-3 | True |
| H90 | Storage (SPH Type) | 0 | idle / unknown | True |
| H90 | Storage (SPH Type) | 1 | IP read requested / modem OK | True |
| H90 | Storage (SPH Type) | 2 | no SIM / set IP succeeded | True |
| H90 | Storage (SPH Type) | 3 | 0=idle / no network / read | True |
| H90 | Storage (SPH Type) | 4 | TCP connect fail | False |
| H90 | Storage (SPH Type) | 5 | TCP connected | False |
| H90 | Storage (SPH Type) | 7 | 0=unknown / GPRSstatus Bit 0-3 | True |
| H90 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | idle / unknown | True |
| H90 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 1 | IP read requested / modem OK | True |
| H90 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 2 | no SIM / set IP succeeded | True |
| H90 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 3 | 0=idle / no network / read | True |
| H90 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 4 | TCP connect fail | False |
| H90 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 5 | TCP connected | False |
| H90 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 7 | 0=unknown / GPRSstatus Bit 0-3 | True |
| H122 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | DisableexportLimit | False |
| H122 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | Enable485exportLimit | False |
| H122 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | Enable232exportLimit | False |
| H122 | TL-X/TL-XH/TL-XH US (MIN Type) | 3 | EnableCTexportLimit | False |
| H122 | MOD TL3-XH | 0 | DisableexportLimit | False |
| H122 | MOD TL3-XH | 1 | Enable485exportLimit | False |
| H122 | MOD TL3-XH | 2 | Enable232exportLimit | False |
| H122 | MOD TL3-XH | 3 | EnableCTexportLimit | False |
| H122 | Storage (MIX Type) | 0 | DisableexportLimit | False |
| H122 | Storage (MIX Type) | 1 | Enable485exportLimit | False |
| H122 | Storage (MIX Type) | 2 | Enable232exportLimit | False |
| H122 | Storage (MIX Type) | 3 | EnableCTexportLimit | False |
| H122 | Storage (SPA Type) | 0 | DisableexportLimit | False |
| H122 | Storage (SPA Type) | 1 | Enable485exportLimit | False |
| H122 | Storage (SPA Type) | 2 | Enable232exportLimit | False |
| H122 | Storage (SPA Type) | 3 | EnableCTexportLimit | False |
| H122 | Storage (SPH Type) | 0 | DisableexportLimit | False |
| H122 | Storage (SPH Type) | 1 | Enable485exportLimit | False |
| H122 | Storage (SPH Type) | 2 | Enable232exportLimit | False |
| H122 | Storage (SPH Type) | 3 | EnableCTexportLimit | False |
| H122 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | DisableexportLimit | False |
| H122 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 1 | Enable485exportLimit | False |
| H122 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 2 | Enable232exportLimit | False |
| H122 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 3 | EnableCTexportLimit | False |
| H124 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | Independent / Independent 1 | True |
| H124 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | DCSource | False |
| H124 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | Parallel / Parallel register value None | True |
| H124 | MOD TL3-XH | 0 | Independent / Independent 1 | True |
| H124 | MOD TL3-XH | 1 | DCSource | False |
| H124 | MOD TL3-XH | 2 | Parallel / Parallel register value None | True |
| H124 | Storage (MIX Type) | 0 | Independent / Independent 1 | True |
| H124 | Storage (MIX Type) | 1 | DCSource | False |
| H124 | Storage (MIX Type) | 2 | Parallel / Parallel register value None | True |
| H124 | Storage (SPA Type) | 0 | Independent / Independent 1 | True |
| H124 | Storage (SPA Type) | 1 | DCSource | False |
| H124 | Storage (SPA Type) | 2 | Parallel / Parallel register value None | True |
| H124 | Storage (SPH Type) | 0 | Independent / Independent 1 | True |
| H124 | Storage (SPH Type) | 1 | DCSource | False |
| H124 | Storage (SPH Type) | 2 | Parallel / Parallel register value None | True |
| H124 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | Independent / Independent 1 | True |
| H124 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 1 | DCSource | False |
| H124 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 2 | Parallel / Parallel register value None | True |

#### Bitfields

| Address | Source identity | Bits | Field | Description | Status |
| --- | --- | --- | --- | --- | --- |
| H0 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| H1 | TL-X/TL-XH/TL-XH US (MIN Type) | [0] | SPI enable | System protection interface enable. | structured |
| H1 | TL-X/TL-XH/TL-XH US (MIN Type) | [1] | AutoTestStart | Automatic test start. | structured |
| H1 | TL-X/TL-XH/TL-XH US (MIN Type) | [2] | LVFRT enable | Low-voltage ride-through enable. | structured |
| H1 | TL-X/TL-XH/TL-XH US (MIN Type) | [3] | FreqDerating Enable | Frequency derating enable. | structured |
| H1 | TL-X/TL-XH/TL-XH US (MIN Type) | [4] | Softstart enable | Soft-start enable. | structured |
| H1 | TL-X/TL-XH/TL-XH US (MIN Type) | [5] | DRMS enable | Demand-response management enable. | structured |
| H1 | TL-X/TL-XH/TL-XH US (MIN Type) | [6] | PowerVoltFunc Enable | Power/voltage function enable. | structured |
| H1 | TL-X/TL-XH/TL-XH US (MIN Type) | [7] | HVFRT enable | High-voltage ride-through enable. | structured |
| H1 | TL-X/TL-XH/TL-XH US (MIN Type) | [8] | ROCOF enable | Rate-of-change-of-frequency protection enable. | structured |
| H1 | TL-X/TL-XH/TL-XH US (MIN Type) | [9] | Recover FreqDeratingMode Enable | Recovery frequency-derating mode enable. | structured |
| H1 | TL-X/TL-XH/TL-XH US (MIN Type) | [10] | Split phase enable | Split-phase enable. | structured |
| H1 | TL-X/TL-XH/TL-XH US (MIN Type) | [11, 15] | Reserved | Reserved by the vendor. | structured |
| H1 | MOD TL3-XH | [0, 3] | forCEI0-21 Bit4~6:forSAA register value | forCEI0-21 Bit4~6:forSAA register value | structured |
| H1 | Storage (MIX Type) | [0, 3] | forCEI0-21 Bit4~6:forSAA register value | forCEI0-21 Bit4~6:forSAA register value | structured |
| H1 | Storage (SPA Type) | [0, 3] | forCEI0-21 Bit4~6:forSAA register value | forCEI0-21 Bit4~6:forSAA register value | structured |
| H1 | Storage (SPH Type) | [0, 3] | forCEI0-21 Bit4~6:forSAA register value | forCEI0-21 Bit4~6:forSAA register value | structured |
| H1 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 3] | forCEI0-21 Bit4~6:forSAA register value | forCEI0-21 Bit4~6:forSAA register value | structured |
| H90 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 3] | 0=idle, 1=IP read requested, 2=set IP succeeded | 0=idle, 1=IP read requested, 2=set IP succeeded | structured |
| H90 | TL-X/TL-XH/TL-XH US (MIN Type) | [4, 7] | 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. register value | 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. register value | structured |
| H90 | MOD TL3-XH | [0, 3] | 0=idle, 1=IP read requested, 2=set IP succeeded | 0=idle, 1=IP read requested, 2=set IP succeeded | structured |
| H90 | MOD TL3-XH | [4, 7] | 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. register value | 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. register value | structured |
| H90 | Storage (MIX Type) | [0, 3] | 0=idle, 1=IP read requested, 2=set IP succeeded | 0=idle, 1=IP read requested, 2=set IP succeeded | structured |
| H90 | Storage (MIX Type) | [4, 7] | 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. register value | 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. register value | structured |
| H90 | Storage (SPA Type) | [0, 3] | 0=idle, 1=IP read requested, 2=set IP succeeded | 0=idle, 1=IP read requested, 2=set IP succeeded | structured |
| H90 | Storage (SPA Type) | [4, 7] | 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. register value | 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. register value | structured |
| H90 | Storage (SPH Type) | [0, 3] | 0=idle, 1=IP read requested, 2=set IP succeeded | 0=idle, 1=IP read requested, 2=set IP succeeded | structured |
| H90 | Storage (SPH Type) | [4, 7] | 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. register value | 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. register value | structured |
| H90 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 3] | 0=idle, 1=IP read requested, 2=set IP succeeded | 0=idle, 1=IP read requested, 2=set IP succeeded | structured |
| H90 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [4, 7] | 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. register value | 0=unknown, 1=modem OK, 2=no SIM, 3=no network, 4=TCP connect fail, 5=TCP connected, etc. register value | structured |

<a id="block-cb-holding-p016-second_group-block-02"></a>
### Second group

- **Vendor heading:** Second group
- **Normalized role:** not normalized (unresolved_ordinal_label)
- **Table / function:** Holding / FC03
- **Address range:** H125–H660
- **Applicable families / models:** MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) (models not specified)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 16–27; 182 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H125 | Inverter type identifier | Reserved | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H126 | Inverter type identifier | Reserved for factory diagnostics; not currently surfaced by the Home Assistant integration. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H127 | Inverter type identifier | Reserved for factory diagnostics; not currently surfaced by the Home Assistant integration. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H128 | Inverter type identifier | Reserved for factory diagnostics; not currently surfaced by the Home Assistant integration. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H129 | Inverter type identifier | Reserved for factory diagnostics; not currently surfaced by the Home Assistant integration. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H130 | Inverter type identifier | Reserved for factory diagnostics; not currently surfaced by the Home Assistant integration. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H131 | Inverter type identifier | Reserved for factory diagnostics; not currently surfaced by the Home Assistant integration. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H132 | Inverter type identifier | Reserved for factory diagnostics; not currently surfaced by the Home Assistant integration. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H133 | Bootloader identifier string | Reserved | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H134 | Bootloader identifier string | Reserved | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H135 | Bootloader identifier string | Reserved | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H136 | Bootloader identifier string | Reserved | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H137 | Reactive power direct-control setpoint (high word) | Positive values command inductive (lagging) vars; negative values request capacitive (leading) vars. | read_write | register value | — | 0.1var | 0.1var | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H138 | Reactive power direct-control setpoint (low word) | Positive values command inductive (lagging) vars; negative values request capacitive (leading) vars. | read_write | register value | — | 0.1var | 0.1var | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H139 | Reactive priority enable | 0：disable 1：enable | read_write | register value | — | 0/1 | 0/1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H140 | Reactive priority ratio | Tune together with the direct-control setpoint to limit how much active power is sacrificed for reactive support. | read_write | register value | — | 0.1 | 0.1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| — | — | — | — | — | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | UNRESOLVED |
| H141 | Night reactive support (SVG) | 0：disable 1：enable | read_write | register value | — | 0/1 | 0/1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H142 | Frequency-watt boost start | Pair with registers 151, 175, and 176 to set the under-frequency support profile. | read_write | register value | — | 0.01H Z | 0.01H | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H143 | Over-frequency recovery point | Works with registers 154-155 and the recovery delay in register 144. | read_write | register value | — | 0.01H Z | 0.01H | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H144 | Over-frequency recovery delay | OFDerate RecoverDelayTime | read_write | register value | — | 50ms | 0000 50ms | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H145 | Zero-current detection enable | Disable only when local interconnection rules explicitly forbid the zero-current method. | read_write | register value | — | — | -1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H146 | Zero-current low voltage | ZeroCurrent StaticlowVolt | read_write | register value | — | 0.1V | 6-230V 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H147 | Zero-current high voltage | ZeroCurrent StaticHighVolt | read_write | register value | — | 0.1V | 30-276V 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H148 | High-voltage derate start | HVoltDerateHighPoint | read_write | register value | — | 0.1V | -1000V 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H149 | High-voltage derate end | Configure together with register 148 to define the slope of the derating curve. | read_write | register value | — | 0.1V | 0-1000V 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H150 | Q(V) stabilisation time | QVPowerStableTime | read_write | register value | — | 0.1S | 0-60S    0.1S | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H151 | Frequency-watt boost stop | Defines the end point of the frequency-watt boost region together with register 142. | read_write | register value | — | 0.01H Z | 0.01H | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H152 | CEI under-frequency ramp start | CEI | read_write | register value | — | 0.01Hz | 6.00-50. 0.01Hz | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H153 | CEI under-frequency ramp end | CEI | read_write | register value | — | 0.01Hz | 0.01Hz 49.10 C | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H154 | CEI over-frequency ramp start | CEI | read_write | register value | — | 0.01Hz | 52. 0.01Hz 50.2 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H155 | CEI over-frequency ramp end | CEI | read_write | register value | — | 0.01Hz | 52. 0.01Hz 51.5 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H156 | CEI undervoltage ramp start | CEI | read_write | register value | — | 0.1V | 00 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H157 | CEI undervoltage ramp end | CEI | read_write | register value | — | 0.1V | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H158 | CEI overvoltage ramp start | CEI | read_write | register value | — | 0.1V | 160-300 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H159 | CEI overvoltage ramp end | CEI | read_write | register value | — | 0.1V | 160-300 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H160 | Nominal grid voltage selection | UL | read_write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H161 | Grid watt restoration delay | UL | read_write | register value | — | 20ms | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H162 | Reconnect ramp slope | UL | read_write | register value | — | 0.1 | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H163 | LFRT stage 1 frequency | UL | read_write | register value | — | 0.01Hz | 5500~650 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H164 | LFRT stage 1 duration | UL | read_write | register value | — | 20ms | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H165 | LFRT stage 2 frequency | UL | read_write | register value | — | 0.01Hz | 5500~650 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H166 | LFRT stage 2 duration | UL | read_write | register value | — | 20ms | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H167 | HFRT stage 1 frequency | UL | read_write | register value | — | 0.01Hz | 5500~650 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H168 | HFRT stage 1 duration | UL | read_write | register value | — | 20ms | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H169 | HFRT stage 2 frequency | UL | read_write | register value | — | 0.01Hz | 500~650 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H170 | HFRT stage 2 duration | UL | read_write | register value | — | 20ms | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H171 | HVRT stage 1 voltage | UL | read_write | register value | — | 0.001 Un | 0.001 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H172 | HVRT stage 1 duration | UL | read_write | register value | — | 20ms | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H173 | HVRT stage 2 voltage | UL | read_write | register value | — | 0.001 Un | 0.001 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H174 | HVRT stage 2 duration | UL | read_write | register value | — | 0.001 Un | 0.001 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H175 | Under-frequency boost delay | 50549 | read_write | register value | — | 50ms | s         50ms | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H176 | Under-frequency boost rate | 50549 | read_write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H177 | Grid restart high-frequency limit | 50549 | read_write | register value | — | 0.01Hz | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H178 | Over-frequency derate response time | Growatt documentation implies steps of roughly 0.1 s; confirm on-site before changing. | read_write | register value | — | — | 00 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H179 | Under-frequency boost response time | Steps are vendor-defined; treat as a tuning knob for the frequency-watt boost ramp rate. | read_write | register value | — | — | 00 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H180 | Meter link status | 0:Missed,1:Received | read_write | register value | — | — | 0 = Missed; 1 = Received / Received register value None | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H181 | Optimizer count | Thetotalnumberofoptimizers connectedtotheinverter | read_write | register value | — | — | -64 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H182 | Optimizer configuration flag | 0x00:Notconfiguredsuccess 0x01:Configurationiscomplete | read_write | register value | — | — | 0 = Notconfiguredsuccess 0x01 / Notconfiguredsuccess 0x01:Configurationiscomplete register value None | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H183 | PV string scan mode | 0：Notsupport Other：PvStringNum | read_write | register value | — | — | 、8、16、 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H184 | BDC parallel count | ThenumberofBDCs | read_write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H185 | Battery pack count | Totalnumberofbattery | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H186 | Reserved | No documented function. | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | RESERVED |
| H187 | VPP function enable status | 0：Disable | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H188 | Datalogger server status | 0：connectionsucceeded | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| — | — | — | — | — | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | UNRESOLVED |
| H200 | PID control reserved | Reserved | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | RESERVED |
| H201 | PID operating mode | 0=Automatic on demand, 1=Continuous, 2=All-night forced run. | write | register value | — | — | W   0:; 0 = Automatic on demand; 1 = Continuous; 2 = All-night forced run / All-night forced run. register value None | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H202 | PID breaker control | Leave enabled unless servicing the PID circuit. | write | register value | — | — | W   0:On | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H203 | PID output voltage setpoint | PID Output voltage option | write | register value | — | V | W   300~1000 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| — | — | — | — | — | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | UNRESOLVED |
| H209 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H210 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H211 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H212 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H213 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H214 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H215 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H216 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H217 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H218 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H219 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H220 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H221 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H222 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H223 | Alternate serial number | Used by newer dataloggers; apply via commissioning tools when required. | read | register value | — | ASCII | ASCII | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| — | — | — | — | — | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | UNRESOLVED |
| H229 | Energy calibration factor | 1-1000,(Percentratio) | read_write | register value | — | 0.1% | 0.1% | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H230–H249 | Anti-islanding override | Never disable anti-islanding on a grid-connected installation unless explicitly authorised. | write | register value | — | — | 1 = disable 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H230 | Anti-islanding override | Never disable anti-islanding on a grid-connected installation unless explicitly authorised. | write | register value | — | — | 1; 1 = disable 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H231 | Fan self-test trigger | The inverter clears the flag automatically once the test completes. | write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H232 | Neutral line monitoring enable | EnableNLineofgrid | write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H233 | Hardware warning flags | wCheckHardware Bit0:GFCIBreak; Bit1:SPSDamage Bit8:EepromReadWarni ng Bit9:EEWriteWarning …… | read | register value | — | — | 0 = GFCIBreak; 1 = SPSDamage Bit8; 9 = EEWriteWarning | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H234 | Hardware warning flags (reserved word) | Monitor for future firmware updates. | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H235 | Neutral-to-ground detection | Should remain enabled for safety compliance. | write | register value | — | — | enable | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H236 | Non-standard voltage range | 0=Standard range, 1=Voltage grade 1, 2=Voltage grade 2. | write | register value | — | — | 2; 0 = Standard range; 1 = Voltage grade 1; 2 = Voltage grade 2 / Voltage grade 2. register value None | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H237 | Appointed spec override | Bit 0: Hungary | write | register value | — | Binary | enable Binary 0; 0 = Hungary / Hungary register value Binary | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H238 | Fast MPPT mode | Reserved | write | register value | — | — | 0,1,2 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H239 | Reserved | Reserved | read | register value | — | — | / | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H240 | Commissioning step index | Internal step counter used during factory self-check sequences. Installers should leave this value unchanged. | read_write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H241 | Installer longitude word | Longitude | read_write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| H242 | Installer latitude word | Latitude | read_write | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| — | — | — | — | — | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | UNRESOLVED |
| H303 | — | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H304 | uwAntiBackf Ant | i-backflow failure | read_write | — | — | — | 0-1000      0. | Declared range only | UNRESOLVED |
| H305 | Qloadspeed Reac | tive loading speed R/W 0 | — | — | — | — | 1% | Declared range only | UNRESOLVED |
| H306 | bParallelAnti P | arallelAnti-Backflow | read_write | — | — | — | 0-1 | Declared range only | UNRESOLVED |
| H307 | lowFailureRe Re | sponseTime | — | — | — | — | — | Declared range only | UNRESOLVED |
| H308 | tiBackflowPo we | r | — | — | — | — | — | Declared range only | UNRESOLVED |
| H309 | comm | and | — | — | — | — | — | Declared range only | UNRESOLVED |
| H310 | bGPRSStatus | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H311 | the Q | (V) curve | — | — | — | — | — | Declared range only | UNRESOLVED |
| H312 | uwQmax_Ca The C | apactive Qmax of R/W | — | — | — | — | 0-1000   0. | Declared range only | UNRESOLVED |
| H313 | — | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H314 | bSuperAntiB Sup | erAntiBackflow     R/W | — | — | — | — | — | Declared range only | UNRESOLVED |
| H315 | uwReactiveP Rea | ctivePowerStableTi R/W | — | — | — | — | S | Declared range only | UNRESOLVED |
| H316 | uwQpStable QpSt | ableTime           R/W | — | — | — | — | S | Declared range only | UNRESOLVED |
| H317 | uwPuDerate PuDe | rateTime           R/W | — | — | — | — | S | Declared range only | UNRESOLVED |
| H318 | uwQVModel QV mo | de Q2 set point R/W | — | — | — | — | 0       0.1% | Declared range only | UNRESOLVED |
| H319 | uwQVModel QV mo | de Q3 set point R/W | — | — | — | — | 0       0.1% | Declared range only | UNRESOLVED |
| H320 | bVrefModel Vref | ModelEnable        R/W | — | — | — | — | ref | Declared range only | UNRESOLVED |
| H321 | uwVrefMod VrefM | odelFilterTime     R/W | — | — | — | — | 0       S | Declared range only | UNRESOLVED |
| H322 | uwUserQPM Activ | e power P1 set R/W | — | — | — | — | 0       0.1% | Declared range only | UNRESOLVED |
| H323 | uwUserQPM Activ | e power P2 set R/W | — | — | — | — | 000       0.1% | Declared range only | UNRESOLVED |
| H324 | uwUserQPM Activ | e power P3 set R/W | — | — | — | — | 000       0.1% | Declared range only | UNRESOLVED |
| H325 | uwUserQPM React | ive power Q1 set R/W | — | — | — | — | 00-10 0.1% | Declared range only | UNRESOLVED |
| H326 | uwUserQPM React | ive power Q2 set R/W | — | — | — | — | 00-10 0.1% | Declared range only | UNRESOLVED |
| H327 | uwUserQPM React | ive power Q3 set R/W | — | — | — | — | 00-10 0.1% | Declared range only | UNRESOLVED |
| H328 | uwAcVoltHig AcV | oltHighDeratPower R/W | — | — | — | — | 000       0.1% | Declared range only | UNRESOLVED |
| H329 | — | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H330 | wProtectMo ode | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H331 | uwUnderFU Under | freqUploadZeroP W | — | — | — | — | 0.01H | Declared range only | UNRESOLVED |
| H332 | FreqDerateZ Fre | qDerateZeroPowerP W | — | — | — | — | 0.01H | Declared range only | UNRESOLVED |
| H333 | bFreqDerati Fre | qDeratingStopMode R/W | — | — | — | — | — | Declared range only | UNRESOLVED |
| H334 | bFreqIncreas Fr | eqIncreasingEnable   R/W | — | — | — | — | — | Declared range only | UNRESOLVED |
| H335 | uwFreqIncre Fre | qIncreasingRecover R/W | — | — | — | — | 50ms | Declared range only | UNRESOLVED |
| H336 | uwFreqIncre Fre | qIncreasingEndLow R/W | — | — | — | — | 0.01H | Declared range only | UNRESOLVED |
| H337 | bFreqIncreas Fr | eqIncreasingStopMo R/W | — | — | — | — | — | Declared range only | UNRESOLVED |
| H338 | uwUserQpC User | QP function, R/W | — | — | — | — | 0    0.1% | Declared range only | UNRESOLVED |
| H339 | uwUserQpC User | QP function, R/W | — | — | — | — | 0    0.1% | Declared range only | UNRESOLVED |
| H340 | uwUserQpC User | QP function, R/W | — | — | — | — | 0    0.1% | Declared range only | UNRESOLVED |
| H341 | wUserQpChr User | QP function, R/W | — | — | — | — | -10 0.1% | Declared range only | UNRESOLVED |
| H342 | wUserQpChr User | QP function, R/W | — | — | — | — | -10 0.1% | Declared range only | UNRESOLVED |
| H343 | wUserQpChr User | QP function, R/W | — | — | — | — | -10 0.1% | Declared range only | UNRESOLVED |
| H344 | uwFreqDerat Fre | qDeratingRecoverLo R/W | — | — | — | — | 0.01H | Declared range only | UNRESOLVED |
| H345 | uwFreqIncre Fre | qIncreasingRecover R/W | — | — | — | — | 0.01H | Declared range only | UNRESOLVED |
| — | — | — | — | — | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | UNRESOLVED |
| H532 | TurnOffUnlo Tur | nOffUnloadSpeed      W/R | — | — | — | — | 0            0. | Declared range only | UNRESOLVED |
| H533 | LimitDevice Ant | i-backflow           W/R | — | — | — | — | — | Declared range only | UNRESOLVED |
| H534 | PowerSetOn Powe | r settings in dc     W/R | — | — | — | — | 00 | Declared range only | UNRESOLVED |
| H535 | OUFreqGrad Over | -under-frequency     W/R | — | — | — | — | — | Declared range only | UNRESOLVED |
| H536 | Country Set Cou | ntry settings under W/R | — | — | — | — | For | Declared range only | UNRESOLVED |
| H538 | InterlockEna Th | ree-machine            W | read_write | — | — | — | -2          0：d | Declared range only | UNRESOLVED |
| H539 | OvTemperDe Over | temperature           W | read_write | — | — | — | — | Declared range only | UNRESOLVED |
| H540 | SafetySetPas Sw | itch between           W | read_write | — | — | — | — | Declared range only | UNRESOLVED |
| H541 | AFCI Onoff | AFCI Onoff             W | read_write | — | — | — | 0/0xA       0xA | Declared range only | UNRESOLVED |
| H542 | AfciSelfChec Af | ciSelfCheck            W | read_write | — | — | — | 0：N | Declared range only | UNRESOLVED |
| H543 | AfciReset | AfciReset              W | read_write | — | — | — | 0：N | Declared range only | UNRESOLVED |
| H544 | AFCIValue1 | AFCIThresholdValue     W | read_write | — | — | — | -65000 | Declared range only | UNRESOLVED |
| H545 | AFCIValue2 | AFCIThresholdValue     W | read_write | — | — | — | -65000 | Declared range only | UNRESOLVED |
| H546 | AFCIValue3 | AFCIThresholdValue     W | read_write | — | — | — | -65000 | Declared range only | UNRESOLVED |
| H547 | OverThresho Ove | rThresholdValueMa W/R | — | — | — | — | -255 | Declared range only | UNRESOLVED |
| H548 | AFCIScanTyp | W | read_write | — | — | — | ~4 | Declared range only | UNRESOLVED |
| H549 | PowerVoltSt Pow | erVoltStopModeEn W/R | — | — | — | — | 、1          0：d | Declared range only | UNRESOLVED |
| H550 | VoltWattRec Vol | tage active power      W | read_write | — | — | — | 5000 20ms | Declared range only | UNRESOLVED |
| H551 | HVoltDerate Vol | tage active cut-off    W | read_write | — | — | — | 00-11 | Declared range only | UNRESOLVED |
| H552 | QVTimeExpo QVTi | meExponent            WR | — | — | — | — | Q varie | Declared range only | UNRESOLVED |
| H553 | Volt-Watt | Voltage active V1 point, | — | — | — | — | 11400 | Declared range only | UNRESOLVED |
| H554 | Volt-Watt | Voltage active V2 point, | — | — | — | — | 11400 | Declared range only | UNRESOLVED |
| — | — | — | — | — | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | UNRESOLVED |
| H600 | Var1 | point, | — | — | — | — | regulat | Declared range only | UNRESOLVED |
| H601 | Var2 | point, | — | — | — | — | regulat | Declared range only | UNRESOLVED |
| H602 | Var3 | point, | — | — | — | — | regulat | Declared range only | UNRESOLVED |
| H603 | Var4 | point, | — | — | — | — | regulat | Declared range only | UNRESOLVED |
| H604 | — | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H605 | OPModEner Allow | ed      inverter R/W | — | — | — | — | 0: outp | Declared range only | UNRESOLVED |
| H608 | OneKeySetB One | key to set battery R/W | — | — | — | — | 0: self | Declared range only | UNRESOLVED |
| H609 | PowerOutpu Zero | Power Output | — | — | — | — | 0：Zero | Declared range only | UNRESOLVED |
| H610 | DealDebugP Flag | bit for clearing | — | — | — | — | — | Declared range only | UNRESOLVED |
| H612 | — | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| — | — | — | — | — | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | UNRESOLVED |
| H660 | ReloadCmd M3 re | mote command | — | — | — | — | — | Declared range only | UNRESOLVED |

#### Enum values

| Address | Source identity | Value | Vendor label | Ambiguous |
| --- | --- | --- | --- | --- |
| H180 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | Missed | False |
| H180 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 1 | Received / Received register value None | True |
| H182 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | Notconfiguredsuccess 0x01 / Notconfiguredsuccess 0x01:Configurationiscomplete register value None | True |
| H201 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | Automatic on demand | False |
| H201 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 1 | Continuous | False |
| H201 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 2 | All-night forced run / All-night forced run. register value None | True |
| H230–H249 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 1 | disable 0 | False |
| H230 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 1 | disable 0 | False |
| H233 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | GFCIBreak | False |
| H233 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 1 | SPSDamage Bit8 | False |
| H233 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 9 | EEWriteWarning | False |
| H236 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | Standard range | False |
| H236 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 1 | Voltage grade 1 | False |
| H236 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 2 | Voltage grade 2 / Voltage grade 2. register value None | True |
| H237 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | Hungary / Hungary register value Binary | True |

#### Bitfields

| Address | Source identity | Bits | Field | Description | Status |
| --- | --- | --- | --- | --- | --- |
| H182 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| H231 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| H233 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0] | GFCIBreak | GFCIBreak | structured |
| H233 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [1] | SPSDamage Bit8:EepromReadWarni ng Bit9:EEWriteWarning …… register value | SPSDamage Bit8:EepromReadWarni ng Bit9:EEWriteWarning …… register value | structured |
| H234 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| H237 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0] | Hungary register value | Hungary register value | structured |

<a id="block-cb-holding-p027-six_group_for_storage_power-block-03"></a>
### Six group for Storage Power

- **Vendor heading:** Six group for Storage Power
- **Normalized role:** storage_power_settings
- **Table / function:** Holding / FC03
- **Address range:** H1000–H1249
- **Applicable families / models:** Storage (MIX Type) (models not specified); Storage (SPA Type) (models not specified); Storage (SPH Type) (models not specified)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 27–35; 117 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H1000 | Float charge current limit i | Float charge current limit i | write | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1001 | PF CMD memory state | PF CMD memory state | write | register value | — | 0or1, | 0or1, | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1002 | Battery discharge start voltage | VbatStartF orDischarg e | read_write | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1003 | VbatlowWa rnClr l | VbatlowWa rnClr l | read_write | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1004 | Vbatstopfo rdischarge | Vbatstopfo rdischarge | write | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1005 | Vbat stop forcharge | Shouldstopcharge whenhigherthanthis voltage | write | register value | — | 0.01V | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1006 | Vbat start for discharge | Should not discharge when lower than this voltage | write | register value | — | 0.01V | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1007 | Vbat constant charge | CVvoltage（acid） | write | register value | — | 0.01V | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1008 | EESysInfo.S ysSetEn | SystemEnable | write | register value | — | — | 15 = UnUsed | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1009 | Battemp lower limit d | Batterytemperature lowerlimitfordischarge | write | register value | — | 0.1℃ | 0-200:0- | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1010 | Bat temp upper limit d | Batterytemperature upperlimitfordischarge | write | register value | — | 0.1℃ | 200-1000 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1011 | Bat temp lower limit c | Lowertemperaturelimit | write | register value | — | 0.1℃ | 0-200:0- | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1012 | Bat temp upper limit c | Uppertemperaturelimit | write | register value | — | 0.1℃ | 200-1000 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1013 | uwUnderFr eDischarge DelyTime | UnderFreDelayTime | read | register value | — | 50ms | 0-20 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1014 | BatMdlSeri alNum | SPH4-11Kused | write | register value | — | — | 00:00 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1015 | BatMdlPara llNum | SPH4-11Kused | write | register value | — | — | 00:00 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1016 | DRMS_EN | 0：disable 1：enable | read | register value | — | / | / | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1017 | Bat First Start Time 4 | Higheight:hours Loweight:minutes | read | register value | — | — | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1018 | Bat First Stop Time 4 | Higheight:hours Loweight:minutes | read | register value | — | — | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1019 | BatFirst on/off Switch4 | Batterypriorityenable1 | read | register value | — | — | 0 or 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1020 | Bat First Start Time 5 | Higheight:hours Loweight:minutes | read | register value | — | — | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1021 | BatFirst StopTime 5 | Higheight:hours Loweight:minutes | read | register value | — | — | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1022 | BatFirst on/off Switch5 | Batterypriorityenable1 | read | register value | — | — | 0 or 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1023 | BatFirst StartTime 6 | Higheight:hours Loweight:minutes | read | register value | — | — | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1024 | BatFirst StopTime 6 | Higheight:hours Loweight:minutes | read | register value | — | — | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1025 | BatFirst on/off Switch6 | Batterypriorityenable1 | read | register value | — | — | 0 or 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1026 | GridFirst StartTime | Higheight:hours Loweight:minutes | read | register value | — | — | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1027 | GridFirst StopTime 4 | Higheight:hours Loweight:minutes | read | register value | — | — | 3 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1028 | Grid First Stop Switch4 | Gridpriorityenable | read | register value | — | — | r 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1029 | GridFirst StartTime 5 | Higheight:hours Loweight:minutes | read | register value | — | — | 3 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1030 | GridFirst StopTime 5 | Higheight:hours Loweight:minutes | read | register value | — | — | 3 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1031 | Grid First Stop Switch5 | Gridpriorityenable | read | register value | — | — | r 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1032 | GridFirst StartTime 6 | Higheight:hours Loweight:minutes | read | register value | — | — | 3 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1033 | GridFirst StopTime 6 | Higheight:hours Loweight:minutes | read | register value | — | — | 3 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1034 | Grid First Stop Switch6 | Gridpriorityenable | read | register value | — | — | r 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1035 | BatFirst StartTime 4 | Higheight:hours Loweight:minutes | read | register value | — | — | 3 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1036 | / | Reserve | read | register value | — | / | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1037 | bCTMode | UsetheCTModeto ChooseRFCT\Cable CT\METER | write | register value | — | — | ETER | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1038 | CTAdjust | CTAdjustenable | write | register value | — | — | isable | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1039 | / | Reserve | read | register value | — | / | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1040 | / | / | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1041 | / | / | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1042 | / | / | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1043 | / | / | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1044 | Priority | ForceChrEn/ForceDischr En Load first/bat first /grid first | read | register value | — | — | Load(de | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1045 | / | / | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1046 | / | / | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1047 | AgingTestSt ep Cmd | Commandforagingtest | read | register value | — | — | default | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1048 | Battery type | Batterytypechooseof buck-boostinput | read | register value | — | — | Lithium | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1049 | / | / | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1050 | / | / | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1051 | / | / | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1052 | / | / | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1053 | / | / | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1054 | / | / | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1060 | BuckUpsFunE n | 0:disable 1:enable | read | register value | — | — | 0:d; 0 = disable / disable 1; 1 = enable register value None | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1061 | BuckUPSVoltS et | UPSoutputvoltage | read | register value | — | — | 0:23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1062 | UPSFreqSet | UPSoutputfrequency | read | register value | — | — | 0:50 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| — | / | / | — | — | — | — | / | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | UNRESOLVED |
| H1070 | Grid-first discharge power rate | Discharge Power Rate whenGridFirst | read_write | register value | — | 1% | W   0-10 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1071 | Grid-first stop SOC | Stop Discharge soc when GridFirst | read_write | register value | — | 1% | 0-10 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| — | — | / | — | — | — | — | / | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | UNRESOLVED |
| H1079 | / | / | read | register value | — | / | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1080 | Grid-first slot 1 start | High byte = hour (0-23); low byte = minute (0-59). | read_write | register value | — | hh:mm | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1081 | Grid-first slot 1 stop | High byte = hour (0-23); low byte = minute (0-59). | read_write | register value | — | hh:mm | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1082 | Grid-first slot 1 enable | Enable:1 Disable:0 | read_write | register value | — | — | 0 or | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1083 | Grid-first slot 2 start | High byte = hour (0-23); low byte = minute (0-59). | read_write | register value | — | hh:mm | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1084 | Grid-first slot 2 stop | High byte = hour (0-23); low byte = minute (0-59). | read_write | register value | — | hh:mm | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1085 | Grid-first slot 2 enable | When set from the LCD, this slot can be tied to the Force Discharge command. | read_write | register value | — | — | 0 or | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1086 | Grid-first slot 3 start | High byte = hour (0-23); low byte = minute (0-59). | read_write | register value | — | hh:mm | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1087 | Grid-first slot 3 stop | High byte = hour (0-23); low byte = minute (0-59). | read_write | register value | — | hh:mm | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1088 | Grid-first slot 3 enable | Enable:1 Disable:0 | read_write | register value | — | — | 0 or | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1089 | / | / | read | register value | — | / | / | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | RESERVED |
| H1090 | Battery-first charge power rate | Charge Power Rate when BatFirst | read_write | register value | — | 1% | -100 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1091 | Battery-first stop SOC | Stop Charge soc when Bat First | read_write | register value | — | 1% | -100 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1092 | Battery-first AC charge enable | WhenBatFirst Enable:1 Disable:0 | read_write | register value | — | — | nable:1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| — | — | — | — | — | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | UNRESOLVED |
| H1099 | Register 1099 | — | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1100 | Battery-first slot 1 start | High byte = hour (0-23); low byte = minute (0-59). | read_write | register value | — | hh:mm | -23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1101 | Battery-first slot 1 stop | High byte = hour (0-23); low byte = minute (0-59). | read_write | register value | — | hh:mm | -23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1102 | Battery-first slot 1 enable | Enable:1 Disable:0 | read_write | register value | — | — | or 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1103 | Battery-first slot 2 start | High byte = hour (0-23); low byte = minute (0-59). | read_write | register value | — | hh:mm | -23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1104 | Battery-first slot 2 stop | High byte = hour (0-23); low byte = minute (0-59). | read_write | register value | — | hh:mm | -23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1105 | Battery-first slot 2 enable | Enable:1 Disable:0 | read_write | register value | — | — | or 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1106 | Battery-first slot 3 start | High byte = hour (0-23); low byte = minute (0-59). | read_write | register value | — | hh:mm | -23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1107 | Battery-first slot 3 stop | High byte = hour (0-23); low byte = minute (0-59). | read_write | register value | — | hh:mm | -23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1108 | Battery-first slot 3 enable | Enable:1 Disable:0 | read_write | register value | — | — | or 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1109 | / | reserve | read | register value | — | / | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | RESERVED |
| H1110 | Load-first slot 1 start | SPA/reserve | read_write | register value | — | hh:mm | -23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | RESERVED |
| H1111 | Load-first slot 1 stop | SPA/reserve | read_write | register value | — | hh:mm | -23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | RESERVED |
| H1112 | Load-first slot 1 enable | SPA/reserve | read_write | register value | — | — | or 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | RESERVED |
| H1113 | Load-first slot 2 start | SPA/reserve | read_write | register value | — | hh:mm | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | RESERVED |
| H1114 | Load-first slot 2 stop | SPA/reserve | read_write | register value | — | hh:mm | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | RESERVED |
| H1115 | Load-first slot 2 enable | SPA/reserve | read_write | register value | — | — | 0 or 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | RESERVED |
| H1116 | Load-first slot 3 start | SPA/reserve | read_write | register value | — | hh:mm | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | RESERVED |
| H1117 | Load-first slot 3 stop | SPA/reserve | read_write | register value | — | hh:mm | 0-23 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | RESERVED |
| H1118 | Load-first slot 3 enable | SPA/reserve | read_write | register value | — | — | 0 or 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | RESERVED |
| H1119 | Energy calculation formula | 0：Theoldformula 1 ： The new formula | read_write | register value | — | / | / | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1120 | Backup enable | MIXUS | read_write | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| H1121 | SGIP enable | MIXUS | read_write | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| — | 1124 | / | — | — | — | — | / | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | UNRESOLVED |
| H1125 | the | first PACK of energy | — | — | — | — | — | Declared range only | UNRESOLVED |
| H1126 | — | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H1127 | — | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H1128 | — | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H1129 | — | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H1130 | — | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H1131 | — | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H1132 | — | — | — | — | — | — | — | Declared range only | UNRESOLVED |
| H8–H1132 | Nominal PV voltage | NormalworkPV voltage | read | register value, unsigned | divisor=10 | 0.1V | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| — | — | — | — | — | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | UNRESOLVED |
| H1244 | Com version Na | me of the battery main | — | — | — | — | — | Declared range only | UNRESOLVED |
| H1245 | Com version Na | me of the battery main | — | — | — | — | — | Declared range only | UNRESOLVED |
| H1246 | Com      versi | on Version of the battery | — | — | — | — | — | Declared range only | UNRESOLVED |
| H1247 | Com version Na | me       of | — | — | — | — | ry | Declared range only | UNRESOLVED |
| H1248 | Com version Na | me       of | — | — | — | — | ry | Declared range only | UNRESOLVED |
| H1249 | Com      versi | on Battery         monito | — | — | — | — | — | Declared range only | UNRESOLVED |

#### Enum values

| Address | Source identity | Value | Vendor label | Ambiguous |
| --- | --- | --- | --- | --- |
| H1008 | Storage (MIX Type) | 15 | UnUsed | False |
| H1008 | Storage (SPA Type) | 15 | UnUsed | False |
| H1008 | Storage (SPH Type) | 15 | UnUsed | False |
| H1060 | Storage (MIX Type) | 0 | disable / disable 1 | True |
| H1060 | Storage (MIX Type) | 1 | enable register value None | False |
| H1060 | Storage (SPA Type) | 0 | disable / disable 1 | True |
| H1060 | Storage (SPA Type) | 1 | enable register value None | False |
| H1060 | Storage (SPH Type) | 0 | disable / disable 1 | True |
| H1060 | Storage (SPH Type) | 1 | enable register value None | False |

<a id="block-cb-holding-p035-use_for_tl_x_and_tl_xh-block-04"></a>
### Use for TL-X and TL-XH

- **Vendor heading:** Use for TL-X and TL-XH
- **Normalized role:** tl_x_tl_xh_registers
- **Table / function:** Holding / FC03
- **Address range:** H3000–H3124
- **Applicable families / models:** TL-X/TL-XH/TL-XH US (MIN Type) (MIN 6000TL-XH); MOD TL3-XH (models not specified)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 35–42; 108 source rows and 26 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H3000 | Export-limit fallback cap | Thepowerrate whenexportLimit failed | read_write | register value, unsigned | divisor=10 | 0.1% | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3001 | Serial Number | Thenewmodel usesthefollowing registerstorecord theserialnumber; The representationis thesameasthe original:one registerholdstwo charactersandthe newserialnumber is30characters. | read_write | serial_number | divisor=10 | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3002 | Serial Number | Serialnumber3-4 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3003 | Serial Number | Serialnumber5-6 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3004 | Serial Number | Serialnumber7-8 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3005 | Serial Number | Serialnumber9-10 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3006 | Serial Number | Serialnumber11-12 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3007 | Serial Number | Serialnumber13-14 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3008 | Serial Number | Serialnumber15-16 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3009 | Serial Number | Serialnumber17-18 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3010 | Serial Number | Serialnumber19-20 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3011 | Serial Number | Serialnumber21-22 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3012 | Serial Number | Serialnumber23-24 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3013 | Serial Number | Serialnumber25-26 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3014 | Serial Number | Serialnumber27-28 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3015 | Serial Number | Serialnumber29-30 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3016 | Dry-contact enable | DryContact functionenable | read_write | register value, unsigned | — | — | :Disable | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3017 | Dry-contact close threshold | The power rate of drycontactturnon | read_write | register value | — | 0.1% | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3018 | Hybrid work mode | MIN2.5~6KTL-XH/ XADoubleCT special | read_write | register value, unsigned | — | — | R/W; 0 = default; 1 = SystemRetrofit2 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3019 | Dry-contact release threshold | Drycontact closurepowerpe rcentage | read_write | register value | — | 0~100 0 | Dry | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3020 | Off-grid box control | Leave at factory value unless instructed by Growatt support. | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3021 | External off-grid enable | 0x00: Disable; （default） 0x01:Enable; | read_write | register value, unsigned | — | — | 0 = Disable; 1 = Enable | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3022 | BDC stop-work bus voltage | BdcStopWorkOfBusVolt | read | register value | — | V | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3023 | Grid topology selection | MIN2.5~6KTL-XH/ XADoubleCT special | read_write | register value, unsigned | — | — | R/W; 0 = SinglePhase 1; 2 = SplitPhase MIN2 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3024 | Float-charge current limit | CCcurrent | read_write | register value, unsigned | divisor=10 | 0.1A | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3025 | Battery-low warning setpoint | Leadacidbattery LVvoltage | read_write | register value | — | 0.1V | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3026 | Battery-low warning clear | Clearbatterylow voltageerror voltagepoint LoadPercent(only lead-Acid): 45.5V(Load< 20%); 48.0V(20%<=Load <=50%); 49.0V(Load> 50%); | read_write | register value | — | 0.1V | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3027 | Battery discharge cutoff | Shouldstop dischargewhen lowerthanthis voltage(only lead-Acid): 46.0V(Load< 20%); 44.8V(20%<=Load <=50%); 44.2V(Load> 50%); | read_write | register value | — | 0.1V | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3028 | Battery charge stop voltage | Shouldstop chargewhen higherthanthis voltage | read_write | register value, unsigned | divisor=100 | 0.01V | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3029 | Battery discharge start voltage | Shouldnot dischargewhen lowerthanthis voltage | read_write | register value, unsigned | divisor=100 | 0.01V | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3030 | Battery constant-charge voltage | CVvoltage（acid） canchargewhen lowerthanthis voltage | read_write | register value, unsigned | divisor=100 | 0.01V | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3031 | Discharge low temperature limit | 0-200:0-20℃ 1000-1400： -40-0℃ | read_write | register value, unsigned | divisor=10 | 0.1℃ | R/W; 200 = 0-20℃ 1000-1400： -40-0℃ register value 0.1℃ | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3032 | Discharge high temperature limit | Batterytemperatureupper limitfordischarge | read_write | register value, unsigned | divisor=10 | 0.1℃ | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3033 | Charge low temperature limit | Battery temperaturelower limit 0-200:0-20℃ 1000-1400： -40-0℃ | read_write | register value, unsigned | divisor=10 | 0.1℃ | R/W; 200 = 0-20℃ 1000-1400： -40-0℃ register value 0.1℃ | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3034 | Charge high temperature limit | Battery temperature upperlimit | read_write | register value, unsigned | divisor=10 | 0.1℃ | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3035 | Under-frequency discharge delay | UnderFreDelay Time | read_write | register value | — | 50ms | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3036 | Grid-first discharge power rate | Grid-first discharge power rate | read_write | u16 percentage; 255 disables limit, unsigned | scale=1, multiplier=1 | % | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3037 | Grid-first stop SOC | Grid-first stop SOC | read_write | u16 percentage, unsigned | scale=1, multiplier=1 | % | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3038 | Grid-first schedule 1 start/control | Grid-first schedule 1 start/control | read_write | packed u16: minute/hour/priority/enable | — | — | R/W; 0 = loadpriority / prohibited; 1 = batterypriority / enabled; 2 = Gridpriority; 6 = minute/hour/priority/enable None; 7 = minutes; 12 = hour | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3039 | Grid-first schedule 1 end | Grid-first schedule 1 end | read_write | packed u16: minute/hour | — | — | R/W; 6 = minute/hour None; 7 = minutes; 12 = hour; 15 = reserved; 15 = reserved / reserved register value None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3040 | Grid-first schedule 2 start/control | Grid-first schedule 2 start/control | read_write | packed u16: minute/hour/priority/enable | — | — | R/W; 0 = loadpriority / prohibited; 1 = batterypriority; 2 = Gridpriority; 6 = minute/hour/priority/enable None; 7 = minutes; 12 = hour; 1 = batterypriority / register value None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3041 | Grid-first schedule 2 end | Grid-first schedule 2 end | read_write | packed u16: minute/hour | — | — | 6 = minute/hour None; 7 = minutes; 12 = hour; 15 = reserved; 15 = reserved / reserved register value W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3042 | Grid-first schedule 3 start/control | Grid-first schedule 3 start/control | read_write | packed u16: minute/hour/priority/enable | — | — | 6 = minute/hour/priority/enable None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3043 | Grid-first schedule 3 end | Grid-first schedule 3 end | read_write | packed u16: minute/hour | — | — | 6 = minute/hour None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3044 | Grid-first schedule 4 start/control | Grid-first schedule 4 start/control | read_write | packed u16: minute/hour/priority/enable | — | — | 6 = minute/hour/priority/enable None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3045 | Grid-first schedule 4 end | Grid-first schedule 4 end | read_write | packed u16: minute/hour | — | — | 6 = minute/hour None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3046 | Reserved | Reserved | read | u16 raw, unsigned | — | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3047 | Battery-first charge power rate | Battery-first charge power rate | read_write | u16 percentage, unsigned | scale=1, multiplier=1 | % | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3048 | Battery-first stop SOC | Battery-first stop SOC | read_write | u16 percentage, unsigned | scale=1, multiplier=1 | % | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3049 | AC charging enabled | AC charge enabled | read_write | u16 enum 0=disabled, 1=enabled, unsigned | scale=1, multiplier=1 | — | 0 = disabled; 1 = enabled None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3050 | Battery-first schedule 1 start/control | Battery-first schedule 1 start/control | read_write | packed u16: minute/hour/priority/enable | — | — | 6 = minute/hour/priority/enable None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3051 | Battery-first schedule 1 end | Battery-first schedule 1 end | read_write | packed u16: minute/hour | — | — | 6 = minute/hour None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3052 | Battery-first schedule 2 start/control | Battery-first schedule 2 start/control | read_write | packed u16: minute/hour/priority/enable | — | — | 6 = minute/hour/priority/enable None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3053 | Battery-first schedule 2 end | Battery-first schedule 2 end | read_write | packed u16: minute/hour | — | — | 6 = minute/hour None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3054 | Battery-first schedule 3 start/control | Battery-first schedule 3 start/control | read_write | packed u16: minute/hour/priority/enable | — | — | 6 = minute/hour/priority/enable None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3055 | Battery-first schedule 3 end | Battery-first schedule 3 end | read_write | packed u16: minute/hour | — | — | 6 = minute/hour None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3056 | Battery-first schedule 4 start/control | Battery-first schedule 4 start/control | read_write | packed u16: minute/hour/priority/enable | — | — | 6 = minute/hour/priority/enable None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3057 | Battery-first schedule 4 end | Battery-first schedule 4 end | read_write | packed u16: minute/hour | — | — | 6 = minute/hour None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3058 | Battery-first schedule 5 start/control | Battery-first schedule 5 start/control | read_write | packed u16: minute/hour/priority/enable | — | — | 6 = minute/hour/priority/enable None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3059 | Battery-first schedule 5 end | Battery-first schedule 5 end | read_write | packed u16: minute/hour | — | — | 6 = minute/hour None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3060–H3069 | Reserved | Reserved | read | register value, unsigned | divisor=10 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| H3070 | Battery type | Batterytype 0:Lithium 1:Lead-acid 2:other | read_write | register value, unsigned | divisor=10 | kWh | 0 = Lithium / Lithium 1; 1 = Lead-acid; 2 = other / other register value kWh | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3071 | BatMdlSeria/ ParalNum | BatMdlSeria/Paral Num; SPH4-11Kused Theupper8bits indicatethe numberofseries segments； Thelower8bits indicatethe numberofparallel sections; | read_write | register value, unsigned | divisor=10 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3072 | Reserved | Reserved | read | register value, unsigned | divisor=10 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| H3073 | Reserved | Reserved | read | register value, unsigned | divisor=10 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| H3074 | Reserved | Reserved | read | register value, unsigned | divisor=10 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| H3075 | Reserved | Reserved | read | register value, unsigned | divisor=10 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| H3076 | Reserved | Reserved | read | register value, unsigned | divisor=10 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| H3077 | Reserved | Reserved | read | register value, unsigned | divisor=10 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| H3078 | Reserved | Reserved | read | register value, unsigned | divisor=10 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| H3079 | UPS/EPS function enable | UPS/EPS function enable | read_write | u16 enum 0=disabled, 1=enabled, unsigned | — | — | 0 = disable 1 / disabled; 1 = enabled None; 0 = disable / disable 1; 1 = enable register value bool | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3080 | UPS/EPS voltage selection | UPS/EPS voltage selection | read_write | u16 enum 0=230 V, 1=208 V, 2=240 V, unsigned | — | V | 0 = 230 V; 1 = 208 V; 2 = 240 V; 0 = 230V; 1 = 208V; 2 = 240V register value V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3081 | UPS/EPS frequency selection | UPS/EPS frequency selection | read_write | u16 enum 0=50 Hz, 1=60 Hz, unsigned | — | Hz | 0 = 50 Hz; 1 = 60 Hz; 0 = 50Hz; 1 = 60Hz register value Hz | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3082 | Load-first stop SOC | Load-first stop SOC | read_write | u16 percentage, unsigned | — | % | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3083 | Reserved | Reserved | read | register value, unsigned | divisor=10 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| H3084 | Reserved | Reserved | read | register value, unsigned | divisor=10 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| H3085 | BDC/BMS RS485 communication address | RS485 communication address of the BDC/BMS battery system on the SYS COM battery interface. | read_write | register value | — | — | default 1; 1..254; 1 = Communication addr / Communication addr=1 1~254: Communication addr=1~254 register value None; 254 = Communication addr | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3086 | BDC/BMS RS485 baud-rate selector | Baud-rate selector for inverter-to-BDC/BMS RS485 communication on the SYS COM battery interface. | read_write | register value | — | — | default 0; 0 = 9600bps; 1 = 38400bps register value None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3087 | Battery rack serial | Forbattery | read_write | register value | — | ASCII | ASC | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3088 | Battery rack serial | SerialNumber3-4 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3089 | Battery rack serial | SerialNumber5-6 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3090 | Battery rack serial | SerialNumber7-8 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3091 | Battery rack serial | SerialNumber9-10 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3092 | Battery rack serial | SerialNumber11-12 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3093 | Battery rack serial | SerialNumber13-14 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3094 | Battery rack serial | SerialNumber15-16 | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3095 | BDC reset command | 0：Invaliddata 1：Resetsetting parameters 2：Resetcorrection parameter 3：Clearhistorical power | read_write | register value, unsigned | — | — | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3096 | BDC monitoring code | ZEBA | read | register value | — | ASCII | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3097 | BDC monitoring code | Four-character identifier for the BDC monitoring firmware (e.g. ZEBA). | read | register value | — | ASCII | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3098 | BDC DTC code | DTC | read | register value | — | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3099 | DSP firmware code | DSPsoftwarecode | read | register value | — | ASCII | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3100 | DSP firmware code | Identifier for the inverter DSP firmware build. | read | register value | — | ASCII | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3101 | DSP firmware version | DSPSoftwareVersion | read | register value | — | ASCII | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3102 | Bus voltage reference | MinimumBUSvoltagefor charginganddischarging batteries | read | register value | — | V | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3103 | BDC monitor firmware | BDCmonitoringsoftware version | read | register value | — | ASCII | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3104 | BMS MCU hardware version | BMS hardware version information | read | register value | — | ASCII | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3105 | BMS firmware version | BMSsoftwareversion information | read | register value | — | ASCII | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3106 | BMS manufacturer | BMSManufacturerName | read | register value | — | ASCII | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3107 | BMS communication interface | BMSCommunicati oninterfacetype： 0:RS485; 1:CAN; | read | register value, unsigned | — | — | 0 = RS485; 1 = CAN | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3108 | BDC module identifier 4 | SxxBxx | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3109 | BDC module identifier 3 | DxxTxx | read_write | register value | — | ASCII | R/W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3110 | BDC module identifier 2 | PxxUxx | read_write | register value | — | ASCII | R/W &*1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3111 | BDC module identifier 1 | Mxxxx | read_write | register value | — | ASCII | R/W &*1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3112 | Reserved | Reserved; reported as zero on known firmware. | read | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| H3113 | BDC protocol version | Bit8-bit15The majorversion numberranges from0-256.In principle,itcannot bechanged Bit0-bit7Minor versionnumber [0-256].Ifthe protocolis changed,youneed toupdatethis version No. | read | register value | — | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |
| H3114 | BDC certification version | BDCCertificationVer | read | register value | — | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | ENRICHED |

#### Enum values

| Address | Source identity | Value | Vendor label | Ambiguous |
| --- | --- | --- | --- | --- |
| H3018 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | default | False |
| H3018 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | SystemRetrofit2 | False |
| H3018 | MOD TL3-XH | 0 | default | False |
| H3018 | MOD TL3-XH | 1 | SystemRetrofit2 | False |
| H3018 | Storage (MIX Type) | 0 | default | False |
| H3018 | Storage (MIX Type) | 1 | SystemRetrofit2 | False |
| H3021 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | Disable | False |
| H3021 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | Enable | False |
| H3021 | MOD TL3-XH | 0 | Disable | False |
| H3021 | MOD TL3-XH | 1 | Enable | False |
| H3021 | Storage (MIX Type) | 0 | Disable | False |
| H3021 | Storage (MIX Type) | 1 | Enable | False |
| H3023 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | SinglePhase 1 | False |
| H3023 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | SplitPhase MIN2 | False |
| H3023 | MOD TL3-XH | 0 | SinglePhase 1 | False |
| H3023 | MOD TL3-XH | 2 | SplitPhase MIN2 | False |
| H3023 | Storage (MIX Type) | 0 | SinglePhase 1 | False |
| H3023 | Storage (MIX Type) | 2 | SplitPhase MIN2 | False |
| H3031 | TL-X/TL-XH/TL-XH US (MIN Type) | 200 | 0-20℃ 1000-1400： -40-0℃ register value 0.1℃ | False |
| H3031 | MOD TL3-XH | 200 | 0-20℃ 1000-1400： -40-0℃ register value 0.1℃ | False |
| H3031 | Storage (MIX Type) | 200 | 0-20℃ 1000-1400： -40-0℃ register value 0.1℃ | False |
| H3033 | TL-X/TL-XH/TL-XH US (MIN Type) | 200 | 0-20℃ 1000-1400： -40-0℃ register value 0.1℃ | False |
| H3033 | MOD TL3-XH | 200 | 0-20℃ 1000-1400： -40-0℃ register value 0.1℃ | False |
| H3033 | Storage (MIX Type) | 200 | 0-20℃ 1000-1400： -40-0℃ register value 0.1℃ | False |
| H3038 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | loadpriority / prohibited | True |
| H3038 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | batterypriority / enabled | True |
| H3038 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | Gridpriority | False |
| H3038 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour/priority/enable None | False |
| H3038 | TL-X/TL-XH/TL-XH US (MIN Type) | 7 | minutes | False |
| H3038 | TL-X/TL-XH/TL-XH US (MIN Type) | 12 | hour | False |
| H3038 | MOD TL3-XH | 0 | loadpriority / prohibited | True |
| H3038 | MOD TL3-XH | 1 | batterypriority / enabled | True |
| H3038 | MOD TL3-XH | 2 | Gridpriority | False |
| H3038 | MOD TL3-XH | 7 | minutes | False |
| H3038 | MOD TL3-XH | 12 | hour | False |
| H3038 | Storage (MIX Type) | 0 | loadpriority / prohibited | True |
| H3038 | Storage (MIX Type) | 1 | batterypriority / enabled | True |
| H3038 | Storage (MIX Type) | 2 | Gridpriority | False |
| H3038 | Storage (MIX Type) | 7 | minutes | False |
| H3038 | Storage (MIX Type) | 12 | hour | False |
| H3039 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour None | False |
| H3039 | TL-X/TL-XH/TL-XH US (MIN Type) | 7 | minutes | False |
| H3039 | TL-X/TL-XH/TL-XH US (MIN Type) | 12 | hour | False |
| H3039 | TL-X/TL-XH/TL-XH US (MIN Type) | 15 | reserved | False |
| H3039 | MOD TL3-XH | 7 | minutes | False |
| H3039 | MOD TL3-XH | 12 | hour | False |
| H3039 | MOD TL3-XH | 15 | reserved / reserved register value None | True |
| H3039 | Storage (MIX Type) | 7 | minutes | False |
| H3039 | Storage (MIX Type) | 12 | hour | False |
| H3039 | Storage (MIX Type) | 15 | reserved / reserved register value None | True |
| H3040 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | loadpriority / prohibited | True |
| H3040 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | batterypriority | False |
| H3040 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | Gridpriority | False |
| H3040 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour/priority/enable None | False |
| H3040 | TL-X/TL-XH/TL-XH US (MIN Type) | 7 | minutes | False |
| H3040 | TL-X/TL-XH/TL-XH US (MIN Type) | 12 | hour | False |
| H3040 | MOD TL3-XH | 0 | loadpriority / prohibited | True |
| H3040 | MOD TL3-XH | 1 | batterypriority / register value None | True |
| H3040 | MOD TL3-XH | 2 | Gridpriority | False |
| H3040 | MOD TL3-XH | 7 | minutes | False |
| H3040 | MOD TL3-XH | 12 | hour | False |
| H3041 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour None | False |
| H3041 | TL-X/TL-XH/TL-XH US (MIN Type) | 7 | minutes | False |
| H3041 | TL-X/TL-XH/TL-XH US (MIN Type) | 12 | hour | False |
| H3041 | TL-X/TL-XH/TL-XH US (MIN Type) | 15 | reserved | False |
| H3041 | MOD TL3-XH | 7 | minutes | False |
| H3041 | MOD TL3-XH | 12 | hour | False |
| H3041 | MOD TL3-XH | 15 | reserved / reserved register value W | True |
| H3041 | Storage (MIX Type) | 7 | minutes | False |
| H3041 | Storage (MIX Type) | 12 | hour | False |
| H3041 | Storage (MIX Type) | 15 | reserved / reserved register value W | True |
| H3042 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour/priority/enable None | False |
| H3043 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour None | False |
| H3044 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour/priority/enable None | False |
| H3045 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour None | False |
| H3049 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | disabled | False |
| H3049 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | enabled None | False |
| H3050 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour/priority/enable None | False |
| H3051 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour None | False |
| H3052 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour/priority/enable None | False |
| H3053 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour None | False |
| H3054 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour/priority/enable None | False |
| H3055 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour None | False |
| H3056 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour/priority/enable None | False |
| H3057 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour None | False |
| H3058 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour/priority/enable None | False |
| H3059 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | minute/hour None | False |
| H3070 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | Lithium / Lithium 1 | True |
| H3070 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | Lead-acid | False |
| H3070 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | other / other register value kWh | True |
| H3070 | MOD TL3-XH | 0 | Lithium / Lithium 1 | True |
| H3070 | MOD TL3-XH | 1 | Lead-acid | False |
| H3070 | MOD TL3-XH | 2 | other / other register value kWh | True |
| H3070 | Storage (MIX Type) | 0 | Lithium / Lithium 1 | True |
| H3070 | Storage (MIX Type) | 1 | Lead-acid | False |
| H3070 | Storage (MIX Type) | 2 | other / other register value kWh | True |
| H3079 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | disable 1 / disabled | True |
| H3079 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | enabled None | False |
| H3079 | MOD TL3-XH | 0 | disable / disable 1 | True |
| H3079 | MOD TL3-XH | 1 | enable register value bool | False |
| H3079 | Storage (MIX Type) | 0 | disable / disable 1 | True |
| H3079 | Storage (MIX Type) | 1 | enable register value bool | False |
| H3080 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | 230 V | False |
| H3080 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | 208 V | False |
| H3080 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | 240 V | False |
| H3080 | MOD TL3-XH | 0 | 230V | False |
| H3080 | MOD TL3-XH | 1 | 208V | False |
| H3080 | MOD TL3-XH | 2 | 240V register value V | False |
| H3080 | Storage (MIX Type) | 0 | 230V | False |
| H3080 | Storage (MIX Type) | 1 | 208V | False |
| H3080 | Storage (MIX Type) | 2 | 240V register value V | False |
| H3081 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | 50 Hz | False |
| H3081 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | 60 Hz | False |
| H3081 | MOD TL3-XH | 0 | 50Hz | False |
| H3081 | MOD TL3-XH | 1 | 60Hz register value Hz | False |
| H3081 | Storage (MIX Type) | 0 | 50Hz | False |
| H3081 | Storage (MIX Type) | 1 | 60Hz register value Hz | False |
| H3085 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | Communication addr / Communication addr=1 1~254: Communication addr=1~254 register value None | True |
| H3085 | TL-X/TL-XH/TL-XH US (MIN Type) | 254 | Communication addr | False |
| H3085 | MOD TL3-XH | 1 | Communication addr / Communication addr=1 1~254: Communication addr=1~254 register value None | True |
| H3085 | MOD TL3-XH | 254 | Communication addr | False |
| H3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | 9600bps | False |
| H3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | 38400bps register value None | False |
| H3086 | MOD TL3-XH | 0 | 9600bps | False |
| H3086 | MOD TL3-XH | 1 | 38400bps register value None | False |
| H3107 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | RS485 | False |
| H3107 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | CAN | False |
| H3107 | MOD TL3-XH | 0 | RS485 | False |
| H3107 | MOD TL3-XH | 1 | CAN | False |
| H3107 | Storage (MIX Type) | 0 | RS485 | False |
| H3107 | Storage (MIX Type) | 1 | CAN | False |

#### Bitfields

| Address | Source identity | Bits | Field | Description | Status |
| --- | --- | --- | --- | --- | --- |
| H3038 | MOD TL3-XH | [0, 7] | minutes | minutes | structured |
| H3038 | MOD TL3-XH | [8, 12] | hour | hour | structured |
| H3038 | Storage (MIX Type) | [0, 7] | minutes | minutes | structured |
| H3038 | Storage (MIX Type) | [8, 12] | hour | hour | structured |
| H3039 | MOD TL3-XH | [0, 7] | minutes | minutes | structured |
| H3039 | MOD TL3-XH | [8, 12] | hour | hour | structured |
| H3039 | MOD TL3-XH | [13, 15] | reserved register value | reserved register value | structured |
| H3039 | Storage (MIX Type) | [0, 7] | minutes | minutes | structured |
| H3039 | Storage (MIX Type) | [8, 12] | hour | hour | structured |
| H3039 | Storage (MIX Type) | [13, 15] | reserved register value | reserved register value | structured |
| H3040 | MOD TL3-XH | [0, 7] | minutes | minutes | structured |
| H3040 | MOD TL3-XH | [8, 12] | hour | hour | structured |
| H3041 | MOD TL3-XH | [0, 7] | minutes | minutes | structured |
| H3041 | MOD TL3-XH | [8, 12] | hour | hour | structured |
| H3041 | MOD TL3-XH | [13, 15] | reserved register value | reserved register value | structured |
| H3041 | Storage (MIX Type) | [0, 7] | minutes | minutes | structured |
| H3041 | Storage (MIX Type) | [8, 12] | hour | hour | structured |
| H3041 | Storage (MIX Type) | [13, 15] | reserved register value | reserved register value | structured |

<a id="block-cb-holding-p042-us_machine_type_time_set-block-05"></a>
### US Machine type Time Set

- **Vendor heading:** US Machine type Time Set
- **Normalized role:** time_set
- **Table / function:** Holding / FC03
- **Address range:** H3125–H3249
- **Applicable families / models:** TL-X/TL-XH/TL-XH US (MIN Type) (MIN 6000TL-XH)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 42–47; 64 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H3125 | Us Tou Month Groups | bit0~3:month_L； bit4~7:month_H bit8, 0:disable1：enable Bit9~15:reserve | read_write | register value | — | — | R/W | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3126 | Us Tou Month Groups | WithTimeMonth1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3127 | Us Tou Month Groups | WithTimeMonth1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3128 | Us Tou Month Groups | WithTimeMonth1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3129 | Us Tou Slot Table | bit0~6:min； bit7~11:hour； bit12~14, 0:loadfirst; | read_write | register value | — | — | R/W   [; 0 = loadfirst; 6 = min / min； bit7~11:hour； bit12~14; 11 = hour | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3130 | Us Tou Slot Table | bit0~6:min； bit7~11:hour； bit12-13, 0:Weekday 1:Weekend 2:WeeK bit14~15：reserve | read_write | register value | — | — | 0 = Weekday / Weekday 1; 1 = Weekend; 2 = WeeK bit14 / WeeK bit14~15：reserve register value None; 6 = min / min； bit7~11:hour； bit12-13; 11 = hour | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3131–H3132 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3133–H3134 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3135–H3136 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3137–H3138 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3139–H3140 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3141–H3142 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3143–H3144 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3145–H3146 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3147–H3148 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3149–H3150 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3151–H3152 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3153–H3154 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3155–H3156 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3157–H3158 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3159–H3160 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3161–H3162 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3163–H3164 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3165–H3166 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3167–H3168 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3169–H3170 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3171–H3172 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3173–H3174 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3175–H3176 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3177–H3178 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3179–H3180 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3181–H3182 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3183–H3184 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3185–H3186 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3187–H3188 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3189–H3190 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3191–H3192 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3193–H3194 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3195–H3196 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3197–H3198 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3199–H3200 | Us Tou Slot Table | SameasTime1 （us） | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3201 | Us Tou Special Day 1 | bit0~7:day； bit8~14:month bit15， 0：disable1： enable | read_write | register value | — | — | 7 = day / day； bit8~14:month bit15， 0：disable1： enable register value None; 14 = month bit15 | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3202 | Us Tou Special Day 1 | bit0~6:min； bit7~11:hour； bit12~14, 0:loadfirst; 1:batfirst； 2:gridfirst； 3:anti-reflux bit15, 0:disable; 1:enable; | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3203 | Us Tou Special Day 1 | bit0~6:min； bit7~11:hour； bit12~15：reserve | read_write | register value | — | — | 6 = min / min； bit7~11:hour； bit12~15：reserve register value None; 11 = hour | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3204–H3205 | Us Tou Special Day 1 | Sameas SpecialDay1_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3206–H3207 | Us Tou Special Day 1 | Sameas SpecialDay1_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3208–H3209 | Us Tou Special Day 1 | Sameas SpecialDay1_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3210–H3211 | Us Tou Special Day 1 | Sameas SpecialDay1_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3212–H3213 | Us Tou Special Day 1 | Sameas SpecialDay1_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3214–H3215 | Us Tou Special Day 1 | Sameas SpecialDay1_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3216–H3217 | Us Tou Special Day 1 | Sameas SpecialDay1_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3218–H3219 | Us Tou Special Day 1 | Sameas SpecialDay1_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3220 | Us Tou Special Day 2 | bit0~7:day； bit8~14:month bit15， 0：disable 1：enable | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3221 | Us Tou Special Day 2 | bit0~6:min； bit7~11:hour； bit12~14, 0:loadfirst; 1:batfirst； 2:gridfirst； 3:anti-reflux bit15, 0:disable; 1:enable; | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3222 | Us Tou Special Day 2 | bit0~6:min； bit7~11:hour； bit12~15：reserve | read_write | register value | — | — | 6 = min / min； bit7~11:hour； bit12~15：reserve register value None; 11 = hour | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3223–H3224 | Us Tou Special Day 2 | Sameas SpecialDay2_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3225–H3226 | Us Tou Special Day 2 | Sameas SpecialDay2_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3227–H3228 | Us Tou Special Day 2 | Sameas SpecialDay2_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3229–H3230 | Us Tou Special Day 2 | Sameas SpecialDay2_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3231–H3232 | Us Tou Special Day 2 | Sameas SpecialDay2_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3233–H3234 | Us Tou Special Day 2 | Sameas SpecialDay2_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3235–H3236 | Us Tou Special Day 2 | Sameas SpecialDay2_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3237–H3238 | Us Tou Special Day 2 | Sameas SpecialDay2_Time 1 | read_write | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| H3239–H3249 | Us Tou Reserved Block | Vendor documentation marks these addresses as reserved; observed values remain zero on known firmware. | read_write | register value | — | — | R/W | TL-X/TL-XH/TL-XH US (MIN Type) | RESERVED |

#### Enum values

| Address | Source identity | Value | Vendor label | Ambiguous |
| --- | --- | --- | --- | --- |
| H3129 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | loadfirst | False |
| H3129 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | min / min； bit7~11:hour； bit12~14 | True |
| H3129 | TL-X/TL-XH/TL-XH US (MIN Type) | 11 | hour | False |
| H3130 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | Weekday / Weekday 1 | True |
| H3130 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | Weekend | False |
| H3130 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | WeeK bit14 / WeeK bit14~15：reserve register value None | True |
| H3130 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | min / min； bit7~11:hour； bit12-13 | True |
| H3130 | TL-X/TL-XH/TL-XH US (MIN Type) | 11 | hour | False |
| H3201 | TL-X/TL-XH/TL-XH US (MIN Type) | 7 | day / day； bit8~14:month bit15， 0：disable1： enable register value None | True |
| H3201 | TL-X/TL-XH/TL-XH US (MIN Type) | 14 | month bit15 | False |
| H3203 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | min / min； bit7~11:hour； bit12~15：reserve register value None | True |
| H3203 | TL-X/TL-XH/TL-XH US (MIN Type) | 11 | hour | False |
| H3222 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | min / min； bit7~11:hour； bit12~15：reserve register value None | True |
| H3222 | TL-X/TL-XH/TL-XH US (MIN Type) | 11 | hour | False |

#### Bitfields

| Address | Source identity | Bits | Field | Description | Status |
| --- | --- | --- | --- | --- | --- |
| H3125 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 3] | month_L； bit4~7:month_H bit8, 0:disable1：enable Bit9~15:reserve register value | month_L； bit4~7:month_H bit8, 0:disable1：enable Bit9~15:reserve register value | structured |
| H3129 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 6] | min； bit7~11:hour； bit12~14, 0:loadfirst | min； bit7~11:hour； bit12~14, 0:loadfirst | structured |
| H3130 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 6] | min； bit7~11:hour； bit12-13, 0:Weekday 1:Weekend 2:WeeK bit14~15：reserve register value | min； bit7~11:hour； bit12-13, 0:Weekday 1:Weekend 2:WeeK bit14~15：reserve register value | structured |
| H3201 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 7] | day； bit8~14:month bit15， 0：disable1： enable register value | day； bit8~14:month bit15， 0：disable1： enable register value | structured |
| H3202 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 6] | min； bit7~11:hour； bit12~14, 0:loadfirst | min； bit7~11:hour； bit12~14, 0:loadfirst | structured |
| H3203 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 6] | min； bit7~11:hour； bit12~15：reserve register value | min； bit7~11:hour； bit12~15：reserve register value | structured |
| H3220 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 7] | day； bit8~14:month bit15， 0：disable 1：enable register value | day； bit8~14:month bit15， 0：disable 1：enable register value | structured |
| H3221 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 6] | min； bit7~11:hour； bit12~14, 0:loadfirst | min； bit7~11:hour； bit12~14, 0:loadfirst | structured |
| H3222 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 6] | min； bit7~11:hour； bit12~15：reserve register value | min； bit7~11:hour； bit12~15：reserve register value | structured |

#### Packed fields

| Address | Source identity | Fields |
| --- | --- | --- |
| H3125 | TL-X/TL-XH/TL-XH US (MIN Type) | [{"bits": [0, 3], "name": "month_low", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "month_L"}, {"bits": [4, 7], "name": "month_high", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "month_H"}, {"bits": [8, 8], "name": "enabled", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "enable"}, {"bits": [9, 15], "name": "reserved", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "reserve"}] |
| H3202 | TL-X/TL-XH/TL-XH US (MIN Type) | [{"bits": [0, 6], "name": "minute", "provenance": ["vendor_v124"], "range": "0-59", "status": "source_explicit", "vendor_label": "min"}, {"bits": [7, 11], "name": "hour", "provenance": ["vendor_v124"], "range": "0-23", "status": "source_explicit", "vendor_label": "hour"}, {"bits": [12, 14], "enum": {"0": "load_first", "1": "battery_first", "2": "grid_first", "3": "anti_reflux"}, "name": "priority", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "loadfirst/batfirst/gridfirst/anti-reflux"}, {"bits": [15, 15], "enum": {"0": "disabled", "1": "enabled"}, "name": "enabled", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "enable"}] |
| H3220 | TL-X/TL-XH/TL-XH US (MIN Type) | [{"bits": [0, 7], "name": "day", "provenance": ["vendor_v124"], "range": "0-31", "status": "source_explicit", "vendor_label": "day"}, {"bits": [8, 14], "name": "month", "provenance": ["vendor_v124"], "range": "1-12", "status": "source_explicit", "vendor_label": "month"}, {"bits": [15, 15], "enum": {"0": "disabled", "1": "enabled"}, "name": "enabled", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "enable"}] |
| H3221 | TL-X/TL-XH/TL-XH US (MIN Type) | [{"bits": [0, 6], "name": "minute", "provenance": ["vendor_v124"], "range": "0-59", "status": "source_explicit", "vendor_label": "min"}, {"bits": [7, 11], "name": "hour", "provenance": ["vendor_v124"], "range": "0-23", "status": "source_explicit", "vendor_label": "hour"}, {"bits": [12, 14], "enum": {"0": "load_first", "1": "battery_first", "2": "grid_first", "3": "anti_reflux"}, "name": "priority", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "loadfirst/batfirst/gridfirst/anti-reflux"}, {"bits": [15, 15], "enum": {"0": "disabled", "1": "enabled"}, "name": "enabled", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "enable"}] |

<a id="block-cb-holding-p047-bdc_information_support_up_to_10_parallel_bdc-block-06"></a>
### BDC information (support up to 10 parallel BDC)

- **Vendor heading:** BDC information (support up to 10 parallel BDC)
- **Normalized role:** bdc_information
- **Table / function:** Holding / FC03
- **Address range:** H5000–H5079
- **Applicable families / models:** Declared range only
- **Source / provenance:** vendor_growatt_v124_2020 pp. 47–47; 4 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H5000–H5039 | Bdc Slot 1 Metadata | Repeat for additional BDCs at 40-register strides (5040-5079, 5080-5119, ). Stored as `bdc_metadata_block`. | read_write | register value | — | — | — | Declared range only | ENRICHED |
| H5040–H5079 | — | 2 | — | — | — | — | — | Declared range only | UNRESOLVED |
| — | )*40--- | N | — | — | — | — | — | Declared range only | UNRESOLVED |
| — | )*40 | — | — | — | — | — | — | Declared range only | UNRESOLVED |

### Reserved ranges

| Range | Status | Basis | Meaning | Source |
| --- | --- | --- | --- | --- |
| H3115–H3124 | RESERVED | vendor_explicit_reserved | Vendor-designated reserved range | V1.24 p.42, Use for TL-X and TL-XH; row 3115 ~ 3124 |

## Input registers

<a id="block-cb-input-p047-first_group-block-07"></a>
### First group

- **Vendor heading:** First group
- **Normalized role:** not normalized (unresolved_ordinal_label)
- **Table / function:** Input / FC04
- **Address range:** I0–I124
- **Applicable families / models:** MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) (models not specified); Storage (MIX Type) (models not specified); Storage (SPH Type) (models not specified)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 47–51; 122 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I0 | Inverter operating status | InverterStatus | read | u16 enum, unsigned | scale=1, multiplier=1 | — | 0:waiting,; 0 = waiting; 1 = normal; 3 = fault | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I1 | PV total power | PpvH | read_write | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I2 | PV total power | PpvL | read_write | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I3 | PV1 DC voltage | Vpv1 | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I4 | PV1 DC current | PV1Curr | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1A | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I5 | PV total power | Ppv1H | read_write | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I6 | PV total power | Ppv1L | read_write | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I7 | PV2 DC voltage | Vpv2 | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I8 | PV2 DC current | PV2Curr | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1A | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I9 | PV total power | Ppv2H | read_write | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I10 | PV total power | Ppv2L | read_write | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I11 | PV3 DC voltage | Vpv3 | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I12 | PV3 DC current | PV3Curr | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1A | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I13 | PV total power | Ppv3H | read_write | register value, unsigned | divisor=10 | 0.1W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I14 | PV total power | Ppv3L | read_write | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I15 | PV4 DC voltage | Vpv4 | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I16 | PV4 DC current | PV4Curr | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1A | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I17 | PV total power | Ppv4H | read_write | register value, unsigned | divisor=10 | 0.1W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I18 | PV total power | Ppv4L | read_write | register value, unsigned | divisor=10 | 0.1W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I19 | PV5 DC voltage | Vpv5 | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I20 | PV5 DC current | PV5Curr | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1A | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I21 | PV total power | Ppv5H | read_write | register value, unsigned | divisor=10 | 0.1W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I22 | PV total power | Ppv5L | read_write | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I23 | PV6 DC voltage | Vpv6 | read | register value, unsigned | divisor=10 | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I24 | PV6 DC current | PV6Curr | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | 0.1A | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I25 | PV total power (high word) | PV6inputpower(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I26 | PV total power (low word) | PV6inputpower(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I27 | PV7 DC voltage | PV7voltage | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I28 | PV7 DC current | PV7inputcurrent | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I29 | PV total power (high word) | PV7inputpower(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I30 | PV total power (low word) | PV7inputpower(low) | read | register value, unsigned | divisor=10 | W | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I31 | PV8 DC voltage | PV8voltage | read | register value, unsigned | divisor=10 | V | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I32 | PV8 DC current | PV8inputcurrent | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I33 | PV total power (high word) | PV8inputpower(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I34 | PV total power (low word) | PV8inputpower(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I35 | AC output power (high word) | Outputpower(high) | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I36 | AC output power (low word) | Outputpower(low) | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I37 | Grid frequency | Gridfrequency | read | register value, unsigned | divisor=100 | Hz | 0.01 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I38 | AC phase L1 voltage | Three/singlephasegridvoltage | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I39 | AC phase L1 current | Three/singlephasegridoutputcurrent | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | A | urrent        0.1A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I40 | AC phase L1 power (high word) | Three/single phase grid output watt VA(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | att           0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I41 | AC phase L1 power (low word) | Three/single phase grid output watt VA(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | att           0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I42 | AC phase L2 voltage | Threephasegridvoltage | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I43 | AC phase L2 current | Threephasegridoutputcurrent | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I44 | AC phase L2 power (high word) | Threephasegridoutputpower(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | igh)          0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I45 | AC phase L2 power (low word) | Threephasegridoutputpower(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | ow)           0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I46 | AC phase L3 voltage | Threephasegridvoltage | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I47 | AC phase L3 current | Threephasegridoutputcurrent | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I48 | AC phase L3 power (high word) | Threephasegridoutputpower(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | igh)          0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I49 | AC phase L3 power (low word) | Threephasegridoutputpower(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | ow)           0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I50 | Vac_RS | Threephasegridvoltage | read | register value, unsigned | scale=0.1, multiplier=0.1 | Linevoltage | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I51 | Vac_ST | Threephasegridvoltage | read | register value, unsigned | scale=0.1, multiplier=0.1 | Linevoltage | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I52 | Vac_TR | Threephasegridvoltage | read | register value, unsigned | scale=0.1, multiplier=0.1 | Linevoltage | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I53 | Output energy today (high word) | Todaygenerateenergy(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1k | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I54 | Output energy today (low word) | Todaygenerateenergy(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1k | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I55 | Output energy total (high word) | Totalgenerateenergy(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1k | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I56 | Output energy total (low word) | Totalgenerateenergy(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1k | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I57 | Inverter runtime (high word) | Raw counter counts seconds; divide by 7200 to obtain hours. | read | register value, unsigned | divisor=7200, scale=0.5, multiplier=0.5 | h | 0.5s | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I58 | Inverter runtime (low word) | Raw counter counts seconds; divide by 7200 to obtain hours. | read | register value, unsigned | divisor=7200, scale=0.5, multiplier=0.5 | h | 0.5s | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I59 | PV1 energy today (high word) | PV1Energytoday(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1k | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I60 | PV1 energy today (low word) | PV1Energytoday(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1k | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I61 | PV1 energy total (high word) | PV1Energytotal(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1k | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I62 | PV1 energy total (low word) | PV1Energytotal(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1k | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I63 | PV2 energy today (high word) | PV2Energytoday(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1k | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I64 | PV2 energy today (low word) | PV2Energytoday(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I65 | PV2 energy total (high word) | PV2Energytotal(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I66 | PV2 energy total (low word) | PV2Energytotal(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I67 | PV3 energy today (high word) | PV3Energytoday(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I68 | PV3 energy today (low word) | PV3Energytoday(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I69 | PV3 energy total (high word) | PV3Energytotal(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I70 | PV3 energy total (low word) | PV3Energytotal(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I71 | PV4 energy today (high word) | PV4Energytoday(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I72 | PV4 energy today (low word) | PV4Energytoday(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I73 | PV4 energy total (high word) | PV4Energytotal(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I74 | PV4 energy total (low word) | PV4Energytotal(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I75 | PV5 energy today (high word) | PV5Energytoday(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I76 | PV5 energy today (low word) | PV5Energytoday(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I77 | PV5 energy total (high word) | PV5Energytotal(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I78 | PV5 energy total (low word) | PV5Energytotal(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I79 | PV6 energy today (high word) | PV6Energytoday(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I80 | PV6 energy today (low word) | PV6Energytoday(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I81 | PV6 energy total (high word) | PV6Energytotal(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I82 | PV6 energy total (low word) | PV6Energytotal(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I83 | PV7 energy today (high word) | PV7Energytoday(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I84 | PV7 energy today (low word) | PV7Energytoday(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I85 | PV7 energy total (high word) | PV7Energytotal(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I86 | PV7 energy total (low word) | PV7Energytotal(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I87 | PV8 energy today (high word) | PV8Energytoday(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I88 | PV8 energy today (low word) | PV8Energytoday(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I89 | PV8 energy total (high word) | PV8Energytotal(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I90 | PV8 energy total (low word) | PV8Energytotal(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I91 | PV energy total (high word) | PVEnergytotal(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I92 | PV energy total (low word) | PVEnergytotal(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I93 | Inverter temperature | Invertertemperature | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | °C | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I94 | IPM temperature | TheinsideIPMininverterTemperature | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | °C | rature | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I95 | Boost temperature | Boosttemperature | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | °C | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I96 | Temp4 | Temp4 | read | register value | — | reserved | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | RESERVED |
| I97 | uwBatVolt_DSP | BatVolt_DSP | read | register value | — | BatVolt(DSP) | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I98 | P-bus voltage | PBusinsideVoltage | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I99 | N-bus voltage | NBusinsideVoltage | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I100 | IPF | InverteroutputPFnow | read | register value | — | — | 0-20000 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I101 | Output power percentage | RealOutputpowerPercent | read | register value | divisor=10, scale=1, multiplier=1 | % | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I102 | OPFullwattH (high word) | OutputMaxpowerLimitedhigh | read | register value, unsigned | scale=1, multiplier=1 | W | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I103 | OPFullwattH (low word) | OutputMaxpowerLimitedlow | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I104 | Derating mode | DeratingMode | read | register value | divisor=10, scale=1, multiplier=1 | — | no derate; | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I105 | Fault code | Inverterfaultmaincode | read | register value | divisor=10, scale=1, multiplier=1 | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I106 | Register 106 | — | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I107 | FaultSubcode | Inverterfaultsubcode | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I108 | RemoteCtrlEn | / | read | register value | — | StoragePow er(SPA) | / | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I109 | RemoteCtrlPow er | / | read | register value | — | StoragePow er(SPA) | / | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I110 | Inverter warning bitfield high word | WarningbitH | read | u16 vendor-defined warning bitfield, unsigned | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I111 | Inverter warning subcode | Inverterwarnsubcode | read | u16 vendor-defined warning subcode, unsigned | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I112 | WarnMaincode | Inverterwarnmaincode | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I113 | real Power Percent | realPowerPercent | read | register value | — | MAX | 100           % | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I114 | inv start delay time | invstartdelaytime | read | register value | — | MAX | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I115 | Inverter aggregate fault code | bINVAllFaultCode | read | register value | — | MAX | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I116 | AC charge Power_H (high word) | Gridpowertolocalload | read | register value | — | Storage Power | 0.1k | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I117 | AC charge Power_H (low word) | Gridpowertolocalload | read | register value | — | Storage Power | 0.1k | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I118 | Priority | 0:LoadFirst | read | register value | — | Storage | 0 = LoadFirst / LoadFirst register value Storage | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I119 | Battery type | 0：Lead-acid 1：Lithiumbattery | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I120 | AutoProofreadC MD | Aging mode Auto-calibration command | read | register value | — | — | bration | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | ENRICHED |
| I124 | reserved | reserved | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type); Storage (MIX Type); Storage (SPH Type) | RESERVED |

#### Enum values

| Address | Source identity | Value | Vendor label | Ambiguous |
| --- | --- | --- | --- | --- |
| I0 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | waiting | False |
| I0 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | normal | False |
| I0 | TL-X/TL-XH/TL-XH US (MIN Type) | 3 | fault | False |
| I118 | Storage (MIX Type) | 0 | LoadFirst / LoadFirst register value Storage | True |
| I118 | Storage (SPH Type) | 0 | LoadFirst / LoadFirst register value Storage | True |
| I118 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | LoadFirst / LoadFirst register value Storage | True |

#### Bitfields

| Address | Source identity | Bits | Field | Description | Status |
| --- | --- | --- | --- | --- | --- |
| I110 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |

<a id="block-cb-input-p051-second_group-block-08"></a>
### Second group

- **Vendor heading:** Second group
- **Normalized role:** not normalized (unresolved_ordinal_label)
- **Table / function:** Input / FC04
- **Address range:** I125–I249
- **Applicable families / models:** MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) (models not specified)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 51–56; 125 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I125 | PIDPV1+Voltage | PIDPV1+Voltage | read | register value | — | 0.1V | e         0~1000V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I126 | PIDPV1+Current | PIDPV1+Current | read | register value | — | 0.1mA | -10~10mA | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I127 | PIDPV2+Voltage | PIDPV2+Voltage | read | register value | — | 0.1V | e 0~1000V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I128 | PIDPV2+Current | PIDPV2+Current | read | register value | — | 0.1mA | -10~10mA | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I129 | PIDPV3+Voltage | PIDPV3+Voltage | read | register value | — | 0.1V | e 0~1000V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I130 | PIDPV3+Current | PIDPV3+Current | read | register value | — | 0.1mA | -10~10mA | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I131 | PIDPV4+Voltage | PIDPV4+Voltage | read | register value | — | 0.1V | e 0~1000V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I132 | PIDPV4+Current | PIDPV4+Current | read | register value | — | 0.1mA | -10~10mA | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I133 | PIDPV5+Voltage | PIDPV5+Voltage | read | register value | — | 0.1V | e 0~1000V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I134 | PIDPV5+Current | PIDPV5+Current | read | register value | — | 0.1mA | -10~10mA | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I135 | PIDPV6+Voltage | PIDPV6+Voltage | read | register value | — | 0.1V | e 0~1000V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I136 | PIDPV6+Current | PIDPV6+Current | read | register value | — | 0.1mA | -10~10mA | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I137 | PIDPV7+Voltage | PIDPV7+Voltage | read | register value | — | 0.1V | e 0~1000V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I138 | PIDPV7+Current | PIDPV7+Current | read | register value | — | 0.1mA | -10~10mA | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I139 | PIDPV8+Voltage | PIDPV8+Voltage | read | register value | — | 0.1V | e 0~1000V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I140 | PIDPV8+Current | PIDPV8+Current | read | register value | — | 0.1mA | -10~10mA | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I141 | PIDStatus | PIDStatus | write | register value | — | — | 0~3 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I142 | V_String1 | V_String1 | read | register value | — | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I143 | Curr_String1 | Curr_String1 | read | register value | — | 0.1A | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I144 | V_String2 | V_String2 | read | register value | — | 0.1V | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I145 | Curr_String2 | PVString2current | read | register value | — | — | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I146 | V_String3 | PVString3voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I147 | Curr_String3 | PVString3current | read | register value | — | — | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I148 | V_String4 | PVString4voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I149 | Curr_String4 | PVString4current | read | register value | — | — | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I150 | V_String5 | PVString5voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I151 | Curr_String5 | PVString5current | read | register value | — | — | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I152 | V_String6 | PVString6voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I153 | Curr_String6 | PVString6current | read | register value | — | — | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I154 | V_String7 | PVString7voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I155 | Curr_String7 | PVString7current | read | register value | — | — | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I156 | V_String8 | PVString8voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I157 | Curr_String8 | PVString8current | read | register value | — | — | -15A~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I158 | V_String9 | PVString9voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I159 | Curr_String9 | PVString9current | read | register value | — | — | -15A~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I160 | V_String10 | PVString10voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I161 | Curr_String10 | PVString10current | read | register value | — | — | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I162 | V_String11 | PVString11voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I163 | Curr_String11 | PVString11current | read | register value | — | — | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I164 | V_String12 | PVString12voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I165 | Curr_String12 | PVString12current | read | register value | — | — | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I166 | V_String13 | PVString13voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I167 | Curr_String13 | PVString13current | read | register value | — | — | -15A~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I168 | V_String14 | PVString14voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I169 | Curr_String14 | PVString14current | read | register value | — | — | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I170 | V_String15 | PVString15voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I171 | Curr_String15 | PVString15current | read | register value | — | — | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I172 | V_String16 | PVString16voltage | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I173 | Curr_String16 | PVString16current | read | register value | — | — | -15~15A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I174 | StrUnmatch | Bit0~15:String1~16unmatch | read | register value | — | suggestive | 15 = String1 / String1~16unmatch register value suggestive | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I175 | StrCurrentUnblan ce | Bit0~15:String1~16currentunblance | read | register value | — | suggestive | blance; 15 = String1 / String1~16currentunblance register value suggestive | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I176 | StrDisconnect | Bit0~15:String1~16disconnect | read | register value | — | suggestive | 15 = String1 / String1~16disconnect register value suggestive | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I177 | PIDFaultCode | Bit0:Outputovervoltage Bit1:ISOfault Bit2:BUSvoltageabnormal Bit3~15:reserved | read | register value | — | — | 0 = Outputovervoltage Bit1; 2 = BUSvoltageabnormal Bit3; 15 = reserved / reserved register value None | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I178 | StringPrompt | StringPrompt Bit0:StringUnmatch Bit1:StrDisconnect Bit2:StrCurrentUnblance | read | register value | — | — | 0 = StringUnmatch Bit1; 2 = StrCurrentUnblance | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I179 | PVWarningValue | PVWarningValue | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I180 | DSP075 Warning Value | DSP075WarningValue | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I181 | DSP075 Fault Value | DSP075FaultValue | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I182 | DSP067 Debug Data1 | DSP067DebugData1 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I183 | DSP067 Debug Data2 | DSP067DebugData2 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I184 | DSP067 Debug Data3 | DSP067DebugData3 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I185 | DSP067 Debug Data4 | DSP067DebugData4 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I186 | DSP067 Debug Data5 | DSP067DebugData5 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I187 | DSP067 Debug Data6 | DSP067DebugData6 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I188 | DSP067 Debug Data7 | DSP067DebugData7 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I189 | DSP067 Debug Data8 | DSP067DebugData8 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I190 | DSP075 Debug Data1 | DSP075DebugData1 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I191 | DSP075 Debug Data2 | DSP075DebugData2 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I192 | DSP075 Debug Data3 | DSP075DebugData3 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I193 | DSP075 Debug Data4 | DSP075DebugData4 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I194 | DSP075 Debug Data55 | DSP075DebugData5 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I195 | DSP075 Debug Data6 | DSP075DebugData6 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I196 | DSP075 Debug Data7 | DSP075DebugData7 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I197 | DSP075 Debug Data8 | DSP075DebugData8 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I198 | bUSBAgingTestOk Flag | USBAgingTestOkFlag | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I199 | bFlashEraseAging OkFlag | FlashEraseAgingOkFlag | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I200 | PVISO | PVISOValue | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I201 | R_DCI | RDCICurr | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I202 | S_DCI | SDCICurr | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I203 | T_DCI | TDCICurr | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I204 | PID_Bus | PIDBusVolt | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I205 | GFCI | GFCICurr | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I206 | SVG/APF Status+SVGAPFEq ualRatio | SVG/APFStatus+SVGAPFEqualRatio | write | register value | — | — | o     High 8 bit： | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I207 | CT_I_R | RphaseloadsidecurrentforSVG | read | register value | — | — | SVG | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I208 | CT_I_S | SphaseloadsidecurrentforSVG | read | register value | — | — | SVG | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I209 | CT_I_T | TphaseloadsidecurrentforSVG | read | register value | — | — | SVG | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I210 | CT_Q_RH (high word) | R phase load side output reactive powerforSVG(High) | read | register value | — | — | ive | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I211 | CT_Q_RH (low word) | R phase load side output reactive powerforSVG(low) | read | register value | — | — | ive | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I212 | CT_Q_SH (high word) | S phase load side output reactive powerforSVG(High) | read | register value | — | — | ive | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I213 | CT_Q_SH (low word) | S phase load side output reactive powerforSVG(low) | read | register value | — | — | ive | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I214 | CT_Q_TH (high word) | T phase load side output reactive powerforSVG(High) | read | register value | — | — | ive | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I215 | CT_Q_TH (low word) | T phase load side output reactive powerforSVG(low) | read | register value | — | — | ive | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I216 | CTHAR_I_R | Rphaseloadsideharmonic | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I217 | CTHAR_I_S | Sphaseloadsideharmonic | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I218 | CTHAR_I_T | Tphaseloadsideharmonic | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I219 | COMP_Q_RH (high word) | R phase compensate reactive power forSVG(High) | read | register value | — | — | wer | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I220 | COMP_Q_RH (low word) | R phase compensate reactive power forSVG(low) | read | register value | — | — | wer | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I221 | COMP_Q_SH (high word) | S phase compensate reactive power forSVG(High) | read | register value | — | — | wer | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I222 | COMP_Q_SH (low word) | S phase compensate reactive power | read | register value | — | — | wer | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I223 | COMP_Q_TH (high word) | T phase compensate reactive power forSVG(High) | read | register value | — | — | wer | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I224 | COMP_Q_TH (low word) | T phase compensate reactive power forSVG(low) | read | register value | — | — | wer | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I225 | COMPHAR_I_R | R phase compensate harmonic for SVG | read | register value | — | — | r | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I226 | COMPHAR_I_S | S phase compensate harmonic for SVG | read | register value | — | — | r | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I227 | COMPHAR_I_T | T phase compensate harmonic for SVG | read | register value | — | — | r | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I228 | bRS232AgingTest OkFlag | RS232AgingTestOkFlag | read | register value | — | — | 0-1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I229 | bFanFaultBit | Bit0:Fan1faultbit Bit1:Fan2faultbit Bit2:Fan3faultbit Bit3:Fan4faultbit Bit4-7:Reserved | read | register value | — | — | 0 = Fan1faultbit Bit1; 2 = Fan3faultbit Bit3; 7 = Reserved / Reserved register value None | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I230 | SacH (high word) | OutputapparentpowerH | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I231 | SacH (low word) | OutputapparentpowerL | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I232 | ReActPowerH (high word) | RealOutputReactivePowerH | read | register value | — | — | Int32 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I233 | ReActPowerH (low word) | RealOutputReactivePowerL | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I234 | Output reactive power (high word) | NominalOutputReactivePowerH | read | register value, unsigned | divisor=10 | var | H | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I235 | Output reactive power (low word) | NominalOutputReactivePowerL | read | register value, unsigned | divisor=10 | var | L | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I236 | Reactive energy total (high word) | Reactivepowergeneration | read | register value, unsigned | divisor=10 | kvarh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I237 | Reactive energy total (low word) | Reactivepowergeneration | read | register value, unsigned | divisor=10 | kvarh | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I238 | bAfciStatus | 0：Waiting 1：Self-checkstate 2：Detectpullarcstate 3：Fault 4：Update | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I239 | uwPresentFFTValu e[CHANNEL_A] | PresentFFTValue[CHANNEL_A] | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I240 | uwPresentFFTValu e[CHANNEL_B] | PresentFFTValue[CHANNEL_B] | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I241 | DSP067 Debug Data1 | DSP067DebugData1 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I242 | DSP067 Debug Data2 | DSP067DebugData2 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I243 | DSP067 Debug | DSP067DebugData3 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I244 | DSP067 Debug Data4 | DSP067DebugData4 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I245 | DSP067 Debug Data5 | DSP067DebugData5 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I246 | DSP067 Debug Data6 | DSP067DebugData6 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I247 | DSP067 Debug Data7 | DSP067DebugData7 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I248 | DSP067 Debug Data8 | DSP067DebugData8 | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I249 | Register 249 | — | read | register value | — | reserved | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |

#### Enum values

| Address | Source identity | Value | Vendor label | Ambiguous |
| --- | --- | --- | --- | --- |
| I174 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 15 | String1 / String1~16unmatch register value suggestive | True |
| I175 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 15 | String1 / String1~16currentunblance register value suggestive | True |
| I176 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 15 | String1 / String1~16disconnect register value suggestive | True |
| I177 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | Outputovervoltage Bit1 | False |
| I177 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 2 | BUSvoltageabnormal Bit3 | False |
| I177 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 15 | reserved / reserved register value None | True |
| I178 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | StringUnmatch Bit1 | False |
| I178 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 2 | StrCurrentUnblance | False |
| I229 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 0 | Fan1faultbit Bit1 | False |
| I229 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 2 | Fan3faultbit Bit3 | False |
| I229 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 7 | Reserved / Reserved register value None | True |

#### Bitfields

| Address | Source identity | Bits | Field | Description | Status |
| --- | --- | --- | --- | --- | --- |
| I174 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 15] | String1~16unmatch register value | String1~16unmatch register value | structured |
| I175 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 15] | String1~16currentunblance register value | String1~16currentunblance register value | structured |
| I176 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 15] | String1~16disconnect register value | String1~16disconnect register value | structured |
| I177 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0] | Outputovervoltage Bit1:ISOfault Bit2:BUSvoltageabnormal Bit3~15:reserved register value | Outputovervoltage Bit1:ISOfault Bit2:BUSvoltageabnormal Bit3~15:reserved register value | structured |
| I178 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0] | StringUnmatch Bit1:StrDisconnect Bit2:StrCurrentUnblance register value | StringUnmatch Bit1:StrDisconnect Bit2:StrCurrentUnblance register value | structured |
| I198 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I199 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I228 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I229 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0] | Fan1faultbit Bit1:Fan2faultbit Bit2:Fan3faultbit Bit3:Fan4faultbit Bit4-7:Reserved register value | Fan1faultbit Bit1:Fan2faultbit Bit2:Fan3faultbit Bit3:Fan4faultbit Bit4-7:Reserved register value | structured |

<a id="block-cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09"></a>
### The eighth group for PV9-PV16 information

- **Vendor heading:** The eighth group for PV9-PV16 information
- **Normalized role:** not normalized (unresolved)
- **Table / function:** Input / FC04
- **Address range:** I875–I999
- **Applicable families / models:** MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) (models not specified)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 56–59; 120 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I875 | Vpv9 | PV9 voltage | read | register value | — | — | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I876 | PV9Curr | PV9 Inputcurrent | read | register value | — | — | 0.1A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I877 | Ppv9H (high word) | PV9 inputpower(High) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I878 | Ppv9H (low word) | PV9 inputpower(Low) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I879 | Vpv10 | PV10voltage | read | register value | — | — | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I880 | PV10Curr | PV10Inputcurrent | read | register value | — | — | 0.1A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I881 | Ppv10H (high word) | PV10inputpower(High) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I882 | Ppv10H (low word) | PV10inputpower(Low) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I883 | Vpv11 | PV11voltage | read | register value | — | — | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I884 | PV11Curr | PV11Inputcurrent | read | register value | — | — | 0.1A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I885 | Ppv11H (high word) | PV11inputpower(High) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I886 | Ppv11H (low word) | PV11inputpower(Low) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I887 | Vpv12 | PV12voltage | read | register value | — | — | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I888 | PV12Curr | PV12Inputcurrent | read | register value | — | — | 0.1A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I889 | Ppv12H (high word) | PV12inputpower(High) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I890 | Ppv12H (low word) | PV12inputpower(Low) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I891 | Vpv13 | PV13voltage | read | register value | — | — | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I892 | PV13Curr | PV13Inputcurrent | read | register value | — | — | 0.1A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I893 | Ppv13H (high word) | PV13inputpower(High) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I894 | Ppv13H (low word) | PV13inputpower(Low) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I895 | Vpv14 | PV14voltage | read | register value | — | — | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I896 | PV14Curr | PV14Inputcurrent | read | register value | — | — | 0.1A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I897 | Ppv14H (high word) | PV14inputpower(High) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I898 | Ppv14H (low word) | PV14inputpower(Low) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I899 | Vpv15 | PV15voltage | read | register value | — | — | 0.1V | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I900 | PV15Curr | PV15Inputcurrent | read | register value | — | — | 0.1A | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I901 | Ppv15H (high word) | PV15inputpower(High) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I902 | Ppv15H (low word) | PV15inputpower(Low) | read | register value | — | — | 0.1W | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I903 | Vpv16 | PV16voltage | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I904 | PV16Curr | PV16Inputcurrent | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I905 | Ppv16H (high word) | PV16inputpower(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I906 | Ppv16H (low word) | PV16inputpower(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I907 | Epv9_todayH (high word) | PV9energytoday(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I908 | Epv9_todayH (low word) | PV9energytoday(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I909 | Epv9_totalH (high word) | PV9energytotal(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I910 | Epv9_totalH (low word) | PV9energytotal(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I911 | Epv10_todayH (high word) | PV10energytoday(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I912 | Epv10_todayH (low word) | PV10energytoday(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I913 | Epv10_totalH (high word) | PV10energytotal(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I914 | Epv10_totalH (low word) | PV10energytotal(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I915 | Epv11_todayH (high word) | PV11energytoday(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I916 | Epv11_todayH (low word) | PV11energytoday(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I917 | Epv11_totalH (high word) | PV11energytotal(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I918 | Epv11_totalH (low word) | PV11energytotal(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I919 | Epv12_todayH (high word) | PV12energytoday(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I920 | Epv12_todayH (low word) | PV12energytoday(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I921 | Epv12_totalH (high word) | PV12energytotal(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I922 | Epv12_totalH (low word) | PV12energytotal(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I923 | Epv13_todayH (high word) | PV13energytoday(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I924 | Epv13_todayH (low word) | PV13energytoday(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I925 | Epv13_totalH (high word) | PV13energytotal(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I926 | Epv13_totalH (low word) | PV13energytotal(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I927 | Epv14_todayH (high word) | PV14energytoday(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I928 | Epv14_todayH (low word) | PV14energytoday(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I929 | Epv14_totalH (high word) | PV14energytotal(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I930 | Epv14_totalH (low word) | PV14energytotal(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I931 | Epv15_todayH (high word) | PV15energytoday(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I932 | Epv15_todayH (low word) | PV15energytoday(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I933 | Epv15_totalH (high word) | PV15energytotal(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I934 | Epv15_totalH (low word) | PV15energytotal(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I935 | Epv16_todayH (high word) | PV16energytoday(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I936 | Epv16_todayH (low word) | PV16energytoday(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I937 | Epv16_totalH (high word) | PV16energytotal(High) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I938 | Epv16_totalH (low word) | PV16energytotal(Low) | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I939 | PIDPV9+Voltage | PID PV9PE Volt/ Flyspan voltage (MAXHV) | read | register value | — | — | e 0~1000V        0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I940 | PIDPV9+Current | PIDPV9PECurrent | read | register value | — | — | -10~10mA       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I941 | PID PV10+ Voltage | PID PV10PE/ Flyspan voltage (MAX HV) | read | register value | — | — | AX 0~1000V       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I942 | PID PV10+ Current | PIDPV10PECurrent | read | register value | — | — | -10~10mA       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I943 | PID PV11+ Voltage | PID PV11PE Volt/ Flyspan voltage (MAXHV) | read | register value | — | — | ge 0~1000V       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I944 | PID PV11+ Current | PIDPV11PECurrent | read | register value | — | — | -10~10mA       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I945 | PID PV12+ Voltage | PID PV12PE Volt/ Flyspan voltage (MAXHV) | read | register value | — | — | ge 0~1000V       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I946 | PID PV12+ Current | PIDPV12PECurrent | read | register value | — | — | -10~10mA       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I947 | PID PV13+ Voltage | PID PV13PE Volt/ Flyspan voltage (MAXHV) | read | register value | — | — | ge 0~1000V       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I948 | PID PV13+ Current | PIDPV13PECurrent | read | register value | — | — | -10~10mA       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I949 | PID PV14+ Voltage | PID PV14PE Volt/ Flyspan voltage (MAXHV) | read | register value | — | — | ge 0~1000V       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I950 | PID PV14+ Current | PIDPV14PECurrent | read | register value | — | — | -10~10mA       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I951 | PID PV15+ Voltage | PID PV15PE Volt/ Flyspan voltage (MAXHV) | read | register value | — | — | ge 0~1000V       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I952 | PID PV15+ Current | PIDPV15PECurrent | read | register value | — | — | -10~10mA       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I953 | PID PV16+ Voltage | PID PV16PE Volt/ Flyspan voltage (MAXHV) | read | register value | — | — | ge 0~1000V       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I954 | PID PV16+ Current | PIDPV16PECurrent | read | register value | — | — | -10~10mA       0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I955 | V_String17 | PVString17voltage | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I956 | Curr_String17 | PVString17Current | read | register value | — | — | -15~15A        0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I957 | V_String18 | PVString18voltage | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I958 | Curr_String18 | PVString18Current | read | register value | — | — | -15~15A        0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I959 | V_String19 | PVString19voltage | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I960 | Curr_String19 | PVString19Current | read | register value | — | — | -15~15A        0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I961 | V_String20 | PVString20voltage | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I962 | Curr_String20 | PVString20Current | read | register value | — | — | -15~15A        0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I963 | V_String21 | PVString21voltage | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I964 | Curr_String21 | PVString21Current | read | register value | — | — | -15~15A        0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I965 | V_String22 | PVString22voltage | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I966 | Curr_String22 | PVString22Current | read | register value | — | — | -15~15A        0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I967 | V_String23 | PVString23voltage | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I968 | Curr_String23 | PVString23Current | read | register value | — | — | -15~15A        0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I969 | V_String24 | PVString24voltage | read | register value | — | — | 0 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I970 | Curr_String24 | 0.1A | read | register value | — | -15A~15A | -15A~1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I971 | V_String25 | 0.1V | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I972 | Curr_String25 | 0.1A | read | register value | — | -15A~15A | -15A~1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I973 | V_String26 | 0.1V | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I974 | Curr_String26 | 0.1A | read | register value | — | -15~15A | -15~15 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I975 | V_String27 | 0.1V | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I976 | Curr_String27 | 0.1A | read | register value | — | -15~15A | -15~15 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I977 | V_String28 | 0.1V | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I978 | Curr_String28 | 0.1A | read | register value | — | -15~15A | -15~15 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I979 | V_String29 | 0.1V | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I980 | Curr_String29 | 0.1A | read | register value | — | -15A~15A | -15A~1 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I981 | V_String30 | 0.1V | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I982 | Curr_String30 | 0.1A | read | register value | — | -15~15A | -15~15 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I983 | V_String31 | 0.1V | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I984 | Curr_String31 | 0.1A | read | register value | — | -15~15A | -15~15 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I985 | V_String32 | 0.1V | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I986 | Curr_String32 | 0.1A | read | register value | — | -15~15A | -15~15 | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I987 | StrUnmatch2 | Bit0~15:String17~32unmatch | read | register value | — | — | 15 = String17 / String17~32unmatch register value None | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I988 | StrCurrentUnblan ce2 | Bit0~15:String 17~32 current unblance | read | register value | — | — | current; 15 = String 17 / String 17~32 current unblance register value None | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I989 | StrDisconnect2 | Bit0~15:String17~32disconnect | read | register value | — | — | ct; 15 = String17 / String17~32disconnect register value None | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I990 | PVWarningValue | PVWarningValue(PV9-PV16) Contains PV9~16 abnormal ， 和 Boost9~16Driveanomalies | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I991 | StrWaringvalue1 | string1~string16abnormal | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| I992 | StrWaringvalue2 | string17~string32abnormal | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |
| — | — | — | — | — | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | UNRESOLVED |
| I999 | SystemCmd | M3toDSPsystemcommand | read | register value | — | — | — | MAX 1500V/MAX-X LV; TL3-X (MAX, MID, MAC Type) | ENRICHED |

#### Enum values

| Address | Source identity | Value | Vendor label | Ambiguous |
| --- | --- | --- | --- | --- |
| I987 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 15 | String17 / String17~32unmatch register value None | True |
| I988 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 15 | String 17 / String 17~32 current unblance register value None | True |
| I989 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | 15 | String17 / String17~32disconnect register value None | True |

#### Bitfields

| Address | Source identity | Bits | Field | Description | Status |
| --- | --- | --- | --- | --- | --- |
| I987 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 15] | String17~32unmatch register value | String17~32unmatch register value | structured |
| I988 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 15] | String 17~32 current unblance register value | String 17~32 current unblance register value | structured |
| I989 | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | [0, 15] | String17~32disconnect register value | String17~32disconnect register value | structured |

<a id="block-cb-input-p059-ninth_group_for_storage_power-block-10"></a>
### Ninth group for Storage power

- **Vendor heading:** Ninth group for Storage power
- **Normalized role:** storage_power_telemetry
- **Table / function:** Input / FC04
- **Address range:** I1000–I1066
- **Applicable families / models:** Storage (MIX Type) (models not specified); Storage (SPA Type) (models not specified); Storage (SPH Type) (models not specified)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 59–62; 67 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I1000 | uwSysWorkMode | uwSysWorkMode | write | register value | — | — | 0x00:waiting | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1001 | Systemfaultword0 | Systemfaultword0 | read | register value | — | Please refer to thefault description of Hybrid | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1002 | Systemfaultword1 | Systemfaultword1 | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1003 | Systemfaultword2 | Systemfaultword2 | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1004 | Systemfaultword3 | Systemfaultword3 | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1005 | Systemfaultword4 | Systemfaultword4 | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1006 | Systemfaultword5 | Systemfaultword5 | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1007 | Systemfaultword6 | Systemfaultword6 | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1008 | Systemfaultword7 | Systemfaultword7 | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1009 | Battery discharge power (high word) | Dischargepower(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1010 | Battery discharge power (low word) | Dischargepower(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1011 | Battery charge power (high word) | Chargepower(high) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1012 | Battery charge power (low word) | Chargepower(low) | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1013 | Vbat | Batteryvoltage | read | register value, unsigned | scale=0.1, multiplier=0.1 | V | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1014 | Battery state of charge | StateofchargeCapacity | read | register value | divisor=10, scale=1, multiplier=1 | lith/leadacid | -100             1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1015 | PactouserR H (high word) | ACpowertouserH | read | register value, unsigned | scale=0.1, multiplier=0.1 | W | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1016 | PactouserR H (low word) | ACpowertouserL | read | register value, unsigned | scale=0.1, multiplier=0.1 | W | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1017 | PactouserS H (high word) | PactouserS H | read | register value | — | — | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1018 | PactouserS H (low word) | PactouserS L | read | register value | — | — | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1019 | PactouserT H (high word) | PactouserT H | read | register value | — | — | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1020 | PactouserT H (low word) | PactouserT H | read | register value | — | — | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1021 | PactouserTotalH (high word) | ACpowertousertotalH | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1022 | PactouserTotalH (low word) | ACpowertousertotalL | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1023 | PactogridR H (high word) | ACpowertogridH | read | register value, unsigned | scale=0.1, multiplier=0.1 | Ac output | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1024 | PactogridR H (low word) | ACpowertogridL | read | register value, unsigned | scale=0.1, multiplier=0.1 | W | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1025 | PactogridS H (high word) | PactogridS H | read | register value | — | — | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1026 | PactogridS H (low word) | PactogridS L | read | register value | — | — | 0 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1027 | PactogridTH | 0.1w | read | register value | — | — | 0.1w | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1028 | PactogridTL | 0.1w | read | register value | — | — | 0.1w | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1029 | pac_to_grid_total | 0.1w | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1w | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1030 | PactogridtotalL | 0.1w | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1w | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1031 | PLocalLoadR H | 0.1w | read | register value, unsigned | scale=0.1, multiplier=0.1 | W | 0.1w | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1032 | PLocalLoadR L | 0.1w | read | register value, unsigned | scale=0.1, multiplier=0.1 | W | 0.1w | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1033 | PLocalLoadS H | 0.1w | read | register value | — | — | 0.1w | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1034 | PLocalLoadS L | 0.1w | read | register value | — | — | 0.1w | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1035 | PLocalLoadT H | 0.1w | read | register value | — | — | 0.1w | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1036 | PLocalLoadT L | 0.1w | read | register value | — | — | 0.1w | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1037 | PLocalLoadtotalH | 0.1w | read | register value, unsigned | scale=0.1, multiplier=0.1 | W | l H    0.1w | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1038 | PLocalLoadtotalL | 0.1w | read | register value, unsigned | scale=0.1, multiplier=0.1 | W | l      0.1w | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1039 | IP2MTemperature | 0.1℃ | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1040 | B2attery Temperature | 0.1℃ | read | register value, unsigned | — | °C | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1041 | SPDSPStatus | SPDSPStatus | read | register value, unsigned | scale=1, multiplier=1 | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1042 | SPBusVolt | 0.1V | read | register value | — | — | 0.1V | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1043 | Register 1043 | — | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1044 | Etouser_todayH (high word) | Etouser_todayH | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1045 | Etouser_todayH (low word) | Etouser_todayL | write | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1046 | Etouser_totalH (high word) | Etouser_totalH | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1047 | Etouser_totalH (low word) | Etouser_totalL | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1048 | Etogrid_todayH (high word) | Etogrid_todayH | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1049 | Etogrid_todayH (low word) | Etogrid_todayL | write | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1050 | Etogrid_totalH (high word) | Etogrid_totalH | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1051 | Etogrid_totalH (low word) | Etogrid_totalL | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1052 | Edischarge1_toda yH (high word) | Edischarge1_toda yH | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1053 | Edischarge1_toda yH (low word) | Edischarge1_toda yL | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1054 | Edischarge1_total H (high word) | Edischarge1_total H | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1055 | Edischarge1_total H (low word) | Edischarge1_total L | write | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1056 | Echarge1_todayH (high word) | Echarge1_todayH | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1057 | Echarge1_todayH (low word) | Echarge1_today L | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1058 | Echarge1_totalH (high word) | Echarge1_totalH | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1059 | Echarge1_totalH (low word) | Echarge1_totalL | read | register value, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1060 | Register 1060 | Localloadenergytoday | read | register value, unsigned | scale=0.1, multiplier=0.1 | kWh | 0.1kW | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1061 | Register 1061 | Localloadenergytoday | read | register value, unsigned | scale=0.1, multiplier=0.1 | kWh | 0.1kW | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1062 | Register 1062 | Localloadenergytotal | read | register value, unsigned | scale=0.1, multiplier=0.1 | kWh | 0.1kW | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1063 | Register 1063 | Localloadenergytotal | read | register value, unsigned | scale=0.1, multiplier=0.1 | kWh | 0.1kW | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1064 | Register 1064 | ExportLimitApparentPowerH | write | register value | — | — | 0.1kW | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1065 | Register 1065 | ExportLimitApparentPowerL | write | register value | — | — | 0.1kW | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1066 | Register 1066 | / | read | register value | — | — | / | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |

<a id="block-cb-input-p062-bms_infomation-block-11"></a>
### BMS Infomation

- **Vendor heading:** BMS Infomation
- **Normalized role:** bms_information
- **Table / function:** Input / FC04
- **Address range:** I1082–I1124
- **Applicable families / models:** Storage (MIX Type) (models not specified); Storage (SPA Type) (models not specified); Storage (SPH Type) (models not specified)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 62–64; 43 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I1082 | Register 1082 | StatusOldfromBMS | read | register value | — | — | etail information, | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1083 | Register 1083 | StatusfromBMS | read | register value | — | — | o | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1084 | Register 1084 | ErrorinfoOldfromBMS | read | register value | — | — | ocument:GrowattxxS | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1085 | Register 1085 | ErrorinfomationfromBMS | read | register value | — | — | ESS Protocol; | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1086 | Register 1086 | SOCfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1087 | Register 1087 | BatteryvoltagefromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1088 | Register 1088 | BatterycurrentfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1089 | Register 1089 | BatterytemperaturefromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1090 | BMS_MaxCurr | Max. charge/discharge current fromBMS(pylon) | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1091 | BMS_GaugeRM | GaugeRMfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1092 | BMS_GaugeFCC | GaugeFCCfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1093 | BMS_FW | BMS_FW | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1094 | BMS_DeltaVolt | DeltaVfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1095 | BMS_CycleCnt | CycleCountfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1096 | BMS_SOH | SOHfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1097 | BMS_ConstantV olt | CVvoltagefromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1098 | BMS_WarnInfoO ld | WarninginfooldfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1099 | BMS_WarnInfo | WarninginfofromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1100 | BMS_GaugeICCu rr | GaugeICcurrentfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1101 | BMS_MCUVersi on | MCUSoftwareversionfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1102 | BMS_GaugeVers ion | GaugeVersionfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1103 | BMS_wGaugeFR Version_L | GaugeFRVersionL16fromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1104 | BMS_wGaugeFR Version_H | GaugeFRVersionH16fromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1105 | BMS_BMSInfo | BMSInformationfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1106 | BMS_PackInfo | PackInformationfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1107 | BMS_UsingCap | UsingCapfromBMS | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1108 | uwMaxCellVolt | Maximumsinglebatteryvoltage | read | register value | — | — | 0.001V | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1109 | uwMinCellVolt | Lowestsinglebatteryvoltage | read | register value | — | — | 0.001V | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1110 | bModuleNum | Batteryparallelnumber | read | register value | — | — | 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1111 | Numberofbatteries | Numberofbatteries | read | register value | — | — | 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1112 | uwMaxVoltCellN o | MaxVoltCellNo | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1113 | uwMinVoltCellN o | MinVoltCellNo | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1114 | uwMaxTemprCe ll_10T | MaxTemprCell_10T | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1115 | uwMinTemprCel l_10T | MinTemprCell_10T | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1116 | uwMaxTemprCe llNo | MaxVoltTemprCellNo | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1117 | uwMinTemprCel | MinVoltTemprCellNo | read | register value | — | — | 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1118 | ProtectpackID | FaultyBatteryAddress | read | register value | — | — | 1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1119 | MaxSOC | ParallelmaximumSOC | read | register value | — | — | 1% | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1120 | MinSOC | ParallelminimumSOC | read | register value | — | — | 1% | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1121 | BMS_Error2 | BatteryProtection2 | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1122 | BMS_Error3 | BatteryProtection3 | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1123 | BMS_WarnInfo2 | BatteryWarn2 | read | register value | — | — | — | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1124 | ACCharge EnergyTodayH | ACChargeEnergytoday | write | register value, unsigned | scale=0.1, multiplier=0.1 | kWh | kwh | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |

<a id="block-cb-input-p062-ups_information_offline-block-12"></a>
### Ups information (offline)

- **Vendor heading:** Ups information (offline)
- **Normalized role:** ups_information
- **Table / function:** Input / FC04
- **Address range:** I1067–I1081
- **Applicable families / models:** Storage (MIX Type) (models not specified); Storage (SPA Type) (models not specified); Storage (SPH Type) (models not specified)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 62–62; 15 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I1067 | EpsFac | UPSfrequency | read | register value | — | — | 000/6000     0.01H | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1068 | EpsVac1 | UPSphaseRoutputvoltage | read | register value | — | — | 300          0.1V | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1069 | EpsIac1 | UPSphaseRoutputcurrent | read | register value | — | — | 0.1A | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1070 | EpsPac1 | UPSphaseRoutputpower(H) | read | register value | — | — | 0.1VA | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1071 | EpsPac1 | UPSphaseRoutputpower(L) | read | register value | — | — | 0.1VA | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1072 | EpsVac2 | UPSphaseSoutputvoltage | read | register value | — | — | 0.1V | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1073 | EpsIac2 | UPSphaseSoutputcurrent | read | register value | — | — | 0.1A | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1074 | EpsPac2 | UPSphaseSoutputpower(H) | read | register value | — | — | 0.1VA | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1075 | EpsPac2 | UPSphaseSoutputpower(L) | read | register value | — | — | 0.1VA | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1076 | EpsVac3 | UPSphaseToutputvoltage | read | register value | — | — | 0.1V | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1077 | EpsIac3 | UPSphaseToutputcurrent | read | register value | — | — | 0.1A | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1078 | EpsPac3 | UPSphaseToutputpower(H) | read | register value | — | — | 0.1VA | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1079 | EpsPac3 | UPSphaseToutputpower(L) | read | register value | — | — | 0.1VA | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1080 | EpsLoadPercent | LoadpercentofUPSouput | read | register value | — | — | -100         1% | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1081 | EpsPF | Powerfactor | read | register value | — | — | -2           0.1 | Storage (MIX Type); Storage (SPA Type); Storage (SPH Type) | ENRICHED |

<a id="block-cb-input-p064-ninth_group_reserved_for_storage_power-block-13"></a>
### Ninth group reserved for storage power

- **Vendor heading:** Ninth group reserved for storage power
- **Normalized role:** storage_power_telemetry_reserved
- **Table / function:** Input / FC04
- **Address range:** I1125–I2124
- **Applicable families / models:** Storage (SPA Type) (models not specified); Storage (SPH Type) (models not specified)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 64–70; 116 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I1125 | ACCharge EnergyTodayH (low word) | ACChargeEnergytoday | write | register value, unsigned | scale=0.1, multiplier=0.1 | kWh | kwh | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1126 | A1CCharge EnergyTotalH | A1CCharge EnergyTotalH | read | register value, unsigned | scale=0.1, multiplier=0.1 | kWh | — | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1127 | ACCharge EnergyTotalL | ACCharge EnergyTotalL | read | register value, unsigned | scale=0.1, multiplier=0.1 | kWh | — | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1128 | AC Charge Power H (high word) | ACChargePower | write | register value | — | — | W | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1129 | AC Charge Power H (low word) | ACChargePower | write | register value | — | — | w | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1130 | 70% INV Power adjust | uwGridPower_70_AdjEE_SP | write | register value | — | — | W | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1131 | Extra AC Power to grid_H (high word) | ExtrainverteACPowertogrid High | read | register value | — | — | For SPA | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1132 | Extra AC Power to grid_H (low word) | ExtrainverteACPowertogridLow | read | register value | — | — | — | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1133 | Eextra_todayH (high word) | ExtrainverterPowerTOUser_Extra today(high) | read | register value | — | 0.1kWh | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1134 | Eextra_todayH (low word) | ExtrainverterPowerTOUser_Extra today(low) | read | register value | — | 0.1kWh | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1135 | Eextra_totalH (high word) | ExtrainverterPowerTOUser_Extra total(high) | read | register value | — | 0.1kWh | — | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1136 | Eextra_totalH (low word) | ExtrainverterPowerTOUser_Extra total(low) | read | register value | — | 0.1kWh | — | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1137 | Esystem_today H (high word) | SystemelectricenergytodayH | read | register value | — | 0.1kWh | — | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1138 | Esystem_today H (low word) | SystemelectricenergytodayL | read | register value | — | SPA used System electric energytodayL | 0.1kWh | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1139 | Esystem_totalH (high word) | SystemelectricenergytotalH | read | register value | — | SPA used System electric energytotalH | 0.1kWh | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1140 | Esystem_totalH (low word) | SystemelectricenergytotalL | read | register value | — | SPA used System electric energytotalL | 0.1kWh | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1141 | Eself_todayH (high word) | selfelectricenergytodayH | read | register value | — | self electric energytodayH | 0.1kWh | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1142 | Eself_todayH (low word) | selfelectricenergytodayL | read | register value | — | self electric energytodayL | 0.1kWh | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1143 | Eself_totalH (high word) | selfelectricenergytotalH | read | register value | — | self electric energytotalH | 0.1kWh | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1144 | Eself_totalH (low word) | selfelectricenergytotalL | read | register value | — | self electric energytotalL | 0.1kWh | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1145 | PSystemH (high word) | SystempowerH | read | register value | — | SystempowerH | 0.1w | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1146 | PSystemH (low word) | SystempowerL | read | register value | — | SystempowerL | 0.1w | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1147 | PSelfH (high word) | selfpowerH | read | register value | — | selfpowerH | 0.1w | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1148 | PSelfH (low word) | selfpowerL | read | register value | — | selfpowerL | 0.1w | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1149 | EPVAll_TodayH (high word) | PVelectricenergytodayH | read | register value | — | — | — | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1150 | EPVAll_TodayH (low word) | PVelectricenergytodayL | read | register value | — | — | — | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1151 | AcDischarge PackSn | Discharge power pack serial number | read | register value | — | — | erial R   / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1152 | Accdischarge power_H (high word) | Cumulative discharge power high 16-bitbyte | read | register value | — | — | R         0.1kWH | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1153 | Accdischarge power_H (low word) | Cumulative discharge power low 16-bitbyte | read | register value | — | — | 0.1kWH | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1154 | AccCharge PackSn | chargepowerpackserialnumber | read | register value | — | — | R    / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1155 | AccCharge power_H (high word) | Cumulative charge power high 16-bitbyte | read | register value | — | — | 0.1kWH | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1156 | AccCharge power_H (low word) | Cumulative charge power low 16-bitbyte | read | register value | — | — | 0.1kWH | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1157 | FirstBattFaultSn | FirstBattFaultSn | read | register value | — | — | / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1158 | Second BattFaultSn | Second BattFaultSn | read | register value | — | — | / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1159 | Third BattFaultSn | Third BattFaultSn | read | register value | — | — | / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1160 | Fourth BattFaultSn | Fourth BattFaultSn | read | register value | — | — | / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1161 | Batteryhistory faultcode1 | Batteryhistoryfaultcode1 | read | register value | — | — | / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1162 | Batteryhistory faultcode2 | Batteryhistoryfaultcode2 | read | register value | — | — | / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1163 | Batteryhistory faultcode3 | Batteryhistoryfaultcode3 | read | register value | — | — | / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1164 | Batteryhistory faultcode4 | Batteryhistoryfaultcode4 | read | register value | — | — | / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1165 | Batteryhistory faultcode5 | Batteryhistoryfaultcode5 | read | register value | — | — | R   / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1166 | Batteryhistory faultcode6 | Batteryhistoryfaultcode6 | read | register value | — | — | R   / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1167 | Batteryhistory faultcode7 | Batteryhistoryfaultcode7 | read | register value | — | — | R   / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1168 | Batteryhistory faultcode8 | Batteryhistoryfaultcode8 | read | register value | — | — | R   / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1169 | Number of battery codes | Number of battery codes PACK number + BIC forward and reversecodes | read | register value | — | — | R   / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1170 | Register 1170 | — | read | register value | — | — | — | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| — | /                    / | — | — | — | — | — | /   / | Storage (SPA Type); Storage (SPH Type) | UNRESOLVED |
| I1199 | NewEPowerCalc Flag | Intelligent reading is used to identify software compatibility features | read | register value | — | 0 ： Old energy calculation； 1 ： new energy calculation | — | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1200 | MaxCellVolt | Maximumcellvoltage | read | register value | — | — | R   0.001V | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1201 | MinCellVolt | Minimumcellvoltage | read | register value | — | — | R   0.001V | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1202 | ModuleNum | NumberofBatterymodules | read | register value | — | — | R   / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1203 | TotalCellNum | Totalnumberofcells | read | register value | — | — | R   / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1204 | MaxVoltCellNo | MaxVoltCellNo | read | register value | — | — | R   / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1205 | MinVoltCellNo | MinVoltCellNo | read | register value | — | — | R   / | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1206 | MaxTemprCell_ 10T | MaxTemprCell_10T | read | register value | — | — | R   0.1℃ | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1207 | MinTemprCell_1 0T | MinTemprCell_10T | read | register value | — | — | R   0.1℃ | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1208 | MaxTemprCellN o | MaxTemprCellNo | read | register value | — | — | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1209 | MinTemprCellN o | MinTemprCellNo | read | register value | — | — | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1210 | ProtectPackID | FaultPackID | read | register value | — | — | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1211 | MaxSOC | ParallelmaximumSOC | read | register value | — | — | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1212 | MinSOC | ParallelminimumSOC | read | register value | — | — | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1213 | BatProtect1Add | BatProtect1Add | read | register value | — | — | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1214 | BatProtect2Add | BatProtect2Add | read | register value | — | — | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1215 | BatWarn1Add | BatWarn1Add | read | register value | — | — | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1216 | BMS_HighestSof tVersion | BMS_HighestSoftVersion | read | register value | — | — | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1217 | BMS_Hardware Version | BMS_HardwareVersion | read | register value | — | — | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1218 | BMS_RequestTy pe | BMS_RequestType | read | register value | — | — | R | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| — | /                    / | — | — | — | — | — | / | Storage (SPA Type); Storage (SPH Type) | UNRESOLVED |
| I1248 | bKeyAgingTestO kFlag | Success sign of key detection beforeaging | read | register value | — | 1：Finishedtest 0 ： test not completed | — | Storage (SPA Type); Storage (SPH Type) | ENRICHED |
| I1249 | / | / | read | register value | — | reversed | / | Storage (SPA Type); Storage (SPH Type) | RESERVED |
| I2000 | InverterStatus | Inverterrunstate | read | register value | — | — | 0:waiting | Storage (SPA Type) | ENRICHED |
| — | reversed | — | — | — | — | — | — | Storage (SPA Type); Storage (SPH Type) | UNRESOLVED |
| I2035 | PacH | Outputpower(high) | read | register value | — | — | — | Storage (SPA Type) | ENRICHED |
| I2036 | PacL | Outputpower(low) | read | register value | — | — | — | Storage (SPA Type) | ENRICHED |
| I2037 | Fac | Gridfrequency | read | register value | — | — | — | Storage (SPA Type) | ENRICHED |
| I2038 | Vac1 | Three/singlephasegridvoltage | read | register value | — | — | — | Storage (SPA Type) | ENRICHED |
| I2039 | Iac1 | Three/singlephasegridoutputcurrent | read | register value | — | — | urrent | Storage (SPA Type) | ENRICHED |
| I2040 | Pac1H | Three/single phase grid output watt VA(high) | read | register value | — | — | att | Storage (SPA Type) | ENRICHED |
| I2041 | Pac1L | Three/single phase grid output watt VA(low) | read | register value | — | — | att | Storage (SPA Type) | ENRICHED |
| — | reversed | — | — | — | — | — | — | Storage (SPA Type); Storage (SPH Type) | UNRESOLVED |
| I2053 | EactodayH | Todaygenerateenergy(high) | read | register value | — | — | — | Storage (SPA Type) | ENRICHED |
| I2054 | EactodayL | Todaygenerateenergy(low) | read | register value | — | — | — | Storage (SPA Type) | ENRICHED |
| I2055 | EactotalH (high word) | Totalgenerateenergy(high) | read | register value | — | SPA | — | Storage (SPA Type) | ENRICHED |
| I2056 | EactotalH (low word) | Totalgenerateenergy(low) | read | register value | — | SPA | — | Storage (SPA Type) | ENRICHED |
| I2057 | TimetotalH (high word) | Worktimetotal(high) | read | register value | — | SPA | — | Storage (SPA Type) | ENRICHED |
| I2058 | TimetotalH (low word) | Worktimetotal(low) | read | register value | — | SPA | — | Storage (SPA Type) | ENRICHED |
| — | reversed | — | — | — | — | — | — | Storage (SPA Type); Storage (SPH Type) | UNRESOLVED |
| I2093 | Temp1 | Invertertemperature | read | register value | — | SPA | — | Storage (SPA Type) | ENRICHED |
| I2094 | Temp2 | TheinsideIPMininverterTemperature | read | register value | — | SPA | rature | Storage (SPA Type) | ENRICHED |
| I2095 | Temp3 | Boosttemperature | read | register value | — | SPA | — | Storage (SPA Type) | ENRICHED |
| I2096 | Temp4 | Temp4 | read | register value | — | reserved | — | Storage (SPA Type) | RESERVED |
| I2097 | uwBatVolt_DSP | BatVolt_DSP | read | register value | — | BatVolt(DSP) | — | Storage (SPA Type) | ENRICHED |
| I2098 | PBusVoltage | PBusinsideVoltage | read | register value | — | SPA | — | Storage (SPA Type) | ENRICHED |
| I2099 | NBusVoltage | NBusinsideVoltage | read | register value | — | SPA | — | Storage (SPA Type) | ENRICHED |
| I2100 | RemoteCtrlEn | / | read | register value | — | Remote setup enable | — | Storage (SPA Type) | ENRICHED |
| I2101 | RemoteCtrlPow er | / | read | register value | — | Remotely setpower | 2.Grid | Storage (SPA Type) | ENRICHED |
| I2102 | Extra AC Power to grid_H | ExtrainverteACPowertogridHigh | read | register value | — | SPAused | igh      For SPA | Storage (SPA Type) | ENRICHED |
| I2103 | Extra AC Power to grid_L | ExtrainverteACPowertogridLow | read | register value | — | SPAused | w | Storage (SPA Type) | ENRICHED |
| I2104 | Eextra_todayH | ExtrainverterPowerTOUser_Extra today(high) | read | register value | — | SPA used | R | Storage (SPA Type) | ENRICHED |
| I2105 | Eextra_todayL | ExtrainverterPowerTOUser_Extra today(low) | read | register value | — | SPA used | R | Storage (SPA Type) | ENRICHED |
| I2106 | Eextra_totalH | Extrainverter PowerTOUser_Extratotal(high) | read | register value | — | SPA used | — | Storage (SPA Type) | ENRICHED |
| I2107 | Eextra_totalL | ExtrainverterPowerTOUser_Extra total(low) | read | register value | — | SPA used | — | Storage (SPA Type) | ENRICHED |
| I2108 | Esystem_today H | SystemelectricenergytodayH | read | register value | — | SPA used System electric energy todayH | — | Storage (SPA Type) | ENRICHED |
| I2109 | Esystem_ today L | SystemelectricenergytodayL | read | register value | — | SPA used System electric energy todayL | — | Storage (SPA Type) | ENRICHED |
| I2110 | Esystem_totalH | SystemelectricenergytotalH | read | register value | — | SPA used System | — | Storage (SPA Type) | ENRICHED |
| I2111 | Esystem_totalL | SystemelectricenergytotalL | read | register value | — | — | 0.1kWh | Storage (SPA Type) | ENRICHED |
| I2112 | EACharge_Today _H (high word) | ACChargeenergytoday | read | register value | — | — | 0.1kwh | Storage (SPA Type) | ENRICHED |
| I2113 | EACharge_Today _H (low word) | ACChargeenergytoday | read | register value | — | — | 0.1kwh | Storage (SPA Type) | ENRICHED |
| I2114 | EACharge_Total _H (high word) | ACChargeenergytotal | read | register value | — | — | 0.1kwh | Storage (SPA Type) | ENRICHED |
| I2115 | EACharge_Total _H (low word) | ACChargeenergytotal | read | register value | — | — | 0.1kwh | Storage (SPA Type) | ENRICHED |
| I2116 | AC charge Power_H | Gridpowertolocalload | read | register value | — | — | 0.1kwh | Storage (SPA Type) | ENRICHED |
| I2117 | AC charge Power_L | Gridpowertolocalload | read | register value | — | — | 0.1kwh | Storage (SPA Type) | ENRICHED |
| I2118 | Priority | 0:LoadFirst 1:BatteryFirst 2:GridFirst | read | register value | — | — | 0 = LoadFirst / LoadFirst 1; 1 = BatteryFirst; 2 = GridFirst / GridFirst register value None | Storage (SPA Type) | ENRICHED |
| I2119 | Battery type | 0：Lead-acid 1：Lithiumbattery | read | register value | — | — | — | Storage (SPA Type) | ENRICHED |
| I2120 | AutoProofreadC MD | Agingmode | read | register value | — | — | — | Storage (SPA Type) | ENRICHED |
| I2124 | reserved | reserved | read | register value | — | — | — | Storage (SPA Type) | RESERVED |

#### Enum values

| Address | Source identity | Value | Vendor label | Ambiguous |
| --- | --- | --- | --- | --- |
| I2118 | Storage (SPA Type) | 0 | LoadFirst / LoadFirst 1 | True |
| I2118 | Storage (SPA Type) | 1 | BatteryFirst | False |
| I2118 | Storage (SPA Type) | 2 | GridFirst / GridFirst register value None | True |

#### Bitfields

| Address | Source identity | Bits | Field | Description | Status |
| --- | --- | --- | --- | --- | --- |
| I1199 | Storage (SPA Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I1199 | Storage (SPH Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I1248 | Storage (SPA Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I1248 | Storage (SPH Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |

<a id="block-cb-input-p070-use_for_tl_x_and_tl_xh-block-14"></a>
### Use for TL-X and TL-XH

- **Vendor heading:** Use for TL-X and TL-XH
- **Normalized role:** tl_x_tl_xh_registers
- **Table / function:** Input / FC04
- **Address range:** I3000–I3280
- **Applicable families / models:** TL-X/TL-XH/TL-XH US (MIN Type) (MIN 6000TL-XH); MOD TL3-XH (models not specified)
- **Source / provenance:** vendor_growatt_v124_2020 pp. 70–84; 273 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I3000 | Inverter operating status | Inverter status | read | u16 packed: high byte mode, low byte status, unsigned | scale=1, multiplier=1 | — | 0 = Waitingmodule / Waitingmodule 1; 1 = Self-testmode; 2 = Reserved 3 / Reserved 3：SysFault module; 4 = Flashmodule 5 / Flashmodule 5：PVBATOnlinemodule: 6：BatOnlinemodule register value None | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3001 | PV total power (high word) | Total PV/input power | read | u32 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3002 | PV total power (low word) | Total PV input power summed across all strings (0.1 W resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3003 | PV1 voltage | PV1 voltage | read | u16 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3004 | PV1 current | PV1 current | read | u16 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1A | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3005 | PV1 power (high word) | PV1 power | read | u32 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3006 | PV1 power (low word) | Real-time DC power from PV1 computed from voltage and current readings. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3007 | PV2 voltage | PV2 voltage | read | u16 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3008 | PV2 current | PV2 current | read | u16 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1A | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3009 | PV2 power (high word) | PV2 power | read | u32 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3010 | PV2 power (low word) | Real-time DC power from PV2 computed from voltage and current readings. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3011 | PV3 DC voltage | PV3voltage | read | register value | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3012 | PV3 DC current | PV3inputcurrent | read | register value | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1A | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3013 | PV3 DC power (high word) | PV3power | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3014 | PV3 DC power (low word) | Real-time DC power from PV3 computed from voltage and current readings. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3015 | PV4 DC voltage | PV4voltage | read | register value | divisor=10, scale=0.1, multiplier=0.1 | V | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3016 | PV4 DC current | PV4inputcurrent | read | register value | divisor=10, scale=0.1, multiplier=0.1 | A | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3017 | PV4 DC power (high word) | PV4power | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3018 | PV4 DC power (low word) | Real-time DC power from PV4 computed from voltage and current readings. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3019 | System output power (high word) | Systemoutputpower | read | register value, signed | divisor=10, scale=0.1, multiplier=0.1 | W | 0. | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3020 | System output power (low word) | AC output power reported by the TL-XH mirror block (0.1 W resolution). Mirrors the value at register 35. | read | register value, signed | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3021 | Output reactive power (high word) | reactivepower | read | s32 / 10, signed | divisor=10, scale=0.1, multiplier=0.1 | var | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3022 | Output reactive power (low word) | Instantaneous reactive power on the AC output (positive = inductive, negative = capacitive). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | var | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3023 | AC output power | AC output power | read | u32 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3024 | AC output power | Active AC output power delivered by the inverter (0.1 W resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3025 | Grid frequency | Grid frequency | read | u16 / 100, unsigned | divisor=100, scale=0.01, multiplier=0.01 | Hz | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3026 | AC phase L1 voltage | AC phase L1 voltage | read | u16 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | V | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3027 | AC phase L1 current | AC phase L1 current | read | u16 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | A | urrent        0.1A | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3028 | AC phase L1 power | AC phase L1 power | read | u32 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | W | att        0.1VA | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3029 | AC phase L1 power | Active power exported on phase L1. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3030 | AC phase L2 voltage | Threephasegridvoltage | read | register value | divisor=10, scale=0.1, multiplier=0.1 | V | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3031 | AC phase L2 current | Threephasegridoutputcurrent | read | register value | divisor=10, scale=0.1, multiplier=0.1 | A | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3032 | AC phase L2 power | Threephasegridoutputpower | read | register value | divisor=10, scale=0.1, multiplier=0.1 | VA | 0.1VA | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3033 | AC phase L2 power | Active power exported on phase L2. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3034 | AC phase L3 voltage | Threephasegridvoltage | read | register value | divisor=10, scale=0.1, multiplier=0.1 | V | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3035 | AC phase L3 current | Threephasegridoutputcurrent | read | register value | divisor=10, scale=0.1, multiplier=0.1 | A | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3036 | AC phase L3 power | Threephasegridoutputpower | read | register value | divisor=10, scale=0.1, multiplier=0.1 | VA | 0.1VA | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3037 | AC phase L3 power | Active power exported on phase L3. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3038 | RS line voltage | Threephasegridvoltage | read | register value | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3039 | ST line voltage | Threephasegridvoltage | read | register value | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3040 | TR line voltage | Threephasegridvoltage | read | register value | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3041 | Grid import power (high word) | Power to user/grid import | read | s32 / 10, signed | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3042 | Grid import power (low word) | Real-time active power delivered to on-site (self-consumption) loads. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3043 | Grid export power (high word) | Power to grid/export | read | s32 / 10, signed | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3044 | Grid export power (low word) | Active power exported to the utility grid. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3045 | House load power (high word) | User load power | read | s32 / 10, signed | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3046 | House load power (low word) | Aggregate instantaneous demand from on-site loads. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3047 | Inverter runtime | Inverter runtime | read | u32 / 7200, unsigned | divisor=7200, scale=0.0001388888888888889, multiplier=0.5 | h | 0.5s | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3048 | Inverter runtime | Raw counter counts seconds; divide by 7200 to obtain hours. | read | register value | divisor=7200, scale=0.5, multiplier=0.5 | h | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3049 | AC energy today | AC energy today | read | u32 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3050 | Output energy today | Energy exported to the AC output today (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3051 | Output energy total | Totalgenerateenergy | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3052 | Output energy total | Lifetime AC output energy (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3053 | PV energy total | PVenergytotal | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     P | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3054 | PV energy total | Total PV energy generated across all strings (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | t | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3055 | PV1 energy today | PV1energytoday | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3056 | PV1 energy today | Energy harvested by PV1 today. Values use 0.1 kWh resolution. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3057 | PV1 energy total | PV1energytotal | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3058 | PV1 energy total | Lifetime energy harvested by PV1. Values use 0.1 kWh resolution. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3059 | PV2 energy today | PV2energytoday | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3060 | PV2 energy today | Energy harvested by PV2 today. Values use 0.1 kWh resolution. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3061 | PV2 energy total | PV2energytotal | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3062 | PV2 energy total | Lifetime energy harvested by PV2. Values use 0.1 kWh resolution. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3063 | PV3 energy today | PV3energytoday | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3064 | PV3 energy today | Energy harvested by PV3 today. Values use 0.1 kWh resolution. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3065 | PV3 energy total | PV3energytotal | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3066 | PV3 energy total | Lifetime energy harvested by PV3. Values use 0.1 kWh resolution. | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3067 | Load energy today (high word) | Todayenergytouser | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     T | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3068 | Load energy today (low word) | Energy delivered to on-site loads today (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3069 | Load energy total (high word) | Totalenergytouser | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     T | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3070 | Load energy total (low word) | Lifetime energy delivered to on-site loads (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3071 | Grid export energy today (high word) | Todayenergytogrid | read | u32 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     T | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3072 | Grid export energy today (low word) | Energy exported to the grid today (0.1 kWh resolution). | read | u32 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3073 | Grid export energy total (high word) | Totalenergytogrid | read | u32 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     T | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3074 | Grid export energy total (low word) | Lifetime energy exported to the grid (0.1 kWh resolution). | read | u32 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | t | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3075 | User load energy today (high word) | Todayenergyofuserload | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     T | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3076 | User load energy today (low word) | Energy delivered to on-site loads today (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3077 | User load energy total (high word) | Totalenergyofuserload | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     T | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3078 | User load energy total (low word) | Lifetime energy delivered to on-site loads (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | o | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3079 | PV4 energy today | PV4 energy today | read | u32 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3080 | PV4 energy today | Energy harvested by PV string 4 today (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3081 | PV4 energy total | PV4 energy total | read | u32 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3082 | PV4 energy total | Lifetime energy harvested by PV string 4 (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3083 | PV energy today (high word) | PVenergytoday | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3084 | PV energy today (low word) | Total PV energy harvested across all strings today (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3085 | Reserved | Reserved in V1.24; no input semantic is defined. | read | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3086 | Derating mode | DeratingMode | read | u16 enum, unsigned | scale=1, multiplier=1 | — | 0 = not_derated; 1 = pv_high; 2 = power_constant; 3 = grid_voltage_high; 4 = frequency_high; 5 = dc_source_mode; 6 = inverter_temperature; 7 = active_power_order; 8 = load_speed; 9 = over_back_by_time; 10 = internal_temperature; 11 = outdoor_temperature; 12 = line_impedance_calculation; 13 = parallel_anti_backflow; 14 = local_anti_backflow; 15 = bdc_load_priority; 16 = ct_check_error; 0 = cNOTDerate; 1 = cPVHighDer ate; 2 = cPowerCon stantDerate; 3 = cGridVHigh Derate; 4 = cFreqHighD erate; 5 = cDcSoureM odeDerate; 6 = cInvTemprD erate; 7 = cActivePow erOrder; 8 = cLoadSpeed Process; 9 = cOverBack byTime; 10 = cInternalT emprDerate; 11 = cOutTemp rDerate; 12 = cLineImpe CalcDerate; 13 = cParallelA ntiBackflowD erate; 14 = cLocalAnti BackflowDera te; 15 = cBdcLoadP riDerate; 16 = cChkCTErr Derate | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3087 | PV insulation resistance | PVISOvalue | read | register value | divisor=1, scale=1, multiplier=1 | kΩ | 1KΩ | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3088 | Residual current R | RDCICurr | read | register value | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1mA | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3089 | Residual current S | SDCICurr | read | register value | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1mA | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3090 | Residual current T | TDCICurr | read | register value | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1mA | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3091 | GFCI current | GFCICurr | read | register value | divisor=1, scale=1, multiplier=1 | A | 1mA | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3092 | Total bus voltage | totalbusvoltage | read | register value | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3093 | Inverter temperature | Invertertemperature | read | register value | divisor=10, scale=0.1, multiplier=0.1 | °C | 0.1℃ | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3094 | IPM temperature | TheinsideIPMininvertertemperature | read | register value | divisor=10, scale=0.1, multiplier=0.1 | °C | rature        0.1℃ | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3095 | Boost temperature | Boosttemperature | read | register value | divisor=10, scale=0.1, multiplier=0.1 | °C | 0.1℃ | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3096 | Temp4 | Reserved | read | register value, signed | divisor=10 | — | 0.1℃ | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3097 | Communication board temperature | Commmunicationbroadtemperature | read | register value | divisor=10, scale=0.1, multiplier=0.1 | °C | 0.1℃ | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3098 | P-bus voltage | PBusinsideVoltage | read | register value | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3099 | N-bus voltage | NBusinsideVoltage | read | register value | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3100 | Inverter output power factor | InverteroutputPFnow | read | register value | divisor=1, scale=1, multiplier=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3101 | Output power percentage | RealOutputpowerPercent | read | register value, unsigned | divisor=1, scale=1, multiplier=1 | % | 1% | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3102 | Output max power limit (high word) | OutputMaxpowerLimited | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3103 | Output max power limit (low word) | Current active output power limit enforced by the inverter (0.1 W resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3104 | Standby flags | Inverterstandbyflag | read | u16 vendor-defined bitfield, unsigned | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3105 | Fault code | Inverterfaultmaincode | read | register value | divisor=1, scale=1, multiplier=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3106 | Warning main code | InverterWarningmaincode | read | register value | divisor=1, scale=1, multiplier=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3107 | Fault subcode | Inverterfaultsubcode | read | register value, signed | divisor=1 | — | bitf | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3108 | Warning subcode | InverterWarningsubcode | read | register value, signed | divisor=1 | — | bitf | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3109 | Register 3109 | — | read | register value, signed | divisor=1 | — | bitf | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3110 | Inverter warning bitfield | Current inverter warning code (vendor-defined bitmask). | read | u16 vendor-defined warning bitfield, unsigned | — | — | bitf | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3111 | Present FFT value (vendor channel A) | PresentFFTValue[CHANNEL_A] | read | u16 vendor-defined diagnostic value, unsigned | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3112 | AFCI status | AFCIStatus | read | register value | divisor=1, scale=1, multiplier=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3113 | AFCI strength (channel A) | AFCIStrength[CHANNEL_A] | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3114 | AFCI self-check (channel A) | AFCISelfCheck[CHANNEL_A] | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3115 | Inverter start delay | invstartdelaytime | read | register value | divisor=1, scale=1, multiplier=1 | s | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3116 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3117 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3118 | BDC connect state | BDCconnectstate | read | u16 enum, unsigned | scale=1, multiplier=1 | — | 0 = no_bdc_connected; 1 = bdc1_connected; 2 = bdc2_connected; 3 = bdc1_and_bdc2_connected; 0 = No BDC Connect; 1 = BDC1 Connect; 2 = BDC2 Connect; 3 = BDC1+BDC2 Connect | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3119 | Dry contact state | CurrentstatusofDryContact | read | register value | divisor=1, scale=1, multiplier=1 | — | D; 0 = turnoff; 1 = turnon | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3120 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3121 | Self-use power (high word) | self-usepower | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3122 | Self-use power (low word) | Real-time power consumed by on-site loads (0.1 W resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3123 | System energy today (high word) | Systemenergytoday | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3124 | System energy today (low word) | Total energy processed by the hybrid system today (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3125 | Battery discharge energy today (high word) | Todaydischargeenergy | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     T | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3126 | Battery discharge energy today (low word) | Energy discharged from the battery into the AC system today (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3127 | Battery discharge energy total (high word) | Totaldischargeenergy | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     T | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3128 | Battery discharge energy total (low word) | Total energy discharged from the battery (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3129 | Battery charge energy today (high word) | Chargeenergytoday | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     C | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3130 | Battery charge energy today (low word) | Energy charged into the battery today (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | e | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3131 | Battery charge energy total (high word) | Chargeenergytotal | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     C | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3132 | Battery charge energy total (low word) | Total energy charged into the battery (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | e | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3133 | AC charge energy today (high word) | TodayenergyofACcharge | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     T | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3134 | AC charge energy today (low word) | Energy charged into the battery from AC today (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | o | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3135 | AC charge energy total (high word) | TotalenergyofACcharge | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | 0.1kWh     T | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3136 | AC charge energy total (low word) | Lifetime energy charged into the battery from AC (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | o | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3137 | System energy total (high word) | Lifetime hybrid system energy throughput (0.1 kWh resolution). | read | register value | divisor=1, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3138 | System energy total (low word) | Totalenergyofsystemoutput\ | read | register value | divisor=1, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3139 | Self-use energy today (high word) | TodayenergyofSelfoutput | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3140 | Self-use energy today (low word) | Energy supplied to on-site loads today (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3141 | Self-use energy total (high word) | TotalenergyofSelfoutput | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3142 | Self-use energy total (low word) | Lifetime energy supplied to on-site loads (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3143 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3144 | Priority mode | WordMode | read | register value | scale=1, multiplier=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3145 | EPS frequency | UPSfrequency | read | register value, signed | — | Hz | 0.01 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3146 | EPS phase R voltage | UPSphaseRoutputvoltage | read | register value, signed | divisor=10 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3147 | EPS phase R current | UPSphaseRoutputcurrent | read | register value, signed | divisor=10 | A | 0.1A | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3148 | EPS phase R apparent power (high word) | UPSphaseRoutputpower | read | register value | — | VA | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3149 | EPS phase R apparent power (low word) | Phase R apparent power on the EPS output (0.1 VA resolution). | read | register value | — | VA | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3150 | EPS phase S voltage | UPSphaseSoutputvoltage | read | register value, signed | divisor=10 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3151 | EPS phase S current | UPSphaseSoutputcurrent | read | register value, signed | divisor=10 | A | 0.1A | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3152 | EPS phase S apparent power (high word) | UPSphaseSoutputpower | read | register value, signed | divisor=10 | VA | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3153 | EPS phase S apparent power (low word) | Phase S apparent power on the EPS output (0.1 VA resolution). | read | register value, signed | divisor=10 | VA | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3154 | EPS phase T voltage | UPSphaseToutputvoltage | read | register value, signed | divisor=10 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3155 | EPS phase T current | UPSphaseToutputcurrent | read | register value, signed | divisor=10 | A | 0.1A | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3156 | AC phase L3 power (high word) | UPSphaseToutputpower | read | register value, signed | divisor=10 | VA | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3157 | AC phase L3 power (low word) | Phase T apparent power on the EPS output (0.1 VA resolution). | read | register value, signed | divisor=10 | VA | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3158 | EPS total apparent power (high word) | UPSoutputpower | read | register value, signed | divisor=10 | VA | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3159 | EPS total apparent power (low word) | Total apparent power delivered by the EPS output (0.1 VA resolution). | read | register value, signed | divisor=10 | VA | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3160 | EPS load percentage | LoadpercentofUPSouput | read | register value, signed | divisor=10 | % | 0.10 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3161 | BDC power factor | Powerfactor | read | register value, signed | divisor=10 | pf | 0.1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3162 | BDC DC voltage | DCvoltage | read | register value, signed | divisor=1 | V | 1mV | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3163 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3164 | BDC data-separation flag | BDC presence flag | read | u16 enum 0=no separate BDC data, 1=separate BDC data, unsigned | — | — | 0 = no_separate_bdc_data; 1 = separate_bdc_data; 0 = Don'tneed 1：need | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3165 | BDC derating mode | BDCDeratingMode: 0=Normal, unrestricted; 1=Standby or fault; 2=Maximum battery current limit (discharge); 3=Battery discharge enabled; 4=High bus discharge derating; 5=High temperature discharge derating; 6=System warning, no discharge; 16=Maximum charging current; 17=High temperature charging; 18=Final soft charge; 19=SOC setting limits; 20=Battery low temperature; 21=High bus voltage; 22=Battery SOC (charging); 23=Need to charge; 24=System warning, not charging. Values 7-15 and 25-29 are reserved. | read | u16 enum, unsigned | scale=1, multiplier=1 | — | 0 = normal_unrestricted; 1 = standby_or_fault; 2 = maximum_discharge_current_limit; 3 = battery_discharge_enabled; 4 = high_bus_discharge_derating; 5 = high_temperature_discharge_derating; 6 = system_warning_no_discharge; 16 = maximum_battery_charging_current; 17 = high_temperature_charging; 18 = final_soft_charge; 19 = soc_setting_limits_charging; 20 = battery_low_temperature_charging; 21 = high_bus_voltage_charging; 22 = battery_soc_charging; 23 = need_to_charge; 24 = system_warning_not_charging; 0 = Normal | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3166 | BDC system mode and status | SystemworkStateandmodeThe upper8bitsindicatethemode; 0：Nochargeanddischarge； 1：charge； 2：Discharge； Thelower8bitsrepresentthestatus; 0:StandbyStatus; 1:NormalStatus; 2:FaultStatus 3：FlashStatus; | read | u16 packed: upper byte mode, lower byte status, unsigned | scale=1, multiplier=1 | — | 0 = StandbyStatus; 1 = NormalStatus; 2 = FaultStatus 3 / FaultStatus 3：FlashStatus | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3167 | BDC fault code | Storgedevicefaultcode | read | u16 vendor-defined fault code, unsigned | scale=1, multiplier=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3168 | BDC warning code | Storgedevicewarningcode | read | u16 vendor-defined warning code, unsigned | scale=1, multiplier=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3169 | Battery voltage | Battery voltage | read | u16 / 100, unsigned | divisor=100, scale=0.01, multiplier=0.1 | V | 0.01 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3170 | Battery current | Battery current | read | u16 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1A | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3171 | Battery state of charge | Battery SOC | read | u16 percentage, unsigned | scale=1, multiplier=1 | % | 1% | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3172 | VBUS1 voltage | TotalBUSvoltage | read | u16 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3173 | VBUS2 voltage | OntheBUSvoltage | read | u16 / 10, unsigned | divisor=10, scale=0.1, multiplier=0.1 | V | 0.1V | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3174 | Buck/boost current | BUCK-BOOSTCurrent | read | register value | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1A | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3175 | LLC stage current | LLCCurrent | read | register value | divisor=10, scale=0.1, multiplier=0.1 | A | 0.1A | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3176 | Battery temperature A | TempertureA | read | register value | divisor=10, scale=0.1, multiplier=0.1 | °C | 0.1℃ | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3177 | Battery temperature B | TempertureB | read | register value | divisor=10, scale=0.1, multiplier=0.1 | °C | 0.1℃ | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3178 | Battery discharge power (high word) | Battery discharge power | read | s32 / 10, signed | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1W | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3179 | Battery discharge power (low word) | Real-time discharge power flowing from the battery (0.1 W resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3180 | Battery charge power (high word) | Battery charge power | read | s32 / 10, signed | divisor=10, scale=0.1, multiplier=0.1 | W | 0.1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3181 | Battery charge power (low word) | Real-time charge power flowing into the battery (0.1 W resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | W | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3182 | BDC discharge energy total | Dischargetotalenergyofstorgedevice | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | device        0.1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3183 | BDC discharge energy total | Lifetime energy discharged by the battery DC converter (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3184 | BDC charge energy total | Chargetotalenergyofstorgedevice | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | vice           0.1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3185 | BDC charge energy total | Lifetime energy charged into the battery via the BDC (0.1 kWh resolution). | read | register value | divisor=10, scale=0.1, multiplier=0.1 | kWh | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3186 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3187 | BDC flag word | BDCmark(chargeanddischarge, faultalarmcode) Bit0:ChargeEn;BDCallowscharging Bit1:DischargeEn;BDCallows discharge Bit2~7:Resvd;reserved Bit8~11:WarnSubCode;BDC sub-warningcode Bit12~15:FaultSubCode;BDC sub-errorcode | read | u16 bitfield, unsigned | divisor=1 | — | 0 = ChargeEn; 1 = DischargeEn; 7 = Resvd; 11 = WarnSubCode; 15 = FaultSubCode | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3188 | VBUS2 low voltage | LowerBUSvoltage | read | register value, signed | divisor=10 | V | 0.1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3189 | BMS max cell index | BmsMaxVoltCellNo | read | register value | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3190 | BMS min cell index | BmsMinVoltCellNo | read | register value | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3191 | BMS average temperature (vendor channel A) | BmsBatteryAvgTemp | read | u16 temperature; scale not specified by vendor, unsigned | — | °C | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3192 | BMS max cell temperature A | BmsMaxCellTemp | read | register value | divisor=10 | °C | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3193 | BMS average temperature B | BmsBatteryAvgTemp | read | register value | divisor=10 | °C | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3194 | BMS maximum cell temperature (vendor channel B) | BmsMaxCellTemp | read | u16 temperature; scale not specified by vendor, unsigned | — | °C | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3195 | BMS average temperature (vendor channel C) | BmsBatteryAvgTemp | read | u16 temperature; scale not specified by vendor, unsigned | — | °C | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3196 | BMS maximum SOC | BmsMaxSOC | read | u16 percentage, unsigned | scale=1 | % | 1% | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3197 | BMS minimum SOC | BmsMinSOC | read | u16 percentage, unsigned | scale=1 | % | 1% | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3198 | Parallel battery count | ParallelBatteryNum | read | register value | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3199 | BMS derate reason | BmsDerateReason | read | register value | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3200 | BMS gauge full-charge capacity | BmsGaugeFCC（Ah） | read | u16 Ah; scale not specified by vendor, unsigned | — | Ah | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3201 | BMS gauge remaining capacity | BmsGaugeRM（Ah） | read | u16 Ah; scale not specified by vendor, unsigned | — | Ah | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3202 | BMS protect flags 1 | BMSProtect1 | read | register value | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3203 | BMS warning flags 1 | BMSWarn1 | read | register value | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3204 | BMS fault flags 1 | BMSFault1 | read | register value | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3205 | BMS fault flags 2 | BMSFault2 | read | register value | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3206 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3207 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3208 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3209 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3210 | Battery insulation status | BatteryISOdetectionstatus | read | u16 enum 0=not detected, 1=detection completed, unsigned | — | — | 0 = not_detected; 1 = detection_completed | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3211 | Battery request flags | batteryworkrequest | read | u16 bitfield, unsigned | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3212 | BMS status | BMS status | read | u16 enum, unsigned | — | — | 0 = dormancy; 1 = charge; 2 = discharge; 3 = free; 4 = standby; 5 = soft_start; 6 = fault; 7 = update; 1 = Charge; 2 = Discharge; 5 = Softstart | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3213 | BMS protect flags 2 | BMSProtect2 | read | register value | divisor=1 | — | R        1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3214 | BMS warning flags 2 | BMSWarn2 | read | register value | divisor=1 | — | R        1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3215 | Battery state of charge | BMS SOC | read | u16 percentage, unsigned | — | % | R        1% | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3216 | Battery voltage | BMS battery voltage | read | u16 / 100, unsigned | divisor=100, scale=0.01 | V | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3217 | Battery current | BMS battery current | read | s16 / 100, signed | divisor=100, scale=0.01 | A | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3218 | BMS max cell temperature | batterycellmaximumtemperature | read | register value | divisor=10 | °C | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3219 | BMS max charge current | Maximumchargingcurrent | read | register value | divisor=100 | A | R        0.01A | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3220 | BMS max discharge current | Maximumdischargecurrent | read | register value | divisor=100 | A | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3221 | BMS cycle count | BMSCycleCnt | read | u16 cycle count, unsigned | scale=1 | cycles | R        1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3222 | BMS state of health | BMS SOH | read | u16 percentage, unsigned | scale=1 | % | R        1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3223 | BMS charge voltage limit | Batterychargingvoltagelimitvalue | read | register value | divisor=100 | V | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3224 | BMS discharge voltage limit | Batterydischargevoltagelimitvalue | read | u16 / 100, unsigned | divisor=100, scale=0.01 | V | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3225 | BMS warning flags 3 | BMSWarn3 | read | register value | divisor=1 | — | R        1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3226 | BMS protect flags 3 | BMSProtect3 | read | register value | divisor=1 | — | R        1 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3227 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3228 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3229 | Reserved | Reserved | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | RESERVED |
| I3230 | BMS maximum cell voltage | BMSBatterySingleVoltMax | read | u16 / 1000, unsigned | divisor=1000, scale=0.001 | V | R        0 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3231 | BMS minimum cell voltage | BMSBatterySingleVoltMin | read | u16 / 1000, unsigned | divisor=1000, scale=0.001 | V | R        0 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3232 | Battery load voltage | BatteryLoadVolt | read | u16 / 100, unsigned | divisor=100, scale=0.01 | V | R        0 | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3233 | Register 3233 | — | read | register value, signed | divisor=1 | — | — | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3234 | Debug data 1 | Debugdata1 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3235 | Debug data 2 | Debugdata2 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3236 | Debug data 3 | Debugdata3 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3237 | Debug data 4 | Debugdata4 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3238 | Debug data 5 | Debugdata5 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3239 | Debug data 6 | Debugdata6 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3240 | Debug data 7 | Debugdata7 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3241 | Debug data 8 | Debugdata8 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3242 | Debug data 9 | Debugdata9 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3243 | Debug data 10 | Debugdata10 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3244 | Debug data 11 | Debugdata10 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3245 | Debug data 12 | Debugdata12 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3246 | Debug data 13 | Debugdata13 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3247 | Debug data 14 | Debugdata14 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3248 | Debug data 15 | Debugdata15 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3249 | Debug data 16 | Debugdata16 | read | register value, signed | divisor=1 | — | R | TL-X/TL-XH/TL-XH US (MIN Type); MOD TL3-XH | QUALIFIED |
| I3250 | Pex1H (high word) | PVinverter1outputpowerH | read | register value | — | — | R        0. | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3251 | Pex1H (low word) | PVinverter1outputpowerL | read | register value | — | — | R        0. | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3252 | Pex2H (high word) | PVinverter2outputpowerH | read | register value | — | — | R        0. | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3253 | Pex2H (low word) | PVinverter2outputpowerL | read | register value | — | — | R        0. | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3254 | Eex1TodayH (high word) | PVinverter1energyTodayH | read | register value | — | — | R        0. | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3255 | Eex1TodayH (low word) | PVinverter1energyTodayL | read | register value | — | — | R        0. | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3256 | Eex2TodayH (high word) | PVinverter2energyTodayH | read | register value | — | — | R        0. | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3257 | Eex2TodayH (low word) | PVinverter2energyTodayL | read | register value | — | — | R        0. | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3258 | Eex1TotalH (high word) | PVinverter1energyTotalH | read | register value | — | — | R        0. | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3259 | Eex1TotalH (low word) | PVinverter1energyTotalL | read | register value | — | — | R        0. | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3260 | Eex2TotalH (high word) | PVinverter2energyTotalH | read | register value | — | — | R        0. | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3261 | Eex2TotalH (low word) | PVinverter2energyTotalL | read | register value | — | — | R        0. | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3262 | uwBatNo | batterypacknumber | read | register value | — | BDC reports are updated every 15 minutes | R | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3263 | BatSerialNum1 | BatterypackserialnumberSN[0]SN[1] | read | register value | — | BDC reports are updated every 15 minutes | N[1]   R | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3264 | BatSerialNum2 | BatterypackserialnumberSN[2]SN[3] | read | register value | — | — | N[3]   R | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3265 | BatSerialNum3 | BatterypackserialnumberSN[4]SN[5] | read | register value | — | — | N[5]   R | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3266 | BatSerialNum4 | BatterypackserialnumberSN[6]SN[7] | read | register value | — | — | N[7]   R | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3267 | BatSerialNum5 | BatterypackserialnumberSN[8]SN[9] | read | register value | — | — | N[9]   R | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3268 | BatSerialNum6 | Batterypackserial numberSN[10]SN[11] | read | register value | — | — | R | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3269 | BatSerialNum7 | Batterypackserial numberSN[12]SN[13] | read | register value | — | — | R | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3270 | BatSerialNum8 | Batterypackserial numberSN[14]SN[15] | read | register value | — | — | R | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |
| I3271–I3279 | Reserve | Reserve | read | register value | — | — | — | TL-X/TL-XH/TL-XH US (MIN Type) | RESERVED |
| I3280 | Clear current-day data flag | Cleardaydataflag | read | u16 vendor-defined flag, unsigned | — | — | R | TL-X/TL-XH/TL-XH US (MIN Type) | QUALIFIED |

#### Enum values

| Address | Source identity | Value | Vendor label | Ambiguous |
| --- | --- | --- | --- | --- |
| I3000 | MOD TL3-XH | 0 | Waitingmodule / Waitingmodule 1 | True |
| I3000 | MOD TL3-XH | 1 | Self-testmode | False |
| I3000 | MOD TL3-XH | 2 | Reserved 3 / Reserved 3：SysFault module | True |
| I3000 | MOD TL3-XH | 4 | Flashmodule 5 / Flashmodule 5：PVBATOnlinemodule: 6：BatOnlinemodule register value None | True |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | not_derated | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | pv_high | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | power_constant | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 3 | grid_voltage_high | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 4 | frequency_high | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 5 | dc_source_mode | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | inverter_temperature | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 7 | active_power_order | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 8 | load_speed | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 9 | over_back_by_time | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 10 | internal_temperature | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 11 | outdoor_temperature | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 12 | line_impedance_calculation | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 13 | parallel_anti_backflow | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 14 | local_anti_backflow | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 15 | bdc_load_priority | False |
| I3086 | TL-X/TL-XH/TL-XH US (MIN Type) | 16 | ct_check_error | False |
| I3086 | MOD TL3-XH | 0 | cNOTDerate | False |
| I3086 | MOD TL3-XH | 1 | cPVHighDer ate | False |
| I3086 | MOD TL3-XH | 2 | cPowerCon stantDerate | False |
| I3086 | MOD TL3-XH | 3 | cGridVHigh Derate | False |
| I3086 | MOD TL3-XH | 4 | cFreqHighD erate | False |
| I3086 | MOD TL3-XH | 5 | cDcSoureM odeDerate | False |
| I3086 | MOD TL3-XH | 6 | cInvTemprD erate | False |
| I3086 | MOD TL3-XH | 7 | cActivePow erOrder | False |
| I3086 | MOD TL3-XH | 8 | cLoadSpeed Process | False |
| I3086 | MOD TL3-XH | 9 | cOverBack byTime | False |
| I3086 | MOD TL3-XH | 10 | cInternalT emprDerate | False |
| I3086 | MOD TL3-XH | 11 | cOutTemp rDerate | False |
| I3086 | MOD TL3-XH | 12 | cLineImpe CalcDerate | False |
| I3086 | MOD TL3-XH | 13 | cParallelA ntiBackflowD erate | False |
| I3086 | MOD TL3-XH | 14 | cLocalAnti BackflowDera te | False |
| I3086 | MOD TL3-XH | 15 | cBdcLoadP riDerate | False |
| I3086 | MOD TL3-XH | 16 | cChkCTErr Derate | False |
| I3118 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | no_bdc_connected | False |
| I3118 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | bdc1_connected | False |
| I3118 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | bdc2_connected | False |
| I3118 | TL-X/TL-XH/TL-XH US (MIN Type) | 3 | bdc1_and_bdc2_connected | False |
| I3118 | MOD TL3-XH | 0 | No BDC Connect | False |
| I3118 | MOD TL3-XH | 1 | BDC1 Connect | False |
| I3118 | MOD TL3-XH | 2 | BDC2 Connect | False |
| I3118 | MOD TL3-XH | 3 | BDC1+BDC2 Connect | False |
| I3119 | MOD TL3-XH | 0 | turnoff | False |
| I3119 | MOD TL3-XH | 1 | turnon | False |
| I3164 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | no_separate_bdc_data | False |
| I3164 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | separate_bdc_data | False |
| I3164 | MOD TL3-XH | 0 | Don'tneed 1：need | False |
| I3164 | Storage (MIX Type) | 0 | Don'tneed 1：need | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | normal_unrestricted | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | standby_or_fault | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | maximum_discharge_current_limit | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 3 | battery_discharge_enabled | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 4 | high_bus_discharge_derating | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 5 | high_temperature_discharge_derating | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | system_warning_no_discharge | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 16 | maximum_battery_charging_current | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 17 | high_temperature_charging | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 18 | final_soft_charge | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 19 | soc_setting_limits_charging | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 20 | battery_low_temperature_charging | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 21 | high_bus_voltage_charging | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 22 | battery_soc_charging | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 23 | need_to_charge | False |
| I3165 | TL-X/TL-XH/TL-XH US (MIN Type) | 24 | system_warning_not_charging | False |
| I3165 | MOD TL3-XH | 0 | Normal | False |
| I3166 | MOD TL3-XH | 0 | StandbyStatus | False |
| I3166 | MOD TL3-XH | 1 | NormalStatus | False |
| I3166 | MOD TL3-XH | 2 | FaultStatus 3 / FaultStatus 3：FlashStatus | True |
| I3187 | MOD TL3-XH | 0 | ChargeEn | False |
| I3187 | MOD TL3-XH | 1 | DischargeEn | False |
| I3187 | MOD TL3-XH | 7 | Resvd | False |
| I3187 | MOD TL3-XH | 11 | WarnSubCode | False |
| I3187 | MOD TL3-XH | 15 | FaultSubCode | False |
| I3210 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | not_detected | False |
| I3210 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | detection_completed | False |
| I3212 | TL-X/TL-XH/TL-XH US (MIN Type) | 0 | dormancy | False |
| I3212 | TL-X/TL-XH/TL-XH US (MIN Type) | 1 | charge | False |
| I3212 | TL-X/TL-XH/TL-XH US (MIN Type) | 2 | discharge | False |
| I3212 | TL-X/TL-XH/TL-XH US (MIN Type) | 3 | free | False |
| I3212 | TL-X/TL-XH/TL-XH US (MIN Type) | 4 | standby | False |
| I3212 | TL-X/TL-XH/TL-XH US (MIN Type) | 5 | soft_start | False |
| I3212 | TL-X/TL-XH/TL-XH US (MIN Type) | 6 | fault | False |
| I3212 | TL-X/TL-XH/TL-XH US (MIN Type) | 7 | update | False |
| I3212 | MOD TL3-XH | 0 | dormancy | False |
| I3212 | MOD TL3-XH | 1 | Charge | False |
| I3212 | MOD TL3-XH | 2 | Discharge | False |
| I3212 | MOD TL3-XH | 3 | free | False |
| I3212 | MOD TL3-XH | 4 | standby | False |
| I3212 | MOD TL3-XH | 5 | Softstart | False |
| I3212 | MOD TL3-XH | 6 | fault | False |
| I3212 | MOD TL3-XH | 7 | update | False |
| I3212 | Storage (MIX Type) | 0 | dormancy | False |
| I3212 | Storage (MIX Type) | 1 | Charge | False |
| I3212 | Storage (MIX Type) | 2 | Discharge | False |
| I3212 | Storage (MIX Type) | 3 | free | False |
| I3212 | Storage (MIX Type) | 4 | standby | False |
| I3212 | Storage (MIX Type) | 5 | Softstart | False |
| I3212 | Storage (MIX Type) | 6 | fault | False |
| I3212 | Storage (MIX Type) | 7 | update | False |

#### Bitfields

| Address | Source identity | Bits | Field | Description | Status |
| --- | --- | --- | --- | --- | --- |
| I3104 | TL-X/TL-XH/TL-XH US (MIN Type) | [0] | turn off Order | Standby was requested by the turn-off order. | structured |
| I3104 | TL-X/TL-XH/TL-XH US (MIN Type) | [1] | PVLow | PV input is below the standby threshold. | structured |
| I3104 | TL-X/TL-XH/TL-XH US (MIN Type) | [2] | AC Volt/Freq out of scope | AC voltage or frequency is out of scope. | structured |
| I3104 | TL-X/TL-XH/TL-XH US (MIN Type) | [3, 7] | Reserved | Reserved by the vendor. | structured |
| I3104 | MOD TL3-XH | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3110 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3164 | MOD TL3-XH | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3164 | Storage (MIX Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3187 | TL-X/TL-XH/TL-XH US (MIN Type) | [0] | ChargeEn | BDC allows charging. | structured |
| I3187 | TL-X/TL-XH/TL-XH US (MIN Type) | [1] | DischargeEn | BDC allows discharge. | structured |
| I3187 | TL-X/TL-XH/TL-XH US (MIN Type) | [2, 7] | Resvd | Reserved. | structured |
| I3187 | TL-X/TL-XH/TL-XH US (MIN Type) | [8, 11] | WarnSubCode | BDC sub-warning code. | structured |
| I3187 | TL-X/TL-XH/TL-XH US (MIN Type) | [12, 15] | FaultSubCode | BDC sub-error code. | structured |
| I3187 | MOD TL3-XH | [0] | ChargeEn | ChargeEn | structured |
| I3187 | MOD TL3-XH | [1] | DischargeEn | DischargeEn | structured |
| I3187 | MOD TL3-XH | [2, 7] | Resvd | Resvd | structured |
| I3187 | MOD TL3-XH | [8, 11] | WarnSubCode | WarnSubCode | structured |
| I3187 | MOD TL3-XH | [12, 15] | FaultSubCode | FaultSubCode | structured |
| I3202 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3202 | MOD TL3-XH | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3202 | Storage (MIX Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3203 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3203 | MOD TL3-XH | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3203 | Storage (MIX Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3204 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3204 | MOD TL3-XH | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3204 | Storage (MIX Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3205 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3205 | MOD TL3-XH | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3205 | Storage (MIX Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3211 | TL-X/TL-XH/TL-XH US (MIN Type) | [0] | Prohibit charging | 1 prohibits charging; 0 allows charging. | structured |
| I3211 | TL-X/TL-XH/TL-XH US (MIN Type) | [1] | Enable strong charge | 1 enables strong charge; 0 disables strong charge. | structured |
| I3211 | TL-X/TL-XH/TL-XH US (MIN Type) | [2] | Enable strong charge2 | 1 enables strong charge2; 0 disables strong charge2. | structured |
| I3211 | TL-X/TL-XH/TL-XH US (MIN Type) | [8] | Discharge is prohibited | 1 prohibits discharge; 0 allows discharge. | structured |
| I3211 | TL-X/TL-XH/TL-XH US (MIN Type) | [9] | Turn on power reduction | 1 turns on power reduction; 0 turns it off. | structured |
| I3211 | MOD TL3-XH | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3211 | Storage (MIX Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3213 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3213 | MOD TL3-XH | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3213 | Storage (MIX Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3214 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3214 | MOD TL3-XH | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3214 | Storage (MIX Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3225 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3225 | MOD TL3-XH | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3225 | Storage (MIX Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3226 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3226 | MOD TL3-XH | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3226 | Storage (MIX Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |
| I3280 | TL-X/TL-XH/TL-XH US (MIN Type) | [0, 15] | undocumented flag word | The source identifies a packed flag word but does not define safe individual meanings. | placeholder |

#### Packed fields

| Address | Source identity | Fields |
| --- | --- | --- |
| I3000 | TL-X/TL-XH/TL-XH US (MIN Type) | [{"bits": [8, 15], "description": "Vendor-defined inverter mode byte.", "enum": {"0": "waiting_module", "1": "self_test", "2": "reserved", "3": "system_fault_module", "4": "flash_module", "5": "pv_battery_online_module", "6": "battery_online_module"}, "name": "mode", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "high-byte mode"}, {"bits": [0, 7], "description": "The vendor source does not enumerate the low-byte values separately.", "name": "status", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "low-byte status"}] |
| I3166 | TL-X/TL-XH/TL-XH US (MIN Type) | [{"bits": [8, 15], "enum": {"0": "no_charge_or_discharge", "1": "charge", "2": "discharge"}, "name": "mode", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "mode"}, {"bits": [0, 7], "enum": {"0": "standby", "1": "normal", "2": "fault", "3": "flash"}, "name": "status", "provenance": ["vendor_v124"], "status": "source_explicit", "vendor_label": "status"}] |

<a id="block-cb-input-p084-bdc_and_bms_information_support_up_to_10_parallel_bdcs-block-15"></a>
### BDC and BMS information (support up to 10 PARALLEL BDCS)

- **Vendor heading:** BDC and BMS information (support up to 10 PARALLEL BDCS)
- **Normalized role:** bms_information
- **Table / function:** Input / FC04
- **Address range:** I4000–I5079
- **Applicable families / models:** Declared range only
- **Source / provenance:** vendor_growatt_v124_2020 pp. 84–84; 5 source rows and 0 reviewed evidence claims. See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json).

| Addr | Variable | Description | Access | Type | Scale | Unit | Range / Enum | Applicability | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| I4000–I4107 | 1                    T | he first 8 registers are the 16 | — | — | — | — | -bit serial number | Declared range only | UNRESOLVED |
| I4108–I4215 | 2                    T | he first 8 registers are the 16 | — | — | — | — | -bit serial number | Declared range only | UNRESOLVED |
| — | T | he first 8 registers are the 16 | — | — | — | — | -bit serial number | Declared range only | UNRESOLVED |
| I4864–I4971 | 9                    T | he first 8 registers are the 16 | — | — | — | — | -bit serial number | Declared range only | UNRESOLVED |
| I4972–I5079 | 10                   T | he first 8 registers are the 16 | — | — | — | — | -bit serial number | Declared range only | UNRESOLVED |

### Reserved ranges

| Range | Status | Basis | Meaning | Source |
| --- | --- | --- | --- | --- |
| I3281–I3374 | RESERVED | vendor_specified_range, no_individual_semantic_rows, stock_shine_reads_range, runtime_all_zero | declared block words with no individual V1.24 semantic row; treated as reserved or unused | V1.24 input TL-X/TL-XH block: I3280 is last explicit row; next source block begins at I4000 |

## Logical multi-word fields

These rows preserve the accepted component order, word roles, and status. Unknown word order remains unknown; the entries do not imply an additional decoding rule.

| Variable | Family | Component registers | Encoding | Word order | Status |
| --- | --- | --- | --- | --- | --- |
| Module code segments | TL-X/TL-XH/TL-XH US (MIN Type) | H118 (word_1), H119 (word_2), H120 (word_3), H121 (word_4) | register value | unknown | unknown_word_order |
| Firmware | TL-X/TL-XH/TL-XH US (MIN Type) | H12 (high_word), H13 (middle_word), H14 (low_word) | register value | high_middle_low | source_explicit |
| Inverter serial number | TL-X/TL-XH/TL-XH US (MIN Type) | H23 (word_1), H24 (word_2), H25 (word_3), H26 (word_4), H27 (word_5) | ASCII, 10 characters | unknown | unknown_word_order |
| Inverter Model | TL-X/TL-XH/TL-XH US (MIN Type) | H28 (high_word), H29 (low_word) | register value | high_low | source_explicit |
| Serial Number | TL-X/TL-XH/TL-XH US (MIN Type) | H3001 (word_1), H3002 (word_2), H3003 (word_3), H3004 (word_4), H3005 (word_5), H3006 (word_6), H3007 (word_7), H3008 (word_8) | serial_number | unknown | unknown_word_order |
| Serial Number | TL-X/TL-XH/TL-XH US (MIN Type) | H3009 (word_1), H3010 (word_2), H3011 (word_3), H3012 (word_4), H3013 (word_5), H3014 (word_6), H3015 (word_7), H3016 (word_8) | register value | unknown | unknown_word_order |
| Battery type | TL-X/TL-XH/TL-XH US (MIN Type) | H3070 (word_1), H3071 (word_2) | register value | unknown | unknown_word_order |
| Reserved | TL-X/TL-XH/TL-XH US (MIN Type) | H3072 (word_1), H3073 (word_2) | register value | unknown | unknown_word_order |
| Reserved | TL-X/TL-XH/TL-XH US (MIN Type) | H3074 (word_1), H3075 (word_2) | register value | unknown | unknown_word_order |
| Reserved | TL-X/TL-XH/TL-XH US (MIN Type) | H3076 (word_1), H3077 (word_2) | register value | unknown | unknown_word_order |
| Reserved | TL-X/TL-XH/TL-XH US (MIN Type) | H3078 (word_1), H3079 (word_2) | register value | unknown | unknown_word_order |
| Reserved | TL-X/TL-XH/TL-XH US (MIN Type) | H3083 (word_1), H3084 (word_2) | register value | unknown | unknown_word_order |
| Battery rack serial | TL-X/TL-XH/TL-XH US (MIN Type) | H3087 (word_1), H3088 (word_2), H3089 (word_3), H3090 (word_4), H3091 (word_5), H3092 (word_6), H3093 (word_7), H3094 (word_8) | register value | unknown | unknown_word_order |
| BDC monitoring code | TL-X/TL-XH/TL-XH US (MIN Type) | H3096 (word_1), H3097 (word_2) | register value | unknown | unknown_word_order |
| DSP firmware code | TL-X/TL-XH/TL-XH US (MIN Type) | H3099 (word_1), H3100 (word_2) | register value | unknown | unknown_word_order |
| Us Tou Month Groups | TL-X/TL-XH/TL-XH US (MIN Type) | H3125 (word_1), H3126 (word_2), H3127 (word_3), H3128 (word_4) | register value | unknown | unknown_word_order |
| Manufacturer information string | TL-X/TL-XH/TL-XH US (MIN Type) | H34 (word_1), H35 (word_2), H36 (word_3), H37 (word_4), H38 (word_5), H39 (word_6), H40 (word_7), H41 (word_8) | register value | unknown | unknown_word_order |
| Rated apparent power | TL-X/TL-XH/TL-XH US (MIN Type) | H6 (high_word), H7 (low_word) | register value | high_low | source_explicit |
| Controller firmware build string | TL-X/TL-XH/TL-XH US (MIN Type) | H82 (word_1), H83 (word_2), H84 (word_3), H85 (word_4), H86 (word_5), H87 (word_6) | register value | unknown | unknown_word_order |
| Firmware | TL-X/TL-XH/TL-XH US (MIN Type) | H9 (high_word), H10 (middle_word), H11 (low_word) | firmware_version | high_middle_low | source_explicit |
| PV total power | TL-X/TL-XH/TL-XH US (MIN Type) | I1 (word_1), I2 (word_2) | register value | unknown | unknown_word_order |
| PV3 DC voltage | TL-X/TL-XH/TL-XH US (MIN Type) | I11 (word_1), I12 (word_2) | register value | unknown | unknown_word_order |
| PV total power | TL-X/TL-XH/TL-XH US (MIN Type) | I13 (word_1), I14 (word_2) | register value | unknown | unknown_word_order |
| PV4 DC voltage | TL-X/TL-XH/TL-XH US (MIN Type) | I15 (word_1), I16 (word_2) | register value | unknown | unknown_word_order |
| PV total power | TL-X/TL-XH/TL-XH US (MIN Type) | I17 (word_1), I18 (word_2) | register value | unknown | unknown_word_order |
| PV total power | TL-X/TL-XH/TL-XH US (MIN Type) | I21 (word_1), I22 (word_2) | register value | unknown | unknown_word_order |
| Output reactive power | TL-X/TL-XH/TL-XH US (MIN Type) | I234 (high_word), I235 (low_word) | register value | high_low | source_explicit |
| Reactive energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I236 (high_word), I237 (low_word) | register value | high_low | source_explicit |
| PV total power | TL-X/TL-XH/TL-XH US (MIN Type) | I25 (high_word), I26 (low_word) | register value | high_low | source_explicit |
| PV7 DC voltage | TL-X/TL-XH/TL-XH US (MIN Type) | I27 (word_1), I28 (word_2) | register value | unknown | unknown_word_order |
| PV total power | TL-X/TL-XH/TL-XH US (MIN Type) | I29 (high_word), I30 (low_word) | register value | high_low | source_explicit |
| PV1 DC voltage | TL-X/TL-XH/TL-XH US (MIN Type) | I3 (word_1), I4 (word_2) | register value | unknown | unknown_word_order |
| PV total power | TL-X/TL-XH/TL-XH US (MIN Type) | I3001 (high_word), I3002 (low_word) | u32 / 10 | high_low | source_explicit |
| PV1 power | TL-X/TL-XH/TL-XH US (MIN Type) | I3005 (high_word), I3006 (low_word) | u32 / 10 | high_low | source_explicit |
| PV2 power | TL-X/TL-XH/TL-XH US (MIN Type) | I3009 (high_word), I3010 (low_word) | u32 / 10 | high_low | source_explicit |
| PV3 DC power | TL-X/TL-XH/TL-XH US (MIN Type) | I3013 (high_word), I3014 (low_word) | register value | high_low | source_explicit |
| PV4 DC power | TL-X/TL-XH/TL-XH US (MIN Type) | I3017 (high_word), I3018 (low_word) | register value | high_low | source_explicit |
| System output power | TL-X/TL-XH/TL-XH US (MIN Type) | I3019 (high_word), I3020 (low_word) | register value | high_low | source_explicit |
| Output reactive power | TL-X/TL-XH/TL-XH US (MIN Type) | I3021 (high_word), I3022 (low_word) | s32 / 10 | high_low | source_explicit |
| AC output power | TL-X/TL-XH/TL-XH US (MIN Type) | I3023 (word_1), I3024 (word_2) | u32 / 10 | unknown | unknown_word_order |
| AC phase L1 power | TL-X/TL-XH/TL-XH US (MIN Type) | I3028 (word_1), I3029 (word_2) | u32 / 10 | unknown | unknown_word_order |
| AC phase L2 power | TL-X/TL-XH/TL-XH US (MIN Type) | I3032 (word_1), I3033 (word_2) | register value | unknown | unknown_word_order |
| AC phase L3 power | TL-X/TL-XH/TL-XH US (MIN Type) | I3036 (word_1), I3037 (word_2) | register value | unknown | unknown_word_order |
| Grid import power | TL-X/TL-XH/TL-XH US (MIN Type) | I3041 (high_word), I3042 (low_word) | s32 / 10 | high_low | source_explicit |
| Grid export power | TL-X/TL-XH/TL-XH US (MIN Type) | I3043 (high_word), I3044 (low_word) | s32 / 10 | high_low | source_explicit |
| House load power | TL-X/TL-XH/TL-XH US (MIN Type) | I3045 (high_word), I3046 (low_word) | s32 / 10 | high_low | source_explicit |
| Inverter runtime | TL-X/TL-XH/TL-XH US (MIN Type) | I3047 (word_1), I3048 (word_2) | u32 / 7200 | unknown | unknown_word_order |
| AC energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3049 (word_1), I3050 (word_2) | u32 / 10 | unknown | unknown_word_order |
| Output energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3051 (word_1), I3052 (word_2) | register value | unknown | unknown_word_order |
| PV energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3053 (word_1), I3054 (word_2) | register value | unknown | unknown_word_order |
| PV1 energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3055 (word_1), I3056 (word_2) | register value | unknown | unknown_word_order |
| PV1 energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3057 (word_1), I3058 (word_2) | register value | unknown | unknown_word_order |
| PV2 energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3059 (word_1), I3060 (word_2) | register value | unknown | unknown_word_order |
| PV2 energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3061 (word_1), I3062 (word_2) | register value | unknown | unknown_word_order |
| PV3 energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3063 (word_1), I3064 (word_2) | register value | unknown | unknown_word_order |
| PV3 energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3065 (word_1), I3066 (word_2) | register value | unknown | unknown_word_order |
| Load energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3067 (high_word), I3068 (low_word) | register value | high_low | source_explicit |
| Load energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3069 (high_word), I3070 (low_word) | register value | high_low | source_explicit |
| Grid export energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3071 (high_word), I3072 (low_word) | u32 / 10 | high_low | source_explicit |
| Grid export energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3073 (high_word), I3074 (low_word) | u32 / 10 | high_low | source_explicit |
| User load energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3075 (high_word), I3076 (low_word) | register value | high_low | source_explicit |
| User load energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3077 (high_word), I3078 (low_word) | register value | high_low | source_explicit |
| PV4 energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3079 (word_1), I3080 (word_2) | u32 / 10 | unknown | unknown_word_order |
| PV4 energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3081 (word_1), I3082 (word_2) | u32 / 10 | unknown | unknown_word_order |
| PV energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3083 (high_word), I3084 (low_word) | register value | high_low | source_explicit |
| PV8 DC voltage | TL-X/TL-XH/TL-XH US (MIN Type) | I31 (word_1), I32 (word_2) | register value | unknown | unknown_word_order |
| Output max power limit | TL-X/TL-XH/TL-XH US (MIN Type) | I3102 (high_word), I3103 (low_word) | register value | high_low | source_explicit |
| Self-use power | TL-X/TL-XH/TL-XH US (MIN Type) | I3121 (high_word), I3122 (low_word) | register value | high_low | source_explicit |
| System energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3123 (high_word), I3124 (low_word) | register value | high_low | source_explicit |
| Battery discharge energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3125 (high_word), I3126 (low_word) | register value | high_low | source_explicit |
| Battery discharge energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3127 (high_word), I3128 (low_word) | register value | high_low | source_explicit |
| Battery charge energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3129 (high_word), I3130 (low_word) | register value | high_low | source_explicit |
| Battery charge energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3131 (high_word), I3132 (low_word) | register value | high_low | source_explicit |
| AC charge energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3133 (high_word), I3134 (low_word) | register value | high_low | source_explicit |
| AC charge energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3135 (high_word), I3136 (low_word) | register value | high_low | source_explicit |
| System energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3137 (high_word), I3138 (low_word) | register value | high_low | source_explicit |
| Self-use energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I3139 (high_word), I3140 (low_word) | register value | high_low | source_explicit |
| Self-use energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3141 (high_word), I3142 (low_word) | register value | high_low | source_explicit |
| EPS phase R apparent power | TL-X/TL-XH/TL-XH US (MIN Type) | I3148 (high_word), I3149 (low_word) | register value | high_low | source_explicit |
| EPS phase S apparent power | TL-X/TL-XH/TL-XH US (MIN Type) | I3152 (high_word), I3153 (low_word) | register value | high_low | source_explicit |
| AC phase L3 power | TL-X/TL-XH/TL-XH US (MIN Type) | I3156 (high_word), I3157 (low_word) | register value | high_low | source_explicit |
| EPS total apparent power | TL-X/TL-XH/TL-XH US (MIN Type) | I3158 (high_word), I3159 (low_word) | register value | high_low | source_explicit |
| Battery discharge power | TL-X/TL-XH/TL-XH US (MIN Type) | I3178 (high_word), I3179 (low_word) | s32 / 10 | high_low | source_explicit |
| Battery charge power | TL-X/TL-XH/TL-XH US (MIN Type) | I3180 (high_word), I3181 (low_word) | s32 / 10 | high_low | source_explicit |
| BDC discharge energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3182 (word_1), I3183 (word_2) | register value | unknown | unknown_word_order |
| BDC charge energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I3184 (word_1), I3185 (word_2) | register value | unknown | unknown_word_order |
| Pex1H | TL-X/TL-XH/TL-XH US (MIN Type) | I3250 (high_word), I3251 (low_word) | register value | high_low | source_explicit |
| Pex2H | TL-X/TL-XH/TL-XH US (MIN Type) | I3252 (high_word), I3253 (low_word) | register value | high_low | source_explicit |
| Eex1TodayH | TL-X/TL-XH/TL-XH US (MIN Type) | I3254 (high_word), I3255 (low_word) | register value | high_low | source_explicit |
| Eex2TodayH | TL-X/TL-XH/TL-XH US (MIN Type) | I3256 (high_word), I3257 (low_word) | register value | high_low | source_explicit |
| Eex1TotalH | TL-X/TL-XH/TL-XH US (MIN Type) | I3258 (high_word), I3259 (low_word) | register value | high_low | source_explicit |
| Eex2TotalH | TL-X/TL-XH/TL-XH US (MIN Type) | I3260 (high_word), I3261 (low_word) | register value | high_low | source_explicit |
| PV total power | TL-X/TL-XH/TL-XH US (MIN Type) | I33 (high_word), I34 (low_word) | register value | high_low | source_explicit |
| AC output power | TL-X/TL-XH/TL-XH US (MIN Type) | I35 (high_word), I36 (low_word) | register value | high_low | source_explicit |
| Grid frequency | TL-X/TL-XH/TL-XH US (MIN Type) | I37 (word_1), I38 (word_2) | register value | unknown | unknown_word_order |
| AC phase L1 power | TL-X/TL-XH/TL-XH US (MIN Type) | I40 (high_word), I41 (low_word) | register value | high_low | source_explicit |
| AC phase L2 power | TL-X/TL-XH/TL-XH US (MIN Type) | I44 (high_word), I45 (low_word) | register value | high_low | source_explicit |
| AC phase L3 power | TL-X/TL-XH/TL-XH US (MIN Type) | I48 (high_word), I49 (low_word) | register value | high_low | source_explicit |
| PV total power | TL-X/TL-XH/TL-XH US (MIN Type) | I5 (word_1), I6 (word_2) | register value | unknown | unknown_word_order |
| Output energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I53 (high_word), I54 (low_word) | register value | high_low | source_explicit |
| Output energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I55 (high_word), I56 (low_word) | register value | high_low | source_explicit |
| Inverter runtime | TL-X/TL-XH/TL-XH US (MIN Type) | I57 (high_word), I58 (low_word) | register value | high_low | source_explicit |
| PV1 energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I59 (high_word), I60 (low_word) | register value | high_low | source_explicit |
| PV1 energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I61 (high_word), I62 (low_word) | register value | high_low | source_explicit |
| PV2 energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I63 (high_word), I64 (low_word) | register value | high_low | source_explicit |
| PV2 energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I65 (high_word), I66 (low_word) | register value | high_low | source_explicit |
| PV3 energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I67 (high_word), I68 (low_word) | register value | high_low | source_explicit |
| PV3 energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I69 (high_word), I70 (low_word) | register value | high_low | source_explicit |
| PV4 energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I71 (high_word), I72 (low_word) | register value | high_low | source_explicit |
| PV4 energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I73 (high_word), I74 (low_word) | register value | high_low | source_explicit |
| PV5 energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I75 (high_word), I76 (low_word) | register value | high_low | source_explicit |
| PV5 energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I77 (high_word), I78 (low_word) | register value | high_low | source_explicit |
| PV6 energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I79 (high_word), I80 (low_word) | register value | high_low | source_explicit |
| PV6 energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I81 (high_word), I82 (low_word) | register value | high_low | source_explicit |
| PV7 energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I83 (high_word), I84 (low_word) | register value | high_low | source_explicit |
| PV7 energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I85 (high_word), I86 (low_word) | register value | high_low | source_explicit |
| PV8 energy today | TL-X/TL-XH/TL-XH US (MIN Type) | I87 (high_word), I88 (low_word) | register value | high_low | source_explicit |
| PV8 energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I89 (high_word), I90 (low_word) | register value | high_low | source_explicit |
| PV total power | TL-X/TL-XH/TL-XH US (MIN Type) | I9 (word_1), I10 (word_2) | register value | unknown | unknown_word_order |
| PV energy total | TL-X/TL-XH/TL-XH US (MIN Type) | I91 (high_word), I92 (low_word) | register value | high_low | source_explicit |
| Module code segments | MOD TL3-XH | H118 (word_1), H119 (word_2), H120 (word_3), H121 (word_4) | register value | unknown | unknown_word_order |
| Firmware | MOD TL3-XH | H12 (high_word), H13 (middle_word), H14 (low_word) | register value | high_middle_low | source_explicit |
| Serial Number | MOD TL3-XH | H23 (word_1), H24 (word_2), H25 (word_3), H26 (word_4), H27 (word_5) | serial_number | unknown | unknown_word_order |
| Inverter Model | MOD TL3-XH | H28 (high_word), H29 (low_word) | register value | high_low | source_explicit |
| Serial Number | MOD TL3-XH | H3001 (word_1), H3002 (word_2), H3003 (word_3), H3004 (word_4), H3005 (word_5), H3006 (word_6), H3007 (word_7), H3008 (word_8) | serial_number | unknown | unknown_word_order |
| Serial Number | MOD TL3-XH | H3009 (word_1), H3010 (word_2), H3011 (word_3), H3012 (word_4), H3013 (word_5), H3014 (word_6), H3015 (word_7), H3016 (word_8) | register value | unknown | unknown_word_order |
| Register 3041 | MOD TL3-XH | H3041 (word_1), H3042 (word_2) | register value | unknown | unknown_word_order |
| Register 3043 | MOD TL3-XH | H3043 (word_1), H3044 (word_2) | register value | unknown | unknown_word_order |
| Register 3045 | MOD TL3-XH | H3045 (word_1), H3046 (word_2) | register value | unknown | unknown_word_order |
| Register 3051 | MOD TL3-XH | H3051 (word_1), H3052 (word_2) | register value | unknown | unknown_word_order |
| Register 3053 | MOD TL3-XH | H3053 (word_1), H3054 (word_2) | register value | unknown | unknown_word_order |
| Register 3055 | MOD TL3-XH | H3055 (word_1), H3056 (word_2) | register value | unknown | unknown_word_order |
| Register 3057 | MOD TL3-XH | H3057 (word_1), H3058 (word_2) | register value | unknown | unknown_word_order |
| Register 3059 | MOD TL3-XH | H3059 (word_1), H3060–H3069 (word_2) | register value | unknown | unknown_word_order |
| BatMdlSeria/ ParalNum | MOD TL3-XH | H3071 (word_1), H3072 (word_2) | register value | unknown | unknown_word_order |
| Reserved | MOD TL3-XH | H3073 (word_1), H3074 (word_2) | register value | unknown | unknown_word_order |
| Reserved | MOD TL3-XH | H3075 (word_1), H3076 (word_2) | register value | unknown | unknown_word_order |
| Reserved | MOD TL3-XH | H3077 (word_1), H3078 (word_2) | register value | unknown | unknown_word_order |
| Reserved | MOD TL3-XH | H3083 (word_1), H3084 (word_2) | register value | unknown | unknown_word_order |
| Battery rack serial | MOD TL3-XH | H3087 (word_1), H3088 (word_2), H3089 (word_3), H3090 (word_4), H3091 (word_5), H3092 (word_6), H3093 (word_7), H3094 (word_8) | register value | unknown | unknown_word_order |
| BDC monitoring code | MOD TL3-XH | H3096 (word_1), H3097 (word_2) | register value | unknown | unknown_word_order |
| DSP firmware code | MOD TL3-XH | H3099 (word_1), H3100 (word_2) | register value | unknown | unknown_word_order |
| Manufacturer information string | MOD TL3-XH | H34 (word_1), H35 (word_2), H36 (word_3), H37 (word_4), H38 (word_5), H39 (word_6), H40 (word_7), H41 (word_8) | register value | unknown | unknown_word_order |
| Rated apparent power | MOD TL3-XH | H6 (high_word), H7 (low_word) | register value | high_low | source_explicit |
| Controller firmware build string | MOD TL3-XH | H82 (word_1), H83 (word_2), H84 (word_3), H85 (word_4), H86 (word_5), H87 (word_6) | register value | unknown | unknown_word_order |
| Firmware | MOD TL3-XH | H9 (high_word), H10 (middle_word), H11 (low_word) | firmware_version | high_middle_low | source_explicit |
| PV total power | MOD TL3-XH | I3001 (high_word), I3002 (low_word) | register value | high_low | source_explicit |
| PV1 DC power | MOD TL3-XH | I3005 (high_word), I3006 (low_word) | register value | high_low | source_explicit |
| PV2 DC power | MOD TL3-XH | I3009 (high_word), I3010 (low_word) | register value | high_low | source_explicit |
| PV3 DC power | MOD TL3-XH | I3013 (high_word), I3014 (low_word) | register value | high_low | source_explicit |
| PV4 DC power | MOD TL3-XH | I3017 (high_word), I3018 (low_word) | register value | high_low | source_explicit |
| System output power | MOD TL3-XH | I3019 (high_word), I3020 (low_word) | register value | high_low | source_explicit |
| Output reactive power | MOD TL3-XH | I3021 (high_word), I3022 (low_word) | register value | high_low | source_explicit |
| AC output power | MOD TL3-XH | I3023 (high_word), I3024 (low_word) | register value | high_low | source_explicit |
| AC phase L1 power | MOD TL3-XH | I3028 (high_word), I3029 (low_word) | register value | high_low | source_explicit |
| AC phase L2 power | MOD TL3-XH | I3032 (high_word), I3033 (low_word) | register value | high_low | source_explicit |
| AC phase L3 power | MOD TL3-XH | I3036 (high_word), I3037 (low_word) | register value | high_low | source_explicit |
| Grid import power | MOD TL3-XH | I3041 (high_word), I3042 (low_word) | register value | high_low | source_explicit |
| Grid export power | MOD TL3-XH | I3043 (high_word), I3044 (low_word) | register value | high_low | source_explicit |
| House load power | MOD TL3-XH | I3045 (high_word), I3046 (low_word) | register value | high_low | source_explicit |
| Inverter runtime | MOD TL3-XH | I3047 (high_word), I3048 (low_word) | register value | high_low | source_explicit |
| Output energy today | MOD TL3-XH | I3049 (high_word), I3050 (low_word) | register value | high_low | source_explicit |
| Output energy total | MOD TL3-XH | I3051 (high_word), I3052 (low_word) | register value | high_low | source_explicit |
| PV energy total | MOD TL3-XH | I3053 (high_word), I3054 (low_word) | register value | high_low | source_explicit |
| PV1 energy today | MOD TL3-XH | I3055 (high_word), I3056 (low_word) | register value | high_low | source_explicit |
| PV1 energy total | MOD TL3-XH | I3057 (high_word), I3058 (low_word) | register value | high_low | source_explicit |
| PV2 energy today | MOD TL3-XH | I3059 (high_word), I3060 (low_word) | register value | high_low | source_explicit |
| PV2 energy total | MOD TL3-XH | I3061 (high_word), I3062 (low_word) | register value | high_low | source_explicit |
| PV3 energy today | MOD TL3-XH | I3063 (high_word), I3064 (low_word) | register value | high_low | source_explicit |
| PV3 energy total | MOD TL3-XH | I3065 (high_word), I3066 (low_word) | register value | high_low | source_explicit |
| Load energy today | MOD TL3-XH | I3067 (high_word), I3068 (low_word) | register value | high_low | source_explicit |
| Load energy total | MOD TL3-XH | I3069 (high_word), I3070 (low_word) | register value | high_low | source_explicit |
| Grid export power | MOD TL3-XH | I3071 (high_word), I3072 (low_word) | register value | high_low | source_explicit |
| Grid export power | MOD TL3-XH | I3073 (high_word), I3074 (low_word) | register value | high_low | source_explicit |
| User load energy today | MOD TL3-XH | I3075 (high_word), I3076 (low_word) | register value | high_low | source_explicit |
| User load energy total | MOD TL3-XH | I3077 (high_word), I3078 (low_word) | register value | high_low | source_explicit |
| PV4 energy today | MOD TL3-XH | I3079 (high_word), I3080 (low_word) | register value | high_low | source_explicit |
| PV4 energy total | MOD TL3-XH | I3081 (high_word), I3082 (low_word) | register value | high_low | source_explicit |
| PV energy today | MOD TL3-XH | I3083 (high_word), I3084 (low_word) | register value | high_low | source_explicit |
| Output max power limit | MOD TL3-XH | I3102 (high_word), I3103 (low_word) | register value | high_low | source_explicit |
| Warning code | MOD TL3-XH | I3110 (word_1), I3111 (word_2) | register value | unknown | unknown_word_order |
| Self-use power | MOD TL3-XH | I3121 (high_word), I3122 (low_word) | register value | high_low | source_explicit |
| System energy today | MOD TL3-XH | I3123 (high_word), I3124 (low_word) | register value | high_low | source_explicit |
| Battery discharge energy today | MOD TL3-XH | I3125 (high_word), I3126 (low_word) | register value | high_low | source_explicit |
| Battery discharge energy total | MOD TL3-XH | I3127 (high_word), I3128 (low_word) | register value | high_low | source_explicit |
| Battery charge energy today | MOD TL3-XH | I3129 (high_word), I3130 (low_word) | register value | high_low | source_explicit |
| Battery charge energy total | MOD TL3-XH | I3131 (high_word), I3132 (low_word) | register value | high_low | source_explicit |
| AC charge energy today | MOD TL3-XH | I3133 (high_word), I3134 (low_word) | register value | high_low | source_explicit |
| AC charge energy total | MOD TL3-XH | I3135 (high_word), I3136 (low_word) | register value | high_low | source_explicit |
| System energy total | MOD TL3-XH | I3137 (high_word), I3138 (low_word) | register value | high_low | source_explicit |
| Self-use energy today | MOD TL3-XH | I3139 (high_word), I3140 (low_word) | register value | high_low | source_explicit |
| Self-use energy total | MOD TL3-XH | I3141 (high_word), I3142 (low_word) | register value | high_low | source_explicit |
| EPS phase R apparent power | MOD TL3-XH | I3148 (high_word), I3149 (low_word) | register value | high_low | source_explicit |
| EPS phase S apparent power | MOD TL3-XH | I3152 (high_word), I3153 (low_word) | register value | high_low | source_explicit |
| AC phase L3 power | MOD TL3-XH | I3156 (high_word), I3157 (low_word) | register value | high_low | source_explicit |
| EPS total apparent power | MOD TL3-XH | I3158 (high_word), I3159 (low_word) | register value | high_low | source_explicit |
| Battery discharge power | MOD TL3-XH | I3178 (high_word), I3179 (low_word) | register value | high_low | source_explicit |
| Battery charge power | MOD TL3-XH | I3180 (high_word), I3181 (low_word) | register value | high_low | source_explicit |
| BDC discharge energy total | MOD TL3-XH | I3182 (word_1), I3183 (word_2) | register value | unknown | unknown_word_order |
| BDC charge energy total | MOD TL3-XH | I3184 (word_1), I3185 (word_2) | register value | unknown | unknown_word_order |
| Module code segments | Storage (MIX Type) | H118 (word_1), H119 (word_2), H120 (word_3), H121 (word_4) | register value | unknown | unknown_word_order |
| Firmware | Storage (MIX Type) | H12 (high_word), H13 (middle_word), H14 (low_word) | register value | high_middle_low | source_explicit |
| Serial Number | Storage (MIX Type) | H23 (word_1), H24 (word_2), H25 (word_3), H26 (word_4), H27 (word_5) | serial_number | unknown | unknown_word_order |
| Inverter Model | Storage (MIX Type) | H28 (high_word), H29 (low_word) | register value | high_low | source_explicit |
| Serial Number | Storage (MIX Type) | H3001 (word_1), H3002 (word_2), H3003 (word_3), H3004 (word_4), H3005 (word_5), H3006 (word_6), H3007 (word_7), H3008 (word_8) | serial_number | unknown | unknown_word_order |
| Serial Number | Storage (MIX Type) | H3009 (word_1), H3010 (word_2), H3011 (word_3), H3012 (word_4), H3013 (word_5), H3014 (word_6), H3015 (word_7), H3016 (word_8) | register value | unknown | unknown_word_order |
| Register 3041 | Storage (MIX Type) | H3041 (word_1), H3042 (word_2) | register value | unknown | unknown_word_order |
| Register 3043 | Storage (MIX Type) | H3043 (word_1), H3044 (word_2) | register value | unknown | unknown_word_order |
| Register 3045 | Storage (MIX Type) | H3045 (word_1), H3046 (word_2) | register value | unknown | unknown_word_order |
| Register 3051 | Storage (MIX Type) | H3051 (word_1), H3052 (word_2) | register value | unknown | unknown_word_order |
| Register 3053 | Storage (MIX Type) | H3053 (word_1), H3054 (word_2) | register value | unknown | unknown_word_order |
| Register 3055 | Storage (MIX Type) | H3055 (word_1), H3056 (word_2) | register value | unknown | unknown_word_order |
| Register 3057 | Storage (MIX Type) | H3057 (word_1), H3058 (word_2) | register value | unknown | unknown_word_order |
| Register 3059 | Storage (MIX Type) | H3059 (word_1), H3060–H3069 (word_2) | register value | unknown | unknown_word_order |
| BatMdlSeria/ ParalNum | Storage (MIX Type) | H3071 (word_1), H3072 (word_2) | register value | unknown | unknown_word_order |
| Reserved | Storage (MIX Type) | H3073 (word_1), H3074 (word_2) | register value | unknown | unknown_word_order |
| Reserved | Storage (MIX Type) | H3075 (word_1), H3076 (word_2) | register value | unknown | unknown_word_order |
| Reserved | Storage (MIX Type) | H3077 (word_1), H3078 (word_2) | register value | unknown | unknown_word_order |
| Reserved | Storage (MIX Type) | H3083 (word_1), H3084 (word_2) | register value | unknown | unknown_word_order |
| Battery rack serial | Storage (MIX Type) | H3087 (word_1), H3088 (word_2), H3089 (word_3), H3090 (word_4), H3091 (word_5), H3092 (word_6), H3093 (word_7), H3094 (word_8) | register value | unknown | unknown_word_order |
| BDC monitoring code | Storage (MIX Type) | H3096 (word_1), H3097 (word_2) | register value | unknown | unknown_word_order |
| DSP firmware code | Storage (MIX Type) | H3099 (word_1), H3100 (word_2) | register value | unknown | unknown_word_order |
| Manufacturer information string | Storage (MIX Type) | H34 (word_1), H35 (word_2), H36 (word_3), H37 (word_4), H38 (word_5), H39 (word_6), H40 (word_7), H41 (word_8) | register value | unknown | unknown_word_order |
| Rated apparent power | Storage (MIX Type) | H6 (high_word), H7 (low_word) | register value | high_low | source_explicit |
| Controller firmware build string | Storage (MIX Type) | H82 (word_1), H83 (word_2), H84 (word_3), H85 (word_4), H86 (word_5), H87 (word_6) | register value | unknown | unknown_word_order |
| Firmware | Storage (MIX Type) | H9 (high_word), H10 (middle_word), H11 (low_word) | firmware_version | high_middle_low | source_explicit |
| PV total power | Storage (MIX Type) | I1 (word_1), I2 (word_2) | register value | unknown | unknown_word_order |
| Battery discharge power | Storage (MIX Type) | I1009 (high_word), I1010 (low_word) | register value | high_low | source_explicit |
| Battery charge power | Storage (MIX Type) | I1011 (high_word), I1012 (low_word) | register value | high_low | source_explicit |
| PactouserR H | Storage (MIX Type) | I1015 (high_word), I1016 (low_word) | register value | high_low | source_explicit |
| PactouserS H | Storage (MIX Type) | I1017 (high_word), I1018 (low_word) | register value | high_low | source_explicit |
| PactouserT H | Storage (MIX Type) | I1019 (high_word), I1020 (low_word) | register value | high_low | source_explicit |
| PactouserTotalH | Storage (MIX Type) | I1021 (high_word), I1022 (low_word) | register value | high_low | source_explicit |
| PactogridR H | Storage (MIX Type) | I1023 (high_word), I1024 (low_word) | register value | high_low | source_explicit |
| PactogridS H | Storage (MIX Type) | I1025 (high_word), I1026 (low_word) | register value | high_low | source_explicit |
| pac_to_grid_total | Storage (MIX Type) | I1029 (word_1), I1030 (word_2) | register value | unknown | unknown_word_order |
| OPFullwattH | Storage (MIX Type) | I102 (high_word), I103 (low_word) | register value | high_low | source_explicit |
| PLocalLoadR H | Storage (MIX Type) | I1031 (word_1), I1032 (word_2) | register value | unknown | unknown_word_order |
| PLocalLoadtotalH | Storage (MIX Type) | I1037 (word_1), I1038 (word_2) | register value | unknown | unknown_word_order |
| Etouser_todayH | Storage (MIX Type) | I1044 (high_word), I1045 (low_word) | register value | high_low | source_explicit |
| Etouser_totalH | Storage (MIX Type) | I1046 (high_word), I1047 (low_word) | register value | high_low | source_explicit |
| Etogrid_todayH | Storage (MIX Type) | I1048 (high_word), I1049 (low_word) | register value | high_low | source_explicit |
| Etogrid_totalH | Storage (MIX Type) | I1050 (high_word), I1051 (low_word) | register value | high_low | source_explicit |
| Edischarge1_toda yH | Storage (MIX Type) | I1052 (high_word), I1053 (low_word) | register value | high_low | source_explicit |
| Edischarge1_total H | Storage (MIX Type) | I1054 (high_word), I1055 (low_word) | register value | high_low | source_explicit |
| Echarge1_todayH | Storage (MIX Type) | I1056 (high_word), I1057 (low_word) | register value | high_low | source_explicit |
| Echarge1_totalH | Storage (MIX Type) | I1058 (high_word), I1059 (low_word) | register value | high_low | source_explicit |
| Register 1060 | Storage (MIX Type) | I1060 (word_1), I1061 (word_2) | register value | unknown | unknown_word_order |
| Register 1062 | Storage (MIX Type) | I1062 (word_1), I1063 (word_2) | register value | unknown | unknown_word_order |
| PV3 DC voltage | Storage (MIX Type) | I11 (word_1), I12 (word_2) | register value | unknown | unknown_word_order |
| Warning code | Storage (MIX Type) | I110 (word_1), I111 (word_2) | register value | unknown | unknown_word_order |
| AC charge Power_H | Storage (MIX Type) | I116 (high_word), I117 (low_word) | register value | high_low | source_explicit |
| PV total power | Storage (MIX Type) | I13 (word_1), I14 (word_2) | register value | unknown | unknown_word_order |
| PV4 DC voltage | Storage (MIX Type) | I15 (word_1), I16 (word_2) | register value | unknown | unknown_word_order |
| PV total power | Storage (MIX Type) | I17 (word_1), I18 (word_2) | register value | unknown | unknown_word_order |
| PV total power | Storage (MIX Type) | I21 (word_1), I22 (word_2) | register value | unknown | unknown_word_order |
| PV total power | Storage (MIX Type) | I25 (high_word), I26 (low_word) | register value | high_low | source_explicit |
| PV7 DC voltage | Storage (MIX Type) | I27 (word_1), I28 (word_2) | register value | unknown | unknown_word_order |
| PV total power | Storage (MIX Type) | I29 (high_word), I30 (low_word) | register value | high_low | source_explicit |
| PV1 DC voltage | Storage (MIX Type) | I3 (word_1), I4 (word_2) | register value | unknown | unknown_word_order |
| Grid import power | Storage (MIX Type) | I3041 (high_word), I3042 (low_word) | register value | high_low | source_explicit |
| Grid export power | Storage (MIX Type) | I3043 (high_word), I3044 (low_word) | register value | high_low | source_explicit |
| House load power | Storage (MIX Type) | I3045 (high_word), I3046 (low_word) | register value | high_low | source_explicit |
| Load energy today | Storage (MIX Type) | I3067 (word_1), I3068 (word_2) | register value | unknown | unknown_word_order |
| Load energy total | Storage (MIX Type) | I3069 (word_1), I3070 (word_2) | register value | unknown | unknown_word_order |
| Grid export power | Storage (MIX Type) | I3071 (word_1), I3072 (word_2) | register value | unknown | unknown_word_order |
| Grid export power | Storage (MIX Type) | I3073 (word_1), I3074 (word_2) | register value | unknown | unknown_word_order |
| PV8 DC voltage | Storage (MIX Type) | I31 (word_1), I32 (word_2) | register value | unknown | unknown_word_order |
| Battery discharge energy today | Storage (MIX Type) | I3125 (high_word), I3126 (low_word) | register value | high_low | source_explicit |
| Battery discharge energy total | Storage (MIX Type) | I3127 (high_word), I3128 (low_word) | register value | high_low | source_explicit |
| Battery charge energy today | Storage (MIX Type) | I3129 (high_word), I3130 (low_word) | register value | high_low | source_explicit |
| Battery charge energy total | Storage (MIX Type) | I3131 (high_word), I3132 (low_word) | register value | high_low | source_explicit |
| Battery discharge power | Storage (MIX Type) | I3178 (high_word), I3179 (low_word) | register value | high_low | source_explicit |
| Battery charge power | Storage (MIX Type) | I3180 (high_word), I3181 (low_word) | register value | high_low | source_explicit |
| PV total power | Storage (MIX Type) | I33 (high_word), I34 (low_word) | register value | high_low | source_explicit |
| AC output power | Storage (MIX Type) | I35 (high_word), I36 (low_word) | register value | high_low | source_explicit |
| Grid frequency | Storage (MIX Type) | I37 (word_1), I38 (word_2) | register value | unknown | unknown_word_order |
| AC phase L1 power | Storage (MIX Type) | I40 (high_word), I41 (low_word) | register value | high_low | source_explicit |
| AC phase L2 power | Storage (MIX Type) | I44 (high_word), I45 (low_word) | register value | high_low | source_explicit |
| AC phase L3 power | Storage (MIX Type) | I48 (high_word), I49 (low_word) | register value | high_low | source_explicit |
| PV total power | Storage (MIX Type) | I5 (word_1), I6 (word_2) | register value | unknown | unknown_word_order |
| Output energy today | Storage (MIX Type) | I53 (high_word), I54 (low_word) | register value | high_low | source_explicit |
| Output energy total | Storage (MIX Type) | I55 (high_word), I56 (low_word) | register value | high_low | source_explicit |
| Inverter runtime | Storage (MIX Type) | I57 (high_word), I58 (low_word) | register value | high_low | source_explicit |
| PV1 energy today | Storage (MIX Type) | I59 (high_word), I60 (low_word) | register value | high_low | source_explicit |
| PV1 energy total | Storage (MIX Type) | I61 (high_word), I62 (low_word) | register value | high_low | source_explicit |
| PV2 energy today | Storage (MIX Type) | I63 (high_word), I64 (low_word) | register value | high_low | source_explicit |
| PV2 energy total | Storage (MIX Type) | I65 (high_word), I66 (low_word) | register value | high_low | source_explicit |
| PV3 energy today | Storage (MIX Type) | I67 (high_word), I68 (low_word) | register value | high_low | source_explicit |
| PV3 energy total | Storage (MIX Type) | I69 (high_word), I70 (low_word) | register value | high_low | source_explicit |
| PV4 energy today | Storage (MIX Type) | I71 (high_word), I72 (low_word) | register value | high_low | source_explicit |
| PV4 energy total | Storage (MIX Type) | I73 (high_word), I74 (low_word) | register value | high_low | source_explicit |
| PV5 energy today | Storage (MIX Type) | I75 (high_word), I76 (low_word) | register value | high_low | source_explicit |
| PV5 energy total | Storage (MIX Type) | I77 (high_word), I78 (low_word) | register value | high_low | source_explicit |
| PV6 energy today | Storage (MIX Type) | I79 (high_word), I80 (low_word) | register value | high_low | source_explicit |
| PV6 energy total | Storage (MIX Type) | I81 (high_word), I82 (low_word) | register value | high_low | source_explicit |
| PV7 energy today | Storage (MIX Type) | I83 (high_word), I84 (low_word) | register value | high_low | source_explicit |
| PV7 energy total | Storage (MIX Type) | I85 (high_word), I86 (low_word) | register value | high_low | source_explicit |
| PV8 energy today | Storage (MIX Type) | I87 (high_word), I88 (low_word) | register value | high_low | source_explicit |
| PV8 energy total | Storage (MIX Type) | I89 (high_word), I90 (low_word) | register value | high_low | source_explicit |
| PV total power | Storage (MIX Type) | I9 (word_1), I10 (word_2) | register value | unknown | unknown_word_order |
| PV energy total | Storage (MIX Type) | I91 (high_word), I92 (low_word) | register value | high_low | source_explicit |
| Module code segments | Storage (SPA Type) | H118 (word_1), H119 (word_2), H120 (word_3), H121 (word_4) | register value | unknown | unknown_word_order |
| Firmware | Storage (SPA Type) | H12 (high_word), H13 (middle_word), H14 (low_word) | register value | high_middle_low | source_explicit |
| Serial Number | Storage (SPA Type) | H23 (word_1), H24 (word_2), H25 (word_3), H26 (word_4), H27 (word_5) | serial_number | unknown | unknown_word_order |
| Inverter Model | Storage (SPA Type) | H28 (high_word), H29 (low_word) | register value | high_low | source_explicit |
| Manufacturer information string | Storage (SPA Type) | H34 (word_1), H35 (word_2), H36 (word_3), H37 (word_4), H38 (word_5), H39 (word_6), H40 (word_7), H41 (word_8) | register value | unknown | unknown_word_order |
| Rated apparent power | Storage (SPA Type) | H6 (high_word), H7 (low_word) | register value | high_low | source_explicit |
| Controller firmware build string | Storage (SPA Type) | H82 (word_1), H83 (word_2), H84 (word_3), H85 (word_4), H86 (word_5), H87 (word_6) | register value | unknown | unknown_word_order |
| Firmware | Storage (SPA Type) | H9 (high_word), H10 (middle_word), H11 (low_word) | firmware_version | high_middle_low | source_explicit |
| Battery discharge power | Storage (SPA Type) | I1009 (high_word), I1010 (low_word) | register value | high_low | source_explicit |
| Battery charge power | Storage (SPA Type) | I1011 (high_word), I1012 (low_word) | register value | high_low | source_explicit |
| PactouserR H | Storage (SPA Type) | I1015 (high_word), I1016 (low_word) | register value | high_low | source_explicit |
| PactouserS H | Storage (SPA Type) | I1017 (high_word), I1018 (low_word) | register value | high_low | source_explicit |
| PactouserT H | Storage (SPA Type) | I1019 (high_word), I1020 (low_word) | register value | high_low | source_explicit |
| PactouserTotalH | Storage (SPA Type) | I1021 (high_word), I1022 (low_word) | register value | high_low | source_explicit |
| PactogridR H | Storage (SPA Type) | I1023 (high_word), I1024 (low_word) | register value | high_low | source_explicit |
| PactogridS H | Storage (SPA Type) | I1025 (high_word), I1026 (low_word) | register value | high_low | source_explicit |
| pac_to_grid_total | Storage (SPA Type) | I1029 (word_1), I1030 (word_2) | register value | unknown | unknown_word_order |
| PLocalLoadR H | Storage (SPA Type) | I1031 (word_1), I1032 (word_2) | register value | unknown | unknown_word_order |
| PLocalLoadtotalH | Storage (SPA Type) | I1037 (word_1), I1038 (word_2) | register value | unknown | unknown_word_order |
| Etouser_todayH | Storage (SPA Type) | I1044 (high_word), I1045 (low_word) | register value | high_low | source_explicit |
| Etouser_totalH | Storage (SPA Type) | I1046 (high_word), I1047 (low_word) | register value | high_low | source_explicit |
| Etogrid_todayH | Storage (SPA Type) | I1048 (high_word), I1049 (low_word) | register value | high_low | source_explicit |
| Etogrid_totalH | Storage (SPA Type) | I1050 (high_word), I1051 (low_word) | register value | high_low | source_explicit |
| Edischarge1_toda yH | Storage (SPA Type) | I1052 (high_word), I1053 (low_word) | register value | high_low | source_explicit |
| Edischarge1_total H | Storage (SPA Type) | I1054 (high_word), I1055 (low_word) | register value | high_low | source_explicit |
| Echarge1_todayH | Storage (SPA Type) | I1056 (high_word), I1057 (low_word) | register value | high_low | source_explicit |
| Echarge1_totalH | Storage (SPA Type) | I1058 (high_word), I1059 (low_word) | register value | high_low | source_explicit |
| Register 1060 | Storage (SPA Type) | I1060 (word_1), I1061 (word_2) | register value | unknown | unknown_word_order |
| Register 1062 | Storage (SPA Type) | I1062 (word_1), I1063 (word_2) | register value | unknown | unknown_word_order |
| ACCharge EnergyTodayH | Storage (SPA Type) | I1124 (high_word), I1125 (low_word) | register value | high_low | source_explicit |
| A1CCharge EnergyTotalH | Storage (SPA Type) | I1126 (word_1), I1127 (word_2) | register value | unknown | unknown_word_order |
| AC Charge Power H | Storage (SPA Type) | I1128 (high_word), I1129 (low_word) | register value | high_low | source_explicit |
| Extra AC Power to grid_H | Storage (SPA Type) | I1131 (high_word), I1132 (low_word) | register value | high_low | source_explicit |
| Eextra_todayH | Storage (SPA Type) | I1133 (high_word), I1134 (low_word) | register value | high_low | source_explicit |
| Eextra_totalH | Storage (SPA Type) | I1135 (high_word), I1136 (low_word) | register value | high_low | source_explicit |
| Esystem_today H | Storage (SPA Type) | I1137 (high_word), I1138 (low_word) | register value | high_low | source_explicit |
| Esystem_totalH | Storage (SPA Type) | I1139 (high_word), I1140 (low_word) | register value | high_low | source_explicit |
| Eself_todayH | Storage (SPA Type) | I1141 (high_word), I1142 (low_word) | register value | high_low | source_explicit |
| Eself_totalH | Storage (SPA Type) | I1143 (high_word), I1144 (low_word) | register value | high_low | source_explicit |
| PSystemH | Storage (SPA Type) | I1145 (high_word), I1146 (low_word) | register value | high_low | source_explicit |
| PSelfH | Storage (SPA Type) | I1147 (high_word), I1148 (low_word) | register value | high_low | source_explicit |
| EPVAll_TodayH | Storage (SPA Type) | I1149 (high_word), I1150 (low_word) | register value | high_low | source_explicit |
| Accdischarge power_H | Storage (SPA Type) | I1152 (high_word), I1153 (low_word) | register value | high_low | source_explicit |
| AccCharge power_H | Storage (SPA Type) | I1155 (high_word), I1156 (low_word) | register value | high_low | source_explicit |
| EactotalH | Storage (SPA Type) | I2055 (high_word), I2056 (low_word) | register value | high_low | source_explicit |
| TimetotalH | Storage (SPA Type) | I2057 (high_word), I2058 (low_word) | register value | high_low | source_explicit |
| EACharge_Today _H | Storage (SPA Type) | I2112 (high_word), I2113 (low_word) | register value | high_low | source_explicit |
| EACharge_Total _H | Storage (SPA Type) | I2114 (high_word), I2115 (low_word) | register value | high_low | source_explicit |
| Module code segments | Storage (SPH Type) | H118 (word_1), H119 (word_2), H120 (word_3), H121 (word_4) | register value | unknown | unknown_word_order |
| Firmware | Storage (SPH Type) | H12 (high_word), H13 (middle_word), H14 (low_word) | register value | high_middle_low | source_explicit |
| Serial Number | Storage (SPH Type) | H23 (word_1), H24 (word_2), H25 (word_3), H26 (word_4), H27 (word_5) | serial_number | unknown | unknown_word_order |
| Inverter Model | Storage (SPH Type) | H28 (high_word), H29 (low_word) | register value | high_low | source_explicit |
| Manufacturer information string | Storage (SPH Type) | H34 (word_1), H35 (word_2), H36 (word_3), H37 (word_4), H38 (word_5), H39 (word_6), H40 (word_7), H41 (word_8) | register value | unknown | unknown_word_order |
| Rated apparent power | Storage (SPH Type) | H6 (high_word), H7 (low_word) | register value | high_low | source_explicit |
| Controller firmware build string | Storage (SPH Type) | H82 (word_1), H83 (word_2), H84 (word_3), H85 (word_4), H86 (word_5), H87 (word_6) | register value | unknown | unknown_word_order |
| Firmware | Storage (SPH Type) | H9 (high_word), H10 (middle_word), H11 (low_word) | firmware_version | high_middle_low | source_explicit |
| PV total power | Storage (SPH Type) | I1 (word_1), I2 (word_2) | register value | unknown | unknown_word_order |
| Battery discharge power | Storage (SPH Type) | I1009 (high_word), I1010 (low_word) | register value | high_low | source_explicit |
| Battery charge power | Storage (SPH Type) | I1011 (high_word), I1012 (low_word) | register value | high_low | source_explicit |
| PactouserR H | Storage (SPH Type) | I1015 (high_word), I1016 (low_word) | register value | high_low | source_explicit |
| PactouserS H | Storage (SPH Type) | I1017 (high_word), I1018 (low_word) | register value | high_low | source_explicit |
| PactouserT H | Storage (SPH Type) | I1019 (high_word), I1020 (low_word) | register value | high_low | source_explicit |
| PactouserTotalH | Storage (SPH Type) | I1021 (high_word), I1022 (low_word) | register value | high_low | source_explicit |
| PactogridR H | Storage (SPH Type) | I1023 (high_word), I1024 (low_word) | register value | high_low | source_explicit |
| PactogridS H | Storage (SPH Type) | I1025 (high_word), I1026 (low_word) | register value | high_low | source_explicit |
| pac_to_grid_total | Storage (SPH Type) | I1029 (word_1), I1030 (word_2) | register value | unknown | unknown_word_order |
| OPFullwattH | Storage (SPH Type) | I102 (high_word), I103 (low_word) | register value | high_low | source_explicit |
| PLocalLoadR H | Storage (SPH Type) | I1031 (word_1), I1032 (word_2) | register value | unknown | unknown_word_order |
| PLocalLoadtotalH | Storage (SPH Type) | I1037 (word_1), I1038 (word_2) | register value | unknown | unknown_word_order |
| Etouser_todayH | Storage (SPH Type) | I1044 (high_word), I1045 (low_word) | register value | high_low | source_explicit |
| Etouser_totalH | Storage (SPH Type) | I1046 (high_word), I1047 (low_word) | register value | high_low | source_explicit |
| Etogrid_todayH | Storage (SPH Type) | I1048 (high_word), I1049 (low_word) | register value | high_low | source_explicit |
| Etogrid_totalH | Storage (SPH Type) | I1050 (high_word), I1051 (low_word) | register value | high_low | source_explicit |
| Edischarge1_toda yH | Storage (SPH Type) | I1052 (high_word), I1053 (low_word) | register value | high_low | source_explicit |
| Edischarge1_total H | Storage (SPH Type) | I1054 (high_word), I1055 (low_word) | register value | high_low | source_explicit |
| Echarge1_todayH | Storage (SPH Type) | I1056 (high_word), I1057 (low_word) | register value | high_low | source_explicit |
| Echarge1_totalH | Storage (SPH Type) | I1058 (high_word), I1059 (low_word) | register value | high_low | source_explicit |
| Register 1060 | Storage (SPH Type) | I1060 (word_1), I1061 (word_2) | register value | unknown | unknown_word_order |
| Register 1062 | Storage (SPH Type) | I1062 (word_1), I1063 (word_2) | register value | unknown | unknown_word_order |
| PV3 DC voltage | Storage (SPH Type) | I11 (word_1), I12 (word_2) | register value | unknown | unknown_word_order |
| Warning code | Storage (SPH Type) | I110 (word_1), I111 (word_2) | register value | unknown | unknown_word_order |
| ACCharge EnergyTodayH | Storage (SPH Type) | I1124 (high_word), I1125 (low_word) | register value | high_low | source_explicit |
| A1CCharge EnergyTotalH | Storage (SPH Type) | I1126 (word_1), I1127 (word_2) | register value | unknown | unknown_word_order |
| Extra AC Power to grid_H | Storage (SPH Type) | I1131 (high_word), I1132 (low_word) | register value | high_low | source_explicit |
| Eextra_todayH | Storage (SPH Type) | I1133 (high_word), I1134 (low_word) | register value | high_low | source_explicit |
| Eextra_totalH | Storage (SPH Type) | I1135 (high_word), I1136 (low_word) | register value | high_low | source_explicit |
| Esystem_today H | Storage (SPH Type) | I1137 (high_word), I1138 (low_word) | register value | high_low | source_explicit |
| Esystem_totalH | Storage (SPH Type) | I1139 (high_word), I1140 (low_word) | register value | high_low | source_explicit |
| Eself_todayH | Storage (SPH Type) | I1141 (high_word), I1142 (low_word) | register value | high_low | source_explicit |
| Eself_totalH | Storage (SPH Type) | I1143 (high_word), I1144 (low_word) | register value | high_low | source_explicit |
| PSystemH | Storage (SPH Type) | I1145 (high_word), I1146 (low_word) | register value | high_low | source_explicit |
| PSelfH | Storage (SPH Type) | I1147 (high_word), I1148 (low_word) | register value | high_low | source_explicit |
| EPVAll_TodayH | Storage (SPH Type) | I1149 (high_word), I1150 (low_word) | register value | high_low | source_explicit |
| Accdischarge power_H | Storage (SPH Type) | I1152 (high_word), I1153 (low_word) | register value | high_low | source_explicit |
| AccCharge power_H | Storage (SPH Type) | I1155 (high_word), I1156 (low_word) | register value | high_low | source_explicit |
| AC charge Power_H | Storage (SPH Type) | I116 (high_word), I117 (low_word) | register value | high_low | source_explicit |
| PV total power | Storage (SPH Type) | I13 (word_1), I14 (word_2) | register value | unknown | unknown_word_order |
| PV4 DC voltage | Storage (SPH Type) | I15 (word_1), I16 (word_2) | register value | unknown | unknown_word_order |
| PV total power | Storage (SPH Type) | I17 (word_1), I18 (word_2) | register value | unknown | unknown_word_order |
| PV total power | Storage (SPH Type) | I21 (word_1), I22 (word_2) | register value | unknown | unknown_word_order |
| PV total power | Storage (SPH Type) | I25 (high_word), I26 (low_word) | register value | high_low | source_explicit |
| PV7 DC voltage | Storage (SPH Type) | I27 (word_1), I28 (word_2) | register value | unknown | unknown_word_order |
| PV total power | Storage (SPH Type) | I29 (high_word), I30 (low_word) | register value | high_low | source_explicit |
| PV1 DC voltage | Storage (SPH Type) | I3 (word_1), I4 (word_2) | register value | unknown | unknown_word_order |
| PV8 DC voltage | Storage (SPH Type) | I31 (word_1), I32 (word_2) | register value | unknown | unknown_word_order |
| PV total power | Storage (SPH Type) | I33 (high_word), I34 (low_word) | register value | high_low | source_explicit |
| AC output power | Storage (SPH Type) | I35 (high_word), I36 (low_word) | register value | high_low | source_explicit |
| Grid frequency | Storage (SPH Type) | I37 (word_1), I38 (word_2) | register value | unknown | unknown_word_order |
| AC phase L1 power | Storage (SPH Type) | I40 (high_word), I41 (low_word) | register value | high_low | source_explicit |
| AC phase L2 power | Storage (SPH Type) | I44 (high_word), I45 (low_word) | register value | high_low | source_explicit |
| AC phase L3 power | Storage (SPH Type) | I48 (high_word), I49 (low_word) | register value | high_low | source_explicit |
| PV total power | Storage (SPH Type) | I5 (word_1), I6 (word_2) | register value | unknown | unknown_word_order |
| Output energy today | Storage (SPH Type) | I53 (high_word), I54 (low_word) | register value | high_low | source_explicit |
| Output energy total | Storage (SPH Type) | I55 (high_word), I56 (low_word) | register value | high_low | source_explicit |
| Inverter runtime | Storage (SPH Type) | I57 (high_word), I58 (low_word) | register value | high_low | source_explicit |
| PV1 energy today | Storage (SPH Type) | I59 (high_word), I60 (low_word) | register value | high_low | source_explicit |
| PV1 energy total | Storage (SPH Type) | I61 (high_word), I62 (low_word) | register value | high_low | source_explicit |
| PV2 energy today | Storage (SPH Type) | I63 (high_word), I64 (low_word) | register value | high_low | source_explicit |
| PV2 energy total | Storage (SPH Type) | I65 (high_word), I66 (low_word) | register value | high_low | source_explicit |
| PV3 energy today | Storage (SPH Type) | I67 (high_word), I68 (low_word) | register value | high_low | source_explicit |
| PV3 energy total | Storage (SPH Type) | I69 (high_word), I70 (low_word) | register value | high_low | source_explicit |
| PV4 energy today | Storage (SPH Type) | I71 (high_word), I72 (low_word) | register value | high_low | source_explicit |
| PV4 energy total | Storage (SPH Type) | I73 (high_word), I74 (low_word) | register value | high_low | source_explicit |
| PV5 energy today | Storage (SPH Type) | I75 (high_word), I76 (low_word) | register value | high_low | source_explicit |
| PV5 energy total | Storage (SPH Type) | I77 (high_word), I78 (low_word) | register value | high_low | source_explicit |
| PV6 energy today | Storage (SPH Type) | I79 (high_word), I80 (low_word) | register value | high_low | source_explicit |
| PV6 energy total | Storage (SPH Type) | I81 (high_word), I82 (low_word) | register value | high_low | source_explicit |
| PV7 energy today | Storage (SPH Type) | I83 (high_word), I84 (low_word) | register value | high_low | source_explicit |
| PV7 energy total | Storage (SPH Type) | I85 (high_word), I86 (low_word) | register value | high_low | source_explicit |
| PV8 energy today | Storage (SPH Type) | I87 (high_word), I88 (low_word) | register value | high_low | source_explicit |
| PV8 energy total | Storage (SPH Type) | I89 (high_word), I90 (low_word) | register value | high_low | source_explicit |
| PV total power | Storage (SPH Type) | I9 (word_1), I10 (word_2) | register value | unknown | unknown_word_order |
| PV energy total | Storage (SPH Type) | I91 (high_word), I92 (low_word) | register value | high_low | source_explicit |
| Module code segments | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | H118 (word_1), H119 (word_2), H120 (word_3), H121 (word_4) | register value | unknown | unknown_word_order |
| Inverter type identifier | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | H125 (word_1), H126 (word_2), H127 (word_3), H128 (word_4), H129 (word_5), H130 (word_6), H131 (word_7), H132 (word_8) | register value | unknown | unknown_word_order |
| Firmware | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | H12 (high_word), H13 (middle_word), H14 (low_word) | register value | high_middle_low | source_explicit |
| Bootloader identifier string | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | H133 (word_1), H134 (word_2), H135 (word_3), H136 (word_4) | register value | unknown | unknown_word_order |
| Reactive power direct-control setpoint | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | H137 (high_word), H138 (low_word) | register value | high_low | source_explicit |
| Alternate serial number | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | H209 (word_1), H210 (word_2), H211 (word_3), H212 (word_4), H213 (word_5), H214 (word_6), H215 (word_7), H216 (word_8) | register value | unknown | unknown_word_order |
| Serial Number | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | H23 (word_1), H24 (word_2), H25 (word_3), H26 (word_4), H27 (word_5) | serial_number | unknown | unknown_word_order |
| Inverter Model | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | H28 (high_word), H29 (low_word) | register value | high_low | source_explicit |
| Manufacturer information string | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | H34 (word_1), H35 (word_2), H36 (word_3), H37 (word_4), H38 (word_5), H39 (word_6), H40 (word_7), H41 (word_8) | register value | unknown | unknown_word_order |
| Rated apparent power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | H6 (high_word), H7 (low_word) | register value | high_low | source_explicit |
| Controller firmware build string | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | H82 (word_1), H83 (word_2), H84 (word_3), H85 (word_4), H86 (word_5), H87 (word_6) | register value | unknown | unknown_word_order |
| Firmware | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | H9 (high_word), H10 (middle_word), H11 (low_word) | firmware_version | high_middle_low | source_explicit |
| PV total power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I1 (word_1), I2 (word_2) | register value | unknown | unknown_word_order |
| OPFullwattH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I102 (high_word), I103 (low_word) | register value | high_low | source_explicit |
| PV3 DC voltage | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I11 (word_1), I12 (word_2) | register value | unknown | unknown_word_order |
| Warning code | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I110 (word_1), I111 (word_2) | register value | unknown | unknown_word_order |
| AC charge Power_H | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I116 (high_word), I117 (low_word) | register value | high_low | source_explicit |
| PV total power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I13 (word_1), I14 (word_2) | register value | unknown | unknown_word_order |
| PV4 DC voltage | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I15 (word_1), I16 (word_2) | register value | unknown | unknown_word_order |
| PV total power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I17 (word_1), I18 (word_2) | register value | unknown | unknown_word_order |
| PV total power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I21 (word_1), I22 (word_2) | register value | unknown | unknown_word_order |
| CT_Q_RH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I210 (high_word), I211 (low_word) | register value | high_low | source_explicit |
| CT_Q_SH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I212 (high_word), I213 (low_word) | register value | high_low | source_explicit |
| CT_Q_TH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I214 (high_word), I215 (low_word) | register value | high_low | source_explicit |
| COMP_Q_RH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I219 (high_word), I220 (low_word) | register value | high_low | source_explicit |
| COMP_Q_SH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I221 (high_word), I222 (low_word) | register value | high_low | source_explicit |
| COMP_Q_TH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I223 (high_word), I224 (low_word) | register value | high_low | source_explicit |
| SacH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I230 (high_word), I231 (low_word) | register value | high_low | source_explicit |
| ReActPowerH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I232 (high_word), I233 (low_word) | register value | high_low | source_explicit |
| Output reactive power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I234 (high_word), I235 (low_word) | register value | high_low | source_explicit |
| Reactive energy total | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I236 (high_word), I237 (low_word) | register value | high_low | source_explicit |
| PV total power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I25 (high_word), I26 (low_word) | register value | high_low | source_explicit |
| PV7 DC voltage | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I27 (word_1), I28 (word_2) | register value | unknown | unknown_word_order |
| PV total power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I29 (high_word), I30 (low_word) | register value | high_low | source_explicit |
| PV1 DC voltage | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I3 (word_1), I4 (word_2) | register value | unknown | unknown_word_order |
| PV8 DC voltage | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I31 (word_1), I32 (word_2) | register value | unknown | unknown_word_order |
| PV total power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I33 (high_word), I34 (low_word) | register value | high_low | source_explicit |
| AC output power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I35 (high_word), I36 (low_word) | register value | high_low | source_explicit |
| Grid frequency | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I37 (word_1), I38 (word_2) | register value | unknown | unknown_word_order |
| AC phase L1 power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I40 (high_word), I41 (low_word) | register value | high_low | source_explicit |
| AC phase L2 power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I44 (high_word), I45 (low_word) | register value | high_low | source_explicit |
| AC phase L3 power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I48 (high_word), I49 (low_word) | register value | high_low | source_explicit |
| PV total power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I5 (word_1), I6 (word_2) | register value | unknown | unknown_word_order |
| Output energy today | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I53 (high_word), I54 (low_word) | register value | high_low | source_explicit |
| Output energy total | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I55 (high_word), I56 (low_word) | register value | high_low | source_explicit |
| Inverter runtime | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I57 (high_word), I58 (low_word) | register value | high_low | source_explicit |
| PV1 energy today | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I59 (high_word), I60 (low_word) | register value | high_low | source_explicit |
| PV1 energy total | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I61 (high_word), I62 (low_word) | register value | high_low | source_explicit |
| PV2 energy today | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I63 (high_word), I64 (low_word) | register value | high_low | source_explicit |
| PV2 energy total | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I65 (high_word), I66 (low_word) | register value | high_low | source_explicit |
| PV3 energy today | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I67 (high_word), I68 (low_word) | register value | high_low | source_explicit |
| PV3 energy total | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I69 (high_word), I70 (low_word) | register value | high_low | source_explicit |
| PV4 energy today | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I71 (high_word), I72 (low_word) | register value | high_low | source_explicit |
| PV4 energy total | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I73 (high_word), I74 (low_word) | register value | high_low | source_explicit |
| PV5 energy today | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I75 (high_word), I76 (low_word) | register value | high_low | source_explicit |
| PV5 energy total | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I77 (high_word), I78 (low_word) | register value | high_low | source_explicit |
| PV6 energy today | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I79 (high_word), I80 (low_word) | register value | high_low | source_explicit |
| PV6 energy total | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I81 (high_word), I82 (low_word) | register value | high_low | source_explicit |
| PV7 energy today | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I83 (high_word), I84 (low_word) | register value | high_low | source_explicit |
| PV7 energy total | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I85 (high_word), I86 (low_word) | register value | high_low | source_explicit |
| Ppv9H | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I877 (high_word), I878 (low_word) | register value | high_low | source_explicit |
| PV8 energy today | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I87 (high_word), I88 (low_word) | register value | high_low | source_explicit |
| Ppv10H | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I881 (high_word), I882 (low_word) | register value | high_low | source_explicit |
| Ppv11H | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I885 (high_word), I886 (low_word) | register value | high_low | source_explicit |
| Ppv12H | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I889 (high_word), I890 (low_word) | register value | high_low | source_explicit |
| Ppv13H | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I893 (high_word), I894 (low_word) | register value | high_low | source_explicit |
| Ppv14H | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I897 (high_word), I898 (low_word) | register value | high_low | source_explicit |
| PV8 energy total | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I89 (high_word), I90 (low_word) | register value | high_low | source_explicit |
| PV total power | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I9 (word_1), I10 (word_2) | register value | unknown | unknown_word_order |
| Ppv15H | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I901 (high_word), I902 (low_word) | register value | high_low | source_explicit |
| Ppv16H | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I905 (high_word), I906 (low_word) | register value | high_low | source_explicit |
| Epv9_todayH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I907 (high_word), I908 (low_word) | register value | high_low | source_explicit |
| Epv9_totalH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I909 (high_word), I910 (low_word) | register value | high_low | source_explicit |
| Epv10_todayH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I911 (high_word), I912 (low_word) | register value | high_low | source_explicit |
| Epv10_totalH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I913 (high_word), I914 (low_word) | register value | high_low | source_explicit |
| Epv11_todayH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I915 (high_word), I916 (low_word) | register value | high_low | source_explicit |
| Epv11_totalH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I917 (high_word), I918 (low_word) | register value | high_low | source_explicit |
| Epv12_todayH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I919 (high_word), I920 (low_word) | register value | high_low | source_explicit |
| PV energy total | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I91 (high_word), I92 (low_word) | register value | high_low | source_explicit |
| Epv12_totalH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I921 (high_word), I922 (low_word) | register value | high_low | source_explicit |
| Epv13_todayH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I923 (high_word), I924 (low_word) | register value | high_low | source_explicit |
| Epv13_totalH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I925 (high_word), I926 (low_word) | register value | high_low | source_explicit |
| Epv14_todayH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I927 (high_word), I928 (low_word) | register value | high_low | source_explicit |
| Epv14_totalH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I929 (high_word), I930 (low_word) | register value | high_low | source_explicit |
| Epv15_todayH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I931 (high_word), I932 (low_word) | register value | high_low | source_explicit |
| Epv15_totalH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I933 (high_word), I934 (low_word) | register value | high_low | source_explicit |
| Epv16_todayH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I935 (high_word), I936 (low_word) | register value | high_low | source_explicit |
| Epv16_totalH | MAX 1500V/MAX-X LV/TL3-X (MAX, MID, MAC Type) | I937 (high_word), I938 (low_word) | register value | high_low | source_explicit |
