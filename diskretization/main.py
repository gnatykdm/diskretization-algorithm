from utils import setup_logger, read_from_csv, load_df_to_csv, show_time
from logging import Logger
import pandas as pd
import os
import bisect
from collections import Counter

logger: Logger = setup_logger()

@show_time
def diskretization_alg(csv_path: str, column: str, label_column: str, n_bins: int = 2) -> None:
    if n_bins < 2:
        logger.error("n_bins must be at least 2.")
        return

    logger.info(f"Start discretization of column: '{column}' into {n_bins} bins")

    df: pd.DataFrame = read_from_csv(csv_path)
    if column not in df.columns or label_column not in df.columns:
        logger.error(f"Column '{column}' or '{label_column}' does not exist in dataset.")
        return

    data = list(zip(df[column], df[label_column]))
    data.sort(key=lambda x: x[0])
    intervals = [(None, None, data)]
    splits = []

    def get_possible_splits(subset):
        return [ (subset[i-1][0] + subset[i][0]) / 2
                 for i in range(1, len(subset)) if subset[i-1][0] != subset[i][0] ]

    def separated_pairs_fast(subset, split):
        left_labels = Counter(label for value, label in subset if value <= split)
        right_labels = Counter(label for value, label in subset if value > split)

        total_left = sum(left_labels.values())
        total_right = sum(right_labels.values())
        total = total_left * total_right

        matching_pairs = sum(left_labels[l] * right_labels[l] for l in left_labels if l in right_labels)
        return total - matching_pairs 

    for _ in range(n_bins - 1):
        best_gain = -1
        best_split = None
        best_interval_idx = None

        for idx, (low, high, subset) in enumerate(intervals):
            for s in get_possible_splits(subset):
                gain = separated_pairs_fast(subset, s)
                if gain > best_gain:
                    best_gain = gain
                    best_split = s
                    best_interval_idx = idx

        if best_split is None:
            logger.warning("No further splits possible.")
            break

        low, high, subset = intervals.pop(best_interval_idx)
        left = [d for d in subset if d[0] <= best_split]
        right = [d for d in subset if d[0] > best_split]

        intervals.insert(best_interval_idx, (best_split, high, right))
        intervals.insert(best_interval_idx, (low, best_split, left))
        splits.append(best_split)

        logger.info(f"Selected split {best_split:.4f} with separation gain {best_gain}")

    splits.sort()
    labels = [f"≤{splits[0]:.2f}"] + \
         [f">{splits[i - 1]:.2f}–≤{splits[i]:.2f}" for i in range(1, len(splits))] + \
         [f">{splits[-1]:.2f}"]


    def assign_bin(x):
        return labels[bisect.bisect_right(splits, x)]

    new_col = f"{column}_diskret"
    df[new_col] = df[column].apply(assign_bin)

    filename = os.path.basename(csv_path)
    output_path = f"diskretized_{filename}"
    load_df_to_csv(df, output_path)

    logger.info(f"Discretization complete: {len(labels)} bins. Output saved to '{output_path}'.")


def main() -> None:
    diskretization_alg("test_data.csv", "distance", "label", n_bins=3)

if __name__ == '__main__':
    main()
