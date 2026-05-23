//! Rolling mean/std methane anomaly flags.

/// Rolling mean with `mode="same"` (ones(window)/window convolution).
pub fn rolling_mean_same(methane: &[f64], window: usize) -> Vec<f64> {
    let n = methane.len();
    let w = window.max(1);
    let mut conv = vec![0.0; n];
    for i in 0..n {
        let mut sum = 0.0;
        let mut count = 0usize;
        for j in 0..w {
            let idx = i as isize + j as isize - (w as isize / 2);
            if idx >= 0 && (idx as usize) < n {
                sum += methane[idx as usize];
                count += 1;
            }
        }
        conv[i] = sum / count.max(1) as f64;
    }
    conv
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
