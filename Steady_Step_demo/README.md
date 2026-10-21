# Steady Step (demo) - INFOMGMT 399 Group 2 (The Big 4)

Demo artefact for the live presentation and technical demo video. Synthetic data only.

## Run (Mac: python3)
```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Data is built automatically on first run. Tests: `pip install pytest`, then `python3 -m pytest -v`.

## What each file does
| File | Role |
|---|---|
| generate_data.py | Synthetic dataset from the teaching team's data structure |
| rules.py | Day-21 features -> 3 indicators -> flag + plain-language reason |
| booking.py | Booking validation (no double booking) |
| fairness.py | Flag rate by group vs overall (10-point review rule) |
| scenarios.py | Tests T1 normal, T2 boundary, T3 error (used by pytest) |
| app.py | Side menu - Student: Overview, Weekly check-in (3 questions, 1-5), My progress, Find support (book an adviser + confirmation). Adviser: Learners to check in with, Fairness check, How it works |
| ui.py | Look and feel only (matches Report 2 screens: navy side menu, cream cards, green headings) |
| AI_use_log.md | Complete before submission |
