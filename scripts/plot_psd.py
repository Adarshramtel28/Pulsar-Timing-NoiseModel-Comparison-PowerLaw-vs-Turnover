
'''
The files required here for comparison are as follows :
1. tempo2 files obtained after using the spectralModel plugin
2. chains file obtianed after sampling parameter using ptmcmcsampler

'''



import numpy as np
import matplotlib.pyplot as plt


# --- Load chain ---
chain = np.loadtxt('chain_1_729.txt')   # shape (Nsamples, Nparams)


# --- Apply burn-in ---
pct = 0.3
burn = int(pct * chain.shape[0])
post = chain[burn:]


# --- Map chain columns to parameters ---
# my sampling order: EFAC, gamma, log10_A
'''can use : for i, name in enumerate(pta.param_names):
    print(i, name)

    in enterprise modelling script to determine indices '''

efac_samples = post[:, 0]
efac_samples     = post[:, 0]  # EFAC
gamma_samples    = post[:, 1]  # red noise spectral index
log10A_samples   = post[:, 2]  # red noise log10 amplitude


# --- Frequency grid from tempo2 ---

f_t2 = np.loadtxt('cholSpec_729.dat')  # raw frequencies
f_t2 = f_t2[:,0] *365.25               # in order to convert to 1/yr frequency 


# --- Posterior PSD draws on same grid as Tempo2 ---
idx_draws = np.random.choice(len(log10A_samples), size=500, replace=False)


# --- Reference frequency (1/yr) ---
f_ref = 1.0


def S_from_logA_gamma(f, log10A, gamma, f_ref=1.0):
    # f and f_ref must be in same units (we use 1/yr)

    A = 10.0**(log10A)                    # A defined at f_ref (dimensionless)
    return (A**2 / (12.0 * np.pi**2)) * (f / f_ref)**(-gamma)


psd_draws = np.array([
    S_from_logA_gamma(f_t2, log10A_samples[i], gamma_samples[i])
    for i in idx_draws
])


psd_median = np.median(psd_draws, axis=0)
psd_lower = np.percentile(psd_draws, 5, axis=0)
psd_upper = np.percentile(psd_draws, 95, axis=0)


# --- Load tempo2 outputs ---
comp = np.loadtxt('comp_729.dat')        # raw PSD
chol = np.loadtxt('cholSpec_729.dat')    # tempo2 spectral model


#convert to 1/yr
chol[:,0] *= 365.25
comp[:,0] *=  365.25



# --- Plot ---
plt.figure(figsize=(7,5))
plt.loglog(comp[:,0], comp[:,1], color='C0', label='Raw PSD (comp.dat)', alpha=0.6)
plt.loglog(chol[:,0], chol[:,1], color='C1', label='Tempo2 model (cholSpec.dat)', lw=1.5, alpha = 0.8)


# --- Plot Bayesian PSD on same freq grid ---
plt.fill_between(f_t2, psd_lower, psd_upper, color="green", alpha=0.5, label="Bayes posterior 90%")
plt.plot(f_t2, psd_median, color="green", lw=2, label="Bayes median (power-law)")


plt.xlabel('Frequency [1/yr]')
plt.ylabel('PSD')
plt.legend()
plt.tight_layout()
plt.show()