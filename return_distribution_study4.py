#!/usr/bin/env python3
"""
return_distribution_study.py
================================

Self-contained empirical stock-return distribution study framework.

Run:
    python return_distribution_study.py

This is a single standalone file. All configuration is embedded in the
DEFAULT_CONFIG dictionary below -- edit that dictionary directly to control the
scope of the analysis (inputs, frequency, distributions, estimation, ranking,
outputs, etc.). No external configuration file is required.

Optionally, you may still override settings from a YAML file if PyYAML is
installed by passing --config path/to/config.yml, but this is entirely optional;
the script is fully functional on its own.

What this program does
----------------------
1. Loads price or return time series from CSV/Parquet files or optional tickers.
2. Supports one or many assets, with or without a date column.
3. Computes simple/log/excess returns and aggregates to D/W/M horizons.
4. Cleans missing/stale values, optionally winsorizes and volatility-standardizes.
5. Fits configurable candidate distributions using SciPy and optional scikit-learn.
6. Computes EDA statistics, in-sample goodness-of-fit, out-of-sample validation,
   VaR/ES forecasts and backtests, rankings and plots.
7. Estimates per-asset Merton jump-diffusion parameters (mu, sigma, lambda,
   mu_j, sigma_j) by MLE -- everything needed to run a next-stage Monte Carlo
   simulation WITH a jump component (see simulate_merton()).
8. Writes the parameter estimates in wide and/or long format (the long format
   adds explicit param_name, role, note, and per-asset rank columns).
9. Writes CSV tables and PNG charts to a configurable output directory.

Core dependencies
-----------------
Required: numpy, pandas, scipy, matplotlib
Optional: pyyaml for optional external --config overrides; scikit-learn for
Gaussian mixtures; statsmodels for Ljung-Box and ARCH-LM diagnostics; yfinance
for ticker downloads. All optional dependencies degrade gracefully if absent.

Configuration reference
-----------------------
input:
  paths: list of CSV/Parquet files. If empty, tickers can be used if yfinance is installed.
  tickers: optional symbols to download with yfinance.
  start_date/end_date: ticker-download date range.
  has_date_column: whether files include an explicit date column.
  date_column/date_format: date parsing controls.
  price_columns/return_columns: explicit asset columns. If empty, numeric columns are inferred.
  column_mapping: optional rename map from source column names to desired asset names.
  price_or_return: 'price' or 'return'.
  csv_options/parquet_options: forwarded to pandas readers.
frequency:
  target: target return horizon, one of D/W/M.
  source_frequency: descriptive only; usually D for daily input.
  aggregation_method: non_overlapping or overlapping. Non-overlapping is used for dated data.
  return_type: simple, log, or excess.
  risk_free: risk-free handling for excess returns.
preprocessing:
  handle_missing: drop, ffill, bfill, interpolate.
  stale_price: checks repeated prices before computing returns if prices are supplied.
  winsorize: optional clipping by quantiles.
  volatility_standardization: optional rolling z-score by estimated volatility.
  outlier_policy: keep, flag, winsorize, drop.
  minimum_observations: minimum usable observations per asset.
distributions:
  enabled: model names to fit.
  settings: distribution-specific parameter settings.
estimation:
  method: MLE is implemented through scipy.stats.fit where applicable.
  bootstrap: optional bootstrap confidence intervals for fitted parameters.
in_sample:
  metrics: metrics to report; all implemented metrics are calculated where feasible.
out_of_sample:
  validation scheme and parameters; static split is fully implemented, rolling/expanding
  are supported in a simplified walk-forward mode.
tail_risk:
  VaR/ES confidence levels and backtest options.
ranking:
  dimension weights and normalization method.
  normalization: 'percentile' | 'zscore' | 'minmax' | 'borda' | 'none'.
  normalize_per_asset: True normalizes within each asset (per-asset scorecard is
    never pooled across assets); False normalizes across the whole pooled table.
output:
  output_dir and toggles for CSV tables and PNG plots.
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import os
import sys
import time
import warnings
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

try:
    import yaml
    YAML_AVAILABLE = True
except Exception:
    yaml = None
    YAML_AVAILABLE = False

try:
    import scipy.stats as st
    from scipy import optimize
    from scipy.special import gammaln
except Exception as exc:  # pragma: no cover
    raise SystemExit("SciPy is required. Install with: pip install scipy") from exc

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception as exc:  # pragma: no cover
    raise SystemExit("matplotlib is required. Install with: pip install matplotlib") from exc

try:
    from sklearn.mixture import GaussianMixture
    SKLEARN_AVAILABLE = True
except Exception:
    GaussianMixture = None
    SKLEARN_AVAILABLE = False

try:
    import statsmodels.api as sm
    from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
    STATSMODELS_AVAILABLE = True
except Exception:
    sm = None
    acorr_ljungbox = None
    het_arch = None
    STATSMODELS_AVAILABLE = False

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except Exception:
    yf = None
    YFINANCE_AVAILABLE = False

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)

DEFAULT_CONFIG: Dict[str, Any] = {
    "input": {
        "paths": ["C:/Users/s6983759/Desktop/bf1_macro1/study_return_distribution/input_return_sample.csv"],
        "tickers": [],
        "start_date": None,
        "end_date": None,
        "has_date_column": False,
        "date_column": None,
        "date_format": None,
        "price_columns": [],
        "return_columns": ["asset_1", "asset_2", "asset_3"],
        "column_mapping": {},
        "price_or_return": "return",
        "csv_options": {"sep": ",", "encoding": "utf-8"},
        "parquet_options": {},
    },
    "frequency": {
        "target": "D",
        "source_frequency": "D",
        "aggregation_method": "non_overlapping",
        "return_type": "log",
        "risk_free": {
            "enabled": False,
            "annual_rate": 0.0,
            "column": None,
            "day_count": 252,
        },
    },
    "preprocessing": {
        "handle_missing": "drop",
        "stale_price": {"enabled": False, "max_consecutive_stale": 5, "treat_as_missing": False},
        "winsorize": {"enabled": False, "lower_quantile": 0.001, "upper_quantile": 0.999},
        "volatility_standardization": {"enabled": False, "window": 63, "demean": True, "min_periods": 20},
        "outlier_policy": {"method": "keep", "zscore_threshold": 8.0},
        "minimum_observations": 100,
    },
    "distributions": {
        "enabled": [
            "normal",
            "student_t",
            "skewed_t",
            "ged",
            "johnsonsu",
            "normal_inverse_gaussian",
            "genhyperbolic",
            "gaussian_mixture",
            "generalized_pareto",
        ],
        "settings": {
            "gaussian_mixture": {"n_components": 2, "covariance_type": "full", "random_state": 42, "max_iter": 500},
            "generalized_pareto": {"tail": "left", "threshold_quantile": 0.05},
            "all": {"fit_timeout_seconds": 60},
        },
    },
    "estimation": {
        "method": "MLE",
        "bootstrap": {"enabled": False, "n_boot": 500, "random_state": 42, "ci_level": 0.95, "sample_fraction": 1.0},
    },
    # ------------------------------------------------------------------
    # JUMP block. Estimates Merton jump-diffusion parameters PER ASSET so
    # the next-stage Monte Carlo can include a jump (Poisson) component.
    #   method:
    #     "merton_mle"  -> full 5-parameter MLE (mu, sigma, lambda, mu_j,
    #                       sigma_j) on the return series. Recommended.
    #     "threshold"   -> fast method-of-moments: flag |r| above a
    #                       volatility-scaled threshold as jumps, then
    #                       lambda = n_jumps / years, and jump-size moments
    #                       from the flagged returns. Used as MLE seed too.
    #   periods_per_year: annualization factor for lambda. For sequence-
    #     independent / no-date data this is only a labeling convention
    #     (252=daily, 52=weekly, 12=monthly); jump COUNTS are unaffected.
    #   threshold_sigma: jump cutoff in units of robust sigma (Lee-Mykland
    #     style); 3.0-4.0 is standard.
    # ------------------------------------------------------------------
    "jump": {
        "enabled": True,
        "method": "merton_mle",          # "merton_mle" | "threshold"
        "periods_per_year": 252,
        "threshold_sigma": 4.0,
        "n_max_jumps": 10,                # truncation of the Poisson sum in MLE
        "max_iter": 500,
        "random_state": 42,
    },
    "in_sample": {
        "metrics": ["loglik", "AIC", "BIC", "HQC", "KS", "AD", "CvM", "CDF_RMSE", "CDF_MAE", "quantile_error"],
        "quantile_grid": [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.975, 0.99, 0.995, 0.999],
        "tail_weighted": True,
    },
    "out_of_sample": {
        "enabled": False,
        "method": "split",
        "split_fraction": 0.7,
        "rolling_window": 750,
        "expanding_min_window": 750,
        "refit_frequency": 20,
        "min_test_observations": 50,
    },
    "tail_risk": {
        "enabled": True,
        "confidence_levels": [0.90, 0.95, 0.975, 0.99, 0.995],
        "tail": "left",
        "backtests": {"kupiec": True, "christoffersen": False, "dynamic_quantile": False, "basel_traffic_light": True, "es_exceedance_residual": True},
    },
    "ranking": {
        "weights": {"statistical_fit": 0.25, "tail_fit": 0.30, "out_of_sample": 0.25, "stability_robustness": 0.10, "practical_usefulness": 0.10},
        # normalization: "percentile" | "zscore" | "minmax" | "borda" | "none".
        #   Use "none" to skip normalization entirely (raw metrics, oriented so higher=better).
        "normalization": "percentile",
        # normalize_per_asset: when True (default), normalization is computed WITHIN
        #   each asset so the per-asset scorecard never pools assets together.
        #   When False, normalization is computed across the whole pooled table.
        #   (Ignored when normalization == "none".)
        "normalize_per_asset": True,
        "higher_is_better_metrics": ["loglik", "oos_loglik", "stability_score", "practical_score"],
        "lower_is_better_metrics": ["AIC", "BIC", "HQC", "KS", "AD", "CvM", "CDF_RMSE", "CDF_MAE", "quantile_error", "tail_score_raw"],
        "practical_scores": {"normal": 0.95, "student_t": 0.90, "skewed_t": 0.75, "ged": 0.75, "johnsonsu": 0.65, "normal_inverse_gaussian": 0.55, "genhyperbolic": 0.50, "gaussian_mixture": 0.45, "generalized_pareto": 0.60},
    },
    "output": {
        "output_dir": "C:/Users/s6983759/Desktop/bf1_macro1/study_return_distribution/output",
        "save_tables": True,
        # param_format controls how parameter_estimates is written:
        #   "wide" -> parameter_estimates.csv only (param_0..param_n columns)
        #   "long" -> parameter_estimates_long.csv only (one row per param,
        #             with param_name, value, role, note, and rank columns)
        #   "both" -> write BOTH files (default)
        "param_format": "both",
        "save_plots": True,
        "plot_formats": ["png"],
        "plots": {"histogram_fitted_density": True, "ecdf_fitted": True, "qq": True, "pit_histogram": True, "var_exceedance": True, "rolling_vol": False},
        "verbosity": 1,
        "random_seed": 42,
    },
}

SCIPY_DISTS = {
    "normal": st.norm,
    "student_t": st.t,
    "skewed_t": st.skewnorm,  # practical skewed proxy; SciPy lacks Hansen skew-t
    "ged": st.gennorm,
    "johnsonsu": st.johnsonsu,
    "normal_inverse_gaussian": st.norminvgauss,
}
if hasattr(st, "genhyperbolic"):
    SCIPY_DISTS["genhyperbolic"] = st.genhyperbolic

PARAM_COUNTS = {
    "normal": 2,
    "student_t": 3,
    "skewed_t": 3,
    "ged": 3,
    "johnsonsu": 4,
    "normal_inverse_gaussian": 4,
    "genhyperbolic": 5,
    "gaussian_mixture": None,
    "generalized_pareto": 3,
}

# ---------------------------------------------------------------------------
# Parameter NAMES, in the exact positional order returned by scipy's .fit()
# (shape parameters first, then loc, then scale). These line up 1:1 with the
# param_0, param_1, ... columns in the wide parameter_estimates table and are
# used to build the long-format table and to drive Monte Carlo simulation.
# ---------------------------------------------------------------------------
PARAM_NAMES: Dict[str, List[str]] = {
    "normal": ["loc", "scale"],
    "student_t": ["df", "loc", "scale"],
    "skewed_t": ["a", "loc", "scale"],          # a = skewness (skewnorm proxy)
    "ged": ["beta", "loc", "scale"],            # beta = shape (gennorm)
    "johnsonsu": ["a", "b", "loc", "scale"],     # a=skew, b=tail
    "normal_inverse_gaussian": ["a", "b", "loc", "scale"],  # a=tail, b=asymmetry
    "genhyperbolic": ["p", "a", "b", "loc", "scale"],
    "generalized_pareto": ["c", "loc", "scale"],  # c = tail index xi
}

# Human-readable description of each (distribution, parameter).
PARAM_NOTES: Dict[Tuple[str, str], str] = {
    ("normal", "loc"): "mean (mu)",
    ("normal", "scale"): "standard deviation (sigma)",
    ("student_t", "df"): "degrees of freedom (nu); lower = fatter tails",
    ("student_t", "loc"): "location (mu)",
    ("student_t", "scale"): "scale (sigma); not the std unless df large",
    ("skewed_t", "a"): "skewness shape (skewnorm 'a'); 0 = symmetric",
    ("skewed_t", "loc"): "location",
    ("skewed_t", "scale"): "scale",
    ("ged", "beta"): "shape (gennorm beta); 2=normal, <2 fat tails, >2 thin",
    ("ged", "loc"): "location (mu)",
    ("ged", "scale"): "scale",
    ("johnsonsu", "a"): "skewness shape (gamma)",
    ("johnsonsu", "b"): "tail/kurtosis shape (delta); must be > 0",
    ("johnsonsu", "loc"): "location (xi)",
    ("johnsonsu", "scale"): "scale (lambda)",
    ("normal_inverse_gaussian", "a"): "tail heaviness (alpha*delta)",
    ("normal_inverse_gaussian", "b"): "asymmetry (beta*delta)",
    ("normal_inverse_gaussian", "loc"): "location (mu)",
    ("normal_inverse_gaussian", "scale"): "scale (delta)",
    ("genhyperbolic", "p"): "lambda (subfamily/GIG shape)",
    ("genhyperbolic", "a"): "tail heaviness (alpha*delta)",
    ("genhyperbolic", "b"): "asymmetry (beta*delta)",
    ("genhyperbolic", "loc"): "location (mu)",
    ("genhyperbolic", "scale"): "scale (delta)",
    ("generalized_pareto", "c"): "tail index xi; >0 heavy tail (POT excesses)",
    ("generalized_pareto", "loc"): "threshold offset (fixed at 0 in this study)",
    ("generalized_pareto", "scale"): "scale (beta) of the excess distribution",
}


def _param_role(pname: str) -> str:
    if pname == "loc":
        return "location"
    if pname == "scale":
        return "scale"
    if pname.startswith("weight"):
        return "weight"
    if pname.startswith("mean"):
        return "location"
    if pname.startswith("variance"):
        return "scale"
    if pname.startswith("jump_") or pname in ("lambda", "diffusion_mu", "diffusion_sigma"):
        return "jump"
    if pname.startswith("meta"):
        return "meta"
    return "shape"


@dataclass
class FittedModel:
    name: str
    params: Any
    success: bool
    message: str = ""
    n_params: int = 0
    train_n: int = 0
    meta: Optional[Dict[str, Any]] = None

    def logpdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        if not self.success:
            return np.full_like(x, np.nan, dtype=float)
        if self.name == "gaussian_mixture":
            gm = self.params
            return gm.score_samples(x.reshape(-1, 1))
        if self.name == "generalized_pareto":
            return gpd_logpdf_unconditional(x, self.params, self.meta or {})
        dist = SCIPY_DISTS[self.name]
        return dist.logpdf(x, *self.params)

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        if not self.success:
            return np.full_like(x, np.nan, dtype=float)
        if self.name == "gaussian_mixture":
            return gm_cdf(self.params, x)
        if self.name == "generalized_pareto":
            return gpd_cdf_unconditional(x, self.params, self.meta or {})
        dist = SCIPY_DISTS[self.name]
        return dist.cdf(x, *self.params)

    def ppf(self, q: np.ndarray) -> np.ndarray:
        q = np.asarray(q, dtype=float)
        if not self.success:
            return np.full_like(q, np.nan, dtype=float)
        if self.name == "gaussian_mixture":
            return gm_ppf(self.params, q)
        if self.name == "generalized_pareto":
            return gpd_ppf_unconditional(q, self.params, self.meta or {})
        dist = SCIPY_DISTS[self.name]
        return dist.ppf(q, *self.params)

    def mean(self) -> float:
        try:
            if self.name == "gaussian_mixture":
                return float(np.dot(self.params.weights_, self.params.means_.ravel()))
            if self.name == "generalized_pareto":
                return np.nan
            return float(SCIPY_DISTS[self.name].mean(*self.params))
        except Exception:
            return np.nan


def deep_update(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_update(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path: Optional[str]) -> Dict[str, Any]:
    """Return the embedded DEFAULT_CONFIG, optionally overridden by a YAML file.

    The script is fully standalone: configuration lives in DEFAULT_CONFIG. An
    external YAML override is only applied if an explicit --config path is given
    and PyYAML is installed; otherwise the embedded defaults are used.
    """
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    if path:
        if not YAML_AVAILABLE:
            print("PyYAML not installed; ignoring --config and using embedded DEFAULT_CONFIG.")
        elif not os.path.exists(path):
            print(f"Config file not found ({path}); using embedded DEFAULT_CONFIG.")
        else:
            with open(path, "r", encoding="utf-8") as f:
                user_cfg = yaml.safe_load(f) or {}
            cfg = deep_update(cfg, user_cfg)
            print(f"Loaded config override: {path}")
    else:
        print("Using embedded DEFAULT_CONFIG (standalone mode).")
    return cfg


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def infer_numeric_columns(df: pd.DataFrame, exclude: Iterable[str]) -> List[str]:
    exclude_set = set([e for e in exclude if e])
    return [c for c in df.columns if c not in exclude_set and pd.api.types.is_numeric_dtype(df[c])]


def load_data(config: Dict[str, Any]) -> pd.DataFrame:
    """Load prices or returns from CSV/Parquet files or optional yfinance tickers."""
    icfg = config["input"]
    frames: List[pd.DataFrame] = []
    paths = icfg.get("paths") or []
    for path in paths:
        if not path:
            continue
        if not os.path.exists(path):
            alt = os.path.join(os.getcwd(), path)
            if os.path.exists(alt):
                path = alt
            else:
                print(f"WARNING: input path not found and skipped: {path}")
                continue
        ext = os.path.splitext(path)[1].lower()
        if ext in [".parquet", ".pq"]:
            df = pd.read_parquet(path, **(icfg.get("parquet_options") or {}))
        else:
            df = pd.read_csv(path, **(icfg.get("csv_options") or {}))
        df = prepare_input_frame(df, icfg)
        frames.append(df)
    tickers = icfg.get("tickers") or []
    if tickers:
        if not YFINANCE_AVAILABLE:
            print("WARNING: yfinance not installed; ticker download skipped.")
        else:
            data = yf.download(tickers, start=icfg.get("start_date"), end=icfg.get("end_date"), auto_adjust=True, progress=False)
            if isinstance(data.columns, pd.MultiIndex):
                px = data.get("Close") if "Close" in data.columns.get_level_values(0) else data.iloc[:, 0]
            else:
                px = data[["Close"]].rename(columns={"Close": tickers[0]})
            px.index = pd.to_datetime(px.index)
            frames.append(px)
    if not frames:
        raise ValueError("No input data loaded. Provide input.paths or tickers.")
    if len(frames) == 1:
        out = frames[0]
    else:
        out = pd.concat(frames, axis=1)
    out = out.loc[:, ~out.columns.duplicated()]
    return out


def prepare_input_frame(df: pd.DataFrame, icfg: Dict[str, Any]) -> pd.DataFrame:
    mapping = icfg.get("column_mapping") or {}
    if mapping:
        df = df.rename(columns=mapping)
    has_date = bool(icfg.get("has_date_column", True))
    date_col = icfg.get("date_column")
    if has_date and date_col and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], format=icfg.get("date_format"), errors="coerce")
        df = df.dropna(subset=[date_col]).sort_values(date_col).set_index(date_col)
    elif has_date and date_col and date_col not in df.columns:
        print(f"WARNING: date column {date_col} not found; treating rows as ordered observations.")
        df.index = pd.RangeIndex(len(df))
    else:
        df.index = pd.RangeIndex(len(df))
    explicit = icfg.get("price_columns") or icfg.get("return_columns") or []
    cols = explicit if explicit else infer_numeric_columns(df, exclude=[date_col])
    if not cols:
        raise ValueError("No numeric asset columns found.")
    out = df[cols].apply(pd.to_numeric, errors="coerce")
    return out


def flag_stale_prices(prices: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    scfg = config["preprocessing"].get("stale_price", {})
    if not scfg.get("enabled", False):
        return prices
    max_stale = int(scfg.get("max_consecutive_stale", 5))
    if not scfg.get("treat_as_missing", False):
        return prices
    out = prices.copy()
    for col in out.columns:
        same = out[col].diff().eq(0)
        groups = (~same).cumsum()
        run = same.groupby(groups).cumcount() + 1
        out.loc[same & (run >= max_stale), col] = np.nan
    return out


def compute_returns(data: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """Compute returns from prices or pass through pre-computed returns."""
    icfg = config["input"]
    fcfg = config["frequency"]
    kind = (icfg.get("price_or_return") or "price").lower()
    rtype = (fcfg.get("return_type") or "log").lower()
    data = data.sort_index() if isinstance(data.index, pd.DatetimeIndex) else data.copy()
    if kind == "return":
        ret = data.copy()
    else:
        px = flag_stale_prices(data, config)
        if rtype == "log":
            ret = np.log(px / px.shift(1))
        else:
            ret = px.pct_change()
    ret = aggregate_frequency(ret, config)
    if rtype == "excess" or bool(fcfg.get("risk_free", {}).get("enabled", False)):
        ret = subtract_risk_free(ret, config)
    return ret


def aggregate_frequency(returns: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """Aggregate daily returns to daily/weekly/monthly horizons."""
    target = (config["frequency"].get("target") or "D").upper()
    rtype = (config["frequency"].get("return_type") or "log").lower()
    if target == "D":
        return returns
    if isinstance(returns.index, pd.DatetimeIndex):
        rule = "W-FRI" if target == "W" else "M"
        if rtype == "log":
            return returns.resample(rule).sum(min_count=1)
        return (1.0 + returns).resample(rule).prod(min_count=1) - 1.0
    step = 5 if target == "W" else 21
    arr = []
    idx = []
    for start in range(0, len(returns), step):
        block = returns.iloc[start:start + step]
        if len(block) == 0:
            continue
        if rtype == "log":
            arr.append(block.sum(axis=0, min_count=1))
        else:
            arr.append((1.0 + block).prod(axis=0) - 1.0)
        idx.append(start + len(block) - 1)
    return pd.DataFrame(arr, index=idx, columns=returns.columns)


def subtract_risk_free(ret: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    rf = config["frequency"].get("risk_free", {})
    day_count = float(rf.get("day_count", 252))
    target = (config["frequency"].get("target") or "D").upper()
    periods = {"D": day_count, "W": 52.0, "M": 12.0}.get(target, day_count)
    if rf.get("column") and rf.get("column") in ret.columns:
        return ret.drop(columns=[rf.get("column")]).sub(ret[rf.get("column")], axis=0)
    rate = float(rf.get("annual_rate", 0.0) or 0.0)
    per = rate / periods
    return ret - per


def preprocess(returns: pd.DataFrame, config: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Clean missing values, handle outliers, winsorize and optionally volatility-standardize."""
    pcfg = config["preprocessing"]
    x = returns.replace([np.inf, -np.inf], np.nan).copy()
    method = pcfg.get("handle_missing", "drop")
    if method == "ffill":
        x = x.ffill().dropna(how="all")
    elif method == "bfill":
        x = x.bfill().dropna(how="all")
    elif method == "interpolate":
        x = x.interpolate().dropna(how="all")
    else:
        x = x.dropna(how="all")
    flags = pd.DataFrame(False, index=x.index, columns=x.columns)
    opol = pcfg.get("outlier_policy", {})
    if opol.get("method", "keep") in ["flag", "drop", "winsorize"]:
        zthr = float(opol.get("zscore_threshold", 8.0))
        z = (x - x.mean()) / x.std(ddof=1).replace(0, np.nan)
        flags = z.abs() > zthr
        if opol.get("method") == "drop":
            x = x.mask(flags)
        elif opol.get("method") == "winsorize":
            x = x.clip(lower=x.quantile(0.001), upper=x.quantile(0.999), axis=1)
    wcfg = pcfg.get("winsorize", {})
    if wcfg.get("enabled", False):
        lo = float(wcfg.get("lower_quantile", 0.001))
        hi = float(wcfg.get("upper_quantile", 0.999))
        x = x.clip(lower=x.quantile(lo), upper=x.quantile(hi), axis=1)
    vcfg = pcfg.get("volatility_standardization", {})
    if vcfg.get("enabled", False):
        window = int(vcfg.get("window", 63))
        minp = int(vcfg.get("min_periods", max(5, window // 3)))
        vol = x.rolling(window, min_periods=minp).std().replace(0, np.nan)
        mu = x.rolling(window, min_periods=minp).mean() if vcfg.get("demean", True) else 0.0
        x = (x - mu) / vol
    x = x.dropna(how="all")
    return x, flags


def eda_summary(series: pd.Series, asset: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Return descriptive statistics and optional diagnostics for one return series."""
    x = series.dropna().astype(float)
    out = {
        "asset": asset,
        "n": int(x.size),
        "mean": x.mean(),
        "median": x.median(),
        "std": x.std(ddof=1),
        "skew": x.skew(),
        "excess_kurtosis": x.kurtosis(),
        "min": x.min(),
        "max": x.max(),
        "iqr": x.quantile(0.75) - x.quantile(0.25),
        "q001": x.quantile(0.001),
        "q01": x.quantile(0.01),
        "q05": x.quantile(0.05),
        "q95": x.quantile(0.95),
        "q99": x.quantile(0.99),
        "q999": x.quantile(0.999),
    }
    if x.size >= 8:
        try:
            jb = st.jarque_bera(x)
            out["jarque_bera_stat"] = float(jb.statistic)
            out["jarque_bera_p"] = float(jb.pvalue)
        except Exception:
            pass
    if STATSMODELS_AVAILABLE and x.size >= 20:
        try:
            lb = acorr_ljungbox(x, lags=[min(10, x.size // 5)], return_df=True)
            out["ljung_box_p"] = float(lb["lb_pvalue"].iloc[-1])
            arch_res = het_arch(x - x.mean(), nlags=min(10, x.size // 5))
            out["arch_lm_p"] = float(arch_res[1])
        except Exception:
            pass
    try:
        out["hill_left_5pct"] = hill_estimator(-x, 0.05)
        out["hill_right_5pct"] = hill_estimator(x, 0.05)
    except Exception:
        pass
    return out


def hill_estimator(x: pd.Series, tail_fraction: float = 0.05) -> float:
    vals = np.sort(np.asarray(x.dropna(), dtype=float))
    vals = vals[vals > 0]
    if vals.size < 20:
        return np.nan
    k = max(5, int(vals.size * tail_fraction))
    top = vals[-k:]
    threshold = vals[-k - 1] if vals.size > k else vals[0]
    if threshold <= 0:
        return np.nan
    return float(np.mean(np.log(top / threshold)))


def fit_distribution(x: np.ndarray, name: str, config: Dict[str, Any]) -> FittedModel:
    """Fit a named distribution to a one-dimensional return sample."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if x.size < 5:
        return FittedModel(name, None, False, "too few observations", train_n=x.size)
    try:
        if name == "gaussian_mixture":
            return fit_gaussian_mixture(x, config)
        if name == "generalized_pareto":
            return fit_gpd_tail(x, config)
        if name not in SCIPY_DISTS:
            return FittedModel(name, None, False, "not available in scipy", train_n=x.size)
        dist = SCIPY_DISTS[name]
        if name == "normal":
            params = dist.fit(x)
        else:
            params = dist.fit(x)
        k = len(params)
        return FittedModel(name=name, params=params, success=True, n_params=k, train_n=x.size, meta={"params": params})
    except Exception as exc:
        return FittedModel(name, None, False, f"fit failed: {exc}", train_n=x.size)


def fit_gaussian_mixture(x: np.ndarray, config: Dict[str, Any]) -> FittedModel:
    if not SKLEARN_AVAILABLE:
        return FittedModel("gaussian_mixture", None, False, "scikit-learn unavailable", train_n=x.size)
    s = config["distributions"].get("settings", {}).get("gaussian_mixture", {})
    n_components = int(s.get("n_components", 2))
    gm = GaussianMixture(n_components=n_components, covariance_type=s.get("covariance_type", "full"), random_state=s.get("random_state", 42), max_iter=int(s.get("max_iter", 500)))
    gm.fit(x.reshape(-1, 1))
    k = (n_components - 1) + n_components + n_components
    return FittedModel("gaussian_mixture", gm, True, n_params=k, train_n=x.size, meta={"n_components": n_components})


def fit_gpd_tail(x: np.ndarray, config: Dict[str, Any]) -> FittedModel:
    s = config["distributions"].get("settings", {}).get("generalized_pareto", {})
    tail = s.get("tail", config.get("tail_risk", {}).get("tail", "left"))
    q = float(s.get("threshold_quantile", 0.05))
    if tail == "left":
        threshold = np.quantile(x, q)
        excess = threshold - x[x <= threshold]
        p_tail = np.mean(x <= threshold)
    else:
        threshold = np.quantile(x, 1 - q)
        excess = x[x >= threshold] - threshold
        p_tail = np.mean(x >= threshold)
    excess = excess[excess >= 0]
    if excess.size < 20:
        return FittedModel("generalized_pareto", None, False, "too few tail observations", train_n=x.size)
    c, loc, scale = st.genpareto.fit(excess, floc=0)
    meta = {"tail": tail, "threshold": float(threshold), "p_tail": float(p_tail), "body_min": float(np.min(x)), "body_max": float(np.max(x))}
    return FittedModel("generalized_pareto", (c, loc, scale), True, n_params=3, train_n=x.size, meta=meta)


def gm_cdf(gm: Any, x: np.ndarray) -> np.ndarray:
    vals = np.zeros_like(x, dtype=float)
    means = gm.means_.ravel()
    weights = gm.weights_.ravel()
    if gm.covariance_type == "full":
        stds = np.sqrt(gm.covariances_.reshape(-1))
    elif gm.covariance_type == "diag":
        stds = np.sqrt(gm.covariances_.reshape(-1))
    elif gm.covariance_type == "tied":
        stds = np.repeat(np.sqrt(gm.covariances_.reshape(-1)[0]), len(weights))
    else:
        stds = np.sqrt(gm.covariances_.reshape(-1))
    for w, m, s in zip(weights, means, stds):
        vals += w * st.norm.cdf(x, loc=m, scale=max(s, 1e-12))
    return np.clip(vals, 0, 1)


def gm_ppf(gm: Any, q: np.ndarray) -> np.ndarray:
    q = np.asarray(q, dtype=float)
    means = gm.means_.ravel()
    std = float(np.sqrt(np.max(gm.covariances_)))
    lo = np.min(means) - 12 * std
    hi = np.max(means) + 12 * std
    out = []
    for qi in q:
        try:
            root = optimize.brentq(lambda z: gm_cdf(gm, np.array([z]))[0] - qi, lo, hi, maxiter=100)
        except Exception:
            grid = np.linspace(lo, hi, 2000)
            root = grid[np.argmin(np.abs(gm_cdf(gm, grid) - qi))]
        out.append(root)
    return np.asarray(out)


def gpd_cdf_unconditional(x: np.ndarray, params: Tuple[float, float, float], meta: Dict[str, Any]) -> np.ndarray:
    tail = meta.get("tail", "left")
    threshold = float(meta.get("threshold"))
    p_tail = float(meta.get("p_tail", 0.05))
    c, loc, scale = params
    out = np.empty_like(x, dtype=float)
    if tail == "left":
        mask = x <= threshold
        excess = threshold - x[mask]
        out[mask] = p_tail * (1.0 - st.genpareto.cdf(excess, c, loc=loc, scale=scale))
        body = ~mask
        span = max(float(meta.get("body_max", threshold)) - threshold, 1e-12)
        out[body] = p_tail + (1 - p_tail) * np.clip((x[body] - threshold) / span, 0, 1)
    else:
        mask = x >= threshold
        body = ~mask
        span = max(threshold - float(meta.get("body_min", threshold)), 1e-12)
        out[body] = (1 - p_tail) * np.clip((x[body] - float(meta.get("body_min", 0))) / span, 0, 1)
        excess = x[mask] - threshold
        out[mask] = 1 - p_tail + p_tail * st.genpareto.cdf(excess, c, loc=loc, scale=scale)
    return np.clip(out, 0, 1)


def gpd_ppf_unconditional(q: np.ndarray, params: Tuple[float, float, float], meta: Dict[str, Any]) -> np.ndarray:
    tail = meta.get("tail", "left")
    threshold = float(meta.get("threshold"))
    p_tail = float(meta.get("p_tail", 0.05))
    c, loc, scale = params
    q = np.asarray(q, dtype=float)
    out = np.empty_like(q, dtype=float)
    if tail == "left":
        mask = q <= p_tail
        out[mask] = threshold - st.genpareto.ppf(1 - q[mask] / p_tail, c, loc=loc, scale=scale)
        body = ~mask
        out[body] = threshold + (q[body] - p_tail) / max(1 - p_tail, 1e-12) * (float(meta.get("body_max", threshold)) - threshold)
    else:
        mask = q >= 1 - p_tail
        out[mask] = threshold + st.genpareto.ppf((q[mask] - (1 - p_tail)) / p_tail, c, loc=loc, scale=scale)
        body = ~mask
        out[body] = float(meta.get("body_min", threshold)) + q[body] / max(1 - p_tail, 1e-12) * (threshold - float(meta.get("body_min", threshold)))
    return out


def gpd_logpdf_unconditional(x: np.ndarray, params: Tuple[float, float, float], meta: Dict[str, Any]) -> np.ndarray:
    tail = meta.get("tail", "left")
    threshold = float(meta.get("threshold"))
    p_tail = float(meta.get("p_tail", 0.05))
    c, loc, scale = params
    out = np.full_like(x, -20.0, dtype=float)
    if tail == "left":
        mask = x <= threshold
        out[mask] = np.log(max(p_tail, 1e-12)) + st.genpareto.logpdf(threshold - x[mask], c, loc=loc, scale=scale)
    else:
        mask = x >= threshold
        out[mask] = np.log(max(p_tail, 1e-12)) + st.genpareto.logpdf(x[mask] - threshold, c, loc=loc, scale=scale)
    return out


def gof_metrics(x: np.ndarray, model: FittedModel, config: Dict[str, Any]) -> Dict[str, Any]:
    """Compute in-sample goodness-of-fit metrics."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    n = x.size
    out = {"distribution": model.name, "success": model.success, "n": n, "message": model.message}
    if not model.success or n == 0:
        return out
    lp = model.logpdf(x)
    lp = np.where(np.isfinite(lp), lp, -1e6)
    ll = float(np.sum(lp))
    k = int(model.n_params or 1)
    out.update({"loglik": ll, "n_params": k, "AIC": 2 * k - 2 * ll, "BIC": np.log(max(n, 1)) * k - 2 * ll, "HQC": 2 * k * np.log(np.log(max(n, 3))) - 2 * ll})
    xs = np.sort(x)
    emp = np.arange(1, n + 1) / (n + 1)
    cdf = np.clip(model.cdf(xs), 1e-9, 1 - 1e-9)
    dif = cdf - emp
    out["KS"] = float(np.max(np.abs(dif)))
    out["CvM"] = float(np.mean(dif ** 2) + 1.0 / (12 * n))
    out["AD"] = float(anderson_darling_from_cdf(cdf, n))
    out["CDF_RMSE"] = float(np.sqrt(np.mean(dif ** 2)))
    out["CDF_MAE"] = float(np.mean(np.abs(dif)))
    qgrid = np.asarray(config["in_sample"].get("quantile_grid", [0.01, 0.05, 0.5, 0.95, 0.99]), dtype=float)
    try:
        empq = np.quantile(x, qgrid)
        fitq = model.ppf(qgrid)
        out["quantile_error"] = float(np.nanmean(np.abs(empq - fitq)))
        tails = (qgrid <= 0.05) | (qgrid >= 0.95)
        out["tail_quantile_error"] = float(np.nanmean(np.abs(empq[tails] - fitq[tails]))) if tails.any() else np.nan
    except Exception:
        out["quantile_error"] = np.nan
        out["tail_quantile_error"] = np.nan
    return out


def anderson_darling_from_cdf(cdf: np.ndarray, n: int) -> float:
    cdf = np.clip(np.sort(cdf), 1e-9, 1 - 1e-9)
    i = np.arange(1, n + 1)
    return float(-n - np.mean((2 * i - 1) * (np.log(cdf) + np.log(1 - cdf[::-1]))))


def oos_validate(x: np.ndarray, name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Perform out-of-sample validation using split, rolling or expanding windows."""
    ocfg = config["out_of_sample"]
    if not ocfg.get("enabled", True):
        return {"distribution": name, "oos_enabled": False}
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    min_test = int(ocfg.get("min_test_observations", 50))
    if n < min_test + 50:
        return {"distribution": name, "oos_enabled": True, "oos_message": "too few observations"}
    method = ocfg.get("method", "split")
    pits: List[float] = []
    logliks: List[float] = []
    if method == "split":
        split = int(n * float(ocfg.get("split_fraction", 0.7)))
        split = min(max(split, 20), n - min_test)
        model = fit_distribution(x[:split], name, config)
        if not model.success:
            return {"distribution": name, "oos_enabled": True, "oos_message": model.message}
        test = x[split:]
        logliks = list(model.logpdf(test))
        pits = list(model.cdf(test))
    else:
        refit = int(ocfg.get("refit_frequency", 20))
        if method == "rolling":
            win = int(ocfg.get("rolling_window", 750))
            start = min(max(win, 50), n - min_test)
        else:
            start = min(max(int(ocfg.get("expanding_min_window", 750)), 50), n - min_test)
        model = None
        for t in range(start, n):
            if model is None or (t - start) % refit == 0:
                train = x[max(0, t - int(ocfg.get("rolling_window", 750))):t] if method == "rolling" else x[:t]
                model = fit_distribution(train, name, config)
            if model and model.success:
                logliks.append(float(model.logpdf(np.array([x[t]]))[0]))
                pits.append(float(model.cdf(np.array([x[t]]))[0]))
    lp = np.asarray(logliks, dtype=float)
    pit = np.asarray(pits, dtype=float)
    pit = pit[np.isfinite(pit)]
    out = {"distribution": name, "oos_enabled": True, "oos_n": int(lp.size), "oos_loglik": float(np.nansum(lp)), "oos_avg_loglik": float(np.nanmean(lp)) if lp.size else np.nan}
    if pit.size > 10:
        out["pit_mean"] = float(np.mean(pit))
        out["pit_std"] = float(np.std(pit, ddof=1))
        try:
            out["pit_ks_uniform_stat"] = float(st.kstest(pit, "uniform").statistic)
            out["pit_ks_uniform_p"] = float(st.kstest(pit, "uniform").pvalue)
        except Exception:
            pass
    out["pit_values"] = pit.tolist()[:100000]
    return out


def tail_risk_backtest(x: np.ndarray, model: FittedModel, config: Dict[str, Any]) -> pd.DataFrame:
    """Compute VaR/ES and Kupiec/Christoffersen exceedance backtests."""
    tcfg = config["tail_risk"]
    if not tcfg.get("enabled", True) or not model.success:
        return pd.DataFrame()
    tail = tcfg.get("tail", "left")
    rows = []
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    for cl in tcfg.get("confidence_levels", [0.95, 0.99]):
        alpha = 1 - float(cl)
        qprob = alpha if tail == "left" else float(cl)
        try:
            var = float(model.ppf(np.array([qprob]))[0])
            es = expected_shortfall(model, qprob, tail=tail)
        except Exception:
            var, es = np.nan, np.nan
        if tail == "left":
            hits = x < var
            loss_mag = var - x[hits]
        else:
            hits = x > var
            loss_mag = x[hits] - var
        n = len(x)
        exc = int(np.sum(hits))
        kup_stat, kup_p = kupiec_test(exc, n, alpha)
        chr_ind, chr_ind_p, chr_cc, chr_cc_p = christoffersen_test(hits, alpha)
        basel = basel_traffic_light(exc, n, alpha) if tcfg.get("backtests", {}).get("basel_traffic_light", True) else ""
        rows.append({
            "distribution": model.name,
            "confidence_level": cl,
            "tail": tail,
            "VaR": var,
            "ES": es,
            "n": n,
            "exceedances": exc,
            "expected_exceedances": n * alpha,
            "exceedance_rate": exc / n if n else np.nan,
            "kupiec_LR_uc": kup_stat,
            "kupiec_p": kup_p,
            "christoffersen_LR_ind": chr_ind,
            "christoffersen_ind_p": chr_ind_p,
            "christoffersen_LR_cc": chr_cc,
            "christoffersen_cc_p": chr_cc_p,
            "avg_exceedance_magnitude": float(np.mean(loss_mag)) if loss_mag.size else 0.0,
            "max_exceedance_magnitude": float(np.max(loss_mag)) if loss_mag.size else 0.0,
            "basel_zone": basel,
        })
    return pd.DataFrame(rows)


def expected_shortfall(model: FittedModel, qprob: float, tail: str = "left") -> float:
    if model.name == "generalized_pareto":
        qs = np.linspace(max(1e-5, qprob / 200), qprob, 500) if tail == "left" else np.linspace(qprob, min(0.99999, 1 - (1 - qprob) / 200), 500)
    else:
        qs = np.linspace(1e-4, qprob, 500) if tail == "left" else np.linspace(qprob, 0.9999, 500)
    vals = model.ppf(qs)
    return float(np.nanmean(vals))


def kupiec_test(exceedances: int, n: int, alpha: float) -> Tuple[float, float]:
    if n <= 0:
        return np.nan, np.nan
    phat = exceedances / n
    if phat <= 0 or phat >= 1:
        phat = min(max(phat, 1e-12), 1 - 1e-12)
    alpha = min(max(alpha, 1e-12), 1 - 1e-12)
    ll0 = (n - exceedances) * np.log(1 - alpha) + exceedances * np.log(alpha)
    ll1 = (n - exceedances) * np.log(1 - phat) + exceedances * np.log(phat)
    lr = -2 * (ll0 - ll1)
    return float(lr), float(1 - st.chi2.cdf(lr, 1))


def christoffersen_test(hits: np.ndarray, alpha: float) -> Tuple[float, float, float, float]:
    h = np.asarray(hits, dtype=int)
    if h.size < 2:
        return np.nan, np.nan, np.nan, np.nan
    h0, h1 = h[:-1], h[1:]
    n00 = np.sum((h0 == 0) & (h1 == 0)); n01 = np.sum((h0 == 0) & (h1 == 1))
    n10 = np.sum((h0 == 1) & (h1 == 0)); n11 = np.sum((h0 == 1) & (h1 == 1))
    def safe_log(p): return np.log(np.clip(p, 1e-12, 1 - 1e-12))
    pi01 = n01 / max(n00 + n01, 1)
    pi11 = n11 / max(n10 + n11, 1)
    pi = (n01 + n11) / max(n00 + n01 + n10 + n11, 1)
    ll_ind = (n00 + n10) * safe_log(1 - pi) + (n01 + n11) * safe_log(pi)
    ll_dep = n00 * safe_log(1 - pi01) + n01 * safe_log(pi01) + n10 * safe_log(1 - pi11) + n11 * safe_log(pi11)
    lr_ind = -2 * (ll_ind - ll_dep)
    exc = int(h.sum())
    lr_uc, _ = kupiec_test(exc, len(h), alpha)
    lr_cc = lr_uc + lr_ind
    return float(lr_ind), float(1 - st.chi2.cdf(lr_ind, 1)), float(lr_cc), float(1 - st.chi2.cdf(lr_cc, 2))


def basel_traffic_light(exceedances: int, n: int, alpha: float) -> str:
    if n <= 0:
        return "NA"
    # Probability zones from binomial quantiles; aligns conceptually with Basel green/yellow/red.
    q95 = st.binom.ppf(0.95, n, alpha)
    q9999 = st.binom.ppf(0.9999, n, alpha)
    if exceedances <= q95:
        return "green"
    if exceedances <= q9999:
        return "yellow"
    return "red"


# ===========================================================================
# JUMP ESTIMATION (Merton jump-diffusion) -- per asset
# ===========================================================================
# The Merton (1976) jump-diffusion log-return over one period is a Poisson
# mixture of normals:
#     r = (mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z + sum_{i=1}^{N} J_i
# with N ~ Poisson(lambda*dt) and J_i ~ Normal(mu_j, sigma_j^2). The density
# is the standard infinite Poisson-weighted sum of normals, truncated at
# n_max_jumps for numerical evaluation. We estimate the 5 parameters
# (mu, sigma, lambda, mu_j, sigma_j) by maximum likelihood, seeded by a
# threshold (method-of-moments) jump detector. dt = 1 / periods_per_year.

def _merton_neg_loglik(params: np.ndarray, r: np.ndarray, dt: float, n_max: int) -> float:
    mu, sigma, lam, mu_j, sigma_j = params
    if sigma <= 1e-9 or sigma_j < 0 or lam < 0:
        return 1e12
    ks = np.arange(0, n_max + 1)
    log_pois = -lam * dt + ks * np.log(max(lam * dt, 1e-300)) - gammaln(ks + 1.0)
    drift = (mu - 0.5 * sigma * sigma) * dt
    total = np.zeros_like(r, dtype=float)
    for j, k in enumerate(ks):
        mean_k = drift + k * mu_j
        var_k = sigma * sigma * dt + k * sigma_j * sigma_j
        if var_k <= 0:
            continue
        comp = np.exp(log_pois[j]) * np.exp(-0.5 * (r - mean_k) ** 2 / var_k) / np.sqrt(2.0 * np.pi * var_k)
        total = total + comp
    total = np.maximum(total, 1e-300)
    return float(-np.sum(np.log(total)))


def threshold_jump_estimates(r: np.ndarray, dt: float, threshold_sigma: float) -> Dict[str, float]:
    """Method-of-moments jump estimates via a robust volatility-scaled cutoff.

    A return is flagged as a jump if |r - median| exceeds threshold_sigma times a
    robust (MAD-based) sigma. lambda is jumps-per-year; jump-size mean/std come
    from the flagged returns; diffusion mu/sigma from the non-jump returns.
    """
    r = np.asarray(r, dtype=float)
    r = r[np.isfinite(r)]
    med = float(np.median(r))
    mad = float(np.median(np.abs(r - med))) * 1.4826
    robust_sigma = mad if mad > 1e-12 else float(np.std(r))
    cutoff = threshold_sigma * robust_sigma
    is_jump = np.abs(r - med) > cutoff
    n_jumps = int(np.sum(is_jump))
    years = max(len(r) * dt, 1e-9)
    lam = n_jumps / years
    if n_jumps >= 2:
        mu_j = float(np.mean(r[is_jump] - med))
        sigma_j = float(np.std(r[is_jump], ddof=1))
    elif n_jumps == 1:
        mu_j = float(r[is_jump][0] - med)
        sigma_j = robust_sigma
    else:
        mu_j = 0.0
        sigma_j = robust_sigma
    body = r[~is_jump] if np.any(~is_jump) else r
    diff_mu = float(np.mean(body) / dt) if dt > 0 else float(np.mean(body))
    diff_sigma = float(np.std(body, ddof=1) / np.sqrt(dt)) if dt > 0 else float(np.std(body, ddof=1))
    return {
        "n_jumps": float(n_jumps),
        "lambda": float(lam),
        "jump_mu": mu_j,
        "jump_sigma": float(max(sigma_j, 1e-8)),
        "diffusion_mu": diff_mu,
        "diffusion_sigma": float(max(diff_sigma, 1e-8)),
        "threshold": float(cutoff),
    }


def estimate_jump_parameters(x: np.ndarray, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Estimate Merton jump-diffusion parameters for a single asset's returns.

    Returns a dict of named parameters ready for Monte Carlo, or None if the
    jump block is disabled / data is insufficient.
    """
    jcfg = config.get("jump", {})
    if not jcfg.get("enabled", False):
        return None
    r = np.asarray(x, dtype=float)
    r = r[np.isfinite(r)]
    if r.size < 30:
        return None
    ppy = float(jcfg.get("periods_per_year", 252))
    dt = 1.0 / ppy if ppy > 0 else 1.0
    thr_sigma = float(jcfg.get("threshold_sigma", 4.0))
    method = jcfg.get("method", "merton_mle")
    seed = threshold_jump_estimates(r, dt, thr_sigma)
    result: Dict[str, Any] = {
        "method": method,
        "periods_per_year": ppy,
        "dt": dt,
        "threshold_sigma": thr_sigma,
        "n_jumps_detected": seed["n_jumps"],
    }
    if method == "threshold":
        result.update({
            "diffusion_mu": seed["diffusion_mu"],
            "diffusion_sigma": seed["diffusion_sigma"],
            "lambda": seed["lambda"],
            "jump_mu": seed["jump_mu"],
            "jump_sigma": seed["jump_sigma"],
            "converged": True,
        })
        return result
    # ---- Merton MLE (seeded by threshold estimates) ----
    n_max = int(jcfg.get("n_max_jumps", 10))
    x0 = np.array([
        seed["diffusion_mu"],
        max(seed["diffusion_sigma"], 1e-4),
        max(seed["lambda"], 1.0),          # at least ~1 jump/yr as a starting point
        seed["jump_mu"],
        max(seed["jump_sigma"], 1e-3),
    ], dtype=float)
    bounds = [(-10.0, 10.0), (1e-4, 5.0), (0.0, ppy), (-2.0, 2.0), (1e-4, 2.0)]
    try:
        res = optimize.minimize(
            _merton_neg_loglik, x0, args=(r, dt, n_max),
            method="L-BFGS-B", bounds=bounds,
            options={"maxiter": int(jcfg.get("max_iter", 500))},
        )
        mu, sigma, lam, mu_j, sigma_j = res.x
        converged = bool(res.success)
        nll = float(res.fun)
    except Exception as exc:
        result.update({
            "diffusion_mu": seed["diffusion_mu"], "diffusion_sigma": seed["diffusion_sigma"],
            "lambda": seed["lambda"], "jump_mu": seed["jump_mu"], "jump_sigma": seed["jump_sigma"],
            "converged": False, "message": f"MLE failed: {exc}; using threshold seed",
        })
        return result
    k = 5
    n = r.size
    aic = 2 * k + 2 * nll
    bic = k * np.log(n) + 2 * nll
    result.update({
        "diffusion_mu": float(mu),
        "diffusion_sigma": float(sigma),
        "lambda": float(lam),
        "jump_mu": float(mu_j),
        "jump_sigma": float(sigma_j),
        "loglik": float(-nll),
        "AIC": float(aic),
        "BIC": float(bic),
        "converged": converged,
    })
    return result


def simulate_merton(jump_params: Dict[str, Any], n_periods: int, n_paths: int = 1,
                    horizon_periods: int = 1, random_state: int = 42) -> np.ndarray:
    """Monte Carlo helper: simulate Merton jump-diffusion RETURNS.

    Returns an array of simulated per-horizon returns using the estimated
    diffusion + Poisson jump parameters. Each simulated value sums
    `horizon_periods` independent one-period returns. Output shape:
    (n_paths, n_periods) if n_paths>1 else (n_periods,).
    """
    rng = np.random.default_rng(random_state)
    dt = float(jump_params.get("dt", 1.0 / float(jump_params.get("periods_per_year", 252))))
    mu = float(jump_params["diffusion_mu"])
    sigma = float(jump_params["diffusion_sigma"])
    lam = float(jump_params["lambda"])
    mu_j = float(jump_params["jump_mu"])
    sigma_j = float(jump_params["jump_sigma"])
    drift = (mu - 0.5 * sigma * sigma) * dt
    out = np.zeros((n_paths, n_periods), dtype=float)
    for _ in range(horizon_periods):
        diff = drift + sigma * np.sqrt(dt) * rng.standard_normal((n_paths, n_periods))
        n_jumps = rng.poisson(lam * dt, size=(n_paths, n_periods))
        jump_sum = np.where(n_jumps > 0,
                            rng.normal(n_jumps * mu_j, np.sqrt(np.maximum(n_jumps, 0)) * sigma_j),
                            0.0)
        out += diff + jump_sum
    return out[0] if n_paths == 1 else out


# ===========================================================================
# LONG-FORMAT PARAMETER TABLE
# ===========================================================================

def _as_pylist(cell: Any) -> List[float]:
    if isinstance(cell, list):
        return cell
    if cell is None or (isinstance(cell, float) and pd.isna(cell)):
        return []
    try:
        return list(ast.literal_eval(str(cell)))
    except Exception:
        return []


def build_param_long(params_df: pd.DataFrame, ranking_df: pd.DataFrame,
                     jump_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Convert wide parameter_estimates into a long table with named params.

    Columns: asset, distribution, rank, param_name, value, role, note.
    `rank` is each distribution's rank within its asset (from ranking_scorecard).
    Gaussian-mixture weights/means/variances are expanded per component, GPD meta
    fields are surfaced, and (optionally) Merton jump parameters are appended as a
    pseudo-distribution named 'merton_jump' so MC has everything in one place.
    """
    rank_map: Dict[Tuple[Any, str], Any] = {}
    if ranking_df is not None and not ranking_df.empty and "rank" in ranking_df.columns:
        for _, rr in ranking_df.iterrows():
            rank_map[(rr.get("asset"), rr.get("distribution"))] = rr.get("rank")
    rows: List[Dict[str, Any]] = []

    def emit(asset, dist, pname, value, note=""):
        rows.append({
            "asset": asset, "distribution": dist,
            "rank": rank_map.get((asset, dist), np.nan),
            "param_name": pname, "value": value,
            "role": _param_role(pname), "note": note,
        })

    if params_df is not None and not params_df.empty:
        param_cols = [c for c in params_df.columns if c.startswith("param_")]
        for _, r in params_df.iterrows():
            asset = r.get("asset", "")
            dist = r["distribution"]
            if dist == "gaussian_mixture":
                weights = _as_pylist(r.get("weights"))
                means = _as_pylist(r.get("means"))
                covs = _as_pylist(r.get("covariances"))
                for kk in range(len(weights)):
                    emit(asset, dist, f"weight_{kk}", weights[kk], f"mixing weight of component {kk}")
                    emit(asset, dist, f"mean_{kk}", means[kk], f"mean of component {kk}")
                    emit(asset, dist, f"variance_{kk}", covs[kk], f"variance of component {kk} (std=sqrt)")
            else:
                names = PARAM_NAMES.get(dist)
                if names is None:
                    for c in param_cols:
                        v = r.get(c)
                        if pd.notna(v):
                            emit(asset, dist, c, v, "")
                else:
                    for i, pname in enumerate(names):
                        v = r.get(f"param_{i}")
                        if pd.notna(v):
                            emit(asset, dist, pname, v, PARAM_NOTES.get((dist, pname), ""))
            for mc in ["meta_tail", "meta_threshold", "meta_p_tail", "meta_body_min", "meta_body_max"]:
                if mc in params_df.columns:
                    v = r.get(mc)
                    if pd.notna(v) and v != "":
                        emit(asset, dist, mc.replace("meta_", "meta:"), v, "context, not a fitted parameter")

    # Append Merton jump parameters as a pseudo-distribution row group.
    if jump_df is not None and not jump_df.empty:
        jp_fields = [
            ("diffusion_mu", "Merton diffusion drift mu (annualized)"),
            ("diffusion_sigma", "Merton diffusion volatility sigma (annualized)"),
            ("lambda", "jump intensity (expected jumps per year)"),
            ("jump_mu", "mean jump size (log)"),
            ("jump_sigma", "std dev of jump size (log)"),
            ("periods_per_year", "annualization factor used (dt = 1/this)"),
            ("n_jumps_detected", "jumps flagged by threshold detector"),
        ]
        for _, jr in jump_df.iterrows():
            asset = jr.get("asset", "")
            for fld, note in jp_fields:
                if fld in jump_df.columns and pd.notna(jr.get(fld)):
                    rows.append({
                        "asset": asset, "distribution": "merton_jump",
                        "rank": np.nan, "param_name": fld, "value": jr.get(fld),
                        "role": _param_role(fld), "note": note,
                    })

    cols = ["asset", "distribution", "rank", "param_name", "value", "role", "note"]
    out = pd.DataFrame(rows, columns=cols)
    if not out.empty:
        out = out.sort_values(["asset", "rank", "distribution"], na_position="last").reset_index(drop=True)
    return out


def bootstrap_parameters(x: np.ndarray, name: str, config: Dict[str, Any]) -> pd.DataFrame:
    bcfg = config["estimation"].get("bootstrap", {})
    if not bcfg.get("enabled", False):
        return pd.DataFrame()
    rng = np.random.default_rng(int(bcfg.get("random_state", 42)))
    n_boot = int(bcfg.get("n_boot", 200))
    frac = float(bcfg.get("sample_fraction", 1.0))
    n = len(x)
    rows = []
    for b in range(n_boot):
        sample = rng.choice(x, size=max(5, int(frac * n)), replace=True)
        m = fit_distribution(sample, name, config)
        if m.success and isinstance(m.params, tuple):
            row = {"distribution": name, "bootstrap": b}
            for i, p in enumerate(m.params):
                row[f"param_{i}"] = p
            rows.append(row)
    return pd.DataFrame(rows)


def normalize_scores(df: pd.DataFrame, metric: str, higher: bool, method: str) -> pd.Series:
    vals = pd.to_numeric(df[metric], errors="coerce")
    if method == "none":
        # No normalization: use raw values oriented so that higher == better,
        # leaving cross-metric aggregation to operate on the raw scale.
        out = vals if higher else -vals
        return out.fillna(out.mean() if out.notna().any() else 0.0)
    if vals.notna().sum() <= 1:
        return pd.Series(0.5, index=df.index)
    if method == "zscore":
        z = (vals - vals.mean()) / vals.std(ddof=1)
        if not higher:
            z = -z
        return pd.Series(st.norm.cdf(z.fillna(0)), index=df.index)
    if method == "minmax":
        mn, mx = vals.min(), vals.max()
        score = (vals - mn) / (mx - mn) if mx > mn else pd.Series(0.5, index=df.index)
        if not higher:
            score = 1 - score
        return score.fillna(0.0)
    if method == "borda":
        rank = vals.rank(ascending=not higher, method="average")
        return 1 - (rank - 1) / max(len(vals) - 1, 1)
    # percentile default
    pct = vals.rank(pct=True, ascending=not higher)
    return pct.fillna(0.0)


def rank_models(metrics_df: pd.DataFrame, oos_df: pd.DataFrame, tail_df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """Rank fitted models by statistical fit, tail fit, OOS, robustness and practicality."""
    if metrics_df.empty:
        return pd.DataFrame()
    r = metrics_df.copy()
    if not oos_df.empty:
        oos_slim = oos_df.drop(columns=["pit_values"], errors="ignore")
        r = r.merge(oos_slim, on=["asset", "distribution"], how="left")
    if not tail_df.empty:
        tail_summary = tail_df.groupby(["asset", "distribution"], as_index=False).agg({"kupiec_p": "mean", "christoffersen_cc_p": "mean", "avg_exceedance_magnitude": "mean", "exceedance_rate": "mean"})
        tail_summary["tail_score_raw"] = (1 - tail_summary["kupiec_p"].fillna(0)) + (1 - tail_summary["christoffersen_cc_p"].fillna(0)) + tail_summary["avg_exceedance_magnitude"].fillna(0).rank(pct=True)
        r = r.merge(tail_summary[["asset", "distribution", "tail_score_raw", "kupiec_p", "christoffersen_cc_p"]], on=["asset", "distribution"], how="left")
    weights = config["ranking"].get("weights", {})
    method = config["ranking"].get("normalization", "percentile")
    # When True (default), normalization is computed WITHIN each asset so the
    # per-asset scorecard never pools assets together. When False, normalization
    # is computed across the whole pooled table.
    per_asset = bool(config["ranking"].get("normalize_per_asset", True))
    practical_map = config["ranking"].get("practical_scores", {})
    r["practical_score"] = r["distribution"].map(practical_map).fillna(0.5)
    # Stability proxy: penalize high parameter count and failed OOS/PIT calibration.
    r["stability_score"] = 1.0 / (1.0 + r["n_params"].fillna(3))
    scores = pd.DataFrame(index=r.index)
    metric_list = ["loglik", "AIC", "BIC", "HQC", "KS", "AD", "CvM", "CDF_RMSE", "CDF_MAE", "quantile_error", "tail_quantile_error", "oos_loglik", "tail_score_raw", "stability_score", "practical_score"]
    for metric in metric_list:
        if metric in r.columns:
            higher = metric in config["ranking"].get("higher_is_better_metrics", [])
            if metric in ["stability_score", "practical_score"]:
                higher = True
            if metric in config["ranking"].get("lower_is_better_metrics", []):
                higher = False
            if per_asset and method != "none" and "asset" in r.columns:
                # Normalize within each asset group, then stitch back together.
                col = pd.Series(index=r.index, dtype=float)
                for _, grp in r.groupby("asset"):
                    col.loc[grp.index] = normalize_scores(grp, metric, higher, method)
                scores[metric + "_score"] = col
            else:
                scores[metric + "_score"] = normalize_scores(r, metric, higher, method)
    fit_cols = [c for c in scores.columns if c.replace("_score", "") in ["loglik", "AIC", "BIC", "HQC", "KS", "AD", "CvM", "CDF_RMSE", "CDF_MAE", "quantile_error"]]
    tail_cols = [c for c in scores.columns if c.replace("_score", "") in ["tail_quantile_error", "tail_score_raw"]]
    oos_cols = [c for c in scores.columns if c.replace("_score", "") in ["oos_loglik"]]
    r["statistical_fit_score"] = scores[fit_cols].mean(axis=1) if fit_cols else 0.5
    r["tail_fit_score"] = scores[tail_cols].mean(axis=1) if tail_cols else 0.5
    r["out_of_sample_score"] = scores[oos_cols].mean(axis=1) if oos_cols else 0.5
    r["stability_robustness_score"] = scores.get("stability_score_score", pd.Series(0.5, index=r.index))
    r["practical_usefulness_score"] = scores.get("practical_score_score", pd.Series(0.5, index=r.index))
    r["final_score"] = (
        weights.get("statistical_fit", 0.25) * r["statistical_fit_score"] +
        weights.get("tail_fit", 0.30) * r["tail_fit_score"] +
        weights.get("out_of_sample", 0.25) * r["out_of_sample_score"] +
        weights.get("stability_robustness", 0.10) * r["stability_robustness_score"] +
        weights.get("practical_usefulness", 0.10) * r["practical_usefulness_score"]
    )
    r["rank"] = r.groupby("asset")["final_score"].rank(ascending=False, method="first")
    return r.sort_values(["asset", "rank"])


def make_plots(asset: str, x: np.ndarray, models: List[FittedModel], oos_rows: List[Dict[str, Any]], tail_df: pd.DataFrame, config: Dict[str, Any], output_dir: str) -> None:
    """Save diagnostic plots for one asset."""
    if not config["output"].get("save_plots", True):
        return
    pcfg = config["output"].get("plots", {})
    formats = config["output"].get("plot_formats", ["png"])
    safe_asset = str(asset).replace("/", "_").replace(" ", "_")
    x = np.asarray(x, dtype=float); x = x[np.isfinite(x)]
    grid = np.linspace(np.nanpercentile(x, 0.1), np.nanpercentile(x, 99.9), 500)
    good_models = [m for m in models if m.success and m.name != "generalized_pareto"]
    if pcfg.get("histogram_fitted_density", True):
        plt.figure(figsize=(10, 6))
        plt.hist(x, bins=80, density=True, alpha=0.35, color="steelblue", label="Empirical")
        for m in good_models[:8]:
            pdf = np.exp(m.logpdf(grid))
            pdf = np.where(np.isfinite(pdf), pdf, np.nan)
            plt.plot(grid, pdf, label=m.name, lw=1.4)
        plt.title(f"{asset}: Histogram and fitted densities")
        plt.legend(fontsize=8); plt.tight_layout()
        save_fig(output_dir, f"{safe_asset}_hist_density", formats)
    if pcfg.get("ecdf_fitted", True):
        plt.figure(figsize=(10, 6))
        xs = np.sort(x); emp = np.arange(1, len(xs) + 1) / (len(xs) + 1)
        plt.plot(xs, emp, label="Empirical", color="black")
        for m in good_models[:8]:
            plt.plot(xs, m.cdf(xs), label=m.name, lw=1.2)
        plt.title(f"{asset}: ECDF vs fitted CDF")
        plt.legend(fontsize=8); plt.tight_layout()
        save_fig(output_dir, f"{safe_asset}_ecdf", formats)
    if pcfg.get("qq", True):
        qs = np.linspace(0.01, 0.99, 99)
        empq = np.quantile(x, qs)
        for m in good_models[:8]:
            plt.figure(figsize=(6, 6))
            fitq = m.ppf(qs)
            plt.scatter(fitq, empq, s=12)
            lo, hi = np.nanmin([fitq, empq]), np.nanmax([fitq, empq])
            plt.plot([lo, hi], [lo, hi], color="red", lw=1)
            plt.title(f"{asset}: Q-Q {m.name}")
            plt.xlabel("Fitted quantile"); plt.ylabel("Empirical quantile"); plt.tight_layout()
            save_fig(output_dir, f"{safe_asset}_qq_{m.name}", formats)
    if pcfg.get("pit_histogram", True):
        for row in oos_rows:
            pits = np.asarray(row.get("pit_values", []), dtype=float)
            if pits.size > 10:
                plt.figure(figsize=(7, 4))
                plt.hist(pits, bins=20, range=(0, 1), color="slateblue", alpha=0.75)
                plt.title(f"{asset}: PIT histogram {row['distribution']}")
                plt.tight_layout(); save_fig(output_dir, f"{safe_asset}_pit_{row['distribution']}", formats)
    if pcfg.get("var_exceedance", True) and not tail_df.empty:
        # Plot first/best distribution at 95% level.
        sub = tail_df[(tail_df["asset"] == asset) & (tail_df["confidence_level"].round(3) == 0.950)]
        if not sub.empty:
            row = sub.iloc[0]
            var = row["VaR"]
            plt.figure(figsize=(11, 4))
            plt.plot(np.arange(len(x)), x, lw=0.8, label="returns")
            plt.axhline(var, color="red", linestyle="--", label=f"VaR 95% {row['distribution']}")
            plt.title(f"{asset}: VaR exceedance chart")
            plt.legend(); plt.tight_layout(); save_fig(output_dir, f"{safe_asset}_var_exceedance", formats)
    if pcfg.get("rolling_vol", True):
        plt.figure(figsize=(11, 4))
        pd.Series(x).rolling(63, min_periods=20).std().plot(color="darkgreen")
        plt.title(f"{asset}: Rolling 63-period volatility")
        plt.tight_layout(); save_fig(output_dir, f"{safe_asset}_rolling_vol", formats)


def save_fig(output_dir: str, stem: str, formats: List[str]) -> None:
    for fmt in formats:
        plt.savefig(os.path.join(output_dir, f"{stem}.{fmt}"), dpi=140)
    plt.close()


def run_study(config: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """Run the complete return distribution study end-to-end."""
    np.random.seed(int(config["output"].get("random_seed", 42)))
    output_dir = ensure_dir(config["output"].get("output_dir", "return_distribution_output"))
    data = load_data(config)
    returns = compute_returns(data, config)
    returns, outlier_flags = preprocess(returns, config)
    min_obs = int(config["preprocessing"].get("minimum_observations", 100))
    enabled = config["distributions"].get("enabled", [])
    all_eda, all_metrics, all_oos, all_tail, all_params, all_boot = [], [], [], [], [], []
    all_jump: List[Dict[str, Any]] = []
    for asset in returns.columns:
        s = returns[asset].dropna().astype(float)
        if len(s) < min_obs:
            print(f"Skipping {asset}: only {len(s)} observations (<{min_obs}).")
            continue
        print(f"Analyzing {asset}: {len(s)} observations")
        x = s.values
        eda = eda_summary(s, asset, config); all_eda.append(eda)
        models: List[FittedModel] = []
        oos_rows: List[Dict[str, Any]] = []
        for name in enabled:
            model = fit_distribution(x, name, config)
            models.append(model)
            met = gof_metrics(x, model, config); met["asset"] = asset; all_metrics.append(met)
            if model.success:
                params = model.params
                if name == "gaussian_mixture":
                    p_row = {"asset": asset, "distribution": name, "weights": model.params.weights_.ravel().tolist(), "means": model.params.means_.ravel().tolist(), "covariances": np.asarray(model.params.covariances_).ravel().tolist()}
                else:
                    p_row = {"asset": asset, "distribution": name}
                    if isinstance(params, tuple):
                        for i, p in enumerate(params):
                            p_row[f"param_{i}"] = p
                    if model.meta:
                        p_row.update({f"meta_{k}": v for k, v in model.meta.items() if isinstance(v, (int, float, str))})
                all_params.append(p_row)
                bt = bootstrap_parameters(x, name, config)
                if not bt.empty:
                    bt["asset"] = asset; all_boot.append(bt)
            oos = oos_validate(x, name, config); oos["asset"] = asset; all_oos.append(oos); oos_rows.append(oos)
            td = tail_risk_backtest(x, model, config)
            if not td.empty:
                td["asset"] = asset; all_tail.append(td)
        # --- Per-asset Merton jump-diffusion estimation (for next-stage MC) ---
        jp = estimate_jump_parameters(x, config)
        if jp is not None:
            jp_row = {"asset": asset}
            jp_row.update(jp)
            all_jump.append(jp_row)
        tail_asset_df = pd.concat(all_tail, ignore_index=True) if all_tail else pd.DataFrame()
        make_plots(asset, x, models, oos_rows, tail_asset_df, config, output_dir)
    eda_df = pd.DataFrame(all_eda)
    metrics_df = pd.DataFrame(all_metrics)
    oos_df = pd.DataFrame(all_oos)
    tail_df = pd.concat(all_tail, ignore_index=True) if all_tail else pd.DataFrame()
    params_df = pd.DataFrame(all_params)
    boot_df = pd.concat(all_boot, ignore_index=True) if all_boot else pd.DataFrame()
    jump_df = pd.DataFrame(all_jump)
    ranking_df = rank_models(metrics_df, oos_df, tail_df, config)
    agg_rank = aggregate_ranking(ranking_df)
    # Long-format parameter table with role, note, and per-asset rank columns,
    # plus Merton jump parameters appended as a 'merton_jump' pseudo-distribution.
    param_long_df = build_param_long(params_df, ranking_df, jump_df)
    param_format = str(config["output"].get("param_format", "both")).lower()
    outputs = {"eda_summary": eda_df, "in_sample_metrics": metrics_df, "oos_validation": oos_df.drop(columns=["pit_values"], errors="ignore"), "tail_backtests": tail_df, "bootstrap_parameters": boot_df, "jump_parameters": jump_df, "ranking_scorecard": ranking_df, "aggregate_ranking": agg_rank}
    # Add parameter tables according to the requested format.
    if param_format in ("wide", "both"):
        outputs["parameter_estimates"] = params_df
    if param_format in ("long", "both"):
        outputs["parameter_estimates_long"] = param_long_df
    if config["output"].get("save_tables", True):
        for name, df in outputs.items():
            if df is not None and not df.empty:
                df.to_csv(os.path.join(output_dir, f"{name}.csv"), index=False)
    manifest = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "output_dir": os.path.abspath(output_dir), "param_format": param_format, "tables": [f"{k}.csv" for k, v in outputs.items() if v is not None and not v.empty]}
    with open(os.path.join(output_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Study complete. Outputs written to: {os.path.abspath(output_dir)}")
    if not agg_rank.empty:
        print("\nAggregate ranking (top rows):")
        print(agg_rank.head(10).to_string(index=False))
    return outputs


def aggregate_ranking(ranking_df: pd.DataFrame) -> pd.DataFrame:
    if ranking_df.empty:
        return pd.DataFrame()
    return ranking_df.groupby("distribution", as_index=False).agg(mean_final_score=("final_score", "mean"), median_rank=("rank", "median"), assets_covered=("asset", "nunique")).sort_values(["mean_final_score", "median_rank"], ascending=[False, True])


def main() -> None:
    parser = argparse.ArgumentParser(description="Empirical stock-return distribution study")
    parser.add_argument("--config", default=None, help="Optional path to a YAML override file. If omitted, the embedded DEFAULT_CONFIG is used (standalone mode).")
    args = parser.parse_args()
    cfg = load_config(args.config)
    run_study(cfg)


if __name__ == "__main__":
    main()
