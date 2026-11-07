#!/usr/bin/env python3
"""Start a new language: python3 scripts/new_language.py <code> "<name in the language>" "<English name>"

Example: python3 scripts/new_language.py tr "Türkçe" "Turkish"
Creates translations/<code>.json with every English key and empty values to fill in.
"""
import json
import re
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "translations"
RTL = {"ar", "fa", "he", "ur", "ps", "sd", "yi", "dv", "ckb", "ug"}

if len(sys.argv) != 4:
    sys.exit(__doc__)
code, name, english = sys.argv[1:]
if not re.match(r"^[a-z]{2,3}(-[A-Z]{2}|-[A-Z][a-z]{3})?$", code):
    sys.exit(f"{code!r} is not a language code like 'tr' or 'pt-BR' (see https://www.loc.gov/standards/iso639-2/php/code_list.php)")
path = DIR / f"{code}.json"
if path.exists():
    sys.exit(f"{path.name} already exists, so the language has been started. Fill in the empty strings there.")
en = json.loads((DIR / "en.json").read_text(encoding="utf-8"))
data = {"_meta": {"name": name, "english": english, "dir": "rtl" if code.split("-")[0] in RTL else "ltr"}}
for section in ("web", "mobile", "system"):
    data[section] = {key: "" for key in en[section]}
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Created translations/{code}.json with {sum(len(data[s]) for s in ('web', 'mobile', 'system'))} strings to translate.")
