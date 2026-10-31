# Worked example: chess (puzzles + play the computer)

**User:** "I pay $14/month for Chess.com but I only do puzzles and play the bot. Build me my own?"

## Free-first (say this first)
> Before I build anything: **Lichess** (lichess.org) is free, has no ads, is open source, and has puzzles, play against the computer, and online games. If you just want to stop paying, it already covers what you use. Want your own anyway? I can make a simpler, offline, no-account version that's tuned to you.

Build only if they say yes.

## Interview answers (example)
- Daily puzzles, about 10 a day. Plays the computer at an easy-to-medium level.
- iPhone. Wants it offline on the subway. Wants to keep a puzzle rating and streak.

## In / Out
**In:**
- Puzzles with themes (forks, mates in 2…) and a personal puzzle rating.
- A daily streak.
- Play the computer at levels 1-10, with undo and hint.
- Save and resume games, and export games as PGN.

**Wish list (step 6):** suggested extras were (1) a "review my mistakes" queue, (2) a puzzle timer off switch, (3) a weekly progress chart, and (4) a theme filter built from the puzzles they miss. They chose **(1) Review my mistakes**:
- Every puzzle they get wrong goes into a replay queue, and comes back after 1, 3 and 7 days until they solve it cleanly.
- Games against the computer add the positions where their evaluation dropped by 2+ pawns (measured by the same Stockfish worker).
- Nothing needs a server; the queue lives in IndexedDB and is included in Export.

**Out:**
- Online play against people. Use Lichess for that; it's free.
- Video lessons and courses.
- Chess.com's own puzzles, game-review labels and design. That content is theirs.
- Cloud sync across devices. Export/Import is provided instead.

## Building blocks (re-open each license at build time)

| Part | Does | License (checked 2026-10-30) | Obligation |
|---|---|---|---|
| Lichess puzzle database (database.lichess.org) | 6.1M rated, themed puzzles as CSV | CC0 ("anything you like") | none; credit Lichess anyway |
| lichess-org/chess-openings | opening names | CC0-1.0 | none |
| chess.js (jhlywa/chess.js) | legal moves, check/mate, PGN/FEN | BSD-2-Clause | keep notice |
| cm-chessboard (shaack/cm-chessboard) | SVG board, drag/tap moves | MIT | keep notice |
| stockfish.js (nmrugg/stockfish.js), Stockfish | engine in a Web Worker (WASM) | GPL-3.0 | public source repo + license + "Source code" link in Credits |

Not chosen: chessground (GPL-3.0, Lichess's board). It's fine to use with the same GPL steps, but cm-chessboard keeps the rest MIT.

## Content (step 7)
Offer the three sources:
1. **Openly licensed:** the Lichess puzzle DB (CC0), as below. This is the default.
2. **Their own:** positions from their own games (PGN export from wherever they play), turned into puzzles by the same script.
3. **Made by the bot:** run `tools/make_puzzles.py` on a Lichess monthly games file (CC0, database.lichess.org). It keeps only positions where Stockfish (MultiPV 2) finds a single clearly best move (≥ +250 cp or mate, second-best ≥ 200 cp worse and ≤ +100). Mate-in-one positions are kept only if exactly one move mates. Each puzzle is re-checked at 4x the search depth.
   - `tools/sample_puzzles.json` has 6 sample outputs (tested 2026-10-30).
   - Tag these "Made by your bot from a Lichess game (CC0)", and spot-check 10 by replaying them.
   - Never take positions from the paid app's puzzles or screenshots.

All puzzles live in `content/puzzles.json`. The user can delete or add positions (FEN + moves) from an Edit screen.

## Build notes
- **Puzzles:**
  - Download `lichess_db_puzzle.csv.zst` on your computer. Decompress it with `zstd -d`.
  - Sample about 3,000 puzzles across the user's rating band (e.g. 800-1800), weighted by their themes, using `Popularity > 80`.
  - Write them to `puzzles.json` (a few hundred KB) and precache it. Never ship the whole 6M file.
- **Puzzle logic:** FEN is the position *before* the opponent's move. Apply `Moves[0]` automatically. The user must find `Moves[1]`, the app plays `Moves[2]`, and so on. Accept any move that gives mate in place of the expected mating move.
- **Rating:** simple Elo update against the puzzle's `Rating` (K≈32 for the first 30 puzzles, then 16). Store it in IndexedDB with the streak and history.
- **Engine:**
  - Run Stockfish in a Web Worker.
  - Levels map to UCI `Skill Level` 0-20 plus a short `movetime` (e.g. 100-1000 ms).
  - Use the **lite single-threaded** build (`stockfish-*-lite-single.js` + `.wasm`, about 1.7 MB). The stockfish.js README recommends it, and it needs no special server headers.
  - Multi-threaded builds need `Cross-Origin-Opener-Policy` and `Cross-Origin-Embedder-Policy` headers, which GitHub Pages doesn't let you set.
- **Credits screen:**
  - Lichess (CC0 data).
  - chess.js (BSD-2), cm-chessboard (MIT), Stockfish (GPL-3.0) with a link to the public repo.
  - "Not affiliated with Chess.com or Lichess."

## Wrap-up message (example)
> **Pocket Puzzles is on your home screen.** 3,000 puzzles near your level, a streak, and the computer at 10 levels, all offline. Tap Export in Settings now and then to back up your rating and games.
> Remember: **you cancel Chess.com yourself.** If you subscribed in the App Store, do it under Settings → your name → Subscriptions. Download any games you want to keep first. Want me to check in next Friday to see if you miss anything?
