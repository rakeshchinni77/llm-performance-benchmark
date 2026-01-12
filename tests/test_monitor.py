from benchmark.monitor import ResourceMonitor


def test_resource_monitor_ram_only():
    monitor = ResourceMonitor(monitor_gpu=False)
    monitor.start()
    monitor.sample(duration=0.05)
    stats = monitor.stop()

    assert "peak_ram_mb" in stats
    assert stats["peak_ram_mb"] > 0
    assert stats["peak_gpu_mb"] is None
