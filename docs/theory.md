# Theory and Results: Power-law vs Turnover Red Noise Models

## Background

Pulsar timing data often exhibit **red noise** (low-frequency noise). Two commonly used spectral forms are:

- **Power-Law Spectrum**[https://github.com/nanograv/enterprise/blob/master/enterprise/signals/gp_priors.py]

This is the standard model for red noise, where the noise power decreases with frequency $f$ according to a spectral index $\gamma$. It's a simple and robust model for many astrophysical processes.

The spectral shape is defined as:
$$
P(f) \propto f^{-\gamma}
$$
The fully parameterized form used in the analysis is:
$$
P(f) = \frac{A^2}{12\pi^2} (f_{\text{yr}})^{\gamma - 3} f^{-\gamma}
$$

**Parameters:**
* **$A$**: The dimensionless amplitude of the red noise, typically specified as `log10_A`.
* **$\gamma$**: The spectral index, which determines the steepness of the spectrum.

---

- **Turnover Spectrum**[https://github.com/nanograv/enterprise/blob/master/enterprise/signals/gp_priors.py]

This model extends the simple power law by introducing a suppression of power below a certain "corner" frequency, $f_c$. 

The spectrum is modeled as:
$$
P(f) = P_0 \left( \frac{f}{f_{\text{yr}}} \right)^{-\gamma} \left[ 1 + \left(\frac{f_c}{f}\right)^\kappa \right]^{-2\beta}
$$
where $P_0 = \frac{A^2}{12\pi^2 f_{\text{yr}}^3}$ is a constant amplitude factor.

**Parameters:**
* **$A$**: The intrinsic amplitude of the process, specified as `log10_A`.
* **$\gamma$**: The spectral index at high frequencies ($f \gg f_c$).
* **$f_c$**: The corner frequency below which the spectrum "turns over" or flattens, specified as `lf0` ($\log_{10}f_c$).
* **$\kappa$**: A parameter that controls the steepness of the turnover.
* **$\beta$**: An additional parameter that provides flexibility in shaping the turnover.

The aim: determine whether a turnover model is required, or whether a simple power law suffices.

---

## Models compared

| Short name | Description |
|------------|-------------|
| **F+RN**   | EFAC + intrinsic red noise (power law). |
| **WN+RN**  | EFAC + EQUAD + intrinsic red noise (power law). |
| **F+CF**   | EFAC + red noise with turnover (corner frequency). |
| **WN+CF**  | EFAC + EQUAD + turnover red noise. |
| **WN**     | (white-noise only model) |

Bayesian evidence (\(\log Z\)) was computed using **Enterprise** with **DYNESTY**. Priors followed Grover et al. (2024) and Parthasarathy et al. (2019). Following the conventions of Kass & Raftery (1995), we interpret Bayes factors (Δlog Z) using the scale:
\[
\Delta\log Z = \log Z_{\text{best}} - \log Z_{\text{model}}.
\]
Larger positive \(\Delta\log Z\) indicates stronger evidence **against** the tested model when compared to the best fit model.

A practical interpretation guide (approximate):
- \(\Delta\log Z \lesssim 1\): negligible / inconclusive  
- \(1 \lesssim \Delta\log Z \lesssim 3\): weak-to-moderate evidence  
- \(3 \lesssim \Delta\log Z \lesssim 5\): strong evidence  
- \(\Delta\log Z \gtrsim 5\): very strong / decisive evidence

> **Note:** Each reported \(\log Z\) has sampling uncertainty (± value). When \(\Delta\log Z\) is comparable to the \(\log Z\) uncertainties, interpret the result cautiously.

---

## Results — Bayes factors

### Pulsar **J0729-1836**
Best model: **F+RN** 

| Model    | \(\Delta\log Z = \log Z_{\text{best}} - \log Z_{\text{model}}\) |
|----------|------------------------------------------------------------------:|
| **F+RN** | 0.0000 |
| WN+RN    | 0.8922 |
| F+CF     | 3.6256 |
| WN+CF    | 4.0663 |

**Interpretation (J0729-1836):**
- F+RN is the preferred model.
- Turnover models (F+CF, WN+CF) are **disfavored** with \(\Delta\log Z \approx 3.6\)–4.1 → **evidence against turnover**(Kass and Raftery 1995).
- WN+RN is mildly disfavored (\(\Delta\log Z \approx 0.89\)): this is on the cusp of the "negligible → weak" scale, so EFAC vs EFAC+EQUAD choice is not decisively different but F+RN is the better fit here.

### Pulsar **J1910-0309** 
Best model: **WN+RN** 

| Model    | \(\Delta\log Z = \log Z_{\text{best}} - \log Z_{\text{model}}\) |
|----------|-----------------------------------------------------------------:|
| **WN+RN**| 0.0000 |
| F+RN     | 0.0814 |
| WN       | 9.3767 |
| F+CF     | 9.7425 |
| WN+CF    | 9.7598 |

**Interpretation (J1910-0309):**
- WN+RN is nominally the best model, but **F+RN is essentially tied** with \(\Delta\log Z \approx 0.08\), which is **much smaller than the reported sampling uncertainties** (~0.17–0.18). Thus **no significant preference** between WN+RN and F+RN — they are effectively equivalent given the uncertainties.
- The turnover models (F+CF, WN+CF), and the purely white-noise model (WN) are ** disfavored** relative to the best model (\(\Delta\log Z \approx 9.4\)–9.8 → **decisive**).

---

## Overall interpretation 

- **Both pulsars prefer simple power-law descriptions** of red noise.  
- For J0729-1836, there is evidence against turnover models (\(\Delta\log Z \gtrsim 3.6\)).  
- For J1910-0309, turnover models are disfavored (\(\Delta\log Z \gtrsim 9\)), and the small difference between WN+RN and F+RN is **not significant** compared to sampling uncertainties.
- To detect a turnover robustly one would likely need longer baselines or more sensitive timing to increase evidence separation, and a larger pulsar sample[Parthasarathy A., et al. (2019)].

---

## References

- Grover H., Joshi B.C., Singha J., et al. (2024). *PASA*. [doi:10.1017/pasa.2024.96]  
- Parthasarathy A., et al. (2019). *MNRAS, 489, 3810*. [doi:10.1093/mnras/stz2383]  
- Robert E. Kass, Adrian E. Raftery, Bayes Factors, Journal of the American Statistical Association, Vol. 90, No. 430 (Jun., 1995), pp. 773-795.
