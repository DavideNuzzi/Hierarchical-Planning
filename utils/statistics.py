import numpy as np
from scipy.stats import mannwhitneyu, wilcoxon


def mann_whitney_effect_size(x1, x2, wendt_formula=True):

    n1 = len(x1)
    n2 = len(x2)

    u_stat, p_val = mannwhitneyu(x1, x2, alternative='two-sided', method='asymptotic')
    
    if wendt_formula:
        r = (2 * u_stat) / (n1 * n2) - 1
    else:
        z = (u_stat - n1*n2/2) / np.sqrt(n1*n2*(n1 + n2 + 1)/12)
        r = z / np.sqrt(n1 + n2)

    return p_val, r


def wilcoxon_effect_size(x1, x2):

    W, p_val = wilcoxon(x1, x2, alternative='two-sided')
    diffs = x1 - x2
    n = np.sum(diffs != 0)

    mu_W = n * (n + 1) / 4
    sigma_W = np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    Z = (W - mu_W) / sigma_W
    r = Z / np.sqrt(n)
    return p_val, r


def false_discovery(p_values):

    p_sorted_inds = np.argsort(p_values)
    N = len(p_sorted_inds)
    p_values_corrected = np.zeros(len(p_values))

    for i in range(len(p_sorted_inds)):
        p_ind = p_sorted_inds[i]
        p = p_values[p_ind]
        p_mod = p * N / (i + 1)
        p_values_corrected[p_ind] = p_mod

    return p_values_corrected
