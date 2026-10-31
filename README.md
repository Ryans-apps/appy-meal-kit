# Appy Meal kit

Helper files for **Appy Meal**, a Grok Bot template that builds your own private web app to replace an app you pay for, or to combine the 2-3 apps you juggle into one.

Grok Bot templates can't carry extra files, so the starter code, worked examples and build tools live here. An Appy Meal bot fetches them on its first build.

## What's here

| Path | What it is |
|---|---|
| `scaffold/` | Working offline web-app (PWA) starter: `index.html`, `app.js` (IndexedDB store, Export/Import backup), `manifest.webmanifest`, `sw.js` (offline cache, scoped per app), icons and a Credits screen. See `scaffold/README.md`. |
| `examples/chess.md` | Replace a chess subscription: puzzles plus play-the-computer, with the free options to suggest first |
| `examples/habit-tracker.md` | Zero-dependency streak-based habit tracker |
| `examples/sleep-sounds-timer.md` | Generated white, pink and brown noise with a sleep or focus timer |
| `examples/combine-recipes-groceries.md` | Combine mode: a recipe box and a grocery list merged into one app |
| `examples/combine-video-photo-editor.md` | Combine mode: a video editor plus a layered photo editor in one offline web app, with a license table and browser limits |
| `tools/make_apk.sh` | Optional: wraps a finished app into a signed Android APK with Capacitor, for the user's own phone only |
| `tools/make_puzzles.py` | Makes original chess puzzles from CC0 Lichess games, checked with Stockfish for a single best answer |
| `tools/sample_puzzles.json` | 6 sample puzzles produced by `make_puzzles.py` |

## How an Appy Meal bot uses it

Clone the whole kit:

```bash
git clone --depth 1 https://github.com/Ryans-apps/appy-meal-kit
cp -r appy-meal-kit/scaffold apps/<app-name>
```

Or fetch single files by raw URL:

```
https://raw.githubusercontent.com/Ryans-apps/appy-meal-kit/main/scaffold/index.html
https://raw.githubusercontent.com/Ryans-apps/appy-meal-kit/main/tools/make_apk.sh
```

Browse it at https://ryans-apps.github.io/appy-meal-kit/

## Notes

- No keys, passwords or personal data belong in this repo. `make_apk.sh` reads the keystore password from the `KS_PASS` environment variable and creates the signing key outside the app folder. Keep both private.
- Tool versions in `make_apk.sh` were current on 2026-10-30. Re-check them before use.
- License: MIT (see `LICENSE`). Outside projects keep their own licenses (see `THIRD_PARTY_NOTICES.md`).
