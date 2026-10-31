# PWA scaffold

Copy this folder to `apps/<app-name>/`, then:
1. Rename "My App" and `myapp` (in index.html, manifest, app.js `DB`, and sw.js `CACHE`).
2. Make the PNG icons: `rsvg-convert -w 192 icon.svg > icon-192.png && rsvg-convert -w 512 icon.svg > icon-512.png`. If rsvg-convert is missing, `apt-get install librsvg2-bin`, or use ImageMagick/Python.
3. Add every new file to `FILES` in sw.js.
4. Fill in the Credits list.
5. Run it: `python3 -m http.server 8080`, then open http://localhost:8080.
