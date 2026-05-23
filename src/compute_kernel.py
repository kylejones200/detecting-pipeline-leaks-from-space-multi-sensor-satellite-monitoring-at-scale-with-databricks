import numpy as np

def rolling_mean_same(methane, window):
    k = np.ones(window) / window
    return np.convolve(methane, k, mode="same")

def rolling_std_window(methane, window):
    n = len(methane)
    out = np.empty(n)
    for i in range(n):
        sl = methane[max(0, i - window): min(n, i + window)]
        out[i] = sl.std()
    return out

def rolling_anomaly_flags(methane, window=14, sigma_mult=3.0):
    m = np.asarray(methane, dtype=float)
    mean = rolling_mean_same(m, window)
    std = rolling_std_window(m, window)
    return (m > mean + sigma_mult * std).astype(float)
