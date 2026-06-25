# Agents

## Tech Stack (planned)

- TypeScript + React (client-side SPA)
- Web Workers for simulation
- Optional Rust/WebAssembly for hot loops

## Commands

No tooling configured yet. When adding:
- Use Vite for React/TypeScript dev server
- Place lint, typecheck, and test commands in package.json scripts

## Architecture Notes

- Simulation engine is behind a swappable interface
- Historical market data feeds the block-bootstrap return sampling
