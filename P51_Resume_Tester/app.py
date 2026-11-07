"""Web UI for the P51 tester.  Run:  streamlit run app.py"""
import os, subprocess, sys, tempfile
import pandas as pd
import streamlit as st

st.set_page_config(page_title="P51 Resume Screening Tester", layout="wide")
st.title("P51 · Counterfactual Resume Screening Tester")
st.caption("Same resume, only name / gender / hometown changed. Do the scores move?")

with st.sidebar:
    backend = st.radio("Screener", ["mock (offline demo)", "anthropic (real LLM)"])
    real = backend.startswith("anthropic")
    mock_bias = True
    key = ""
    if real:
        key = st.text_input("ANTHROPIC_API_KEY", type="password", value=os.environ.get("ANTHROPIC_API_KEY", ""))
        model = st.text_input("Model", value="claude-sonnet-5-5")
        debias = st.checkbox("Add 'ignore name/gender/hometown' instruction (mitigation test)")
    else:
        mock_bias = st.checkbox("Inject simulated bias (uncheck = null control)", value=True)
    reps = st.slider("Repetitions per resume", 1, 10, 5)
    thr = st.slider("Flag threshold (points)", 0.5, 10.0, 3.0, 0.5)
    emb = st.selectbox("Equivalence embedder", ["auto", "bert", "tfidf"])
    go = st.button("Run experiment", type="primary")

if go:
    out = tempfile.mkdtemp(prefix="p51_")
    cmd = [sys.executable, "run_experiment.py", "--backend", "anthropic" if real else "mock",
           "--reps", str(reps), "--threshold", str(thr), "--embedder", emb, "--out", out]
    env = dict(os.environ); env["PYTHONIOENCODING"] = "utf-8"; env["PYTHONUTF8"] = "1"
    if real:
        env["ANTHROPIC_API_KEY"] = key
        cmd += ["--model", model] + (["--debias-prompt"] if debias else [])
    elif not mock_bias:
        cmd += ["--no-mock-bias"]
    with st.spinner("Running… (real LLM runs make 20 x reps API calls)"):
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=os.path.dirname(os.path.abspath(__file__)))
    if r.returncode != 0:
        st.error("Run failed"); st.code(r.stdout + "\n" + r.stderr)
    else:
        if not real:
            st.warning("SIMULATED results from the mock screener. They say nothing about a real LLM.")
        df = pd.read_csv(f"{out}/gap_table.csv", encoding="utf-8-sig")
        n_flag = int((df.status == "FLAG").sum())
        c1, c2, c3 = st.columns(3)
        c1.metric("Pairs flagged", f"{n_flag} / {len(df)}")
        c2.metric("Largest |gap|", f"{df.gap.abs().max():.2f} pts")
        c3.metric("Pairs identical after masking (U3)", f"{int(df.equivalent.sum())} / {len(df)}")
        st.subheader("Gap table")
        st.dataframe(df.style.map(lambda v: {"FLAG": "background-color:#f5b7b1", "WATCH": "background-color:#fcf3cf"}.get(v, ""),
                                   subset=["status"]))
        st.subheader("Charts")
        a, b, c = st.columns(3)
        a.image(f"{out}/chart_gap_per_pair.png"); b.image(f"{out}/chart_gap_by_attribute.png"); c.image(f"{out}/chart_base_vs_variant.png")
        st.subheader("Report and mitigations")
        st.markdown(open(f"{out}/report.md", encoding="utf-8").read())
        st.download_button("Download gap_table.csv", open(f"{out}/gap_table.csv", "rb"), "gap_table.csv")
else:
    st.info("Choose settings in the sidebar and click **Run experiment**.")
