# Pokémon TCG Card Dataset ⚡️

A flat-file dataset for the Pokémon Trading Card Game.

<br>
  
> [!IMPORTANT]
> Every card printing and card oracle has a dedicated file, and core game properties are populated.<br>
> This dataset is independently maintained — it is not synchronised with any upstream API.<br>
> Editors are actively collaborating on this data and welcome community contributions.

<br>

## 📊 Contents

| | |
| --- | --- |
| Card printings | 21,184 |
| Card oracles | 14,938 |
| Sets | 198 |
| Collections | 19 |
| Decks | 188 |
| Formats | 3 |

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

- `data/card/`: **Physical printings.** Properties specific to one exact card: artist, flavor text, rarity, collector number and regulation mark.<br>

- `data/oracle/`: **Rules shared by every reprint.** The card's core mechanics: HP, attacks, abilities, weakness and retreat cost.<br>

- `data/set/`: **Release data.** Cards take on their set's properties during the build. A set is a group of cards sharing a set mark and number sequence, *not* a retail product. One product can hold several sets ([why](CONTRIBUTING.md#-what-counts-as-a-set)).<br>

- `data/collection/`: **Larger groupings.** Eras such as *Neo* or *Scarlet & Violet*, each grouping several sets.<br>

- `data/format/`: **Card legality.** Rules for each format: allowed sets and regulation marks, plus bans and restrictions for specific cards.<br>

- `data/deck/`: **Pre-constructed lists.** Official product decklists (Theme Decks, Battle Decks) that map card IDs to quantities. Each entry points to a *specific printing*, not just an oracle ([why](CONTRIBUTING.md#oracle-ids-vs-card-ids)).<br>

- `schema/`: **Validation rules.** A strict schema for each record type, which every contribution is checked against. `schema/dataset.yml` lists the Pokémon-specific vocabulary the shared build needs.<br>

- `dist/`: **Build output.** The compiled files. This folder is git-ignored, so run `cardcarp-compile` to produce it.

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

## 🐝 Community & Contributing

This dataset relies on community contributions to stay accurate and up-to-date. If you spot a missing card, a typo in rules text or incorrect set data, please contribute. Start with [CONTRIBUTING](CONTRIBUTING.md).
  
*   **[Join Discord](https://chat.cardcarp.com):** Discuss structure and data accuracy.

<br>

## 🪩 Featured Apps

These projects use this dataset in production. (*If you have built an app, simulator, or tool using this data, please share on Discord!*)

*   **[CardCarp](https://cardcarp.com)**: a companion web app that showcases every card.

<br>  
  

## 🍥 Support the Project

If this dataset is useful to you and you'd like to help keep it updated, you can support the project here:

*   **[Buy Me a Coffee Page](https://patronage.cardcarp.com)**

  
<br>    
  
## ⚖️ Legal Disclaimer

<sub>This is an independent, community-driven project and is not affiliated with, endorsed by, sponsored by, or connected to any publisher or intellectual property owner.</sub>

<sub>Card data and images are strictly for educational study, historical preservation, and personal, non-commercial use.</sub>

<sub>All trademarks, copyrights, and artwork remain the exclusive property of their respective rights holders.</sub>

<sub>No challenge to any intellectual property rights is intended, nor is there intent to compete with sales or commercial distributions of these intellectual properties.</sub>
