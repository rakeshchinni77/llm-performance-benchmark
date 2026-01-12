from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
import matplotlib.pyplot as plt

from benchmark.exceptions import ReportError


def save_results_csv(
    results: List[Dict[str, Any]],
    output_dir: Path,
) -> Path:
    """
    Save raw benchmark results to CSV.
    """
    try:
        df = pd.DataFrame(results)
        output_dir.mkdir(parents=True, exist_ok=True)

        csv_path = output_dir / "results.csv"
        df.to_csv(csv_path, index=False)

        return csv_path

    except Exception as exc:
        raise ReportError(f"Failed to save results CSV: {exc}") from exc


def plot_average_latency(
    results: List[Dict[str, Any]],
    output_dir: Path,
) -> Path:
    """
    Plot average latency per model.
    """
    try:
        df = pd.DataFrame(results)
        avg_latency = df.groupby("model_name")["latency_sec"].mean()

        plt.figure(figsize=(8, 5))
        avg_latency.plot(kind="bar")
        plt.ylabel("Average Latency (seconds)")
        plt.title("Average Inference Latency by Model")
        plt.tight_layout()

        plot_path = output_dir / "latency_comparison.png"
        plt.savefig(plot_path)
        plt.close()

        return plot_path

    except Exception as exc:
        raise ReportError(f"Failed to generate latency plot: {exc}") from exc


def plot_peak_memory(
    results: List[Dict[str, Any]],
    output_dir: Path,
) -> Path:
    """
    Plot peak RAM usage per model.
    """
    try:
        df = pd.DataFrame(results)
        avg_memory = df.groupby("model_name")["peak_ram_mb"].mean()

        plt.figure(figsize=(8, 5))
        avg_memory.plot(kind="bar")
        plt.ylabel("Peak RAM Usage (MB)")
        plt.title("Average Peak RAM Usage by Model")
        plt.tight_layout()

        plot_path = output_dir / "memory_comparison.png"
        plt.savefig(plot_path)
        plt.close()

        return plot_path

    except Exception as exc:
        raise ReportError(f"Failed to generate memory plot: {exc}") from exc


def print_summary(results: List[Dict[str, Any]]) -> None:
    """
    Print benchmark summary to console.
    """
    df = pd.DataFrame(results)

    print("\n===== Benchmark Summary =====")
    print(df.groupby("model_name")[[
        "latency_sec",
        "tokens_per_sec",
        "peak_ram_mb",
    ]].mean().round(4))
