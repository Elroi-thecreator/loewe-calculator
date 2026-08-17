"""
Loewe Additivity and Combination Index (CI) Analysis in Python
Provides utilities to:
1. Calculate Loewe CI from known equipotent doses.
2. Invert 4-Parameter Logistic (4PL / Hill) dose-response curves.
3. Compute and plot an Isobologram.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def loewe_ci(d_A, d_B, D_A, D_B):
    """
    Calculate Loewe Combination Index (CI).
    CI = (d_A / D_A) + (d_B / D_B)
    """
    d_A, d_B, D_A, D_B = np.asarray(d_A), np.asarray(d_B), np.asarray(D_A), np.asarray(D_B)
    return (d_A / D_A) + (d_B / D_B)


def hill_4pl(dose, bottom, top, ec50, hill_slope):
    """
    4-Parameter Logistic (4PL) Hill Dose-Response Equation:
    E(D) = Bottom + (Top - Bottom) / (1 + (EC50 / D)^HillSlope)
    """
    return bottom + (top - bottom) / (1.0 + (ec50 / np.maximum(dose, 1e-12)) ** hill_slope)


def invert_hill(effect, bottom, top, ec50, hill_slope):
    """
    Inverts the 4PL curve to solve for the dose D that produces a given effect E.
    """
    normalized_frac = (effect - bottom) / (top - effect)
    if normalized_frac <= 0:
        return np.nan
    return ec50 * (normalized_frac ** (1.0 / hill_slope))


def plot_isobologram(D_A, D_B, d_A, d_B, unit="uM", save_path="isobologram.png"):
    """
    Generate and save a publication-ready Isobologram plot.
    """
    ci = loewe_ci(d_A, d_B, D_A, D_B)
    
    plt.figure(figsize=(7, 6))
    
    # Line of additivity
    plt.plot([0, D_A], [D_B, 0], 'b--', lw=2, label='Loewe Additivity Line (CI = 1.0)')
    
    # Synergy region shading
    plt.fill_between([0, D_A], [D_B, 0], 0, color='green', alpha=0.1, label='Synergy Zone (CI < 1)')
    
    # Observed point
    point_color = 'green' if ci < 0.9 else ('blue' if ci <= 1.1 else 'red')
    label_txt = f'Observed Combo (dA={d_A}, dB={dB})\nCI = {ci:.2f}'
    plt.scatter([d_A], [d_B], color=point_color, s=120, zorder=5, label=label_txt)
    
    plt.xlim(0, max(D_A, d_A) * 1.2)
    plt.ylim(0, max(D_B, d_B) * 1.2)
    plt.xlabel(f'Drug A Dose ({unit})', fontweight='bold')
    plt.ylabel(f'Drug B Dose ({unit})', fontweight='bold')
    plt.title(f'Isobologram Analysis (CI = {ci:.2f})', fontweight='bold', fontsize=13)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[✓] Saved isobologram plot to {save_path}")


if __name__ == '__main__':
    # Demonstration
    D_A = 100.0  # Solo equipotent dose for Drug A
    D_B = 50.0   # Solo equipotent dose for Drug B
    dA = 25.0    # Combo dose Drug A
    dB = 15.0    # Combo dose Drug B

    ci = loewe_ci(dA, dB, D_A, D_B)
    classification = "Synergy" if ci < 0.9 else ("Additivity" if ci <= 1.1 else "Antagonism")
    
    print("=" * 45)
    print("LOEWE ADDITIVITY ANALYSIS RESULTS")
    print("=" * 45)
    print(f"Drug A Solo IC50 (D_A) : {D_A}")
    print(f"Drug B Solo IC50 (D_B) : {D_B}")
    print(f"Combo Dose A (d_A)     : {dA}")
    print(f"Combo Dose B (d_B)     : {dB}")
    print(f"Combination Index (CI) : {ci:.4f}")
    print(f"Outcome                : {classification}")
    print("=" * 45)

    plot_isobologram(D_A, D_B, dA, dB, unit="µM", save_path="isobologram_demo.png")
