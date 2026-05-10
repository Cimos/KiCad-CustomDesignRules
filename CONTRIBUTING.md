# Contributing

Thanks for taking the time to contribute. This repo is small but used by a lot of KiCad projects, so please read the conventions below before opening a PR.

## Supported KiCad version

KiCad 8.0 and later. Rules use features that don't exist in KiCad 7.

## Adding or updating a rule

Every rule must be backed by a specific, citable line in the fab's published capabilities. Drive-by tweaks based on personal experience belong in your own project, not here.

1. **Find the source.** Locate the exact entry in the fab's capabilities page or design rules document.
   - JLCPCB: https://jlcpcb.com/capabilities/pcb-capabilities
   - PCBWay: https://www.pcbway.com/capabilities.html
2. **Add the rule** to the relevant `<FAB>/<FAB>.kicad_dru` file.
3. **Name it** using the `FAB: Rule Name` convention, e.g. `JLCPCB: Trace Width (Outer Layer)`. The prefix matters — it makes DRC output readable when a project includes rules from multiple sources.
4. **Comment the source** above the rule. Include the URL and the literal value(s) from the page so future reviewers can verify against capability changes. Example:
   ```
   # JLCPCB: outer layer trace width >=3.5mil for 4-6 layer 1oz/0.5oz
   # https://jlcpcb.com/capabilities/pcb-capabilities
   (rule "JLCPCB: Trace Width (Outer Layer)"
       ...
   )
   ```
5. **Add a test footprint** to `<FAB>/<FAB>.kicad_pcb` that exercises the rule (one footprint that should pass, optionally one that should fail). Run DRC and confirm the result matches.
6. **Scope conditions tightly.** A rule like `(condition "A.Pad_Type == 'SMD'")` matches every SMD pad on the board — usually not what you want. Prefer net classes, footprint properties, or pad-size thresholds when targeting a specific device class.

## Reporting capability changes

If a fab updates their published spec, open an issue with the link, the old value, and the new value. Don't open a PR until the change is confirmed against the source.

## PR checklist

- [ ] Rule name uses the `FAB: Rule Name` convention
- [ ] Source link and quoted value in a comment above the rule
- [ ] Test footprint added to the relevant `.kicad_pcb`
- [ ] DRC run locally on the test PCB and result is as expected
- [ ] Condition is scoped to only the intended objects
