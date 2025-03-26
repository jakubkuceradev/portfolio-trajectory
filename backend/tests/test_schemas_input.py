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


# def valid_return_model_statistical(self):
#     # For a non-parametric cls type, only returns_source is required.
#     return ReturnModelInput(
#         modelType="statistical",  # This will be normalized to ModelType.STATISTICAL
#         returnsSource="global",  # Normalized to ReturnsSource.GLOBAL
#     )


# def valid_cash_flow_strategy():
#     # Using the default "zero" strategy which requires no additional fields.
#     return CashFlowInput(strategy="zero")


# ---------------------------
# Tests for SimulationConfig
# ---------------------------


# def test_valid_simulation_config_single_balance():
#     """Valid configuration when initial_balances is a single positive float."""
#     config_data = {
#         "numSteps": 100,  # valid: between 11 and 2000
#         "numPaths": 1000,  # valid: between 99 and 1,000,000
#         "initialBalances": 1500.0,  # single positive float
#         "percentiles": [1, 10, 25, 50, 75, 90, 99],
#         "returnModel": valid_return_model_statistical(),
#         "cashFlowStrategy": valid_cash_flow_strategy(),
#     }
#     config = SimulationConfig(**config_data)
#     assert config.num_steps == 100
#     assert config.num_paths == 1000
#     assert config.initial_balances == 1500.0
#     assert all(0 < p < 100 for p in config.percentiles)


# def test_valid_simulation_config_list_balance():
#     """Valid configuration when initial_balances is a list with length equal to num_paths."""
#     num_paths = 10
#     # Create a list of 10 positive balances.
#     balances = [1000.0 + i * 10 for i in range(num_paths)]
#     config_data = {
#         "numSteps": 200,
#         "numPaths": num_paths,
#         "initialBalances": balances,
#         "percentiles": [10, 20, 30, 40, 50],
#         "returnModel": valid_return_model_statistical(),
#         "cashFlowStrategy": valid_cash_flow_strategy(),
#     }
#     config = SimulationConfig(**config_data)
#     assert isinstance(config.initial_balances, list)
#     assert len(config.initial_balances) == num_paths


# def test_invalid_initial_balances_list_length():
#     """An error should be raised if initial_balances list length doesn't equal num_paths."""
#     config_data = {
#         "numSteps": 150,
#         "numPaths": 5,  # expecting 5 balances
#         "initialBalances": [1000.0, 1100.0, 1200.0],  # only 3 provided
#         "percentiles": [5, 25, 50, 75, 95],
#         "returnModel": valid_return_model_statistical(),
#         "cashFlowStrategy": valid_cash_flow_strategy(),
#     }
#     with pytest.raises(
#         ValidationError, match=r"initialBalances must have the same length as numPaths"
#     ):
#         SimulationConfig(**config_data)


# def test_invalid_initial_balance_value():
#     """An error should be raised if any balance in the list is non-positive."""
#     num_paths = 3
#     balances = [1000.0, -500.0, 1200.0]  # one balance is negative
#     config_data = {
#         "numSteps": 120,
#         "numPaths": num_paths,
#         "initialBalances": balances,
#         "percentiles": [10, 50, 90],
#         "returnModel": valid_return_model_statistical(),
#         "cashFlowStrategy": valid_cash_flow_strategy(),
#     }
#     with pytest.raises(
#         ValidationError, match=r"allInitialBalances must be greater than 0"
#     ):
#         SimulationConfig(**config_data)


# def test_invalid_percentiles():
#     """An error should be raised if any percentile is not between 0 and 100 (exclusive)."""
#     config_data = {
#         "numSteps": 130,
#         "numPaths": 500,
#         "initialBalances": 2000.0,
#         "percentiles": [0, 50, 100],  # 0 and 100 are invalid
#         "returnModel": valid_return_model_statistical(),
#         "cashFlowStrategy": valid_cash_flow_strategy(),
#     }
#     with pytest.raises(
#         ValidationError,
#         match=r"eachPercentile must be greater than 0 and less than 100",
#     ):
#         SimulationConfig(**config_data)


# def test_invalid_num_steps():
#     """An error should be raised if num_steps is out of the allowed range."""
#     config_data = {
#         "numSteps": 10,  # too low; must be greater than 11
#         "numPaths": 500,
#         "initialBalances": 2000.0,
#         "percentiles": [5, 50, 95],
#         "returnModel": valid_return_model_statistical(),
#         "cashFlowStrategy": valid_cash_flow_strategy(),
#     }
#     with pytest.raises(ValidationError, match=r"ensure this value is greater than 11"):
#         SimulationConfig(**config_data)


# def test_invalid_num_paths():
#     """An error should be raised if num_paths is out of the allowed range."""
#     config_data = {
#         "numSteps": 100,
#         "numPaths": 50,  # too low; must be greater than 99
#         "initialBalances": 2000.0,
#         "percentiles": [5, 50, 95],
#         "returnModel": valid_return_model_statistical(),
#         "cashFlowStrategy": valid_cash_flow_strategy(),
#     }
#     with pytest.raises(ValidationError, match=r"ensure this value is greater than 99"):
#         SimulationConfig(**config_data)
