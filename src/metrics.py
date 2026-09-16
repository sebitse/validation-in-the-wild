"""Metrics and agronomic reconciliation shared by the research notebook."""

from collections.abc import Sequence

import numpy as np
import pandas as pd


DEFAULT_TARGET_COLUMNS = (
    "Dry_Green_g",
    "Dry_Dead_g",
    "Dry_Clover_g",
    "GDM_g",
    "Dry_Total_g",
)
DEFAULT_TARGET_WEIGHTS = (0.1, 0.1, 0.1, 0.2, 0.5)


def weighted_r2_metric(y_true: np.ndarray, y_pred: np.ndarray, target_weights: Sequence[float] | None = None):
    """Calculate the competition-style global weighted R2 score."""
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    if y_true.ndim == 1:
        y_true = y_true.reshape(-1, 1)
    if y_pred.ndim == 1:
        y_pred = y_pred.reshape(-1, 1)
    if y_true.shape != y_pred.shape:
        raise ValueError(f"Shape mismatch: {y_true.shape} versus {y_pred.shape}")

    weights = np.asarray(
        DEFAULT_TARGET_WEIGHTS if target_weights is None else target_weights,
        dtype=np.float64,
    )
    if len(weights) != y_true.shape[1]:
        raise ValueError("One target weight is required per output column.")

    ss_res = np.sum(weights * np.sum((y_true - y_pred) ** 2, axis=0))
    global_mean = np.average(np.mean(y_true, axis=0), weights=weights)
    ss_tot = np.sum(weights * np.sum((y_true - global_mean) ** 2, axis=0))
    return float(1.0 - ss_res / (ss_tot + 1e-8))


def calculate_regression_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model_name: str = "specialist",
    target_cols: Sequence[str] | None = None,
    target_weights: Sequence[float] | None = None,
) -> tuple[dict[str, float | str], pd.DataFrame]:

    """Return the original aggregate and per-target regression metrics."""

    target_cols = list(DEFAULT_TARGET_COLUMNS if target_cols is None else target_cols)
    weights = np.asarray(
        DEFAULT_TARGET_WEIGHTS if target_weights is None else target_weights,
        dtype=float,
    )

    weights = weights / weights.sum()
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    if y_true.shape != y_pred.shape or y_true.ndim != 2:
        raise ValueError("Expected matching two-dimensional target and prediction arrays.")

    # These are the raw-value forms used by scikit-learn in the source notebook.
    # Keeping the formulas local also lets the dependency-light smoke suite run.
    mae = np.mean(np.abs(y_true - y_pred), axis=0)
    mse = np.mean((y_true - y_pred) ** 2, axis=0)
    rmse = np.sqrt(mse)
    r2 = []
    for column in range(y_true.shape[1]):
        truth = y_true[:, column]
        denominator = np.sum((truth - truth.mean()) ** 2)
        r2.append(1.0 - np.sum((truth - y_pred[:, column]) ** 2) / (denominator + 1e-8))

    per_target = pd.DataFrame(
        {
            "Model": model_name,
            "Target": target_cols,
            "R2": r2,
            "MAE_g": mae,
            "RMSE_g": rmse,
        }
    )
    summary = {
        "Model": model_name,
        "Weighted_R2": weighted_r2_metric(y_true, y_pred, weights),
        "Macro_MAE_g": float(np.mean(mae)),
        "Macro_RMSE_g": float(np.mean(rmse)),
        "Weighted_MAE_g": float(np.sum(weights * mae)),
        "Weighted_RMSE_g": float(np.sqrt(np.sum(weights * mse))),
    }
    return summary, per_target


def post_process_biomass(df_preds: pd.DataFrame) -> pd.DataFrame:
    """Project predictions onto the agronomic constraints and enforce non-negativity."""

    ordered = ["Dry_Green_g", "Dry_Clover_g", "Dry_Dead_g", "GDM_g", "Dry_Total_g"]

    if not all(column in df_preds.columns for column in ordered):
        raise ValueError(f"Reconciliation requires columns {ordered}")

    values = df_preds[ordered].to_numpy(dtype=float).T
    constraints = np.array(
        [[1, 1, 0, -1, 0], [0, 0, 1, 1, -1]],
        dtype=float,
    )

    projection = (
        np.eye(5)
        - constraints.T
        @ np.linalg.pinv(constraints @ constraints.T)
        @ constraints
    )

    reconciled = (projection @ values).T.clip(min=0)
    result = df_preds.copy()
    result[ordered] = reconciled
    result["GDM_g"] = result["Dry_Green_g"] + result["Dry_Clover_g"]
    result["Dry_Total_g"] = result["GDM_g"] + result["Dry_Dead_g"]

    return result


def reconcile_array(predictions: np.ndarray, target_cols: Sequence[str] = DEFAULT_TARGET_COLUMNS):
    """Apply biomass reconciliation to an array in target-column order."""

    target_cols = list(target_cols)
    frame = pd.DataFrame(np.asarray(predictions), columns=target_cols)
    return post_process_biomass(frame)[target_cols].to_numpy(dtype=float)

