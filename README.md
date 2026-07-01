# KiCad Custom Design Rules

Custom design rules for KiCad that match the manufacturing capabilities of common PCB fab houses. Rules are stored in `.kicad_dru` files and validated against a paired test board (`.kicad_pcb`) so each rule has at least one footprint that passes or fails as expected.

The rules are authored against the KiCad 8 custom-rules syntax and are forward-compatible with **KiCad 9 and 10** — every token used here is unchanged across those releases (KiCad 9/10 only add new constraints on top). If you're on KiCad 8, 9, or 10, they just work.

> Maintained fork of [labtroll/KiCad-DesignRules](https://github.com/labtroll/KiCad-DesignRules), which has been inactive since November 2024.

## Supported fabs

| Fab    | Folder                | Source of capabilities                            |
|--------|-----------------------|---------------------------------------------------|
| JLCPCB | [`JLCPCB/`](JLCPCB/)  | https://jlcpcb.com/capabilities/pcb-capabilities  |
| PCBWay | [`PCBWay/`](PCBWay/)  | https://www.pcbway.com/capabilities.html          |

Each folder contains:

- `<FAB>.kicad_dru` — the rule file you copy into your project
- `<FAB>.kicad_pcb`, `.kicad_sch`, `.kicad_pro` — a small test board exercising the rules

## Use in your project

1. Copy the relevant `.kicad_dru` from `JLCPCB/` or `PCBWay/` into your KiCad project folder.
2. Rename it to match your project: `your-project.kicad_dru`.
3. KiCad picks it up automatically. View under `File > Board Setup > Design Rules > Custom Rules`.
4. Run `Inspect > Design Rules Checker` (or press F8) to apply.

Many rules have alternates commented out for different layer counts or copper weights. Read the comments at the top of each rule and uncomment the variant that matches what you're ordering.

## Validation

Every `.kicad_dru` file is checked in CI by a small linter (`tools/lint_dru.py`, no dependencies) that catches malformed s-expressions, missing `(version 1)` headers, rules with no constraint, duplicate names, wrong fab prefixes, and lowercase item-type literals (`'track'`/`'via'`/`'pad'`) that KiCad silently never matches. Run it locally with:

```
python3 tools/lint_dru.py
```

The linter is a fast syntax/consistency gate — KiCad has no standalone `.kicad_dru` validator. For a full electrical DRC, KiCad 8+ can run the rules headlessly against the paired test board:

```
kicad-cli pcb drc --exit-code-violations --severity-error JLCPCB/JLCPCB.kicad_pcb
```

## KiCad documentation

- [Custom Design Rules (8.0)](https://docs.kicad.org/8.0/en/pcbnew/pcbnew.html#custom-design-rules) — the syntax these rules are written against
- [Design Rules Check (8.0)](https://docs.kicad.org/8.0/en/pcbnew/pcbnew.html#design_rule_checking)
- [KiCad CLI reference](https://docs.kicad.org/en/cli/cli.html) — `kicad-cli pcb drc` for headless checking

## Contributing

Bug reports, capability updates, and PRs are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the conventions used in this repo.

## License

[MIT](LICENSE)
