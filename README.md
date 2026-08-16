# This project has moved

**➜ [github.com/Cimos/kicad-druid](https://github.com/Cimos/kicad-druid)**

Development continues there as **kicad-druid**, a standalone project. The full commit history came with it, so nothing is lost.

This repository stays up so existing links and clones keep working, and will be archived once the move has settled. It will not receive further updates.

## Why the move

This repo was a fork, and GitHub excludes forks from repository search results. People looking for KiCad design rules were consistently landing on the original upstream project rather than the maintained version here. A standalone repository is indexed normally.

## What is in the new repo

The same rules, plus everything since:

- JLCPCB and PCBWay rule files, each with a paired test board
- KiCad 8 syntax, forward-compatible with KiCad 9 and 10
- CI linting for `.kicad_dru` files, including layer-name checking
- A fix for the silkscreen layer-name bug that could silently disable every rule in the file

## Open issues

Issues here are not being migrated. If something you reported is still outstanding, please open it on [kicad-druid](https://github.com/Cimos/kicad-druid/issues).

## Origins

Originally forked from [labtroll/KiCad-DesignRules](https://github.com/labtroll/KiCad-DesignRules) by Morten Hattesen.
