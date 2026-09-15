# Protocols and native read layout

## `120_v124`

```json
{
  "maximum_read_words": 125,
  "maximum_write_words": 125,
  "minimum_cmd_period_ms": 850,
  "native_read_blocks": [
    {
      "applicability": "TL-X/TL-XH",
      "count": 125,
      "end": 124,
      "start": 0,
      "table": "holding"
    },
    {
      "applicability": "TL-X/TL-XH",
      "count": 125,
      "end": 3124,
      "start": 3000,
      "table": "holding"
    },
    {
      "applicability": "TL-XH US where applicable",
      "count": 125,
      "end": 3249,
      "start": 3125,
      "table": "holding"
    },
    {
      "applicability": "TL-X/TL-XH",
      "count": 125,
      "end": 3124,
      "start": 3000,
      "table": "input"
    },
    {
      "applicability": "TL-X/TL-XH",
      "count": 125,
      "end": 3249,
      "start": 3125,
      "table": "input"
    },
    {
      "applicability": "TL-XH",
      "count": 125,
      "end": 3374,
      "start": 3250,
      "table": "input"
    }
  ],
  "recommended_cmd_period_ms": 1000,
  "source": "vendor_v124"
}
```

## `legacy_315`

```json
{
  "boundary_rules": "Vendor V3.14/3.15 grouping restrictions apply.",
  "maximum_read_words": 45,
  "maximum_write_words": 45,
  "minimum_cmd_period_ms": 850,
  "recommended_cmd_period_ms": 1000,
  "source": "protocol_v314"
}
```
