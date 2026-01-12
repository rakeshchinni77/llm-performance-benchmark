import time
import psutil

from benchmark.exceptions import ResourceMonitorError

try:
    import pynvml
    _NVML_AVAILABLE = True
except ImportError:
    _NVML_AVAILABLE = False


class ResourceMonitor:
    """
    Monitor peak RAM and GPU memory usage during inference.
    """

    def __init__(self, monitor_gpu: bool = True):
        self.monitor_gpu = monitor_gpu and _NVML_AVAILABLE

        self._process = psutil.Process()
        self._peak_ram_mb = 0.0

        self._gpu_handle = None
        self._peak_gpu_mb = 0.0

        if self.monitor_gpu:
            try:
                pynvml.nvmlInit()
                self._gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            except Exception:
                # GPU monitoring will be disabled gracefully
                self.monitor_gpu = False

    def start(self):
        """
        Reset peak measurements.
        """
        self._peak_ram_mb = self._get_ram_mb()
        self._peak_gpu_mb = self._get_gpu_mb() if self.monitor_gpu else 0.0

    def stop(self) -> dict:
        """
        Return peak memory usage.
        """
        try:
            # Final check
            self._update_peaks()

            return {
                "peak_ram_mb": round(self._peak_ram_mb, 2),
                "peak_gpu_mb": round(self._peak_gpu_mb, 2)
                if self.monitor_gpu
                else None,
            }

        except Exception as exc:
            raise ResourceMonitorError(
                f"Failed to collect resource metrics: {exc}"
            ) from exc

    def _get_ram_mb(self) -> float:
        mem_bytes = self._process.memory_info().rss
        return mem_bytes / (1024 ** 2)

    def _get_gpu_mb(self) -> float:
        if not self.monitor_gpu:
            return 0.0

        info = pynvml.nvmlDeviceGetMemoryInfo(self._gpu_handle)
        return info.used / (1024 ** 2)

    def _update_peaks(self):
        """
        Update peak RAM/GPU values.
        """
        ram_mb = self._get_ram_mb()
        self._peak_ram_mb = max(self._peak_ram_mb, ram_mb)

        if self.monitor_gpu:
            gpu_mb = self._get_gpu_mb()
            self._peak_gpu_mb = max(self._peak_gpu_mb, gpu_mb)

    def sample(self, interval: float = 0.01, duration: float = 0.5):
        """
        Sample resource usage periodically.
        Intended to be run during inference.
        """
        end_time = time.time() + duration
        while time.time() < end_time:
            self._update_peaks()
            time.sleep(interval)

    def cleanup(self):
        """
        Clean up GPU monitoring resources.
        """
        if self.monitor_gpu:
            try:
                pynvml.nvmlShutdown()
            except Exception:
                pass
