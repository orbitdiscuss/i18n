# Contributing

Thanks for helping bring Orbit to more people in their own language.

## Fix or finish a translation

1. Open `translations/<code>.json` (for example [translations/de.json](translations/de.json)).
2. Edit on GitHub with the pencil icon, or fork and edit locally.
3. Change only the text on the right of each `"key": "text"` pair. Keys stay exactly as they are.
4. Open a pull request. The automatic check tells you if anything needs fixing.

An empty string (`""`) means the text isn't translated yet; the apps show English there.

## Add a new language

1. Open an [Add a language](../../issues/new?template=add-language.yml) issue first, so two people don't translate the same thing.
2. Create the file:

   ```sh
   python3 scripts/new_language.py tr "Türkçe" "Turkish"
   ```

   This writes `translations/tr.json` with every English string and empty translations. Use a [language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) like `tr`, or a regional one like `pt-BR` when the region matters.
3. Translate as much as you like and open a pull request. Partial work is welcome; others can continue it.
4. Once a language reaches 90%, the Orbit team turns it on in the website and both apps, and it ships with the next release.

## Writing guidelines

- **Keep placeholders.** `{name}`, `{n}`, `%@`, `%d` and `%lld` are filled in by the app. Keep every one of them, unchanged. Move them wherever your grammar needs.
- **Reordering `%@`:** if your sentence needs the values in another order, number all of them: `%2$@ … %1$@`. Don't number only some of them.
- **Plurals:** keys ending in `_one`, `_other` (and in some languages `_zero`, `_two`, `_few`, `_many`) are the forms of one sentence for different numbers. Add the forms your language uses ([CLDR plural rules](https://www.unicode.org/cldr/charts/latest/supplemental/language_plural_rules.html)); leave out the ones it doesn't.
- **Tone:** friendly and plain, like talking to a friend. Use the informal "you" where your language has one, as the existing translations do.
- **Short labels:** buttons and tabs have little room. If the English is one word, aim for one or two.
- **Brand names:** "Orbit" stays "Orbit". For "spark", "orbit" (a community) and "aura", see `_context` in [en.json](translations/en.json), and use the same word everywhere.
- **Right-to-left languages:** set `"dir": "rtl"` in `_meta` (the helper script does this). To keep a left-to-right piece such as `@%@` intact inside RTL text, wrap it in the invisible characters U+2066 and U+2069, as the Arabic and Persian files do.
- **Don't** add HTML, emoji or text that isn't in the English source.

## English source

`translations/en.json` is exported from the apps, so changes made to it here would be overwritten. If an English string is wrong or unclear, open an issue and we'll fix it at the source.

## Check your changes locally

```sh
python3 scripts/check.py
```

It needs only Python 3. Errors must be fixed; warnings (untranslated or very long strings) are only hints.

## Please don't

- Use machine translation without reading the result. Reviewed machine output is fine; unreviewed output usually reads oddly.
- Report bugs in the apps here. Use support@orbitdiscuss.com.
- Report security vulnerabilities publicly. Email support@orbitdiscuss.com instead.

By contributing you agree that your translations are licensed under [CC BY 4.0](LICENSE).
