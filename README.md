# portfolio-trajectory

Interactive lifecycle investing simulator with block-bootstrap market returns and probabilistic financial events.

portfolio-trajectory is an open-source web application for modeling long-term portfolio outcomes under uncertainty. It helps users explore how different financial strategies may perform across many possible historical market trajectories, using probabilistic simulation instead of single-point projections.

The project is focused on polished interaction design, transparent methodology, and intuitive visualization of investment risk.

## Purpose

The main question the app explores is:

> Given current wealth, expected savings or withdrawals, uncertain future financial events, and a selected portfolio strategy, what range of outcomes should a user expect?

The application is intended for FIRE and investing enthusiasts, individual planners, and anyone interested in understanding how portfolio decisions may behave across different market environments.

## Core concept

The simulator generates many possible future portfolio paths using historical monthly market data. Instead of assuming a fixed return rate, it samples blocks of historical returns to preserve some of the autocorrelation and regime behavior found in real markets.

Users can define a financial scenario with:

- starting portfolio value,
- simulation horizon,
- portfolio allocation,
- recurring contributions or withdrawals,
- large one-time financial events,
- bootstrap settings,
- and strategy assumptions.

The result is visualized as a range of probabilistic outcomes rather than a single forecast.

## Key features

Planned core features include:

- interactive timeline-based scenario editor,
- historical block-bootstrap return simulation,
- stock, bond, and cash portfolio model,
- fixed allocation with rebalancing,
- probabilistic one-time cashflow events,
- real and nominal portfolio tracking,
- percentile-based trajectory visualization,
- probability of ruin and drawdown statistics,
- scenario export and reproducible configuration files.

## Probabilistic events

The app's timeline supports major financial events such as:

- home purchases,
- large medical expenses,
- inheritance,
- philanthropic giving,
- major one-time spending goals,
- and other positive or negative cashflows.

Events may include uncertainty in timing, amount, and occurrence. Initial distributions are expected to include fixed, uniform, and normal distributions.

## Simulation methodology

The first implementation focuses on monthly block bootstrap simulation.

Each run builds a possible future timeline by sampling consecutive blocks of historical monthly returns. These sampled blocks include market returns and inflation, allowing each simulated path to develop its own nominal and real value trajectory.

The block length is configurable. A one-month block is equivalent to ordinary bootstrap sampling, while longer blocks can better preserve short- and medium-term market behavior.

## Visualization

The primary interface is an interactive portfolio trajectory chart.

Expected visual outputs include:

- percentile bands over time,
- median and lower-bound outcome lines,
- terminal wealth distribution,
- probability of ruin over time,
- drawdown and recovery statistics,
- event markers on the timeline,
- and comparison views for future strategy evaluation.

The goal is to make probabilistic investing outcomes understandable at a glance while still exposing enough detail for deeper analysis.

## Technical direction

The initial implementation is planned as a client-side TypeScript and React application.

Simulation logic will start in TypeScript, likely running inside a Web Worker to keep the interface responsive. The simulation engine will be designed behind a clear interface so performance-critical hot loops can later be replaced with Rust compiled to WebAssembly if needed.

The intended architecture is:

- React and TypeScript for the user interface,
- TypeScript for scenario modeling and validation,
- Web Workers for simulation execution,
- a swappable simulation engine interface,
- optional Rust/WebAssembly for future numerical hot loops.
