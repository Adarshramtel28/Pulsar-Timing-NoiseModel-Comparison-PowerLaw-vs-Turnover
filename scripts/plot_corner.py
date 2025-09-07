
"""
Posterior plot generator for PTA red noise models.

Reads PTMCMCSampler output (chains_1.txt) and produces:
- Corner plots of posterior distributions
- 1D histograms with credible intervals
"""

import numpy as np
import matplotlib.pyplot as plt
import corner
import os



CHAIN_FILE = "chain_1_J1910.txt"   # enter your file path here
BURN_IN_FRAC = 0.25  # discard 25% of chain

# Example param indices (replace with your own using pta.param_names.index(...))
INDICES = {
    "EFAC": 0,           # example: first column
    "EQUAD" : 1,
    r"$\gamma_\mathrm{red}$": 2,
    r"$\log_{10}A_\mathrm{red}$": 3,
}


labels = ['EFAC',"$\gamma_\mathrm{red}$",r"$\log_{10}A_\mathrm{red}$"]

def load_chain(chain_file, burn_in_frac=0.25):
    """
    Load MCMC chain as NumPy array and drop burn-in.
    """
    if not os.path.exists(chain_file):
        raise FileNotFoundError(f"Chain file {chain_file} not found!")

    chain = np.loadtxt(chain_file)
    burn = int(burn_in_frac * chain.shape[0])
    return chain[burn:, :]


def make_corner(chain, indices, psr_name="PSR J1910-0309", outname="posterior_corner.png"):
    """
    Make corner plot from selected parameter indices, with enhanced labels and title.

    Parameters
    ----------
    chain : np.ndarray
        MCMC chain array (samples x parameters)
    indices : dict
        Dictionary mapping label -> column index in chain
    psr_name : str
        Pulsar name to include in the title
    outname : str
        Output file name for the figure
    """
    cols = list(indices.values())
    labels = list(indices.keys())

    fig = corner.corner(
        chain[:, cols],
        labels=labels,
        label_kwargs={"fontsize": 14, "fontweight": "bold"},
        levels=[0.68, 0.95],
        plot_datapoints=False,
        fill_contours=True,
        show_titles=True,
        title_fmt=".2f",
        title_kwargs={"fontsize": 12, "fontweight": "bold"},
        color="darkgreen"
    )

    # Add main title above the figure
    fig.suptitle(f"Posterior for {psr_name}", fontsize=16, fontweight="bold", y=1.02)

    # Optional: adjust spacing to fit the title
    fig.tight_layout()
    fig.subplots_adjust(top=0.92)  # leave space for suptitle

    fig.savefig(outname, dpi=200, bbox_inches="tight")
    print(f"[OK] Corner plot saved to {outname}")


def make_marginals(chain, indices, outdir="marginals"):
    """
    Make 1D marginal histograms with credible intervals.
    """
    os.makedirs(outdir, exist_ok=True)

    for label, idx in indices.items():
        samples = chain[:, idx]
        q16, q50, q84 = np.percentile(samples, [16, 50, 84])
        q2p5, q97p5 = np.percentile(samples, [2.5, 97.5])

        plt.figure()
        plt.hist(samples, bins=40, density=True, color="skyblue", alpha=0.7)
        plt.axvline(q50, color="k", lw=2, label=f"Median = {q50:.2f}")
        plt.axvspan(q16, q84, color="orange", alpha=0.3, label="68% CI")
        plt.axvspan(q2p5, q97p5, color="red", alpha=0.15, label="95% CI")
        plt.xlabel(label, fontsize=14)
        plt.ylabel("Posterior density", fontsize=12)
        plt.legend(fontsize=10)
        plt.tight_layout()
        outfile = f"{outdir}/{label.strip('$').replace('\\', '')}_posterior.png"
        plt.savefig(outfile, dpi=200)
        plt.close()

        print(f"[OK] Marginal for {label} saved to {outfile}")


if __name__ == "__main__":
    chain = load_chain(CHAIN_FILE, BURN_IN_FRAC)
    make_corner(chain, INDICES, outname="posterior_corner.png")
    make_marginals(chain, INDICES)
