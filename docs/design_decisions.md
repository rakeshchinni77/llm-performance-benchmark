# Design Decisions – LLM Performance Benchmarking Tool

This document explains **why** specific architectural, technical, and implementation decisions were made while building the LLM Performance Benchmarking Tool.

The goal is to demonstrate **engineering judgment**, **trade-off awareness**, and a **production-oriented mindset**, rather than simply delivering working code.

---

## 1. Why a CLI-Based Tool?

### Decision
The benchmarking tool is implemented as a **command-line interface (CLI)** instead of a notebook or GUI.

### Reasoning
- CLI tools are **automation-friendly**
- Easy to integrate into:
  - CI pipelines
  - Batch benchmarking jobs
  - MLOps workflows
- Encourages **configuration-driven execution**
- Matches real-world production and evaluation setups

This design makes the tool suitable for both **local experimentation** and **enterprise workflows**.

---

## 2. Why Configuration-Driven (YAML)?

### Decision
All benchmark parameters are defined in a YAML configuration file.

### Reasoning
- Avoids hardcoding model names, paths, or runtime options
- Enables:
  - Easy model swapping
  - Reproducible experiments
  - Clear separation of code and experiment logic
- YAML is human-readable and widely used in MLOps (Kubernetes, CI, ML pipelines)

Configuration validation using a **JSON schema** ensures early failure for invalid setups.

---

## 3. Why Modular Architecture?

### Decision
The codebase is split into focused modules:
- `dataset.py`
- `models.py`
- `metrics.py`
- `monitor.py`
- `runner.py`
- `reporter.py`

### Reasoning
- Improves readability and maintainability
- Each module has **one responsibility**
- Makes the system:
  - Testable
  - Extensible
  - Easier to debug

This mirrors how production ML systems are structured.

---

## 4. Why Hugging Face Transformers?

### Decision
The tool uses Hugging Face `transformers` for model loading and inference.

### Reasoning
- Industry-standard library for LLMs
- Large ecosystem of open-source pretrained models
- Supports multiple architectures with a unified API
- Allows easy extension to future models

This choice ensures **broad model compatibility** without vendor lock-in.

---

## 5. Why End-to-End Latency Measurement?

### Decision
Latency is measured around the **entire inference call**, not just token generation.

### Reasoning
- End-to-end latency reflects **real user experience**
- Includes:
  - Tokenization
  - Model forward pass
  - Decoding
- More realistic for production systems than micro-benchmarks

This makes the benchmark results **actionable**, not misleading.

---

## 6. Why Tokens per Second for Throughput?

### Decision
Throughput is calculated as **tokens generated per second**.

### Reasoning
- Normalizes performance across models of different sizes
- More meaningful than raw execution time alone
- Commonly used metric in LLM serving systems

This allows fair comparison between models.

---

## 7. Why Basic Quality Metrics Instead of BLEU / ROUGE?

### Decision
The tool uses **simple automated quality metrics**:
- Output length
- Vocabulary diversity

### Reasoning
- Benchmarking focus is **performance**, not NLP task accuracy
- BLEU / ROUGE require reference datasets
- Simple metrics:
  - Are deterministic
  - Cheap to compute
  - Work for arbitrary prompts

This aligns with the project’s objective: **model selection**, not task evaluation.

---

## 8. Why psutil and pynvml for Memory Monitoring?

### Decision
- `psutil` for RAM monitoring
- `pynvml` for GPU memory monitoring

### Reasoning
- Lightweight, low overhead
- Widely used and reliable
- Allows peak memory tracking during inference
- GPU monitoring is **optional and fail-safe**

The tool runs correctly on **CPU-only systems** without crashing.

---

## 9. Why Fail-Safe Execution?

### Decision
Model load failures or inference errors do **not crash the entire benchmark**.

### Reasoning
- Real-world systems often encounter:
  - Out-of-memory errors
  - Model download issues
  - Hardware limitations
- The tool logs failures and continues with other models/prompts

This behavior reflects **production robustness** rather than academic assumptions.

---

## 10. Why CSV + PNG Outputs?

### Decision
Results are exported as:
- CSV for raw metrics
- PNG plots for visualization

### Reasoning
- CSV:
  - Easy to inspect
  - Compatible with Excel, Pandas, BI tools
- PNG:
  - Portable
  - Easy to include in reports and documentation

This dual output format supports both **technical** and **non-technical stakeholders**.

---

## 11. Why Unit Tests Instead of Integration Tests?

### Decision
The test suite focuses on **unit tests**, not full model inference.

### Reasoning
- Full inference tests are:
  - Slow
  - Hardware-dependent
  - Flaky in CI
- Unit tests ensure:
  - Metric correctness
  - CLI behavior
  - Runner edge-case handling

This keeps CI **fast, reliable, and deterministic**.

---

## 12. Why GitHub Actions for CI?

### Decision
GitHub Actions is used for continuous integration.

### Reasoning
- Native GitHub support
- Easy setup
- Free for public repositories
- Matches industry-standard workflows

CI ensures that:
- Code quality is maintained
- Tests pass on every change
- The project is reproducible by evaluators

---

## 13. Why Environment Metadata Capture?

### Decision
The tool records hardware and software environment details.

### Reasoning
- Benchmark results depend heavily on:
  - CPU/GPU
  - RAM
  - Library versions
- Capturing metadata enables:
  - Reproducibility
  - Fair comparison across systems
  - Transparent reporting

This is a key MLOps best practice.

---

## 14. Overall Design Philosophy

The system is designed to be:

- **Practical** – solves a real decision-making problem
- **Extensible** – easy to add new models or metrics
- **Robust** – handles failures gracefully
- **Readable** – clear structure and naming
- **Production-oriented** – not a demo or notebook

---

## 15. Conclusion

Every design choice in this project prioritizes:
- Real-world usability
- Engineering best practices
- Reproducibility
- Evaluator clarity

This tool is not just a benchmark script — it is a **foundation for real LLM evaluation pipelines**.
