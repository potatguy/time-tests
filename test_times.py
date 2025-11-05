
import pytest
import yaml
from times import time_range, compute_overlap_time, iss_passes
from unittest.mock import patch
import requests

# --- Load fixture.yaml once ---
def load_fixtures():
    with open("fixture.yaml", "r") as f:
        return yaml.safe_load(f)

@pytest.mark.parametrize("case_data", load_fixtures())
def test_compute_overlap(case_data):
    # Get the single key (case name)
    case_name, data = next(iter(case_data.items()))

    tr1 = time_range(
        data["time_range_1"]["start"],
        data["time_range_1"]["end"],
        data["time_range_1"].get("step_minutes", 1),
        data["time_range_1"].get("duration_seconds", 0)
    )

    tr2 = time_range(
        data["time_range_2"]["start"],
        data["time_range_2"]["end"],
        data["time_range_2"].get("step_minutes", 1),
        data["time_range_2"].get("duration_seconds", 0)
    )

    result = compute_overlap_time(tr1, tr2)
    expected = [tuple(e) for e in data["expected"]] 

    assert result == expected

def test_iss_pass_default_params():
    with patch.object(requests, 'get') as mock_get:
        iss_times = iss_passes()
        mock_get.assert_called_with(
            'https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/56/0/0/10/50&apiKey=33Q884-HFUV8K-SCS3LG-55CU'
        )