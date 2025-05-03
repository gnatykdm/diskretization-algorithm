from utils import setup_logger, read_from_csv, load_df_to_csv, show_time
from logging import Logger
import pandas as pd
import itertools
import os

logger: Logger = setup_logger()

@show_time
def diskretization_alg(csv_path: str, column: str, label_column: str, n_bins: int = 2) -> None:
    logger.info(f"Start discretization of column: {column} into {n_bins} bins")

    df: pd.DataFrame = read_from_csv(csv_path)
    if column not in df.columns or label_column not in df.columns:
        logger.error(f"Column '{column}' or '{label_column}' does not exist.")
        return

    data = list(zip(df[column], df[label_column]))
    data.sort(key=lambda x: x[0])

    intervals = [(None, None, data)]  
    splits = []

    def get_possible_splits(subset):
        return [ (subset[i-1][0] + subset[i][0]) / 2
                 for i in range(1, len(subset)) if subset[i-1][0] != subset[i][0] ]

    def separated_pairs(subset, split):
        left = [d for d in subset if d[0] <= split]
        right = [d for d in subset if d[0] > split]
        return sum(1 for a, b in itertools.product(left, right) if a[1] != b[1])

    for _ in range(n_bins - 1):
        best_gain = -1
        best_interval_idx = None
        best_split = None

        for idx, (low, high, subset) in enumerate(intervals):
            poss = get_possible_splits(subset)
            for s in poss:
                gain = separated_pairs(subset, s)
                if gain > best_gain:
                    best_gain = gain
                    best_interval_idx = idx
                    best_split = s

        if best_split is None:
            logger.warning("No further splits possible.")
            break
        low, high, subset = intervals.pop(best_interval_idx)
        left = [d for d in subset if d[0] <= best_split]
        right = [d for d in subset if d[0] > best_split]
        intervals.insert(best_interval_idx, (best_split, high, right))
        intervals.insert(best_interval_idx, (low, best_split, left))
        splits.append(best_split)
        logger.info(f"Selected split {best_split} with gain {best_gain}")

    splits = sorted(splits)
    labels = []
    bounds = [-float('inf')] + splits + [float('inf')]
    for i in range(len(bounds)-1):
        low = bounds[i]
        high = bounds[i+1]
        if i == 0:
            labels.append(f"≤{high}")
        elif i == len(bounds)-2:
            labels.append(f">{low}")
        else:
            labels.append(f">{low}–≤{high}")

    def assign_bin(x):
        for i in range(len(splits)+1):
            if (i == 0 and x <= splits[0]) or \
               (i == len(splits) and x > splits[-1]) or \
               (0 < i < len(splits) and splits[i-1] < x <= splits[i]):
                return labels[i]
    new_col = f"{column}_diskret"
    df[new_col] = df[column].apply(assign_bin)

    filename = os.path.basename(csv_path)
    output_path = f"diskretized_{filename}"
    load_df_to_csv(df, output_path)
    logger.info(f"Discretization complete: {len(labels)} bins. Saved to {output_path}")


def main() -> None:
    diskretization_alg("test_data.csv", "distance", "label", n_bins=3)

if __name__ == '__main__':
    main()
