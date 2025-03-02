"""Import CamelModel for case conversion."""

from portfolio_trajectory.schemas.base import CamelModel


class ValueArray(CamelModel):
    """Represents arrays of nominal and real values."""

    nominal: list[float]
    real: list[float]


class SingleValue(CamelModel):
    """Represents a pair of nominal and real single values."""

    nominal: float
    real: float


class PathData(CamelModel):
    """Represents a path entry with an identifier and associated values."""

    id: int
    values: ValueArray


class Paths(CamelModel):
    """Holds collections of balance and return path data."""

    balances: list[PathData]
    returns: list[PathData]


class PercentilePath(CamelModel):
    """Represents percentile-based path data with corresponding values."""

    percentile: int
    values: ValueArray


class MetricData(CamelModel):
    """Represents a computed metric for a specific path, including its percentile and value."""

    percentile: int
    value: SingleValue
    example_path_id: int


class Parameters(CamelModel):
    """Holds simulation parameters such as the number of steps and paths."""

    num_steps: int
    num_paths: int


class Metrics(CamelModel):
    """Contains various metric collections computed from the paths."""

    percentile_balances: list[PercentilePath]
    end_balance: list[MetricData]
    mean_return: list[MetricData]
    volatility: list[MetricData]
    max_drawdown: list[MetricData]
    contributions: list[MetricData]
    withdrawals: list[MetricData]


class Data(CamelModel):
    """Represents the complete dataset including parameters, paths, and metrics."""

    parameters: Parameters
    paths: Paths
    metrics: Metrics
