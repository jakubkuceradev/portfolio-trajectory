"""Modules providing validation and typing."""

from enum import Enum
from datetime import datetime
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

    strategy: Strategy = Field(default=Strategy.ZERO)
    contribution: float | None = Field(None)
    withdrawal: float | None = Field(None)
    months_to_retirement: int | None = Field(None)

    @field_validator("strategy", mode="before")
    @classmethod
    def normalize_strings(cls, value: str) -> str:
        """Normalize and validate string fields."""
        if isinstance(value, str):
            return to_snake(value)
        return value

    @model_validator(mode="after")
    def validate_required_fields(self):
        """Ensure required fields are provided based on the selected strategy."""
        required_fields = {
            Strategy.FIXED: ["contribution"],
            Strategy.FIXED_LIFECYCLE: [
                "contribution",
                "withdrawal",
                "months_to_retirement",
            ],
        }

        missing_fields = [
            field
            for field in required_fields.get(self.strategy, [])
            if getattr(self, field) is None
        ]

        if missing_fields:
            raise ValueError(
                f"{', '.join(map(to_camel, missing_fields))} is required for {to_camel(self.strategy)} model"
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
    start_date: datetime | None = Field(None)
    end_date: datetime | None = Field(None)
    block_size: int = Field(1, gt=0)
    circular: bool = Field(True)

    @field_validator("model_type", "returns_source", mode="before")
    @classmethod
    def normalize_strings(cls, value: str) -> str:
        """Convert certain string fields to snake_case before validation."""
        if isinstance(value, str):
            return to_snake(value)
        return value

    @model_validator(mode="after")
    def validate_required_fields(self):
        """Ensure required fields are provided based on model_type."""
        required_fields = {
            ModelType.PARAMETRIC: [
                "nominal_expected_return",
                "nominal_standard_deviation",
                "real_expected_return",
                "real_standard_deviation",
            ],
            ModelType.BOOTSTRAP: ["returns_source"],
            ModelType.STATISTICAL: ["returns_source"],
        }

        missing_fields = [
            field
            for field in required_fields.get(self.model_type, [])
            if getattr(self, field) is None
        ]

        if missing_fields:
            raise ValueError(
                f"{', '.join(map(to_camel, missing_fields))} is required for {to_camel(self.model_type)} model"
            )

        return self
