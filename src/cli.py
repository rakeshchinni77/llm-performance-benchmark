import argparse
import sys
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError

# NOTE:
# runner will be implemented in Step 16
# We import lazily to avoid early failures


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

        print("[INFO] Configuration loaded and validated successfully.")
        print("[INFO] Starting LLM benchmarking process...")

        # Import runner lazily (implemented later)
        from benchmark.runner import run_benchmark  # noqa: E402

        run_benchmark(config)

    else:
        raise RuntimeError("Unknown command")
