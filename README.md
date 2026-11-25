# The World in One Day — news-image-20261125

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/TUHIN729/nov25-news-image/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/TUHIN729/nov25-news-image/reward.svg)](https://make.fun/bounty/news-image-20261125)

A hero-led newspaper front page summing up the world's news of
**Wednesday 25 November 2026** — Shanghai's party chief falls in Xi's
purge, the UN's femicide count, Huawei's guilty verdict, a CIA breach,
25 hostages in Cartagena, 700,000 Russian troops killed, and a 5.3
quake in Nepal — drawn entirely in code.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png — 1024x1024 PNG, deterministic, no network
```

`main.py` is pure Python 3 standard library (no third-party packages):
it draws the page with an embedded 5x7 bitmap font and writes the PNG
with `zlib` itself, so the two grader runs produce byte-identical output.

## Entry

- Competition: [news-image-20261125](https://make.fun/bounty/news-image-20261125)
- $100 pot (1st $20) · deadline 27 November 2026 06:00 Dhaka
- Sources: Reuters, AP, AFP, UN Women, The Hindu, NDTV, RFE/RL
