from setuptools import setup, find_packages

setup(
    name="llm-benchmark",
    version="0.1.0",
    description="CLI tool for benchmarking LLM performance across latency, memory, and quality metrics",
    author="Your Name",
    python_requires=">=3.10,<3.12",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "llm-bench=cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
)
