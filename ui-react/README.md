# Financial Document Intelligence UI

This is a web UI built with **Vite + React + TypeScript + Tailwind CSS**.

You do not need to know React to run it locally.

## Prerequisites

- **Node.js**: install the latest LTS version (recommended).
- **npm**: comes with Node.

To verify:

```bash
node -v
npm -v
```

## Run locally

1. Install dependencies:

```bash
npm install
```

1. Start the dev server:

```bash
npm run dev
```

1. Open the URL printed in your terminal (usually):

```text
http://localhost:5173
```

## Production build

1. Build:

```bash
npm run build
```

1. Preview the production build locally:

```bash
npm run preview
```

## Common issues

- **Port already in use**
  - Stop the process using the port, or run Vite on a different port:
    - `npm run dev -- --port 5174`

- **Blank page / styles missing**
  - Make sure you ran `npm install`.
  - Restart the dev server.

- **Node version problems**
  - If you see odd build errors, upgrade to the latest Node LTS.
