# Pokémon TCG Card Dataset ⚡️

A flat-file dataset for the Pokémon Trading Card Game.

<br>

> [!IMPORTANT]
> Every card printing and card oracle has its own file, and core game properties are filled in.<br>
> This dataset is maintained by hand. It is not synced with any upstream API.<br>
> Editors are actively working on this data and welcome community contributions.

<br>

## 🚀 Quick Start

You need Python 3.10 or newer.

```bash
git clone https://github.com/cardcarp/ptcg.git
cd ptcg
pip install .
cardcarp-compile
```

The compiled dataset is written to `dist/`. `dist/database.json` has every printing joined with its oracle, set, collection and format legality.

This repo contains only data and schemas. The build comes from [cardcarp/compile](https://github.com/cardcarp/compile), a pipeline shared by the CardCarp datasets, and `pip install .` installs it.

<br>

## 🕸️ Structure

The build combines the repo's individual YAML files into flat JSON records.

| Folder | Holds |
| --- | --- |
| `data/card/` | **Physical printings.** Properties of one exact card: artist, flavor text, rarity, collector number and regulation mark |
| `data/oracle/` | **Rules shared by every reprint.** HP, attacks, abilities, weakness and retreat cost |
| `data/set/` | **Release data.** A group of cards sharing a set mark and number sequence, *not* a retail product, so one product can hold several sets ([why](CONTRIBUTING.md#-what-counts-as-a-set)) |
| `data/collection/` | **Larger groupings.** Eras such as *Neo* or *Scarlet & Violet*, each grouping several sets |
| `data/format/` | **Card legality.** Allowed sets and regulation marks, plus bans and restrictions for specific cards |
| `data/deck/` | **Pre-constructed lists.** Official decklists (Theme Decks, Battle Decks). Each entry points to a *specific printing*, not just an oracle ([why](CONTRIBUTING.md#oracle-ids-vs-card-ids)) |
| `schema/` | **Validation rules.** One schema per record type, plus `dataset.yml`, the Pokémon-specific vocabulary the shared build needs |
| `dist/` | **Build output.** Git-ignored. Run `cardcarp-compile` to produce it |

<br>

### Folder cascade

Cards, oracles and sets all nest the same way, so a file's path shows where the card sits in the release history:

```
data/card/standard/01-base/01-base/058-pikachu.yml
└ type
    └ collection
        └ set
            └ card

data/oracle/standard/01-base/01-base/058-pikachu.yml
data/set/standard/01-base/01-base.yml
data/collection/01-base.yml
```

Collection type is the top level: `standard` for main-line expansions, `extra` for promos and one-off distributions. Number prefixes put each level in release order. They only help editors find files, and **they are not part of any ID**.

Records refer to each other by readable names (`set: Base`, `collection: Neo`), and every ID is generated during the build. Read [CONTRIBUTING](CONTRIBUTING.md#-how-ids-work) before adding records.

<br>

## 🐍 Commands

Run every command from the root of this repo.

| Command | What it does |
| --- | --- |
| `cardcarp-compile` | **The build.** Validates every file, checks every reference, and writes `dist/` |
| `cardcarp-split` | Regenerates `data/card`, `data/oracle`, `data/set` and `data/collection` from `dist/`, for bulk edits and formatting cleanup |
| `cardcarp-sets` | Writes `dist/sets.json`, the tree of collection types, collections and sets |
| `cardcarp-manifest` | Writes `dist/manifest.json`, all cards and decks keyed by id |
| `cardcarp-properties` | Writes `dist/properties.json`, the distinct values available for filtering |

The [compile README](https://github.com/cardcarp/compile#-commands) covers each command in detail, including how IDs and legality are calculated.

<br>

## 🐝 Community

Found a missing card, a typo in rules text or wrong set data? Contributions are welcome. Start with [CONTRIBUTING](CONTRIBUTING.md).

- **[Join Discord](https://chat.cardcarp.com):** discuss structure and data accuracy, or share something you've built with this data.<br>
- **[CardCarp](https://cardcarp.com):** the web app built on this dataset.<br>
- **[Support the project](https://patronage.cardcarp.com):** help keep the dataset maintained.

<br>

## 📜 License

The files in this repo are released under [MIT No Attribution](LICENSE.md).

<sub>CardCarp is an independent, community-driven project. It is not affiliated with, endorsed by, or sponsored by any publisher or intellectual property owner. Card data and images are for educational study, historical preservation, and personal, non-commercial use. All trademarks, copyrights and artwork remain the property of their respective owners, and no challenge to those rights is intended.</sub>
