import time
from typing import Dict, Set


def measure_latency(func, *args, **kwargs) -> tuple[float, any]:
    """
    Measure end-to-end latency of a callable.

    Returns:
        latency_seconds (float)
        result (any)
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()

    latency = end_time - start_time
    return latency, result


def compute_throughput(tokens_generated: int, latency_seconds: float) -> float:
    """
    Compute throughput in tokens per second.
    """
    if latency_seconds <= 0:
        return 0.0
    return tokens_generated / latency_seconds


def compute_output_length(output_text: str) -> int:
    """
    Compute output length in number of tokens (whitespace-based).
    """
    if not output_text:
        return 0
    return len(output_text.split())


def compute_vocabulary_diversity(output_text: str) -> float:
    """
    Compute vocabulary diversity:
        unique_tokens / total_tokens
    """
    if not output_text:
        return 0.0

    tokens = output_text.split()
    if not tokens:
        return 0.0

    unique_tokens: Set[str] = set(tokens)
    return len(unique_tokens) / len(tokens)


def aggregate_metrics(
    latency: float,
    tokens_generated: int,
    output_text: str,
) -> Dict[str, float]:
    """
    Aggregate all metrics into a single dictionary.
    """
    throughput = compute_throughput(tokens_generated, latency)
    output_length = compute_output_length(output_text)
    vocab_diversity = compute_vocabulary_diversity(output_text)

    return {
        "latency_sec": round(latency, 4),
        "tokens_per_sec": round(throughput, 4),
        "output_length": output_length,
        "vocab_diversity": round(vocab_diversity, 4),
    }
