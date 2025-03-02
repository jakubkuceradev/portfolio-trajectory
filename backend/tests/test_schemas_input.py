"""Modules importing testing tools and tested classes."""

import pytest
from pydantic import ValidationError
from portfolio_trajectory.schemas.input import CashFlowInput
from portfolio_trajectory.schemas.input import (
    ReturnModelInput,
    ModelType,
    ReturnsSource,
)


# CashFlowInput
def test_valid_zero_strategy():
    """Test valid input for 'zero' strategy (no extra fields required)."""
    data = {"strategy": "zero"}
    model = CashFlowInput(**data)
    assert model.strategy == "zero"
    assert model.contribution is None
    assert model.withdrawal is None


def test_valid_fixed_strategy():
    """Test valid input for 'fixed' strategy with required 'contribution'."""
    data = {"strategy": "fixed", "contribution": 500.0}
    model = CashFlowInput(**data)
    assert model.strategy == "fixed"
    assert model.contribution == 500.0
    assert model.withdrawal is None


def test_valid_fixed_lifecycle_strategy():
    """Test valid input for 'fixed_lifecycle' strategy with required fields."""
    data = {"strategy": "fixed_lifecycle", "contribution": 500.0, "withdrawal": 300.0}
    with pytest.raises(ValidationError, match=r"monthsToRetirement"):
        CashFlowInput(**data)


def test_invalid_fixed_strategy_missing_contribution():
    """Test 'fixed' strategy should raise error if 'contribution' is missing."""
    data = {"strategy": "fixed"}
    with pytest.raises(ValidationError, match=r"contribution"):
        CashFlowInput(**data)


def test_invalid_fixed_lifecycle_missing_fields():
    """Test 'fixed_lifecycle' strategy should raise error if required fields are missing."""
    data = {"strategy": "fixed_lifecycle", "contribution": 500.0}
    with pytest.raises(ValidationError, match=r"withdrawal"):
        CashFlowInput(**data)


def test_invalid_strategy_value():
    """Test invalid strategy value should raise error."""
    data = {"strategy": "invalid_strategy"}
    with pytest.raises(ValidationError, match=r"Input"):
        CashFlowInput(**data)


def test_strategy_case_conversion():
    """Test that camelCase and snake_case strategies are properly converted."""
    data = {
        "strategy": "fixedLifecycle",
        "contribution": 500.0,
        "withdrawal": 300.0,
        "monthsToRetirement": 36,
    }
    model = CashFlowInput(**data)
    assert model.strategy == "fixed_lifecycle"

    data_snake = {
        "strategy": "fixed_lifecycle",
        "contribution": 500.0,
        "withdrawal": 300.0,
        "months_to_retirement": 36,
    }
    model_snake = CashFlowInput(**data_snake)
    assert model_snake.strategy == "fixed_lifecycle"


# ReturnModelInput


class TestReturnModelInput:
    """Test the ReturnModelInput class."""

    def test_valid_parametric_model(self):
        """Test that a parametric model input is valid when all required fields are provided."""
        data = {
            "modelType": "parametric",
            "nominalExpectedReturn": 0.07,
            "nominalStandardDeviation": 0.15,
            "realExpectedReturn": 0.05,
            "realStandardDeviation": 0.1,
            "returnsSource": "usa",
            "startDate": "2010-01-01",
            "endDate": "2023-12-31",
            "blockSize": 2,
            "circular": False,
        }
        model = ReturnModelInput(**data)
        assert model.model_type == ModelType.PARAMETRIC
        assert model.returns_source == ReturnsSource.USA
        assert model.nominal_expected_return == 0.07
        assert model.block_size == 2

    def test_invalid_parametric_missing_required_field(self):
        """Test that a parametric model input raises an error when required fields are missing."""
        data = {
            "modelType": "parametric",
            # "nominalExpectedReturn" is missing
            "nominalStandardDeviation": 0.15,
            "realExpectedReturn": 0.05,
            "realStandardDeviation": 0.1,
            "returnsSource": "usa",
        }
        with pytest.raises(ValidationError, match=r"nominalExpectedReturn"):
            ReturnModelInput(**data)

    def test_valid_statistical_model(self):
        """Test that a statistical model input is valid when the required returnsSource is provided."""
        data = {
            "modelType": "statistical",
            "returnsSource": "global",
            "blockSize": 1,
            "circular": True,
        }
        model = ReturnModelInput(**data)
        assert model.model_type == ModelType.STATISTICAL
        assert model.returns_source == ReturnsSource.GLOBAL

    def test_valid_bootstrap_model(self):
        """Test that a bootstrap model input is valid when the required returnsSource is provided."""
        data = {
            "modelType": "bootstrap",
            "returnsSource": "global",
        }
        model = ReturnModelInput(**data)
        assert model.model_type == ModelType.BOOTSTRAP
        assert model.returns_source == ReturnsSource.GLOBAL

    def test_normalization_of_strings(self):
        """Test that modelType and returnsSource are normalized to snake_case."""
        data = {
            "modelType": "Parametric",  # mixed-case input
            "nominalExpectedReturn": 0.07,
            "nominalStandardDeviation": 0.15,
            "realExpectedReturn": 0.05,
            "realStandardDeviation": 0.1,
            "returnsSource": "USA",  # upper-case input
        }
        model = ReturnModelInput(**data)
        # The normalization should convert these to lowercase snake_case values.
        assert model.model_type == ModelType.PARAMETRIC
        assert model.returns_source == ReturnsSource.USA

    def test_missing_returns_source_for_statistical(self):
        """Test that returnsSource is required for statistical and bootstrap models (handled by pydantic)."""
        data = {
            "modelType": "statistical",
            # Missing returnsSource; pydantic should raise a field-required error.
        }
        with pytest.raises(ValidationError, match=r"returnsSource"):
            ReturnModelInput(**data)

    def test_ticker_returns_source_for_bootstrap(self):
        """Test that returnsSource can be any string."""
        data = {
            "modelType": "bootstrap",
            "returnsSource": "VFINX",
        }

        model = ReturnModelInput(**data)
        assert model.model_type == ModelType.BOOTSTRAP
        assert model.returns_source == "vfinx"
