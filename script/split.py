import json
import os
import shutil

from part.util import to_kebab_case, save_yml, load_schema_order, order_by_schema

# The only trees this script owns. data/format and data/deck are deliberately
# excluded: both are hand-authored, both carry comments and block scalars that a
# JSON round-trip would flatten, and neither is large enough for a bulk edit to
# be worth that risk. They are never read, rewritten, or deleted here.
OWNED_DIRS = ('data/oracle', 'data/collection', 'data/set', 'data/card')

REQUIRED_INPUTS = ('dist/collection.json', 'dist/set.json', 'dist/oracle.json', 'dist/card.json')


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def split_json_to_yml():
    # Split /dist JSONs back into individual YAMLs. This is the exact inverse of
    # compile.py: ids are dropped and every cross-reference is written back as
    # the human-readable name it was derived from.

    missing = [path for path in REQUIRED_INPUTS if not os.path.exists(path)]
    if missing:
        print("Error: cannot split without a complete build. Missing:")
        for path in missing:
            print(f"  - {path}")
        return

    collections = load_json('dist/collection.json')
    sets = load_json('dist/set.json')
    oracles = load_json('dist/oracle.json')
    cards = load_json('dist/card.json')

    print("Cleaning up old data...")
    for folder in OWNED_DIRS:
        # Clear previous YAMLs and folders to avoid orphaned content
        shutil.rmtree(folder, ignore_errors=True)
    os.makedirs('data', exist_ok=True)

    print("Starting decomposition...")

    # --- Folder cascade: collection_type / collection / set ------------------
    def collection_folder(collection_id):
        record = collections[collection_id]
        return f"{int(record['index']):02d}-{to_kebab_case(record['name'])}"

    def set_folder(set_id):
        record = sets[set_id]
        return f"{int(record['index']):02d}-{to_kebab_case(record['name'])}"

    def set_path(set_id):
        collection_id = sets[set_id]['collection_id']
        return (f"{to_kebab_case(collections[collection_id]['type'])}"
                f"/{collection_folder(collection_id)}"
                f"/{set_folder(set_id)}")

    collection_order = load_schema_order('collection')
    set_order = load_schema_order('set')
    oracle_order = load_schema_order('oracle')
    card_order = load_schema_order('card')

    # --- 1. Collections ------------------------------------------------------
    for collection_id, record in collections.items():
        save_yml(f"data/collection/{collection_folder(collection_id)}.yml",
                 order_by_schema(dict(record), collection_order))
    print(f"Finished collections. Total: {len(collections)}")

    # --- 2. Sets: collection_id becomes the collection's name ----------------
    for set_id, record in sets.items():
        entry = dict(record)
        entry['collection'] = collections[entry.pop('collection_id')]['name']
        save_yml(f"data/set/{set_path(set_id)}.yml", order_by_schema(entry, set_order))
    print(f"Finished sets. Total: {len(sets)}")

    # --- 3. Oracles ----------------------------------------------------------
    # An oracle's `origin` is the card id of its earliest printing, so that card
    # gives both the set it belongs in and the index its filename starts with.
    for oracle_id, record in oracles.items():
        origin = cards[record['origin']]
        filename = f"{origin['card_index']}-{to_kebab_case(record['name'])}.yml"
        save_yml(f"data/oracle/{set_path(origin['set_id'])}/{filename}",
                 order_by_schema(dict(record), oracle_order))
    print(f"Finished oracles. Total: {len(oracles)}")

    # --- 4. Cards ------------------------------------------------------------
    # Cards carry no name of their own; it lives on the oracle they point at.
    for card_id, record in cards.items():
        entry = dict(record)
        oracle_id = entry.pop('oracle_id')
        oracle = oracles[oracle_id]
        set_id = entry.pop('set_id')

        # Oracle ids are already kebab-case, so the reference is the id itself
        entry['oracle'] = oracle_id
        entry['set'] = sets[set_id]['name']
        entry['index'] = entry.pop('card_index')

        filename = f"{entry['index']}-{to_kebab_case(oracle['name'])}.yml"
        save_yml(f"data/card/{set_path(set_id)}/{filename}",
                 order_by_schema(entry, card_order))
    print(f"Finished cards. Total: {len(cards)}")


if __name__ == "__main__":
    split_json_to_yml()
