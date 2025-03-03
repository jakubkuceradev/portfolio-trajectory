"""Import testing tools and tested classes."""

import pytest
from pydantic import ValidationError
from portfolio_trajectory.schemas.input import (
    Strategy,
    CashFlowInput,
    ModelType,
    ReturnsSource,
    ReturnModelInput,
)


class TestCashFlowInput:
    """Test the CashFlowInput class."""

    def test_valid_zero_strategy(self):
        """Test valid input for 'zero' strategy."""
        data = {"strategy": "zero"}
        cls = CashFlowInput(**data)
        assert cls.strategy == Strategy.ZERO
        assert cls.strategy == "zero"
        assert cls.contribution is None
        assert cls.withdrawal is None

    def test_invalid_zero_strategy_unused_field(self):
        """Test unused field for 'zero' strategy."""
        data = {"strategy": "zero", "contribution": 500.0}  # 'contribution' is unused
        with pytest.raises(ValidationError, match=r"contribution"):
            CashFlowInput(**data)

    def test_valid_fixed_strategy(self):
        """Test valid input for 'fixed' strategy."""
        data = {"strategy": "fixed", "contribution": "500.0"}
        cls = CashFlowInput(**data)
        assert cls.strategy == Strategy.FIXED
        assert cls.strategy == "fixed"
        assert cls.contribution == 500.0
        assert cls.withdrawal is None

    def test_invalid_fixed_strategy_missing_field(self):
        """Test missing required field for 'fixed' strategy."""
        data = {
            "strategy": "fixed",
            # 'contribution' is missing
        }
        with pytest.raises(ValidationError, match=r"contribution"):
            CashFlowInput(**data)

    def test_invalid_fixed_unused_field(self):
        """Test unused field for 'fixed' strategy."""
        data = {
            "strategy": "fixed",
            "contribution": "500",
            "withdrawal": "400",  # 'withdrawal' is unused
        }
        with pytest.raises(ValidationError, match=r"withdrawal"):
            CashFlowInput(**data)

    def test_valid_fixed_lifecycle_strategy(self):
        """Test valid input for 'fixed_lifecycle' strategy."""
        data = {
            "strategy": "fixedLifecycle",
            "contribution": "500",
            "withdrawal": -400,
            "monthsToRetirement": 32,
        }
        cls = CashFlowInput(**data)
        assert cls.strategy == Strategy.FIXED_LIFECYCLE
        assert cls.strategy == "fixed_lifecycle"
        assert cls.contribution == 500.0
        assert cls.withdrawal == -400.0
        assert cls.months_to_retirement == 32

    def test_invalid_fixed_lifecycle_strategy(self):
        """Test missing required field for 'fixed_lifecycle' strategy."""
        data = {
            "strategy": "fixed_lifecycle",
            "contribution": 500.0,
            "withdrawal": 300.0,
            # 'monthsToRetirement' is missing
        }
        with pytest.raises(ValidationError, match=r"monthsToRetirement"):
            CashFlowInput(**data)

    def test_invalid_fixed_lifecycle_invalid_field(self):
        """Test invalid field for 'fixed_lifecycle' strategy."""
        data = {
            "strategy": "fixedLifecycle",
            "contribution": 500.0,
            "withdrawal": 300.0,
            "monthsToRetirement": -1,
        }
        with pytest.raises(ValidationError, match=r"monthsToRetirement"):
            CashFlowInput(**data)

    def test_invalid_fixed_lifecycle_missing_fields(self):
        """Test missing required field for 'fixed_lifecycle' strategy."""
        data = {"strategy": "fixed_lifecycle", "contribution": 500.0}
        with pytest.raises(ValidationError, match=r"withdrawal"):
            CashFlowInput(**data)

    def test_invalid_strategy_value(self):
        """Test invalid required field 'strategy'."""
        data = {"strategy": "invalid_strategy"}
        with pytest.raises(ValidationError, match=r"strategy"):
            CashFlowInput(**data)

    def test_strategy_case_conversion(self):
        """Test that camelCase and snake_case strategies are properly converted."""
        data = {
            "strategy": "fixedLifecycle",
            "contribution": 500.0,
            "withdrawal": 300.0,
            "monthsToRetirement": 36,
        }
        cls = CashFlowInput(**data)
        assert cls.strategy == Strategy.FIXED_LIFECYCLE
        assert cls.strategy == "fixed_lifecycle"

        data_snake = {
            "strategy": "fixed_lifecycle",
            "contribution": 500.0,
            "withdrawal": 300.0,
            "months_to_retirement": 36,
        }
        cls_snake = CashFlowInput(**data_snake)
        assert cls_snake.strategy == Strategy.FIXED_LIFECYCLE
        assert cls_snake.strategy == "fixed_lifecycle"


class TestReturnModelInput:
    """Test the ReturnModelInput class."""

    def test_valid_parametric_model(self):
        """Test valid input for 'parametric' model."""
        data = {
            "modelType": "parametric",
            "nominalExpectedReturn": 0.07,
            "nominalStandardDeviation": 0.15,
            "realExpectedReturn": 0.05,
            "realStandardDeviation": 0.1,
        }
        cls = ReturnModelInput(**data)
        assert cls.model_type == ModelType.PARAMETRIC
        assert cls.model_type == "parametric"
        assert cls.nominal_expected_return == 0.07
        assert cls.real_standard_deviation == 0.1

    def test_invalid_parametric_missing_field(self):
        """Test missing field for 'parametric' model."""
        data = {
            "modelType": "parametric",
            # "nominalExpectedReturn" is missing
            "nominalStandardDeviation": 0.15,
            "realExpectedReturn": 0.05,
            "realStandardDeviation": 0.1,
        }
        with pytest.raises(ValidationError, match=r"nominalExpectedReturn"):
            ReturnModelInput(**data)

    def test_invalid_parametric_unused_field(self):
        """Test unused field for 'parametric' model."""
        data = {
            "modelType": "parametric",
            "nominalExpectedReturn": 0.07,
            "nominalStandardDeviation": "0.15",
            "realExpectedReturn": 0.05,
            "realStandardDeviation": "0.1",
            "blockSize": 1,  # 'block_size' is unused
        }
        with pytest.raises(ValidationError, match=r"blockSize"):
            ReturnModelInput(**data)

    def test_valid_statistical_model(self):
        """Test valid input for 'statistical' model."""
        data = {
            "modelType": "statistical",
            "returnsSource": "USA",
            "startDate": "2004-09-01",
        }
        cls = ReturnModelInput(**data)
        assert cls.model_type == ModelType.STATISTICAL
        assert cls.model_type == "statistical"
        assert cls.returns_source == ReturnsSource.USA
        assert cls.returns_source == "usa"
        assert cls.start_date is not None

    def test_invalid_statistical_invalid_date_field(self):
        """Test invalid 'endDate' field for 'statistical' model."""
        data = {
            "modelType": "statistical",
            "returnsSource": "global",
            "startDate": "2004-02-01",
            "endDate": "2007",
        }
        with pytest.raises(ValidationError, match=r"endDate"):
            ReturnModelInput(**data)

    def test_invalid_statistical_missing_field(self):
        """Test missing field for 'statistical' model."""
        data = {
            "modelType": "statistical",
            # 'returnsSource' is missing
            "startDate": "2004-09-08",
            "endDate": "2007-01-01",
        }
        with pytest.raises(ValidationError, match=r"returnsSource"):
            ReturnModelInput(**data)

    def test_invalid_statistical_unused_field(self):
        """Test unused field for 'statistical' model."""
        data = {
            "modelType": "statistical",
            "returnsSource": "global",
            "startDate": "1999-12-26",
            "circular": False,
        }
        with pytest.raises(ValidationError, match=r"circular"):
            ReturnModelInput(**data)

    def test_valid_bootstrap_model(self):
        """Test valid input for 'bootstrap' model."""
        data = {
            "modelType": "bootstrap",
            "returnsSource": "global",
            "circular": "false",
        }
        cls = ReturnModelInput(**data)
        assert cls.model_type == ModelType.BOOTSTRAP
        assert cls.model_type == "bootstrap"
        assert cls.returns_source == ReturnsSource.GLOBAL
        assert cls.returns_source == "global"
        assert cls.block_size == 1
        assert cls.circular is False

    def test_valid_ticker_bootstrap_model(self):
        """Test valid 'returnsSource' field for 'bootstrap' model."""
        data = {
            "modelType": "bootstrap",
            "returnsSource": "VFINX",
            "blockSize": "17.0",
        }

        cls = ReturnModelInput(**data)
        assert cls.model_type == ModelType.BOOTSTRAP
        assert cls.returns_source == "vfinx"
        assert cls.block_size == 17
        assert cls.circular is True

    def test_invalid_bootstrap_missing_field(self):
        """Test missing field for 'bootstrap' model."""
        data = {
            "modelType": "bootstrap",
            # 'returnsSource' is missing
            "startDate": "2012-12-12",
            "circular": True,
        }
        with pytest.raises(ValidationError, match=r"returnsSource"):
            ReturnModelInput(**data)

    def test_invalid_bootstrap_unused_field(self):
        """Test unused field for 'bootstrap' model."""
        data = {
            "modelType": "bootstrap",
            "returnsSource": "GLOBAL",
            "startDate": "2000-01-01",
            "realStandardDeviation": 0.17,  # 'realStandardDeviation' is unused
        }
        with pytest.raises(ValidationError, match=r"realStandardDeviation"):
            ReturnModelInput(**data)

    def test_invalid_bootstrap_invalid_dates(self):
        """Test invalid 'startDate' and 'endDate' fields."""
        data = {
            "modelType": "bootstrap",
            "returnsSource": "VFINX",
            "blockSize": "17.0",
            "startDate": "2004-09-01",  # 'startDate' is after 'endDate'
            "endDate": "2003-12-01",
        }
        with pytest.raises(ValidationError, match=r"startDate"):
            ReturnModelInput(**data)
