import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

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

# Uncertainties on the cross-sections (down, up) in percent. All on mH=125.09 GeV at 14 TeV.
# TH: theory scale, PDFaS: PDF+alphaS, PDFTH: PDF theory (ggF only).
# Entries are ordered largest-bar-first: the first key is always the full total (PDFaS),
# and the last key is the smallest, innermost bar. See `uncertainty_steps`.
data = {
    "ggF": {
        "PDFaS": (-2.5, 2.5),
        "PDFTH": (-2.4, 2.4),
        "EWK": (-1, 1),
        "t,b,c": (-0.34, 0.34),
        "QCD scale":    (-3.3, 0.32),
    },
    "VBF": {
        "PDFaS": (-2.1, 2.1),
        "TU": (-1.1,1.1),
        "QCD scale":    (-0.097, 0.14),
    },
    "WH": {
        "PDFaS": (-1.8, 1.8),
        "QCD scale": (-0.7,0.5)
    },
    "ZH": {
        "PDFaS": (-1.5, 1.5),
        "QCD scale": (-2.7,3.0)
    },
    "ttH": {
        "PDFaS": (-2.7, 2.7),
        "virt": (-0.9,0.9),
        "QCD scale": (-2.1, 1.4),
    },
    "tH (t-ch)": {
        "PDFaS": (-1.9, 1.9),
        "QCD scale+FS": (-15, 6.4)
    },
    "tH (s-ch)": {
        "PDFaS": (-2.3, 2.3),
        "QCD scale+FS": (-1.8, 2.4)
    },
    "tH (W-ass)": {
        "PDFaS": (-3.6, 3.6),
        "QCD scale+FS": (-6.4, 4.8)
    },
    "bbH": {
        "PDFaS": (-2.9, 2.9),
        "mB": (-1.83, 1.83),
        "muB": (-5.4, 5.4),
        "QCD scale": (-6.2, 6.2),
    }, #  # type: ignore
}


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

# Maps each `data` key to the corresponding total_* function parameter name, so that the
# display order of `data` (used for labelling/coloring) can differ from the argument order
# the combination formulas expect.
param_names = {
    "ggF":        {"PDFaS": "PDFaS", "PDFTH": "PDFTH", "QCD scale": "QCDscale", "EWK": "EWK", "t,b,c": "tbc"},
    "VBF":        {"PDFaS": "PDFaS", "QCD scale": "QCDscale", "TU": "TU"},
    "WH":         {"PDFaS": "PDFaS", "QCD scale": "QCDscale"},
    "ZH":         {"PDFaS": "PDFaS", "QCD scale": "QCDscale"},
    "ttH":        {"PDFaS": "PDFaS", "QCD scale": "QCDscale", "virt": "virt"},
    "tH (t-ch)":  {"PDFaS": "PDFaS", "QCD scale+FS": "QCDscaleFS"},
    "tH (s-ch)":  {"PDFaS": "PDFaS", "QCD scale+FS": "QCDscaleFS"},
    "tH (W-ass)": {"PDFaS": "PDFaS", "QCD scale+FS": "QCDscaleFS"},
    "bbH":        {"PDFaS": "PDFaS", "mB": "mB", "QCD scale": "QCDscale", "muB": "muB"},
}

zero = (0.0, 0.0)


def uncertainty_steps(mode_key):
    """Build up from all sources zero to all sources at their quoted values, adding one
    source at a time in reverse dictionary order. Depth 0 is the full total (every source
    added); depth d has the first d sources (in dict order) still zeroed. Each step is
    labelled by the source that was just switched on, i.e. `keys[depth]`."""
    keys = list(data[mode_key].keys())
    func = total_funcs[mode_key]
    names = param_names[mode_key]
    steps = []
    for depth in range(len(keys)):
        kwargs = {names[k]: (data[mode_key][k] if i >= depth else zero) for i, k in enumerate(keys)}
        steps.append((keys[depth], func(**kwargs)))
    return steps


breakdowns = {mode_key: uncertainty_steps(mode_key) for mode_key in total_funcs}
totals = {mode_key: steps[0][1] for mode_key, steps in breakdowns.items()}

production_mode_labels = {
    "ggF":        r"$\delta\sigma_{\mathrm{ggF}}$",
    "VBF":        r"$\delta\sigma_{\mathrm{VBF}}$",
    "WH":         r"$\delta\sigma_{\mathrm{WH}}$",
    "ZH":         r"$\delta\sigma_{\mathrm{ZH}}$",
    "ttH":        r"$\delta\sigma_{\mathrm{ttH}}$",
    "tH (t-ch)":  r"$\delta\sigma_{\mathrm{tH\ (t\mathrm{-}ch)}}$",
    "tH (s-ch)":  r"$\delta\sigma_{\mathrm{tH\ (s\mathrm{-}ch)}}$",
    "tH (W-ass)": r"$\delta\sigma_{\mathrm{tH\ (W\mathrm{-}ass)}}$",
    "bbH":        r"$\delta\sigma_{\mathrm{bbH}}$",
}


# Colored by uncertainty source rather than by depth/position, so the same source always
# reads as the same color across modes: PDFaS (the total) is always red, QCD scale is
# always light blue, and each mode's extra sources get their own blue/pink shade.
SOURCE_COLORS = {
    "PDFaS":         "#c1121f",  # red
    "QCD scale":     "#9ecae1",  # light blue
    "QCD scale+FS":  "#9ecae1",  # light blue
    "EWK":           "#08519c",  # dark blue
    "t,b,c":         "#4292c6",  # medium blue
    "TU":            "#4292c6",  # medium blue
    "virt":          "#4292c6",  # medium blue (matches muB)
    "muB":           "#4292c6",  # medium blue
    "mB":            "#e07a7a",  # pink/red
    "PDFTH":         "#f4a6a6",  # light pink/red
}

# Text shown for each source; anything not listed falls back to its raw key ("QCD scale",
# "QCD scale+FS", "TU" are left as-is).
DISPLAY_LABELS = {
    "PDFaS": r"PDF+$\alpha_s$",
    "PDFTH": "PDF-TH",
    "EWK":   r"$\delta(EWK)$",
    "t,b,c": r"$\delta(t,b,c)$",
    "virt":  r"$\delta_{virt}$",
    "muB":   r"$\mu_b$",
    "mB":    r"$m_B$",
}
# Every label except the QCD scale ones is prefixed with "+ " to read as an additional
# source being switched on.
NO_PREFIX_KEYS = {"QCD scale", "QCD scale+FS"}


def display_label(key):
    text = DISPLAY_LABELS.get(key, key)
    return text if key in NO_PREFIX_KEYS else "+ " + text


STEP_HEIGHT_BASE = 0.55
STEP_HEIGHT_RATIO = 0.68


def step_height(depth):
    return STEP_HEIGHT_BASE * (STEP_HEIGHT_RATIO ** depth)


LABEL_FONTSIZE = 15  # matches xtick.labelsize
ROW_SPACING = 3.2
LABEL_X_GAP_FRAC = 0.03
# Extra horizontal push per step away from the innermost (QCD scale) bar, so labels
# further out don't stay clustered around close-together tips.
LABEL_X_STEP_FRAC = 0.05
# Clears the tallest (depth-0) bar in a row, so inner labels don't sit on top of it.
LABEL_Y_BASE = STEP_HEIGHT_BASE / 2 + 0.18
# Extra step per tier, so a third/fourth label sharing a side stacks further out
# instead of colliding with the first label on that side.
LABEL_Y_STEP = 0.46
# Extra headroom added around the axes so no label is ever clipped by the plot frame.
LABEL_Y_MARGIN = 0.35


def plot_uncertainty_breakdown(mode_keys, filename):
    labels = [production_mode_labels[key] for key in mode_keys]
    y_base = ROW_SPACING * np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(15, 1.9 * len(labels) + 2))

    for spine in ax.spines.values():
        spine.set_linewidth(2.0)
        spine.set_color("black")

    ax.tick_params(axis="both", which="major", width=2, length=6)

    # The horizontal gap between a bar's tip and its label is scaled to this plot's own
    # x-axis range so it stays proportionate whether the panel spans a few percent or
    # tens of percent.
    max_unc = max(abs(v) for key in mode_keys for _, (dn, up) in breakdowns[key] for v in (dn, up))
    label_x_gap = LABEL_X_GAP_FRAC * max_unc
    label_x_step = LABEL_X_STEP_FRAC * max_unc

    label_y_min = y_base[0]
    label_y_max = y_base[-1]
    for i, mode_key in enumerate(mode_keys):
        n_steps = len(breakdowns[mode_key])
        for depth, (label, (dn, up)) in enumerate(breakdowns[mode_key]):
            color = SOURCE_COLORS[label]
            height = step_height(depth)
            ax.barh(
                y_base[i],
                width=up - dn,
                left=dn,
                height=height,
                color=color,
                edgecolor=color,
                linewidth=1.5,
                alpha=1.0,
                zorder=3 + depth,
            )
            # Labels sit right next to their own bar's tip, alternating just above/below
            # the row's midline (innermost bar, e.g. QCD scale, always goes below), so
            # they stay tight around the bars instead of stacking out along the x-axis.
            # A third/fourth label sharing a side steps further out to avoid colliding
            # with the one closer in.
            reverse_depth = (n_steps - 1) - depth
            below = reverse_depth % 2 == 0
            tier = reverse_depth // 2
            offset = LABEL_Y_BASE + tier * LABEL_Y_STEP
            label_y = y_base[i] + offset if below else y_base[i] - offset
            label_y_min = min(label_y_min, label_y)
            label_y_max = max(label_y_max, label_y)
            va = "top" if below else "bottom"
            label_x = up + label_x_gap + reverse_depth * label_x_step
            ax.annotate(
                display_label(label),
                xy=(up, y_base[i]),
                xytext=(label_x, label_y),
                ha="left",
                va=va,
                fontsize=LABEL_FONTSIZE,
                color="black",
                arrowprops=dict(arrowstyle="-", color=color, lw=1, shrinkA=2, shrinkB=2),
                annotation_clip=False,
                zorder=20 + depth,
            )

    ax.axvline(0, color="0.2", linewidth=1.5, zorder=10)

    ax.set_yticks(y_base)
    ax.set_yticklabels(labels, ha="right")
    ax.tick_params(axis="y", pad=8)
    ax.yaxis.tick_left()
    ax.yaxis.set_label_position("left")
    ax.tick_params(axis="y", which="major", left=True, right=False, direction="out", width=2, length=6)

    ax.invert_yaxis()
    # Grow the axes to fully contain the outermost labels, so none of them (e.g. the
    # widest "above" label in the top row) ends up rendered outside the plot frame.
    ax.set_ylim(label_y_max + LABEL_Y_MARGIN, label_y_min - LABEL_Y_MARGIN)

    ax.set_xlabel("Relative uncertainty [%]")
    ax.set_title(r"$\sqrt{s}=14$ TeV, $m_h=125.09$ GeV                   LHC Higgs WG1")

    ax.xaxis.set_major_locator(MultipleLocator(1))

    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    ax.set_xlim(-1.15 * max_unc, 1.15 * max_unc)

    fig.tight_layout()

    fig.savefig(filename, bbox_inches="tight")

    return fig, ax


plot_uncertainty_breakdown(["ggF", "VBF", "WH", "ZH"], "uncertainty_breakdown_ggF_VBF_WH_ZH.pdf")
plot_uncertainty_breakdown(["ttH", "tH (t-ch)", "tH (s-ch)", "tH (W-ass)", "bbH"], "uncertainty_breakdown_ttH_tH_bbH.pdf")

plt.show()

