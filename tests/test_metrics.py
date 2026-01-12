from benchmark.metrics import (
    compute_throughput,
    compute_output_length,
    compute_vocabulary_diversity,
    aggregate_metrics,
)


def test_compute_throughput():
    assert compute_throughput(100, 2.0) == 50.0
    assert compute_throughput(0, 1.0) == 0.0


def test_output_length():
    text = "hello world this is test"
    assert compute_output_length(text) == 5


def test_vocab_diversity():
    text = "hello hello world"
    assert compute_vocabulary_diversity(text) == 2 / 3


def test_aggregate_metrics():
    metrics = aggregate_metrics(
        latency=1.0,
        tokens_generated=20,
        output_text="a b c a",
    )
    assert metrics["latency_sec"] == 1.0
    assert metrics["tokens_per_sec"] == 20.0
    assert metrics["output_length"] == 4
