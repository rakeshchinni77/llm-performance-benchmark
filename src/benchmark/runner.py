from pathlib import Path
from typing import List, Dict, Any

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
    print("[INFO] Initializing benchmark run")

    # Load dataset
    dataset_cfg = config["dataset"]
    prompts = load_dataset(
        path=dataset_cfg["path"],
        fmt=dataset_cfg["format"],
        text_field=dataset_cfg["text_field"],
        max_prompts=dataset_cfg.get("max_prompts"),
    )

    print(f"[INFO] Loaded {len(prompts)} prompts")

    # Environment metadata
    env = get_environment_metadata()
    print(f"[INFO] Environment: {env['python_version']} | CPU cores: {env['cpu_cores']}")

    results: List[Dict[str, Any]] = []

    # Model loop
    for model_cfg in config["models"]:
        model_id = model_cfg["id"]
        model_name = model_cfg["name"]

        print(f"\n[INFO] Loading model: {model_name}")

        try:
            model = HuggingFaceModel(
                model_id=model_id,
                device=config["runtime"]["device"],
                dtype=model_cfg["dtype"],
            )
        except ModelLoadError as e:
            print(f"[ERROR] Model load failed: {e}")
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

            except InferenceError as e:
                print(f"[WARN] Inference failed: {e}")

            finally:
                monitor.cleanup()

    # HARD ASSERT (IMPORTANT)
    if not results:
        raise RuntimeError(
            "Benchmark completed but NO RESULTS were collected. "
            "Check model loading or inference."
        )

    # Reporting
    output_dir = Path(config["output"]["base_dir"]) / "latest"
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = save_results_csv(results, output_dir)
    latency_plot = plot_average_latency(results, output_dir)
    memory_plot = plot_peak_memory(results, output_dir)

    print_summary(results)

    print("\n[INFO] Benchmark completed successfully")
    print(f"[INFO] CSV saved at: {csv_path}")
    print(f"[INFO] Plots saved at: {output_dir}")
