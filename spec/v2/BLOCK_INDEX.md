# Block Index

| Block | Table | Function | Range | Register definitions | Applicability paths |
| --- | --- | --- | --- | --- | --- |
| cb-holding-p009-first_group-block-01 | holding | FC03 | 0–124 | 125 | 7 |
| cb-holding-p016-second_group-block-02 | holding | FC03 | 125–660 | 182 | 2 |
| cb-holding-p027-six_group_for_storage_power-block-03 | holding | FC03 | 1000–1249 | 117 | 3 |
| cb-holding-p035-use_for_tl_x_and_tl_xh-block-04 | holding | FC03 | 3000–3124 | 106 | 2 |
| cb-holding-p042-us_machine_type_time_set-block-05 | holding | FC03 | 3125–3249 | 64 | 1 |
| cb-holding-p047-bdc_information_support_up_to_10_parallel_bdc-block-06 | holding | FC03 | 5000–5079 | 4 | 0 |
| cb-input-p047-first_group-block-07 | input | FC04 | 0–124 | 122 | 4 |
| cb-input-p051-second_group-block-08 | input | FC04 | 125–249 | 125 | 2 |
| cb-input-p056-the_eighth_group_for_pv9_pv16_information-block-09 | input | FC04 | 875–999 | 120 | 1 |
| cb-input-p059-ninth_group_for_storage_power-block-10 | input | FC04 | 1000–1066 | 67 | 3 |
| cb-input-p062-bms_infomation-block-11 | input | FC04 | 1082–1124 | 43 | 3 |
| cb-input-p062-ups_information_offline-block-12 | input | FC04 | 1067–1081 | 15 | 3 |
| cb-input-p064-ninth_group_reserved_for_storage_power-block-13 | input | FC04 | 1125–2124 | 116 | 3 |
| cb-input-p070-use_for_tl_x_and_tl_xh-block-14 | input | FC04 | 3000–3280 | 273 | 5 |
| cb-input-p084-bdc_and_bms_information_support_up_to_10_parallel_bdcs-block-15 | input | FC04 | 4000–5079 | 5 | 0 |

## Reserved ranges

| Range | Table | Start | End | Status | Basis |
| --- | --- | --- | --- | --- | --- |
| holding:3115-3124 | holding | 3115 | 3124 | RESERVED | vendor_explicit_reserved |
| input:3281-3374 | input | 3281 | 3374 | RESERVED | vendor_specified_range, no_individual_semantic_rows, stock_shine_reads_range, runtime_all_zero |

Reserved ranges are first-class and never materialized as semantic registers.
