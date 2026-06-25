# portfolio-trajectory Discovery Notes

This document preserves the full set of ideas, decisions, assumptions, push-backs, and open questions discussed during the initial project discovery conversation. It intentionally includes details that may not belong in the primary public documentation or MVP PRD.

## 1. Working Name

Working project name:

```text
portfolio-trajectory
```

The name reflects the project's focus on simulating long-horizon portfolio paths rather than producing a single deterministic forecast.

## 2. Project Purpose

The project is an open-source personal project to be hosted on the creator's website. It should be polished enough to serve as a public portfolio/CV piece.

The product should prioritize:

- Polish over feature breadth.
- Visual quality.
- Strong user interaction design.
- Correct but transparent methodology.
- Learning how to create interactive web application elements.
- A foundation for a later PRD.

The tool should help the creator understand:

- Feature boundaries.
- User interactions.
- Simulation assumptions.
- Edge cases.
- Architecture tradeoffs.
- Data model needs.

## 3. Intended Audience

Primary intended users:

- FIRE enthusiasts.
- Investment enthusiasts.
- Average people trying to estimate how much they need to deposit to reach financial goals.
- Users comparing long-term financial strategies.

Possible professional users:

- Financial advisors.
- Retirement planners.

These professional users could use the tool to demonstrate portfolio strategies and outcome uncertainty to customers.

Secondary audiences:

- Potential employers.
- Open-source contributors.
- Developers interested in simulation, React, TypeScript, Rust/WASM, or interactive visualization.

## 4. Correctness and Product Philosophy

Correctness is vital, but the domain is fundamentally limited because forward-looking investment planning is probabilistic and necessarily depends on assumptions about future markets.

Important framing:

- The tool should not imply certainty.
- Outcomes should be presented probabilistically.
- The UI should make uncertainty visually intuitive.
- Methodological assumptions should be inspectable.
- The project should focus on a few well-implemented features rather than many shallow ones.

The strongest positioning is not a full personal finance app, but a simulation and visualization tool for lifecycle investing.

## 5. Core Use Case

Primary question:

> Given my current age, wealth, expected savings, uncertain future life events, and a selected strategy, what are the expected outcomes for different percentiles?

Typical user interests:

- Mean outcome.
- Median outcome.
- Lower-bound outcome, especially 5th or 10th percentile.
- Whether the strategy succeeds in approximately 90–95% of historical-bootstrap situations.
- Maximizing spending.
- Maximizing expected terminal money.
- Avoiding ruin.
- Evaluating a personal financial strategy with industry-standard block bootstrap simulation.

Important note:

- Lower percentiles below the 5th may be less representative in bootstrap-based simulations, especially with finite historical data and limited unique block combinations.

## 6. MVP Product Direction

Suggested MVP identity:

> A local-first web app that simulates personal portfolio trajectories using monthly historical block bootstrap sampling, user-defined portfolio allocations, and probabilistic one-time cashflow events. It visualizes real and nominal outcomes through percentile bands, failure probabilities, and summary statistics.

Suggested MVP inclusions:

- Scenario setup.
- Historical monthly block bootstrap.
- Stocks/bonds/cash portfolio.
- Fixed allocation with rebalancing.
- Probabilistic one-time cashflow events.
- Percentile fan chart.
- Terminal wealth distribution.
- Probability of ruin.
- Exportable scenario and result summaries.

Suggested MVP exclusions:

- Accounts.
- Server caching.
- Taxes.
- Income modeling.
- LETFs.
- Conditional events.
- Event covariance.
- Complex strategies.
- Strategy scripting.

Reasoning:

The most impressive public version is likely to be a polished, interactive simulator rather than a broad but incomplete retirement planning application.

## 7. Timeline Model

The simulation uses monthly time steps.

Rationale:

- Block bootstrapping is usually preferred because it better captures autocorrelation in stock market returns than independent monthly sampling.
- Time units below one month are unreasonable for the primary model if the source data is monthly.
- Monthly units are practical for lifecycle investing.
- Typical bootstrap block size may be one to five years.
- Block starting points do not need to be aligned with calendar years.
- This allows sampled sequences to start at historically interesting months, such as near the top of the dot-com bubble.

Default timeline:

```text
month 0 -> month N
```

Possible later extension:

- Age-based timeline.
- Calendar-year labels.
- Current age.
- Current income.
- Fixed or glided deposit percentage.
- Probabilistic income and deposit calculation.
- Retirement age.
- Lifespan modeling.

Death/lifespan:

- Death can be fixed or modeled probabilistically depending on settings.
- Age and lifespan may not be part of the MVP.

Inflation:

- Inflation is captured alongside stock and bond performance.
- Inflation is included through bootstrap sampling.
- Each simulation run has its own sampled inflation path.

Values tracked:

- Nominal values.
- Real values.
- Inflation index per run.

## 8. Probabilistic Events

The main interactive widget is an interactive timeline/graph element that allows insertion of probabilistic events.

Common event examples:

- Buying a house.
- Large medical expenses typical near end of life.
- Philanthropic goals near end of life.
- Inheritance.
- Other large expenses.
- Other large windfalls.

Events should eventually allow the user to specify:

- Time interval.
- Money amount interval.
- Distribution type.
- Occurrence probability.
- Future covariance with other events.
- Future conditionals.

Initial event model:

- Mostly one-time events.
- Later configurable recurring events.
- Uncertainty may exist in date, amount, and occurrence.
- Events may fail to occur entirely.
- Supported MVP distributions: fixed, uniform, normal/Gaussian.

Goal events:

- Goal events are not part of the app initially.
- Users determine goals themselves by inspecting resulting statistics.
- If users want to model a goal, they can add deterministic spending to simulate it.

Potential event categories:

- Housing.
- Medical.
- Inheritance.
- Philanthropy.
- Education.
- Custom.

Open design choices:

- Whether event amounts are specified in today's dollars or future nominal dollars.
- Whether dates are month offsets, calendar dates, or ages.
- Whether normal distributions should be truncated.
- How normal distribution parameters are specified.
- How to represent uncertainty visually.
- Whether to provide generic events first or polished preset templates.

## 9. Dependency and Conditional Modeling

Dependency modeling is considered complicated and likely a very late-stage feature.

It should not be implemented from the beginning, but the architecture should avoid making it impossible.

Ideas discussed:

- Correlation matrices between individual user-specified events.
- Conditional retirement date shifting.
- Inheritance depending on parent death date.
- Medical expenses depending on lifespan.
- Home purchase depending on portfolio reaching a threshold.
- Philanthropic giving only if portfolio exceeds a threshold.
- Retirement date changing if portfolio underperforms.

Initial choice:

- Conditionals are future-only.
- MVP events can be independent.
- Data model should still separate event definitions from sampled event realizations.

## 10. Market Return Simulation

The main simulation uses a long timeline of US and global market stock returns for each month, with additional information for bonds and cash/HYSA.

Simulation method:

- Generate parallel simulation runs.
- Pick blocks of consecutive historical months at random.
- Typical block length: one to five years.
- Apply monthly asset returns.
- Apply inflation.
- Apply contributions, withdrawals, events, fees, and rebalancing.

Block bootstrap reasoning:

- Captures some autocorrelation and sequence structure.
- More realistic than independent random month sampling.
- Retains relationships between asset classes and inflation if sampled as linked monthly vectors.
- Gives diversity while keeping historically grounded paths.

Block size:

- Configurable.
- Block length of one month becomes ordinary bootstrap.
- Fixed block size first.
- Possible future support for randomly selected block sizes.
- Possible future stationary bootstrap.

Wrap-around:

- Should be available as a setting.
- With wrap-around enabled, a block can start near the end of the dataset and continue from the beginning.
- With wrap-around disabled, valid block starts must allow the full block to fit within the dataset.

## 11. Historical Data Sources

Desired public datasets:

- Fama-French research data.
- US market premium as proxy for US total stock market.
- Similar global stock data.
- Risk-free rate as proxy for HYSA or short-term T-bills.
- Inflation CPI from official sources.
- Bond data from public/open funds or datasets.

Historical coverage:

- Prefer going as far back as possible.
- Global stocks may limit practical coverage to around 1980.
- Reconstructed historical indexes are acceptable if correctly adjusted for fees.

Important data questions:

- Whether to use total return or excess return.
- Whether to reconstruct total market return as market excess return plus risk-free rate.
- Which cash proxy to use.
- Which bond return series to use.
- Whether global stocks are required for MVP.
- How to handle missing data when one series starts later than another.
- Whether to use only overlapping common periods.
- Whether to allow reduced comparability with warnings.
- How to expose data provenance in the UI.

## 12. Asset Model

Simplest initial portfolio model:

- Stocks.
- Bonds.
- Cash.

Possible later asset model:

- US stocks.
- Global stocks.
- International ex-US stocks.
- US bonds.
- Global bonds.
- Cash / risk-free rate.
- Leveraged ETFs.
- More complex products.

Fees:

- Fees are modeled per asset.
- Fees can be represented by adjusting returns of the indices.
- Better long-term design: treat fees as first-class return transforms so assumptions remain auditable.

## 13. Portfolio Allocation and Strategies

Initial strategy:

- Fixed allocation with periodic rebalancing.

Allocation behavior:

- Users should eventually define allocations as percentages over time.
- Fixed allocation may be sufficient for v1.
- Future-proofing should avoid large refactors later.

Taxes:

- Ignore taxes for now.

Contributions:

- Later stages should allow contributions to nudge toward the target distribution.
- Contribution nudging means directing new deposits toward underweight assets before selling existing holdings.

Potential strategy types:

- Fixed allocation.
- Periodic rebalancing.
- Threshold rebalancing.
- Glide path.
- Age-based stock/bond shift.
- Nudging.
- Lifecycle leverage.
- Dynamic retirement date shifting.
- Alternative allocation experiments.
- Adding stocks or complex products.

Potential strategy abstraction:

A strategy could be modeled as a function of:

- Time.
- Portfolio state.
- Scenario state.
- Potentially previous returns or drawdowns.

Future question:

- Should strategies react to market conditions or only to age/time?

## 14. LETF Modeling

Leveraged ETFs are an advanced feature and probably not present in the MVP.

Future LETF modeling idea:

- Create a synthetic ETF using daily market returns.
- Estimate cost of debt using a formula based on the risk-free rate.
- Use logistic regression and data from index documentation about debt rates.
- Include financing cost.
- Include expense ratios.
- Include volatility drag.

Important modeling caveat:

- Because the main simulation uses monthly data, LETF modeling from monthly returns would be approximate.
- More accurate LETF modeling likely requires daily data.

## 15. Simulation Engine

Expected run count:

- At least 10,000 runs.
- Probably more later.

Parallelism:

- Monte Carlo bootstrapping is embarrassingly parallel.
- Server-side implementation would allow strongly typed, parallel languages such as C++, Go, or Rust.
- However, hosting constraints may make server-side simulation difficult.

Server constraints:

- Available VMs may only have 4–8 GB RAM.
- Simulation can be memory-heavy.

Client-side considerations:

- A local-first app is cheaper, easier to host, and privacy-friendly.
- Web Workers can avoid blocking the UI.
- Rust/WASM may provide performance advantages and a strong CV story.
- TypeScript-only may be simpler and easier to audit.

Reproducibility:

- Not a major user-facing priority.
- Caching may be added later.
- Tests should still use deterministic seeds and golden scenarios.

Memory consideration:

- Avoid storing every full simulated path unless necessary.
- Compute summary statistics incrementally or store compressed outputs.
- Store selected sample paths only for visualization if needed.

Possible output architecture:

- Full per-run data for smaller runs.
- Percentile summaries per month for larger runs.
- Per-run terminal statistics.
- Optional sampled representative paths.

## 16. Client vs Server Architecture

Server-side advantages:

- Easier use of languages optimized for parallelism.
- Easier use of large data processing libraries.
- Potential for caching complete simulation runs.
- Potential shareable links to cached results.

Server-side disadvantages:

- RAM constraints.
- Hosting cost.
- More deployment complexity.
- Privacy implications.
- Potential backend bottleneck.

Client-side advantages:

- Easy static hosting.
- Privacy-friendly.
- No accounts needed.
- No server compute cost.
- Excellent fit for open-source demo.
- Scenarios can be exported locally.

Client-side disadvantages:

- Browser performance limits.
- Browser memory limits.
- Parallelism is more complex.
- Long simulations need careful UX.

Suggested direction:

- Start client-side.
- Use TypeScript/React UI.
- Run simulations in a Web Worker.
- Keep simulation engine independent enough to port to Rust/WASM later.

## 17. Frontend and Tech Stack Preferences

Preferred frontend:

- TypeScript.
- React.
- Probably not Next.js, though still uncertain.

Backend comfort:

- Python is comfortable but may not be ideal for calculation-heavy simulation due to the GIL and parallelization needs.
- NumPy does not solve all parallelization needs for this use case.

Possible backend or engine languages:

- Rust.
- Go.
- C++.
- TypeScript for MVP.

Database if server route is chosen:

- SQLite.
- Postgres.

Project organization:

- Monorepo seems reasonable.
- Open source.

Optimization priorities:

- Polish.
- Learning.
- Interactivity.
- Maintainability.
- Good architecture.

## 18. Suggested Technical Direction

A practical staged architecture:

1. Build a clean TypeScript simulation engine in a separate package.
2. Run it in a Web Worker from the React frontend.
3. Keep scenario schemas serializable and language-neutral.
4. Add benchmarks and golden tests.
5. If performance is insufficient, port the engine to Rust/WASM behind the same interface.

Potential packages:

```text
packages/core
packages/data
apps/web
```

Potential domain modules:

```text
simulation/
bootstrap/
portfolio/
events/
strategies/
statistics/
schema/
```

## 19. Visualization Direction

The main visualization should probably be the centerpiece of the app.

Suggested primary chart:

- Percentile trajectory fan.
- X-axis: month, year, or age.
- Y-axis: portfolio value.
- 5th–95th percentile band.
- 10th–90th percentile band.
- 25th–75th percentile band.
- Median line.
- Optional mean line, visually deemphasized.
- Ruin threshold at zero.
- Event markers along the timeline.

Hover/scrub behavior:

At a selected month, show:

- Median wealth.
- 10th percentile wealth.
- 5th percentile wealth.
- Probability of ruin by that month.
- Possibly inflation information.
- Relevant event probability windows.

Secondary chart:

- Terminal wealth distribution.
- Histogram or density chart.
- Helps users understand that percentile paths are not single simulated paths.

Risk-over-time chart:

- Cumulative probability of ruin.
- Probability of being below starting real wealth.
- Probability of being below user-defined threshold in the future.

Strategy comparison:

Avoid overlaying too many fan charts. Prefer:

- Strategy A chart.
- Strategy B chart.
- Difference chart.
- Median difference.
- 10th percentile difference.
- Probability-of-ruin difference.

Potential visualization libraries:

- Apache ECharts.
- D3 for custom visual grammar.
- Canvas for high-performance custom timeline overlays.
- SVG for precise interaction if data volume is modest.

## 20. Output Statistics

Statistics should usually be calculated for nominal and real values.

Mentioned or suggested statistics:

- Mean terminal wealth.
- Median terminal wealth.
- 5th percentile terminal wealth.
- 10th percentile terminal wealth.
- Standard deviation.
- Largest drop / max drawdown.
- Longest time before going even.
- Longest underwater period.
- Time to recovery.
- Probability of ruin.
- Success probability.
- Median bequest.
- Expected shortfall / CVaR.
- Worst 5% outcome.
- Retirement failure age.
- Probability of being below starting real wealth.
- Probability of being below a user-defined threshold.

Definitions needing clarification:

- Max drawdown from nominal or real wealth.
- Underwater period relative to high-water mark.
- Time to break even relative to starting wealth or previous peak.
- Whether success should be user-defined.
- Whether app should avoid defining success by default.

## 21. Product Shape

The app will be a web application.

Accounts:

- Avoid accounts for as long as possible.
- Accounts are not out of the question later.

Export:

- Scenarios should be exportable.
- Results should be exportable.
- Export format should likely include JSON for scenario state and CSV/JSON for result summaries.

Shareable links:

- Good future idea.
- Links could encode simulation settings.
- Alternatively, links could point to complete cached runs.
- Cached run links imply a server or persistent storage layer.

## 22. Documentation Preferences

The current documentation should serve as a foundation for a PRD.

Documentation should help understand:

- Features.
- Interactions.
- Edge cases.
- Architecture.
- Simulation assumptions.
- Tradeoffs.

User preference:

- Leave out a backlog for now.
- Do not include disclaimers.
- Docs should describe features as what they do.
- Some parts may talk about planning.

Potential document set:

- Primary documentation file.
- Comprehensive discussion notes.
- Later PRD.
- Later methodology document.
- Later architecture document.
- Later data source document.

## 23. Suggested README / CV Emphasis

Potential README emphasis areas:

- Interactive financial simulation.
- Historical block-bootstrap methodology.
- Percentile visualization.
- TypeScript/React product polish.
- Web Worker or Rust/WASM simulation architecture.
- Open-source engineering practices.
- Tests and benchmarks.

Potential CV value:

- Complex stateful UI.
- Data visualization.
- Simulation engine design.
- Statistical modeling.
- Performance optimization.
- Type-safe domain modeling.
- Browser-based computation.

## 24. Open Questions from the Conversation

### MVP Boundary

- Should v1 support one scenario only, or compare strategies immediately?
- Should the app feel like a calculator, visual simulator, planning notebook, or strategy laboratory?
- What is the smallest impressive demo suitable for the website?
- How much methodological completeness is needed before public release?

### Financial Model

- Can portfolio value go negative?
- Does ruin clamp the portfolio to zero?
- Can future contributions revive a ruined portfolio?
- Does ruin mean wealth below zero, inability to withdraw, or below a user-defined floor?
- Are contributions applied before or after market returns?
- Are events applied before or after market returns?
- When exactly does rebalancing occur?
- Is monthly rebalancing the default?
- Can users disable rebalancing?
- Are recurring contributions specified in real or nominal dollars?

### Bootstrap Methodology

- Is each path built by repeatedly sampling blocks until the horizon is filled?
- Are final blocks truncated?
- How exactly does wrap-around behave?
- Should block size be fixed, uniformly sampled from a range, or geometrically distributed later?
- Should all asset classes and inflation be sampled as linked vectors?
- Is independent asset-class sampling ever allowed?
- How should missing data be handled?
- Should the app use only overlapping common historical periods?

### Data

- What is the exact stock return unit?
- Should total returns be reconstructed from Fama-French excess returns plus risk-free rate?
- What is the cash proxy?
- What is the initial bond dataset?
- Is global stock required for MVP?
- Should dataset provenance appear in the UI?
- Should there be a dedicated data quality page?
- How are fees modeled and displayed?

### Event Model

- Are event dates month offsets, calendar dates, or age ranges?
- Does event type determine sign?
- How should normal distributions be parameterized?
- Should normal distributions be truncated?
- Are date samples rounded to nearest month?
- Is occurrence independent of date and amount?
- Can multiple events occur in the same month?
- Does same-month event ordering matter?
- Are event values inflation-indexed?
- Should there be labels/categories?
- Generic event creation or polished preset templates first?

### Strategy Model

- Is a strategy a pure function of time, portfolio state, and scenario state?
- Can a strategy inspect past returns and drawdowns?
- Can strategies react to market conditions?
- How should glide paths be represented?
- Should threshold rebalancing be future-supported in schema?
- Should strategy definitions be serializable as JSON?
- Should user-authored scripts ever be allowed?

### Engine Architecture

- TypeScript engine first or Rust/WASM from the beginning?
- How important is contributor readability?
- What is the target device and browser range?
- Should mobile be supported?
- Should Safari be supported?
- Should long simulations show partial results?
- Should simulations update automatically or require a Run button?
- Should results be progressively calculated after input edits?

### Statistics

- Should max drawdown be nominal, real, or both?
- What exactly is an underwater period?
- What exactly is time to break even?
- Should success probability be user-defined?
- Should there be a default success condition?
- Should CVaR be included?
- Are stats final-only or per-month?
- Can users download all per-run stats?

### UX

- Should the event editor be drag-and-drop?
- Can users drag event ranges on the chart?
- Should event amount distributions be edited visually?
- How should event timing uncertainty be represented?
- Can event markers be clicked and edited inline?
- Should the app use a sidebar plus results canvas layout?
- Should advanced bootstrap settings be hidden?
- Should the UI include explanatory statistical tooltips?
- Should there be a methodology mode?

## 25. Recommended Early Decisions

The most important early decisions are:

1. Build a client-side MVP unless performance proves insufficient.
2. Use React and TypeScript for the frontend.
3. Implement the first simulation engine in TypeScript inside a Web Worker.
4. Keep the engine pure and separate from UI.
5. Use fixed allocation with rebalancing as the first strategy.
6. Support only generic one-time cashflow events initially.
7. Use monthly linked-vector block bootstrap sampling.
8. Start with percentile fan chart, terminal distribution, and ruin probability.
9. Store/export scenario settings as JSON.
10. Keep accounts, taxes, LETFs, conditionals, and covariance out of the MVP.

## 26. Possible Primary User Flow

1. User opens the app.
2. User enters starting wealth.
3. User chooses time horizon.
4. User chooses recurring contribution or withdrawal.
5. User chooses stock/bond/cash allocation.
6. User selects bootstrap settings.
7. User optionally adds one or more probabilistic events.
8. User runs the simulation.
9. App displays percentile fan chart.
10. User hovers over the timeline to inspect results.
11. User checks terminal wealth distribution and risk stats.
12. User exports scenario or results.
13. Later, user compares with another strategy.

## 27. Possible Scenario JSON Shape

```json
{
  "version": 1,
  "name": "Example scenario",
  "timeline": {
    "unit": "month",
    "horizonMonths": 480
  },
  "initialPortfolio": {
    "totalValue": 250000,
    "valueMode": "real",
    "allocations": {
      "stocks": 0.7,
      "bonds": 0.2,
      "cash": 0.1
    }
  },
  "cashflows": {
    "recurringMonthly": {
      "amount": 2000,
      "valueMode": "real"
    }
  },
  "strategy": {
    "type": "fixed_allocation",
    "targetAllocation": {
      "stocks": 0.7,
      "bonds": 0.2,
      "cash": 0.1
    },
    "rebalance": {
      "type": "periodic",
      "frequencyMonths": 12
    }
  },
  "events": [
    {
      "id": "house_purchase",
      "label": "House purchase",
      "type": "expense",
      "occurrenceProbability": 0.6,
      "date": {
        "distribution": "uniform",
        "minMonth": 72,
        "maxMonth": 120
      },
      "amount": {
        "distribution": "normal",
        "mean": 150000,
        "standardDeviation": 30000,
        "valueMode": "real"
      }
    }
  ],
  "simulation": {
    "runs": 10000,
    "bootstrap": {
      "type": "block",
      "blockLengthMonths": 60,
      "wrapAround": true
    }
  }
}
```

## 28. Possible Result Summary Shape

```json
{
  "version": 1,
  "scenarioName": "Example scenario",
  "runs": 10000,
  "horizonMonths": 480,
  "percentilesByMonth": {
    "realPortfolioValue": {
      "p05": [],
      "p10": [],
      "p25": [],
      "p50": [],
      "p75": [],
      "p90": [],
      "p95": []
    },
    "nominalPortfolioValue": {
      "p05": [],
      "p10": [],
      "p25": [],
      "p50": [],
      "p75": [],
      "p90": [],
      "p95": []
    }
  },
  "terminalStats": {
    "real": {
      "mean": 0,
      "median": 0,
      "p05": 0,
      "p10": 0,
      "expectedShortfall05": 0
    },
    "nominal": {
      "mean": 0,
      "median": 0,
      "p05": 0,
      "p10": 0,
      "expectedShortfall05": 0
    }
  },
  "riskStats": {
    "probabilityOfRuin": 0,
    "medianMaxDrawdown": 0,
    "medianLongestUnderwaterMonths": 0
  }
}
```

## 29. Suggested Order of Operations to Decide

A proposed monthly sequence:

1. Apply recurring contributions or withdrawals.
2. Apply probabilistic events scheduled for the month.
3. Apply asset returns.
4. Apply inflation index update.
5. Apply asset fees.
6. Rebalance if applicable.
7. Record end-of-month state.

This should be finalized early and locked into tests.

## 30. Edge Cases to Consider

Event edge cases:

- Event amount sampled below zero.
- Expense larger than current portfolio.
- Multiple events in same month.
- Event date sampled outside timeline.
- Event occurrence probability of zero or one.
- Normal distribution producing impossible values.
- Event value specified as real but displayed nominal.

Portfolio edge cases:

- Allocation percentages not summing to one.
- Negative allocations.
- Zero starting wealth.
- Zero or negative recurring cashflow.
- Portfolio below zero.
- Rebalancing with zero wealth.
- Fees larger than returns.

Bootstrap edge cases:

- Block length longer than dataset.
- Horizon shorter than block length.
- Missing months.
- Non-overlapping datasets.
- Wrap-around block crossing dataset boundary.
- Truncated final block.

Visualization edge cases:

- Heavy-tailed outcomes compressing chart readability.
- Negative wealth on log scale.
- Percentile paths crossing due to interpolation or calculation bugs.
- Mean far above median.
- Ruin paths creating many zero-value paths.

Export edge cases:

- Version migration.
- Large result files.
- Unknown future strategy types.
- Backward compatibility.

## 31. Candidate Glossary

Block bootstrap:

- Sampling consecutive historical blocks instead of individual independent months.

Path:

- One simulated future timeline.

Run:

- One simulation path generated from sampled market data and event realizations.

Scenario:

- Complete user-defined set of inputs, including portfolio, events, strategy, and simulation settings.

Strategy:

- Rule that determines allocations and rebalancing behavior over time.

Event:

- Probabilistic positive or negative cashflow applied to the portfolio.

Ruin:

- A portfolio failure state, definition to be finalized.

Real value:

- Value adjusted for simulated inflation.

Nominal value:

- Dollar value without inflation adjustment.

Percentile fan chart:

- Visualization showing percentile bands of simulated outcomes over time.

Underwater period:

- Time spent below a previous high-water mark or other break-even threshold.

## 32. Summary of Current Consensus

Current strongest consensus:

- Open-source website-hosted web application.
- Polished CV-worthy product.
- React/TypeScript frontend.
- Likely monorepo.
- Client-side simulation should be considered strongly.
- TypeScript simulation engine in Web Worker is likely best first step.
- Rust/WASM remains a future optimization or alternate implementation.
- MVP should focus on block-bootstrap simulation, fixed allocation, probabilistic one-time events, and excellent visualization.
- Monthly time unit is fixed.
- Block size is configurable.
- Wrap-around is configurable.
- Taxes, accounts, LETFs, conditionals, covariance, and complex strategies are future work.
- Documentation should support later PRD creation.
