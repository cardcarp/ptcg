# Contributing

Thank you for helping maintain this data!

Before jumping in, please review these community resources:

*   **[Join Discord](https://discord.gg/9ASXsqeUWr):** Discuss structure and data accuracy.

## 🌭 Local Setup

Before submitting a pull-request, please test your changes locally to ensure they compile correctly.

1. Clone repository.
2. Install required Python dependencies: `pip install .`
3. Run the compile script to verify your YAML syntax and schema compliance: `python script/compile.py`

## 🪲 Automated Validation

Every pull-request is automatically validated against the schema via GitHub Actions. If the pipeline fails, your pull-request cannot be merged. You can view the exact line causing the error by clicking "Details" on the failed GitHub-Action check.

<br>

## 🔑 How IDs Work

**Never write an ID into a YAML file.** Every ID is derived from the record's own properties at build time, and cross-references are written as human-readable names.

| Record | ID is derived from | Example |
| --- | --- | --- |
| Collection | `name` | `Base` → `base` |
| Set | `name` | `Team Rocket` → `team-rocket` |
| Card | `set` + `index` | `Base` + `058` → `base-058` |
| Oracle | `name` + `origin` | `Pikachu` + `base-058` → `pikachu-base-058` |
| Deck | `set` + `name` | `BREAKpoint` + `Wave Slasher` → `breakpoint-wave-slasher` |

So a card references its set as `set: Base`, not `set: base` and never `set: base1`. The build kebab-cases it for you.

**`oracle` is the one reference written in kebab-case**, because an oracle has no single human name that identifies it — `oracle: pikachu-base-058`, not `Pikachu-base-058`. See below for why an oracle needs the extra anchor.

Filenames exist purely so editors can find things. The number prefix (`058-pikachu.yml`) is navigation, not identity — renaming a file changes nothing about the data. If two records derive the same ID the build **fails and names both files**, rather than silently overwriting one.

### `origin` on oracles

Thousands of cards are named "Pikachu", so a name alone cannot identify an oracle. `origin` anchors it to the printing the card first appeared in (`base-058`). It is anchored to the *earliest* printing so that adding reprints never changes an existing oracle's ID.

### Oracle IDs vs card IDs

The two ID shapes answer different questions, and both are needed:

| | identifies | shape | example |
| --- | --- | --- | --- |
| **Oracle** | a set of mechanics, shared by every printing of it | `name` + `origin` | `pikachu-base-058` |
| **Card** | one specific printing | `set` + `index` | `base-058` |

An oracle answers *"what does this card do?"* — it is what you reach for when two printings are the same card. A card answers *"which printing is this?"* — its artist, rarity, set and collector number.

**Card IDs are not merely internal plumbing.** Deck lists reference them, because a decklist has to name a specific printing rather than a set of mechanics:

```yaml
highlight: breakpoint-040     # Greninja

list:
  main:
    breakpoint-040: 2         # Greninja, from BREAKpoint
    xy-123: 2                 # Professor's Letter, from XY
    roaring-skies-094: 1      # Wally, from Roaring Skies
```

A theme deck draws from several sets at once, and `xy-123` names exactly one card. Pointing at the oracle instead would say "some Professor's Letter" — true, but not what shipped in the box, and not enough to reproduce the product.

This is why a card ID has to stay stable, and why the build refuses to let two cards derive the same one.

<br>

## 📇 Card `index`

`index` is the printed collector number, normalized so it sorts correctly and stays unique within its set:

- Strip any letter prefix and zero-pad to three digits — `SM01` → `001`, `GG01` → `001`
- Keep a trailing letter — `SM30a` → `030a`, `28a` → `028a`
- If stripping the prefix would collide with another card in the same set, the prefixed card re-attaches its prefix — `001` and `gg01` become `001` and `001gg`
- Cards numbered with letters keep them — Unown `A` → `a`, Alph Lithograph `ONE` → `one`

<br>

## 🎴 What Counts as a Set

**A set is a group of cards sharing a set-mark and its own numbering sequence — not a retail product.** Two cards belong to the same set when their collector numbers run in one continuous series. How they were sold is irrelevant.

This matters because retail packaging and card numbering do not line up:

**One product, several sets.** *Crown Zenith* shipped as a single product, but its cards are numbered in two independent runs — `1/159` through `160/159`, and `GG01/GG70` through `GG70/GG70`. Those are two sets here:

```
data/set/standard/11-sword-shield/…/crown-zenith.yml                 160 cards
data/set/standard/11-sword-shield/…/crown-zenith-galarian-gallery.yml 70 cards
```

The same applies to every Trainer Gallery (`TG01`–`TG30`), the *Hidden Fates* and *Shining Fates* Shiny Vaults (`SV01`–`SV94`), and the *Celebrations Classic Collection*.

**One product, split in two.** A Trainer Kit box contains two decks, each with its own numbering starting at 1. So *XY Trainer Kit — Bisharp & Wigglytuff* is two sets, `xy-trainer-kit-bisharp` and `xy-trainer-kit-wigglytuff`. Official set lists usually show it as one entry; ours shows two.

### Why the rule is load-bearing

Card `index` strips the letter prefix (see above), so Galarian Gallery's `GG01` normalizes to `001` — byte-identical to Crown Zenith's own `001`. Card IDs are `set` + `index`, so keeping them in one set would make `crown-zenith-001` ambiguous between two different cards. The build would reject it as a duplicate ID rather than silently drop one.

So the set boundary is not cosmetic: it is what makes the numbering unambiguous. **If you are unsure whether something is one set or two, look at whether the collector numbers restart.** If they do, it is two sets.

<br>

## 🧬 Curation Decisions

The source data these files were built from disagreed with itself in places. Where a judgement call was made, it is recorded here. **Please do not "correct" these back without raising it on Discord first** — each one is deliberate.

### Conflicting values between printings

Cards that are mechanically identical sometimes carried different values for a field that cannot vary between printings. In each case one printing was chosen as correct:

| Oracle | Field | Chosen | Rejected |
| --- | --- | --- | --- |
| Dark Vileplume | weakness | `Fire ×2` | The non-holo Team Rocket printing said `Fighting ×2`; holo and non-holo of one card cannot differ. |
| Electrike | weakness | `Fighting ×2` | The Arceus printing said `Fighting +10`, the Platinum-era additive format, against `×2` on its three later printings. |
| Entei & Raikou LEGEND | weakness | `Water ×2` + `Fighting ×2` | This card prints as two halves; the top half recorded only one of the two weaknesses. |
| Kirlia | resistance | `Fighting -30` | The McDonald's Collection 2023 promo said `Psychic -30` against `Fighting -30` on all four Scarlet & Violet printings. |
| Floette | preevolution | `Flabébé` | A promo printing dropped the accents. |
| Kakuna | preevolution | `Weedle` | The Base Set printing listed Kakuna as its own pre-evolution. |

### Oracle merging

Reprints are collapsed into a single oracle when they share every mechanic — name, HP, subtypes, attack names, energy costs, damage. **Wording differences do not create a new oracle.** Official text was reworded across eras (often to clarify early translations), and those variants belong in `errata`, not in a duplicate oracle.

Five cards are the exception. They share a name, HP, attack name and cost, but their effects genuinely differ, so they are kept as separate oracles:

- **Unown** — the `ex10` set gives Unown A–Z one shared attack name with a different effect per letter
- **Pikachu-EX** — one printing flips coins for `30×`, the other discards all Lightning for `50×`
- **Metapod** — one printing prevents all damage, the other reduces damage by 40
- **Blastoise** — Base-era Hydro Pump wordings
- **Bulbasaur** — Base-era Leech Seed wordings

### `regulation` is a list

A card's regulation mark belongs to its printing, not its mechanics — `Energy Switch` has been printed under `D`, `F`, `G` and `I`. The oracle carries every mark it has ever been printed under, because a player may use any printing whose mark is legal in the current format.

### Collection grouping

Upstream reported a flat list of series with no grouping of its own, so collections are grouped here:

- **Gym** is part of the **Base** collection. Sources disagree on whether it is a separate era; this dataset treats it as part of the original Wizards run.
- **Other** and **POP** are collection type `extra`, not `standard`. They are promo and one-off distributions rather than main-line expansions.
- **McDonald** holds all twelve *McDonald's Collection* sets (2011–2024), split out of `Other` so the annual promo run reads as one series.
- **Classic** holds the three *Pokémon TCG Classic* decks (Blastoise, Charizard, Venusaur), split out of `Other` for the same reason.
- **Black Star** holds all ten Black Star promo sets, from *Wizards* (1999) to *Mega Evolution* (2025). They were previously scattered across nine era collections, one apiece.
- **Trainer Kit** holds all twenty-one Trainer Kit sets, likewise pulled out of the era collections they shipped under.

`Other` is now genuinely miscellaneous — Miscellaneous, Southern Islands, Legendary Collection, Best of Game, Poké Card Creator Pack, Pokémon Rumble and Pokémon Futsal Collection.

There is no longer an **NP** collection. *Nintendo Black Star Promos* was its only member, so gathering the promos dissolved it.

The **Kalos Starter Set** is in `Trainer Kit` despite its name. It is the same product type as the kits either side of it; only the English naming differs.

Collection `index` is numbered within its own type, so `standard` and `extra` each start at `01`. Moving a collection between types renumbers only that type.

### Set naming

Two conventions apply to the gathered collections, both to stop the same product line being spelled several ways:

**No `Promos` suffix.** Sets are *Wizards Black Star*, not *Wizards Black Star Promos*. Sources disagree on whether the word is singular or plural, and there is no official convention to appeal to, so the dataset drops it rather than picking a side.

**Era names in full, not abbreviated.** Upstream mixes both forms; this dataset always spells the era out:

| upstream | here |
| --- | --- |
| `DP` | Diamond & Pearl |
| `HGSS` | HeartGold & SoulSilver |
| `BW` | Black & White |
| `SM` | Sun & Moon |
| `SWSH` | Sword & Shield |

`EX` and `XY` are left as they are — those *are* the era names in full. The same rule retired the `HS—` prefix from the HeartGold & SoulSilver main-line sets, which are simply *Unleashed*, *Undaunted* and *Triumphant*.

### Individual card fixes

- **Ancient Mew** (`Miscellaneous`) — the source gave its number as the literal string `None`; it is `001`, the only card in that set.
- **Celebrations Classic Collection** — four cards share the printed number `15`, because Celebrations reprints keep the number of the set they originally came from. They are disambiguated as `015a1`–`015a4`.
- **Unown `!` and `?`** — stored as `exclamation` and `question`, since punctuation cannot survive an ID or a filename.
- **Costless attacks** — a handful of attacks were marked with a `Free` pseudo-energy. They carry no `cost` at all.
