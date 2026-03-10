# Space Invaders — Neon Edition

A modern, neon-themed Space Invaders game built with **Next.js 15**, **TypeScript**, and **Tailwind CSS**. Features smooth animations, procedural sound effects, destructible barriers, and responsive touch controls.

## Features

- **Neon cyberpunk visual theme** — glowing aliens, CRT scanlines, animated starfield
- **Three difficulty levels** — Easy, Medium, and Hard with progressive alien speed and shoot rate
- **Level progression** — clear a wave to advance; aliens respawn faster each level
- **UFO mystery ship** — flies across the top for 50–300 bonus points
- **Destructible barriers** — pixel-level (8×6 segment grid) damage simulation per bunker
- **Particle explosion effects** on every kill and player hit
- **Procedural sound effects** via Web Audio API — no external audio files required
- **High score persistence** via localStorage
- **Pause / Resume** with `P` or `Escape`
- **Fully responsive** — works on desktop, tablet, and mobile
- **Mobile touch controls** — on-screen ◀ ▶ move buttons + FIRE + ⏸ pause
- **Animated menus** using Framer Motion

## Tech Stack

| Technology | Purpose |
|---|---|
| Next.js 15 (App Router) | Framework & routing |
| TypeScript (strict mode) | Type safety |
| Tailwind CSS v4 | Styling |
| HTML5 Canvas | Game rendering |
| Framer Motion | UI animations |
| Web Audio API | Procedural sound effects |
| nanoid | Unique entity IDs |
| localStorage | High score persistence |

## Controls

### Desktop (Keyboard)

| Key | Action |
|---|---|
| `Arrow Left` / `A` | Move left |
| `Arrow Right` / `D` | Move right |
| `Space` / `Arrow Up` / `W` | Fire |
| `P` / `Escape` | Pause / Resume |

### Mobile (Touch)

| Button | Action |
|---|---|
| ◀ | Move left |
| ▶ | Move right |
| FIRE | Shoot |
| ⏸ | Pause / Resume |

## Alien Score Values

| Alien | Points |
|---|---|
| Small (top row) | 30 pts |
| Medium (middle rows) | 20 pts |
| Large (bottom rows) | 10 pts |
| UFO Mystery Ship | 50–300 pts |

## Getting Started

### Prerequisites

- Node.js 18+
- npm / yarn / pnpm / bun

### Run Locally

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Deploy to Vercel

This project is pre-configured for zero-config Vercel deployment.

**Option 1 — Vercel Dashboard:**
1. Push your code to a GitHub repository
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import your repository and click **Deploy** — no additional configuration needed

**Option 2 — Vercel CLI:**
```bash
npx vercel
```

## Project Structure

```
src/
├── app/
│   ├── layout.tsx             # Root layout with metadata & CRT scanline overlay
│   ├── page.tsx               # Home page
│   └── globals.css            # Global styles & neon CSS variables
├── components/
│   ├── SpaceInvadersGame.tsx  # Root game component (state orchestration)
│   ├── GameCanvas.tsx         # Canvas renderer wrapper
│   ├── MenuScreen.tsx         # Animated main menu with difficulty selection
│   ├── GameOverScreen.tsx     # Victory / game over overlay
│   └── MobileControls.tsx    # Touch input buttons for mobile
├── hooks/
│   ├── useGameLoop.ts         # requestAnimationFrame game loop
│   ├── useKeyboard.ts         # Keyboard input state tracking
│   ├── useSound.ts            # Web Audio API procedural sound effects
│   └── useHighScore.ts        # localStorage high score persistence
├── utils/
│   ├── gameInit.ts            # Initial state factories (aliens, barriers)
│   ├── gameLogic.ts           # Per-frame update logic (pure functions)
│   └── renderer.ts            # Canvas 2D drawing functions
├── types/
│   └── game.ts                # TypeScript interfaces & type definitions
└── constants/
    └── game.ts                # Canvas dimensions, difficulty configs, colors
```

## License

MIT
