use detecting_pipeline_leaks_from_space_multi_sensor_satellite_monitoring_at_scale_with_databricks_core::rolling_anomaly_flags;
use numpy::{PyArray1, PyReadonlyArray1, IntoPyArray};
use pyo3::prelude::*;

#[pyfunction]
fn rolling_anomaly_flags_py<'py>(py: Python<'py>, methane: PyReadonlyArray1<f64>, window: usize, sigma_mult: f64) -> PyResult<Bound<'py, PyArray1<f64>>> {
    Ok(rolling_anomaly_flags(methane.as_slice()?, window, sigma_mult).into_pyarray(py))
}

#[pyfunction]
#[pyo3(signature = (methane, window=14, sigma_mult=3.0, iterations=2_000))]
fn bench_kernel_py(methane: PyReadonlyArray1<f64>, window: usize, sigma_mult: f64, iterations: usize) -> PyResult<f64> {
    let m = methane.as_slice()?.to_vec();
    let start = std::time::Instant::now();
    for _ in 0..iterations { let _ = rolling_anomaly_flags(&m, window, sigma_mult); }
    Ok(start.elapsed().as_secs_f64())
}

#[pymodule]
fn detecting_pipeline_leaks_from_space_multi_sensor_satellite_monitoring_at_scale_with_databricks_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rolling_anomaly_flags_py, m)?)?;
    m.add_function(wrap_pyfunction!(bench_kernel_py, m)?)?;
    Ok(())
}
