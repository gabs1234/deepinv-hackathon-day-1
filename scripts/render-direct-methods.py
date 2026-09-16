"""Render illustrative CTF/TIE/ICT line cuts for the introductory slide.

These analytic curves are independent of the measured reconstruction runs.
The ICT denominator follows Farago et al., doi:10.1364/OL.530330.
"""

from pathlib import Path
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "public" / "phase-retrieval"
DISTANCE_RATIOS = (1.0, 1.37)
GAMMA = 10.0
COLORS = ("#666666", "#326899")
STYLES = ("-", (0, (4, 2)))
BACKGROUND = "#fffff8"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "font.size": 11,
    "mathtext.fontset": "dejavuserif",
    "figure.facecolor": BACKGROUND,
    "axes.facecolor": BACKGROUND,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#888888",
    "axes.linewidth": 0.65,
    "axes.labelcolor": "#333333",
    "text.color": "#222222",
    "xtick.color": "#555555",
    "ytick.color": "#555555",
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "axes.grid": False,
    "svg.fonttype": "path",
})


def response(method, u, distance_ratio):
    chi = np.pi * distance_ratio * np.asarray(u) ** 2
    if method == "ctf":
        return 2 * np.sin(chi)
    if method == "tie":
        return 2 * chi
    return np.cos(chi) + GAMMA * np.sin(chi)


def zeros(method, distance_ratio, upper):
    if method == "tie":
        return np.array([0.0])
    if method == "ctf":
        values = np.sqrt(np.arange(0, 10) / distance_ratio)
    else:
        values = np.sqrt(
            (np.arange(1, 10) * np.pi - np.arctan(1 / GAMMA))
            / (np.pi * distance_ratio)
        )
    return values[values <= upper]


def render(method):
    # TIE is deliberately restricted to chi <= 0.269, where sin(chi) ~ chi.
    upper = 0.25 if method == "tie" else 1.70
    u = np.linspace(0.0, upper, 1800)
    fig, ax = plt.subplots(figsize=(4.5, 3.0))
    fig.subplots_adjust(left=0.15, right=0.84, bottom=0.24, top=0.85)
    all_responses = []
    all_zeros = []
    for index, ratio in enumerate(DISTANCE_RATIOS):
        values = response(method, u, ratio)
        roots = zeros(method, ratio, upper)
        # These checks exercise the analytic formulas, not pixel appearance.
        assert np.allclose(response(method, roots, ratio), 0, atol=1e-12)
        ax.plot(u, values, color=COLORS[index], ls=STYLES[index], lw=1.55)
        ax.plot(roots, np.zeros_like(roots), ls="none", marker="o" if index == 0 else "s",
                ms=4, mfc=BACKGROUND, mec=COLORS[index], mew=1, clip_on=False)
        # Labels beside endpoints; shape and dash also distinguish distances.
        ax.annotate(rf"$z_{index + 1}$", xy=(upper, values[-1]),
                    xytext=(6, 0), textcoords="offset points", va="center",
                    color=COLORS[index], fontsize=12)
        all_responses.append(values)
        all_zeros.append(roots.tolist())

    ax.spines["bottom"].set_bounds(0, upper)
    ax.spines["left"].set_bounds(np.min(all_responses), np.max(all_responses))
    ax.set_xlim(0, upper)
    ax.set_xlabel(r"$u=q\sqrt{\lambda z_1}$", labelpad=4)
    ax.set_ylabel(r"$D_z$" if method == "ict" else r"$h_z$", labelpad=1)
    if method == "tie":
        ax.set_ylim(-0.025, 0.57)
        ax.set_xticks([0, 0.1, 0.2, 0.25], ["0", "0.1", "0.2", "0.25"])
        ax.set_yticks([0, 0.25, 0.5])
        ax.set_title("Only DC is a zero · low-frequency zoom", fontsize=11, pad=12)
    else:
        limit = 2.25 if method == "ctf" else 11.2
        ax.set_ylim(-limit, limit)
        ax.set_xticks([0, 0.5, 1, 1.5], ["0", "0.5", "1", "1.5"])
        ax.set_yticks([-2, 0, 2] if method == "ctf" else [-10, 0, 10])
        ax.axhline(0, color="#888888", linewidth=0.6, zorder=0)
        ax.set_title("Repeated zeros shift with distance", fontsize=11, pad=12)

    fig.savefig(OUTPUT / f"direct-{method}.svg", facecolor=BACKGROUND,
                metadata={"Date": None, "Description": f"Analytic {method.upper()} transfer functions; z2/z1=1.37."})
    plt.close(fig)
    return {"u_range": [0, upper], "zero_locations": all_zeros}


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    result = {
        "source": "scripts/render-direct-methods.py",
        "kind": "analytic illustration, not experimental reconstruction",
        "coordinate": "u = q sqrt(lambda z1); q in cycles per length",
        "distance_ratios": DISTANCE_RATIOS,
        "ict_delta_over_beta": GAMMA,
        "panels": {method: render(method) for method in ("ctf", "tie", "ict")},
        "sources": [
            "https://arxiv.org/html/2205.01099v2",
            "https://doi.org/10.1364/OL.530330",
            "https://irp.pages.gwdg.de/hotopy/reference/generated/generated/hotopy.holo.ICT.html",
        ],
    }
    assert max(np.pi * max(DISTANCE_RATIOS) * 0.25 ** 2, 0) < 0.27
    assert np.allclose(response("ict", 0, 1), 1)
    (OUTPUT / "direct-methods-manifest.json").write_text(json.dumps(result, indent=2) + "\n")
    print("Rendered CTF, TIE and ICT transfer-function line cuts.")


if __name__ == "__main__":
    main()
