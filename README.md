# KiCad Custom Design Rules

Custom design rules for KiCad 8 that match the manufacturing capabilities of common PCB fab houses. Rules are stored in `.kicad_dru` files and validated against a paired test board (`.kicad_pcb`) so each rule has at least one footprint that passes or fails as expected.

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

## KiCad documentation

- [Custom Design Rules (8.0)](https://docs.kicad.org/8.0/en/pcbnew/pcbnew.html#custom-design-rules)
- [Design Rules Check (8.0)](https://docs.kicad.org/8.0/en/pcbnew/pcbnew.html#design_rule_checking)

## Contributing

Bug reports, capability updates, and PRs are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the conventions used in this repo.

## License

[MIT](LICENSE)
