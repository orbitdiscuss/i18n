#!/usr/bin/env python3
"""Checks every translations/<code>.json against translations/en.json.

    python3 scripts/check.py            # errors fail, warnings are printed
    python3 scripts/check.py --status   # coverage table (Markdown)
    python3 scripts/check.py --readme   # rewrite the status table in README.md

Errors: invalid JSON, unknown sections or keys, placeholders that differ from English,
unknown plural forms, wrong text direction, bidi control characters, new HTML tags.
Warnings: untranslated strings, translations much longer than English.
Python standard library only.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "translations"
SECTIONS = ("web", "mobile", "system")
PLURALS = ("zero", "one", "two", "few", "many", "other")
PLURAL = re.compile(r"^(.+)_(" + "|".join(PLURALS) + r")$")
RTL = {"ar", "fa", "he", "ur", "ps", "sd", "yi", "dv", "ckb", "ug"}
WEB_VAR = re.compile(r"\{(\w+)\}")
PRINTF = re.compile(r"%(?:(\d+)\$)?([-+ 0#]*\d*(?:\.\d+)?(?:hh|h|ll|l|q|z|t|j)?[@dDiuUxXoOfeEgGcCsSpaA%])")
OVERRIDE = re.compile("[\u202a-\u202e]")  # embeddings and overrides; isolates (U+2066-2069) are fine when balanced
TAG = re.compile(r"</?([a-zA-Z][\w-]*)[^>]*>")
CODE = re.compile(r"^[a-z]{2,3}(-[A-Z]{2}|-[A-Z][a-z]{3})?$")

errors, warnings = [], []


def err(f, msg):
    errors.append(f"{f}: {msg}")


def warn(f, msg):
    warnings.append(f"{f}: {msg}")


def balanced_isolates(text):
    depth = 0
    for ch in text:
        if ch in "\u2066\u2067\u2068":
            depth += 1
        elif ch == "\u2069":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def placeholders(section, text):
    if section == "web":
        return Counter(WEB_VAR.findall(text))
    out = Counter()
    for _, spec in PRINTF.findall(text):
        if spec != "%":
            out[re.sub(r"[-+ 0#\d.]", "", spec).replace("q", "ll")] += 1
    return out


def load(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        err(path.name, f"not valid JSON ({e})")
        return None
    if not isinstance(data, dict):
        err(path.name, "must be a JSON object")
        return None
    return data


def group(en_section, key):
    """English forms that a key (or a plural form of it) belongs to."""
    m = PLURAL.match(key)
    base = m.group(1) if m else key
    forms = [k for k in (base, *(f"{base}_{c}" for c in PLURALS)) if k in en_section]
    return base, forms


def check_lang(path, en):
    name = path.name
    code = path.stem
    data = load(path)
    if data is None:
        return None
    if not CODE.match(code):
        err(name, "file name must be a language code like 'tr' or 'pt-BR'")
    meta = data.get("_meta")
    if not isinstance(meta, dict) or not all(isinstance(meta.get(k), str) and meta.get(k) for k in ("name", "english", "dir")):
        err(name, '"_meta" needs "name" (in the language), "english" (English name) and "dir" ("ltr" or "rtl")')
    elif meta["dir"] != ("rtl" if code.split("-")[0] in RTL else "ltr"):
        err(name, f'"_meta.dir" should be "{"rtl" if code.split("-")[0] in RTL else "ltr"}"')
    for k in data:
        if k not in SECTIONS and k != "_meta":
            err(name, f"unknown section {k!r} (expected {', '.join(SECTIONS)})")
    for s in SECTIONS:
        table = data.get(s, {})
        if not isinstance(table, dict):
            err(name, f'"{s}" must be an object')
            continue
        for key, value in table.items():
            where = f"{s} {key!r}"
            if not isinstance(value, str):
                err(name, f"{where}: value must be a string")
                continue
            base, forms = group(en[s], key)
            if key not in en[s]:
                if not (PLURAL.match(key) and forms):
                    err(name, f"{where}: not in en.json (removed or misspelled key?)")
                    continue
            if not value.strip():
                continue
            if OVERRIDE.search(value) or not balanced_isolates(value):
                err(name, f"{where}: invisible direction characters must be balanced isolates (U+2066-2068 ... U+2069)")
            english = [en[s][f] for f in forms] or [en[s].get(key, "")]
            mine = placeholders(s, value)
            if len(forms) > 1 or PLURAL.match(key):
                allowed = Counter()
                for e in english:
                    allowed |= placeholders(s, e)
                extra = mine - allowed
                if extra:
                    err(name, f"{where}: placeholder {', '.join(extra)} is not in the English text")
            elif mine != placeholders(s, english[0]):
                want = ", ".join(sorted(placeholders(s, english[0]).elements())) or "none"
                err(name, f"{where}: placeholders must match English ({want})")
            if s == "mobile" and sum(1 for p, _ in PRINTF.findall(value) if p) not in (0, sum(mine.values())):
                err(name, f"{where}: either number every placeholder (%1$@, %2$@) or none")
            new_tags = set(TAG.findall(value)) - set(t for e in english for t in TAG.findall(e))
            if new_tags:
                err(name, f"{where}: HTML tags not in English: {', '.join(sorted(new_tags))}")
            if len(english[0]) >= 12 and len(value) > 3 * len(english[0]) + 20:
                warn(name, f"{where}: much longer than English, it may not fit")
    return data


def coverage(en, data):
    total = sum(len(en[s]) for s in SECTIONS)
    done = sum(1 for s in SECTIONS for k in en[s] if str((data.get(s) or {}).get(k, "")).strip())
    return done, total


def status_table(en, langs):
    rows = ["| Language | Code | Translated | Progress |", "| --- | --- | --- | --- |"]
    for code, data in sorted(langs.items(), key=lambda x: -coverage(en, x[1])[0]):
        done, total = coverage(en, data)
        pct = 100 * done // total
        meta = data.get("_meta") or {}
        label = "in the apps" if meta.get("live") is True else "ready to turn on" if pct >= 90 else "in progress"
        rows.append(f"| {meta.get('english', code)} ({meta.get('name', code)}) | `{code}` | {done} / {total} ({pct}%) | {label} |")
    return "\n".join(rows)


def main():
    en = load(DIR / "en.json")
    if en is None:
        sys.exit("\n".join(errors))
    langs = {}
    for path in sorted(DIR.glob("*.json")):
        if path.stem != "en":
            data = check_lang(path, en)
            if data is not None:
                langs[path.stem] = data
    for p in DIR.iterdir():
        if p.suffix != ".json":
            err(p.name, "only <code>.json files belong in translations/")
    if "--status" in sys.argv or "--readme" in sys.argv:
        table = status_table(en, langs)
        if "--readme" in sys.argv:
            readme = ROOT / "README.md"
            text = readme.read_text(encoding="utf-8")
            new = re.sub(r"(<!-- status:start -->).*?(<!-- status:end -->)", lambda m: f"{m.group(1)}\n{table}\n{m.group(2)}", text, flags=re.S)
            if new != text:
                readme.write_text(new, encoding="utf-8")
        else:
            print(table)
        return
    for code, data in langs.items():
        done, total = coverage(en, data)
        if done < total:
            warnings.append(f"{code}.json: {total - done} of {total} strings not translated yet")
    for w in warnings:
        print(f"::warning::{w}" if "GITHUB_ACTIONS" in __import__("os").environ else f"warning: {w}")
    for e in errors:
        print(f"::error::{e}" if "GITHUB_ACTIONS" in __import__("os").environ else f"error: {e}")
    print(f"{len(langs) + 1} languages checked: {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
