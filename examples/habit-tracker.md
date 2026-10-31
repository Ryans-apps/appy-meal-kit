# Worked example: habit tracker

**User:** "I pay $40/year for a habit app. I track 5 habits and mostly care about streaks."

## Free-first (say this first)
> On Android, **Loop Habit Tracker** is free, open source (GPL-3.0), and has no ads, so it may be all you need. On iPhone, or if you'd like exactly your 5 habits and nothing else, I'll build you one.

Check the current free tier of the app they're paying for, too. Many habit apps allow a few habits for free.

## Interview answers (example)
- 5 daily habits plus 1 "3x a week" habit. Checks them off at night.
- iPhone. Wants streaks, a month calendar, and a nudge at 9 pm.

## In / Out
**In:**
- Daily and "N times a week" habits.
- One-tap check-off, with undo.
- Current and best streak.
- A month calendar heatmap.
- Notes on a day.
- Export/Import as JSON and CSV.

**Out:**
- Social challenges and friends.
- The paid app's coaching content and its look.
- Watch apps and widgets (web apps can't do these).

**Wish list (step 6):** suggested extras were (1) reminders, (2) a "skip day" that doesn't break the streak, (3) a weekly summary, and (4) habit notes. They chose **(1) a 9 pm reminder**. Be honest about how it works:
- **Web push** works on iPhone only for home-screen web apps on iOS 16.4+, after they tap Allow, and it needs a push server. It's more setup, and it's off by default here.
- **Workable versions, offered instead:**
  - an **.ics calendar event** the app downloads (repeating daily at 9 pm, with its own alert, which works even if the app is closed);
  - a Grok Bot routine message.
- **Not possible:** a home-screen widget or watch complication. Use the app's fast "Today" screen instead.

**Nudge:** web push on iPhone needs the installed web app plus a push server. Simpler: offer a Grok Bot routine that messages them at 9 pm ("Habits check: tap to open"). Create it only if they say yes.

## Building blocks

| Part | Does | License (checked 2026-10-30) | Obligation |
|---|---|---|---|
| none: plain HTML/CSS/JS | everything | n/a | n/a |
| Chart.js (optional) | trend charts | MIT | keep notice |

Prefer zero dependencies. The calendar heatmap is a CSS grid.

**Content (step 7):** optional. If they want habit ideas or tips, write fresh ones and check any health claims (sleep, exercise) against cited sources such as CDC or NHS pages. Add the "not medical advice" line, label them "Made by your bot", and save them in `content/tips.md`.

## Build notes
- **Data model** (IndexedDB):
  - `habits {id, name, emoji, target: {type: 'daily'|'weekly', n}, createdAt, archived}`
  - `checks {habitId, date: 'YYYY-MM-DD'}`
- **Dates:** use the phone's local date, never UTC, so a check at 11 pm counts for today.
- **Streak:**
  - Daily habits: count consecutive days back from today. If today isn't checked yet, start from yesterday so the streak doesn't show 0 at breakfast.
  - Weekly habits: count consecutive weeks that met N.
- **Big tap targets.** Checking off is a single tap with a short haptic (`navigator.vibrate`) where supported; Android only.
- **Credits:** "Not affiliated with any habit app."

## Wrap-up message (example)
> **Streaks is on your home screen.** Your 6 habits, streaks, and a month view. Your data lives only on this phone, so tap Export now and then.
> **You cancel the old app yourself**, and export your history from it first if it lets you. I set up the 9 pm nudge you asked for; say "stop habit nudges" any time.
