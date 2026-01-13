from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import json
import logging

import pandas as pd
from tqdm import tqdm

from benchmark.dataset import load_dataset
from benchmark.models import HuggingFaceModel
from benchmark.monitor import ResourceMonitor
from benchmark.metrics import measure_latency, aggregate_metrics
from benchmark.environment import get_environment_metadata
from benchmark.reporter import (
    save_results_csv,
    plot_average_latency,
    plot_peak_memory,
    print_summary,
)
from benchmark.exceptions import ModelLoadError, InferenceError


def run_benchmark(config: dict) -> None:
    logging.info("Initializing benchmark run")

    # Output directories (timestamped + latest)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    base_dir = Path(config["output"]["base_dir"])

    output_dir = base_dir / timestamp
    latest_dir = base_dir / "latest"

    output_dir.mkdir(parents=True, exist_ok=True)
    latest_dir.mkdir(parents=True, exist_ok=True)

    # Load dataset
    dataset_cfg = config["dataset"]
    prompts = load_dataset(
        path=dataset_cfg["path"],
        fmt=dataset_cfg["format"],
        text_field=dataset_cfg["text_field"],
        max_prompts=dataset_cfg.get("max_prompts"),
    )

    logging.info(f"Loaded {len(prompts)} prompts")

    # Environment metadata
    env = get_environment_metadata()
    logging.info(
        f"Environment: Python {env['python_version']} | CPU cores: {env['cpu_cores']}"
    )

    env_path = output_dir / "environment.json"
    with open(env_path, "w", encoding="utf-8") as f:
        json.dump(env, f, indent=2)

    logging.info(f"Environment metadata saved to {env_path}")

    results: List[Dict[str, Any]] = []

    # Model loop
    for model_cfg in config["models"]:
        model_id = model_cfg["id"]
        model_name = model_cfg["name"]

        logging.info(f"Loading model: {model_name}")

        try:
            model = HuggingFaceModel(
                model_id=model_id,
                device=config["runtime"]["device"],
                dtype=model_cfg["dtype"],
            )
        except ModelLoadError as exc:
            logging.error(f"Model load failed: {exc}")
            continue

        for prompt in tqdm(prompts, desc=f"Running {model_name}"):
            monitor = ResourceMonitor(
                monitor_gpu=(config["runtime"]["device"] == "cuda")
            )

            try:
                monitor.start()

                latency, (output_text, output_tokens) = measure_latency(
                    model.generate,
                    prompt["prompt"],
                    config["generation"],
                )

                monitor.sample()
                mem = monitor.stop()

                metrics = aggregate_metrics(
                    latency=latency,
                    tokens_generated=output_tokens,
                    output_text=output_text,
                )

                results.append({
                    "model_id": model_id,
                    "model_name": model_name,
                    "prompt_id": prompt["id"],
                    **metrics,
                    "peak_ram_mb": mem["peak_ram_mb"],
                    "peak_gpu_mb": mem["peak_gpu_mb"],
                })

            except InferenceError as exc:
                logging.warning(f"Inference failed: {exc}")

            finally:
                monitor.cleanup()

    # Safety check
    if not results:
        raise RuntimeError(
            "Benchmark completed but NO RESULTS were collected. "
            "Check model loading or inference."
        )

    # Reporting (CSV + plots)
    csv_path = save_results_csv(results, output_dir)
    plot_average_latency(results, output_dir)
    plot_peak_memory(results, output_dir)

    print_summary(results)

    logging.info(f"Results CSV saved at {csv_path}")

    # Summary markdown
    summary_path = output_dir / "summary.md"

    df = pd.DataFrame(results)
    summary_df = df.groupby("model_name")[[
        "latency_sec",
        "tokens_per_sec",
        "peak_ram_mb"
    ]].mean().round(3)

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Benchmark Summary\n\n")
        f.write(f"- Models tested: {df['model_name'].nunique()}\n")
        f.write(f"- Total runs: {len(df)}\n\n")
        f.write("## Average Metrics per Model\n\n")
        f.write(summary_df.to_markdown())

    logging.info(f"Summary report saved to {summary_path}")

    # Update latest/ directory
    for item in latest_dir.iterdir():
        if item.is_file():
            item.unlink()

    for file in output_dir.iterdir():
        if file.is_file():
            target = latest_dir / file.name
            target.write_bytes(file.read_bytes())

    logging.info("Updated outputs/latest with most recent run")

    logging.info("Benchmark completed successfully")
