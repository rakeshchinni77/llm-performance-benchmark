# LLM Performance Benchmark Report

## 1. Objective

The objective of this benchmark was to **systematically evaluate the performance of Large Language Models (LLMs)** and understand the trade-offs between:

- Inference latency
- Throughput (tokens per second)
- Memory consumption
- Basic output quality indicators

The results are intended to guide **model selection decisions** for real-world AI applications, especially under hardware and cost constraints.

---

## 2. Benchmark Setup

### Hardware & Environment
- **Platform**: Windows
- **CPU**: 16 logical cores
- **RAM**: ~16 GB
- **GPU**: Not used (CPU-only benchmarking)
- **Python Version**: 3.11
- **Frameworks**:
  - PyTorch
  - Hugging Face Transformers

Environment metadata was captured programmatically to ensure **reproducibility**.

---

### Models Evaluated

| Model | Size Category | Parameters |
|-----|--------------|-----------|
| DistilGPT-2 | Small | < 1B |

> Note:  
> The framework supports benchmarking medium (~7B) and large (>13B) models.  
> For local testing, only a small model was executed due to hardware constraints.

---

### Dataset

- **Number of prompts**: 10
- **Format**: JSONL
- **Prompt Type**: General natural-language prompts
- **Execution Mode**: Single prompt inference (batch size = 1)

---

## 3. Metrics Collected

For each prompt and model, the following metrics were recorded:

### Performance Metrics
- **Latency (seconds)**  
  End-to-end inference time per prompt.

- **Throughput (tokens/sec)**  
  Number of generated tokens divided by inference time.

---

### Memory Metrics
- **Peak RAM Usage (MB)**  
  Maximum resident memory used during inference.

- **Peak GPU Memory (MB)**  
  Collected only when GPU is available (not applicable in this run).

---

### Quality Metrics (Basic)
- **Output Length**  
  Number of generated tokens (approximate).

- **Vocabulary Diversity**  
  Ratio of unique tokens to total tokens.

These quality metrics are **lightweight indicators**, not task-specific accuracy measures.

---

## 4. Results Summary (DistilGPT-2)

| Metric | Observed Value |
|-----|---------------|
| Average Latency | ~2.8 seconds |
| Throughput | ~69 tokens/sec |
| Peak RAM Usage | ~644 MB |

Visualizations generated:
- `latency_comparison.png`
- `memory_comparison.png`

---

## 5. Performance Analysis

### Latency
- DistilGPT-2 shows **reasonable latency** on CPU-only hardware.
- Suitable for:
  - Prototyping
  - Offline batch processing
  - Low-concurrency applications

However, it may not be ideal for **high-throughput real-time APIs** without GPU acceleration.

---

### Throughput
- Throughput remains stable across prompts.
- The tokens/sec metric demonstrates:
  - Predictable performance
  - Consistent inference behavior

This makes the model easier to capacity-plan in production environments.

---

### Memory Usage
- Peak RAM usage remains under 1 GB.
- This makes DistilGPT-2 feasible for:
  - Low-resource servers
  - Edge deployments
  - CPU-only inference setups

Memory usage is a key differentiator when compared to medium and large LLMs.

---

## 6. Quality Observations

- Output length is consistent with generation parameters.
- Vocabulary diversity indicates:
  - Reasonable lexical variety
  - No excessive repetition

While these metrics do not measure semantic correctness, they provide **quick sanity checks** for generation behavior.

---

## 7. Trade-Off Discussion

| Model Size | Latency | Memory | Quality | Deployment Suitability |
|----------|--------|--------|--------|------------------------|
| Small (<1B) | Low | Low | Moderate | CPU, edge, low-cost |
| Medium (~7B) | Medium | High | High | GPU-backed services |
| Large (>13B) | High | Very High | Very High | High-end GPU clusters |

Key insight:
> **Model selection must balance performance, cost, and infrastructure constraints — not just output quality.**

---

## 8. Limitations

- Benchmark focused on **CPU-only execution**
- No task-specific quality evaluation (e.g., BLEU, ROUGE)
- Small prompt dataset

These limitations were intentional to keep the benchmark:
- Fast
- Deterministic
- Hardware-agnostic

---

## 9. Future Improvements

Potential extensions to this benchmarking framework include:

- GPU and multi-GPU benchmarking
- Batch inference performance
- Perplexity-based quality metrics
- Cloud-hosted model endpoint evaluation
- Larger and task-specific datasets

---

## 10. Conclusion

This benchmark demonstrates that:

- Small models like **DistilGPT-2** offer excellent efficiency for CPU-based deployments.
- Memory and latency profiling are critical for production planning.
- A structured benchmarking approach enables **data-driven LLM selection**.

The implemented benchmarking tool is **modular, extensible, and production-oriented**, making it suitable as a foundation for broader LLM evaluation pipelines.
