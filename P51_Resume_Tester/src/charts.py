"""U4 - charts of score gaps."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

COL = {"FLAG": "#c0392b", "WATCH": "#e0a800", "OK": "#2e8b57"}

def gap_bar(df, threshold, path, title_suffix=""):
    fig, ax = plt.subplots(figsize=(9, 5))
    y = np.arange(len(df))[::-1]
    for yi, (_, r) in zip(y, df.iterrows()):
        ax.barh(yi, r["gap"], color=COL[r["status"]], alpha=.85)
        ax.plot([r["ci_low"], r["ci_high"]], [yi, yi], color="black", lw=1.2)
    ax.axvline(0, color="black", lw=.8)
    for s in (-threshold, threshold):
        ax.axvline(s, color="grey", ls="--", lw=1)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{r.pair_id} {r.attribute}\n{r.base_label} → {r.var_label}" for r in df.itertuples()], fontsize=7)
    ax.set_xlabel("Score gap (variant − base), points on 0-100 scale; whiskers = 95% CI")
    ax.set_title(f"Counterfactual score gaps per pair (dashed = ±{threshold:g} threshold){title_suffix}")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=c, label=k) for k, c in COL.items()], loc="lower right")
    fig.tight_layout(); fig.savefig(path, dpi=140); plt.close(fig)

def attr_summary(df, threshold, path):
    g = df.groupby("attribute")["gap"].agg(["mean", "min", "max"]).reindex(["gender", "name_origin", "hometown"])
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    x = np.arange(len(g))
    ax.bar(x, g["mean"], color="#4a6fa5", alpha=.85)
    for xi, a in zip(x, df.groupby("attribute", sort=False)):
        pass
    for xi, att in zip(x, g.index):
        pts = df[df.attribute == att]["gap"]
        ax.scatter([xi] * len(pts), pts, color="black", s=18, zorder=3)
    ax.axhline(0, color="black", lw=.8)
    for s in (-threshold, threshold):
        ax.axhline(s, color="grey", ls="--", lw=1)
    ax.set_xticks(x); ax.set_xticklabels(["gender", "name origin", "hometown"])
    ax.set_ylabel("Mean gap (points)"); ax.set_title("Mean gap by manipulated attribute (dots = pairs)")
    fig.tight_layout(); fig.savefig(path, dpi=140); plt.close(fig)

def score_scatter(df, path):
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    lim = [min(df.base_mean.min(), df.var_mean.min()) - 2, max(df.base_mean.max(), df.var_mean.max()) + 2]
    ax.plot(lim, lim, color="grey", ls=":")
    for r in df.itertuples():
        ax.scatter(r.base_mean, r.var_mean, color=COL[r.status], s=60)
        ax.annotate(r.pair_id, (r.base_mean, r.var_mean), fontsize=7, xytext=(3, 3), textcoords="offset points")
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel("Base resume mean score"); ax.set_ylabel("Counterfactual resume mean score")
    ax.set_title("Identical resumes should sit on the diagonal")
    fig.tight_layout(); fig.savefig(path, dpi=140); plt.close(fig)
