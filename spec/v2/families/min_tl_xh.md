# TL-X/TL-XH/TL-XH US (MIN Type)

`v124-instruction-min-tlx-tlxh`: TL-X/TL-XH/TL-XH US (MIN Type): 03 register range: 0~124, 3000~3124, 3125~3249 (TL-XH US); 04 register range: 3000~3124, 3125~3249, 3250~3374 (TL-XH)

| Applicability path | Resolved block |
| --- | --- |
| v124-holding-p009-first_group-block-01:v124-instruction-min-tlx-tlxh:holding:0:124:3 | declared/no semantic block |
| v124-holding-p035-use_for_tl_x_and_tl_xh-block-04:v124-instruction-min-tlx-tlxh:holding:3000:3124:3 | declared/no semantic block |
| v124-holding-p042-us_machine_type_time_set-block-05:v124-instruction-min-tlx-tlxh:holding:3125:3249:3:tl_xh_us | declared/no semantic block |
| v124-input-p070-use_for_tl_x_and_tl_xh-block-14:v124-instruction-min-tlx-tlxh:input:3000:3124:4 | declared/no semantic block |
| v124-input-p070-use_for_tl_x_and_tl_xh-block-14:v124-instruction-min-tlx-tlxh:input:3125:3249:4 | declared/no semantic block |
| v124-input-p070-use_for_tl_x_and_tl_xh-block-14:v124-instruction-min-tlx-tlxh:input:3250:3374:4:tl_xh | declared/no semantic block |

Block projections: `cb-holding-p009-first_group-block-01`, `cb-holding-p035-use_for_tl_x_and_tl_xh-block-04`, `cb-holding-p042-us_machine_type_time_set-block-05`, `cb-input-p070-use_for_tl_x_and_tl_xh-block-14`. Register rows below are references to shared block definitions; applicability does not duplicate them.

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
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3000 | holding | 3000 | control.export_limit_fallback_cap | Export-limit fallback cap | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3001 | holding | 3001 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3002 | holding | 3002 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3003 | holding | 3003 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3004 | holding | 3004 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3005 | holding | 3005 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3006 | holding | 3006 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3007 | holding | 3007 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3008 | holding | 3008 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3009 | holding | 3009 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3010 | holding | 3010 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3011 | holding | 3011 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3012 | holding | 3012 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3013 | holding | 3013 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3014 | holding | 3014 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3015 | holding | 3015 | control.serial_number | Serial Number | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3016 | holding | 3016 | control.dry_contact_enable | Dry-contact enable | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3017 | holding | 3017 | control.dry_contact_close_threshold | Dry-contact close threshold | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3018 | holding | 3018 | control.hybrid_work_mode | Hybrid work mode | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3019 | holding | 3019 | control.dry_contact_release_threshold | Dry-contact release threshold | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3020 | holding | 3020 | control.off_grid_box_control | Off-grid box control | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3021 | holding | 3021 | control.external_off_grid_enable | External off-grid enable | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3022 | holding | 3022 | telemetry.bdc_stop_work_bus_voltage | BDC stop-work bus voltage | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3023 | holding | 3023 | control.grid_topology_selection | Grid topology selection | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3024 | holding | 3024 | control.float_charge_current_limit | Float-charge current limit | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3025 | holding | 3025 | control.battery_low_warning_setpoint | Battery-low warning setpoint | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3026 | holding | 3026 | control.battery_low_warning_clear | Battery-low warning clear | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3027 | holding | 3027 | control.battery_discharge_cutoff | Battery discharge cutoff | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3028 | holding | 3028 | control.battery_charge_stop_voltage | Battery charge stop voltage | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3029 | holding | 3029 | battery.discharge_start_voltage | Battery discharge start voltage | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3030 | holding | 3030 | control.battery_constant_charge_voltage | Battery constant-charge voltage | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3031 | holding | 3031 | control.discharge_low_temperature_limit | Discharge low temperature limit | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3032 | holding | 3032 | control.discharge_high_temperature_limit | Discharge high temperature limit | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3033 | holding | 3033 | control.charge_low_temperature_limit | Charge low temperature limit | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3034 | holding | 3034 | control.charge_high_temperature_limit | Charge high temperature limit | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3035 | holding | 3035 | control.under_frequency_discharge_delay | Under-frequency discharge delay | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3036 | holding | 3036 | grid.first.discharge.rate | Grid-first discharge power rate | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3037 | holding | 3037 | grid.first.stop.soc | Grid-first stop SOC | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3038 | holding | 3038 | grid.first.schedule.1.start.control | Grid-first schedule 1 start/control | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3039 | holding | 3039 | grid.first.schedule.1.end | Grid-first schedule 1 end | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3040 | holding | 3040 | grid.first.schedule.2.start.control | Grid-first schedule 2 start/control | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3041 | holding | 3041 | grid.first.schedule.2.end | Grid-first schedule 2 end | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3042 | holding | 3042 | grid.first.schedule.3.start.control | Grid-first schedule 3 start/control | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3043 | holding | 3043 | grid.first.schedule.3.end | Grid-first schedule 3 end | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3044 | holding | 3044 | grid.first.schedule.4.start.control | Grid-first schedule 4 start/control | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3045 | holding | 3045 | grid.first.schedule.4.end | Grid-first schedule 4 end | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3046 | holding | 3046 |  | Reserved | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3047 | holding | 3047 | battery.first.charge.rate | Battery-first charge power rate | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3048 | holding | 3048 | battery.first.stop.soc | Battery-first stop SOC | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3049 | holding | 3049 | ac.charge.enabled | AC charging enabled | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3050 | holding | 3050 | battery.first.schedule.1.start.control | Battery-first schedule 1 start/control | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3051 | holding | 3051 | battery.first.schedule.1.end | Battery-first schedule 1 end | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3052 | holding | 3052 | battery.first.schedule.2.start.control | Battery-first schedule 2 start/control | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3053 | holding | 3053 | battery.first.schedule.2.end | Battery-first schedule 2 end | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3054 | holding | 3054 | battery.first.schedule.3.start.control | Battery-first schedule 3 start/control | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3055 | holding | 3055 | battery.first.schedule.3.end | Battery-first schedule 3 end | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3056 | holding | 3056 | battery.first.schedule.4.start.control | Battery-first schedule 4 start/control | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3057 | holding | 3057 | battery.first.schedule.4.end | Battery-first schedule 4 end | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3058 | holding | 3058 | battery.first.schedule.5.start.control | Battery-first schedule 5 start/control | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3059 | holding | 3059 | battery.first.schedule.5.end | Battery-first schedule 5 end | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3060 | holding | 3060 |  | Reserved | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3070 | holding | 3070 | battery.type | Battery type | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3071 | holding | 3071 | control.batmdlseria_paralnum | BatMdlSeria/ ParalNum | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3072 | holding | 3072 |  | Reserved | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3073 | holding | 3073 |  | Reserved | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3074 | holding | 3074 |  | Reserved | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3075 | holding | 3075 |  | Reserved | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3076 | holding | 3076 |  | Reserved | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3077 | holding | 3077 |  | Reserved | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3078 | holding | 3078 |  | Reserved | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3079 | holding | 3079 | ups.eps.function.enable | UPS/EPS function enable | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3080 | holding | 3080 | ups.eps.voltage.selection | UPS/EPS voltage selection | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3081 | holding | 3081 | ups.eps.frequency.selection | UPS/EPS frequency selection | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3082 | holding | 3082 | load.first.stop.soc | Load-first stop SOC | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3083 | holding | 3083 |  | Reserved | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3084 | holding | 3084 |  | Reserved | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3085 | holding | 3085 | bdc_bms_slave_address | BDC/BMS RS485 communication address | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3086 | holding | 3086 | bdc_bms_rs485_baud_rate | BDC/BMS RS485 baud-rate selector | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3087 | holding | 3087 | control.battery_rack_serial | Battery rack serial | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3088 | holding | 3088 | control.battery_rack_serial | Battery rack serial | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3089 | holding | 3089 | control.battery_rack_serial | Battery rack serial | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3090 | holding | 3090 | control.battery_rack_serial | Battery rack serial | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3091 | holding | 3091 | control.battery_rack_serial | Battery rack serial | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3092 | holding | 3092 | control.battery_rack_serial | Battery rack serial | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3093 | holding | 3093 | control.battery_rack_serial | Battery rack serial | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3094 | holding | 3094 | control.battery_rack_serial | Battery rack serial | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3095 | holding | 3095 | control.bdc_reset_command | BDC reset command | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3096 | holding | 3096 | field.bdc_monitoring_code | BDC monitoring code | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3097 | holding | 3097 | field.bdc_monitoring_code | BDC monitoring code | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3098 | holding | 3098 | field.bdc_dtc_code | BDC DTC code | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3099 | holding | 3099 | field.dsp_firmware_code | DSP firmware code | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3100 | holding | 3100 | field.dsp_firmware_code | DSP firmware code | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3101 | holding | 3101 | field.dsp_firmware_version | DSP firmware version | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3102 | holding | 3102 | telemetry.bus_voltage_reference | Bus voltage reference | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3103 | holding | 3103 | field.bdc_monitor_firmware | BDC monitor firmware | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3104 | holding | 3104 | battery.bms_mcu_hardware_version | BMS MCU hardware version | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3105 | holding | 3105 | battery.bms_firmware_version | BMS firmware version | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3106 | holding | 3106 | battery.bms_manufacturer | BMS manufacturer | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3107 | holding | 3107 | battery.bms_communication_interface | BMS communication interface | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3108 | holding | 3108 | control.bdc_module_identifier_4 | BDC module identifier 4 | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3109 | holding | 3109 | control.bdc_module_identifier_3 | BDC module identifier 3 | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3110 | holding | 3110 | control.bdc_module_identifier_2 | BDC module identifier 2 | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3111 | holding | 3111 | control.bdc_module_identifier_1 | BDC module identifier 1 | read_write |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3112 | holding | 3112 |  | Reserved | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3113 | holding | 3113 | field.bdc_protocol_version | BDC protocol version | read |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04:holding:3114 | holding | 3114 | field.bdc_certification_version | BDC certification version | read |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3125 | holding | 3125 | control.us_tou_month_groups | Us Tou Month Groups | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3126 | holding | 3126 | control.us_tou_month_groups | Us Tou Month Groups | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3127 | holding | 3127 | control.us_tou_month_groups | Us Tou Month Groups | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3128 | holding | 3128 | control.us_tou_month_groups | Us Tou Month Groups | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3129 | holding | 3129 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3130 | holding | 3130 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3131 | holding | 3131 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3133 | holding | 3133 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3135 | holding | 3135 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3137 | holding | 3137 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3139 | holding | 3139 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3141 | holding | 3141 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3143 | holding | 3143 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3145 | holding | 3145 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3147 | holding | 3147 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3149 | holding | 3149 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3151 | holding | 3151 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3153 | holding | 3153 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3155 | holding | 3155 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3157 | holding | 3157 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3159 | holding | 3159 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3161 | holding | 3161 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3163 | holding | 3163 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3165 | holding | 3165 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3167 | holding | 3167 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3169 | holding | 3169 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3171 | holding | 3171 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3173 | holding | 3173 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3175 | holding | 3175 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3177 | holding | 3177 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3179 | holding | 3179 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3181 | holding | 3181 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3183 | holding | 3183 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3185 | holding | 3185 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3187 | holding | 3187 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3189 | holding | 3189 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3191 | holding | 3191 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3193 | holding | 3193 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3195 | holding | 3195 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3197 | holding | 3197 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3199 | holding | 3199 | control.us_tou_slot_table | Us Tou Slot Table | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3201 | holding | 3201 | control.us_tou_special_day_1 | Us Tou Special Day 1 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3202 | holding | 3202 | control.us_tou_special_day_1 | Us Tou Special Day 1 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3203 | holding | 3203 | control.us_tou_special_day_1 | Us Tou Special Day 1 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3204 | holding | 3204 | control.us_tou_special_day_1 | Us Tou Special Day 1 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3206 | holding | 3206 | control.us_tou_special_day_1 | Us Tou Special Day 1 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3208 | holding | 3208 | control.us_tou_special_day_1 | Us Tou Special Day 1 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3210 | holding | 3210 | control.us_tou_special_day_1 | Us Tou Special Day 1 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3212 | holding | 3212 | control.us_tou_special_day_1 | Us Tou Special Day 1 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3214 | holding | 3214 | control.us_tou_special_day_1 | Us Tou Special Day 1 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3216 | holding | 3216 | control.us_tou_special_day_1 | Us Tou Special Day 1 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3218 | holding | 3218 | control.us_tou_special_day_1 | Us Tou Special Day 1 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3220 | holding | 3220 | control.us_tou_special_day_2 | Us Tou Special Day 2 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3221 | holding | 3221 | control.us_tou_special_day_2 | Us Tou Special Day 2 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3222 | holding | 3222 | control.us_tou_special_day_2 | Us Tou Special Day 2 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3223 | holding | 3223 | control.us_tou_special_day_2 | Us Tou Special Day 2 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3225 | holding | 3225 | control.us_tou_special_day_2 | Us Tou Special Day 2 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3227 | holding | 3227 | control.us_tou_special_day_2 | Us Tou Special Day 2 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3229 | holding | 3229 | control.us_tou_special_day_2 | Us Tou Special Day 2 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3231 | holding | 3231 | control.us_tou_special_day_2 | Us Tou Special Day 2 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3233 | holding | 3233 | control.us_tou_special_day_2 | Us Tou Special Day 2 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3235 | holding | 3235 | control.us_tou_special_day_2 | Us Tou Special Day 2 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3237 | holding | 3237 | control.us_tou_special_day_2 | Us Tou Special Day 2 | read_write |
| cb-holding-p042-us_machine_type_time_set-block-05:holding:3239 | holding | 3239 | control.us_tou_reserved_block | Us Tou Reserved Block | read_write |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3000 | input | 3000 | inverter.status | Inverter operating status | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3001 | input | 3001 | pv.total_power | PV total power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3002 | input | 3002 | telemetry.pv_input_power | PV total power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3003 | input | 3003 | telemetry.pv1_voltage | PV1 voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3004 | input | 3004 | telemetry.pv1_current | PV1 current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3005 | input | 3005 | telemetry.pv1_power | PV1 power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3006 | input | 3006 | telemetry.pv1_dc_power | PV1 power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3007 | input | 3007 | telemetry.pv2_voltage | PV2 voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3008 | input | 3008 | telemetry.pv2_current | PV2 current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3009 | input | 3009 | telemetry.pv2_power | PV2 power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3010 | input | 3010 | telemetry.pv2_dc_power | PV2 power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3011 | input | 3011 | telemetry.pv3_dc_voltage | PV3 DC voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3012 | input | 3012 | telemetry.pv3_dc_current | PV3 DC current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3013 | input | 3013 | telemetry.pv3_dc_power | PV3 DC power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3014 | input | 3014 | telemetry.pv3_dc_power | PV3 DC power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3015 | input | 3015 | telemetry.pv4_dc_voltage | PV4 DC voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3016 | input | 3016 | telemetry.pv4_dc_current | PV4 DC current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3017 | input | 3017 | telemetry.pv4_dc_power | PV4 DC power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3018 | input | 3018 | telemetry.pv4_dc_power | PV4 DC power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3019 | input | 3019 | telemetry.system_output_power | System output power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3020 | input | 3020 | telemetry.system_output_power | System output power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3021 | input | 3021 | telemetry.output_reactive_power | Output reactive power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3022 | input | 3022 | telemetry.output_reactive_power | Output reactive power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3023 | input | 3023 | telemetry.ac_output_power | AC output power | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3024 | input | 3024 | telemetry.ac_output_power | AC output power | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3025 | input | 3025 | grid.frequency | Grid frequency | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3026 | input | 3026 | telemetry.ac_phase_l1_voltage | AC phase L1 voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3027 | input | 3027 | telemetry.ac_phase_l1_current | AC phase L1 current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3028 | input | 3028 | telemetry.ac_phase_l1_power | AC phase L1 power | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3029 | input | 3029 | telemetry.ac_phase_l1_power | AC phase L1 power | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3030 | input | 3030 | telemetry.ac_phase_l2_voltage | AC phase L2 voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3031 | input | 3031 | telemetry.ac_phase_l2_current | AC phase L2 current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3032 | input | 3032 | telemetry.ac_phase_l2_power | AC phase L2 power | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3033 | input | 3033 | telemetry.ac_phase_l2_power | AC phase L2 power | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3034 | input | 3034 | telemetry.ac_phase_l3_voltage | AC phase L3 voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3035 | input | 3035 | telemetry.ac_phase_l3_current | AC phase L3 current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3036 | input | 3036 | ac.phase.l3_power | AC phase L3 power | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3037 | input | 3037 | ac.phase.l3_power | AC phase L3 power | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3038 | input | 3038 | telemetry.rs_line_voltage | RS line voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3039 | input | 3039 | telemetry.st_line_voltage | ST line voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3040 | input | 3040 | telemetry.tr_line_voltage | TR line voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3041 | input | 3041 | grid.import_power | Grid import power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3042 | input | 3042 | telemetry.load_supply_power | Grid import power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3043 | input | 3043 | grid.export_power | Grid export power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3044 | input | 3044 | grid.export_power | Grid export power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3045 | input | 3045 | load.house_power | House load power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3046 | input | 3046 | telemetry.home_load_power | House load power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3047 | input | 3047 | inverter.runtime | Inverter runtime | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3048 | input | 3048 | field.inverter_runtime | Inverter runtime | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3049 | input | 3049 | telemetry.ac_energy_today | AC energy today | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3050 | input | 3050 | telemetry.output_energy_today | Output energy today | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3051 | input | 3051 | telemetry.output_energy_total | Output energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3052 | input | 3052 | telemetry.output_energy_total | Output energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3053 | input | 3053 | telemetry.pv_energy_total | PV energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3054 | input | 3054 | telemetry.pv_energy_total | PV energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3055 | input | 3055 | telemetry.pv1_energy_today | PV1 energy today | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3056 | input | 3056 | telemetry.pv1_energy_today | PV1 energy today | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3057 | input | 3057 | telemetry.pv1_energy_total | PV1 energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3058 | input | 3058 | telemetry.pv1_energy_total | PV1 energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3059 | input | 3059 | telemetry.pv2_energy_today | PV2 energy today | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3060 | input | 3060 | telemetry.pv2_energy_today | PV2 energy today | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3061 | input | 3061 | telemetry.pv2_energy_total | PV2 energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3062 | input | 3062 | telemetry.pv2_energy_total | PV2 energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3063 | input | 3063 | telemetry.pv3_energy_today | PV3 energy today | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3064 | input | 3064 | telemetry.pv3_energy_today | PV3 energy today | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3065 | input | 3065 | telemetry.pv3_energy_total | PV3 energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3066 | input | 3066 | telemetry.pv3_energy_total | PV3 energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3067 | input | 3067 | telemetry.load_energy_today | Load energy today (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3068 | input | 3068 | telemetry.load_energy_today | Load energy today (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3069 | input | 3069 | telemetry.load_energy_total | Load energy total (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3070 | input | 3070 | telemetry.load_energy_total | Load energy total (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3071 | input | 3071 | grid.export_energy_today | Grid export energy today (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3072 | input | 3072 | grid.export_energy_today | Grid export energy today (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3073 | input | 3073 | grid.export_energy_total | Grid export energy total (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3074 | input | 3074 | grid.export_energy_total | Grid export energy total (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3075 | input | 3075 | telemetry.user_load_energy_today | User load energy today (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3076 | input | 3076 | telemetry.user_load_energy_today | User load energy today (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3077 | input | 3077 | telemetry.user_load_energy_total | User load energy total (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3078 | input | 3078 | telemetry.user_load_energy_total | User load energy total (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3079 | input | 3079 | telemetry.pv4_energy_today | PV4 energy today | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3080 | input | 3080 | telemetry.pv4_energy_today | PV4 energy today | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3081 | input | 3081 | pv.mppt4.energy_total | PV4 energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3082 | input | 3082 | pv.mppt4.energy_total | PV4 energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3083 | input | 3083 | telemetry.pv_energy_today | PV energy today (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3084 | input | 3084 | telemetry.pv_energy_today | PV energy today (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3085 | input | 3085 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3086 | input | 3086 | diagnostic.derating_mode | Derating mode | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3087 | input | 3087 | field.pv_insulation_resistance | PV insulation resistance | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3088 | input | 3088 | telemetry.residual_current_r | Residual current R | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3089 | input | 3089 | telemetry.residual_current_s | Residual current S | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3090 | input | 3090 | telemetry.residual_current_t | Residual current T | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3091 | input | 3091 | telemetry.gfci_current | GFCI current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3092 | input | 3092 | telemetry.total_bus_voltage | Total bus voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3093 | input | 3093 | diagnostic.inverter_temperature | Inverter temperature | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3094 | input | 3094 | diagnostic.ipm_temperature | IPM temperature | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3095 | input | 3095 | diagnostic.boost_temperature | Boost temperature | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3096 | input | 3096 | field.temp4 | Temp4 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3097 | input | 3097 | diagnostic.communication_board_temperature | Communication board temperature | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3098 | input | 3098 | telemetry.p_bus_voltage | P-bus voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3099 | input | 3099 | telemetry.n_bus_voltage | N-bus voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3100 | input | 3100 | telemetry.inverter_output_power_factor | Inverter output power factor | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3101 | input | 3101 | telemetry.output_power_percentage | Output power percentage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3102 | input | 3102 | telemetry.output_max_power_limit | Output max power limit (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3103 | input | 3103 | telemetry.output_max_power_limit | Output max power limit (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3104 | input | 3104 | field.standby_flags | Standby flags | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3105 | input | 3105 | diagnostic.fault_code | Fault code | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3106 | input | 3106 | diagnostic.warning_main_code | Warning main code | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3107 | input | 3107 | diagnostic.fault_subcode | Fault subcode | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3108 | input | 3108 | diagnostic.warning_subcode | Warning subcode | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3109 | input | 3109 |  | Register 3109 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3110 | input | 3110 | inverter.warning_flags | Inverter warning bitfield | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3111 | input | 3111 | inverter.present_fft_value_channel_a | Present FFT value (vendor channel A) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3112 | input | 3112 | diagnostic.afci_status | AFCI status | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3113 | input | 3113 | field.afci_strength_channel_a | AFCI strength (channel A) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3114 | input | 3114 | field.afci_self_check_channel_a | AFCI self-check (channel A) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3115 | input | 3115 | field.inverter_start_delay | Inverter start delay | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3116 | input | 3116 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3117 | input | 3117 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3118 | input | 3118 | field.bdc_connect_state | BDC connect state | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3119 | input | 3119 | field.dry_contact_state | Dry contact state | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3120 | input | 3120 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3121 | input | 3121 | telemetry.self_use_power | Self-use power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3122 | input | 3122 | telemetry.self_use_power | Self-use power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3123 | input | 3123 | telemetry.system_energy_today | System energy today (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3124 | input | 3124 | telemetry.system_energy_today | System energy today (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3125 | input | 3125 | battery.discharge_energy_today | Battery discharge energy today (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3126 | input | 3126 | battery.discharge_energy_today | Battery discharge energy today (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3127 | input | 3127 | battery.discharge_energy_total | Battery discharge energy total (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3128 | input | 3128 | battery.discharge_energy_total | Battery discharge energy total (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3129 | input | 3129 | battery.charge_energy_today | Battery charge energy today (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3130 | input | 3130 | battery.charge_energy_today | Battery charge energy today (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3131 | input | 3131 | battery.charge_energy_total | Battery charge energy total (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3132 | input | 3132 | battery.charge_energy_total | Battery charge energy total (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3133 | input | 3133 | battery.ac_charge_energy_today | AC charge energy today (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3134 | input | 3134 | battery.ac_charge_energy_today | AC charge energy today (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3135 | input | 3135 | battery.ac_charge_energy_total | AC charge energy total (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3136 | input | 3136 | battery.ac_charge_energy_total | AC charge energy total (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3137 | input | 3137 | telemetry.system_energy_total | System energy total (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3138 | input | 3138 | telemetry.system_energy_total | System energy total (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3139 | input | 3139 | telemetry.self_use_energy_today | Self-use energy today (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3140 | input | 3140 | telemetry.self_use_energy_today | Self-use energy today (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3141 | input | 3141 | telemetry.self_use_energy_total | Self-use energy total (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3142 | input | 3142 | telemetry.self_use_energy_total | Self-use energy total (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3143 | input | 3143 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3144 | input | 3144 | field.priority_mode | Priority mode | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3145 | input | 3145 | telemetry.eps_frequency | EPS frequency | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3146 | input | 3146 | telemetry.eps_phase_r_voltage | EPS phase R voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3147 | input | 3147 | telemetry.eps_phase_r_current | EPS phase R current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3148 | input | 3148 | telemetry.eps_phase_r_apparent_power | EPS phase R apparent power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3149 | input | 3149 | telemetry.eps_phase_r_apparent_power | EPS phase R apparent power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3150 | input | 3150 | telemetry.eps_phase_s_voltage | EPS phase S voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3151 | input | 3151 | telemetry.eps_phase_s_current | EPS phase S current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3152 | input | 3152 | telemetry.eps_phase_s_apparent_power | EPS phase S apparent power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3153 | input | 3153 | telemetry.eps_phase_s_apparent_power | EPS phase S apparent power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3154 | input | 3154 | telemetry.eps_phase_t_voltage | EPS phase T voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3155 | input | 3155 | telemetry.eps_phase_t_current | EPS phase T current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3156 | input | 3156 | ac.phase.l3_power | AC phase L3 power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3157 | input | 3157 | ac.phase.l3_power | AC phase L3 power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3158 | input | 3158 | telemetry.eps_total_apparent_power | EPS total apparent power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3159 | input | 3159 | telemetry.eps_total_apparent_power | EPS total apparent power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3160 | input | 3160 | field.eps_load_percentage | EPS load percentage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3161 | input | 3161 | telemetry.bdc_power_factor | BDC power factor | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3162 | input | 3162 | telemetry.bdc_dc_voltage | BDC DC voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3163 | input | 3163 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3164 | input | 3164 | bdc.data_separation | BDC data-separation flag | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3165 | input | 3165 | bdc.derating_mode | BDC derating mode | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3166 | input | 3166 | bdc.system_mode_status | BDC system mode and status | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3167 | input | 3167 | bdc.fault_code | BDC fault code | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3168 | input | 3168 | bdc.warning_code | BDC warning code | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3169 | input | 3169 | battery.voltage | Battery voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3170 | input | 3170 | battery.current | Battery current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3171 | input | 3171 | battery.soc | Battery state of charge | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3172 | input | 3172 | telemetry.vbus1_voltage | VBUS1 voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3173 | input | 3173 | telemetry.vbus2_voltage | VBUS2 voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3174 | input | 3174 | telemetry.buck_boost_current | Buck/boost current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3175 | input | 3175 | telemetry.llc_stage_current | LLC stage current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3176 | input | 3176 | diagnostic.battery_temperature_a | Battery temperature A | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3177 | input | 3177 | diagnostic.battery_temperature_b | Battery temperature B | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3178 | input | 3178 | battery.discharge_power | Battery discharge power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3179 | input | 3179 | battery.discharge_power | Battery discharge power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3180 | input | 3180 | battery.charge_power | Battery charge power (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3181 | input | 3181 | battery.charge_power | Battery charge power (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3182 | input | 3182 | telemetry.bdc_discharge_energy_total | BDC discharge energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3183 | input | 3183 | telemetry.bdc_discharge_energy_total | BDC discharge energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3184 | input | 3184 | telemetry.bdc_charge_energy_total | BDC charge energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3185 | input | 3185 | telemetry.bdc_charge_energy_total | BDC charge energy total | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3186 | input | 3186 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3187 | input | 3187 | field.bdc_flag_word | BDC flag word | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3188 | input | 3188 | telemetry.vbus2_low_voltage | VBUS2 low voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3189 | input | 3189 | battery.bms_max_cell_index | BMS max cell index | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3190 | input | 3190 | battery.bms_min_cell_index | BMS min cell index | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3191 | input | 3191 | diagnostic.bms_average_temperature_channel_a | BMS average temperature (vendor channel A) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3192 | input | 3192 | diagnostic.bms_max_cell_temperature_a | BMS max cell temperature A | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3193 | input | 3193 | diagnostic.bms_average_temperature_b | BMS average temperature B | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3194 | input | 3194 | diagnostic.bms_max_cell_temperature_channel_b | BMS maximum cell temperature (vendor channel B) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3195 | input | 3195 | diagnostic.bms_average_temperature_channel_c | BMS average temperature (vendor channel C) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3196 | input | 3196 | battery.bms_max_soc | BMS maximum SOC | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3197 | input | 3197 | battery.bms_min_soc | BMS minimum SOC | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3198 | input | 3198 | battery.parallel_battery_count | Parallel battery count | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3199 | input | 3199 | control.bms_derate_reason | BMS derate reason | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3200 | input | 3200 | battery.bms_full_charge_capacity | BMS gauge full-charge capacity | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3201 | input | 3201 | battery.bms_remaining_capacity | BMS gauge remaining capacity | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3202 | input | 3202 | battery.bms_protect_flags_1 | BMS protect flags 1 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3203 | input | 3203 | diagnostic.bms_warning_flags_1 | BMS warning flags 1 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3204 | input | 3204 | diagnostic.bms_fault_flags_1 | BMS fault flags 1 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3205 | input | 3205 | diagnostic.bms_fault_flags_2 | BMS fault flags 2 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3206 | input | 3206 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3207 | input | 3207 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3208 | input | 3208 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3209 | input | 3209 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3210 | input | 3210 | diagnostic.battery_insulation_status | Battery insulation status | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3211 | input | 3211 | battery.request_flags | Battery request flags | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3212 | input | 3212 | diagnostic.bms_status | BMS status | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3213 | input | 3213 | battery.bms_protect_flags_2 | BMS protect flags 2 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3214 | input | 3214 | diagnostic.bms_warning_flags_2 | BMS warning flags 2 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3215 | input | 3215 | battery.soc | Battery state of charge | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3216 | input | 3216 | battery.voltage | Battery voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3217 | input | 3217 | battery.current | Battery current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3218 | input | 3218 | diagnostic.bms_max_cell_temperature | BMS max cell temperature | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3219 | input | 3219 | battery.bms_max_charge_current | BMS max charge current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3220 | input | 3220 | battery.bms_max_discharge_current | BMS max discharge current | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3221 | input | 3221 | battery.bms_cycle_count | BMS cycle count | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3222 | input | 3222 | battery.bms_soh | BMS state of health | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3223 | input | 3223 | battery.bms_charge_voltage_limit | BMS charge voltage limit | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3224 | input | 3224 | battery.bms_discharge_voltage_limit | BMS discharge voltage limit | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3225 | input | 3225 | diagnostic.bms_warning_flags_3 | BMS warning flags 3 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3226 | input | 3226 | battery.bms_protect_flags_3 | BMS protect flags 3 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3227 | input | 3227 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3228 | input | 3228 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3229 | input | 3229 |  | Reserved | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3230 | input | 3230 | battery.bms_max_cell_voltage | BMS maximum cell voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3231 | input | 3231 | battery.bms_min_cell_voltage | BMS minimum cell voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3232 | input | 3232 | battery.load_voltage | Battery load voltage | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3233 | input | 3233 |  | Register 3233 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3234 | input | 3234 | field.debug_data_1 | Debug data 1 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3235 | input | 3235 | field.debug_data_2 | Debug data 2 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3236 | input | 3236 | field.debug_data_3 | Debug data 3 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3237 | input | 3237 | field.debug_data_4 | Debug data 4 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3238 | input | 3238 | field.debug_data_5 | Debug data 5 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3239 | input | 3239 | field.debug_data_6 | Debug data 6 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3240 | input | 3240 | field.debug_data_7 | Debug data 7 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3241 | input | 3241 | field.debug_data_8 | Debug data 8 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3242 | input | 3242 | field.debug_data_9 | Debug data 9 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3243 | input | 3243 | field.debug_data_10 | Debug data 10 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3244 | input | 3244 | field.debug_data_11 | Debug data 11 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3245 | input | 3245 | field.debug_data_12 | Debug data 12 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3246 | input | 3246 | field.debug_data_13 | Debug data 13 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3247 | input | 3247 | field.debug_data_14 | Debug data 14 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3248 | input | 3248 | field.debug_data_15 | Debug data 15 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3249 | input | 3249 | field.debug_data_16 | Debug data 16 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3250 | input | 3250 | field.pex1h | Pex1H (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3251 | input | 3251 | field.pex1l | Pex1H (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3252 | input | 3252 | field.pex2h | Pex2H (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3253 | input | 3253 | field.pex2l | Pex2H (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3254 | input | 3254 | field.eex1todayh | Eex1TodayH (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3255 | input | 3255 | field.eex1todayl | Eex1TodayH (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3256 | input | 3256 | field.eex2todayh | Eex2TodayH (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3257 | input | 3257 | field.eex2todayl | Eex2TodayH (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3258 | input | 3258 | field.eex1totalh | Eex1TotalH (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3259 | input | 3259 | field.eex1totall | Eex1TotalH (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3260 | input | 3260 | field.eex2totalh | Eex2TotalH (high word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3261 | input | 3261 | field.eex2totall | Eex2TotalH (low word) | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3262 | input | 3262 | field.uwbatno | uwBatNo | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3263 | input | 3263 | field.batserialnum1 | BatSerialNum1 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3264 | input | 3264 | field.batserialnum2 | BatSerialNum2 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3265 | input | 3265 | field.batserialnum3 | BatSerialNum3 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3266 | input | 3266 | field.batserialnum4 | BatSerialNum4 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3267 | input | 3267 | field.batserialnum5 | BatSerialNum5 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3268 | input | 3268 | field.batserialnum6 | BatSerialNum6 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3269 | input | 3269 | field.batserialnum7 | BatSerialNum7 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3270 | input | 3270 | field.batserialnum8 | BatSerialNum8 | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3271 | input | 3271 | field.reserve | Reserve | read |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14:input:3280 | input | 3280 | field.clear_current_day_data_flag | Clear current-day data flag | read |
