import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from matplotlib.lines import Line2D
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

# YR4 : https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG136TeVxsec_extrap

data = {
      "$\delta\sigma_{ggF}$": {
        "YR4": (-7.4, 5.6),
        "R5": (-7.4, 4.8),
        "R5 without PDF": (-4.6, 1.7),
        "HL-LHC": (-1.60, 1.60),
    },
      "$\delta\sigma_{ggF(gauss)}$": {
        "YR4": (-5, 5),
        "R5": (-4.7, 4.7),
        "R5 without PDF": (-2.7, 2.7), # 4.6/sqrt(3)
        "HL-LHC": (-1.60, 1.60),
    },
    "$\delta\sigma_{VBF}$": {
        "YR4": (-2.6, 2.6), # included delta_ew of 1.5% from YR4 pg 89 (like TU+scale in R5)
        "R5": (-2.4, 2.4),
        "R5 without PDF": (-1.1, 1.1),
        "HL-LHC": (-3.1, 3.1),
    },
    "$\delta\sigma_{WH}$": {
        "YR4": (-1.9, 1.8),   
        "R5": (-1.9, 1.8), # From W+/W-H in note seems to match YR4
        "R5 without PDF": (-0.7, 0.5),
        "HL-LHC": (-5.7, 5.7),
    },
    "$\delta\sigma_{ZH}$": {
        "YR4": (-3.6, 4.1), 
        "R5": (-3.1, 3.3),
        "R5 without PDF": (-2.7, 2.9),
        "HL-LHC": (-4.2, 4.2),
    },
    "$\delta\sigma_{ttH}$": {
        "YR4": (-9.8, 6.7),
        "R5": (-3.6, 3.2),
        "R5 without PDF": (-2.3, 1.7),
        "HL-LHC": (-4.3, 4.3),
    },
    "$\delta\sigma_{tH (t-ch)}$": {
        "YR4": (-15.1, 7.3),
        "R5": (-15.1, 6.6),
        "R5 without PDF": (-15, 6.3),
        "HL-LHC": (0.0, 0.0),
    },
    "$\delta\sigma_{tH (s-ch)}$": {
        "YR4": (-2.7, 3.1),
        "R5": (-2.9, 3.3),
        "R5 without PDF": (-1.8, 2.4),
        "HL-LHC": (0.0, 0.0),
    },
     "$\delta\sigma_{tH (W-as)}$": {
        "YR4": (-9.3, 8),
        "R5": (-7.3, 6),
        "R5 without PDF": (-6.4, 4.8),
        "HL-LHC": (0.0, 0.0),
    },
    "$\delta\sigma_{bbH}$": {
        "YR4": (-24.1, 20.1),
        "R5": (-8.9, 8.9),
        "R5 without PDF": (-8.2, 8.2),
        "HL-LHC": (0.0, 0.0),
    },
}

prediction_methods = [
    "YR4",
    "R5",
    "R5 without PDF",
]

colors = {
    "YR4": "black",
    "R5": "tab:red",
    "R5 without PDF": "tab:green",
}

markers = {
    "YR4": "o",
    "R5": "s",
    "R5 without PDF": "s",
}

linestyles = {
    "YR4": "-",
    "R5": "-",
    "R5 without PDF": "-",
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
    "YR4": -0.12,
    "R5": 0.00,
    "R5 without PDF": 0.12,
}

for i, mode in enumerate(production_modes):

    neg, pos = data[mode]["HL-LHC"]

    ax.barh(
        y_base[i],
        -neg + pos, #DM
        left=neg,
        height=0.62,
        facecolor="#BFD7EA",
        edgecolor="#BFD7EA",
        #hatch="///",
        alpha=0.45,
        linewidth=2.0,
        zorder=0,
    )

block_height = 0.09  # try 0.08–0.12
    
for method in prediction_methods:

    for i, mode in enumerate(production_modes):

        neg, pos = data[mode][method] 
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
ax.set_yticklabels(production_modes)

ax.invert_yaxis()

ax.set_xlabel("Relative uncertainty [%]")
ax.set_title(r"$\sqrt{s}=14$ TeV, $m_{h}=125.09$ GeV                   LHC Higgs WG1")

ax.xaxis.set_major_locator(MultipleLocator(2))

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.5,
)

ax.set_axisbelow(True)

max_unc = max(
    max(abs(v) for pair in data[mode].values() for v in pair)
    for mode in production_modes
)

ax.set_xlim(
    -1.05 * max_unc,
     1.05 * max_unc,
)

legend_handles = [
    Patch(
        facecolor="black",
        edgecolor="black",
        label="YR4",
    ),
    Patch(
        facecolor="tab:red",
        edgecolor="tab:red",
        label="Report 5",
    ),
    Patch(
        facecolor="tab:green",
        edgecolor="tab:green",
        label="Report 5 without\nPDF+$\\alpha_{s}$ & PDF-TH",
    ),
    Patch(
        facecolor="#BFD7EA",
        edgecolor="#BFD7EA",
        #hatch="///",
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
    "production_mode_uncertainties.pdf",
    bbox_inches="tight",
)

plt.show()
