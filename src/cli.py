import argparse
import sys
from pathlib import Path

import yaml
from jsonschema import validate, ValidationError

from benchmark.logging_utils import setup_logging


def load_yaml(path: Path) -> dict:
    """Load a YAML file and return its contents."""
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_config(config: dict, schema_path: Path) -> None:
    """Validate benchmark config against schema."""
    schema = load_yaml(schema_path)
    try:
        validate(instance=config, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Config validation failed: {e.message}") from e


def parse_args():
    parser = argparse.ArgumentParser(
        prog="llm-bench",
        description="Benchmark and compare LLM performance (latency, memory, quality)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # run command
    run_parser = subparsers.add_parser(
        "run", help="Run LLM performance benchmark"
    )
    run_parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to benchmark configuration YAML file",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.command == "run":
        config_path = Path(args.config)
        schema_path = Path("config/schema.yaml")

        try:
            config = load_yaml(config_path)
            validate_config(config, schema_path)
        except Exception as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            sys.exit(1)

        # Initialize logging BEFORE benchmark starts
        log_dir = Path(config["output"]["base_dir"]) / "logs"
        setup_logging(
            log_dir=log_dir,
            level=config["output"].get("log_level", "INFO"),
        )

        print("[INFO] Configuration loaded and validated successfully.")
        print("[INFO] Starting LLM benchmarking process...")

        # Lazy import to avoid startup failures
        from benchmark.runner import run_benchmark  # noqa: E402

        run_benchmark(config)

    else:
        raise RuntimeError("Unknown command")


if __name__ == "__main__":
    main()
