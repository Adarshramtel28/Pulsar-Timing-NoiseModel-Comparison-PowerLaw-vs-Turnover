# Pulsar Red Noise: Comparing Turnover and Power-law Models with Tempo2 and Enterprise

This repository compares spectral model outputs from **Tempo2** with Bayesian inference using **Enterprise** for red noise in pulsar timing data.


The work builds on the methods and codes developed by the **IIT Roorkee Pulsar Timing Group**.  
My role involved modifying existing code for sampling and usability, along with implementing my own plotting scripts for direct comparisons.

⚠️ **Disclaimer:**  
This repository does not contain raw pulsar data or original pipeline codes (PTMCMC/dynesty). Only modified plotting scripts and example figures are provided.  

The pulsar data used (J0729-1836 and J1910-0309) comes courtesy of the **Indian Pulsar Timing Array (InPTA)**, and I am grateful to the collaboration for access.

This is an exploratory research project. The results are preliminary and have not been independently verified.
---

Credits also go to the developers of [Enterprise][Ellis, J. A., Vallisneri, M., Taylor, S. R., & Baker, P. T. (2020, September 29)] and [Tempo2] [Hobbs, G. B., Edwards, R. T., & Manchester, R. N. (2006)],
including the spectralModel and autospectral plugins [Coles et al.(2012)].

## Project Motivation

Pulsar timing data often exhibit **red noise**, which can be modeled in two main ways:

- **Power-law spectrum** (simple scaling across frequencies)  
- **Turnover spectrum** (flattening at low frequencies)

This project performs a Bayesian comparison of these models for two pulsars, alongside a direct comparison of power spectral densities (PSDs) obtained via:

- **Tempo2** (spectralModel plugin, Coles et al. 2012), utilizing a turnover spectrum.
- **Enterprise** Bayesian sampling, with a Power law spectrum

---


## Steps Taken

For a detailed explanation of the theoretical background (power-law vs turnover models) and a summary of Bayes factor results, see `docs/theory.md`.

**1. Model comparison**  
A Bayesian model comparison was carried out between four noise models, following [Grover et al. 2024](https://doi.org/10.1017/pasa.2024.96):

| Model   | Description |
|---------|-------------|
| **F+RN**  | White noise scaling factor (EFAC) + intrinsic pulsar red noise (simple power law). |
| **WN+RN** | EFAC + white noise error in quadrature (EQUAD) + intrinsic pulsar red noise (power law). |
| **F+CF**  | EFAC + pulsar red noise modeled with a turnover spectrum. |
| **WN+CF** | EFAC + EQUAD + turnover-spectrum red noise. |

- Bayesian inference was performed with the **DYNESTY** package within the **Enterprise** framework.  
- Priors followed the works of [Grover et al. 2024](https://doi.org/10.1017/pasa.2024.96) and [Parthasarathy et al. 2019](https://doi.org/10.1093/mnras/stz2383).  
- Results:  
  - **J0729-1836** favored the F+RN model.  
  - **J1910-0309** favored the WN+RN model.  
  - Neither pulsar favored turnover models.  
- Computed Bayes factors strongly supported the **simple power-law model** as sufficient to explain the noise.

**2. Bayesian sampling**  
Ran Bayesian parameter estimation with Enterprise under a simple power-law assumption.

**3. Posterior analysis**  
Extracted posterior distributions and produced power spectral density (PSD) estimates.

**4. Tempo2 PSDs**  
Ran the **Tempo2 spectralModel** plugin (with turnover) to obtain independent PSD estimates.

**5. Comparison**  
Overlaid Enterprise-derived and Tempo2-derived PSDs for two pulsars and compared.

**6. Corner plots**  
Produced corner plots of sampled parameters for transparency.

---

## Key Results

- Bayes factor comparisons indicated that the **turnover model is not favored** over the simple power-law model in this case study.  
- **Conclusion:** For the pulsars analyzed, a simple power law suffices. More sensitive data or additional pulsars would be required to decisively distinguish turnover features.

---

## How to Run the Code

- Plotting scripts: `scripts/` 
- Example notebook with PSD overlays: `notebooks/`  
  - ⚠️ These notebooks require external `.dat` and `chains-1.txt` files, which are not included in this repository.  
- Figures: `results/`  


---

## Acknowledgments & References

- **Enterprise developers** — Ellis, J. A., Vallisneri, M., Taylor, S. R., & Baker, P. T. (2020). *ENTERPRISE: Enhanced Numerical Toolbox Enabling a Robust PulsaR Inference SuitE (v3.0.0)*. Zenodo. [doi:10.5281/zenodo.4059815](http://doi.org/10.5281/zenodo.4059815)  
- **Tempo2 team** — Hobbs, G. B., Edwards, R. T., & Manchester, R. N. (2006). *Tempo2, a new pulsar-timing package – I. An overview.*  
- **InPTA collaboration** — Joshi, B.C., Arumugasamy, P., Bagchi, M. et al. (2018). *Precision pulsar timing with the ORT and the GMRT and its applications in pulsar astrophysics.* J Astrophys Astron 39
- **IIT Roorkee pulsar timing group** for their support and guidance.[Grover H, Joshi BC, Singha J, et al.][https://doi.org/10.1017/pasa.2024.96].
