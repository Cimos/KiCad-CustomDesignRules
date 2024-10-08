# KiCad-Custom-Design-Rules

Forked From [KiCad-DesignRules](https://github.com/labtroll/KiCad-DesignRules) due to lack of activity and renamed to "KiCad-Custom-Design-Rules".

JLCPCB Design Rules for KiCad 8.0, implemented as Custom Rules in PCB Editor (`File > Board_Setup... > Design Rules > Custom Rules`), and stored in the `.kicad_dru` file.

These rules use some features only available in KiCad 7.0.

Each design rule is validated for PASS/FAIL the associated PCB (`.kicad_pcb`).

## Use in your KiCad 8 project

Simply copy the [`JLCPCB.kicad_dru`](JLCPCB/JLCPCB.kicad_dru) file into your KiCad 7 project folder, and rename it to match your project name `your-project.kicad_dru`.

The JLCPCB Design Rules will automatically be included in the KiCad PCB Editor (`File`>`Board Setup...`>`Design Rules`>`Custom Rules`), and be included when performing a [Design Rules Check (DRC)](https://docs.kicad.org/8.0/en/pcbnew/pcbnew.html#design_rule_checking) (`Inspect`>`Design Rules Checker`).

## JLCPCB documentation

- [PCB Manufacturing & Assembly Capabilities](https://jlcpcb.com/capabilities/pcb-capabilities)

## KiCAD documentation

- [Custom Design Rules (KiCad 8.0)](https://docs.kicad.org/8.0/en/pcbnew/pcbnew.html#custom-design-rules)
