#!/usr/bin/env python3
import argparse, sys, time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/"src"))
from compute_kernel import rolling_anomaly_flags
def main():
    p=argparse.ArgumentParser(); p.add_argument("--n",type=int,default=5000); p.add_argument("--iterations",type=int,default=2000); a=p.parse_args()
    m=np.ascontiguousarray(np.sin(np.arange(a.n)*0.01)+2.0+np.random.default_rng(0).normal(0,0.05,a.n), dtype=float)
    t0=time.perf_counter()
    for _ in range(a.iterations): rolling_anomaly_flags(m)
    py_s=time.perf_counter()-t0
    try:
        import detecting_pipeline_leaks_from_space_multi_sensor_satellite_monitoring_at_scale_with_databricks_rs as rs
    except ImportError:
        print("Build rust extension"); print(f"Python {py_s:.3f}s"); return
    rs_s=rs.bench_kernel_py(m,14,3.0,a.iterations)
    print(f"Python {py_s:.3f}s Rust {rs_s:.3f}s speedup {py_s/rs_s:.1f}x")
    np.testing.assert_allclose(rolling_anomaly_flags(m[:200]), rs.rolling_anomaly_flags_py(m[:200],14,3.0), rtol=1e-10)
    print("Correctness: OK")
if __name__=="__main__": main()
