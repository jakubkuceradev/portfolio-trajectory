# Agents

## Tech Stack (planned)

- TypeScript + React (client-side SPA)
- Web Workers for simulation
- Optional Rust/WebAssembly for hot loops

## Commands

- `npm run dev` — React Router dev server
- `npm run lint` — ESLint
- `npm run format` — Prettier write
- `npm run format:check` — Prettier check
- `npm run typecheck` — `react-router typegen && tsc`

## Workflow

- **Always lint before format before committing**: `npm run lint && npm run format`

## Architecture Notes

- Simulation engine is behind a swappable interface
- Historical market data feeds the block-bootstrap return sampling
