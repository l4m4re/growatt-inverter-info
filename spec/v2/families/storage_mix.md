# Storage (MIX Type)

`v124-instruction-storage-mix`: Storage (MIX Type): 03 register range: 0~124, 1000~1124; 04 register range: 0~124, 1000~1124

| Applicability path | Resolved block |
| --- | --- |
| v124-holding-p009-first_group-block-01:v124-instruction-storage-mix:holding:0:124:3 | declared/no semantic block |
| v124-holding-p027-six_group_for_storage_power-block-03:v124-instruction-storage-mix:holding:1000:1124:3 | declared/no semantic block |
| v124-input-p047-first_group-block-07:v124-instruction-storage-mix:input:0:124:4 | declared/no semantic block |
| v124-input-p059-ninth_group_for_storage_power-block-10:v124-instruction-storage-mix:input:1000:1124:4 | declared/no semantic block |
| v124-input-p062-bms_infomation-block-11:v124-instruction-storage-mix:input:1000:1124:4 | declared/no semantic block |
| v124-input-p062-ups_information_offline-block-12:v124-instruction-storage-mix:input:1000:1124:4 | declared/no semantic block |

Block projections: `cb-holding-p009-first_group-block-01`, `cb-holding-p027-six_group_for_storage_power-block-03`, `cb-input-p047-first_group-block-07`, `cb-input-p059-ninth_group_for_storage_power-block-10`, `cb-input-p062-bms_infomation-block-11`, `cb-input-p062-ups_information_offline-block-12`. Register rows below are references to shared block definitions; applicability does not duplicate them.

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
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1000 | holding | 1000 | control.float_charge_current_limit_i | Float charge current limit i | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1001 | holding | 1001 | control.pf_cmd_memory_state | PF CMD memory state | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1002 | holding | 1002 | battery.discharge_start_voltage | Battery discharge start voltage | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1003 | holding | 1003 | field.vbatlowwa_rnclr_l | VbatlowWa rnClr l | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1004 | holding | 1004 | control.vbatstopfo_rdischarge | Vbatstopfo rdischarge | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1005 | holding | 1005 | control.vbat_stop_forcharge | Vbat stop forcharge | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1006 | holding | 1006 | control.vbat_start_for_discharge | Vbat start for discharge | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1007 | holding | 1007 | control.vbat_constant_charge | Vbat constant charge | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1008 | holding | 1008 | control.eesysinfo_s_ysseten | EESysInfo.S ysSetEn | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1009 | holding | 1009 | control.battemp_lower_limit_d | Battemp lower limit d | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1010 | holding | 1010 | control.bat_temp_upper_limit_d | Bat temp upper limit d | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1011 | holding | 1011 | control.bat_temp_lower_limit_c | Bat temp lower limit c | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1012 | holding | 1012 | control.bat_temp_upper_limit_c | Bat temp upper limit c | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1013 | holding | 1013 | field.uwunderfr_edischarge_delytime | uwUnderFr eDischarge DelyTime | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1014 | holding | 1014 | control.batmdlseri_alnum | BatMdlSeri alNum | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1015 | holding | 1015 | control.batmdlpara_llnum | BatMdlPara llNum | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1016 | holding | 1016 | field.drms_en | DRMS_EN | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1017 | holding | 1017 | field.bat_first_start_time_4 | Bat First Start Time 4 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1018 | holding | 1018 | field.bat_first_stop_time_4 | Bat First Stop Time 4 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1019 | holding | 1019 | field.batfirst_on_off_switch4 | BatFirst on/off Switch4 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1020 | holding | 1020 | field.bat_first_start_time_5 | Bat First Start Time 5 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1021 | holding | 1021 | field.batfirst_stoptime_5 | BatFirst StopTime 5 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1022 | holding | 1022 | field.batfirst_on_off_switch5 | BatFirst on/off Switch5 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1023 | holding | 1023 | field.batfirst_starttime_6 | BatFirst StartTime 6 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1024 | holding | 1024 | field.batfirst_stoptime_6 | BatFirst StopTime 6 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1025 | holding | 1025 | field.batfirst_on_off_switch6 | BatFirst on/off Switch6 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1026 | holding | 1026 | field.gridfirst_starttime | GridFirst StartTime | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1027 | holding | 1027 | field.gridfirst_stoptime_4 | GridFirst StopTime 4 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1028 | holding | 1028 | field.grid_first_stop_switch4 | Grid First Stop Switch4 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1029 | holding | 1029 | field.gridfirst_starttime_5 | GridFirst StartTime 5 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1030 | holding | 1030 | field.gridfirst_stoptime_5 | GridFirst StopTime 5 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1031 | holding | 1031 | field.grid_first_stop_switch5 | Grid First Stop Switch5 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1032 | holding | 1032 | field.gridfirst_starttime_6 | GridFirst StartTime 6 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1033 | holding | 1033 | field.gridfirst_stoptime_6 | GridFirst StopTime 6 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1034 | holding | 1034 | field.grid_first_stop_switch6 | Grid First Stop Switch6 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1035 | holding | 1035 | field.batfirst_starttime_4 | BatFirst StartTime 4 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1036 | holding | 1036 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1037 | holding | 1037 | control.bctmode | bCTMode | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1038 | holding | 1038 | control.ctadjust | CTAdjust | write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1039 | holding | 1039 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1040 | holding | 1040 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1041 | holding | 1041 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1042 | holding | 1042 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1043 | holding | 1043 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1044 | holding | 1044 | field.priority | Priority | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1045 | holding | 1045 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1046 | holding | 1046 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1047 | holding | 1047 | field.agingtestst_ep_cmd | AgingTestSt ep Cmd | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1048 | holding | 1048 | battery.type | Battery type | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1049 | holding | 1049 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1050 | holding | 1050 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1051 | holding | 1051 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1052 | holding | 1052 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1053 | holding | 1053 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1054 | holding | 1054 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1060 | holding | 1060 | field.buckupsfune_n | BuckUpsFunE n | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1061 | holding | 1061 | field.buckupsvolts_et | BuckUPSVoltS et | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1062 | holding | 1062 | field.upsfreqset | UPSFreqSet | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1070 | holding | 1070 | grid.first.discharge.rate | Grid-first discharge power rate | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1071 | holding | 1071 | grid.first.stop.soc | Grid-first stop SOC | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1079 | holding | 1079 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1080 | holding | 1080 | control.grid_first_slot_1_start | Grid-first slot 1 start | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1081 | holding | 1081 | control.grid_first_slot_1_stop | Grid-first slot 1 stop | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1082 | holding | 1082 | control.grid_first_slot_1_enable | Grid-first slot 1 enable | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1083 | holding | 1083 | control.grid_first_slot_2_start | Grid-first slot 2 start | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1084 | holding | 1084 | control.grid_first_slot_2_stop | Grid-first slot 2 stop | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1085 | holding | 1085 | control.grid_first_slot_2_enable | Grid-first slot 2 enable | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1086 | holding | 1086 | control.grid_first_slot_3_start | Grid-first slot 3 start | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1087 | holding | 1087 | control.grid_first_slot_3_stop | Grid-first slot 3 stop | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1088 | holding | 1088 | control.grid_first_slot_3_enable | Grid-first slot 3 enable | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1089 | holding | 1089 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1090 | holding | 1090 | battery.first.charge.rate | Battery-first charge power rate | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1091 | holding | 1091 | battery.first.stop.soc | Battery-first stop SOC | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1092 | holding | 1092 | control.battery_first_ac_charge_enable | Battery-first AC charge enable | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1099 | holding | 1099 |  | Register 1099 | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1100 | holding | 1100 | control.battery_first_slot_1_start | Battery-first slot 1 start | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1101 | holding | 1101 | control.battery_first_slot_1_stop | Battery-first slot 1 stop | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1102 | holding | 1102 | control.battery_first_slot_1_enable | Battery-first slot 1 enable | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1103 | holding | 1103 | control.battery_first_slot_2_start | Battery-first slot 2 start | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1104 | holding | 1104 | control.battery_first_slot_2_stop | Battery-first slot 2 stop | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1105 | holding | 1105 | control.battery_first_slot_2_enable | Battery-first slot 2 enable | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1106 | holding | 1106 | control.battery_first_slot_3_start | Battery-first slot 3 start | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1107 | holding | 1107 | control.battery_first_slot_3_stop | Battery-first slot 3 stop | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1108 | holding | 1108 | control.battery_first_slot_3_enable | Battery-first slot 3 enable | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1109 | holding | 1109 | field.unknown | / | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1110 | holding | 1110 | control.load_first_slot_1_start | Load-first slot 1 start | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1111 | holding | 1111 | control.load_first_slot_1_stop | Load-first slot 1 stop | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1112 | holding | 1112 | control.load_first_slot_1_enable | Load-first slot 1 enable | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1113 | holding | 1113 | control.load_first_slot_2_start | Load-first slot 2 start | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1114 | holding | 1114 | control.load_first_slot_2_stop | Load-first slot 2 stop | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1115 | holding | 1115 | control.load_first_slot_2_enable | Load-first slot 2 enable | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1116 | holding | 1116 | control.load_first_slot_3_start | Load-first slot 3 start | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1117 | holding | 1117 | control.load_first_slot_3_stop | Load-first slot 3 stop | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1118 | holding | 1118 | control.load_first_slot_3_enable | Load-first slot 3 enable | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1119 | holding | 1119 | control.energy_calculation_formula | Energy calculation formula | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1120 | holding | 1120 | control.backup_enable | Backup enable | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:1121 | holding | 1121 | control.sgip_enable | SGIP enable | read_write |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:8 | holding | 8 | telemetry.nominal_pv_voltage | Nominal PV voltage | read |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:row:032-0366 | holding | None |  | / |  |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:row:032-0369 | holding | None |  |  |  |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:row:033-0384 | holding | None |  |  |  |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:row:034-0408 | holding | None |  | 1124 |  |
| cb-holding-p027-six_group_for_storage_power-block-03:holding:row:035-0418 | holding | None |  |  |  |
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
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1000 | input | 1000 | control.uwsysworkmode | uwSysWorkMode | write |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1001 | input | 1001 | diagnostic.systemfaultword0 | Systemfaultword0 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1002 | input | 1002 | diagnostic.systemfaultword1 | Systemfaultword1 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1003 | input | 1003 | diagnostic.systemfaultword2 | Systemfaultword2 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1004 | input | 1004 | diagnostic.systemfaultword3 | Systemfaultword3 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1005 | input | 1005 | diagnostic.systemfaultword4 | Systemfaultword4 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1006 | input | 1006 | diagnostic.systemfaultword5 | Systemfaultword5 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1007 | input | 1007 | diagnostic.systemfaultword6 | Systemfaultword6 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1008 | input | 1008 | diagnostic.systemfaultword7 | Systemfaultword7 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1009 | input | 1009 | battery.discharge_power | Battery discharge power (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1010 | input | 1010 | field.pdischarge1l | Battery discharge power (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1011 | input | 1011 | battery.charge_power | Battery charge power (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1012 | input | 1012 | field.pcharge1l | Battery charge power (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1013 | input | 1013 | field.vbat | Vbat | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1014 | input | 1014 | battery.soc | Battery state of charge | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1015 | input | 1015 | field.pactouserr_h | PactouserR H (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1016 | input | 1016 | field.pactouserr_l | PactouserR H (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1017 | input | 1017 | field.pactousers_h | PactouserS H (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1018 | input | 1018 | field.pactousers_l | PactouserS H (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1019 | input | 1019 | field.pactousert_h | PactouserT H (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1020 | input | 1020 | field.pactousert_l | PactouserT H (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1021 | input | 1021 | field.pactousertotalh | PactouserTotalH (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1022 | input | 1022 | field.pactousertotall | PactouserTotalH (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1023 | input | 1023 | field.pactogridr_h | PactogridR H (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1024 | input | 1024 | field.pactogridr_l | PactogridR H (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1025 | input | 1025 | field.pactogrids_h | PactogridS H (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1026 | input | 1026 | field.pactogrids_l | PactogridS H (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1027 | input | 1027 | field.pactogridth | PactogridTH | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1028 | input | 1028 | field.pactogridtl | PactogridTL | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1029 | input | 1029 | field.pac_to_grid_total | pac_to_grid_total | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1030 | input | 1030 | field.pactogridtotall | PactogridtotalL | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1031 | input | 1031 | field.plocalloadr_h | PLocalLoadR H | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1032 | input | 1032 | field.plocalloadr_l | PLocalLoadR L | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1033 | input | 1033 | field.plocalloads_h | PLocalLoadS H | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1034 | input | 1034 | field.plocalloads_l | PLocalLoadS L | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1035 | input | 1035 | field.plocalloadt_h | PLocalLoadT H | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1036 | input | 1036 | field.plocalloadt_l | PLocalLoadT L | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1037 | input | 1037 | field.plocalloadtotalh | PLocalLoadtotalH | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1038 | input | 1038 | field.plocalloadtotall | PLocalLoadtotalL | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1039 | input | 1039 | diagnostic.ip2mtemperature | IP2MTemperature | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1040 | input | 1040 | diagnostic.b2attery_temperature | B2attery Temperature | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1041 | input | 1041 | diagnostic.spdspstatus | SPDSPStatus | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1042 | input | 1042 | field.spbusvolt | SPBusVolt | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1043 | input | 1043 |  | Register 1043 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1044 | input | 1044 | field.etouser_todayh | Etouser_todayH (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1045 | input | 1045 | control.etouser_todayl | Etouser_todayH (low word) | write |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1046 | input | 1046 | field.etouser_totalh | Etouser_totalH (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1047 | input | 1047 | field.etouser_totall | Etouser_totalH (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1048 | input | 1048 | field.etogrid_todayh | Etogrid_todayH (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1049 | input | 1049 | control.etogrid_todayl | Etogrid_todayH (low word) | write |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1050 | input | 1050 | field.etogrid_totalh | Etogrid_totalH (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1051 | input | 1051 | field.etogrid_totall | Etogrid_totalH (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1052 | input | 1052 | field.edischarge1_toda_yh | Edischarge1_toda yH (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1053 | input | 1053 | field.edischarge1_toda_yl | Edischarge1_toda yH (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1054 | input | 1054 | field.edischarge1_total_h | Edischarge1_total H (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1055 | input | 1055 | control.edischarge1_total_l | Edischarge1_total H (low word) | write |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1056 | input | 1056 | field.echarge1_todayh | Echarge1_todayH (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1057 | input | 1057 | field.echarge1_today_l | Echarge1_todayH (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1058 | input | 1058 | field.echarge1_totalh | Echarge1_totalH (high word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1059 | input | 1059 | field.echarge1_totall | Echarge1_totalH (low word) | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1060 | input | 1060 |  | Register 1060 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1061 | input | 1061 |  | Register 1061 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1062 | input | 1062 |  | Register 1062 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1063 | input | 1063 |  | Register 1063 | read |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1064 | input | 1064 |  | Register 1064 | write |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1065 | input | 1065 |  | Register 1065 | write |
| cb-input-p059-ninth_group_for_storage_power-block-10:input:1066 | input | 1066 |  | Register 1066 | read |
| cb-input-p062-bms_infomation-block-11:input:1082 | input | 1082 |  | Register 1082 | read |
| cb-input-p062-bms_infomation-block-11:input:1083 | input | 1083 |  | Register 1083 | read |
| cb-input-p062-bms_infomation-block-11:input:1084 | input | 1084 |  | Register 1084 | read |
| cb-input-p062-bms_infomation-block-11:input:1085 | input | 1085 |  | Register 1085 | read |
| cb-input-p062-bms_infomation-block-11:input:1086 | input | 1086 |  | Register 1086 | read |
| cb-input-p062-bms_infomation-block-11:input:1087 | input | 1087 |  | Register 1087 | read |
| cb-input-p062-bms_infomation-block-11:input:1088 | input | 1088 |  | Register 1088 | read |
| cb-input-p062-bms_infomation-block-11:input:1089 | input | 1089 |  | Register 1089 | read |
| cb-input-p062-bms_infomation-block-11:input:1090 | input | 1090 | battery.bms_maxcurr | BMS_MaxCurr | read |
| cb-input-p062-bms_infomation-block-11:input:1091 | input | 1091 | battery.bms_gaugerm | BMS_GaugeRM | read |
| cb-input-p062-bms_infomation-block-11:input:1092 | input | 1092 | battery.bms_gaugefcc | BMS_GaugeFCC | read |
| cb-input-p062-bms_infomation-block-11:input:1093 | input | 1093 | battery.bms_fw | BMS_FW | read |
| cb-input-p062-bms_infomation-block-11:input:1094 | input | 1094 | battery.bms_deltavolt | BMS_DeltaVolt | read |
| cb-input-p062-bms_infomation-block-11:input:1095 | input | 1095 | battery.bms_cyclecnt | BMS_CycleCnt | read |
| cb-input-p062-bms_infomation-block-11:input:1096 | input | 1096 | battery.bms_soh | BMS_SOH | read |
| cb-input-p062-bms_infomation-block-11:input:1097 | input | 1097 | battery.bms_constantv_olt | BMS_ConstantV olt | read |
| cb-input-p062-bms_infomation-block-11:input:1098 | input | 1098 | diagnostic.bms_warninfoo_ld | BMS_WarnInfoO ld | read |
| cb-input-p062-bms_infomation-block-11:input:1099 | input | 1099 | diagnostic.bms_warninfo | BMS_WarnInfo | read |
| cb-input-p062-bms_infomation-block-11:input:1100 | input | 1100 | battery.bms_gaugeiccu_rr | BMS_GaugeICCu rr | read |
| cb-input-p062-bms_infomation-block-11:input:1101 | input | 1101 | battery.bms_mcuversi_on | BMS_MCUVersi on | read |
| cb-input-p062-bms_infomation-block-11:input:1102 | input | 1102 | battery.bms_gaugevers_ion | BMS_GaugeVers ion | read |
| cb-input-p062-bms_infomation-block-11:input:1103 | input | 1103 | battery.bms_wgaugefr_version_l | BMS_wGaugeFR Version_L | read |
| cb-input-p062-bms_infomation-block-11:input:1104 | input | 1104 | battery.bms_wgaugefr_version_h | BMS_wGaugeFR Version_H | read |
| cb-input-p062-bms_infomation-block-11:input:1105 | input | 1105 | battery.bms_bmsinfo | BMS_BMSInfo | read |
| cb-input-p062-bms_infomation-block-11:input:1106 | input | 1106 | battery.bms_packinfo | BMS_PackInfo | read |
| cb-input-p062-bms_infomation-block-11:input:1107 | input | 1107 | battery.bms_usingcap | BMS_UsingCap | read |
| cb-input-p062-bms_infomation-block-11:input:1108 | input | 1108 | battery.uwmaxcellvolt | uwMaxCellVolt | read |
| cb-input-p062-bms_infomation-block-11:input:1109 | input | 1109 | battery.uwmincellvolt | uwMinCellVolt | read |
| cb-input-p062-bms_infomation-block-11:input:1110 | input | 1110 | field.bmodulenum | bModuleNum | read |
| cb-input-p062-bms_infomation-block-11:input:1111 | input | 1111 | field.numberofbatteries | Numberofbatteries | read |
| cb-input-p062-bms_infomation-block-11:input:1112 | input | 1112 | battery.uwmaxvoltcelln_o | uwMaxVoltCellN o | read |
| cb-input-p062-bms_infomation-block-11:input:1113 | input | 1113 | battery.uwminvoltcelln_o | uwMinVoltCellN o | read |
| cb-input-p062-bms_infomation-block-11:input:1114 | input | 1114 | field.uwmaxtemprce_ll_10t | uwMaxTemprCe ll_10T | read |
| cb-input-p062-bms_infomation-block-11:input:1115 | input | 1115 | field.uwmintemprcel_l_10t | uwMinTemprCel l_10T | read |
| cb-input-p062-bms_infomation-block-11:input:1116 | input | 1116 | field.uwmaxtemprce_llno | uwMaxTemprCe llNo | read |
| cb-input-p062-bms_infomation-block-11:input:1117 | input | 1117 | field.uwmintemprcel | uwMinTemprCel | read |
| cb-input-p062-bms_infomation-block-11:input:1118 | input | 1118 | field.protectpackid | ProtectpackID | read |
| cb-input-p062-bms_infomation-block-11:input:1119 | input | 1119 | battery.maxsoc | MaxSOC | read |
| cb-input-p062-bms_infomation-block-11:input:1120 | input | 1120 | battery.minsoc | MinSOC | read |
| cb-input-p062-bms_infomation-block-11:input:1121 | input | 1121 | battery.bms_error2 | BMS_Error2 | read |
| cb-input-p062-bms_infomation-block-11:input:1122 | input | 1122 | battery.bms_error3 | BMS_Error3 | read |
| cb-input-p062-bms_infomation-block-11:input:1123 | input | 1123 | diagnostic.bms_warninfo2 | BMS_WarnInfo2 | read |
| cb-input-p062-bms_infomation-block-11:input:1124 | input | 1124 | control.accharge_energytodayh | ACCharge EnergyTodayH | write |
| cb-input-p062-ups_information_offline-block-12:input:1067 | input | 1067 | field.epsfac | EpsFac | read |
| cb-input-p062-ups_information_offline-block-12:input:1068 | input | 1068 | field.epsvac1 | EpsVac1 | read |
| cb-input-p062-ups_information_offline-block-12:input:1069 | input | 1069 | field.epsiac1 | EpsIac1 | read |
| cb-input-p062-ups_information_offline-block-12:input:1070 | input | 1070 | field.epspac1 | EpsPac1 | read |
| cb-input-p062-ups_information_offline-block-12:input:1071 | input | 1071 | field.epspac1 | EpsPac1 | read |
| cb-input-p062-ups_information_offline-block-12:input:1072 | input | 1072 | field.epsvac2 | EpsVac2 | read |
| cb-input-p062-ups_information_offline-block-12:input:1073 | input | 1073 | field.epsiac2 | EpsIac2 | read |
| cb-input-p062-ups_information_offline-block-12:input:1074 | input | 1074 | field.epspac2 | EpsPac2 | read |
| cb-input-p062-ups_information_offline-block-12:input:1075 | input | 1075 | field.epspac2 | EpsPac2 | read |
| cb-input-p062-ups_information_offline-block-12:input:1076 | input | 1076 | field.epsvac3 | EpsVac3 | read |
| cb-input-p062-ups_information_offline-block-12:input:1077 | input | 1077 | field.epsiac3 | EpsIac3 | read |
| cb-input-p062-ups_information_offline-block-12:input:1078 | input | 1078 | field.epspac3 | EpsPac3 | read |
| cb-input-p062-ups_information_offline-block-12:input:1079 | input | 1079 | field.epspac3 | EpsPac3 | read |
| cb-input-p062-ups_information_offline-block-12:input:1080 | input | 1080 | field.epsloadpercent | EpsLoadPercent | read |
| cb-input-p062-ups_information_offline-block-12:input:1081 | input | 1081 | field.epspf | EpsPF | read |
