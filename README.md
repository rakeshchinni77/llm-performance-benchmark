# LLM Performance Benchmarking Tool

A production-quality, configuration-driven **command-line benchmarking tool** to evaluate and compare the performance of Large Language Models (LLMs).

This project is built to help engineers and ML practitioners make **informed model selection decisions** by analyzing trade-offs between **latency, throughput, memory usage, and output quality** before deploying models to production.

---

## Project Objective

Selecting the right LLM for production is not only about output quality. Real-world systems must balance:

- Inference speed  
- Hardware resource usage  
- Scalability constraints  
- Cost and deployment feasibility  

This tool provides a **systematic and reproducible way** to benchmark multiple LLMs and generate **clear, actionable performance reports**.

---

## Key Features

- Command-line interface (CLI)
- Supports multiple Hugging Face LLMs
- Configuration-driven (YAML)
- Measures:
  - Inference latency
  - Tokens per second (throughput)
  - Peak RAM usage
  - Peak GPU memory usage (if available)
- Basic automated quality metrics:
  - Output length
  - Vocabulary diversity
- CSV result export
- Performance visualizations (PNG)
- Robust error handling (model failures don’t crash runs)
- Fully tested with PyTest
- CI pipeline using GitHub Actions

---

## What This Tool Benchmarks

For each model and prompt, the tool records:

| Category | Metrics |
|--------|--------|
| Performance | Latency (seconds), Tokens/sec |
| Memory | Peak RAM, Peak GPU memory |
| Quality (basic) | Output length, Vocabulary diversity |

---

## Project Structure

```
llm-performance-benchmark/
├── README.md
├── requirements.txt
├── setup.py
├── pyproject.toml
│
├── .github/
│ └── workflows/
│ └── ci.yml
│
├── config/
│ ├── benchmark.yaml
│ ├── prompts.jsonl
│ └── schema.yaml
│
├── src/
│ ├── cli.py
│ └── benchmark/
│ ├── runner.py
│ ├── models.py
│ ├── metrics.py
│ ├── monitor.py
│ ├── reporter.py
│ ├── environment.py
│ └── exceptions.py
│
├── tests/
│ ├── test_cli.py
│ ├── test_metrics.py
│ ├── test_monitor.py
│ └── test_runner.py
│
├── outputs/
│ └── latest/
│ ├── results.csv
│ ├── latency_comparison.png
│ └── memory_comparison.png
│
└── docs/
└── benchmark_report.md
```

---

## Setup Instructions

### 1️.Clone the repository

```bash
git clone https://github.com/rakeshchinni77/llm-performance-benchmark.git
cd llm-performance-benchmark

```
### 2️.Create and activate virtual environment
```bash
python -m venv .venv

```
Windows
```bash
.venv\Scripts\Activate.ps1
```
Linux / macOS
```bash
source .venv/bin/activate
```
### 3️.Install dependencies
```bash
pip install -r requirements.txt
pip install -e .
```
---

## How to Run the Benchmark

The tool is executed via the CLI and controlled using a YAML configuration file.

```bash

python -m src.cli run --config config/benchmark.yaml

```
---

## Configuration Overview (benchmark.yaml)

The configuration file defines:

Models to benchmark

Dataset location

Generation parameters

Runtime device (CPU / GPU)

Output settings

Example (simplified):

```
models:
  - id: "distilgpt2"
    name: "DistilGPT-2 (Small)"
    provider: "huggingface"
    size: "<1B"
    dtype: "float32"

dataset:
  path: "config/prompts.jsonl"
  format: "jsonl"
  text_field: "prompt"

runtime:
  device: "cpu"

```
The configuration is validated using a JSON schema before execution.

---

## Output Artifacts

After execution, results are saved in:

```bash

outputs/latest/

```

---

## Visualizations

Latency Comparison
Helps identify fast vs slow models

Memory Usage Comparison
Highlights hardware feasibility

These charts allow quick comparison for production decision-making.

---

## Testing

All core components are unit tested.

Run tests locally:

```bash
pytest -v
```

---
## Continuous Integration (CI)

This repository includes a GitHub Actions workflow that:

Sets up Python 3.11

Installs dependencies

Runs all tests using PyTest

CI runs automatically on every push and pull request to main.

---

## Design Principles

1.Modularity – clear separation of concerns

2.Configuration-driven – no hardcoded models or paths

3.Fail-safe execution – partial failures don’t stop the run

4.Production mindset – realistic metrics and reporting

5.Reproducibility – environment metadata captured

---

### Benchmark Analysis

A detailed interpretation of the benchmark results is provided in:

📘 docs/benchmark_report.md

---

### Future Enhancements

Perplexity-based quality metrics

Batch inference benchmarking

Multi-GPU benchmarking

Cloud-hosted model evaluation

API endpoint benchmarking

---

### License

This project is released under the MIT License.


