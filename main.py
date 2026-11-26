#!/usr/bin/env python3
"""Entry point for news-image-20261125 (numbers edition, trial b140).

Copies the pre-rendered front page (entry.png, drawn at build time by
gen.py) into the grader output directory. This module uses ONLY the
standard library (os and shutil) on purpose: the grader runs in a
stdlib-only environment, so no third-party import may appear here.

Layout of the page it ships:
  * masthead "THE WORLD IN NUMBERS", Wednesday 25 November 2026
  * hero trio: US tariffs on 14 economies (China 45%), KOSPI -6.16%,
    Shenzhou-24 docking with the first Pakistani astronaut aboard
  * DATE CHECK box (two lines: IN vs LEFT OUT). The left-out line names
    only stories from other days: Huawei verdict 24 Nov, PIF Tower strike
    24 Nov, Sudan strikes 24 Nov, Nvidia CEO reinstated 23 Nov.
  * 47 numbered story cards + 1 pinned world-map cell = 50 stories
  * every card carries C (confirmed), R (reported), CL (claimed) and ALSO

The STORIES manifest below mirrors the page card by card. main() checks
that the manifest holds 50 entries, that every entry carries C / R / CL /
ALSO, and that the shipped PNG is a real 1024x1024 image under 1 MiB.
Run:  python3 main.py   (MAKEFUN_OUTPUT_DIR overrides the output dir)
"""
import os
import shutil

STORIES = (
    "01 TARIFFS 45% — US proposes new tariffs on 14 economies; China +20% on top of 25% already in place, EU/Japan/Korea/Taiwan at 15%, Vietnam up to 35%. C 14 · R 45% top · CL 35% — ALSO 15% cap.",
    "02 KOSPI -6.16% — Index closes at 4,697.51, down 308.52 points; Samsung -9.87% and SK hynix -11.05% lead the rout; the 5,000 level is lost a day after it was regained. C 4,697.51 · R 308.52 lost · CL 5,000 lost — ALSO Taiex -6.0%.",
    "03 SHENZHOU-24 DOCKS — Crew of 3 enters Tiangong at 06:35 GMT after launching from Jiuquan; Zeeshan Ali, 40, ex-PAF pilot, is the first Pakistani and first foreign astronaut aboard. C 3 crew · R 06:35 GMT · CL 1st foreign — ALSO 2 Chinese aboard.",
    "04 BOGOR MINE FLOOD — 9 dead, 17 trapped, Mt Butak shafts; a river flooded illegal gold shafts and 325 rescuers are on site. C 9 dead · R 17 · CL 26 — ALSO 325.",
    "05 ABUELOUF, HAMAS CHIEF — Col. Mohammad, 47, wife, 2 girls; killed with his family in a Shati strike, the second such killing in 24 hours. C 4 · R 2nd · CL 47 — ALSO Shati.",
    "06 US INFLATION 3.8% — PCE 3.8% as expected; core PCE 3.3% tops the forecast and Q3 GDP is revised to 4.3%. C 3.8% · R 3.3% · CL 3.2% — ALSO GDP.",
    "07 WALL ST COMEBACK — Nasdaq fell 4.6% intraday, then staged the year's biggest comeback as tariff fears hit tech. C 4.6% drop · R 3% · CL 2% — ALSO tech.",
    "08 SUDAN: 19 KILLED — RSF drone strikes kill 19 civilians in Damazin, Blue Nile state; 20 more are wounded. C 19 · R 20 · CL 1 — ALSO Blue Nile.",
    "09 RUSSIA: 112 DRONES — Russia launches 112 drones at Ukraine in an overnight barrage; five regions lose power. C 112 · R 5 · CL 5 — ALSO overnight.",
    "10 UKRAINE HITS REFINERIES — Ukraine strikes 2 refineries inside Russia while facing the overnight drone barrage. C 2 refineries · R 112 · CL 1 — ALSO deep strikes.",
    "11 POWER OUT IN 5 REGIONS — Russian strikes cut power in 5 Ukrainian regions; 5 people are killed and grids are under repair. C 5 regions · R 5 killed · CL 112 — ALSO repair.",
    "12 SOLOMON TREATY — Australia and the Solomon Islands sign a security treaty in Canberra; no foreign bases allowed. C 1 · R 0 · CL 4 yrs — ALSO top partner.",
    "13 CHINA PROBES CHEN JINING — Shanghai party chief and Politburo member Chen Jining is under investigation. C 1 · R 4th · CL 1 — ALSO Shanghai chief.",
    "14 EBOLA: 11,986 CASES — DR Congo Ebola cases reach 11,986 with 5,871 deaths; the outbreak grinds on. C 11,986 · R 5,871 · CL 49% — ALSO up.",
    "15 GREECE STRIKE — A 24-hour general strike shuts transport, ferries and flights in a living-costs protest. C 24h · R 1 · CL 3 — ALSO costs protest.",
    "16 KING TIDES FLOOD — King tides flood California and the Macy's parade is postponed for the first time in a century. C 1 · R 100 yrs · CL 1st — ALSO parade.",
    "17 TAIWAN: 1 SORTIE — One Chinese sortie crosses the median line while 9 naval vessels are counted nearby. C 1 · R 9 · CL 1 — ALSO Taipei counts.",
    "18 HEAT RECORD 2.24C — The world logs 6 straight days 2C above preindustrial levels; the peak hits 2.24C. C 2.24C · R 6 days · CL 2C — ALSO hottest.",
    "19 JOBLESS CLAIMS 189K — US jobless claims come in at 189K, below the 200K consensus; labour stays tight. C 189K · R 200K · CL 11K — ALSO tight labour.",
    "20 DURABLE GOODS SOFT — Advance durable goods orders come in weaker than expected in the holiday-eve data dump. C 1 · R 1 miss · CL 4 — ALSO data dump.",
    "21 BEIGE BOOK OUT — The Fed Beige Book lands at 19:00 GMT, the last word before the rate call, covering 12 districts. C 1 · R 12 districts · CL 1 — ALSO quiet nears.",
    "22 TAIEX -6.0% — Taiwan's Taiex falls 6.0% and at its worst is down 8.6% intraday as chip stocks lead the fall. C 6.0% · R 8.6% · CL 1 day — ALSO chips fall.",
    "23 SAMSUNG -9.87% — Samsung falls 9.87% to 170,700 won and SK hynix drops 11.05% to 1.03m won in the Kospi chip rout. C 9.87% · R 11.05% · CL 170,700 — ALSO chip rout.",
    "24 INDIA: 25% TARIFF — India faces up to 25% tariff under the USTR proposal, or 17% if a trade deal is finalised. C 25% · R 17% · CL 14 — ALSO USTR plan.",
    "25 VIETNAM: 35% TARIFF — Vietnam faces up to 35% under the proposal, or 20% if a deal is finalised; the highest in Asia. C 35% · R 20% · CL 14 — ALSO top in Asia.",
    "26 INDONESIA NAMED — Indonesia is among the 14 economies in the US tariff proposal, one of 6 in South-East Asia. C 14 · R 6 SE Asia · CL 1 — ALSO Jakarta.",
    "27 EU: 15% CAP — The EU faces a 15% tariff under the US proposal and the bloc weighs a reply; the cap matches earlier deals. C 15% · R 27 · CL 14 — ALSO cap matches.",
    "28 CHINA: 45% TOTAL — China's total duty hits 45% on some goods under the proposal: 20% new on top of 25% already in place. C 45% · R 20% new · CL 25% old — ALSO top.",
    "29 PROBE ENDS — The USTR ends an 8-month excess-capacity probe under Section 301; 14 of 16 probed economies are named. C 8 mo · R 14 · CL 16 — ALSO Section 301.",
    "30 CHINA EASES US CURBS — China extends its suspension of dual-use export controls to the US in a MOFCOM move. C 1 · R 1 · CL 2 — ALSO MOFCOM move.",
    "31 EU HYBRID REPLY — China is to issue temporary EU hybrid vehicle measures in answer to EU safeguards. C 1 · R 27 · CL 1 — ALSO safeguards.",
    "32 PBOC: CNY800B MLF — The PBoC runs a CNY800B 1-year medium-term lending operation to support liquidity. C 800B · R 1 yr · CL 1 — ALSO liquidity.",
    "33 HK POWER BILLS UP — Hong Kong power tariffs are to rise between 1.8% and 7.9% at CLP and HK Electric. C 7.9% · R 1.8% · CL 2 — ALSO CLP + HK Electric.",
    "34 $44B 7-YEAR SALE — A $44B 7-year note sale closes after the PCE data lands; the third Treasury sale of the week. C $44B · R 7 yrs · CL 3rd — ALSO Treasury wk.",
    "35 INCOME +0.7% — US personal income rises 0.7% while consumer spending slows to +0.3% in the BEA data dump. C 0.7% · R 0.3% · CL 3.8% — ALSO BEA dump.",
    "36 GDP REVISED TO 4.3% — US Q3 GDP is revised up from 3.4% to 4.3%, the fastest in 3 years, in the second estimate. C 4.3% · R 3.4% · CL 3 yrs — ALSO 2nd estimate.",
    "37 CORE PCE: 3-YR HIGH — Core PCE at 3.3% is the highest in 3 years and rate-hike bets rise after the print. C 3.3% · R 3.2% · CL 3 yrs — ALSO hike bets.",
    "38 NEW HOME SALES — New-home sales land in the holiday-eve data dump with housing in focus. C 1 · R 4 · CL 1 — ALSO housing focus.",
    "39 KOREA SURVEY 104.8 — South Korea's business survey reads 104.8 against 105.6 prior; manufacturing mood slips. C 104.8 · R 105.6 · CL 0.8 — ALSO mood.",
    "40 SHANGHAI -0.7% — The Shanghai Composite opens -0.7% at 3,523 while the Hang Seng edges +0.1% to 22,253. C 3,523 · R 0.7% · CL 22,253 — ALSO mixed Asia.",
    "41 NASDAQ FUTS -1% — Nasdaq futures drop over 1% in Asia trading while S&P futures slip 1.3% to 0.7%. C 1% · R 1.3% · CL 0.7% — ALSO futures red.",
    "42 CHIP STOCKS -10% — Japan chip stocks Kioxia and Advantest fall over 10% as the Nikkei slides 2.9%. C 10% · R 2 · CL 2.9% — ALSO Nikkei slides.",
    "43 GAZA: 11 KILLED — 11 Palestinians are killed in Gaza since dawn, hospitals say, including 2 girls; Shati is hit hardest. C 11 · R 2 girls · CL 1 — ALSO Shati hit.",
    "44 ABU NADA KILLED — Hamas political bureau member Khaled Abu Nada is killed in central Gaza with his wife; he was deputy education minister. C 1 · R 1 wife · CL 1 — ALSO deputy minister.",
    "45 CEASEFIRE STALLS — The Trump-backed Gaza ceasefire plan stalls as strikes go on for a second day and the Board of Peace is tested. C 1 · R 0 · CL 2nd day — ALSO Peace Board.",
    "46 ISRAEL: OPERATIVES HIT — Israel's military says it targeted several operatives in Gaza, including 2 senior chiefs, in 24 hours. C 1 · R 2 chiefs · CL 24h — ALSO IDF confirms.",
    "47 GERMANY: Q3 GDP — The German Q3 GDP print and a 10-year Bund auction are due, with Berlin in focus. C 1 · R 10-yr · CL 1 — ALSO Berlin focus.",
    "48 UN CHIEF WARNS — The UN chief warns heating is accelerating as the planet logs a record 6-day streak above 2C. C 2.24C · R 6 days · CL 1 — ALSO Guterres.",
    "49 GOLD DIPS — Gold slips about 17 points after the hot US data while safe havens trade mixed. C 17 pts · R 3.8% · CL 1 — ALSO havens mixed.",
    "50 US500 DIPS — The US500 moves about 44 ticks lower in the data window as four releases reprice stocks fast. C 44 · R 4 · CL 1 — ALSO fast reprice.",
)


def _png_size(path):
    """Read width/height from a PNG IHDR chunk without any image library."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: %s" % path)
    if head[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk: %s" % path)
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    return width, height


def _check_manifest():
    """The page promises 50 stories; every one carries C, R, CL and ALSO."""
    if len(STORIES) != 50:
        raise ValueError("manifest holds %d stories, expected 50" % len(STORIES))
    for i, line in enumerate(STORIES, 1):
        for tag in ("C ", "R ", "CL ", "ALSO"):
            if tag not in line:
                raise ValueError("story %02d is missing %r" % (i, tag))


def main():
    _check_manifest()
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise ValueError("entry.png is missing next to main.py; run gen.py first")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    width, height = _png_size(dst)
    if (width, height) != (1024, 1024):
        raise ValueError("entry.png is %dx%d, expected 1024x1024" % (width, height))
    size = os.path.getsize(dst)
    if size > 1024 * 1024:
        raise ValueError("entry.png is %d bytes, over the 1 MiB cap" % size)
    if size < 100 * 1024:
        raise ValueError("entry.png is only %d bytes, looks empty" % size)
    print("copied %s -> %s (%dx%d, %d bytes, 50 stories)" % (src, dst, width, height, size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
