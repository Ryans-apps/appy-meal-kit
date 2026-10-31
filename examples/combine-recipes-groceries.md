# Worked example: Combine mode (a recipe box and a grocery list app)

**User:** "I keep recipes in one app ($30/year) and do my shopping list in another (free, but full of ads). I'm forever copying ingredients across. Can you merge them into one?"

Same guardrails for both apps:
- public pages only, read logged-out;
- no logins and no code;
- their screenshots only if they choose to send them;
- functionality, not looks;
- none of either app's own recipes or content.

## Free-first (say this first)
Check whether either app already does both jobs, or has a built-in "add to list" for the other. Also check whether a free open-source app covers both: re-check current options and licenses at build time. If one does, say so first.

## Public research (step 3), grouped by app

| # | Which app | Feature (your own words) | Free or paid tier | Source | Notes from reviews |
|---|---|---|---|---|---|
| 1 | Recipe app | Save recipes from a web link | paid | (feature page, opened this turn) | imports sometimes miss steps |
| 2 | Recipe app | Scale servings | paid | (help article) | loved |
| 3 | Grocery app | Shared list by aisle | free | (store listing) | ads complained about |
| … | | | | | |

**Overlaps:** both have a plain list, and the user picks the grocery app's aisle grouping.

**Hand-offs:** "copy ingredients from a recipe to the list". This becomes the headline merged feature.

## In / Out (tagged by source app)
**In:**
- [Recipe] Recipe box with tags and search.
- [Recipe] Scale servings.
- [Grocery] List grouped by aisle, with tap to tick.
- **[Merged]** "Add ingredients to list", which skips what they already have.
- **[Merged]** Week planner that builds the list.

**Out:**
- [Recipe] The recipe app's own recipe collection (its content).
- [Grocery] Live sharing with family. That needs a server; offer an Export link or a text share of the list instead.

**Bringing data over:** they export recipes from the recipe app's own export (if it has one) and send the file. You write an importer for that file.

## Wish list (step 6)
Suggested extras:
1. Pantry staples that never get added twice.
2. Cost per recipe.
3. Cook mode, which keeps the screen on with the Screen Wake Lock API.
4. Share the list to a partner through the share sheet.

They chose (1) and (3).

## Content (step 7)
Their own recipes come first. If they want starter recipes, write **fresh** ones and label them "Made by your bot". Never reword recipes from either app or from screenshots. Nutrition facts are checked against USDA FoodData Central (cite it), with the "not medical advice" line.

## Wrap-up (example)
> **Sam's Kitchen is on your home screen.** Recipes, a week plan, and a grocery list in aisle order. Tap "Add to list" on any recipe.
> You can now stop using both apps. **You cancel the recipe subscription yourself** (export your recipes first). The grocery app is free, so delete it whenever you like.
