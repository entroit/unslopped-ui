# Catalog lookup

Read this when a named theme, style, brand example, measured layout or detector rule can resolve a design decision. The archive is optional reference data. Current `SKILL.md` and focused references govern its use.

Run these commands from the skill directory, or invoke the script by its full path. The script finds its data relative to its own location and requires only Python 3.

```sh
python3 scripts/catalog.py search "contrast gradient" --limit 3
python3 scripts/catalog.py search "Almanac" --source hallmark --kind theme
python3 scripts/catalog.py show hallmark-theme-almanac
python3 scripts/catalog.py show ux-brand-zara --chars 2000
python3 scripts/catalog.py show ux-001
```

Search results give IDs, excerpts, source groups, record kinds, heading paths and original line locations. Choose the record that fits the task, then use `show` for its full content. For details beyond a theme's short recipe, search its name within the same source without restricting the record kind.

`search` and `list` default to six results and accept at most twenty. Use their JSON `next_offset` with `--offset` to continue. `show` defaults to 6,000 characters and allows at most 12,000 per response. If its `next_offset` is non-null, continue from that character offset to finish the record.

```sh
python3 scripts/catalog.py list --source ux --kind style --limit 6 --offset 6
python3 scripts/catalog.py show ux-brand-zara --offset 2000 --chars 6000
python3 scripts/catalog.py info
```

Read the selected recipe's conditions and source limitations along with its values. Treat historical comparisons, documented defects and rejected examples according to their context. A detector threshold describes its implementation, not the minimum size or quality a product should target. Reconstructed brand records need verification against the current official identity before a brand-specific implementation.

An unknown ID or invalid bound produces a JSON error and exit status 2. An empty search result means no match for that query; it is not evidence that the archive has no relevant guidance.

`python3 scripts/catalog.py check` verifies the catalog hash, record count and unique IDs. This checks integrity, not design quality. The catalog is compressed in `data/records.jsonl.gz`; the script reads it directly. Retrieve selected records instead of loading the complete catalog into context.
