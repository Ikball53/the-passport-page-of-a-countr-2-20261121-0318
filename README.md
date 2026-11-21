[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Ikball53/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Ikball53/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

# The Passport Page of a Country That Does Not Exist — Republic of Thalvarra

An open two-page passport spread for the invented maritime Republic of Thalvarra
(capital: Port Senn; language: Thalvarri; currency: thaler, TLM). The data page
shows holder Mira Solenne (born 04 JUN 1991 in Port Senn), passport TV 482 9173,
issued 12 MAR 2022 by the Port Senn Passport Office, expiring 11 MAR 2032, with
a two-line machine-readable zone. The facing page carries a plausible travel
history in order: a same-day ferry crossing to the Free City of Bellmar
(18–25 JUL 2023) and a 7-day visit to the Kingdom of Ostravia via Keld Pass
(02–09 OCT 2024) under transit visa OV-4471. The telling paperwork detail is the
endorsement on the data page: the bearer is a licensed tide-reader, valid for
night crossings of the Senn Channel (fee 45 TLM, receipt 8814) — a working
document detail that reveals a seafaring country without any caption.

## How it works

`build_image.py` draws the 1024×720 spread with Pillow and saves `entry.png`.
`main.py` (Python 3.13, standard library only, no network) copies the bundled
`entry.png` to `/output/entry.png`, creating `/output` if needed.
