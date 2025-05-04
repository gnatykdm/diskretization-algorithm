import logging
from logging import Logger, Formatter, StreamHandler
from typing import Callable, Any
import pandas as pd
import time
import os

def show_time(func: Callable) -> Callable:
    def timer(*args: Any, **kwargs: Any) -> Any:
        start: float = time.time()
        result: Any = func(*args, **kwargs)
        finish: float = time.time()
        print(f"--[INFO] Time for all discretization - ({finish - start:.4f} sec) --")
        return result
    return timer

def setup_logger() -> Logger:
    logger: Logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch: StreamHandler = StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter: Formatter = Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(ch)

    return logger

logger: Logger = setup_logger()

def read_from_csv(csv_name: str) -> pd.DataFrame:
    if not csv_name:
        logger.error("CSV Path is NULL.")
        return pd.DataFrame()

    if not os.path.exists(csv_name):
        logger.error("CSV File does not exist.")
        return pd.DataFrame()

    df: pd.DataFrame = pd.read_csv(csv_name)
    logger.info(f"CSV file '{csv_name}' loaded successfully.")
    return df

def load_df_to_csv(df: pd.DataFrame, csv_name: str) -> None:
    if df.empty or not csv_name:
        logger.error("DataFrame is empty or CSV name is NULL.")
        return

    df.to_csv(csv_name, index=False, encoding="utf-8-sig")
    logger.info(f"DataFrame successfully saved to '{csv_name}'.")
