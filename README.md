# The World in Numbers — 25 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![make.fun rank](https://make.fun/badge/news-image-20261125/akbare12/news-25-b140-numbers/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![make.fun reward](https://make.fun/badge/news-image-20261125/akbare12/news-25-b140-numbers/reward.svg)](https://make.fun/bounty/news-image-20261125)

One front page that sums up Wednesday 25 November 2026 in numbers: **50 stories,
13 illustrated scenes, one pinned world map** — every story dated that day, nothing
from any other day.

## The front page

- **Hero trio** — US proposes new tariffs on 14 economies (China's total duty hits
  45%); the KOSPI crashes **−6.16%** to 4,697.51; Shenzhou-24 docks at Tiangong
  with the first Pakistani astronaut aboard. Each hero carries a WHY IT MATTERS.
- **DATE CHECK** — two lines. IN: 50 stories, every one dated 25 Nov 2026.
  LEFT OUT: Huawei verdict 24 Nov, PIF Tower strike 24 Nov, Sudan strikes
  24 Nov, Nvidia CEO reinstated 23 Nov.
- **47 numbered cards + map** — Bogor mine flood (9 dead, 17 trapped), the killing
  of Hamas security chief Col. Mohammad Abuelouf in Shati, US PCE 3.8% and Q3 GDP
  revised to 4.3%, the Solomon Islands treaty, Ebola at 11,986 cases, and more.
- **Every card carries C (confirmed), R (reported), CL (claimed) — plus ALSO.**
  The legend sits above the grid so every number on the page can be read at a glance.

## Verified before shipping

- `entry.png` is 1024×1024 and 206,685 bytes (under the 1 MiB cap).
- `main.py` passes a stdlib-only simulation: fresh venv without Pillow, different
  working directory, empty output directory, read-only repo copy — exit 0 and the
  output hash matches the shipped file.
- No story on the page is dated any day other than 25 November 2026.

## How it is built

- `gen.py` renders `entry.png` (1024×1024) with Pillow at build time.
- `main.py` is standard-library only (`os` + `shutil`): it copies `entry.png`
  into `MAKEFUN_OUTPUT_DIR` and verifies the PNG header, size and story count.
- `entry.png` is the shipped page; `gen.py` is the recipe that drew it.

## Sources

Reuters, AP, Xinhua, Al Jazeera, BEA, USTR, CNN Indonesia, Detik,
Jakarta Globe, TradingView, FXStreet, Argus.
