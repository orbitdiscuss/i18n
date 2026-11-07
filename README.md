<p align="center">
  <img src="https://raw.githubusercontent.com/orbitdiscuss/.github/main/profile/lockup.png#gh-light-mode-only" alt="Orbit" height="56">
  <img src="https://raw.githubusercontent.com/orbitdiscuss/.github/main/profile/lockup-white.png#gh-dark-mode-only" alt="Orbit" height="56">
</p>

# Orbit translations, in the open

This repository holds every word of [Orbit](https://orbitdiscuss.com)'s interface (the website and the iPhone and Android apps) in every language we support. Anyone can fix a translation or bring Orbit to a new language. Changes merged here ship with the next release of the apps.

## Languages

<!-- status:start -->
<!-- status:end -->

English is the source. A language is turned on in the apps once it reaches 90%; strings that aren't translated yet show in English.

## How it works

| File | What it is |
| --- | --- |
| [translations/en.json](translations/en.json) | The English source. It comes straight from the apps, so please suggest English fixes in an issue. |
| `translations/<code>.json` | One file per language, with the same keys as English. An empty string means "not translated yet". |

Each file has three sections:

- **`web`**: the website at orbitdiscuss.com.
- **`mobile`**: the iPhone and Android apps (they share one set of strings).
- **`system`**: the text iOS shows when Orbit asks for permission, for example to use the camera.

Notes for tricky words (what a "spark" or an "orbit" is) are in the `_context` section of `en.json`.

## Help translate

- **Fix a translation:** open the language file, press the pencil icon on GitHub, edit the text and propose the change. That's the whole process.
- **Finish a language:** search the file for `""` and fill in what's missing.
- **Add a new language:** open an [Add a language](../../issues/new?template=add-language.yml) issue so nobody duplicates the work, then follow [CONTRIBUTING.md](CONTRIBUTING.md).

Every pull request is checked automatically: keys must match English, placeholders like `{name}` and `%@` must be kept, and right-to-left languages are set up correctly. The check tells you exactly which line to fix.

## Contributors

New here? Start with an issue labelled [good first issue](https://github.com/orbitdiscuss/i18n/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) or [translation](https://github.com/orbitdiscuss/i18n/issues?q=is%3Aissue+is%3Aopen+label%3Atranslation). Every merged contribution is credited here.

<a href="https://github.com/orbitdiscuss/i18n/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=orbitdiscuss/i18n" alt="Contributors">
</a>

## Contact

- Questions about a translation: open an issue
- General support: support@orbitdiscuss.com
- Security issues: please do not open a public issue; email support@orbitdiscuss.com

Translations in this repository are licensed under [CC BY 4.0](LICENSE); the scripts in [scripts/](scripts) are under the [MIT License](scripts/LICENSE). The Orbit name and logo are trademarks and are not covered by either license.
