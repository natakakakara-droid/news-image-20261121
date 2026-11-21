# The World in One Day — 21 November 2026

A newspaper front page that sums up Saturday 21 November 2026 in five
verified stories, drawn as vector-style art with headline text so the day's
news reads from the image alone.

## The five stories

1. **THE HAGUE — WORLD COURT: Myanmar guilty of genocide.** The
   International Court of Justice found Myanmar's military responsible for
   genocide against the Rohingya in Rakhine State (2016–18) — the first
   time the court has held a state responsible for genocide. Myanmar called
   the ruling "unfair". (Reuters, 20 Nov 2026)
2. **UKRAINE — WAR: Russia hits three Kyiv bridges.** Overnight, Russia
   fired 400+ drones and 110+ missiles in one of the war's biggest
   barrages; three Dnipro bridges in Kyiv were damaged, at least nine
   people killed, power cut across the capital. (The Times / BBC, 20–21 Nov
   2026)
3. **INDIA — WEATHER: Cyclone Akvan strikes Odisha.** The storm made
   landfall near Gopalpur with gusts to 90 km/h; more than 300,000 people
   were moved to shelters. (IMD / The Hindu BusinessLine, 20 Nov 2026)
4. **ANTALYA — CLIMATE: COP31 draft drops fossil fuels.** The final draft
   of the UN climate talks omits coal, oil and gas, and the $120bn
   adaptation figure; negotiations spill into overtime as the 1.5°C limit
   nears breach. (AP / Fast Company, 20–21 Nov 2026)
5. **BRUSSELS — EUROPE: UK and EU seal Brexit reset.** Deals on food
   trade, linked carbon markets and youth mobility — 100,000 young people
   a year may live, work and study on either side for up to three years.
   (Reuters, 20 Nov 2026)

## How it is built

`render.py` draws `entry.png` (1024×1024) with Pillow from the DejaVu
fonts on the build machine — masthead, dateline, five story panels, each
with its own small illustration (scales of justice, a bridge under attack,
a cyclone spiral, a globe, the EU stars and Big Ben). `main.py` is the
grader entrypoint: it copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
using only the standard library, so the graded run needs no fonts, no
network and no randomness, and two runs write byte-identical output.

## Run

```sh
python3 render.py                    # rebuild entry.png (build machine)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # grade-style run
```
