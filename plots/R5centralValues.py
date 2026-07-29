
# Central values of the cross-sections, from the R5 and YR4. 
# All for mH=125.09 GeV at 14 TeV.

CentralValues = {
    "ggF": {
        "R5": 
        "YR4": 
    }
}

# Uncertainties on the cross-sections (down, up) in percent, from the R5. 
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
