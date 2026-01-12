from typing import List, Dict, Any
from tqdm import tqdm

from benchmark.dataset import load_dataset
from benchmark.models import HuggingFaceModel
from benchmark.monitor import ResourceMonitor
from benchmark.metrics import measure_latency, aggregate_metrics
from benchmark.environment import get_environment_metadata
from benchmark.exceptions import (
    BenchmarkError,
    InferenceError,
    ModelLoadError,
)


def run_benchmark(config: dict) -> None:
    """
    Main benchmark orchestration function.
    """
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

    # Collect environment metadata
    environment = get_environment_metadata()

    # Prepare result container
    all_results: List[Dict[str, Any]] = []

    # Loop over models
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
        except ModelLoadError as exc:
            print(f"[ERROR] {exc}")
            continue

        # Loop over prompts
        for record in tqdm(prompts, desc=f"Running {model_name}"):
            prompt_id = record["id"]
            prompt_text = record["prompt"]

            monitor = ResourceMonitor(
                monitor_gpu=(config["runtime"]["device"] == "cuda")
            )

            try:
                monitor.start()

                latency, (output_text, output_tokens) = measure_latency(
                    model.generate,
                    prompt_text,
                    config["generation"],
                )

                monitor.sample()
                resource_metrics = monitor.stop()

                metrics = aggregate_metrics(
                    latency=latency,
                    tokens_generated=output_tokens,
                    output_text=output_text,
                )

                result = {
                    "model_id": model_id,
                    "model_name": model_name,
                    "prompt_id": prompt_id,
                    "latency_sec": metrics["latency_sec"],
                    "tokens_per_sec": metrics["tokens_per_sec"],
                    "output_length": metrics["output_length"],
                    "vocab_diversity": metrics["vocab_diversity"],
                    "peak_ram_mb": resource_metrics["peak_ram_mb"],
                    "peak_gpu_mb": resource_metrics["peak_gpu_mb"],
                }

                all_results.append(result)

            except InferenceError as exc:
                print(f"[WARN] Inference failed for model {model_name}: {exc}")

            finally:
                monitor.cleanup()

    # Final reporting (placeholder)
    print("\n[INFO] Benchmark run completed")
    print(f"[INFO] Total successful runs: {len(all_results)}")

    # NOTE:
    # Saving results + plots handled in reporter.py (Step 17)
