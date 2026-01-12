import sys
from cli import parse_args


def test_cli_parse_run(monkeypatch):
    test_args = [
        "llm-bench",
        "run",
        "--config",
        "config/benchmark.yaml",
    ]
    monkeypatch.setattr(sys, "argv", test_args)

    args = parse_args()
    assert args.command == "run"
    assert args.config == "config/benchmark.yaml"
