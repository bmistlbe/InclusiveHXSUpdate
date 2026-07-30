# Code that produces a plot showing the contribution of each source of uncertainty to the whole. The uncertainties are sequentially included in the total, starting from QCD scale and ending with PDF+aS, with the order of what comes in-between specified further down in the script. 
# The result is two bar charts (one for VBF, ggF, WH and ZH, and one for the rest) showing how the uncertainty increases as components are included. 
# Code started by Robin and extended by Claude.
# Run with `python R5breakdown.py`. Output `uncertainty_breakdown_*.pdf` where * lists production modes

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

# Uncertainties on the cross-sections (down, up) in percent. All on mH=125.09 GeV at 14 TeV.
# The uncertainty names here are used later to feed into functions calculating the total uncertainty, and to specify the label and colour of the uncertainty, so make sure not to change them.
# Entries are ordered largest-bar-first: the first key is always the full total (PDFaS),
# and the last key is the smallest, innermost bar. See `uncertainty_steps`.
data = {
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


zero = (0.0, 0.0)


def uncertainty_steps(mode_key):
    """Build up from all sources zero to all sources at their quoted values, adding one
    source at a time in reverse dictionary order. Depth 0 is the full total (every source
    added); depth d has the first d sources (in dict order) still zeroed. Each step is
    labelled by the source that was just switched on, i.e. `keys[depth]`."""
    keys = list(data[mode_key].keys())
    func = total_funcs[mode_key]
    steps = []
    for depth in range(len(keys)):
        kwargs = {k: (data[mode_key][k] if i >= depth else zero) for i, k in enumerate(keys)}
        steps.append((keys[depth], func(**kwargs)))
    return steps


breakdowns = {mode_key: uncertainty_steps(mode_key) for mode_key in total_funcs}

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
# always light blue, and each mode's extra sources get their own shade.
SOURCE_COLORS = {
    "PDFaS":       "#c1121f",  # red
    "QCDscale":    "#6bb5da",  # blue
    "QCDscaleFS":  "#6bb5da",  # blue
    "EWK":         "#a946a2",  # purple
    "tbc":         "#08519c",  # dark blue
    "TU":          "#eeb800",  # deep yellow
    "virt":        "#1b5e20",  # dark green
    "muB":         "#6fbf73",  # light green
    "mB":          "#8c564b",  # brown
    "PDFTH":       "#f4a6a6",  # light pink/red
}

# Text shown for each source; anything not listed falls back to its raw key ("TU" is
# left as-is).
DISPLAY_LABELS = {
    "PDFaS":      r"PDF+$\alpha_s$",
    "PDFTH":      "PDF-TH",
    "EWK":        r"$\delta(EWK)$",
    "tbc":        r"$\delta(t,b,c)$",
    "virt":       r"$\delta_{virt}$",
    "muB":        r"$\mu_b$",
    "mB":         r"$m_B$",
    "QCDscale":   "QCD scale",
    "QCDscaleFS": "QCD scale+FS",
}
# QCD scale (and its tH variant) is the base against which everything else is combined,
# so it gets no prefix and is always listed first in the legend.
NO_PREFIX_KEYS = {"QCDscale", "QCDscaleFS"}
# Sources added in quadrature get a "+ in a circle" (i.e. "in quadrature") prefix;
# everything else (besides QCD scale) is added linearly and gets a plain "+".
QUADRATURE_KEYS = {"PDFaS", "virt", "muB", "mB"}


def legend_entries(mode_keys):
    """Legend rows for these modes, ordered to match the bars themselves: QCD scale
    (smallest, innermost) first, PDFaS (the total, largest) last, everything else in
    between ordered smallest-to-largest. Returns (key, display_text) pairs, with the
    production mode appended in brackets for any source unique to a single mode."""
    modes_for_key = {}
    order_info = {}
    next_index = 0
    for mode_key in mode_keys:
        n = len(breakdowns[mode_key])
        for depth, (label, _) in enumerate(breakdowns[mode_key]):
            modes_for_key.setdefault(label, set()).add(mode_key)
            if label not in order_info:
                reverse_depth = (n - 1) - depth
                order_info[label] = (reverse_depth, next_index)
                next_index += 1

    def sort_key(item):
        return order_info[item]

    qcd_keys = sorted((k for k in order_info if k in NO_PREFIX_KEYS), key=sort_key)
    total_keys = sorted((k for k in order_info if k == "PDFaS"), key=sort_key)
    other_keys = sorted(
        (k for k in order_info if k not in NO_PREFIX_KEYS and k != "PDFaS"),
        key=sort_key,
    )

    entries = []
    for key in qcd_keys + other_keys + total_keys:
        text = DISPLAY_LABELS.get(key, key)
        if key not in NO_PREFIX_KEYS:
            prefix = r"$\oplus$" if key in QUADRATURE_KEYS else "+"
            text = f"{prefix} {text}"
        if len(modes_for_key[key]) == 1:
            text = f"{text} ({next(iter(modes_for_key[key]))})"
        entries.append((key, text))
    return entries


STEP_HEIGHT_BASE = 0.55
STEP_HEIGHT_RATIO = 0.68


def step_height(depth):
    return STEP_HEIGHT_BASE * (STEP_HEIGHT_RATIO ** depth)


LABEL_FONTSIZE = 15  # matches xtick.labelsize
ROW_SPACING = 1.0


def plot_uncertainty_breakdown(mode_keys, filename, qcd_label_override=None, legend_order=None):
    """Plot the nested uncertainty-breakdown bars for `mode_keys` and save to `filename`.

    `qcd_label_override`, if given, replaces the legend text for "QCD scale" and merges
    it with "QCD scale+FS" into a single entry. `legend_order`, if given, is a list of
    `data` keys giving an explicit legend row order, overriding the default
    smallest-to-largest ordering for the keys it lists.
    """
    labels = [production_mode_labels[key] for key in mode_keys]
    y_base = ROW_SPACING * np.arange(len(labels))

    max_unc = max(abs(v) for key in mode_keys for _, (dn, up) in breakdowns[key] for v in (dn, up))
    # Figure width and tick spacing scale with this plot's own x-axis range, so a panel
    # spanning tens of percent doesn't cram its tick labels into a narrow, fixed-width axes.
    fig_width = 7 + 0.4 * max_unc
    tick_step = 1 if max_unc <= 10 else 2

    fig, ax = plt.subplots(figsize=(fig_width, 0.8 * len(labels) + 1.5))

    for spine in ax.spines.values():
        spine.set_linewidth(2.0)
        spine.set_color("black")

    ax.tick_params(axis="both", which="major", width=2, length=6)

    for i, mode_key in enumerate(mode_keys):
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

    ax.axvline(0, color="0.2", linewidth=1.5, zorder=10)

    for y_prev, y_next in zip(y_base[:-1], y_base[1:]):
        ax.axhline((y_prev + y_next) / 2, color="0.2", linestyle="--", linewidth=1.0, alpha=0.5, zorder=0)

    ax.set_yticks(y_base)
    ax.set_yticklabels(labels, ha="right")
    ax.tick_params(axis="y", pad=8)
    ax.yaxis.tick_left()
    ax.yaxis.set_label_position("left")
    ax.tick_params(axis="y", which="major", left=True, right=False, direction="out", width=2, length=6)

    ax.invert_yaxis()

    ax.set_xlabel("Relative uncertainty [%]")
    ax.set_title(r"$\sqrt{s}=14$ TeV, $m_h=125.09$ GeV                   LHC Higgs WG1")

    ax.xaxis.set_major_locator(MultipleLocator(tick_step))

    ax.grid(axis="x", linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    ax.set_xlim(-1.15 * max_unc, 1.15 * max_unc)

    entries = legend_entries(mode_keys)
    if qcd_label_override is not None:
        # Merge "QCD scale" and "QCD scale+FS" into a single entry (they're the same
        # color anyway), replacing their text with the given override.
        merged = False
        deduped = []
        for key, text in entries:
            if key in NO_PREFIX_KEYS:
                if not merged:
                    deduped.append((key, qcd_label_override))
                    merged = True
            else:
                deduped.append((key, text))
        entries = deduped

    if legend_order is not None:
        order_index = {key: i for i, key in enumerate(legend_order)}
        entries = sorted(entries, key=lambda kv: order_index.get(kv[0], len(order_index)))

    legend_handles = [
        Patch(facecolor=SOURCE_COLORS[key], edgecolor=SOURCE_COLORS[key], label=text)
        for key, text in entries
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper right",
        frameon=True,
        framealpha=1,
        edgecolor="black",
        fancybox=False,
        fontsize=LABEL_FONTSIZE,
    )

    fig.tight_layout()

    fig.savefig(filename, bbox_inches="tight")

    return fig, ax


plot_uncertainty_breakdown(
    ["ggF", "VBF", "WH", "ZH", "ttH", "tH (t-ch)", "tH (s-ch)", "tH (W-ass)", "bbH"],
    "uncertainty_breakdown_all.pdf",
    qcd_label_override="QCD scale (+FS for ttH/tH)",
    legend_order=["QCDscale", "tbc", "EWK", "PDFTH", "TU", "virt", "muB", "mB", "PDFaS"],
)

plt.show()

