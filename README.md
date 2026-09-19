<div id="top"></div>

# Kotogumo

Bootstrap the frontend, Web API, and analysis service for a blog word cloud generator, with shared formatting, type checking, linting, testing, and coverage gates.

## Tech Stack

<p style="display: inline">
  <img src="https://img.shields.io/badge/-TypeScript-3178C6.svg?logo=typescript&style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/-React-61DAFB.svg?logo=react&style=for-the-badge&logoColor=black">
  <img src="https://img.shields.io/badge/-Vite-646CFF.svg?logo=vite&style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/-Hono-E36002.svg?logo=hono&style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/-Python-3776AB.svg?logo=python&style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/-FastAPI-009688.svg?logo=fastapi&style=for-the-badge&logoColor=white">
</p>

## Table of Contents

1. [About the Project](#about-the-project)
2. [Environment](#environment)
3. [Directory Structure](#directory-structure)
4. [Getting Started](#getting-started)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Available Commands](#available-commands)
8. [License](#license)

## About the Project

Kotogumo is split into three independently runnable components:

- `apps/frontend` - the React top page users load in a browser.
- `apps/api` - the Hono Web API that will front the analysis service.
- `services/analysis` - a Python service that will own morphological
  analysis and word cloud image generation as a separate internal process.

This repository currently bootstraps the project structure and quality
gates only: an installable, startable skeleton for each component with a
smoke test proving it starts up correctly (a rendered top page, and a
`GET /health` response from each backend). Product features and production
deployment are out of scope here.

<p align="right">(<a href="#top">back to top</a>)</p>

## Environment

| Language / Framework | Version       |
| -------------------- | ------------- |
| Node.js              | >=22          |
| TypeScript           | 6.0.3         |
| React                | 19.3.0        |
| Vite                 | 8.3.0         |
| Hono                 | 4.13.8        |
| Python               | >=3.14, <3.15 |
| FastAPI              | 0.141.1       |

See `package-lock.json` for the full TypeScript dependency list and
`services/analysis/uv.lock` for the full Python dependency list.

<p align="right">(<a href="#top">back to top</a>)</p>

## Directory Structure

```text
.
├── .github
│   └── workflows
├── apps
│   ├── api
│   │   └── src
│   └── frontend
│       └── src
├── services
│   └── analysis
│       ├── src
│       │   └── analysis
│       └── tests
├── assets
├── LICENSE
├── README.md
└── package.json
```

### Main Directories

| Directory           | Description                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------- |
| `apps/frontend`     | React + TypeScript + Vite top page.                                                         |
| `apps/api`          | Hono Web API running on the Node.js runtime.                                                |
| `services/analysis` | Python + FastAPI analysis service (morphological analysis, word cloud image generation).    |
| `assets`            | Static brand assets (logo, favicon).                                                        |
| `.github/workflows` | CI: formatting, type checking, lint, test, and coverage on push, pull request, and nightly. |

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

### Prerequisites

- Node.js >=22
- [uv](https://docs.astral.sh/uv/) (manages its own Python 3.14 toolchain)

### Clone the Repository

```bash
git clone https://github.com/kishimin/blog-wordcloud.git
cd blog-wordcloud
```

### Frontend and Web API (npm workspace)

Install once from the repository root; this installs both `apps/frontend`
and `apps/api`.

```bash
npm install
```

Run every workspace's test suite:

```bash
npm run test
```

Start the frontend dev server:

```bash
npm run dev -w apps/frontend
```

Open:

```text
http://localhost:5173
```

Start the Web API:

```bash
npm run start -w apps/api
```

Open:

```text
http://localhost:8787/health
```

### Analysis Service

Install dependencies (uv creates and manages the virtual environment):

```bash
cd services/analysis
uv sync
```

Run the test suite:

```bash
uv run pytest
```

Start the service:

```bash
uv run uvicorn analysis.app:app --reload
```

Open:

```text
http://localhost:8000/health
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

### Web API health check

```bash
curl http://localhost:8787/health
```

### Analysis service health check

```bash
curl http://localhost:8000/health
```

Both return the same shape:

```json
{ "status": "ok" }
```

<p align="right">(<a href="#top">back to top</a>)</p>

## API Endpoints

### Web API (`apps/api`)

| Method | Path      | Description                                        |
| ------ | --------- | -------------------------------------------------- |
| `GET`  | `/health` | Returns `{"status": "ok"}` when the process is up. |

### Analysis Service (`services/analysis`)

| Method | Path      | Description                                        |
| ------ | --------- | -------------------------------------------------- |
| `GET`  | `/health` | Returns `{"status": "ok"}` when the process is up. |

<p align="right">(<a href="#top">back to top</a>)</p>

## Available Commands

### Root (npm workspace: frontend and api)

| Command                                            | Description                                                                                    |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `npm install`                                      | Install dependencies for `apps/frontend` and `apps/api`.                                       |
| `npm run format`                                   | Format the TypeScript/JSON/Markdown files with Prettier.                                       |
| `npm run format:check`                             | Check formatting without writing changes.                                                      |
| `npm run typecheck`                                | Type check every workspace package (`tsc --noEmit`).                                           |
| `npm run lint`                                     | Lint every workspace package (ESLint).                                                         |
| `npm run test`                                     | Run every workspace package's Vitest suite.                                                    |
| `npm run test:small`                               | Run only `*.small.test.*` files (ADR-0004/0043: the set CI runs on push).                      |
| `npm run test:pr`                                  | Run Small and Medium test files (the set CI runs on pull requests).                            |
| `npm run test:nightly`                             | Run Small, Medium, and Large test files (the set CI runs on schedule/`workflow_dispatch`).     |
| `npm run test:coverage`                            | Run every workspace package's Vitest suite with coverage (80% threshold enforced per package). |
| `npm run test:coverage:small` / `:pr` / `:nightly` | Same coverage run, scoped to the matching test-size set above.                                 |

### Frontend (`apps/frontend`)

| Command                            | Description                           |
| ---------------------------------- | ------------------------------------- |
| `npm run dev -w apps/frontend`     | Start the Vite dev server.            |
| `npm run build -w apps/frontend`   | Build the production bundle.          |
| `npm run preview -w apps/frontend` | Preview the production build locally. |

### Web API (`apps/api`)

| Command                     | Description                                 |
| --------------------------- | ------------------------------------------- |
| `npm run dev -w apps/api`   | Start the API with auto-reload (tsx watch). |
| `npm run start -w apps/api` | Start the API once, without auto-reload.    |

### Analysis Service (`services/analysis`, run from that directory)

| Command                                    | Description                                                                                    |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `uv sync`                                  | Install dependencies into a managed virtual environment.                                       |
| `uv run ruff format --check .`             | Check formatting without writing changes.                                                      |
| `uv run ruff check .`                      | Lint the service.                                                                              |
| `uv run mypy src tests`                    | Type check the service and its tests (strict mode).                                            |
| `uv run pytest`                            | Run the test suite.                                                                            |
| `uv run pytest -m small`                   | Run only tests marked `small` (ADR-0004/0043: the set CI runs on push).                        |
| `uv run pytest -m "small or medium"`       | Run Small and Medium tests (the set CI runs on pull requests).                                 |
| `uv run pytest --cov`                      | Run the test suite with coverage (80% threshold enforced by `fail_under` in `pyproject.toml`). |
| `uv run uvicorn analysis.app:app --reload` | Start the service with auto-reload.                                                            |

<p align="right">(<a href="#top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE` for the full text.

<p align="right">(<a href="#top">back to top</a>)</p>
