import pytest
from benchmark.runner import run_benchmark


def test_runner_fails_on_empty_results(tmp_path):
    fake_config = {
        "dataset": {
            "path": "config/prompts.jsonl",
            "format": "jsonl",
            "text_field": "prompt",
            "max_prompts": 0,
        },
        "models": [],
        "runtime": {"device": "cpu"},
        "generation": {},
        "output": {"base_dir": str(tmp_path)},
    }

    with pytest.raises(RuntimeError):
        run_benchmark(fake_config)
