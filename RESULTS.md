# RESULTS — news-image-20261124 ("The Tuesday Globe")

## Entry
- Competition: news-image-20261124 — "Sum up 24 November's world news in one image"
- Deadline: Thu 26 Nov 07:00 WIB (2026-11-26T00:00:00Z). Pot $100, top 50 paid.
- Repo: https://github.com/DanuMahiru/news-image-20261124 (to be created by Danu on his phone; NOT pushed — parent pushes).
- Build commit: `fd21b9c` ("The Tuesday Globe — 35 verified Tuesday 24 Nov 2026 stories").
  This report is committed on top of the build commit; the pushed HEAD
  is the commit containing this file (see git log).
- Files: render.py, main.ts, package.json, entry.png, README.md, LICENSE,
  RESEARCH.md, .makefun/owner.json (wallet Ht2eWKDiyDQqBK3k7nxuLbC5zAfywxhipgBd4kdZbGSJ).

## The image
- `entry.png`: 1024×1024 RGB, 190,224 bytes (limit 1 MiB).
- sha256 `2d92415313643ec5006167626273ca85e0b870680e7ee8d721e10e01eca42e17`
  — identical across repeated runs (deterministic).
- main.ts copies entry.png to MAKEFUN_OUTPUT_DIR (or /output); verified
  byte-identical (same sha256 as entry.png).
- "The Tuesday Globe": the proven newspaper-front formula (masthead,
  red date band, dark navy numbers strip, region bar, 4 leads in one
  row with poster-style art panels, 10 secondaries in two columns,
  ALSO list left, dotted map right with 15 pins, DATE CHECK box, HOW WE
  CHECKED legend). Every story carries a verification badge (CONFIRMED /
  OFFICIAL / REPORTED / CLAIM). All drawn with Pillow, no photos, no
  network. Renderer written fresh in this session; the news-23 v2 repo
  was read as reference only (no files copied).
- New in this build: a "coin" lead-art motif (big $ coin + gold
  up-arrow) for the Dow story; the dotted map is a fresh hand-drawn
  outline; two map pins dropped (№8 Gaza meningitis and №11 San
  Francisco — same spots as №2 Gaza City and №6 Santa Clara).

## Stories (all verified Tue 24 Nov 2026; full list + URLs in RESEARCH.md)
- Leads: Dow closes above 50,000 for the first time (50,018.70, +0.85%;
  S&P -0.50%, Nasdaq -1.48%) · Israeli strikes kill Hamas internal
  security chief Naeem Abu Nahel and six others in Gaza · Houthi attack
  hits a Riyadh King Abdullah Financial District tower, wounding 11 —
  second strike on the capital's tallest tower in under a week ·
  Overnight Russian strike on a Zaporizhzhia apartment block kills 2,
  wounds 40 including four children.
- Secondaries: UAE bus crash kills 13 in Ras Al Khaimah · Nvidia slides
  5.9% to $155.38, shedding ~$233bn · Putin vows refinery revenge ·
  Gaza meningitis alert (272 cases in October, 8x the norm) · Iran rial
  hits a record low (2.82m per dollar) · Pope Francis's diary reveals a
  2021–22 spiritual crisis · King tides flood California · Russia's
  Progress 97 cargo ship lifts off to the ISS · Amnesty: Tigray
  shelling must be probed as war crimes (14 dead) · Como edge AEK 1–0.
- ALSO 15–35: US confidence 103.3 · ADI plunges 17.4% · Norway talks
  Ukraine stability · Russian jets enter Korea ADIZ · Iraq seizes Kurd
  oilfields · Japan pays ICC early · UK sanctions four Houthis · UK
  warns firms on sabotage · Hegseth holds 60 Patriots · Hasina seeks
  Dec 16 return · Seoul pays AI-cheat tipsters · China starts 6G
  pilots · Ariane lofts 36 Leo satellites · Falcon 9 launches USSF-266
  · Arsenal 1–1 Dortmund · Bodø/Glimt beat LASK 1–0 · Betis win 2–0 at
  Slovan · Ebola staff still trapped in DRC · FBI probes police DB
  breach · Australia sets 46 AI rules · Huckabee doubts aid cutoff.
- Region counts (computed from the tags): EUROPE 10, AMERICAS 9,
  ASIA 6, MIDEAST 5, WORLD 3, AFRICA 2 = 35.
- DATE CHECK excludes pre-Tuesday items: COP31 collapse, Merkury
  sinking, Huang reinstatement, UN Libya probe call, Megaspeed
  blacklist, Super Bowl IMAX, Board of Peace roadmap, NATO space
  warning, Indonesia factory fire, Guterres AI call.
- Two date corrections caught during research: the UNSMIL Libya probe
  call was Monday 23 Nov (moved to DATE CHECK, replaced in the 35 by
  Norway's Tuesday Ukraine-stability dialogue); the DRC Ebola item was
  reframed to the genuine Tuesday development (UN News Tue update).
- Two spot-checks re-confirmed the lead facts against fresh reports:
  the Dow close (50,018.70, +0.85%; S&P -0.50%; Nasdaq -1.48%) and
  the Hasina December 16 return (Reuters exclusive, dateline Nov 24).

## Verification (visual read of the rendered image)
- Confirmed by eye (full image + zoomed crops of the leads and map):
  every lead body ends on a full stop; every secondary body fits whole
  in two lines with its source appended in grey; every ALSO item fits on
  one line with its badge; all 15 map pins are individually legible
  (Europe/Middle East cluster: 17, 14, 4, 7, 10, 2, 9, 3, 5, 13 each
  readable, leader lines in place); DATE CHECK fits on two lines; HOW WE
  CHECKED legend fits on one line; no overlaps or clipped text remain.
  Render-time assertions (in render.py fit_check) also guard every one
  of these, including a minimum 17px separation between map-pin label
  circles.
- One fix during the build: lead 2's body was trimmed ("Medics said"
  dropped) to stay within 5 lines; the fact (three died at a Khan
  Younis police post) is kept.

## Kit check
- (To be filled in after the kit check runs — parent runs it.)

## NOT submitted (as tasked)
Parent to submit: bundle this builder's session with --muse-usage,
re-run check with the bundle, push the final HEAD to
https://github.com/DanuMahiru/news-image-20261124.git, then submit
before Thu 26 Nov 07:00 WIB. Danu must create the repo on his phone
first (VM repo creation times out).
