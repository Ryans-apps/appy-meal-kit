# Worked example: sleep sounds + focus timer

**User:** "I only use my $60/year sleep app for brown noise and a timer that fades out. iPhone."

## Free-first (say this first)
> Your iPhone already has **Background Sounds**, free and built in: Settings → Accessibility → Audio & Visual → Background Sounds. It includes rain, ocean and noise sounds. On iOS 26 it also has "Stop Sounds with a Timer". That may be all you need. If you want your own mix, brown noise exactly how you like it, a fade-out, and a focus timer, I'll build it, with no ads and no account.

Source: https://support.apple.com/guide/iphone/play-background-sounds-iphb2cfa052c/ios. Re-open it before quoting.

## Interview answers (example)
- Brown noise most nights, sometimes rain. A 45-minute timer with a slow fade.
- A 25/5 focus timer during the day would be nice.
- Must keep playing with the screen locked.

## In / Out
**In:**
- White, pink and brown noise, generated in the app.
- A mix slider.
- Sleep timer with fade-out.
- Focus timer (25/5, adjustable) with a soft chime.
- Saved presets.

**Out:**
- The paid app's soundscapes, recordings, stories and meditations (its paid content).
- Sleep tracking through the microphone (privacy; out by default).

**Wish list (step 6):** suggested extras were (1) keep the screen on as a bedside clock, (2) a bedtime preset that starts mix + timer with one tap, (3) a gentle wake chime, and (4) a sound diary. They chose **(1) and (2)**:
- the **Screen Wake Lock API** for an optional dim "bedside clock" mode (supported in Safari 16.4+);
- a one-tap **Bedtime** preset.
- Be honest about (3): an alarm can't reliably ring with the app closed or the phone locked. The workable version is a phone alarm (offer an .ics event), or keep the app open with wake lock on.

**Content (step 7):** the noise and chimes are **made by the bot**: generated with Web Audio or pre-rendered, and labeled "Made by your bot". Recorded nature sounds come only from public-domain or CC0 libraries, checked per file.

**Recorded sounds (rain etc.):** only files whose own page says CC0 or public domain. Check each file's license, list it in LICENSES.md, and never use the paid app's audio.

## Building blocks

| Part | Does | License | Obligation |
|---|---|---|---|
| Web Audio API (built into the browser) | generates noise, gain, fades | n/a | n/a |
| Python on your computer (optional) | pre-renders a 60 s seamless noise loop as WAV/M4A | n/a (output is ours) | n/a |
| CC0 rain recording (optional) | rain | CC0, confirmed on its page | credit anyway |

## Build notes
- **Noise:**
  - White: random samples.
  - Pink: Paul Kellet's filter.
  - Brown: leaky integration of white noise, then normalize.
  - Fade with `gain.linearRampToValueAtTime`.
- **Screen-locked playback is the risk on iPhone.**
  - Test it on the user's phone (via the preview link) before calling it done.
  - If Web Audio stops when the screen locks, switch to an `<audio loop>` element playing a pre-rendered seamless loop. Generate it on your computer with a crossfaded seam.
  - Use the Media Session API so lock-screen controls show the app's own name.
- **Timer:** use timestamps, not `setInterval` counting, so it stays accurate if the phone throttles the page.
- **Credits:** list any CC0 recording; add "Not affiliated with any sleep app."

## Wrap-up message (example)
> **Hush is on your home screen.** Brown noise, rain, a 45-minute fade-out timer, and a 25/5 focus timer, all offline. Lock your phone tonight and tell me if it stops. I have a fallback ready.
> **You cancel the sleep app yourself** (App Store subscriptions: Settings → your name → Subscriptions).
