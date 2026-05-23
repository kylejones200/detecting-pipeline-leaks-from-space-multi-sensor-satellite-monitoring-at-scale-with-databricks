# Detecting Pipeline Leaks from Space Multi Sensor Satellite Monitoring at Scale with Databricks

Published: 2025-10-24
Medium: [https://medium.com/@kyle-t-jones/detecting-pipeline-leaks-from-space-multi-sensor-satellite-monitoring-at-scale-with-databricks-6d28bc1e4eea](https://medium.com/@kyle-t-jones/detecting-pipeline-leaks-from-space-multi-sensor-satellite-monitoring-at-scale-with-databricks-6d28bc1e4eea)

## Business context

When the Nord Stream pipeline ruptured in September 2022, satellite data detected the leak before official confirmation. TROPOMI measured methane plumes reaching 40 km downstream. Sentinel-2 captured surface disturbances in the Baltic Sea. Sentinel-1 SAR showed coherence loss in the water column. The satellites saw what happened hours before inspection crews could reach the remote location.

Pipeline operators spend billions on inline inspection and aerial surveys, but 95% of the infrastructure goes unmonitored on any given day. A 100,000 km midstream network would require 274 helicopters flying every day to achieve weekly coverage. Satellites image the entire system daily, regardless of terrain, weather, or access restrictions.

Modern satellite systems detect leaks through multiple physical signals: methane absorption in atmospheric columns (TROPOMI), vegetation stress from hydrocarbon exposure (Sentinel-2 multispectral), and ground deformation or surface changes (Sentinel-1 SAR). The challenge isn't data availability --- it's building a scalable pipeline that ingests terabytes of satellite imagery, extracts leak signatures near the right-of-way, scores tiles by anomaly, and presents prioritized inspection targets to field crews.

## About

Place the code for this article in this repository.
The original article export is saved as `article.md`.

## Files

Add your `.ipynb`, `.py`, `.yaml`, `.js`, `.ts`, or other project files here.

## Rust performance port

Side-by-side **Python vs Rust** implementation of the numeric hot loop — rolling methane anomaly flags. Reference PyO3 benchmark: **~180×** on a release build (local machine; run `benchmark_rust.py` to reproduce).

| Path | Role |
|------|------|
| `src/compute_kernel.py` | Python/numpy reference kernel |
| `rust/core/` | Pure Rust library |
| `rust/py/` | PyO3 bindings |
| `rust/bench/` | Standalone CLI benchmark |
| `benchmark_rust.py` | Python vs Rust timing + correctness check |

```bash
# Rust-only CLI benchmark
cd rust && cargo run --release -p detecting_pipeline_leaks_from_space_multi_sensor_satellite_monitoring_at_scale_with_databricks_bench

# Python vs Rust (PyO3)
pip install maturin numpy
maturin develop --release -m rust/py/Cargo.toml
python benchmark_rust.py
```

Python ML training, solvers, and orchestration stay in Python; Rust targets the numeric hot loops. Stochastic generators validate output shapes; deterministic kernels match at tight floating-point tolerance.


## Disclaimer

Educational/demo code only. Not financial, safety, or engineering advice. Use at your own risk. Verify results independently before any production or operational use.

## License

MIT — see [LICENSE](LICENSE).