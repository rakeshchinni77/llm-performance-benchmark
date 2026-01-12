class BenchmarkError(Exception):
    """
    Base exception for all benchmark-related errors.
    """
    pass


class ConfigError(BenchmarkError):
    """
    Raised when the benchmark configuration is invalid.
    """
    pass


class DatasetError(BenchmarkError):
    """
    Raised when there is an issue loading or parsing the dataset.
    """
    pass


class ModelLoadError(BenchmarkError):
    """
    Raised when a model or tokenizer fails to load.
    """
    pass


class InferenceError(BenchmarkError):
    """
    Raised when model inference fails or times out.
    """
    pass


class ResourceMonitorError(BenchmarkError):
    """
    Raised when system or GPU resource monitoring fails.
    """
    pass


class ReportError(BenchmarkError):
    """
    Raised when saving results or generating plots fails.
    """
    pass
