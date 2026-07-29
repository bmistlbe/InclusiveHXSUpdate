# Compares central values between R5 and YR4, displaying (R5-YR4)/YR4 points, and the relative uncertainty on the YR4 prediction.
# Claude-assisted.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "axes.titlesize": 20,
    "xtick.labelsize": 15,
    "ytick.labelsize": 17,
    "legend.fontsize": 14,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

# Central values of the cross-sections in pb, from the R5 and YR4.
# All for mH=125.09 GeV at 14 TeV.

CentralValues = {
    "ggF": {
        "R5": 54.09,
        "YR4": 54.60
    },
    "VBF": {
        "R5": 4.312,
        "YR4": 4.2748
    },
    "WH": {
        "R5":1.521, #0.9304+0.5906
        "YR4": 1.510
    },
    "ZH": {
        "R5":0.9875,
        "YR4": 0.9835
    },
    "ttH": {
        "R5":0.6361,
        "YR4": 0.6128
    },
    "tH (s-ch)": {
        "R5":0.00330,
        "YR4": 0.003240
    },
    "tH (t-ch)": {
        "R5":0.09189,
        "YR4": 0.09012
    },
    # "tH (W-ass)": {
    #     "R5":0.1876,
    #     "YR4": # Not in the YR4?
    # },
    "bbH": {
        "R5":0.596,
        "YR4": 0.55210
    },
}

UncertaintiesR5YR4 = {
      "ggF": {
        "YR4": (-7.4, 5.6),
        "R5": (-7.4, 4.8),
    },
    "VBF": {
        "YR4": (-2.6, 2.6), # included delta_ew of 1.5% from YR4 pg 89 (as TU+scale in R5)
        "R5": (-2.4, 2.4),
    },
    "WH": {
        "YR4": (-1.9, 1.8),   
        "R5": (-1.9, 1.8), # From W+/W-H in note seems to match YR4
    },
    "ZH": {
        "YR4": (-3.6, 4.1), 
        "R5": (-3.1, 3.3),
    },
    "ttH": {
        "YR4": (-9.8, 6.7),
        "R5": (-3.6, 3.2),
    },
    "tH (t-ch)": {
        "YR4": (-15.1, 7.3),
        "R5": (-15.1, 6.6),
    },
    "tH (s-ch)": {
        "YR4": (-2.7, 3.1),
        "R5": (-2.9, 3.3),
    },
     "tH (W-ass)": {
        "YR4": (-9.3, 8),
        "R5": (-7.3, 6),
    },
    "bbH": {
        "YR4": (-24.1, 20.1),
        "R5": (-8.9, 8.9),
    },
}

mode_keys = list(UncertaintiesR5YR4.keys())
y_base = np.arange(len(mode_keys))

# Relative difference of the R5 central value from the YR4 one, for every mode with both
# R5 and YR4 central values available (tH (W-ass) has no YR4 value).
relative_diffs = {}
for mode in mode_keys:
    if mode not in CentralValues:
        continue
    r5 = CentralValues[mode]["R5"]
    yr4 = CentralValues[mode]["YR4"]
    relative_diffs[mode] = (r5 - yr4) / yr4 * 100

fig, ax = plt.subplots(figsize=(10, 0.8 * len(mode_keys) + 1.5))

for spine in ax.spines.values():
    spine.set_linewidth(2.0)
    spine.set_color("black")

ax.tick_params(axis="both", which="major", width=2, length=6)

for i, mode in enumerate(mode_keys):
    if mode not in UncertaintiesR5YR4:
        continue
    dn, up = UncertaintiesR5YR4[mode]["YR4"]
    ax.barh(
        y_base[i],
        width=up - dn,
        left=dn,
        height=0.5,
        color="black",
        edgecolor="black",
        alpha=0.35,
        linewidth=1.5,
        zorder=2,
    )

for i, mode in enumerate(mode_keys):
    if mode not in relative_diffs:
        continue
    ax.scatter(relative_diffs[mode], y_base[i], color="#c1121f", s=60, zorder=3)

ax.axvline(0, color="black", linewidth=1.5, zorder=1)

for y_prev, y_next in zip(y_base[:-1], y_base[1:]):
    ax.axhline((y_prev + y_next) / 2, color="0.2", linestyle="--", linewidth=1.0, alpha=0.5, zorder=0)

ax.set_yticks(y_base)
ax.set_yticklabels(mode_keys, ha="right")
ax.tick_params(axis="y", pad=8)
ax.yaxis.tick_left()
ax.yaxis.set_label_position("left")
ax.tick_params(axis="y", which="major", left=True, right=False, direction="out", width=2, length=6)

ax.invert_yaxis()

ax.set_xlabel("Relative change (%)")
ax.set_title(r"$\sqrt{s}=14$ TeV, $m_h=125.09$ GeV                   LHC Higgs WG1")

max_unc = max(
    [abs(v) for v in relative_diffs.values()]
    + [abs(v) for mode in UncertaintiesR5YR4 for v in UncertaintiesR5YR4[mode]["YR4"]]
)
# Halved tick density (step 4 instead of 2) once labels get wide enough that the minus
# signs start to crowd into the neighbouring number.
tick_step = 1 if max_unc <= 10 else 4
ax.xaxis.set_major_locator(MultipleLocator(tick_step))

ax.grid(axis="x", linestyle="--", alpha=0.5)
ax.set_axisbelow(True)

ax.set_xlim(-1.15 * max_unc, 1.15 * max_unc)

legend_handles = [
    Line2D(
        [0], [0],
        marker="o",
        linestyle="None",
        color="#c1121f",
        markersize=8,
        label=r"$\frac{R5-YR4}{YR4}$",
    ),
    Patch(
        facecolor="black",
        edgecolor="black",
        alpha=0.35,
        label=r"$\delta_{total}$, YR4 (%)",
    ),
]
ax.legend(
    handles=legend_handles,
    loc="upper right",
    frameon=True,
    framealpha=1,
    edgecolor="black",
    fancybox=False,
)

fig.tight_layout()

fig.savefig("central_value_comparison.pdf", bbox_inches="tight")

plt.show()
