# MAX 1500V/MAX-X LV / TL3-X (MAX, MID, MAC Type)

`v124-instruction-tl3-max-mid-mac`: TL3-X (MAX, MID, MAC Type): 03 register range: 0~124, 125~249; 04 register range: 0~124, 125~249

`v124-instruction-max-1500v-max-x-lv`: MAX 1500V, MAX-X LV: 03 register range: 0~124, 125~249; 04 register range: 0~124, 125~249, 875~999

| Applicability path | Resolved block |
| --- | --- |
| v124-holding-p009-first_group-block-01:v124-instruction-max-1500v-max-x-lv:holding:0:124:3 | declared/no semantic block |
| v124-holding-p009-first_group-block-01:v124-instruction-tl3-max-mid-mac:holding:0:124:3 | declared/no semantic block |
| v124-holding-p016-second_group-block-02:v124-instruction-max-1500v-max-x-lv:holding:125:249:3 | declared/no semantic block |
| v124-holding-p016-second_group-block-02:v124-instruction-tl3-max-mid-mac:holding:125:249:3 | declared/no semantic block |
| v124-input-p047-first_group-block-07:v124-instruction-max-1500v-max-x-lv:input:0:124:4 | declared/no semantic block |
| v124-input-p047-first_group-block-07:v124-instruction-tl3-max-mid-mac:input:0:124:4 | declared/no semantic block |
| v124-input-p051-second_group-block-08:v124-instruction-max-1500v-max-x-lv:input:125:249:4 | declared/no semantic block |
| v124-input-p051-second_group-block-08:v124-instruction-tl3-max-mid-mac:input:125:249:4 | declared/no semantic block |
| v124-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:v124-instruction-max-1500v-max-x-lv:input:875:999:4 | declared/no semantic block |

Block projections: `cb-holding-p009-first_group-block-01`, `cb-holding-p016-second_group-block-02`, `cb-input-p047-first_group-block-07`, `cb-input-p051-second_group-block-08`, `cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09`. Register rows below are references to shared block definitions; applicability does not duplicate them.

| Register | Table | Address | Semantic key | Name | Access |
| --- | --- | --- | --- | --- | --- |
| cb-holding-p009-first_group-block-01:holding:0 | holding | 0 | control.inverter_enable_flags | Inverter enable flags | read_write |
| cb-holding-p009-first_group-block-01:holding:1 | holding | 1 | control.safety_function_enable_flags | Safety function enable flags | write |
| cb-holding-p009-first_group-block-01:holding:10 | holding | 10 | field.firmware | Firmware (middle word) | read |
| cb-holding-p009-first_group-block-01:holding:100 | holding | 100 | control.power_factor_curve_lock_out_voltage | Power-factor curve lock-out voltage | write |
| cb-holding-p009-first_group-block-01:holding:101 | holding | 101 | control.power_factor_adjust_value_1 | Power-factor adjust value 1 | write |
| cb-holding-p009-first_group-block-01:holding:102 | holding | 102 | control.power_factor_adjust_value_2 | Power-factor adjust value 2 | write |
| cb-holding-p009-first_group-block-01:holding:103 | holding | 103 | control.power_factor_adjust_value_3 | Power-factor adjust value 3 | write |
| cb-holding-p009-first_group-block-01:holding:104 | holding | 104 | control.power_factor_adjust_value_4 | Power-factor adjust value 4 | write |
| cb-holding-p009-first_group-block-01:holding:105 | holding | 105 | control.power_factor_adjust_value_5 | Power-factor adjust value 5 | write |
| cb-holding-p009-first_group-block-01:holding:106 | holding | 106 | control.power_factor_adjust_value_6 | Power-factor adjust value 6 | write |
| cb-holding-p009-first_group-block-01:holding:107 | holding | 107 | control.q_v_response_delay | Q(V) response delay | write |
| cb-holding-p009-first_group-block-01:holding:108 | holding | 108 | control.over_frequency_derating_delay | Over-frequency derating delay | write |
| cb-holding-p009-first_group-block-01:holding:109 | holding | 109 | control.maximum_reactive_power_magnitude | Maximum reactive power magnitude | write |
| cb-holding-p009-first_group-block-01:holding:11 | holding | 11 | field.firmware | Firmware (low word) | read |
| cb-holding-p009-first_group-block-01:holding:110 | holding | 110 | control.pf_curve_point_1_load | PF curve point 1 load | write |
| cb-holding-p009-first_group-block-01:holding:111 | holding | 111 | control.pf_curve_point_1_target | PF curve point 1 target | write |
| cb-holding-p009-first_group-block-01:holding:112 | holding | 112 | control.pf_curve_point_2_load | PF curve point 2 load | write |
| cb-holding-p009-first_group-block-01:holding:113 | holding | 113 | control.pf_curve_point_2_target | PF curve point 2 target | write |
| cb-holding-p009-first_group-block-01:holding:114 | holding | 114 | control.pf_curve_point_3_load | PF curve point 3 load | write |
| cb-holding-p009-first_group-block-01:holding:115 | holding | 115 | control.pf_curve_point_3_target | PF curve point 3 target | write |
| cb-holding-p009-first_group-block-01:holding:116 | holding | 116 | control.pf_curve_point_4_load | PF curve point 4 load | write |
| cb-holding-p009-first_group-block-01:holding:117 | holding | 117 | control.pf_curve_point_4_target | PF curve point 4 target | write |
| cb-holding-p009-first_group-block-01:holding:118 | holding | 118 | field.module_code_segments | Module code segments | read |
| cb-holding-p009-first_group-block-01:holding:119 | holding | 119 | field.module_code_segments | Module code segments | read |
| cb-holding-p009-first_group-block-01:holding:12 | holding | 12 | field.firmware | Firmware (high word) | read |
| cb-holding-p009-first_group-block-01:holding:120 | holding | 120 | field.module_code_segments | Module code segments | read |
| cb-holding-p009-first_group-block-01:holding:121 | holding | 121 | field.module_code_segments | Module code segments | read |
| cb-holding-p009-first_group-block-01:holding:122 | holding | 122 | control.export_limit_enable_mode | Export limit enable mode | read_write |
| cb-holding-p009-first_group-block-01:holding:123 | holding | 123 | control.export_limit_power_setpoint | Export limit power setpoint | read_write |
| cb-holding-p009-first_group-block-01:holding:124 | holding | 124 | control.tracker_coupling_mode | Tracker coupling mode | write |
| cb-holding-p009-first_group-block-01:holding:13 | holding | 13 | field.firmware | Firmware (middle word) | read |
| cb-holding-p009-first_group-block-01:holding:14 | holding | 14 | field.firmware | Firmware (low word) | read |
| cb-holding-p009-first_group-block-01:holding:15 | holding | 15 | control.lcd_language_selection | LCD language selection | write |
| cb-holding-p009-first_group-block-01:holding:16 | holding | 16 | control.country_profile_configured | Country profile configured | write |
| cb-holding-p009-first_group-block-01:holding:17 | holding | 17 | control.pv_start_voltage_threshold | PV start voltage threshold | write |
| cb-holding-p009-first_group-block-01:holding:18 | holding | 18 | control.start_up_delay | Start-up delay | write |
| cb-holding-p009-first_group-block-01:holding:19 | holding | 19 | control.restart_delay | Restart delay | write |
| cb-holding-p009-first_group-block-01:holding:2 | holding | 2 | control.persist_power_factor_commands | Persist power-factor commands | write |
| cb-holding-p009-first_group-block-01:holding:20 | holding | 20 | control.active_power_ramp_rate_startup | Active power ramp rate (startup) | write |
| cb-holding-p009-first_group-block-01:holding:21 | holding | 21 | control.active_power_ramp_rate_restart | Active power ramp rate (restart) | write |
| cb-holding-p009-first_group-block-01:holding:22 | holding | 22 | control.modbus_rtu_baud_rate | Modbus RTU baud rate | write |
| cb-holding-p009-first_group-block-01:holding:23 | holding | 23 | field.inverter_serial_number | Inverter serial number | read |
| cb-holding-p009-first_group-block-01:holding:24 | holding | 24 | field.serial_number | Serial Number | read |
| cb-holding-p009-first_group-block-01:holding:25 | holding | 25 | field.serial_number | Serial Number | read |
| cb-holding-p009-first_group-block-01:holding:26 | holding | 26 | field.serial_number | Serial Number | read |
| cb-holding-p009-first_group-block-01:holding:27 | holding | 27 | field.serial_number | Serial Number | read |
| cb-holding-p009-first_group-block-01:holding:28 | holding | 28 | field.inverter_model | Inverter Model (high word) | read |
| cb-holding-p009-first_group-block-01:holding:29 | holding | 29 | field.inverter_model | Inverter Model (low word) | read |
| cb-holding-p009-first_group-block-01:holding:3 | holding | 3 | control.active_power_limit_setpoint | Active power limit setpoint | write |
| cb-holding-p009-first_group-block-01:holding:30 | holding | 30 | control.modbus_slave_address | Modbus slave address | write |
| cb-holding-p009-first_group-block-01:holding:31 | holding | 31 | control.firmware_update_trigger | Firmware update trigger | write |
| cb-holding-p009-first_group-block-01:holding:32 | holding | 32 | control.reset_user_configuration | Reset user configuration | write |
| cb-holding-p009-first_group-block-01:holding:33 | holding | 33 | control.factory_reset | Factory reset | write |
| cb-holding-p009-first_group-block-01:holding:34 | holding | 34 | field.manufacturer_information_string | Manufacturer information string | read |
| cb-holding-p009-first_group-block-01:holding:35 | holding | 35 | field.manufacturer_information_string | Manufacturer information string | read |
| cb-holding-p009-first_group-block-01:holding:36 | holding | 36 | field.manufacturer_information_string | Manufacturer information string | read |
| cb-holding-p009-first_group-block-01:holding:37 | holding | 37 | field.manufacturer_information_string | Manufacturer information string | read |
| cb-holding-p009-first_group-block-01:holding:38 | holding | 38 | field.manufacturer_information_string | Manufacturer information string | read |
| cb-holding-p009-first_group-block-01:holding:39 | holding | 39 | field.manufacturer_information_string | Manufacturer information string | read |
| cb-holding-p009-first_group-block-01:holding:4 | holding | 4 | control.reactive_power_limit_setpoint | Reactive power limit setpoint | write |
| cb-holding-p009-first_group-block-01:holding:40 | holding | 40 | field.manufacturer_information_string | Manufacturer information string | read |
| cb-holding-p009-first_group-block-01:holding:41 | holding | 41 | field.manufacturer_information_string | Manufacturer information string | read |
| cb-holding-p009-first_group-block-01:holding:42 | holding | 42 | control.g100_failsafe_enable | G100 failsafe enable | write |
| cb-holding-p009-first_group-block-01:holding:43 | holding | 43 | field.device_type_code | Device type code | read |
| cb-holding-p009-first_group-block-01:holding:44 | holding | 44 | field.trackers_and_phases | Trackers and phases | read |
| cb-holding-p009-first_group-block-01:holding:45 | holding | 45 | control.system_clock_year | System clock year | write |
| cb-holding-p009-first_group-block-01:holding:46 | holding | 46 | control.system_clock_month | System clock month | write |
| cb-holding-p009-first_group-block-01:holding:47 | holding | 47 | control.system_clock_day | System clock day | write |
| cb-holding-p009-first_group-block-01:holding:48 | holding | 48 | control.system_clock_hour | System clock hour | write |
| cb-holding-p009-first_group-block-01:holding:49 | holding | 49 | control.system_clock_minute | System clock minute | write |
| cb-holding-p009-first_group-block-01:holding:5 | holding | 5 | control.power_factor_target | Power factor target | write |
| cb-holding-p009-first_group-block-01:holding:50 | holding | 50 | control.system_clock_second | System clock second | write |
| cb-holding-p009-first_group-block-01:holding:51 | holding | 51 | control.system_clock_weekday | System clock weekday | write |
| cb-holding-p009-first_group-block-01:holding:52 | holding | 52 | control.stage_1_undervoltage_limit | Stage 1 undervoltage limit | write |
| cb-holding-p009-first_group-block-01:holding:53 | holding | 53 | control.stage_1_overvoltage_limit | Stage 1 overvoltage limit | write |
| cb-holding-p009-first_group-block-01:holding:54 | holding | 54 | control.stage_1_underfrequency_limit | Stage 1 underfrequency limit | write |
| cb-holding-p009-first_group-block-01:holding:55 | holding | 55 | control.stage_1_overfrequency_limit | Stage 1 overfrequency limit | write |
| cb-holding-p009-first_group-block-01:holding:56 | holding | 56 | control.stage_2_undervoltage_limit | Stage 2 undervoltage limit | write |
| cb-holding-p009-first_group-block-01:holding:57 | holding | 57 | control.stage_2_overvoltage_limit | Stage 2 overvoltage limit | write |
| cb-holding-p009-first_group-block-01:holding:58 | holding | 58 | control.stage_2_underfrequency_limit | Stage 2 underfrequency limit | write |
| cb-holding-p009-first_group-block-01:holding:59 | holding | 59 | control.stage_2_overfrequency_limit | Stage 2 overfrequency limit | write |
| cb-holding-p009-first_group-block-01:holding:6 | holding | 6 | control.rated_apparent_power | Rated apparent power (high word) | read |
| cb-holding-p009-first_group-block-01:holding:60 | holding | 60 | control.stage_3_undervoltage_limit | Stage 3 undervoltage limit | write |
| cb-holding-p009-first_group-block-01:holding:61 | holding | 61 | control.stage_3_overvoltage_limit | Stage 3 overvoltage limit | write |
| cb-holding-p009-first_group-block-01:holding:62 | holding | 62 | grid.frequency | Grid frequency | write |
| cb-holding-p009-first_group-block-01:holding:63 | holding | 63 | grid.frequency | Grid frequency | write |
| cb-holding-p009-first_group-block-01:holding:64 | holding | 64 | control.reconnect_undervoltage_limit | Reconnect undervoltage limit | write |
| cb-holding-p009-first_group-block-01:holding:65 | holding | 65 | control.reconnect_overvoltage_limit | Reconnect overvoltage limit | write |
| cb-holding-p009-first_group-block-01:holding:66 | holding | 66 | control.reconnect_underfrequency_limit | Reconnect underfrequency limit | write |
| cb-holding-p009-first_group-block-01:holding:67 | holding | 67 | control.reconnect_overfrequency_limit | Reconnect overfrequency limit | write |
| cb-holding-p009-first_group-block-01:holding:68 | holding | 68 | control.stage_1_undervoltage_trip_delay | Stage 1 undervoltage trip delay | write |
| cb-holding-p009-first_group-block-01:holding:69 | holding | 69 | control.stage_1_overvoltage_trip_delay | Stage 1 overvoltage trip delay | write |
| cb-holding-p009-first_group-block-01:holding:7 | holding | 7 | control.rated_apparent_power | Rated apparent power (low word) | read |
| cb-holding-p009-first_group-block-01:holding:70 | holding | 70 | control.stage_2_undervoltage_trip_delay | Stage 2 undervoltage trip delay | write |
| cb-holding-p009-first_group-block-01:holding:71 | holding | 71 | control.stage_2_overvoltage_trip_delay | Stage 2 overvoltage trip delay | write |
| cb-holding-p009-first_group-block-01:holding:72 | holding | 72 | grid.frequency | Grid frequency | write |
| cb-holding-p009-first_group-block-01:holding:73 | holding | 73 | grid.frequency | Grid frequency | write |
| cb-holding-p009-first_group-block-01:holding:74 | holding | 74 | grid.frequency | Grid frequency | write |
| cb-holding-p009-first_group-block-01:holding:75 | holding | 75 | grid.frequency | Grid frequency | write |
| cb-holding-p009-first_group-block-01:holding:76 | holding | 76 | control.stage_3_undervoltage_trip_delay | Stage 3 undervoltage trip delay | write |
| cb-holding-p009-first_group-block-01:holding:77 | holding | 77 | control.stage_3_overvoltage_trip_delay | Stage 3 overvoltage trip delay | write |
| cb-holding-p009-first_group-block-01:holding:78 | holding | 78 | grid.frequency | Grid frequency | write |
| cb-holding-p009-first_group-block-01:holding:79 | holding | 79 | grid.frequency | Grid frequency | write |
| cb-holding-p009-first_group-block-01:holding:8 | holding | 8 | telemetry.nominal_pv_voltage | Nominal PV voltage | read |
| cb-holding-p009-first_group-block-01:holding:80 | holding | 80 | control.ten_minute_overvoltage_limit | Ten-minute overvoltage limit | write |
| cb-holding-p009-first_group-block-01:holding:81 | holding | 81 | control.pv_input_high_voltage_fault | PV input high-voltage fault | write |
| cb-holding-p009-first_group-block-01:holding:82 | holding | 82 | field.controller_firmware_build_string | Controller firmware build string | read |
| cb-holding-p009-first_group-block-01:holding:83 | holding | 83 | field.controller_firmware_build_string | Controller firmware build string | read |
| cb-holding-p009-first_group-block-01:holding:84 | holding | 84 | field.controller_firmware_build_string | Controller firmware build string | read |
| cb-holding-p009-first_group-block-01:holding:85 | holding | 85 | field.controller_firmware_build_string | Controller firmware build string | read |
| cb-holding-p009-first_group-block-01:holding:86 | holding | 86 | field.controller_firmware_build_string | Controller firmware build string | read |
| cb-holding-p009-first_group-block-01:holding:87 | holding | 87 | field.controller_firmware_build_string | Controller firmware build string | read |
| cb-holding-p009-first_group-block-01:holding:88 | holding | 88 | field.modbus_version | Modbus version | read |
| cb-holding-p009-first_group-block-01:holding:89 | holding | 89 | control.power_factor_control_mode | Power-factor control mode | write |
| cb-holding-p009-first_group-block-01:holding:9 | holding | 9 | field.firmware | Firmware (high word) | read |
| cb-holding-p009-first_group-block-01:holding:90 | holding | 90 | control.gprs_modem_ip_status_flags | GPRS modem IP/status flags | write |
| cb-holding-p009-first_group-block-01:holding:91 | holding | 91 | control.frequency_derating_start | Frequency derating start | write |
| cb-holding-p009-first_group-block-01:holding:92 | holding | 92 | control.frequency_derating_slope | Frequency derating slope | write |
| cb-holding-p009-first_group-block-01:holding:93 | holding | 93 | control.cei_0_21_q_v_point_v1s | CEI 0-21 Q(V) point V1S | write |
| cb-holding-p009-first_group-block-01:holding:94 | holding | 94 | control.cei_0_21_q_v_point_v2s | CEI 0-21 Q(V) point V2S | write |
| cb-holding-p009-first_group-block-01:holding:95 | holding | 95 | control.cei_0_21_q_v_point_v1l | CEI 0-21 Q(V) point V1L | write |
| cb-holding-p009-first_group-block-01:holding:96 | holding | 96 | control.cei_0_21_q_v_point_v2l | CEI 0-21 Q(V) point V2L | write |
| cb-holding-p009-first_group-block-01:holding:97 | holding | 97 | control.q_v_lock_in_active_power | Q(V) lock-in active power | write |
| cb-holding-p009-first_group-block-01:holding:98 | holding | 98 | control.q_v_lock_out_active_power | Q(V) lock-out active power | write |
| cb-holding-p009-first_group-block-01:holding:99 | holding | 99 | control.power_factor_curve_lock_in_voltage | Power-factor curve lock-in voltage | write |
| cb-holding-p016-second_group-block-02:holding:125 | holding | 125 | field.inverter_type_identifier | Inverter type identifier | read |
| cb-holding-p016-second_group-block-02:holding:126 | holding | 126 | field.inverter_type_identifier | Inverter type identifier | read |
| cb-holding-p016-second_group-block-02:holding:127 | holding | 127 | field.inverter_type_identifier | Inverter type identifier | read |
| cb-holding-p016-second_group-block-02:holding:128 | holding | 128 | field.inverter_type_identifier | Inverter type identifier | read |
| cb-holding-p016-second_group-block-02:holding:129 | holding | 129 | field.inverter_type_identifier | Inverter type identifier | read |
| cb-holding-p016-second_group-block-02:holding:130 | holding | 130 | field.inverter_type_identifier | Inverter type identifier | read |
| cb-holding-p016-second_group-block-02:holding:131 | holding | 131 | field.inverter_type_identifier | Inverter type identifier | read |
| cb-holding-p016-second_group-block-02:holding:132 | holding | 132 | field.inverter_type_identifier | Inverter type identifier | read |
| cb-holding-p016-second_group-block-02:holding:133 | holding | 133 | field.bootloader_identifier_string | Bootloader identifier string | read |
| cb-holding-p016-second_group-block-02:holding:134 | holding | 134 | field.bootloader_identifier_string | Bootloader identifier string | read |
| cb-holding-p016-second_group-block-02:holding:135 | holding | 135 | field.bootloader_identifier_string | Bootloader identifier string | read |
| cb-holding-p016-second_group-block-02:holding:136 | holding | 136 | field.bootloader_identifier_string | Bootloader identifier string | read |
| cb-holding-p016-second_group-block-02:holding:137 | holding | 137 | control.reactive_power_direct_control_setpoint | Reactive power direct-control setpoint (high word) | read_write |
| cb-holding-p016-second_group-block-02:holding:138 | holding | 138 | control.reactive_power_direct_control_setpoint | Reactive power direct-control setpoint (low word) | read_write |
| cb-holding-p016-second_group-block-02:holding:139 | holding | 139 | control.reactive_priority_enable | Reactive priority enable | read_write |
| cb-holding-p016-second_group-block-02:holding:140 | holding | 140 | control.reactive_priority_ratio | Reactive priority ratio | read_write |
| cb-holding-p016-second_group-block-02:holding:141 | holding | 141 | control.night_reactive_support_svg | Night reactive support (SVG) | read_write |
| cb-holding-p016-second_group-block-02:holding:142 | holding | 142 | control.frequency_watt_boost_start | Frequency-watt boost start | read_write |
| cb-holding-p016-second_group-block-02:holding:143 | holding | 143 | control.over_frequency_recovery_point | Over-frequency recovery point | read_write |
| cb-holding-p016-second_group-block-02:holding:144 | holding | 144 | control.over_frequency_recovery_delay | Over-frequency recovery delay | read_write |
| cb-holding-p016-second_group-block-02:holding:145 | holding | 145 | control.zero_current_detection_enable | Zero-current detection enable | read_write |
| cb-holding-p016-second_group-block-02:holding:146 | holding | 146 | control.zero_current_low_voltage | Zero-current low voltage | read_write |
| cb-holding-p016-second_group-block-02:holding:147 | holding | 147 | control.zero_current_high_voltage | Zero-current high voltage | read_write |
| cb-holding-p016-second_group-block-02:holding:148 | holding | 148 | control.high_voltage_derate_start | High-voltage derate start | read_write |
| cb-holding-p016-second_group-block-02:holding:149 | holding | 149 | control.high_voltage_derate_end | High-voltage derate end | read_write |
| cb-holding-p016-second_group-block-02:holding:150 | holding | 150 | control.q_v_stabilisation_time | Q(V) stabilisation time | read_write |
| cb-holding-p016-second_group-block-02:holding:151 | holding | 151 | control.frequency_watt_boost_stop | Frequency-watt boost stop | read_write |
| cb-holding-p016-second_group-block-02:holding:152 | holding | 152 | control.cei_under_frequency_ramp_start | CEI under-frequency ramp start | read_write |
| cb-holding-p016-second_group-block-02:holding:153 | holding | 153 | control.cei_under_frequency_ramp_end | CEI under-frequency ramp end | read_write |
| cb-holding-p016-second_group-block-02:holding:154 | holding | 154 | control.cei_over_frequency_ramp_start | CEI over-frequency ramp start | read_write |
| cb-holding-p016-second_group-block-02:holding:155 | holding | 155 | control.cei_over_frequency_ramp_end | CEI over-frequency ramp end | read_write |
| cb-holding-p016-second_group-block-02:holding:156 | holding | 156 | control.cei_undervoltage_ramp_start | CEI undervoltage ramp start | read_write |
| cb-holding-p016-second_group-block-02:holding:157 | holding | 157 | control.cei_undervoltage_ramp_end | CEI undervoltage ramp end | read_write |
| cb-holding-p016-second_group-block-02:holding:158 | holding | 158 | control.cei_overvoltage_ramp_start | CEI overvoltage ramp start | read_write |
| cb-holding-p016-second_group-block-02:holding:159 | holding | 159 | control.cei_overvoltage_ramp_end | CEI overvoltage ramp end | read_write |
| cb-holding-p016-second_group-block-02:holding:160 | holding | 160 | control.nominal_grid_voltage_selection | Nominal grid voltage selection | read_write |
| cb-holding-p016-second_group-block-02:holding:161 | holding | 161 | control.grid_watt_restoration_delay | Grid watt restoration delay | read_write |
| cb-holding-p016-second_group-block-02:holding:162 | holding | 162 | control.reconnect_ramp_slope | Reconnect ramp slope | read_write |
| cb-holding-p016-second_group-block-02:holding:163 | holding | 163 | control.lfrt_stage_1_frequency | LFRT stage 1 frequency | read_write |
| cb-holding-p016-second_group-block-02:holding:164 | holding | 164 | control.lfrt_stage_1_duration | LFRT stage 1 duration | read_write |
| cb-holding-p016-second_group-block-02:holding:165 | holding | 165 | control.lfrt_stage_2_frequency | LFRT stage 2 frequency | read_write |
| cb-holding-p016-second_group-block-02:holding:166 | holding | 166 | control.lfrt_stage_2_duration | LFRT stage 2 duration | read_write |
| cb-holding-p016-second_group-block-02:holding:167 | holding | 167 | control.hfrt_stage_1_frequency | HFRT stage 1 frequency | read_write |
| cb-holding-p016-second_group-block-02:holding:168 | holding | 168 | control.hfrt_stage_1_duration | HFRT stage 1 duration | read_write |
| cb-holding-p016-second_group-block-02:holding:169 | holding | 169 | control.hfrt_stage_2_frequency | HFRT stage 2 frequency | read_write |
| cb-holding-p016-second_group-block-02:holding:170 | holding | 170 | control.hfrt_stage_2_duration | HFRT stage 2 duration | read_write |
| cb-holding-p016-second_group-block-02:holding:171 | holding | 171 | control.hvrt_stage_1_voltage | HVRT stage 1 voltage | read_write |
| cb-holding-p016-second_group-block-02:holding:172 | holding | 172 | control.hvrt_stage_1_duration | HVRT stage 1 duration | read_write |
| cb-holding-p016-second_group-block-02:holding:173 | holding | 173 | control.hvrt_stage_2_voltage | HVRT stage 2 voltage | read_write |
| cb-holding-p016-second_group-block-02:holding:174 | holding | 174 | control.hvrt_stage_2_duration | HVRT stage 2 duration | read_write |
| cb-holding-p016-second_group-block-02:holding:175 | holding | 175 | control.under_frequency_boost_delay | Under-frequency boost delay | read_write |
| cb-holding-p016-second_group-block-02:holding:176 | holding | 176 | control.under_frequency_boost_rate | Under-frequency boost rate | read_write |
| cb-holding-p016-second_group-block-02:holding:177 | holding | 177 | control.grid_restart_high_frequency_limit | Grid restart high-frequency limit | read_write |
| cb-holding-p016-second_group-block-02:holding:178 | holding | 178 | control.over_frequency_derate_response_time | Over-frequency derate response time | read_write |
| cb-holding-p016-second_group-block-02:holding:179 | holding | 179 | control.under_frequency_boost_response_time | Under-frequency boost response time | read_write |
| cb-holding-p016-second_group-block-02:holding:180 | holding | 180 | control.meter_link_status | Meter link status | read_write |
| cb-holding-p016-second_group-block-02:holding:181 | holding | 181 | control.optimizer_count | Optimizer count | read_write |
| cb-holding-p016-second_group-block-02:holding:182 | holding | 182 | control.optimizer_configuration_flag | Optimizer configuration flag | read_write |
| cb-holding-p016-second_group-block-02:holding:183 | holding | 183 | control.pv_string_scan_mode | PV string scan mode | read_write |
| cb-holding-p016-second_group-block-02:holding:184 | holding | 184 | control.bdc_parallel_count | BDC parallel count | read_write |
| cb-holding-p016-second_group-block-02:holding:185 | holding | 185 | battery.pack_count | Battery pack count | read |
| cb-holding-p016-second_group-block-02:holding:186 | holding | 186 |  | Reserved | read |
| cb-holding-p016-second_group-block-02:holding:187 | holding | 187 | control.vpp_function_enable_status | VPP function enable status | read |
| cb-holding-p016-second_group-block-02:holding:188 | holding | 188 | diagnostic.datalogger_server_status | Datalogger server status | read |
| cb-holding-p016-second_group-block-02:holding:200 | holding | 200 | field.pid_control_reserved | PID control reserved | read |
| cb-holding-p016-second_group-block-02:holding:201 | holding | 201 | control.pid_operating_mode | PID operating mode | write |
| cb-holding-p016-second_group-block-02:holding:202 | holding | 202 | control.pid_breaker_control | PID breaker control | write |
| cb-holding-p016-second_group-block-02:holding:203 | holding | 203 | control.pid_output_voltage_setpoint | PID output voltage setpoint | write |
| cb-holding-p016-second_group-block-02:holding:209 | holding | 209 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:210 | holding | 210 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:211 | holding | 211 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:212 | holding | 212 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:213 | holding | 213 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:214 | holding | 214 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:215 | holding | 215 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:216 | holding | 216 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:217 | holding | 217 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:218 | holding | 218 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:219 | holding | 219 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:220 | holding | 220 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:221 | holding | 221 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:222 | holding | 222 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:223 | holding | 223 | field.alternate_serial_number | Alternate serial number | read |
| cb-holding-p016-second_group-block-02:holding:229 | holding | 229 | control.energy_calibration_factor | Energy calibration factor | read_write |
| cb-holding-p016-second_group-block-02:holding:231 | holding | 231 | control.fan_self_test_trigger | Fan self-test trigger | write |
| cb-holding-p016-second_group-block-02:holding:232 | holding | 232 | control.neutral_line_monitoring_enable | Neutral line monitoring enable | write |
| cb-holding-p016-second_group-block-02:holding:233 | holding | 233 | diagnostic.hardware_warning_flags | Hardware warning flags | read |
| cb-holding-p016-second_group-block-02:holding:234 | holding | 234 | diagnostic.hardware_warning_flags_reserved_word | Hardware warning flags (reserved word) | read |
| cb-holding-p016-second_group-block-02:holding:235 | holding | 235 | control.neutral_to_ground_detection | Neutral-to-ground detection | write |
| cb-holding-p016-second_group-block-02:holding:236 | holding | 236 | control.non_standard_voltage_range | Non-standard voltage range | write |
| cb-holding-p016-second_group-block-02:holding:237 | holding | 237 | control.appointed_spec_override | Appointed spec override | write |
| cb-holding-p016-second_group-block-02:holding:238 | holding | 238 | control.fast_mppt_mode | Fast MPPT mode | write |
| cb-holding-p016-second_group-block-02:holding:239 | holding | 239 |  | Reserved | read |
| cb-holding-p016-second_group-block-02:holding:240 | holding | 240 | control.commissioning_step_index | Commissioning step index | read_write |
| cb-holding-p016-second_group-block-02:holding:241 | holding | 241 | control.installer_longitude_word | Installer longitude word | read_write |
| cb-holding-p016-second_group-block-02:holding:242 | holding | 242 | control.installer_latitude_word | Installer latitude word | read_write |
| cb-holding-p016-second_group-block-02:holding:row:016-0142 | holding | None |  |  |  |
| cb-holding-p016-second_group-block-02:holding:row:019-0191 | holding | None |  |  |  |
| cb-holding-p016-second_group-block-02:holding:row:019-0196 | holding | None |  |  |  |
| cb-holding-p016-second_group-block-02:holding:row:020-0212 | holding | None |  |  |  |
| cb-holding-p016-second_group-block-02:holding:row:020-0214 | holding | 230 | control.anti_islanding_override | Anti-islanding override | write |
| cb-holding-p016-second_group-block-02:holding:row:020-0215 | holding | 230 | control.anti_islanding_override | Anti-islanding override | write |
| cb-holding-p016-second_group-block-02:holding:row:021-0228 | holding | None |  |  |  |
| cb-holding-p016-second_group-block-02:holding:row:024-0272 | holding | None |  |  |  |
| cb-holding-p016-second_group-block-02:holding:row:026-0295 | holding | None |  |  |  |
| cb-holding-p016-second_group-block-02:holding:row:027-0306 | holding | None |  |  |  |
| cb-input-p047-first_group-block-07:input:0 | input | 0 | inverter.status | Inverter operating status | read |
| cb-input-p047-first_group-block-07:input:1 | input | 1 | pv.total_power | PV total power | read_write |
| cb-input-p047-first_group-block-07:input:10 | input | 10 | pv.total_power | PV total power | read_write |
| cb-input-p047-first_group-block-07:input:100 | input | 100 | field.ipf | IPF | read |
| cb-input-p047-first_group-block-07:input:101 | input | 101 | telemetry.output_power_percentage | Output power percentage | read |
| cb-input-p047-first_group-block-07:input:102 | input | 102 | field.opfullwatth | OPFullwattH (high word) | read |
| cb-input-p047-first_group-block-07:input:103 | input | 103 | field.opfullwattl | OPFullwattH (low word) | read |
| cb-input-p047-first_group-block-07:input:104 | input | 104 | diagnostic.derating_mode | Derating mode | read |
| cb-input-p047-first_group-block-07:input:105 | input | 105 | diagnostic.fault_code | Fault code | read |
| cb-input-p047-first_group-block-07:input:106 | input | 106 |  | Register 106 | read |
| cb-input-p047-first_group-block-07:input:107 | input | 107 | diagnostic.faultsubcode | FaultSubcode | read |
| cb-input-p047-first_group-block-07:input:108 | input | 108 | field.remotectrlen | RemoteCtrlEn | read |
| cb-input-p047-first_group-block-07:input:109 | input | 109 | field.remotectrlpow_er | RemoteCtrlPow er | read |
| cb-input-p047-first_group-block-07:input:11 | input | 11 | telemetry.pv3_dc_voltage | PV3 DC voltage | read |
| cb-input-p047-first_group-block-07:input:110 | input | 110 | inverter.warning_flags_high | Inverter warning bitfield high word | read |
| cb-input-p047-first_group-block-07:input:111 | input | 111 | inverter.warning_subcode | Inverter warning subcode | read |
| cb-input-p047-first_group-block-07:input:112 | input | 112 | diagnostic.warnmaincode | WarnMaincode | read |
| cb-input-p047-first_group-block-07:input:113 | input | 113 | telemetry.real_power_percent | real Power Percent | read |
| cb-input-p047-first_group-block-07:input:114 | input | 114 | field.inv_start_delay_time | inv start delay time | read |
| cb-input-p047-first_group-block-07:input:115 | input | 115 | diagnostic.inverter_all_fault_code | Inverter aggregate fault code | read |
| cb-input-p047-first_group-block-07:input:116 | input | 116 | telemetry.ac_charge_power_h | AC charge Power_H (high word) | read |
| cb-input-p047-first_group-block-07:input:117 | input | 117 | telemetry.ac_charge_power_l | AC charge Power_H (low word) | read |
| cb-input-p047-first_group-block-07:input:118 | input | 118 | field.priority | Priority | read |
| cb-input-p047-first_group-block-07:input:119 | input | 119 | battery.type | Battery type | read |
| cb-input-p047-first_group-block-07:input:12 | input | 12 | telemetry.pv3_dc_current | PV3 DC current | read |
| cb-input-p047-first_group-block-07:input:120 | input | 120 | field.autoproofreadc_md | AutoProofreadC MD | read |
| cb-input-p047-first_group-block-07:input:124 | input | 124 |  | reserved | read |
| cb-input-p047-first_group-block-07:input:13 | input | 13 | pv.total_power | PV total power | read_write |
| cb-input-p047-first_group-block-07:input:14 | input | 14 | pv.total_power | PV total power | read_write |
| cb-input-p047-first_group-block-07:input:15 | input | 15 | telemetry.pv4_dc_voltage | PV4 DC voltage | read |
| cb-input-p047-first_group-block-07:input:16 | input | 16 | telemetry.pv4_dc_current | PV4 DC current | read |
| cb-input-p047-first_group-block-07:input:17 | input | 17 | pv.total_power | PV total power | read_write |
| cb-input-p047-first_group-block-07:input:18 | input | 18 | pv.total_power | PV total power | read_write |
| cb-input-p047-first_group-block-07:input:19 | input | 19 | telemetry.pv5_dc_voltage | PV5 DC voltage | read |
| cb-input-p047-first_group-block-07:input:2 | input | 2 | pv.total_power | PV total power | read_write |
| cb-input-p047-first_group-block-07:input:20 | input | 20 | telemetry.pv5_dc_current | PV5 DC current | read |
| cb-input-p047-first_group-block-07:input:21 | input | 21 | pv.total_power | PV total power | read_write |
| cb-input-p047-first_group-block-07:input:22 | input | 22 | pv.total_power | PV total power | read_write |
| cb-input-p047-first_group-block-07:input:23 | input | 23 | telemetry.pv6_dc_voltage | PV6 DC voltage | read |
| cb-input-p047-first_group-block-07:input:24 | input | 24 | telemetry.pv6_dc_current | PV6 DC current | read |
| cb-input-p047-first_group-block-07:input:25 | input | 25 | pv.total_power | PV total power (high word) | read |
| cb-input-p047-first_group-block-07:input:26 | input | 26 | pv.total_power | PV total power (low word) | read |
| cb-input-p047-first_group-block-07:input:27 | input | 27 | telemetry.pv7_dc_voltage | PV7 DC voltage | read |
| cb-input-p047-first_group-block-07:input:28 | input | 28 | telemetry.pv7_dc_current | PV7 DC current | read |
| cb-input-p047-first_group-block-07:input:29 | input | 29 | pv.total_power | PV total power (high word) | read |
| cb-input-p047-first_group-block-07:input:3 | input | 3 | telemetry.pv1_dc_voltage | PV1 DC voltage | read |
| cb-input-p047-first_group-block-07:input:30 | input | 30 | pv.total_power | PV total power (low word) | read |
| cb-input-p047-first_group-block-07:input:31 | input | 31 | telemetry.pv8_dc_voltage | PV8 DC voltage | read |
| cb-input-p047-first_group-block-07:input:32 | input | 32 | telemetry.pv8_dc_current | PV8 DC current | read |
| cb-input-p047-first_group-block-07:input:33 | input | 33 | pv.total_power | PV total power (high word) | read |
| cb-input-p047-first_group-block-07:input:34 | input | 34 | pv.total_power | PV total power (low word) | read |
| cb-input-p047-first_group-block-07:input:35 | input | 35 | telemetry.ac_output_power | AC output power (high word) | read |
| cb-input-p047-first_group-block-07:input:36 | input | 36 | telemetry.ac_output_power | AC output power (low word) | read |
| cb-input-p047-first_group-block-07:input:37 | input | 37 | grid.frequency | Grid frequency | read |
| cb-input-p047-first_group-block-07:input:38 | input | 38 | telemetry.ac_phase_l1_voltage | AC phase L1 voltage | read |
| cb-input-p047-first_group-block-07:input:39 | input | 39 | telemetry.ac_phase_l1_current | AC phase L1 current | read |
| cb-input-p047-first_group-block-07:input:4 | input | 4 | telemetry.pv1_dc_current | PV1 DC current | read |
| cb-input-p047-first_group-block-07:input:40 | input | 40 | telemetry.ac_phase_l1_power | AC phase L1 power (high word) | read |
| cb-input-p047-first_group-block-07:input:41 | input | 41 | telemetry.ac_phase_l1_power | AC phase L1 power (low word) | read |
| cb-input-p047-first_group-block-07:input:42 | input | 42 | telemetry.ac_phase_l2_voltage | AC phase L2 voltage | read |
| cb-input-p047-first_group-block-07:input:43 | input | 43 | telemetry.ac_phase_l2_current | AC phase L2 current | read |
| cb-input-p047-first_group-block-07:input:44 | input | 44 | telemetry.ac_phase_l2_power | AC phase L2 power (high word) | read |
| cb-input-p047-first_group-block-07:input:45 | input | 45 | telemetry.ac_phase_l2_power | AC phase L2 power (low word) | read |
| cb-input-p047-first_group-block-07:input:46 | input | 46 | telemetry.ac_phase_l3_voltage | AC phase L3 voltage | read |
| cb-input-p047-first_group-block-07:input:47 | input | 47 | telemetry.ac_phase_l3_current | AC phase L3 current | read |
| cb-input-p047-first_group-block-07:input:48 | input | 48 | ac.phase.l3_power | AC phase L3 power (high word) | read |
| cb-input-p047-first_group-block-07:input:49 | input | 49 | ac.phase.l3_power | AC phase L3 power (low word) | read |
| cb-input-p047-first_group-block-07:input:5 | input | 5 | pv.total_power | PV total power | read_write |
| cb-input-p047-first_group-block-07:input:50 | input | 50 | field.vac_rs | Vac_RS | read |
| cb-input-p047-first_group-block-07:input:51 | input | 51 | field.vac_st | Vac_ST | read |
| cb-input-p047-first_group-block-07:input:52 | input | 52 | field.vac_tr | Vac_TR | read |
| cb-input-p047-first_group-block-07:input:53 | input | 53 | telemetry.output_energy_today | Output energy today (high word) | read |
| cb-input-p047-first_group-block-07:input:54 | input | 54 | telemetry.output_energy_today | Output energy today (low word) | read |
| cb-input-p047-first_group-block-07:input:55 | input | 55 | telemetry.output_energy_total | Output energy total (high word) | read |
| cb-input-p047-first_group-block-07:input:56 | input | 56 | telemetry.output_energy_total | Output energy total (low word) | read |
| cb-input-p047-first_group-block-07:input:57 | input | 57 | inverter.runtime | Inverter runtime (high word) | read |
| cb-input-p047-first_group-block-07:input:58 | input | 58 | field.run_time | Inverter runtime (low word) | read |
| cb-input-p047-first_group-block-07:input:59 | input | 59 | telemetry.pv1_energy_today | PV1 energy today (high word) | read |
| cb-input-p047-first_group-block-07:input:6 | input | 6 | pv.total_power | PV total power | read_write |
| cb-input-p047-first_group-block-07:input:60 | input | 60 | telemetry.pv1_energy_today | PV1 energy today (low word) | read |
| cb-input-p047-first_group-block-07:input:61 | input | 61 | telemetry.pv1_energy_total | PV1 energy total (high word) | read |
| cb-input-p047-first_group-block-07:input:62 | input | 62 | telemetry.pv1_energy_total | PV1 energy total (low word) | read |
| cb-input-p047-first_group-block-07:input:63 | input | 63 | telemetry.pv2_energy_today | PV2 energy today (high word) | read |
| cb-input-p047-first_group-block-07:input:64 | input | 64 | telemetry.pv2_energy_today | PV2 energy today (low word) | read |
| cb-input-p047-first_group-block-07:input:65 | input | 65 | telemetry.pv2_energy_total | PV2 energy total (high word) | read |
| cb-input-p047-first_group-block-07:input:66 | input | 66 | telemetry.pv2_energy_total | PV2 energy total (low word) | read |
| cb-input-p047-first_group-block-07:input:67 | input | 67 | telemetry.pv3_energy_today | PV3 energy today (high word) | read |
| cb-input-p047-first_group-block-07:input:68 | input | 68 | telemetry.pv3_energy_today | PV3 energy today (low word) | read |
| cb-input-p047-first_group-block-07:input:69 | input | 69 | telemetry.pv3_energy_total | PV3 energy total (high word) | read |
| cb-input-p047-first_group-block-07:input:7 | input | 7 | telemetry.pv2_dc_voltage | PV2 DC voltage | read |
| cb-input-p047-first_group-block-07:input:70 | input | 70 | telemetry.pv3_energy_total | PV3 energy total (low word) | read |
| cb-input-p047-first_group-block-07:input:71 | input | 71 | telemetry.pv4_energy_today | PV4 energy today (high word) | read |
| cb-input-p047-first_group-block-07:input:72 | input | 72 | telemetry.pv4_energy_today | PV4 energy today (low word) | read |
| cb-input-p047-first_group-block-07:input:73 | input | 73 | pv.mppt4.energy_total | PV4 energy total (high word) | read |
| cb-input-p047-first_group-block-07:input:74 | input | 74 | pv.mppt4.energy_total | PV4 energy total (low word) | read |
| cb-input-p047-first_group-block-07:input:75 | input | 75 | telemetry.pv5_energy_today | PV5 energy today (high word) | read |
| cb-input-p047-first_group-block-07:input:76 | input | 76 | telemetry.pv5_energy_today | PV5 energy today (low word) | read |
| cb-input-p047-first_group-block-07:input:77 | input | 77 | telemetry.pv5_energy_total | PV5 energy total (high word) | read |
| cb-input-p047-first_group-block-07:input:78 | input | 78 | telemetry.pv5_energy_total | PV5 energy total (low word) | read |
| cb-input-p047-first_group-block-07:input:79 | input | 79 | telemetry.pv6_energy_today | PV6 energy today (high word) | read |
| cb-input-p047-first_group-block-07:input:8 | input | 8 | telemetry.pv2_dc_current | PV2 DC current | read |
| cb-input-p047-first_group-block-07:input:80 | input | 80 | telemetry.pv6_energy_today | PV6 energy today (low word) | read |
| cb-input-p047-first_group-block-07:input:81 | input | 81 | telemetry.pv6_energy_total | PV6 energy total (high word) | read |
| cb-input-p047-first_group-block-07:input:82 | input | 82 | telemetry.pv6_energy_total | PV6 energy total (low word) | read |
| cb-input-p047-first_group-block-07:input:83 | input | 83 | telemetry.pv7_energy_today | PV7 energy today (high word) | read |
| cb-input-p047-first_group-block-07:input:84 | input | 84 | telemetry.pv7_energy_today | PV7 energy today (low word) | read |
| cb-input-p047-first_group-block-07:input:85 | input | 85 | telemetry.pv7_energy_total | PV7 energy total (high word) | read |
| cb-input-p047-first_group-block-07:input:86 | input | 86 | telemetry.pv7_energy_total | PV7 energy total (low word) | read |
| cb-input-p047-first_group-block-07:input:87 | input | 87 | telemetry.pv8_energy_today | PV8 energy today (high word) | read |
| cb-input-p047-first_group-block-07:input:88 | input | 88 | telemetry.pv8_energy_today | PV8 energy today (low word) | read |
| cb-input-p047-first_group-block-07:input:89 | input | 89 | telemetry.pv8_energy_total | PV8 energy total (high word) | read |
| cb-input-p047-first_group-block-07:input:9 | input | 9 | pv.total_power | PV total power | read_write |
| cb-input-p047-first_group-block-07:input:90 | input | 90 | telemetry.pv8_energy_total | PV8 energy total (low word) | read |
| cb-input-p047-first_group-block-07:input:91 | input | 91 | telemetry.pv_energy_total | PV energy total (high word) | read |
| cb-input-p047-first_group-block-07:input:92 | input | 92 | telemetry.pv_energy_total | PV energy total (low word) | read |
| cb-input-p047-first_group-block-07:input:93 | input | 93 | diagnostic.inverter_temperature | Inverter temperature | read |
| cb-input-p047-first_group-block-07:input:94 | input | 94 | diagnostic.ipm_temperature | IPM temperature | read |
| cb-input-p047-first_group-block-07:input:95 | input | 95 | diagnostic.boost_temperature | Boost temperature | read |
| cb-input-p047-first_group-block-07:input:96 | input | 96 | field.temp4 | Temp4 | read |
| cb-input-p047-first_group-block-07:input:97 | input | 97 | field.uwbatvolt_dsp | uwBatVolt_DSP | read |
| cb-input-p047-first_group-block-07:input:98 | input | 98 | telemetry.p_bus_voltage | P-bus voltage | read |
| cb-input-p047-first_group-block-07:input:99 | input | 99 | telemetry.n_bus_voltage | N-bus voltage | read |
| cb-input-p051-second_group-block-08:input:125 | input | 125 | telemetry.pidpv1_voltage | PIDPV1+Voltage | read |
| cb-input-p051-second_group-block-08:input:126 | input | 126 | telemetry.pidpv1_current | PIDPV1+Current | read |
| cb-input-p051-second_group-block-08:input:127 | input | 127 | telemetry.pidpv2_voltage | PIDPV2+Voltage | read |
| cb-input-p051-second_group-block-08:input:128 | input | 128 | telemetry.pidpv2_current | PIDPV2+Current | read |
| cb-input-p051-second_group-block-08:input:129 | input | 129 | telemetry.pidpv3_voltage | PIDPV3+Voltage | read |
| cb-input-p051-second_group-block-08:input:130 | input | 130 | telemetry.pidpv3_current | PIDPV3+Current | read |
| cb-input-p051-second_group-block-08:input:131 | input | 131 | telemetry.pidpv4_voltage | PIDPV4+Voltage | read |
| cb-input-p051-second_group-block-08:input:132 | input | 132 | telemetry.pidpv4_current | PIDPV4+Current | read |
| cb-input-p051-second_group-block-08:input:133 | input | 133 | telemetry.pidpv5_voltage | PIDPV5+Voltage | read |
| cb-input-p051-second_group-block-08:input:134 | input | 134 | telemetry.pidpv5_current | PIDPV5+Current | read |
| cb-input-p051-second_group-block-08:input:135 | input | 135 | telemetry.pidpv6_voltage | PIDPV6+Voltage | read |
| cb-input-p051-second_group-block-08:input:136 | input | 136 | telemetry.pidpv6_current | PIDPV6+Current | read |
| cb-input-p051-second_group-block-08:input:137 | input | 137 | telemetry.pidpv7_voltage | PIDPV7+Voltage | read |
| cb-input-p051-second_group-block-08:input:138 | input | 138 | telemetry.pidpv7_current | PIDPV7+Current | read |
| cb-input-p051-second_group-block-08:input:139 | input | 139 | telemetry.pidpv8_voltage | PIDPV8+Voltage | read |
| cb-input-p051-second_group-block-08:input:140 | input | 140 | telemetry.pidpv8_current | PIDPV8+Current | read |
| cb-input-p051-second_group-block-08:input:141 | input | 141 | control.pidstatus | PIDStatus | write |
| cb-input-p051-second_group-block-08:input:142 | input | 142 | field.v_string1 | V_String1 | read |
| cb-input-p051-second_group-block-08:input:143 | input | 143 | field.curr_string1 | Curr_String1 | read |
| cb-input-p051-second_group-block-08:input:144 | input | 144 | field.v_string2 | V_String2 | read |
| cb-input-p051-second_group-block-08:input:145 | input | 145 | field.curr_string2 | Curr_String2 | read |
| cb-input-p051-second_group-block-08:input:146 | input | 146 | field.v_string3 | V_String3 | read |
| cb-input-p051-second_group-block-08:input:147 | input | 147 | field.curr_string3 | Curr_String3 | read |
| cb-input-p051-second_group-block-08:input:148 | input | 148 | field.v_string4 | V_String4 | read |
| cb-input-p051-second_group-block-08:input:149 | input | 149 | field.curr_string4 | Curr_String4 | read |
| cb-input-p051-second_group-block-08:input:150 | input | 150 | field.v_string5 | V_String5 | read |
| cb-input-p051-second_group-block-08:input:151 | input | 151 | field.curr_string5 | Curr_String5 | read |
| cb-input-p051-second_group-block-08:input:152 | input | 152 | field.v_string6 | V_String6 | read |
| cb-input-p051-second_group-block-08:input:153 | input | 153 | field.curr_string6 | Curr_String6 | read |
| cb-input-p051-second_group-block-08:input:154 | input | 154 | field.v_string7 | V_String7 | read |
| cb-input-p051-second_group-block-08:input:155 | input | 155 | field.curr_string7 | Curr_String7 | read |
| cb-input-p051-second_group-block-08:input:156 | input | 156 | field.v_string8 | V_String8 | read |
| cb-input-p051-second_group-block-08:input:157 | input | 157 | field.curr_string8 | Curr_String8 | read |
| cb-input-p051-second_group-block-08:input:158 | input | 158 | field.v_string9 | V_String9 | read |
| cb-input-p051-second_group-block-08:input:159 | input | 159 | field.curr_string9 | Curr_String9 | read |
| cb-input-p051-second_group-block-08:input:160 | input | 160 | field.v_string10 | V_String10 | read |
| cb-input-p051-second_group-block-08:input:161 | input | 161 | field.curr_string10 | Curr_String10 | read |
| cb-input-p051-second_group-block-08:input:162 | input | 162 | field.v_string11 | V_String11 | read |
| cb-input-p051-second_group-block-08:input:163 | input | 163 | field.curr_string11 | Curr_String11 | read |
| cb-input-p051-second_group-block-08:input:164 | input | 164 | field.v_string12 | V_String12 | read |
| cb-input-p051-second_group-block-08:input:165 | input | 165 | field.curr_string12 | Curr_String12 | read |
| cb-input-p051-second_group-block-08:input:166 | input | 166 | field.v_string13 | V_String13 | read |
| cb-input-p051-second_group-block-08:input:167 | input | 167 | field.curr_string13 | Curr_String13 | read |
| cb-input-p051-second_group-block-08:input:168 | input | 168 | field.v_string14 | V_String14 | read |
| cb-input-p051-second_group-block-08:input:169 | input | 169 | field.curr_string14 | Curr_String14 | read |
| cb-input-p051-second_group-block-08:input:170 | input | 170 | field.v_string15 | V_String15 | read |
| cb-input-p051-second_group-block-08:input:171 | input | 171 | field.curr_string15 | Curr_String15 | read |
| cb-input-p051-second_group-block-08:input:172 | input | 172 | field.v_string16 | V_String16 | read |
| cb-input-p051-second_group-block-08:input:173 | input | 173 | field.curr_string16 | Curr_String16 | read |
| cb-input-p051-second_group-block-08:input:174 | input | 174 | field.strunmatch | StrUnmatch | read |
| cb-input-p051-second_group-block-08:input:175 | input | 175 | telemetry.strcurrentunblan_ce | StrCurrentUnblan ce | read |
| cb-input-p051-second_group-block-08:input:176 | input | 176 | field.strdisconnect | StrDisconnect | read |
| cb-input-p051-second_group-block-08:input:177 | input | 177 | diagnostic.pidfaultcode | PIDFaultCode | read |
| cb-input-p051-second_group-block-08:input:178 | input | 178 | field.stringprompt | StringPrompt | read |
| cb-input-p051-second_group-block-08:input:179 | input | 179 | diagnostic.pvwarningvalue | PVWarningValue | read |
| cb-input-p051-second_group-block-08:input:180 | input | 180 | diagnostic.dsp075_warning_value | DSP075 Warning Value | read |
| cb-input-p051-second_group-block-08:input:181 | input | 181 | diagnostic.dsp075_fault_value | DSP075 Fault Value | read |
| cb-input-p051-second_group-block-08:input:182 | input | 182 | field.dsp067_debug_data1 | DSP067 Debug Data1 | read |
| cb-input-p051-second_group-block-08:input:183 | input | 183 | field.dsp067_debug_data2 | DSP067 Debug Data2 | read |
| cb-input-p051-second_group-block-08:input:184 | input | 184 | field.dsp067_debug_data3 | DSP067 Debug Data3 | read |
| cb-input-p051-second_group-block-08:input:185 | input | 185 | field.dsp067_debug_data4 | DSP067 Debug Data4 | read |
| cb-input-p051-second_group-block-08:input:186 | input | 186 | field.dsp067_debug_data5 | DSP067 Debug Data5 | read |
| cb-input-p051-second_group-block-08:input:187 | input | 187 | field.dsp067_debug_data6 | DSP067 Debug Data6 | read |
| cb-input-p051-second_group-block-08:input:188 | input | 188 | field.dsp067_debug_data7 | DSP067 Debug Data7 | read |
| cb-input-p051-second_group-block-08:input:189 | input | 189 | field.dsp067_debug_data8 | DSP067 Debug Data8 | read |
| cb-input-p051-second_group-block-08:input:190 | input | 190 | field.dsp075_debug_data1 | DSP075 Debug Data1 | read |
| cb-input-p051-second_group-block-08:input:191 | input | 191 | field.dsp075_debug_data2 | DSP075 Debug Data2 | read |
| cb-input-p051-second_group-block-08:input:192 | input | 192 | field.dsp075_debug_data3 | DSP075 Debug Data3 | read |
| cb-input-p051-second_group-block-08:input:193 | input | 193 | field.dsp075_debug_data4 | DSP075 Debug Data4 | read |
| cb-input-p051-second_group-block-08:input:194 | input | 194 | field.dsp075_debug_data55 | DSP075 Debug Data55 | read |
| cb-input-p051-second_group-block-08:input:195 | input | 195 | field.dsp075_debug_data6 | DSP075 Debug Data6 | read |
| cb-input-p051-second_group-block-08:input:196 | input | 196 | field.dsp075_debug_data7 | DSP075 Debug Data7 | read |
| cb-input-p051-second_group-block-08:input:197 | input | 197 | field.dsp075_debug_data8 | DSP075 Debug Data8 | read |
| cb-input-p051-second_group-block-08:input:198 | input | 198 | field.busbagingtestok_flag | bUSBAgingTestOk Flag | read |
| cb-input-p051-second_group-block-08:input:199 | input | 199 | field.bflasheraseaging_okflag | bFlashEraseAging OkFlag | read |
| cb-input-p051-second_group-block-08:input:200 | input | 200 | field.pviso | PVISO | read |
| cb-input-p051-second_group-block-08:input:201 | input | 201 | field.r_dci | R_DCI | read |
| cb-input-p051-second_group-block-08:input:202 | input | 202 | field.s_dci | S_DCI | read |
| cb-input-p051-second_group-block-08:input:203 | input | 203 | field.t_dci | T_DCI | read |
| cb-input-p051-second_group-block-08:input:204 | input | 204 | field.pid_bus | PID_Bus | read |
| cb-input-p051-second_group-block-08:input:205 | input | 205 | field.gfci | GFCI | read |
| cb-input-p051-second_group-block-08:input:206 | input | 206 | control.svg_apf_status_svgapfeq_ualratio | SVG/APF Status+SVGAPFEq ualRatio | write |
| cb-input-p051-second_group-block-08:input:207 | input | 207 | field.ct_i_r | CT_I_R | read |
| cb-input-p051-second_group-block-08:input:208 | input | 208 | field.ct_i_s | CT_I_S | read |
| cb-input-p051-second_group-block-08:input:209 | input | 209 | field.ct_i_t | CT_I_T | read |
| cb-input-p051-second_group-block-08:input:210 | input | 210 | field.ct_q_rh | CT_Q_RH (high word) | read |
| cb-input-p051-second_group-block-08:input:211 | input | 211 | field.ct_q_rl | CT_Q_RH (low word) | read |
| cb-input-p051-second_group-block-08:input:212 | input | 212 | field.ct_q_sh | CT_Q_SH (high word) | read |
| cb-input-p051-second_group-block-08:input:213 | input | 213 | field.ct_q_sl | CT_Q_SH (low word) | read |
| cb-input-p051-second_group-block-08:input:214 | input | 214 | field.ct_q_th | CT_Q_TH (high word) | read |
| cb-input-p051-second_group-block-08:input:215 | input | 215 | field.ct_q_tl | CT_Q_TH (low word) | read |
| cb-input-p051-second_group-block-08:input:216 | input | 216 | field.cthar_i_r | CTHAR_I_R | read |
| cb-input-p051-second_group-block-08:input:217 | input | 217 | field.cthar_i_s | CTHAR_I_S | read |
| cb-input-p051-second_group-block-08:input:218 | input | 218 | field.cthar_i_t | CTHAR_I_T | read |
| cb-input-p051-second_group-block-08:input:219 | input | 219 | field.comp_q_rh | COMP_Q_RH (high word) | read |
| cb-input-p051-second_group-block-08:input:220 | input | 220 | field.comp_q_rl | COMP_Q_RH (low word) | read |
| cb-input-p051-second_group-block-08:input:221 | input | 221 | field.comp_q_sh | COMP_Q_SH (high word) | read |
| cb-input-p051-second_group-block-08:input:222 | input | 222 | field.comp_q_sl | COMP_Q_SH (low word) | read |
| cb-input-p051-second_group-block-08:input:223 | input | 223 | field.comp_q_th | COMP_Q_TH (high word) | read |
| cb-input-p051-second_group-block-08:input:224 | input | 224 | field.comp_q_tl | COMP_Q_TH (low word) | read |
| cb-input-p051-second_group-block-08:input:225 | input | 225 | field.comphar_i_r | COMPHAR_I_R | read |
| cb-input-p051-second_group-block-08:input:226 | input | 226 | field.comphar_i_s | COMPHAR_I_S | read |
| cb-input-p051-second_group-block-08:input:227 | input | 227 | field.comphar_i_t | COMPHAR_I_T | read |
| cb-input-p051-second_group-block-08:input:228 | input | 228 | field.brs232agingtest_okflag | bRS232AgingTest OkFlag | read |
| cb-input-p051-second_group-block-08:input:229 | input | 229 | diagnostic.bfanfaultbit | bFanFaultBit | read |
| cb-input-p051-second_group-block-08:input:230 | input | 230 | field.sach | SacH (high word) | read |
| cb-input-p051-second_group-block-08:input:231 | input | 231 | field.sacl | SacH (low word) | read |
| cb-input-p051-second_group-block-08:input:232 | input | 232 | telemetry.reactpowerh | ReActPowerH (high word) | read |
| cb-input-p051-second_group-block-08:input:233 | input | 233 | telemetry.reactpowerl | ReActPowerH (low word) | read |
| cb-input-p051-second_group-block-08:input:234 | input | 234 | telemetry.output_reactive_power | Output reactive power (high word) | read |
| cb-input-p051-second_group-block-08:input:235 | input | 235 | telemetry.output_reactive_power | Output reactive power (low word) | read |
| cb-input-p051-second_group-block-08:input:236 | input | 236 | telemetry.reactive_energy_total | Reactive energy total (high word) | read |
| cb-input-p051-second_group-block-08:input:237 | input | 237 | telemetry.reactive_energy_total | Reactive energy total (low word) | read |
| cb-input-p051-second_group-block-08:input:238 | input | 238 | diagnostic.bafcistatus | bAfciStatus | read |
| cb-input-p051-second_group-block-08:input:239 | input | 239 | field.uwpresentfftvalu_e_channel_a | uwPresentFFTValu e[CHANNEL_A] | read |
| cb-input-p051-second_group-block-08:input:240 | input | 240 | field.uwpresentfftvalu_e_channel_b | uwPresentFFTValu e[CHANNEL_B] | read |
| cb-input-p051-second_group-block-08:input:241 | input | 241 | field.dsp067_debug_data1 | DSP067 Debug Data1 | read |
| cb-input-p051-second_group-block-08:input:242 | input | 242 | field.dsp067_debug_data2 | DSP067 Debug Data2 | read |
| cb-input-p051-second_group-block-08:input:243 | input | 243 | field.dsp067_debug | DSP067 Debug | read |
| cb-input-p051-second_group-block-08:input:244 | input | 244 | field.dsp067_debug_data4 | DSP067 Debug Data4 | read |
| cb-input-p051-second_group-block-08:input:245 | input | 245 | field.dsp067_debug_data5 | DSP067 Debug Data5 | read |
| cb-input-p051-second_group-block-08:input:246 | input | 246 | field.dsp067_debug_data6 | DSP067 Debug Data6 | read |
| cb-input-p051-second_group-block-08:input:247 | input | 247 | field.dsp067_debug_data7 | DSP067 Debug Data7 | read |
| cb-input-p051-second_group-block-08:input:248 | input | 248 | field.dsp067_debug_data8 | DSP067 Debug Data8 | read |
| cb-input-p051-second_group-block-08:input:249 | input | 249 |  | Register 249 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:875 | input | 875 | field.vpv9 | Vpv9 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:876 | input | 876 | field.pv9curr | PV9Curr | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:877 | input | 877 | field.ppv9h | Ppv9H (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:878 | input | 878 | field.ppv9l | Ppv9H (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:879 | input | 879 | field.vpv10 | Vpv10 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:880 | input | 880 | field.pv10curr | PV10Curr | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:881 | input | 881 | field.ppv10h | Ppv10H (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:882 | input | 882 | field.ppv10l | Ppv10H (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:883 | input | 883 | field.vpv11 | Vpv11 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:884 | input | 884 | field.pv11curr | PV11Curr | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:885 | input | 885 | field.ppv11h | Ppv11H (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:886 | input | 886 | field.ppv11l | Ppv11H (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:887 | input | 887 | field.vpv12 | Vpv12 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:888 | input | 888 | field.pv12curr | PV12Curr | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:889 | input | 889 | field.ppv12h | Ppv12H (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:890 | input | 890 | field.ppv12l | Ppv12H (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:891 | input | 891 | field.vpv13 | Vpv13 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:892 | input | 892 | field.pv13curr | PV13Curr | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:893 | input | 893 | field.ppv13h | Ppv13H (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:894 | input | 894 | field.ppv13l | Ppv13H (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:895 | input | 895 | field.vpv14 | Vpv14 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:896 | input | 896 | field.pv14curr | PV14Curr | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:897 | input | 897 | field.ppv14h | Ppv14H (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:898 | input | 898 | field.ppv14l | Ppv14H (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:899 | input | 899 | field.vpv15 | Vpv15 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:900 | input | 900 | field.pv15curr | PV15Curr | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:901 | input | 901 | field.ppv15h | Ppv15H (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:902 | input | 902 | field.ppv15l | Ppv15H (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:903 | input | 903 | field.vpv16 | Vpv16 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:904 | input | 904 | field.pv16curr | PV16Curr | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:905 | input | 905 | field.ppv16h | Ppv16H (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:906 | input | 906 | field.ppv16l | Ppv16H (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:907 | input | 907 | field.epv9_todayh | Epv9_todayH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:908 | input | 908 | field.epv9_todayl | Epv9_todayH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:909 | input | 909 | field.epv9_totalh | Epv9_totalH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:910 | input | 910 | field.epv9_totall | Epv9_totalH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:911 | input | 911 | field.epv10_todayh | Epv10_todayH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:912 | input | 912 | field.epv10_todayl | Epv10_todayH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:913 | input | 913 | field.epv10_totalh | Epv10_totalH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:914 | input | 914 | field.epv10_totall | Epv10_totalH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:915 | input | 915 | field.epv11_todayh | Epv11_todayH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:916 | input | 916 | field.epv11_todayl | Epv11_todayH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:917 | input | 917 | field.epv11_totalh | Epv11_totalH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:918 | input | 918 | field.epv11_totall | Epv11_totalH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:919 | input | 919 | field.epv12_todayh | Epv12_todayH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:920 | input | 920 | field.epv12_todayl | Epv12_todayH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:921 | input | 921 | field.epv12_totalh | Epv12_totalH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:922 | input | 922 | field.epv12_totall | Epv12_totalH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:923 | input | 923 | field.epv13_todayh | Epv13_todayH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:924 | input | 924 | field.epv13_todayl | Epv13_todayH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:925 | input | 925 | field.epv13_totalh | Epv13_totalH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:926 | input | 926 | field.epv13_totall | Epv13_totalH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:927 | input | 927 | field.epv14_todayh | Epv14_todayH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:928 | input | 928 | field.epv14_todayl | Epv14_todayH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:929 | input | 929 | field.epv14_totalh | Epv14_totalH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:930 | input | 930 | field.epv14_totall | Epv14_totalH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:931 | input | 931 | field.epv15_todayh | Epv15_todayH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:932 | input | 932 | field.epv15_todayl | Epv15_todayH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:933 | input | 933 | field.epv15_totalh | Epv15_totalH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:934 | input | 934 | field.epv15_totall | Epv15_totalH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:935 | input | 935 | field.epv16_todayh | Epv16_todayH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:936 | input | 936 | field.epv16_todayl | Epv16_todayH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:937 | input | 937 | field.epv16_totalh | Epv16_totalH (high word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:938 | input | 938 | field.epv16_totall | Epv16_totalH (low word) | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:939 | input | 939 | telemetry.pidpv9_voltage | PIDPV9+Voltage | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:940 | input | 940 | telemetry.pidpv9_current | PIDPV9+Current | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:941 | input | 941 | telemetry.pid_pv10_voltage | PID PV10+ Voltage | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:942 | input | 942 | telemetry.pid_pv10_current | PID PV10+ Current | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:943 | input | 943 | telemetry.pid_pv11_voltage | PID PV11+ Voltage | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:944 | input | 944 | telemetry.pid_pv11_current | PID PV11+ Current | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:945 | input | 945 | telemetry.pid_pv12_voltage | PID PV12+ Voltage | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:946 | input | 946 | telemetry.pid_pv12_current | PID PV12+ Current | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:947 | input | 947 | telemetry.pid_pv13_voltage | PID PV13+ Voltage | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:948 | input | 948 | telemetry.pid_pv13_current | PID PV13+ Current | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:949 | input | 949 | telemetry.pid_pv14_voltage | PID PV14+ Voltage | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:950 | input | 950 | telemetry.pid_pv14_current | PID PV14+ Current | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:951 | input | 951 | telemetry.pid_pv15_voltage | PID PV15+ Voltage | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:952 | input | 952 | telemetry.pid_pv15_current | PID PV15+ Current | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:953 | input | 953 | telemetry.pid_pv16_voltage | PID PV16+ Voltage | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:954 | input | 954 | telemetry.pid_pv16_current | PID PV16+ Current | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:955 | input | 955 | field.v_string17 | V_String17 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:956 | input | 956 | field.curr_string17 | Curr_String17 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:957 | input | 957 | field.v_string18 | V_String18 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:958 | input | 958 | field.curr_string18 | Curr_String18 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:959 | input | 959 | field.v_string19 | V_String19 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:960 | input | 960 | field.curr_string19 | Curr_String19 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:961 | input | 961 | field.v_string20 | V_String20 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:962 | input | 962 | field.curr_string20 | Curr_String20 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:963 | input | 963 | field.v_string21 | V_String21 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:964 | input | 964 | field.curr_string21 | Curr_String21 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:965 | input | 965 | field.v_string22 | V_String22 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:966 | input | 966 | field.curr_string22 | Curr_String22 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:967 | input | 967 | field.v_string23 | V_String23 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:968 | input | 968 | field.curr_string23 | Curr_String23 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:969 | input | 969 | field.v_string24 | V_String24 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:970 | input | 970 | field.curr_string24 | Curr_String24 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:971 | input | 971 | field.v_string25 | V_String25 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:972 | input | 972 | field.curr_string25 | Curr_String25 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:973 | input | 973 | field.v_string26 | V_String26 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:974 | input | 974 | field.curr_string26 | Curr_String26 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:975 | input | 975 | field.v_string27 | V_String27 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:976 | input | 976 | field.curr_string27 | Curr_String27 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:977 | input | 977 | field.v_string28 | V_String28 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:978 | input | 978 | field.curr_string28 | Curr_String28 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:979 | input | 979 | field.v_string29 | V_String29 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:980 | input | 980 | field.curr_string29 | Curr_String29 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:981 | input | 981 | field.v_string30 | V_String30 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:982 | input | 982 | field.curr_string30 | Curr_String30 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:983 | input | 983 | field.v_string31 | V_String31 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:984 | input | 984 | field.curr_string31 | Curr_String31 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:985 | input | 985 | field.v_string32 | V_String32 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:986 | input | 986 | field.curr_string32 | Curr_String32 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:987 | input | 987 | field.strunmatch2 | StrUnmatch2 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:988 | input | 988 | telemetry.strcurrentunblan_ce2 | StrCurrentUnblan ce2 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:989 | input | 989 | field.strdisconnect2 | StrDisconnect2 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:990 | input | 990 | diagnostic.pvwarningvalue | PVWarningValue | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:991 | input | 991 | field.strwaringvalue1 | StrWaringvalue1 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:992 | input | 992 | field.strwaringvalue2 | StrWaringvalue2 | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:999 | input | 999 | field.systemcmd | SystemCmd | read |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09:input:row:059-0966 | input | None |  |  |  |
