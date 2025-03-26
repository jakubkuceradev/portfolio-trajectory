"""Import CamelModel for case conversion."""

from portfolio_trajectory.schemas.base import CamelModel


class ValueArray(CamelModel):
    """Represents arrays of nominal and real values.

    Attributes
    ----------
    nominal : list[float]
        Array of nominal values in the simulation.
    real : list[float]
        Array of real (inflation-adjusted) values in the simulation.
    """

    nominal: list[float]
    real: list[float]


class SingleValue(CamelModel):
    """Represents a pair of nominal and real single values.

    Attributes
    ----------
    nominal : float
        Nominal value of the metric.
    real : float
        Real (inflation-adjusted) value of the metric.
    """

    nominal: float
    real: float


class PathData(CamelModel):
    """Represents a path entry with an identifier and associated values.

    Attributes
    ----------
    id : int
        Unique identifier for the path.
    values : ValueArray
        Nominal and real values associated with the path.
    """

    id: int
    values: ValueArray


class Paths(CamelModel):
    """Holds collections of balance and return path data.

    Attributes
    ----------
    balances : list[PathData]
        list of balance path data entries.
    returns : list[PathData]
        list of return path data entries.
    """

    balances: list[PathData]
    returns: list[PathData]


class PercentilePath(CamelModel):
    """Represents percentile-based path data with corresponding values.

    Attributes
    ----------
    percentile : int
        Percentile rank (e.g., 50 for median).
    values : ValueArray
        Nominal and real values at this percentile.
    """

    percentile: int
    values: ValueArray


class MetricData(CamelModel):
    """Represents a computed metric for a specific path, including its percentile and value.

    Attributes
    ----------
    percentile : int
        Percentile rank of the metric (e.g., 90 for 90th percentile).
    value : SingleValue
        Nominal and real values of the metric.
    example_path_id : int
        Identifier of an example path for this metric.

    Notes
    -----
    Inherits from CamelModel, enabling camelCase JSON input/output (e.g., 'examplePathId' for 'example_path_id').
    """

    percentile: int
    value: SingleValue
    example_path_id: int


class Parameters(CamelModel):
    """Holds simulation parameters such as the number of steps and paths.

    Attributes
    ----------
    num_steps : int
        Number of time steps in the simulation.
    num_paths : int
        Number of simulated paths.

    Notes
    -----
    Inherits from CamelModel, enabling camelCase JSON input/output (e.g., 'numSteps' for 'num_steps').
    """

    num_steps: int
    num_paths: int
    initial_balances: list[float]


class Metrics(CamelModel):
    """Contains various metric collections computed from the paths.

    Attributes
    ----------
    percentile_balances : list[PercentilePath]
        Percentile-based balance paths.
    end_balance : list[MetricData]
        End balance metrics across percentiles.
    mean_return : list[MetricData]
        Mean return metrics across percentiles.
    volatility : list[MetricData]
        Volatility metrics across percentiles.
    max_drawdown : list[MetricData]
        Maximum drawdown metrics across percentiles.
    contributions : list[MetricData]
        Contribution metrics across percentiles.
    withdrawals : list[MetricData]
        Withdrawal metrics across percentiles.

    Notes
    -----
    Inherits from CamelModel, enabling camelCase JSON input/output (e.g., 'endBalance' for 'end_balance').
    """

    percentile_balances: list[PercentilePath]
    end_balance: list[MetricData]
    mean_return: list[MetricData]
    volatility: list[MetricData]
    max_drawdown: list[MetricData]
    contributions: list[MetricData]
    withdrawals: list[MetricData]


class Data(CamelModel):
    """Represents the complete dataset including parameters, paths, and metrics.

    Attributes
    ----------
    parameters : Parameters
        Simulation parameters.
    paths : Paths
        Balance and return path data.
    metrics : Metrics
        Computed metrics from the paths.
    """

    parameters: Parameters
    paths: Paths
    metrics: Metrics
