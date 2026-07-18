# Family Game Hub

A browser-based game site you and your kids can design together. It has
tabs for different kinds of games — an "Arcade" tab for real-time
Python/Pygame games, and a "Puzzle" tab for simpler board/logic games
written in plain JavaScript. Add more tabs as you build more games.

**Live structure:** one landing page (`index.html`) with tabs, each tab
loading a game from its own folder under `games/`.

## Cost: $0

This is designed to be completely free to run:

- **GitHub** — free for a public (or private, with a free personal account)
  repository.
- **GitHub Actions** — free CI minutes for public repos build the site
  automatically every time you push.
- **GitHub Pages** — free static hosting for the finished site. No server,
  no Render account, no monthly bill.

If you'd rather host on Render instead of GitHub Pages, that also has a
free tier for static sites — see "Alternative: Render" below. Either way,
nothing in this project requires a paid plan.

## How the two kinds of games work

- **Puzzle tab (`games/tictactoe/`)** — plain HTML/CSS/JavaScript. Runs
  directly in any browser, no compiling. Best for board games, quizzes,
  memory games — anything turn-based.
- **Arcade tab (`games/snake/`)** — real Python, using the `pygame`
  library. Python doesn't normally run in a browser, so a tool called
  [pygbag](https://pypi.org/project/pygbag/) compiles the game to
  WebAssembly. Best for anything with movement, collisions, or real-time
  action.

## Local setup

You'll need [Python 3.10+](https://www.python.org/downloads/) and
[Git](https://git-scm.com/downloads) installed.

```bash
cd kids-game-hub
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install pygame pygbag
```

### Playing/testing the Puzzle tab locally

No install needed — just open `games/tictactoe/index.html` directly in a
browser, or run a local server from the project root:

```bash
python -m http.server 8000
# then visit http://localhost:8000
```

### Playing/testing the Arcade (Snake) game locally

To run it as a normal desktop Python game (fastest way to test changes):

```bash
python games/snake/main.py
```

To test the actual browser/WASM build before pushing:

```bash
python -m pygbag games/snake/main.py
```

This starts a local dev server (usually `http://localhost:8000`) serving
the compiled browser version — this is the closest preview to what will
actually run on the live site.

### Previewing the whole tabbed site locally (matches production)

`scripts/build_site.sh` runs the same steps as the GitHub Actions
workflow, so you can see the real, finished site — tabs, Snake, and
Tic-Tac-Toe together — before pushing:

```bash
chmod +x scripts/build_site.sh   # first time only
./scripts/build_site.sh
python -m http.server 8000 --directory site
# then visit http://localhost:8000
```

## Putting it on GitHub

```bash
cd kids-game-hub
git init
git add .
git commit -m "Initial game hub"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

## Turning on free hosting (GitHub Pages)

1. On GitHub, go to your repo's **Settings → Pages**.
2. Under "Build and deployment", set **Source** to **GitHub Actions**.
3. Push to `main` (or re-run the workflow from the **Actions** tab).
4. The included workflow (`.github/workflows/deploy.yml`) will
   automatically install `pygbag`, compile Snake to WebAssembly, assemble
   the site, and publish it. Your site will be live at
   `https://<your-username>.github.io/<repo-name>/`.

Every time you push a change — a new game, a tweaked color, a faster
snake — the site rebuilds and redeploys automatically. No manual build
step, no server to maintain.

## Adding a new game

See the "Add a Game" tab on the site itself for the full walkthrough.
Short version:

- **Simple game (no Python):** new folder in `games/`, a self-contained
  `index.html` inside it, and a new tab button/panel in the root
  `index.html`. Use `games/tictactoe/index.html` as a template.
- **Python/Pygame game:** new folder in `games/` with a `main.py` written
  using the async loop pattern in `games/snake/main.py` (required for
  browser compatibility), plus a matching build step added to
  `.github/workflows/deploy.yml` and a new tab in `index.html`.

## Alternative: Render instead of GitHub Pages

If you'd rather use Render:

1. Push this repo to GitHub as above (skip the Pages setup).
2. In Render, create a new **Static Site**, connect the repo.
3. Build command: `pip install pygbag && python -m pygbag --build games/snake/main.py && mkdir -p site/games/snake && cp index.html style.css script.js site/ && cp -r games/snake/build/web/* site/games/snake/ && cp -r games/tictactoe site/games/`
4. Publish directory: `site`
5. Render's free static site tier has no monthly cost, but free services
   may be slower to wake up after inactivity compared to GitHub Pages,
   which has no sleep/spin-down behavior at all.

## Project structure

```
kids-game-hub/
├── index.html              # landing page with tabs
├── style.css
├── script.js
├── games/
│   ├── snake/
│   │   └── main.py         # Python/Pygame, compiled via pygbag
│   └── tictactoe/
│       └── index.html      # plain JS, no build step
└── .github/workflows/
    └── deploy.yml          # auto build + deploy on every push
```
