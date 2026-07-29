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

# Relative uncertainties on the cross-sections (down, up) in percent, from the R5. 
# All on mH=125.09 GeV at 14 TeV.


Uncertainties = {
    "ggF": {
        "PDFaS": (-2.5, 2.5),
        "PDFTH": (-2.4, 2.4),
        "EWK": (-1.0, 1.0),
        "tbc": (-0.34, 0.34),
        "QCDscale": (-3.3, 0.32),
    },
    "VBF": {
        "PDFaS": (-2.1, 2.1),
        "TU": (-1.1, 1.1),
        "QCDscale": (-0.097, 0.14),
    },
    "WH": {
        "PDFaS": (-1.8, 1.8),
        "QCDscale": (-0.7, 0.5),
    },
    "ZH": {
        "PDFaS": (-1.5, 1.5),
        "QCDscale": (-2.7, 3.0),
    },
    "ttH": {
        "PDFaS": (-2.7, 2.7),
        "virt": (-0.9, 0.9),
        "QCDscale": (-2.1, 1.4),
    },
    "tH (t-ch)": {
        "PDFaS": (-1.9, 1.9),
        "QCDscaleFS": (-15, 6.4),
    },
    "tH (s-ch)": {
        "PDFaS": (-2.3, 2.3),
        "QCDscaleFS": (-1.8, 2.4),
    },
    "tH (W-ass)": {
        "PDFaS": (-3.6, 3.6),
        "QCDscaleFS": (-6.4, 4.8),
    },
    "bbH": {
        "PDFaS": (-2.9, 2.9),
        "mB": (-1.83, 1.83),
        "muB": (-5.4, 5.4),
        "QCDscale": (-6.2, 6.2),
    },
}

# How the uncertainties are combined to get the total, for each production mode.
def total_ggF(PDFaS, PDFTH, QCDscale, EWK, tbc):
    """QCDscale+EWK+tbc and PDFTH combined linearly, then added in quadrature with PDFaS.
    Returns (down, up) with down negative by convention."""
    dn = -np.sqrt((abs(QCDscale[0]) + abs(EWK[0]) + abs(tbc[0]) + abs(PDFTH[0])) ** 2 + PDFaS[0] ** 2)
    up =  np.sqrt((QCDscale[1]   + EWK[1] + tbc[1]   + PDFTH[1]) ** 2 + PDFaS[1] ** 2)
    return (dn, up)


def total_VBF(PDFaS, QCDscale, TU):
    """QCDscale and TU added linearly, then added in quadrature to PDFaS.
    Returns (down, up) with down negative by convention."""
    dn = -np.sqrt((abs(QCDscale[0])+abs(TU[0])) ** 2 + PDFaS[0] ** 2)
    up =  np.sqrt((QCDscale[1]+TU[1]) ** 2 + PDFaS[1] ** 2)
    return (dn, up)


def total_WH(PDFaS, QCDscale):
    """PDFaS and QCD scale added in quadrature. Returns (down, up) with down negative by convention."""
    dn = -np.sqrt(PDFaS[0] ** 2 + QCDscale[0] ** 2)
    up =  np.sqrt(PDFaS[1] ** 2 + QCDscale[1] ** 2)
    return (dn, up)


def total_ZH(PDFaS, QCDscale):
    """PDFaS and QCD scale added in quadrature. Returns (down, up) with down negative by convention."""
    dn = -np.sqrt(PDFaS[0] ** 2 + QCDscale[0] ** 2)
    up =  np.sqrt(PDFaS[1] ** 2 + QCDscale[1] ** 2)
    return (dn, up)


def total_ttH(PDFaS, QCDscale, virt):
    """PDFaS and QCD scale and virt all added in quadrature. Returns (down, up) with down negative by convention."""
    dn = -np.sqrt(PDFaS[0] ** 2 + QCDscale[0] ** 2 + virt[0] ** 2)
    up =  np.sqrt(PDFaS[1] ** 2 + QCDscale[1] ** 2 + virt[1] ** 2)
    return (dn, up)


def total_tH_tch(PDFaS, QCDscaleFS):
    """PDFaS and QCD scale FS added in quadrature. Returns (down, up) with down negative by convention."""
    dn = -np.sqrt(PDFaS[0] ** 2 + QCDscaleFS[0] ** 2)
    up =  np.sqrt(PDFaS[1] ** 2 + QCDscaleFS[1] ** 2)
    return (dn, up)


def total_tH_sch(PDFaS, QCDscaleFS):
    """PDFaS and QCD scale FS added in quadrature. Returns (down, up) with down negative by convention."""
    dn = -np.sqrt(PDFaS[0] ** 2 + QCDscaleFS[0] ** 2)
    up =  np.sqrt(PDFaS[1] ** 2 + QCDscaleFS[1] ** 2)
    return (dn, up)


def total_tH_Wass(PDFaS, QCDscaleFS):
    """PDFaS and QCD scale FS added in quadrature. Returns (down, up) with down negative by convention."""
    dn = -np.sqrt(PDFaS[0] ** 2 + QCDscaleFS[0] ** 2)
    up =  np.sqrt(PDFaS[1] ** 2 + QCDscaleFS[1] ** 2)
    return (dn, up)


def total_bbH(PDFaS, mB, QCDscale, muB):
    """PDFaS, mB, QCDscale and muB all added in quadrature. Returns (down, up) with down negative by convention."""
    dn = -np.sqrt(PDFaS[0] ** 2 + mB[0] ** 2 + QCDscale[0] ** 2 + muB[0] ** 2)
    up =  np.sqrt(PDFaS[1] ** 2 + mB[1] ** 2 + QCDscale[1] ** 2 + muB[1] ** 2)
    return (dn, up)


total_funcs = {
    "ggF":        total_ggF,
    "VBF":        total_VBF,
    "WH":         total_WH,
    "ZH":         total_ZH,
    "ttH":        total_ttH,
    "tH (t-ch)":  total_tH_tch,
    "tH (s-ch)":  total_tH_sch,
    "tH (W-ass)": total_tH_Wass,
    "bbH":        total_bbH,
}

mode_keys = list(total_funcs.keys())
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
