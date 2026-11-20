# One image of 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/arisasmara/ai-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/arisasmara/ai-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for the make.fun bounty **news-image-20261120** — "Sum up 20 November's
world news in one image".

## The image

`entry.png` is a single 1024 x 1024 editorial poster. Deep teal / dark-green
background, warm amber accents, white bold labels. A banner across the top
names the day in large letters: **20 NOVEMBER 2026**. Below it, one wide
hero panel and a 2 x 3 grid of six panels sum up the day's news.

The seven stories, all events of Friday 20 November 2026, verified against
Reuters, BBC, CNN, Al Jazeera, Politico and other outlets on the day:

1. **KYIV BRIDGES BLITZED** — 110 missiles, Poland scrambles jets. Russia
   launched its biggest attack on Kyiv's Dnipro bridges of the war: more
   than 110 missiles and around 400 drones overnight, damaging three
   bridges across the Dnipro. Debris from two missiles fell in Poland,
   which scrambled jets and Patriots.
2. **CYCLONE AKVAN LANDS** — Odisha hit, 300,000 evacuated. Cyclone Akvan
   made landfall near Gopalpur, Odisha, on Friday morning with winds of
   70–80 kmph, weakening to a deep depression inland. More than 300,000
   people were evacuated; the third cyclone to hit India in under a month.
3. **ASIA STOCKS CRASH** — Nikkei −4.8%, AI fears spread. Asian markets
   fell sharply: the Nikkei dropped 4.8% to a seven-month low, the Kospi
   5.2%, the Taiex 6.6%, and SoftBank 16%, in the worst week since 2020,
   as the AI rally unravelled.
4. **ITALY STRIKES** — General strike, 100+ cities march. The CGIL union's
   general strike brought marches to more than 100 Italian cities against
   the Meloni government's economic policies, part of a Europe-wide day of
   youth mobilisation.
5. **COP31 STALLS** — Fossil fuels cut from draft. The Antalya climate
   talks reached their final scheduled day with no deal: the latest draft
   stripped out all fossil-fuel language and dropped the $120bn adaptation
   target, and talks looked set to spill into the weekend.
6. **SAUDI WAR DRAGS ON** — Missile downed, Sana'a bombed. The war with
   the Houthis continued on Friday: Saudi air defences intercepted a
   ballistic missile aimed at the southern region, and Saudi airstrikes
   hit Sana'a, a day after the Houthis' missile strike on Riyadh's PIF
   Tower.
7. **HARRIS MEETS MACRON** — Courtesy call in Paris. Former US Vice
   President Kamala Harris met President Emmanuel Macron at the Élysée
   on Friday for a brief private courtesy meeting, with Doug Emhoff
   present.

The picture is a flat, stylised illustration — no photographs, no
photorealistic faces, no company logos. It was drawn by `draw_image.py`
in this repository (Pillow), from the verified story list above.

## The program

`main.py` (Python 3.13, standard library only) does one thing: it copies
the `entry.png` shipped in this repository, byte for byte, to the output
directory as `entry.png`. It uses no network, no clock and no randomness,
so both runs write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The image lands at `out/entry.png`.

To re-render the poster from scratch:

```sh
python3 draw_image.py
```

## License

MIT — see `LICENSE`.
