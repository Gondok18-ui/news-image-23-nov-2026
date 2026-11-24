[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Gondok18-ui/news-image-23-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard)
[![reward](https://make.fun/badge/news-image-20261123/Gondok18-ui/news-image-23-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261123)

# The Daily Meridian — the world of Monday, 23 November 2026, on one page

An original broadsheet newspaper front page, drawn entirely in code, that
sums up the world news of Monday 23 November 2026 in a single 1024×1024
image.

## What the page shows

- **Masthead** — *The Daily Meridian*, with the date line
  "Monday, 23 November 2026" on a navy date bar and a black "Also Today"
  ticker carrying the day's one-line stories: Tarik Skubal's record
  $450M Mets deal, the capture of "El Chapo Isidro" in Sinaloa, the
  Nigeria funeral-boat capsize that killed 24, China's Shenzhou-24 crew,
  the Indonesia factory fire with 34 missing, and the USA & UK winning
  the Women's World Cups.
- **Lead story** — the collapse of the COP31 climate summit: talks break
  down in anger over fossil fuels, with no deal to phase out coal, oil
  and gas. The story carries a drawn illustration — a cracked,
  overheating planet standing in flames beside a thermometer at record
  heat — and a caption from the island-state delegates who walked out.
- **Three panels** — Ukraine's naval drones striking Russian warships at
  Benghazi (and the Sparta II ablaze in the Gulf of Finland); three more
  tankers struck in the Strait of Hormuz amid a record pace of attacks;
  and the FBI's investigation into an apparent hack of the NCIC police
  database.
- **Four briefs** — markets surging as Nvidia's Jensen Huang reignites
  the AI trade; reports of a Russian nuclear-armed satellite and NATO's
  space-defence vow; Britain sanctioning Myanmar's junta leaders after
  the World Court's genocide ruling; and the Democrats' US House
  majority swelling to 259 seats, their largest since 1992.

## How the program works

`main.py` (Python 3, Pillow only) composes the page from flat vector
shapes and typeset text: a double-ruled page frame, a serif masthead, a
navy date bar, a black ticker strip, the lead story with its drawn globe
illustration, three ruled story columns and a row of briefs. All
headlines and body copy are written for this entry, and the drawing is
fully deterministic — no randomness, no clock, no network — so two runs
write byte-identical files.

Run it:

```sh
python3 main.py            # writes entry.png beside the program
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Under the make.fun harness it writes `/output/entry.png`. The image is
a whole PNG, exactly 1024×1024 pixels and well under the 1 MiB limit.
