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
| Collections | 16 |

<br>

## 🕸️ Structure

During the build process, the compilation script merges the project's individual YAML files into flat, fully-realized JSON objects.

- `data/card/`: **Physical Printings.** Properties specific to an exact card (artist, flavor text, rarity, collector number).<br>

- `data/oracle/`: **Consistent Properties.** The card's core mechanics, identical across all reprints (HP, attacks, abilities, weakness, retreat).<br>

- `data/set/`: **Release Data.** Cards inherit set properties during build. A set is a group of cards sharing a set-mark and numbering sequence, *not* a retail product — so one product may hold several sets ([why](CONTRIBUTING.md#-what-counts-as-a-set)).<br>

- `data/collection/`: **Macro-Groupings.** Broader buckets (eras such as *Neo* or *Scarlet & Violet*) that group multiple sets together.<br>

- `data/format/`: **Card Legality.** Standalone rules defining allowed sets, and specific card bans/restrictions.<br>

- `data/deck/`: **Pre-constructed Lists.** Official product decklists (Theme Decks, Battle Decks) mapping card IDs to quantities — a *specific printing*, not just an oracle ([why](CONTRIBUTING.md#oracle-ids-vs-card-ids)).<br>

- `schema/`: **Validation Blueprints.** Strict Schemas to automatically validate contributions.<br>

- `script/`: **Build Pipeline.** Python utilities that compile the individual YAML files into final distribution formats.<br>

- `dist/`: **Distribution Directory.** The final, compiled files. *(Note: This folder is git-ignored. Editors not running the build script locally can instead access these files from the Releases page).*

<br>

### Folder cascade

Cards, oracles and sets all nest the same way, so the path tells you where a card sits in the release history:

```
data/card/standard/01-base/01-base/058-pikachu.yml
          └ type   └ collection
                             └ set   └ card

data/oracle/standard/01-base/01-base/058-pikachu.yml
data/set/standard/01-base/01-base.yml
data/collection/01-base.yml
```

Collection type is the top level — `standard` for main-line expansions, `extra` for promo and one-off distributions. Number prefixes order each level chronologically and exist purely to help editors navigate; **they are not part of any ID**.

Cross-references are written as human-readable names (`set: Base`, `collection: Neo`) and every ID is derived at build time. See [CONTRIBUTING](CONTRIBUTING.md#-how-ids-work) before adding records.

<br>


## 🐍 Scripts

- `python script/compile.py`: Validates every source YAML against `schema/`, checks that all cross-references resolve, and writes the joined JSON to `dist/`. **This is the build** — edit YAML, run this, done.<br>

- `python script/split.py`: Re-generates `data/card`, `data/oracle`, `data/set` and `data/collection` from the compiled JSON — the exact inverse of `compile.py`. Useful for bulk structural changes and for normalising formatting. `data/format` and `data/deck` are hand-authored and are never touched.<br>

<br>
  

## 🐝 Community & Contributing

This dataset relies on community contributions to stay accurate and up-to-date. You are invited to contribute if you spot a missing card, a typo in rules text, incorrect set data, etc.
  
*   **[Join Discord](https://chat.cardcarp.com):** Discuss structure and data accuracy.

<br>

## 🪩 Featured Apps

Here are a few projects currently using this dataset in production. (*If you have built an app, simulator, or tool using this data, please share on Discord!*)

*   **[CardCarp](https://cardcarp.com)** - A companion web-app to showcase all cards. 

<br>  
  

## 🍥 Support the Project

If you found this dataset useful and want to help keep it updated, you can support the project below.

*   **[Buy Me a Coffee Page](https://patronage.cardcarp.com)**

  
<br>    
  
## ⚖️ Legal Disclaimer

<sub>This is an independent, community-driven project and is not affiliated with, endorsed by, sponsored by, or connected to any publisher or intellectual property owner.</sub>

<sub>Card data and images are strictly for educational study, historical preservation, and personal, non-commercial use.</sub>

<sub>All trademarks, copyrights, and artwork remain the exclusive property of their respective rights holders.</sub>

<sub>No challenge to any intellectual property rights is intended, nor is there intent to compete with sales or commercial distributions of these intellectual properties.</sub>
