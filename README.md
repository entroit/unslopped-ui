# unslopped-ui

An agent skill for clearer, more useful interfaces. Improve hierarchy, typography, data displays and interaction while preserving the product's brand and working behavior.

## Install

Run this from your project:

```sh
npx skills add entroit/unslopped-ui --skill unslopped-ui
```

Choose your coding agent when prompted. Keep the complete skill folder together.

## Use

Give your agent the interface and a concrete brief:

```text
Use $unslopped-ui to improve this dashboard. Keep our brand, data and working controls.
```

The skill inspects the existing product, reads the relevant guidance, makes the requested changes and checks the rendered result. A font, color or visual effect is judged by how it serves the interface.

## What's included

- A short [SKILL.md](skills/unslopped-ui/SKILL.md) entry point.
- Seven focused references for app screens, marketing, visual details, interaction, verification, demonstrations and catalog lookup.
- A compressed catalog of 5,816 design records, including 50 themes, 141 styles and 160 brand examples.
- A lookup script that uses Python 3 with no extra packages. Python is needed only for catalog lookup.

From the installed skill folder:

```sh
python3 scripts/catalog.py search "dense table" --limit 3
python3 scripts/catalog.py show hallmark-theme-almanac
```

The agent reads selected records when they help the task. The catalog stays out of its context otherwise.

## Development

```sh
python3 -m unittest discover -s tests
```

## License

[MIT](LICENSE) for the original instructions and code. Bundled reference material retains its license notices in `skills/unslopped-ui/licenses/`.
