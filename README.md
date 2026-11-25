# The Tuesday Globe — news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/DanuMahiru/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/DanuMahiru/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image summing up the world news of **Tuesday 24 November 2026**,
built for the make.fun competition
https://make.fun/bounty/news-image-20261124
(pot $100, top 50 paid; entries close Thu 26 Nov 07:00 WIB).

## The image

`entry.png` (1024×1024, ~190 KB) is a newspaper front page drawn with
Pillow by `render.py`: 35 numbered stories, a huge date masthead
("TUESDAY 24 NOVEMBER 2026"), a 6-cell numbers strip (every cell tied
to an illustrated story), a region bar with per-region counts computed
from the story tags (EUROPE 10, AMERICAS 9, ASIA 6, MIDEAST 5, WORLD 3,
AFRICA 2), 4 large illustrated leads, 10 illustrated secondaries, a
"WHERE IT HAPPENED" dotted world map with 15 numbered pins, an
"ALSO ON TUESDAY" list, a DATE CHECK box, and per-story source
attribution. Every story carries a verification badge — CONFIRMED,
OFFICIAL, REPORTED or CLAIM — explained by a HOW WE CHECKED legend in
the footer. No photos, no network — every glyph is drawn from shapes.

Leads: Dow closes above 50,000 for the first time (50,018.70) · Israeli
strikes kill Hamas security chief Naeem Abu Nahel in Gaza · Houthi
attack hits a Riyadh tower, wounding 11, the second strike in under a
week · Russian strike on a Zaporizhzhia apartment block kills 2,
wounds 40.

## Files

- `render.py` — draws `entry.png` (deterministic: same bytes every run)
- `main.ts` — Node 22, stdlib only; copies `entry.png` to
  `MAKEFUN_OUTPUT_DIR` (or `/output`)
- `entry.png` — the finished image
- `RESEARCH.md` — every story with its source URL
- `RESULTS.md` — build report (commit, hashes, kit check)
- `.makefun/owner.json` — claim file for the make.fun wallet

## Run it

```sh
python3 render.py          # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Research

All 35 stories were verified from live reports on 25 Nov 2026
(Reuters, AP, BBC, Al Jazeera, UN News, NASA, Amnesty International,
the Conference Board, Motley Fool, StockMarketWatch). Only stories
that happened or were first reported on Tuesday 24 Nov 2026 are
leads; earlier items (COP31 collapse, the Merkury sinking, the Huang
reinstatement, the UN Libya probe call, the Megaspeed blacklist, the
Super Bowl IMAX announcement, the Board of Peace roadmap, the NATO
space warning, the Indonesia factory fire, the Guterres AI call) are
listed in the DATE CHECK box, never as leads. Two spot-checks
re-confirmed the lead facts against fresh reports: the Dow close
(50,018.70, +0.85%) and the Hasina December 16 return (Reuters
exclusive, dateline Nov 24). Full list with sources: `RESEARCH.md`.
