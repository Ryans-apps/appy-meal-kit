# Worked example: Combine mode (a paid video editor plus a separate photo editor)

*This is a worked example of how a build goes, not a real user's app. The conversation and choices below are illustrative.*

**User:** "I pay for the pro tier of a video editor for short 9:16 videos, and I use a separate layered photo editor for thumbnails and overlays. I keep exporting from one and importing into the other. Can you merge them into one app on my phone? It should work offline."

Same guardrails for both apps:
- public pages only, read logged-out;
- no logins, no code, no network inspection;
- their screenshots only if they choose to send them;
- functionality, not looks. No brand names, icons, templates, stickers, fonts, music or effects from either app.

## Free-first (say this first)
Check whether either app's free tier already covers what they use, and whether a free, open-source editor does both jobs on their phone. Re-check the current options and licenses at build time and name them with links. If one fits, say so first. Build only if they still want their own.

## Public research (step 3), grouped by app

| # | Which app | Feature (your own words) | Free or paid tier | Source | Notes from reviews |
|---|---|---|---|---|---|
| 1 | Video editor | Trim, split and reorder clips on a timeline | free | (feature page, opened this turn) | — |
| 2 | Video editor | Auto captions with styles | paid | (help article) | accuracy praised; English best |
| 3 | Video editor | Speed change, transitions, filters | free / paid | (store listing) | — |
| 4 | Video editor | 1080p export without a watermark | paid | (pricing page) | main reason people pay |
| 5 | Photo editor | Layers, blend modes, opacity | paid | (feature page) | — |
| 6 | Photo editor | Background removal | paid | (help article) | edges around hair criticised |
| 7 | Photo editor | Clone / heal | free | (store listing) | — |
| … | | | | | |

**Overlaps:** both apps have text with presets and stickers. One shared text and sticker system serves both editors.

**Hand-offs (the copy-paste steps):** "export the photo, then import it into the video as an overlay", and "export a frame to make a thumbnail". These become the headline merged features.

## Checklist (step 5, what they tick)
- [x] Video: trim, split, join video and photo clips, speed, text, stickers, photo overlays, music, voiceover, transitions, filters, 1080×1920 export
- [x] Captions: automatic, editable, styled, burned into the export
- [x] Photo: layers, blend modes, opacity, background removal, masks, text layers, clone and heal
- [ ] Templates marketplace, stock footage library, cloud projects, team sharing (not used)

## In / Out (tagged by source app)
**In:**
- [Video] Timeline with trim, split, join, speed, transitions, filters, text, stickers, overlays, music and voiceover.
- [Video] Captions made on the device (English speech model), editable line by line.
- [Photo] Layers, blend modes, opacity, masks, text layers, clone and heal.
- [Photo] Background removal: a fast mode, and a slower "fine edges" mode.
- **[Merged]** "Send to video": a layered photo becomes a video overlay, and "Edit photo" reopens it with the layers kept.
- **[Merged]** One drafts list for photos and videos, saved automatically.

**Out:**
- Both apps' templates, stock media, stickers, fonts and effects (their content).
- Cloud projects and team sharing. They need a server; offer Export/Import of a backup zip instead.
- Long 4K exports. Too heavy for a phone browser (see browser limits below).

## Wish list (step 6)
Suggested extras:
1. Caption style presets with a word-by-word highlight.
2. A safe-zone guide for the parts of a vertical video that app buttons usually cover, labelled as an estimate.
3. Slow pan-and-zoom (Ken Burns) on photo clips.
4. A quick person cut-out on a video clip.
5. One-tap export, with a faster 720p option.

They chose all five.

## Own content (step 7)
- **Stickers:** a small set of simple shapes (arrow, circle, burst, "NEW" tag, speech bubble, underline) drawn by the bot as SVG. Emoji use the phone's own emoji font, so no emoji font is bundled.
- **Caption presets:** four styles (for example "Bold pop", "Clean box", "Tall", "Marker") designed by the bot from open-licensed fonts.
- **App icon:** made by the bot.
- All of it is labelled "Made by your bot", marked `"madeBy": "bot"`, and editable. Nothing is traced or reworded from either app.
- Music and sound effects only from CC0 sources fetched from the creator's own page, with the license file kept.
- Record each item's origin in `content/SOURCES.md`.

## Building blocks and licenses (step 7)
Checked live on 2026-10-30 with the GitHub license API (`https://api.github.com/repos/<owner>/<repo>/license`), then confirmed by opening the LICENSE file and the npm package metadata. Re-check at build time.

| Part | What it does | License (as checked) | Notes |
|---|---|---|---|
| Mediabunny (WebCodecs) | Read and write MP4/WebM, encode with the browser's own encoder | MPL-2.0 | File-level copyleft: ship it unmodified with its license, or publish changes to its files |
| ffmpeg.wasm (`@ffmpeg/ffmpeg` wrapper) | FFmpeg in the browser (fallback only) | Wrapper MIT (repo API: MIT; npm 0.12.15: MIT) | The wrapper loads a separate core, below |
| ffmpeg.wasm core (`@ffmpeg/core`) | The FFmpeg build itself | npm 0.12.10: **GPL-2.0-or-later** | Built with GPL parts. FFmpeg itself (repo API: NOASSERTION; LICENSE.md) is LGPL-2.1+, and becomes GPL-2.0+ with `--enable-gpl`. If you ship this core, the app's source must be available under GPL-compatible terms. The npm package unpacks to about 65 MB (the .wasm itself is roughly 30 MB), it's slower than WebCodecs, and the multithreaded build (`@ffmpeg/core-mt`, also GPL-2.0-or-later) needs cross-origin isolation. **Plan: don't ship it unless WebCodecs is missing.** |
| MediaPipe Tasks Vision | Fast background / person segmentation | Apache-2.0 (repo API) | Block its usage-logging requests with a CSP and the service worker, and test that there are 0 outside requests |
| MODNet (ONNX) | "Fine edges" cut-out | Apache-2.0 (repo API) | Check the converted model's card too |
| Transformers.js + ONNX Runtime Web | Run the speech model in the browser | Apache-2.0 / MIT (repo API) | |
| Whisper tiny.en / base.en | Speech to text with word timings | Code MIT (repo API); check the weights' model card | English only |
| Konva | Photo editor canvas, layers | MIT (repo API: NOASSERTION; the LICENSE file is MIT) | When the API says NOASSERTION, read the file |
| fflate | Backup zip | MIT (repo API) | |
| Fonts | Text and caption styles | OFL-1.1 / Apache-2.0 | Self-host with the license files |

## Browser limits (say these honestly in the plan)
- **It's a web app.** It opens from a link in Chrome, Safari, Edge or Firefox on a phone, tablet or computer, and can be added to the home screen. Basic editing, drafts and backup work in all four.
- **Export uses WebCodecs.** Chrome and Edge (desktop and Android) have had it for years. Firefox has it on desktop (130+) but not on Android. Safari has video encoding from 16.4 and audio encoding only from 26 (iOS and macOS). The app checks at runtime and says clearly when export isn't available, instead of failing silently.
- **Audio codec:** AAC isn't available for encoding in Firefox or on desktop Linux, so export falls back to Opus there (WebM, or MP4 with Opus). Check AAC on the user's own phone.
- **Heavy video work** (1080p export, captions, cut-outs) runs best in Chrome or Edge on Android or a desktop computer. Expect about real time or slower on a phone, and suggest 720p for long videos.
- **Memory:** phone browsers can kill a tab that uses too much memory, iPhone Safari especially. Process frames as a stream (never load a whole video into memory), cap the export length (for example a 3-minute warning), and save drafts often.
- **File size:** imported videos are stored in the browser's storage (IndexedDB). The quota is large on current browsers, but storage isn't guaranteed. Ask for persistent storage, show usage in Settings, and remind the user to export a backup.
- **iPhone Safari:**
  - Data in a Safari tab and data in the home-screen app are kept **separately**. Pick one, and use backup to move projects.
  - In a Safari tab, site data can be deleted after 7 days without use. The home-screen app is exempt, so recommend adding it to the home screen.
  - The speech and cut-out models are tens of MB. Offer a "download for offline" button rather than assuming they're cached.
- **Offline:** the app shell works offline after the first visit in any of the four browsers. Models work offline only after their packs are downloaded.

## Plan and OK (step 8, example)
> **Plan: one offline editor for photos and 9:16 videos**
> - **In:** the video timeline, captions on the device, layered photo editing with background removal, and Send to video / Edit photo between them. Wish-list extras: caption presets with highlight, safe-zone guide (estimate), Ken Burns, video cut-out, one-tap export with 720p.
> - **Out:** both apps' templates, stock media and effects; cloud projects; 4K.
> - **Content:** bot-made stickers, caption presets and icon (labelled), CC0 music and sound effects.
> - **Parts:** Mediabunny (MPL-2.0), MediaPipe (Apache-2.0), MODNet (Apache-2.0), Transformers.js and ONNX Runtime Web, Whisper, Konva (MIT), fflate (MIT). No ffmpeg.wasm, to stay clear of its GPL core and its size.
> - **Where it works:** any current browser for editing. Exporting and captions work best in Chrome or Edge on Android or a computer. On iPhone, add it to the home screen, and expect slower exports and a memory limit on long videos.
> - **Data:** stays on your device, with a backup zip.
>
> OK to build?

## Wrap-up (example)
> **Your editor is live.** Open the link in any browser, or add it to your home screen. Make a design in Photo, tap **To video**, and it lands on your timeline. Tap **Captions** to transcribe on your phone.
> **You cancel the video editor's pro tier yourself** (export any projects first). The photo editor can go whenever you're happy.
