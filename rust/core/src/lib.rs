//! Rolling mean/std methane anomaly flags.

/// Rolling mean with `mode="same"` (ones(window)/window convolution).
pub fn rolling_mean_same(methane: &[f64], window: usize) -> Vec<f64> {
    let n = methane.len();
    let w = window.max(1);
    if n == 0 {
        return vec![];
    }
    let pad = (w - 1) / 2;
    let mut full = vec![0.0; n + w - 1];
    for k in 0..full.len() {
        let mut sum = 0.0;
        for j in 0..w {
            let ai = k as isize - j as isize;
            if ai >= 0 && (ai as usize) < n {
                sum += methane[ai as usize];
            }
        }
        full[k] = sum / w as f64;
    }
    full[pad..pad + n].to_vec()
}

pub fn rolling_std_window(methane: &[f64], window: usize) -> Vec<f64> {
    let n = methane.len();
    let w = window.max(1);
    let mut out = vec![0.0; n];
    for i in 0..n {
        let start = i.saturating_sub(w);
        let end = (i + w).min(n);
        let slice = &methane[start..end];
        let mean = slice.iter().sum::<f64>() / slice.len().max(1) as f64;
        let var = slice.iter().map(|x| (x - mean).powi(2)).sum::<f64>() / slice.len().max(1) as f64;
        out[i] = var.sqrt();
    }
    out
}

/// Returns 1.0 where methane > rolling_mean + sigma_mult * rolling_std.
pub fn rolling_anomaly_flags(methane: &[f64], window: usize, sigma_mult: f64) -> Vec<f64> {
    let mean = rolling_mean_same(methane, window);
    let std = rolling_std_window(methane, window);
    methane
        .iter()
        .enumerate()
        .map(|(i, &v)| {
            if v > mean[i] + sigma_mult * std[i] {
                1.0
            } else {
                0.0
            }
        })
        .collect()
}
