import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from matplotlib.lines import Line2D
from matplotlib.patches import Patch

plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "axes.titlesize": 18,
    "xtick.labelsize": 12,
    "ytick.labelsize": 17,
    "legend.fontsize": 13,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

## NOTES :

# Run 2 : signal stregth measurements from ATLAS-CONF-2025-006 (Figure 3) and CMS-HIG-21-018 (Figure 6)
#         bbH scaled with ggH, tH scaled with ttH  
#         Using measurement with smallest uncertainty   

# HL-LHC : sigma_i/sigma_SM projection from snowmass (https://arxiv.org/abs/2209.07510)
#          Originally from CERN-2019-007 (Fig 28)


data = {
      "ggF": {
        "YR4": (-7.4, 5.6),
        "R5": (-7.4, 4.8),
        "R5 without PDF": (-4.6, 1.7),
        "HL-LHC": (-1.60, 1.60),
        "Run 2": (-6.0, 7.0),   
    },
      "ggF(gauss)": {
        "YR4": (-5, 5),
        "R5": (-4.7, 4.7),
        "R5 without PDF": (-2.7, 2.7), # 4.6/sqrt(3)
        "HL-LHC": (-1.60, 1.60),
        "Run 2": (-6.0, 7.0),  
    },
    "VBF": {
        "YR4": (-2.6, 2.6), # included delta_ew of 1.5% from YR4 pg 89 (as TU+scale in R5)
        "R5": (-2.4, 2.4),
        "R5 without PDF": (-1.1, 1.1),
        "HL-LHC": (-3.1, 3.1),
        "Run 2": (-11.0, 12.0), 
    },
    "WH": {
        "YR4": (-1.9, 1.8),   
        "R5": (-1.9, 1.8), # From W+/W-H in note seems to match YR4
        "R5 without PDF": (-0.7, 0.5),
        "HL-LHC": (-5.7, 5.7),
        "Run 2": (-16.0, 16.0),
    },
    "ZH": {
        "YR4": (-3.6, 4.1), 
        "R5": (-3.1, 3.3),
        "R5 without PDF": (-2.7, 2.9),
        "HL-LHC": (-4.2, 4.2),
        "Run 2": (-15.0, 17.0),
    },
    "ttH": {
        "YR4": (-9.8, 6.7),
        "R5": (-3.6, 3.2),
        "R5 without PDF": (-2.3, 1.7),
        "HL-LHC": (-4.3, 4.3),
        "Run 2": (-14.0, 15.0), 
    },
    "tH (t-ch)": {
        "YR4": (-15.1, 7.3),
        "R5": (-15.1, 6.6),
        "R5 without PDF": (-15, 6.3),
        "HL-LHC": (0.0, 0.0),
        "Run 2": (0.0, 0.0),
    },
    "tH (s-ch)": {
        "YR4": (-2.7, 3.1),
        "R5": (-2.9, 3.3),
        "R5 without PDF": (-1.8, 2.4),
        "HL-LHC": (0.0, 0.0),
        "Run 2": (0.0, 0.0),
    },
     "tH (W-as)": {
        "YR4": (-9.3, 8),
        "R5": (-7.3, 6),
        "R5 without PDF": (-6.4, 4.8),
        "HL-LHC": (0.0, 0.0),
        "Run 2": (0.0, 0.0),
    },
    "bbH": {
        "YR4": (-24.1, 20.1),
        "R5": (-8.9, 8.9),
        "R5 without PDF": (-8.2, 8.2),
        "HL-LHC": (0.0, 0.0),
        "Run 2": (0.0, 0.0),
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
    "R5": "o",
    "R5 without PDF": "o",
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
    "YR4": -0.15,
    "R5": 0.0,
    "R5 without PDF": 0.15,
}

for i, mode in enumerate(production_modes): # Draw HL-LHC and Run 2 constraints

    neg, pos = data[mode]["HL-LHC"]

    ax.barh(
        y_base[i],
        -neg + pos, 
        left=neg,
        height=0.62,
        facecolor="#BFD7EA",
        edgecolor="blue",
        #hatch="///",
        alpha=0.45,
        linewidth=1.0,
        zorder=0,
    )

    neg, pos = data[mode]["Run 2"]

    ax.barh(
      y_base[i],
      width=pos-neg,
      left=neg,
      height=0.62,
      facecolor="none",
      edgecolor="tab:blue",
      linewidth=1.0,
      linestyle="-",
      zorder=1,
    )
     

block_height = 0.1  
    
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

ax.set_xlabel("Relative uncertainty on production rate [%]") # $\delta\sigma/\sigma$ 
ax.set_title(r"LHC Higgs WG1")

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
    -1.22 * max_unc,
     1.22 * max_unc,
)
#ax.set_xlim(-30, 30)

legend_handles = [
    Patch(
        facecolor="black",
        edgecolor="black",
        label="$\mathrm{\sigma}$ YR4 [$\sqrt{s}=14$ TeV]", # , $m_{h}=125.09$ GeV
    ),
    Patch(
        facecolor="tab:red",
        edgecolor="tab:red",
        label="$\mathrm{\sigma}$ R5 [$\sqrt{s}=14$ TeV]",
    ),
    Patch(
        facecolor="tab:green",
        edgecolor="tab:green",
        label="$\mathrm{\sigma}$ R5 [$\sqrt{s}=14$ TeV]\nexcl. PDF+$\\alpha_{s}$ & PDF-TH",
    ),
    Patch(
        facecolor="none",
        edgecolor="tab:blue",
        label="$\mathrm{\mu}$ LHC Run 2\nATLAS/CMS (best) \n[Stat+Exp+Th]",
    ),
    Patch(
        facecolor="#BFD7EA",
        edgecolor="blue",
        #hatch="///",
        alpha=0.45,
        linewidth=1.0,
        label="$\mathrm{\mu}$ HL-LHC projection\nATLAS + CMS\n[Stat+Exp+Th]",
    ),
]

ax.legend(
    handles=legend_handles,
    loc="upper right",
    bbox_to_anchor=(1.08, 1.1),   # slightly outside right
    labelspacing=0.75,    
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
