"""Import testing tools and tested classes."""

import pytest
from pydantic import ValidationError
from portfolio_trajectory.schemas.output import (
    ValueArray,
    SingleValue,
    PathData,
    Paths,
    PercentilePath,
    MetricData,
    Parameters,
    Metrics,
    Data,
)


# Test ValueArray
def test_value_array_valid():
    """Test ValueArray with valid float lists."""
    data = {"nominal": [1.0, 2.0], "real": [1.5, 2.5]}
    va = ValueArray(**data)
    assert va.nominal == [1.0, 2.0]
    assert va.real == [1.5, 2.5]


def test_value_array_invalid_type():
    """Test ValueArray with invalid type in nominal list."""
    data = {"nominal": ["string"], "real": [1.0]}
    with pytest.raises(ValidationError) as exc_info:
        ValueArray(**data)
    assert "nominal" in str(exc_info.value)


# Test SingleValue
def test_single_value_valid():
    """Test SingleValue with valid float values."""
    data = {"nominal": 10.0, "real": 12.0}
    sv = SingleValue(**data)
    assert sv.nominal == 10.0
    assert sv.real == 12.0


def test_single_value_missing_field():
    """Test SingleValue with missing required field."""
    data = {"nominal": 5.0}  # Missing 'real'
    with pytest.raises(ValidationError) as exc_info:
        SingleValue(**data)
    assert "real" in str(exc_info.value)


# Test PathData
def test_path_data_valid():
    """Test PathData with valid id and values."""
    data = {"id": 1, "values": {"nominal": [1.0, 2.0], "real": [1.5, 2.5]}}
    pd = PathData(**data)
    assert pd.id == 1
    assert isinstance(pd.values, ValueArray)
    assert pd.values.nominal == [1.0, 2.0]


def test_path_data_invalid_values():
    """Test PathData with invalid values type."""
    data = {"id": 1, "values": {"nominal": ["bad"], "real": [1.0]}}
    with pytest.raises(ValidationError) as exc_info:
        PathData(**data)
    assert "values" in str(exc_info.value)


# Test Paths
def test_paths_valid():
    """Test Paths with valid balance and return data."""
    data = {
        "balances": [{"id": 1, "values": {"nominal": [1.0], "real": [1.1]}}],
        "returns": [{"id": 2, "values": {"nominal": [0.5], "real": [0.6]}}],
    }
    paths = Paths(**data)
    assert len(paths.balances) == 1
    assert paths.balances[0].id == 1
    assert len(paths.returns) == 1
    assert paths.returns[0].id == 2


def test_paths_empty_lists():
    """Test Paths with empty balances and returns lists."""
    data = {"balances": [], "returns": []}
    paths = Paths(**data)
    assert paths.balances == []
    assert paths.returns == []


def test_paths_invalid_balances():
    """Test Paths with invalid balances type."""
    data = {
        "balances": "not_a_list",  # Should be a list of PathData
        "returns": [{"id": 2, "values": {"nominal": [0.5], "real": [0.6]}}],
    }
    with pytest.raises(ValidationError) as exc_info:
        Paths(**data)
    assert "balances" in str(exc_info.value)


# Test PercentilePath
def test_percentile_path_valid():
    """Test PercentilePath with valid percentile and values."""
    data = {"percentile": 50, "values": {"nominal": [100.0], "real": [105.0]}}
    pp = PercentilePath(**data)
    assert pp.percentile == 50
    assert pp.values.nominal == [100.0]


def test_percentile_path_invalid_percentile():
    """Test PercentilePath with invalid percentile type."""
    data = {
        "percentile": "not_an_int",  # Should be an int
        "values": {"nominal": [100.0], "real": [105.0]},
    }
    with pytest.raises(ValidationError) as exc_info:
        PercentilePath(**data)
    assert "percentile" in str(exc_info.value)


# Test MetricData
def test_metric_data_valid():
    """Test MetricData with valid percentile, value, and path id."""
    data = {
        "percentile": 75,
        "value": {"nominal": 200.0, "real": 210.0},
        "examplePathId": 3,  # camelCase due to CamelModel
    }
    md = MetricData(**data)
    assert md.percentile == 75
    assert md.value.nominal == 200.0
    assert md.example_path_id == 3


def test_metric_data_invalid_value():
    """Test MetricData with invalid value type."""
    data = {
        "percentile": 75,
        "value": {"nominal": "bad", "real": 210.0},
        "examplePathId": 3,
    }
    with pytest.raises(ValidationError) as exc_info:
        MetricData(**data)
    assert "value" in str(exc_info.value)


# Test Parameters
def test_parameters_valid():
    """Test Parameters with valid step and path counts."""
    data = {"numSteps": 100, "numPaths": 50, "initialBalances": [14.0, 12.0]}  # camelCase due to CamelModel
    params = Parameters(**data)
    assert params.num_steps == 100
    assert params.num_paths == 50


# Test Metrics
def test_metrics_valid():
    """Test Metrics with valid percentile balances and end balance."""
    data = {
        "percentileBalances": [
            {"percentile": 50, "values": {"nominal": [1.0], "real": [1.1]}}
        ],
        "endBalance": [
            {
                "percentile": 90,
                "value": {"nominal": 10.0, "real": 11.0},
                "examplePathId": 1,
            }
        ],
        "meanReturn": [],
        "volatility": [],
        "maxDrawdown": [],
        "contributions": [],
        "withdrawals": [],
    }
    metrics = Metrics(**data)
    assert len(metrics.percentile_balances) == 1
    assert metrics.percentile_balances[0].percentile == 50
    assert len(metrics.end_balance) == 1
    assert metrics.end_balance[0].percentile == 90


# Test Data (Top-Level)
def test_data_valid():
    """Test Data with valid parameters, paths, and metrics."""
    data = {
        "parameters": {"numSteps": 10, "numPaths": 5, "initialBalances": [17.0, 0]},
        "paths": {
            "balances": [{"id": 1, "values": {"nominal": [1.0], "real": [1.1]}}],
            "returns": [],
        },
        "metrics": {
            "percentileBalances": [
                {"percentile": 50, "values": {"nominal": [2.0], "real": [2.2]}}
            ],
            "endBalance": [],
            "meanReturn": [],
            "volatility": [],
            "maxDrawdown": [],
            "contributions": [],
            "withdrawals": [],
        },
    }
    full_data = Data(**data)
    assert full_data.parameters.num_steps == 10
    assert len(full_data.paths.balances) == 1
    assert full_data.metrics.percentile_balances[0].percentile == 50


def test_data_missing_field():
    """Test Data with missing metrics field."""
    data = {
        "parameters": {"numSteps": 10, "numPaths": 5},
        "paths": {"balances": [], "returns": []},
    }
    with pytest.raises(ValidationError) as exc_info:
        Data(**data)
    assert "metrics" in str(exc_info.value)


# Test Serialization
def test_data_serialization():
    """Test Data serialization to dictionary."""
    data_instance = Data(
        parameters=Parameters(num_steps=10, num_paths=5, initial_balances=[11.0, 10.5, 0]),
        paths=Paths(
            balances=[PathData(id=1, values=ValueArray(nominal=[1.0], real=[1.1]))],
            returns=[],
        ),
        metrics=Metrics(
            percentile_balances=[
                PercentilePath(
                    percentile=50, values=ValueArray(nominal=[2.0], real=[2.2])
                )
            ],
            end_balance=[],
            mean_return=[],
            volatility=[],
            max_drawdown=[],
            contributions=[],
            withdrawals=[],
        ),
    )
    json_data = data_instance.model_dump(by_alias=True)  # Use aliases for camelCase
    assert json_data["parameters"]["numSteps"] == 10
    assert json_data["paths"]["balances"][0]["id"] == 1
    assert json_data["metrics"]["percentileBalances"][0]["percentile"] == 50
