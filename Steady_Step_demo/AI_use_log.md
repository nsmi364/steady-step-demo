# AI-use log - Steady Step (INFOMGMT 399, Group 2)

Required by the Presentation & Technical Demo Guide. Add a row **every time** AI materially helps.
Keep prompt exports in `/ai_prompts/`.

| # | Date | Tool / model | Component | What we asked (prompt file) | What the team changed / checked | How we tested it |
|---|---|---|---|---|---|---|
| 1 | 2026-09 | Replit Agent | Report 2 prototype (UI) | Single prompt - Report 2 Appendix B | Replaced in final artefact; kept booking idea, advisers, supportive wording | Team role-play walkthrough (Report 2) |
| 2 | 2026-10-20 | Claude (claude-opus-5-5) | Demo artefact: `generate_data.py`, `rules.py`, `booking.py`, `scenarios.py`, `app.py`, tests | Prompt asking for a Streamlit artefact matching our reports + synthetic data from the teaching team's structure (`ai_prompts/02_claude_starter.md`) | *TO FILL: list our own edits, e.g. changed thresholds, added X, rewrote Y* | `pytest` (4 tests) + in-app Test scenarios page (T1-T3), manual walkthrough of every page |
| 3 | | | | | | |

## Independently developed (team) vs AI-assisted
| Component | Team decision / work | AI-assisted |
|---|---|---|
| Day-21 checkpoint, 3 indicators, 2-of-3 rule, 10-point fairness rule | Team (Report 1 & 2, Appendix H) | Coded with AI help |
| Synthetic data assumptions (distributions, engagement links) | *TO FILL: what we reviewed / changed* | Generator drafted by AI |
| Supportive wording | Team (Chang, Chen & Lee, 2025) | - |
| *TO FILL* | | |

## Checks we ran on AI output
- Data matches every field / allowed value in the teaching team's structure (checked on: ____ by ____)
- No data after day 21 used in the flag (test T4)
- Every flag has a reason (`test_every_flag_has_a_reason`)
