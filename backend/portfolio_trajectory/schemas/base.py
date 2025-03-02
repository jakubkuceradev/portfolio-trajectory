"""Module providing the BaseModel useful for validation"""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """BaseModel that automatically converts camelCase to snake_case and vice versa."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
