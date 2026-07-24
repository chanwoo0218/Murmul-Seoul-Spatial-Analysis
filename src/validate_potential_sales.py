"""Validation metrics for comparing estimated potential sales with later actual sales."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, spearmanr
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def safe_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    mask = y_true != 0
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100) if mask.any() else float("nan")


def smape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    denom = (np.abs(y_true) + np.abs(y_pred)) / 2
    mask = denom != 0
    return float(np.mean(np.abs(y_true[mask] - y_pred[mask]) / denom[mask]) * 100) if mask.any() else float("nan")


def topk_iou(y_true: pd.Series, y_pred: pd.Series, ratio: float = 0.1) -> float:
    k = max(1, int(len(y_true) * ratio))
    true_idx = set(y_true.nlargest(k).index)
    pred_idx = set(y_pred.nlargest(k).index)
    return len(true_idx & pred_idx) / len(true_idx | pred_idx)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--actual", required=True)
    parser.add_argument("--predicted", default="potential_sales")
    parser.add_argument("--output", default="outputs/validation_metrics.json")
    args = parser.parse_args()

    df = pd.read_csv(args.data).dropna(subset=[args.actual, args.predicted])
    y_true = df[args.actual].astype(float)
    y_pred = df[args.predicted].astype(float)
    metrics = {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mape": safe_mape(y_true.to_numpy(), y_pred.to_numpy()),
        "smape": smape(y_true.to_numpy(), y_pred.to_numpy()),
        "r2": float(r2_score(y_true, y_pred)),
        "spearman": float(spearmanr(y_true, y_pred).correlation),
        "kendall_tau": float(kendalltau(y_true, y_pred).correlation),
        "top10_iou": float(topk_iou(y_true, y_pred)),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
