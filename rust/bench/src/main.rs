use detecting_pipeline_leaks_from_space_multi_sensor_satellite_monitoring_at_scale_with_databricks_core::rolling_anomaly_flags;
fn main() { let m: Vec<f64>=(0..5000).map(|i| (i as f64*0.01).sin()+2.0).collect(); for _ in 0..2000 { let _=rolling_anomaly_flags(&m,14,3.0); } }
