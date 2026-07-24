"""Reusable dasymetric-allocation functions for block-level potential-sales analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd


def minmax(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0)
    lo, hi = values.min(), values.max()
    if hi == lo:
        return pd.Series(0.0, index=values.index)
    return (values - lo) / (hi - lo)


def build_commercial_score(
    frame: pd.DataFrame,
    indicator_cols: list[str],
    weights: list[float] | None = None,
) -> pd.Series:
    if not indicator_cols:
        raise ValueError("At least one indicator column is required.")
    if weights is None:
        weights = [1 / len(indicator_cols)] * len(indicator_cols)
    if len(weights) != len(indicator_cols) or not np.isclose(sum(weights), 1.0):
        raise ValueError("weights must match indicator_cols and sum to 1.")
    score = pd.Series(0.0, index=frame.index)
    for col, weight in zip(indicator_cols, weights):
        score += minmax(frame[col]) * weight
    return score.clip(lower=0)


def allocate_sales(
    pieces: gpd.GeoDataFrame,
    market_sales: pd.DataFrame,
    market_col: str,
    sales_col: str,
    score_col: str = "commercial_score",
    overlap_col: str = "overlap_ratio",
) -> gpd.GeoDataFrame:
    merged = pieces.merge(market_sales[[market_col, sales_col]], on=market_col, how="left")
    merged[sales_col] = pd.to_numeric(merged[sales_col], errors="coerce").fillna(0)
    merged[overlap_col] = pd.to_numeric(merged[overlap_col], errors="coerce").fillna(0)
    merged[score_col] = pd.to_numeric(merged[score_col], errors="coerce").fillna(0)

    merged["allocation_weight_raw"] = merged[score_col] * merged[overlap_col]
    denom = merged.groupby(market_col)["allocation_weight_raw"].transform("sum")
    fallback_denom = merged.groupby(market_col)[overlap_col].transform("sum")
    weighted = np.where(
        denom > 0,
        merged["allocation_weight_raw"] / denom,
        np.where(fallback_denom > 0, merged[overlap_col] / fallback_denom, 0),
    )
    merged["allocation_weight"] = weighted
    merged["potential_sales"] = merged[sales_col] * merged["allocation_weight"]
    return merged


def flag_undervalued_blocks(
    frame: pd.DataFrame,
    actual_col: str,
    potential_col: str = "potential_sales",
) -> pd.DataFrame:
    out = frame.copy()
    out["potential_gap"] = out[potential_col] - out[actual_col]
    q1, q3 = out["potential_gap"].quantile([0.25, 0.75])
    threshold = q3 + 1.5 * (q3 - q1)
    out["is_undervalued"] = out["potential_gap"] > threshold
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pieces", required=True, help="GeoJSON/GPKG with block-market pieces")
    parser.add_argument("--sales", required=True, help="CSV with market-level sales")
    parser.add_argument("--output", default="outputs/block_potential_sales.geojson")
    parser.add_argument("--market-col", default="TRDAR_CD")
    parser.add_argument("--sales-col", default="sales")
    parser.add_argument(
        "--indicators",
        nargs="+",
        default=["poi_density", "walk_access", "transit_access", "building_capacity"],
    )
    args = parser.parse_args()

    pieces = gpd.read_file(args.pieces)
    sales = pd.read_csv(args.sales)
    pieces["commercial_score"] = build_commercial_score(pieces, args.indicators)
    result = allocate_sales(pieces, sales, args.market_col, args.sales_col)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_file(output, driver="GeoJSON")
    print(f"Saved {len(result):,} block-market pieces to {output}")


if __name__ == "__main__":
    main()
