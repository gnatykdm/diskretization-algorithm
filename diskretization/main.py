from utils import setup_logger, read_from_csv, load_df_to_csv
from typing import Any
from logging import Logger
import pandas as pd
import os
import bisect
from collections import Counter
import time
import numpy as np 

logger: Logger = setup_logger()

from utils import setup_logger, read_from_csv, load_df_to_csv
from typing import Any
from logging import Logger
import pandas as pd
import os
import bisect
from collections import Counter
import numpy as np

logger: Logger = setup_logger()


def _get_possible_splits(subset: list[tuple[float, Any]]) -> list[float]:
    subset.sort(key=lambda x: x[0])
    return [
        (subset[i - 1][0] + subset[i][0]) / 2
        for i in range(1, len(subset)) if subset[i - 1][0] != subset[i][0]
    ]


def _separated_pairs_fast(subset: list[tuple[float, Any]], split: float) -> int:
    left_labels = Counter(label for value, label in subset if value <= split)
    right_labels = Counter(label for value, label in subset if value > split)

    total_left = sum(left_labels.values())
    total_right = sum(right_labels.values())
    total_pairs = total_left * total_right

    matching_pairs = sum(
        left_labels[l] * right_labels[l] for l in left_labels if l in right_labels
    )
    return total_pairs - matching_pairs


def _format_interval(value: float, splits: list[float]) -> str:
    if not splits:
        return "(-inf; inf)"

    idx = bisect.bisect_right(splits, value)

    if idx == 0:
        return f"(-inf; {splits[0]}]"
    elif idx == len(splits):
        return f"({splits[-1]}; inf)"
    else:
        return f"({splits[idx - 1]}; {splits[idx]}]"


def discretize_attribute(data_tuples: list[tuple[float, Any]], n_bins: int) -> list[float]:
    if n_bins < 2:
        logger.warning("n_bins < 2, no discretization will be performed for this attribute.")
        return []

    intervals = [(None, None, sorted(data_tuples, key=lambda x: x[0]))]
    splits = []

    for _ in range(n_bins - 1):
        candidate_splits = []

        for idx, (_, _, subset) in enumerate(intervals):
            possible_splits = _get_possible_splits(subset)
            if not possible_splits:
                continue

            for s in possible_splits:
                if s not in splits:
                    gain = _separated_pairs_fast(subset, s)
                    candidate_splits.append((gain, s, idx))

        if not candidate_splits:
            logger.warning("No further informative splits found for this attribute.")
            break

        candidate_splits.sort(key=lambda x: x[0], reverse=True)
        best_gain, best_split, best_interval_idx = candidate_splits[0]

        if best_gain < 0:
            logger.warning("No positive gain split found.")
            break

        splits.append(best_split)
        _, _, subset_to_split = intervals.pop(best_interval_idx)
        left_subset = [d for d in subset_to_split if d[0] <= best_split]
        right_subset = [d for d in subset_to_split if d[0] > best_split]

        intervals.insert(best_interval_idx, (best_split, None, right_subset))
        intervals.insert(best_interval_idx, (None, best_split, left_subset))

    splits.sort()
    logger.info(f"Found {len(splits)} splits for the attribute.")
    return splits


def discretize_dataset(csv_path: str, n_bins_per_attribute: int = 2) -> None:
    logger.info(f"Starting discretization process for: {csv_path}")

    df: pd.DataFrame = read_from_csv(csv_path)
    if df.empty:
        logger.error("Input DataFrame is empty. Aborting.")
        return

    if df.shape[1] < 2:
        logger.error("Dataset must have at least one attribute and one decision column.")
        return

    decision_column_name = df.columns[-1]
    attribute_column_names = df.columns[:-1]

    df_discretized = pd.DataFrame()

    for col_name in attribute_column_names:
        logger.info(f"Discretizing attribute: '{col_name}'")
        if not pd.api.types.is_numeric_dtype(df[col_name]):
            logger.warning(f"Column '{col_name}' is not numeric. Skipping discretization.")
            df_discretized[col_name] = df[col_name]
            continue

        data_tuples = list(zip(df[col_name], df[decision_column_name]))
        splits = discretize_attribute(data_tuples, n_bins_per_attribute)
        df_discretized[col_name] = df[col_name].apply(lambda x: _format_interval(x, splits))

    df_discretized[decision_column_name] = df[decision_column_name]

    output_dir = os.path.dirname(csv_path)
    if not output_dir:
        output_dir = "."
    base_name = os.path.basename(csv_path)
    if base_name.lower().endswith('.csv'):
        output_base_name = f"DISC{base_name}"
    else:
        output_base_name = f"DISC{base_name}.csv"

    output_path = os.path.join(output_dir, output_base_name)
    load_df_to_csv(df_discretized, output_path)

    logger.info(f"Discretization complete. Output saved to: {output_path}")

if __name__ == '__main__':
    discretize_dataset("./test_data/data1.csv", n_bins_per_attribute=3)
