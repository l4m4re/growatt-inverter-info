"""Tests for the public Home Assistant consumer reconciliation tool."""

import json
from pathlib import Path

from tools.audit_homeassistant_consumer import compare, effective_decoder

REPO = Path(__file__).parents[1]


def load_spec() -> dict:
    """Load the canonical register specification."""
    return json.loads((REPO / "spec/growatt-register-spec.json").read_text())


def test_effective_decoder_matches_runtime_float32_behavior() -> None:
    """The audit models the consumer's signed two-word float decoder."""
    assert effective_decoder(
        {"value_type": "float", "length": 2, "signed": False, "scale": 10}
    ) == {"datatype": "s32", "signed": True, "scale": 10}
    assert effective_decoder(
        {"value_type": "float", "length": 2, "signed": False, "scale": 10},
        "mapping_declared",
    ) == {"datatype": "u32", "signed": False, "scale": 10}


def test_warning_bitfield_flags_unsupported_two_word_mapping() -> None:
    """I3110 remains one physical warning word and I3111 remains separate."""
    spec = load_spec()
    records = {record["physical_id"]: record for record in spec["registers"]}
    mapping = {
        "device": "tlx",
        "group": "input_tl_xh",
        "family": "min_tl_xh",
        "table": "input",
        "source_file": "custom_components/growatt_local/API/device_type/inverter_120.py",
        "register": 3110,
        "name": "warning_code",
        "length": 2,
        "value_type": "int",
        "signed": False,
        "scale": None,
        "read_write": "r",
        "function_path": "input_tl_xh",
    }

    result = compare(mapping, records["min_tl_xh:input:3110"], None, spec["logical_fields"])

    assert result["mismatch_classification"] == "LENGTH_MISMATCH"
    assert result["required_action"] == "DECODE_FIX_REQUIRED"
    assert result["canonical"]["physical_length_words"] == 1
