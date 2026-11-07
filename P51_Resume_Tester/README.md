# P51 - Counterfactual Resume Screening Tester

Tests whether an LLM screener scores identical resumes differently when only name, gender signal, or hometown changes.

## Easiest: web app
- Windows: double-click `run_app.bat`  (or in a terminal: `.\run_app.bat`)
- Mac/Linux: `./run_app.sh`

Opens a browser UI at http://localhost:8501. Optional real BERT check: `pip install -r requirements-bert.txt`.

## Command line
```bash
pip install -r requirements.txt
python run_experiment.py --backend mock                  # offline, SIMULATED biased screener (demo)
python run_experiment.py --backend mock --no-mock-bias --out outputs_null_control   # null control
export ANTHROPIC_API_KEY=...                             # real audit:
python run_experiment.py --backend anthropic --reps 5 --out outputs_real
python run_experiment.py --backend anthropic --debias-prompt --out outputs_real_debiased   # test a mitigation
python tests/test_pipeline.py
```
Options: `--threshold 3.0`, `--reps 5`, `--embedder auto|bert|tfidf`, `--model <id>` (or env `P51_MODEL`).

## Layout (units)
- `src/design.py`, `src/resumes.py` - **U1** design, 10 base profiles, pairs
- `src/screener.py` - **U2** LLM screener (Anthropic) + offline mock
- `src/similarity.py` - **U3** BERT cosine + strict masked-text check (TF-IDF fallback)
- `src/charts.py` - **U4** charts
- `src/analysis.py`, `run_experiment.py` - **U5** gaps, flags, mitigations, report
- `outputs/` - gap table (`gap_table.csv`, `report.md`), charts, raw scores, equivalence check
- `outputs_null_control/` - same run with an unbiased mock: nothing should flag

## IMPORTANT: what the included results are
The included results use the **mock screener**, not a real LLM, and TF-IDF instead of BERT. This sandbox had no API key and no access to model weights. The mock has bias injected on purpose (female names on technical roles, minority-coded names, small-town hometowns), so the results prove the *tester* detects bias and stays quiet on the null control. They say nothing about Claude or any other real model. Run with `--backend anthropic` and `sentence-transformers` installed for a real audit.
