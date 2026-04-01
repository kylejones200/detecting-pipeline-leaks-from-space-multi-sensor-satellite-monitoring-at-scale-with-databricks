import sys
import os

# Add parent directory to path to import plot_style
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plot_style import set_tufte_defaults, apply_tufte_style, save_tufte_figure, COLORS

"""
Visualization generation for Blog 14: Pipeline Leak Detection from Satellite Data
Creates minimalist-style visualizations for multi-sensor leak detection.
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings

import sys
import os

# Add parent directory to path to import plot_style
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plot_style import set_tufte_defaults, apply_tufte_style, save_tufte_figure, COLORS

# Import Tufte plotting utilities
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from tda_utils import setup_tufte_plot, TufteColors


warnings.filterwarnings('ignore')

def apply_minimalist_style_manual(ax):
    """Apply minimalist style components manually to axis."""
    plt.rcParams["font.family"] = "serif"
    
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_position(("outward", 5))
    ax.spines["bottom"].set_position(("outward", 5))
def generate_methane_time_series():
    """Generate synthetic TROPOMI methane time series with anomalies."""
    np.random.seed(42)
    
    # 90 days of data
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(90)]
    
    # Baseline methane (seasonal + noise)
    baseline = 1850 + 20 * np.sin(np.arange(90) * 2 * np.pi / 365) + np.random.randn(90) * 15
    
    # Add leak events
    leak_indices = [25, 26, 27, 28, 58, 59, 60]
    for idx in leak_indices:
        baseline[idx] += np.random.uniform(150, 300)
    
    return dates, baseline

def create_main_methane_detection_plot():
    """
    Create time series plot showing methane anomaly detection.
    """
    print("Generating main methane detection visualization...")
    
    dates, methane = generate_methane_time_series()
    
    # Calculate rolling baseline and threshold
    window = 14
    rolling_mean = np.convolve(methane, np.ones(window)/window, mode='same')
    rolling_std = np.array([np.std(methane[max(0, i-window):min(len(methane), i+window)]) 
                           for i in range(len(methane))])
    
    threshold = rolling_mean + 3 * rolling_std
    anomalies = methane > threshold
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot baseline
    ax.plot(dates, methane, 'o-', color='black', linewidth=1, 
           markersize=3, markerfacecolor='white', markeredgecolor='black',
           label='TROPOMI CH₄ Observations', zorder=3)
    
    # Plot rolling mean
    ax.plot(dates, rolling_mean, '--', color='black', linewidth=2,
           label='14-Day Rolling Mean', zorder=2)
    
    # Plot threshold
    ax.plot(dates, threshold, ':', color='black', linewidth=2,
           label='Anomaly Threshold (μ + 3σ)', zorder=2)
    
    # Highlight anomalies
    anomaly_dates = [d for d, a in zip(dates, anomalies) if a]
    anomaly_values = [v for v, a in zip(methane, anomalies) if a]
    
    ax.scatter(anomaly_dates, anomaly_values, s=150, 
              facecolors='none', edgecolors='#FF4136', linewidths=3,
              label=f'Detected Anomalies (n={len(anomaly_dates)})', zorder=4)
    
    # Apply minimalist style
    apply_minimalist_style_manual(ax)
    
    ax.set_xlabel('Date', fontsize=11)
    ax.set_ylabel('CH₄ Column Density (ppb)', fontsize=11)
    ax.set_title('Pipeline Leak Detection from TROPOMI Methane Data', 
                 fontsize=13, fontweight='bold', loc='left', pad=20)
    
    ax.legend(loc='upper left', frameon=False, fontsize=9)
    
    # Format x-axis
    ax.tick_params(axis='x', rotation=45)
    
    # Add annotation for leak events
    ax.annotate('Potential Leak Event', 
               xy=(dates[26], methane[26]), xytext=(dates[40], methane[26] + 200),
               arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
               fontsize=9, bbox=dict(boxstyle='round', facecolor='white', edgecolor='black'))
    
    plt.tight_layout()
    plt.savefig('/Users/k.jones/Desktop/blogs/blog_posts/14_satellite_leak_detection_main.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Main methane detection visualization saved")
    print(f"  Anomalies detected: {len(anomaly_dates)}")

def create_multi_sensor_fusion_plot():
    """
    Create plot showing multi-sensor fusion (TROPOMI + Sentinel-2 + Sentinel-1).
    """
    print("Generating multi-sensor fusion visualization...")
    
    # Generate synthetic data for a spatial grid
    np.random.seed(42)
    
    n_points = 100
    x = np.linspace(-2, 2, n_points)
    y = np.linspace(-2, 2, n_points)
    X, Y = np.meshgrid(x, y)
    
    # Simulate leak at (0.5, 0.3)
    leak_x, leak_y = 0.5, 0.3
    
    # TROPOMI methane plume (coarse resolution)
    dist_tropomi = np.sqrt((X - leak_x)**2 + (Y - leak_y)**2)
    tropomi = np.exp(-dist_tropomi**2 / 0.8) * 300 + np.random.randn(n_points, n_points) * 20
    tropomi = np.clip(tropomi, 0, 300)
    
    # Sentinel-2 NDVI anomaly (medium resolution)
    dist_s2 = np.sqrt((X - leak_x)**2 + (Y - leak_y)**2)
    sentinel2 = -np.exp(-dist_s2**2 / 0.4) * 0.3 + np.random.randn(n_points, n_points) * 0.05
    sentinel2 = np.clip(sentinel2, -0.3, 0.1)
    
    # Sentinel-1 SAR coherence loss (fine resolution)
    dist_s1 = np.sqrt((X - leak_x)**2 + (Y - leak_y)**2)
    sentinel1 = -np.exp(-dist_s1**2 / 0.3) * 0.4 + np.random.randn(n_points, n_points) * 0.06
    sentinel1 = np.clip(sentinel1, -0.4, 0.1)
    
    # Create figure with 4 subplots
    fig = plt.figure(figsize=(14, 10))
    
    # TROPOMI
    ax1 = plt.subplot(2, 2, 1)
    im1 = ax1.contourf(X, Y, tropomi, levels=15, cmap='YlOrRd')
    ax1.plot(leak_x, leak_y, 'k*', markersize=20, label='Pipeline Location')
    apply_minimalist_style_manual(ax1)
    ax1.set_xlabel('Easting (km)', fontsize=9)
    ax1.set_ylabel('Northing (km)', fontsize=9)
    ax1.set_title('TROPOMI Methane\n(5.5 km resolution)', 
                  fontsize=11, fontweight='bold', loc='center', pad=10)
    ax1.legend(loc='upper right', frameon=False, fontsize=8)
    cbar1 = plt.colorbar(im1, ax=ax1)
    cbar1.set_label('ΔCH₄ (ppb)', fontsize=9)
    cbar1.outline.set_visible(False)
    
    # Sentinel-2
    ax2 = plt.subplot(2, 2, 2)
    im2 = ax2.contourf(X, Y, sentinel2, levels=15, cmap='RdYlGn')
    ax2.plot(leak_x, leak_y, 'k*', markersize=20, label='Pipeline Location')
    apply_minimalist_style_manual(ax2)
    ax2.set_xlabel('Easting (km)', fontsize=9)
    ax2.set_ylabel('Northing (km)', fontsize=9)
    ax2.set_title('Sentinel-2 NDVI Change\n(10 m resolution)', 
                  fontsize=11, fontweight='bold', loc='center', pad=10)
    ax2.legend(loc='upper right', frameon=False, fontsize=8)
    cbar2 = plt.colorbar(im2, ax=ax2)
    cbar2.set_label('ΔNDVI', fontsize=9)
    cbar2.outline.set_visible(False)
    
    # Sentinel-1
    ax3 = plt.subplot(2, 2, 3)
    im3 = ax3.contourf(X, Y, sentinel1, levels=15, cmap='RdYlGn')
    ax3.plot(leak_x, leak_y, 'k*', markersize=20, label='Pipeline Location')
    apply_minimalist_style_manual(ax3)
    ax3.set_xlabel('Easting (km)', fontsize=9)
    ax3.set_ylabel('Northing (km)', fontsize=9)
    ax3.set_title('Sentinel-1 Coherence Change\n(10 m resolution)', 
                  fontsize=11, fontweight='bold', loc='center', pad=10)
    ax3.legend(loc='upper right', frameon=False, fontsize=8)
    cbar3 = plt.colorbar(im3, ax=ax3)
    cbar3.set_label('Δ Coherence', fontsize=9)
    cbar3.outline.set_visible(False)
    
    # Fused detection score
    ax4 = plt.subplot(2, 2, 4)
    # Normalize and combine
    tropomi_norm = (tropomi - tropomi.min()) / (tropomi.max() - tropomi.min())
    sentinel2_norm = np.abs(sentinel2) / np.abs(sentinel2).max()
    sentinel1_norm = np.abs(sentinel1) / np.abs(sentinel1).max()
    
    fused_score = (tropomi_norm * 0.5 + sentinel2_norm * 0.25 + sentinel1_norm * 0.25) * 100
    
    im4 = ax4.contourf(X, Y, fused_score, levels=15, cmap='hot_r')
    ax4.plot(leak_x, leak_y, 'k*', markersize=20, label='Pipeline Location')
    
    # Add contour for high confidence detection
    ax4.contour(X, Y, fused_score, levels=[60], colors='cyan', linewidths=3, linestyles='--')
    
    apply_minimalist_style_manual(ax4)
    ax4.set_xlabel('Easting (km)', fontsize=9)
    ax4.set_ylabel('Northing (km)', fontsize=9)
    ax4.set_title('Fused Detection Score\n(Multi-Sensor Integration)', 
                  fontsize=11, fontweight='bold', loc='center', pad=10)
    ax4.legend(loc='upper right', frameon=False, fontsize=8)
    cbar4 = plt.colorbar(im4, ax=ax4)
    cbar4.set_label('Leak Confidence (%)', fontsize=9)
    cbar4.outline.set_visible(False)
    
    plt.suptitle('Multi-Sensor Fusion for Pipeline Leak Detection', 
                fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig('/Users/k.jones/Desktop/blogs/blog_posts/14_satellite_multi_sensor_fusion.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ Multi-sensor fusion visualization saved")

def main():
    """Generate all visualizations for Blog 14."""
    set_tufte_defaults()
    print("="*70)
    print("Blog 14: Satellite Leak Detection - Visualizations")
    print("="*70)
    print()
    
    create_main_methane_detection_plot()
    create_multi_sensor_fusion_plot()
    
    print()
    print("="*70)
    print("All visualizations generated successfully!")
    print("="*70)
    print()
    print("Files created:")
    print("  - 14_satellite_leak_detection_main.png")
    print("  - 14_satellite_multi_sensor_fusion.png")

if __name__ == "__main__":
    main()

