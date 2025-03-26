"""Modules providing validation and typing."""

from enum import Enum
from datetime import date
from pydantic import Field, field_validator, model_validator
from pydantic.alias_generators import to_camel, to_snake
from portfolio_trajectory.schemas.base import CamelModel


class Strategy(str, Enum):
    """Enum for allowed cash flow strategies."""

    ZERO = "zero"
    FIXED = "fixed"
    FIXED_LIFECYCLE = "fixed_lifecycle"


class CashFlowInput(CamelModel):
    """Input schema for cash flow strategy and parameters."""

    strategy: Strategy = Field()
    contribution: float | None = Field(None)
    withdrawal: float | None = Field(None)
    months_to_retirement: int | None = Field(None, ge=0)

    @field_validator("strategy", mode="before")
    @classmethod
    def normalize_strings(cls, value: str) -> str:
        """Normalize and validate string fields."""
        if isinstance(value, str):
            return to_snake(value)
        return value

    @model_validator(mode="after")
    def validate_fields(self):
        """Validate required and unused fields based on the selected strategy."""
        if self.strategy == Strategy.ZERO:
            required = []
            unused = ["contribution", "withdrawal", "months_to_retirement"]
        elif self.strategy == Strategy.FIXED:
            required = ["contribution"]
            unused = ["withdrawal", "months_to_retirement"]
        elif self.strategy == Strategy.FIXED_LIFECYCLE:
            required = ["contribution", "withdrawal", "months_to_retirement"]
            unused = []
        else:
            required = []
            unused = []

        # Check for missing required fields.
        missing_fields = [field for field in required if getattr(self, field) is None]
        if missing_fields:
            raise ValueError(
                f"{', '.join(map(to_camel, missing_fields))} "
                f"is required for {to_camel(self.strategy)} model"
            )

        # Check for extra (unused) fields that should be None.
        extra_fields = [field for field in unused if getattr(self, field) is not None]
        if extra_fields:
            raise ValueError(
                f"{', '.join(map(to_camel, extra_fields))} "
                f"must be None for {to_camel(self.strategy)} model"
            )

        return self


class ModelType(str, Enum):
    """Enum for allowed model types."""

    STATISTICAL = "statistical"
    PARAMETRIC = "parametric"
    BOOTSTRAP = "bootstrap"


class ReturnsSource(str, Enum):
    """Enum for allowed historical return sources."""

    GLOBAL = "global"
    USA = "usa"


class ReturnModelInput(CamelModel):
    """Nested input for model parameters."""

    model_type: ModelType = Field()
    nominal_expected_return: float | None = Field(None)
    nominal_standard_deviation: float | None = Field(None, ge=0)
    real_expected_return: float | None = Field(None)
    real_standard_deviation: float | None = Field(None, ge=0)
    returns_source: ReturnsSource | str | None = Field(None)
    start_date: date | None = Field(None)
    end_date: date | None = Field(None)
    block_size: int | None = Field(None, ge=1)
    circular: bool | None = Field(None)

    @field_validator("model_type", "returns_source", mode="before")
    @classmethod
    def normalize_strings(cls, value: str) -> str:
        """Convert certain string fields to snake_case before validation."""
        if isinstance(value, str):
            return to_snake(value)
        return value

    @model_validator(mode="after")
    def validate_fields(self):
        """Validate that required fields are provided and unused fields are None."""
        if self.model_type == ModelType.PARAMETRIC:
            required = [
                "nominal_expected_return",
                "nominal_standard_deviation",
                "real_expected_return",
                "real_standard_deviation",
            ]
            unused = [
                "returns_source",
                "start_date",
                "end_date",
                "block_size",
                "circular",
            ]
        elif self.model_type == ModelType.STATISTICAL:
            required = ["returns_source"]
            unused = [
                "nominal_expected_return",
                "nominal_standard_deviation",
                "real_expected_return",
                "real_standard_deviation",
                "block_size",
                "circular",
            ]
        elif self.model_type == ModelType.BOOTSTRAP:
            required = [
                "returns_source",
            ]
            unused = [
                "nominal_expected_return",
                "nominal_standard_deviation",
                "real_expected_return",
                "real_standard_deviation",
            ]

            if self.block_size is None:
                self.block_size = 1
            if self.circular is None:
                self.circular = True

        missing_fields = [f for f in required if getattr(self, f) is None]
        if missing_fields:
            raise ValueError(
                f"{', '.join(map(to_camel, missing_fields))} "
                f"is required for {self.model_type} model"
            )

        extra_fields = [f for f in unused if getattr(self, f) is not None]
        if extra_fields:
            raise ValueError(
                f"{', '.join(map(to_camel, extra_fields))} "
                f"must be None for {self.model_type} model"
            )

        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("'startDate' cannot be after 'endDate'")

        return self


MIN_STEPS = 12
MAX_STEPS = 12 * 100
MIN_PATHS = 100
MAX_PATHS = 1000000


class SimulationConfig(CamelModel):
    """Top-level configuration for the simulation."""

    num_steps: int = Field(ge=MIN_STEPS, le=MAX_STEPS)
    num_paths: int = Field(ge=MIN_PATHS, le=MAX_PATHS)
    initial_balances: float | list[float]
    percentiles: list[int]
    return_model: ReturnModelInput
    cash_flow_strategy: CashFlowInput

    @field_validator("initial_balances")
    @classmethod
    def validate_initial_balances(
        cls, value: float | list[float]
    ) -> float | list[float]:
        """Ensure initialBalances are greater than or equal to 0."""
        if isinstance(value, list):
            if not all(v >= 0 for v in value):
                raise ValueError(
                    "all values in initialBalances must be greater than or equal to 0"
                )
        else:
            if value < 0:
                raise ValueError("initialBalances must be greater than or equal to 0")
        return value

    @field_validator("percentiles")
    @classmethod
    def validate_percentiles(cls, value: list[int]) -> list[int]:
        """Ensure percentiles are between 0 and 100, unique, and sorted."""
        if not all(0 < p < 100 for p in value):
            raise ValueError("each percentile must be greater than 0 and less than 100")
        if len(set(value)) != len(value):
            raise ValueError("percentiles must be unique")
        return sorted(value)

    @model_validator(mode="after")
    def validate_cross_fields(self):
        """Ensure initialBalances list length equals numPaths if a list."""
        if (
            isinstance(self.initial_balances, list)
            and len(self.initial_balances) != self.num_paths
        ):
            raise ValueError("initialBalances must have the same length as numPaths")
        return self
