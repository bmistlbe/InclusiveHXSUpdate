import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.patches import Patch

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

data = {
    r"$\delta(total)$": {
        "YR4": (-7.4, 5.6),  
        "R5": (-7.4, 4.8),
        "HL-LHC": (-1.6, 1.6),  
    },
    r"$\delta(PDF+\alpha_s)$": {
        "YR4": (-3.2, 3.2),  
        "R5": (-2.5, 2.5),   
        "HL-LHC": (0.0, 0.0),
    },
    r"$\delta(PDF-TH)$": {
        "YR4": (-1.2, 1.2), 
        "R5": (-2.4, 2.4),   
        "HL-LHC": (0.0, 0.0),
    },
    r"$\delta(scale)$": {
        "YR4": (-2.4, 0.2), 
        "R5": (-3.3, 0.3),  
        "HL-LHC": (0.0, 0.0),
    },
    r"$\delta(EWK)$": {
        "YR4": (-1.0, 1.0),
        "R5": (-1.0, 1.0), 
        "HL-LHC": (0.0, 0.0),
    },
    r"$\delta(t,b,c)$": {
        "YR4": (-0.8, 0.8),  
        "R5": (-0.34, 0.34), 
        "HL-LHC": (0.0, 0.0),
    },
    r"$\delta(1/m_t)$": {
        "YR4": (-1.0, 1.0), 
        "R5": (0.0, 0.0),
        "HL-LHC": (0.0, 0.0),
    },
    r"$\delta(trunc.)$": {
        "YR4": (-0.4, 0.4), 
        "R5": (0.0, 0.0),
        "HL-LHC": (0.0, 0.0),
    },
}

prediction_methods = ["YR4", "R5"]

colors = {
    "YR4": "black",
    "R5": "tab:red",
}

production_modes = list(data.keys())
y_base = np.arange(len(production_modes))

fig, ax = plt.subplots(figsize=(12, 7))

for spine in ax.spines.values():
    spine.set_linewidth(2.0)
    spine.set_color("black")

ax.tick_params(
    axis="both",
    which="major",
    width=2,
    length=6,
)

offsets = {
    "YR4": -0.10,
    "R5": 0.10,
}

for i, mode in enumerate(production_modes):

    neg, pos = data[mode]["HL-LHC"]

    if neg != 0.0 or pos != 0.0:
        ax.barh(
            y_base[i],
            -neg + pos,
            left=neg,
            height=0.62,
            facecolor="#BFD7EA",
            edgecolor="#BFD7EA",
            alpha=0.45,
            linewidth=2.0,
            zorder=0,
        )

block_height = 0.09

for method in prediction_methods:

    for i, mode in enumerate(production_modes):

        neg, pos = data[mode][method]

        if neg == 0.0 and pos == 0.0:
            continue

        y = y_base[i] + offsets[method]

        ax.barh(
            y,
            width=pos - neg,
            left=neg,
            height=block_height,
            color=colors[method],
            edgecolor=colors[method],
            linewidth=1.5,
            alpha=0.9,
            zorder=3,
        )

ax.axvline(
    0,
    color="0.2",
    linewidth=1.5,
    zorder=2,
)

for i in range(len(production_modes) - 1):
    ax.axhline(
        i + 0.5,
        color="0.2",
        linestyle="--",
        linewidth=1.5,
        alpha=0.5,
        zorder=0,
    )

ax.set_yticks(y_base)
#ax.set_yticklabels(production_modes)
ax.set_yticklabels(production_modes, ha="right")
ax.tick_params(axis="y", pad=8)

#ax.yaxis.tick_right()
#ax.yaxis.set_label_position("right")
#ax.tick_params(axis="y", length=0)

ax.yaxis.tick_left()
ax.yaxis.set_label_position("left")
ax.tick_params(
    axis="y",
    which="major",
    left=True,
    right=False,
    direction="out",
    width=2,
    length=6,
)


ax.invert_yaxis()

ax.set_xlabel("Relative uncertainty [%]")
ax.set_title(
    r"ggF - $\sqrt{s}=14$ TeV, $m_h=125.09$ GeV                   LHC Higgs WG1"
)

ax.xaxis.set_major_locator(MultipleLocator(2))
ax.set_xlim(-10, 10)

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.5,
)

ax.set_axisbelow(True)

legend_handles = [
    Patch(facecolor="black", edgecolor="black", label="YR4"),
    Patch(facecolor="tab:red", edgecolor="tab:red", label="Report 5"),
    Patch(
        facecolor="#BFD7EA",
        edgecolor="#BFD7EA",
        alpha=0.45,
        linewidth=2.0,
        label="HL-LHC projection\nATLAS and CMS",
    ),
]

ax.legend(
    handles=legend_handles,
    loc="center right",
    frameon=True,
    framealpha=1,
    edgecolor="black",
    fancybox=False,
)

fig.tight_layout()

fig.savefig(
    "ggF_uncertainties.pdf",
    bbox_inches="tight",
)

plt.show()
