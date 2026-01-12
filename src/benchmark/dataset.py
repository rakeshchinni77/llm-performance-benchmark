import json
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd

from benchmark.exceptions import DatasetError


def load_dataset(
    path: str,
    fmt: str,
    text_field: str,
    max_prompts: int | None = None,
) -> List[Dict[str, Any]]:
    """
    Load a prompt dataset from CSV or JSONL format.

    Returns a list of dicts with at least:
        {
            "id": <int>,
            "prompt": <str>
        }
    """
    dataset_path = Path(path)

    if not dataset_path.exists():
        raise DatasetError(f"Dataset file not found: {dataset_path}")

    if fmt not in {"csv", "jsonl"}:
        raise DatasetError(f"Unsupported dataset format: {fmt}")

    records: List[Dict[str, Any]] = []

    try:
        if fmt == "csv":
            df = pd.read_csv(dataset_path)

            if text_field not in df.columns:
                raise DatasetError(
                    f"Missing required column '{text_field}' in CSV dataset"
                )

            for idx, row in df.iterrows():
                records.append(
                    {
                        "id": int(idx),
                        "prompt": str(row[text_field]),
                    }
                )

        elif fmt == "jsonl":
            with open(dataset_path, "r", encoding="utf-8") as f:
                for idx, line in enumerate(f):
                    if not line.strip():
                        continue

                    obj = json.loads(line)

                    if text_field not in obj:
                        raise DatasetError(
                            f"Missing required field '{text_field}' in JSONL record at line {idx + 1}"
                        )

                    records.append(
                        {
                            "id": obj.get("id", idx),
                            "prompt": str(obj[text_field]),
                        }
                    )

    except (json.JSONDecodeError, pd.errors.ParserError) as exc:
        raise DatasetError(f"Failed to parse dataset: {exc}") from exc

    if not records:
        raise DatasetError("Dataset is empty after loading")

    if max_prompts is not None:
        records = records[: max_prompts]

    return records
