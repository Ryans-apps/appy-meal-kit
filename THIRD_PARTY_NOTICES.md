# Third-party notices

The MIT license in `LICENSE` covers the files written for this kit. Nothing third-party is bundled here, but some files use or name outside projects. Their own licenses apply:

| Used by | Project | License | How it's used |
|---|---|---|---|
| `tools/make_puzzles.py` | [Stockfish](https://stockfishchess.org/) | GPL-3.0 | Run as a separate local tool; not included or shipped |
| `tools/make_puzzles.py` | [python-chess](https://github.com/niklasf/python-chess) | GPL-3.0 | Imported locally when you run the script; not included or shipped |
| `tools/make_puzzles.py`, `tools/sample_puzzles.json` | [Lichess games database](https://database.lichess.org/) | CC0 | Source games for the puzzles; the sample file links each source game |
| `tools/make_apk.sh` | [Capacitor](https://capacitorjs.com/) | MIT | Installed from npm when the script runs |
| `tools/make_apk.sh` | Android SDK, Temurin JDK, Node.js | Their own licenses (the Android SDK license must be read and accepted with `sdkmanager --licenses`) | Downloaded by you during setup |

The `examples/` files name other open-source libraries (for example chess.js, cm-chessboard, Mediabunny, MediaPipe, onnxruntime-web). None are included here. Re-check each license when you build, and list every part you use on the app's Credits screen.
