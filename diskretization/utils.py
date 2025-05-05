import logging
from logging import Logger, Formatter, StreamHandler
from typing import Callable, Any
import pandas as pd
import time
import os


def setup_logger() -> Logger:
    logger: Logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.setLevel(logging.INFO) 

        ch: StreamHandler = StreamHandler()
        ch.setLevel(logging.INFO)

        formatter: Formatter = Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        logger.propagate = False 

    return logger

logger: Logger = setup_logger()

def read_from_csv(csv_path: str) -> pd.DataFrame:
    if not csv_path:
        logger.error("CSV Path is NULL.")
        return pd.DataFrame()

    if not os.path.exists(csv_path):
        logger.error(f"CSV File does not exist: {csv_path}")
        return pd.DataFrame()

    try:
        df: pd.DataFrame = pd.read_csv(csv_path)
        if df.empty:
             logger.warning(f"CSV file '{csv_path}' is empty.")
        else:
            logger.info(f"CSV file '{csv_path}' loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error reading CSV file '{csv_path}': {e}")
        return pd.DataFrame()


def load_df_to_csv(df: pd.DataFrame, csv_path: str) -> None:
    if df.empty:
        logger.warning("DataFrame is empty, not saving.")
        return
    if not csv_path:
        logger.error("Output CSV path is NULL.")
        return

    try:
        output_dir = os.path.dirname(csv_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")

        df.to_csv(csv_path, index=False, header=False, encoding="utf-8-sig")
        logger.info(f"DataFrame successfully saved to '{csv_path}'.")
    except Exception as e:
        logger.error(f"Error saving DataFrame to CSV '{csv_path}': {e}")