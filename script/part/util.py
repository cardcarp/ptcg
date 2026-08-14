import re
import os
import sys
import unicodedata

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

_dotenv_loaded = False

def load_dotenv():
    global _dotenv_loaded
    if _dotenv_loaded:
        return
    possible_paths = [
        '.env',
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    ]
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        os.environ[k.strip()] = v.strip().strip('"').strip("'")
            break
    _dotenv_loaded = True

def get_env(key, default=""):
    load_dotenv()
    return os.environ.get(key, default)

def to_kebab_case(text):
    if text is None:
        return ""

    text = str(text)

    # Remove apostrophes entirely (Lodash behavior), curly included so that
    # "Cynthia's" and "Cynthia’s" cannot kebab to different ids
    text = re.sub(r"['‘’]", "", text)

    # Transliterate accents to their base letter, so "Pokémon" becomes
    # "pokemon" rather than being split on the accented character
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))

    # No camelCase splitting: these are proper product names, not code
    # identifiers. "McDonald's" is one word, as are HeartGold and BREAKpoint.

    # Replace non-alphanumeric with hyphens
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text)

    # Normalize case and trim
    return text.lower().strip("-")

def card_dir(record):
    """Path stem for a card, relative to data/card (and any tree mirroring it).

    Takes a joined record from dist/database.json. Append '.yml' for the source
    file, or another extension for a mirrored tree.
    """
    return "/".join([
        to_kebab_case(record.get('collection_type')),
        f"{int(record['collection_index']):02d}-{to_kebab_case(record.get('collection_name'))}",
        f"{int(record['set_index']):02d}-{to_kebab_case(record.get('set_name'))}",
        f"{record.get('card_index')}-{to_kebab_case(record.get('name'))}",
    ])

def save_yml(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    yaml = YAML()
    yaml.width = sys.maxsize
    yaml.explicit_start = False

    # mapping (spaces for dicts), sequence (spaces for list items), offset (spaces before the dash)
    yaml.indent(mapping=2, sequence=4, offset=2)

    cmap = data if isinstance(data, CommentedMap) else CommentedMap(data)

    # Blank line before every top-level key except the first
    for i, key in enumerate(cmap.keys()):
        if i > 0:
            cmap.yaml_set_comment_before_after_key(key, before='\n')

    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(cmap, f)

def load_schema_order(schema_name):
    # Field order is taken from the schema file so the two never drift apart
    schema_path = f'schema/{schema_name}.yml'
    if not os.path.exists(schema_path):
        print(f"Warning: schema/{schema_name}.yml not found, leaving field order as-is.")
        return None

    yaml = YAML()
    with open(schema_path, 'r', encoding='utf-8') as f:
        return list(yaml.load(f).keys())

def order_by_schema(entry, order):
    # Keys the schema knows about come first, in schema order.
    # Anything unrecognized is kept at the end rather than dropped.
    if not order:
        return entry

    ordered = {key: entry[key] for key in order if key in entry}
    ordered.update({k: v for k, v in entry.items() if k not in order})
    return ordered
