# Institutional Macro-Regime Detection, Multi-Asset Signal Identification, and Statistical Validation Curriculum

## Installment 13: Part 13 - Institutional Research Pipeline and Production Implementation

**Scope of this installment.** This installment continues the curriculum with **Part 13 only**. It assumes the global assumptions, timestamp conventions, feature engineering framework, return-target definitions, regime-detection concepts, causal-channel framework, signal-scoring framework, validation framework, machine-learning controls, regime-conditioned forecasting framework, portfolio integration framework, derivatives framework, and risk-management framework established in Installments 1 through 12.

**Educational boundary.** This document is for research education, model design, and institutional portfolio-process development. It is not personalized investment advice, a live trading recommendation, or a guarantee of alpha.

---

# Part 13: Institutional Research Pipeline and Production Implementation

## 13.1 Purpose of the Institutional Research Pipeline

A macro-regime and multi-asset signal platform is not only a collection of models. It is a governed research and production system that transforms raw data into timestamped features, forecasts, regime probabilities, conviction scores, portfolio inputs, monitoring reports, and audit trails. The institutional pipeline must answer a simple question every day or month:

$$
\text{Can we reproduce, explain, validate, monitor, and govern every number used in the investment process?}
$$

If the answer is no, then the system is not production-grade, even if the model appears statistically impressive. Production implementation requires repeatability, point-in-time discipline, version control, data lineage, exception handling, validation evidence, monitoring, permissioning, and human oversight.

The core pipeline can be summarized as:

$$
\text{Raw Data} \rightarrow \text{Clean Data} \rightarrow \text{Point-in-Time Features} \rightarrow \text{Models}
\rightarrow \text{Forecasts} \rightarrow \text{Convictions} \rightarrow \text{Portfolio Inputs} \rightarrow \text{Monitoring}.
$$

Each arrow must be versioned and auditable.

## 13.2 Production Design Principles

A production research platform should be designed around the following principles.

| Principle | Meaning | Failure Mode if Ignored |
|---|---|---|
| Point-in-time integrity | Every feature is available at the decision timestamp. | Look-ahead bias and overstated performance. |
| Reproducibility | A historical run can be recreated from data, code, and configuration. | Results cannot be audited or defended. |
| Modularity | Data, features, models, validation, and portfolio layers are separable. | Small changes break the entire pipeline. |
| Versioning | Data, code, models, and outputs carry version IDs. | Unclear which model produced which signal. |
| Observability | Pipeline health, drift, anomalies, and failures are monitored. | Silent data/model failures enter the investment process. |
| Governance | Model changes require review, approval, and documentation. | Uncontrolled model changes and hidden overfitting. |
| Scalability | Architecture can support larger universes and longer histories. | Research prototypes fail under production load. |
| Degradation safety | Failure modes produce safe fallbacks rather than bad trades. | Missing data or model errors become portfolio risk. |

## 13.3 Data Lake Architecture for Point-in-Time Research

The data lake is the foundation of the research platform. It should store immutable raw data, cleaned data, point-in-time macro vintages, market data, corporate actions, futures metadata, options surfaces, benchmark definitions, and derived features. A strong design separates storage layers.

| Layer | Purpose | Example Objects | Mutability |
|---|---|---|---|
| Bronze | Raw vendor snapshots. | API pulls, files, raw tables. | Immutable. |
| Silver | Cleaned and standardized data. | Adjusted prices, normalized macro releases. | Versioned; not overwritten silently. |
| Gold | Model-ready features and targets. | Lagged macro features, forward returns, PIT universes. | Versioned by feature definition. |
| Research outputs | Experiments and validation artifacts. | Forecasts, IC tables, model metrics, reports. | Immutable after run finalization. |
| Production outputs | Approved live signals and portfolio inputs. | Regime probabilities, conviction scores, risk inputs. | Append-only with corrections documented. |

A key rule is that raw data should not be overwritten. Vendor corrections, restatements, and backfills should be stored as new versions so that the research team can distinguish what was known historically from what is known today.

## 13.4 Macro Vintage Storage

Macro data requires special handling because observations are released after reference periods and often revised. A vintage-aware schema should store reference date, release date, vintage date, and ingestion date separately.

A recommended long-format schema is:

| Field | Type | Meaning |
|---|---|---|
| `series_id` | string | Stable macro series identifier. |
| `country` | string | Country or region. |
| `reference_date` | date | Economic period described by the data. |
| `release_timestamp` | timestamp | Official release time. |
| `vintage_timestamp` | timestamp | Timestamp of this value version. |
| `ingestion_timestamp` | timestamp | When the platform received the value. |
| `value` | float | Observed macro value. |
| `unit` | string | Index, percent, diffusion, level, etc. |
| `source` | string | Vendor or official source. |
| `revision_number` | integer | Initial release, first revision, benchmark revision, etc. |
| `quality_flag` | string | Normal, missing, provisional, revised, restated, suspect. |

A point-in-time macro value at decision time $t$ is:

$$
x_{m,q,t}^{PIT}=x_{m,q}^{(v^*)},
\qquad
v^*=\max\{v: \tau^{avail}_{m,q,v}\leq t_{cutoff}\},
$$

where $m$ is the series, $q$ is the reference date, $v$ is the vintage, and $t_{cutoff}$ is the decision cutoff.

## 13.5 Market Data Storage

Market data should store prices, total return indices, yields, curves, spreads, FX rates, futures contracts, option surfaces, volatility indices, and liquidity metrics. The schema must separate economic meaning from vendor field naming.

| Object | Required Fields | Key Controls |
|---|---|---|
| Equity and index data | price, total return, currency, close timestamp. | Corporate actions, dividend treatment, holiday calendars. |
| Bond and rates data | yield, duration, convexity, curve point, source timestamp. | Curve construction, interpolation, stale quote detection. |
| Credit data | spread, yield, duration, rating bucket, index composition. | Spread duration, index changes, liquidity flags. |
| FX data | spot, forward points, base/quote convention, close time. | Currency quotation convention and holiday alignment. |
| Futures data | contract, expiry, settlement, roll rule, collateral rate. | Contract mapping, roll schedule, back-adjustment policy. |
| Options data | underlying, expiry, strike, delta, IV, bid/ask, surface timestamp. | Moneyness convention, stale quotes, arbitrage filters. |
| Volatility data | implied vol index, realized vol, variance swap proxy. | Methodology changes and term alignment. |

A production platform should store both raw vendor identifiers and internal canonical identifiers. This allows the research team to change vendors or map multiple vendors to a common instrument master.

## 13.6 Instrument Master and Asset Universe Management

A point-in-time asset universe is essential for avoiding survivorship bias. The instrument master should store inception dates, delisting dates, benchmark membership, liquidity eligibility, trading restrictions, currency, exchange, contract specifications, and implementation instrument mapping.

The point-in-time universe is:

$$
\mathcal{U}_t=\{i: \mathrm{inception}_i\leq t,\ \mathrm{active}_i(t)=1,\ \mathrm{eligible}_i(t)=1,\ \mathrm{liquidity}_i(t)\geq L_{min}\}.
$$

Eligibility rules should themselves be versioned. A strategy tested today with a revised universe definition should not overwrite the historical universe used in prior validation.

## 13.7 Feature Store Design

A feature store stores model-ready variables with full lineage. A feature should never be just a column name. It should be a versioned object with a definition, transformation, timestamp convention, availability rule, and owner.

A feature record should include:

| Field | Meaning |
|---|---|
| `feature_id` | Stable identifier, such as `macro_us_cpi_3m_ann_z_v2`. |
| `feature_family` | Growth, inflation, credit, liquidity, trend, carry, volatility, etc. |
| `entity_id` | Country, asset, instrument, sector, or strategy identifier. |
| `decision_date` | Timestamp at which the feature is valid. |
| `value` | Feature value. |
| `source_series` | Raw series used. |
| `transformation` | Formula and parameters. |
| `availability_rule` | Vintage, lag, or market close rule. |
| `lookback` | Rolling/expanding window. |
| `scaling_method` | Rolling z-score, expanding z-score, rank, robust score, none. |
| `code_version` | Git commit or package version. |
| `data_version` | Input data snapshot identifier. |
| `quality_flag` | Normal, missing, stale, clipped, imputed, suspect. |

The feature store should support both offline research and production scoring. Offline feature retrieval must reproduce historical values exactly. Production feature retrieval must be fast, observable, and fail-safe.

## 13.8 Target Store and Label Management

Forecast targets should be stored separately from features. This reduces target leakage and makes horizon definitions explicit.

For asset $i$, timestamp $t$, and horizon $h$, a target record may include:

| Field | Meaning |
|---|---|
| `asset_id` | Asset or strategy identifier. |
| `decision_date` | Signal timestamp. |
| `horizon_months` | 1, 3, 12, or custom. |
| `target_type` | Absolute return, excess return, active return, event, quantile, drawdown. |
| `start_date` | First month included in target. |
| `end_date` | Final month included in target. |
| `value` | Realized target. |
| `benchmark_id` | Cash, benchmark, or reference asset if relevant. |
| `currency_basis` | Local, hedged, or unhedged base currency. |
| `return_convention` | Arithmetic cumulative, log cumulative, annualized. |
| `cost_convention` | Gross, net of transaction cost, net of financing, etc. |

A forward target is valid only after the forward window is fully realized:

$$
\mathrm{available}(Y_{i,t,h}) \geq t+h.
$$

The target store should block any training process that attempts to use targets whose realization date is after the training cutoff.

## 13.9 Model Registry

The model registry stores approved and experimental models, their parameters, training data, validation metrics, and governance status. A model record should include:

| Field | Meaning |
|---|---|
| `model_id` | Stable model identifier. |
| `model_type` | Regression, HMM, GMM, BVAR, ML pipeline, ensemble, optimizer. |
| `version` | Semantic version or hash. |
| `owner` | Research owner and approving committee. |
| `training_cutoff` | Final date used for training. |
| `feature_set_id` | Versioned feature set. |
| `target_definition_id` | Versioned target definition. |
| `hyperparameters` | Model configuration. |
| `validation_report_id` | Approved validation package. |
| `status` | Research, watchlist, approved, production, retired. |
| `effective_date` | Date from which model may be used. |
| `retirement_date` | Date model was retired, if applicable. |

Model versioning matters because a forecast is not only a number. It is the output of a specific model, trained on a specific data snapshot, using a specific configuration.

## 13.10 Experiment Tracking

Experiment tracking records research runs. Each experiment should have a run manifest that specifies all inputs, settings, and outputs.

A minimal run manifest is:

```yaml
run_id: 2026-06-06T21-30-00Z_macro_regime_signal_validation
research_owner: multi_asset_research
code_commit: abc123def456
python_environment: conda:macro-research-1.4.2
data_snapshot: data_lake_2026_06_06_vintage_locked
feature_set: macro_cross_asset_features_v3
target_set: forward_returns_t1_t3_t12_v2
model_config: ridge_panel_regression_alpha_10
validation_design: expanding_walk_forward_min_train_120m
horizons_months: [1, 3, 12]
universe: global_multi_asset_liquid_v5
cost_model: futures_fx_etf_costs_v2
outputs:
  forecasts: s3://research-runs/run_id/forecasts.parquet
  metrics: s3://research-runs/run_id/metrics.json
  report: s3://research-runs/run_id/validation_report.html
```

This record allows another researcher to reproduce or audit the run later.

## 13.11 Backtest Audit Trails

A backtest should be treated as a historical simulation with a complete audit trail. Each rebalance date should store:

| Object | Examples |
|---|---|
| Inputs | Features, regime probabilities, forecasts, covariance, constraints. |
| Model versions | Signal model, risk model, cost model, optimizer version. |
| Decisions | Target weights, trades, rejected trades, constraint shadow prices. |
| Realized outcomes | Returns, slippage, costs, drawdowns, risk contributions. |
| Exceptions | Missing data, stale prices, manual overrides, failed constraints. |
| Attribution | Signal contribution, asset contribution, regime contribution. |

A portfolio decision can be represented as:

$$
w_t = \mathcal{A}(\hat\mu_t,\hat\Sigma_t,C_t,\Omega_t),
$$

where $\mathcal{A}$ is the allocation engine, $\hat\mu_t$ is expected return, $\hat\Sigma_t$ is covariance, $C_t$ is the constraint set, and $\Omega_t$ is metadata including costs, liquidity, leverage, and risk budgets. The audit trail must store all four components.

## 13.12 Validation Reports and Model Governance

Validation reports should be standardized. A production approval process should require a frozen signal definition, a data lineage report, an out-of-sample validation package, cost analysis, risk analysis, failure-mode documentation, and a monitoring plan.

| Governance Stage | Required Evidence | Allowed Use |
|---|---|---|
| Research candidate | Economic rationale and preliminary in-sample diagnostics. | Research only. |
| Watchlist | Point-in-time construction and early walk-forward evidence. | Monitoring dashboard. |
| Low-weight approved | Robust evidence but limited breadth or capacity. | Small composite contribution. |
| Production approved | Full validation, risk review, monitoring, and owner sign-off. | Investment process input. |
| Retired | Signal decay, data problem, or failed governance review. | Archived only. |

A model change should trigger revalidation if it affects features, targets, universe, scaling, training window, objective function, hyperparameters, regime definitions, forecast mapping, or portfolio construction.

## 13.13 Production Monitoring

Production monitoring detects whether live inputs, forecasts, and outputs remain within expected bounds. Monitoring should cover data, features, models, forecasts, portfolios, and realized performance.

| Monitoring Layer | Diagnostic | Example Alert |
|---|---|---|
| Data | Missing values, stale values, outliers, vendor delays. | CPI release not ingested by cutoff. |
| Features | Distribution drift, z-score extremes, rank instability. | Credit stress z-score above historical 99th percentile. |
| Regimes | Probability jumps, excessive switching, entropy. | HMM stress probability jumps from 10% to 80%. |
| Forecasts | Forecast magnitude, dispersion, sign changes. | Expected return exceeds historical forecast cap. |
| Convictions | Concentration, turnover, regime reliability. | Conviction concentrated in one asset class. |
| Portfolio | Risk, constraints, leverage, margin, drawdown. | Active risk exceeds limit. |
| Performance | IC decay, forecast error, calibration. | Rolling 24-month IC below monitoring threshold. |

A useful model-drift statistic compares current feature distribution to historical training distribution. For feature $m$:

$$
D_{m,t}=\frac{|x_{m,t}-\mu_{m,train}|}{\sigma_{m,train}},
$$

where $\mu_{m,train}$ and $\sigma_{m,train}$ are training-period statistics. Large $D_{m,t}$ indicates the model is seeing conditions far from the training distribution.

## 13.14 Forecast Decay Monitoring

A production system should monitor whether forecasts remain useful after approval. For a rolling window $W$, the rolling IC is:

$$
IC_{t,W}=\mathrm{corr}(\hat Y_{s,h},Y_{s,h})_{s=t-W+1}^{t}.
$$

A signal decay alert may be triggered if:

$$
IC_{t,W}<IC_{min}
$$

for several consecutive windows, or if live forecast errors exceed a threshold:

$$
|e_{t,h}|=|Y_{t,h}-\hat Y_{t,h}|>q_{0.95}(|e_{train,h}|).
$$

Forecast decay does not automatically mean a model should be retired. It may reflect a regime where the signal is expected to underperform. The monitoring report should separate expected regime-conditional weakness from unexpected model failure.

## 13.15 Alerting and Exception Handling

Production failures should trigger defined actions. Alerts should be severity-ranked.

| Severity | Example | Action |
|---|---|---|
| Info | Feature within normal range but changed materially. | Log and include in dashboard. |
| Warning | Missing noncritical feature; fallback available. | Use fallback, notify owner. |
| High | Key macro vintage missing or stale. | Freeze affected signal or use prior value with flag. |
| Critical | Model output invalid, optimizer infeasible, or data leakage detected. | Block production release and escalate. |

A safe fallback policy is essential. Examples include:

1. Use previous approved signal if current run fails and data is not stale beyond tolerance.
2. Set affected conviction to neutral if required inputs are missing.
3. Use unconditional covariance if regime-conditioned covariance is unavailable.
4. Block trading if optimizer infeasibility reflects inconsistent constraints.
5. Require human approval for manual overrides.

## 13.16 Batch Versus Real-Time Architecture

Monthly macro-regime systems are often batch-oriented, but some components may update daily or intraday. Architecture should reflect decision frequency.

| Architecture | Best Use | Advantages | Risks |
|---|---|---|---|
| Monthly batch | Strategic/tactical allocation using monthly data. | Simple, auditable, lower operational burden. | Slow reaction to market stress. |
| Daily batch | Market-implied features, risk monitoring, volatility regimes. | More timely risk control. | More noise and turnover. |
| Event-driven | Macro releases, policy decisions, shock updates. | Timely response to surprises. | Requires precise timestamps and execution policy. |
| Intraday | Options, futures, volatility risk, execution. | Fast risk response. | High complexity and microstructure noise. |

A common institutional design is hybrid: macro features update monthly or on release dates, market-implied stress features update daily, and portfolio changes are constrained by the investment mandate's rebalance schedule.

## 13.17 Scaling to Global Multi-Asset Universes

Scaling introduces data, compute, and governance challenges. A global multi-asset universe may include thousands of series, multiple currencies, futures rolls, options surfaces, macro releases across countries, benchmark changes, and historical revisions.

Scaling requirements include:

| Requirement | Production Approach |
|---|---|
| Large data joins | Use DuckDB, Spark, Polars, or columnar storage such as Parquet. |
| Feature computation | Partition by date, country, asset class, and feature family. |
| Model training | Use scheduled jobs with reproducible containers. |
| Cross-sectional ranking | Use point-in-time universe partitions. |
| Options surfaces | Store compressed grids and quality flags. |
| Futures rolls | Version roll schedules and contract mappings. |
| Monitoring | Aggregate dashboards by asset class, region, and signal family. |
| Access control | Permission data by license, role, and jurisdiction. |

A research prototype may use pandas. A production implementation may use Polars, DuckDB, Spark, dbt, Airflow, Dagster, Kubernetes, object storage, and containerized model services.

## 13.18 Recommended Technology Stack

The following is an illustrative architecture, not a mandate.

| Layer | Research Prototype | Institutional Production |
|---|---|---|
| Storage | CSV, local Parquet, SQLite. | S3/ADLS/GCS, Parquet, Delta/Iceberg, warehouse. |
| Compute | pandas, NumPy, statsmodels, sklearn. | Polars, DuckDB, Spark, Ray, numba, C++ where needed. |
| Orchestration | Scripts, notebooks. | Airflow, Dagster, Prefect, dbt. |
| Feature store | Parquet tables and metadata YAML. | Feast/custom feature store with lineage. |
| Model registry | MLflow local tracking. | MLflow, internal registry, approval workflow. |
| Validation | Jupyter reports. | Scheduled validation reports and CI checks. |
| Monitoring | Static charts. | Dashboards, alerting, SLA checks. |
| Deployment | Manual batch runs. | Containerized jobs with controlled promotion. |
| Governance | README and notebooks. | Model-risk management, audit logs, sign-offs. |

## 13.19 Python: Production-Style Data Quality Checks

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DataQualityRule:
    name: str
    max_missing_ratio: float = 0.05
    max_abs_zscore: float = 8.0
    stale_limit: int = 3


def validate_time_index(df: pd.DataFrame, name: str) -> list[str]:
    issues: list[str] = []
    if not isinstance(df.index, pd.DatetimeIndex):
        issues.append(f"{name}: index is not DatetimeIndex")
    elif not df.index.is_monotonic_increasing:
        issues.append(f"{name}: index is not sorted")
    if df.index.has_duplicates:
        issues.append(f"{name}: duplicate timestamps detected")
    return issues


def data_quality_report(df: pd.DataFrame, rule: DataQualityRule) -> pd.DataFrame:
    """Generate simple data-quality diagnostics by column."""
    issues = validate_time_index(df, rule.name)
    if issues:
        raise ValueError("; ".join(issues))

    rows = []
    for col in df.columns:
        x = df[col].replace([np.inf, -np.inf], np.nan).astype(float)
        missing_ratio = float(x.isna().mean())
        dx = x.diff().abs()
        stale_runs = (dx.fillna(0.0) == 0.0).astype(int)
        max_stale = int(stale_runs.groupby((stale_runs != stale_runs.shift()).cumsum()).sum().max())
        hist_mean = x.expanding(36).mean().shift(1)
        hist_std = x.expanding(36).std(ddof=1).shift(1)
        z = ((x - hist_mean) / hist_std.replace(0.0, np.nan)).abs()
        max_z = float(z.max(skipna=True)) if z.notna().any() else np.nan
        rows.append({
            "series": col,
            "missing_ratio": missing_ratio,
            "max_stale_run": max_stale,
            "max_abs_historical_zscore": max_z,
            "missing_breach": missing_ratio > rule.max_missing_ratio,
            "stale_breach": max_stale > rule.stale_limit,
            "outlier_breach": bool(pd.notna(max_z) and max_z > rule.max_abs_zscore),
        })
    return pd.DataFrame(rows).set_index("series")
```

## 13.20 Python: Feature Definition Registry

```python
from dataclasses import asdict, dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class FeatureDefinition:
    feature_id: str
    source_series: list[str]
    transformation: str
    availability_rule: str
    lookback_months: int | None
    scaling_method: str
    owner: str
    version: str
    description: str


def save_feature_registry(features: list[FeatureDefinition], path: str | Path) -> None:
    path = Path(path)
    payload = [asdict(f) for f in features]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_feature_registry(path: str | Path) -> list[FeatureDefinition]:
    path = Path(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [FeatureDefinition(**item) for item in payload]


registry = [
    FeatureDefinition(
        feature_id="us_credit_spread_3m_impulse_z_v1",
        source_series=["us_hy_oas"],
        transformation="x_t - x_t_minus_3, rolling z-score using trailing 60 months",
        availability_rule="market close available at decision timestamp",
        lookback_months=3,
        scaling_method="rolling_zscore_60m_shifted",
        owner="multi_asset_research",
        version="1.0.0",
        description="Credit stress impulse for downside-risk and regime-transition monitoring.",
    )
]

save_feature_registry(registry, "/mnt/data/example_feature_registry.json")
```

## 13.21 Python: Run Manifest and Reproducibility Hash

```python
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def stable_json_hash(payload: dict[str, Any]) -> str:
    """Create a deterministic hash for a JSON-serializable payload."""
    encoded = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def create_run_manifest(
    *,
    run_name: str,
    code_commit: str,
    data_snapshot: str,
    feature_set: str,
    model_config: dict[str, Any],
    validation_config: dict[str, Any],
    output_paths: dict[str, str],
) -> dict[str, Any]:
    manifest = {
        "run_name": run_name,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "code_commit": code_commit,
        "data_snapshot": data_snapshot,
        "feature_set": feature_set,
        "model_config": model_config,
        "validation_config": validation_config,
        "output_paths": output_paths,
    }
    manifest["run_hash"] = stable_json_hash(manifest)
    return manifest


manifest = create_run_manifest(
    run_name="part13_demo_macro_signal_run",
    code_commit="abc123",
    data_snapshot="vintage_locked_2026_06_06",
    feature_set="macro_features_v3",
    model_config={"model": "ridge", "alpha": 10.0},
    validation_config={"method": "expanding_walk_forward", "min_train_months": 120},
    output_paths={"forecasts": "forecasts.parquet", "metrics": "metrics.json"},
)

Path("/mnt/data/example_run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
```

## 13.22 Python: Feature Drift Monitoring

```python
import numpy as np
import pandas as pd


def feature_drift_report(
    live_features: pd.Series,
    training_mean: pd.Series,
    training_std: pd.Series,
    warning_z: float = 3.0,
    critical_z: float = 5.0,
) -> pd.DataFrame:
    """Compare live feature values against training distribution."""
    df = pd.concat(
        [
            live_features.rename("live"),
            training_mean.rename("train_mean"),
            training_std.rename("train_std"),
        ],
        axis=1,
    ).replace([np.inf, -np.inf], np.nan)
    df["drift_z"] = (df["live"] - df["train_mean"]).abs() / df["train_std"].replace(0.0, np.nan)
    df["severity"] = "normal"
    df.loc[df["drift_z"] >= warning_z, "severity"] = "warning"
    df.loc[df["drift_z"] >= critical_z, "severity"] = "critical"
    return df.sort_values("drift_z", ascending=False)
```

## 13.23 Python: Monitoring Live Signal Decay

```python
from scipy.stats import spearmanr


def rolling_information_coefficient(
    forecast: pd.Series,
    realized: pd.Series,
    window: int = 24,
    method: str = "spearman",
) -> pd.Series:
    """Compute rolling IC between forecasts and realized outcomes."""
    df = pd.concat([forecast.rename("forecast"), realized.rename("realized")], axis=1)
    df = df.replace([np.inf, -np.inf], np.nan).dropna().astype(float)
    values = []
    idx = []
    for end in range(window, len(df) + 1):
        block = df.iloc[end - window:end]
        if method == "spearman":
            rho = spearmanr(block["forecast"], block["realized"])[0]
        elif method == "pearson":
            rho = block["forecast"].corr(block["realized"])
        else:
            raise ValueError("method must be 'spearman' or 'pearson'")
        values.append(float(rho))
        idx.append(block.index[-1])
    return pd.Series(values, index=idx, name=f"rolling_{window}m_ic")


def signal_decay_alert(ic_series: pd.Series, threshold: float = 0.0, consecutive: int = 3) -> bool:
    """Return True if rolling IC remains below threshold for consecutive observations."""
    s = ic_series.dropna()
    if len(s) < consecutive:
        return False
    return bool((s.tail(consecutive) < threshold).all())
```

## 13.24 Python: Simple Pipeline Orchestration Skeleton

```python
from dataclasses import dataclass
from typing import Callable


@dataclass
class PipelineStep:
    name: str
    function: Callable
    critical: bool = True


class ResearchPipeline:
    """Minimal pipeline runner with failure handling."""

    def __init__(self, steps: list[PipelineStep]):
        self.steps = steps
        self.results = {}
        self.errors = {}

    def run(self, context: dict):
        for step in self.steps:
            try:
                self.results[step.name] = step.function(context, self.results)
            except Exception as exc:
                self.errors[step.name] = str(exc)
                if step.critical:
                    raise RuntimeError(f"Critical pipeline step failed: {step.name}") from exc
        return {"results": self.results, "errors": self.errors}
```

This skeleton is not a substitute for Airflow, Dagster, Prefect, or enterprise scheduling, but it shows the basic idea: each step should have explicit inputs, outputs, and failure behavior.

## 13.25 Production Readiness Checklist

| Area | Requirement | Status |
|---|---|---|
| Data lineage | Raw, clean, feature, target, and output lineage documented. | Required. |
| Point-in-time integrity | Release dates, vintages, and availability rules implemented. | Required. |
| Universe management | Point-in-time investable universe stored and versioned. | Required. |
| Feature definitions | Feature IDs, transformations, lags, and scaling rules registered. | Required. |
| Target definitions | Horizons, compounding, benchmark, and currency basis registered. | Required. |
| Model registry | Model versions, owners, status, validation reports stored. | Required. |
| Experiment tracking | Run manifests and output hashes generated. | Required. |
| Validation | Walk-forward, robust inference, stability, and cost analysis complete. | Required. |
| Monitoring | Data, feature, model, forecast, conviction, and portfolio alerts active. | Required. |
| Fallback policy | Missing data, stale data, model failure, and optimizer failure responses defined. | Required. |
| Access control | Vendor license and sensitive data permissions enforced. | Required. |
| Documentation | User guide, methodology note, model card, and governance record complete. | Required. |
| Deployment | Container or environment lockfile available. | Required. |
| Review cycle | Periodic model review schedule defined. | Required. |

## 13.26 Common Production Failure Modes

| Failure Mode | Description | Control |
|---|---|---|
| Silent data revision | Vendor revises history without notice. | Immutable snapshots and data-diff alerts. |
| Macro timestamp error | Reference month treated as release month. | Release-calendar joins and vintage checks. |
| Full-sample preprocessing | Scaling or PCA trained on future data. | Pipeline tests that fit transformations inside training windows. |
| Model drift | Live features outside training distribution. | Drift dashboard and uncertainty scaling. |
| Signal decay | Live IC falls below expected range. | Rolling IC monitoring and review trigger. |
| Optimizer infeasibility | Constraints conflict under new risk estimates. | Pre-trade feasibility checks and fallback weights. |
| Cost-model underestimation | Net performance worse than expected. | Live cost monitoring and slippage calibration. |
| Label switching | Regime labels change across refits. | Profile-based label alignment. |
| Manual override opacity | Human changes not documented. | Override ticket, reason, approver, expiry date. |
| Environment drift | Different Python or package versions change outputs. | Locked environments and CI reproducibility tests. |

## 13.27 Documentation Set for Institutional Use

A production-ready macro-regime platform should maintain the following documents.

| Document | Purpose |
|---|---|
| Methodology manual | Explains theory, features, models, validation, and portfolio integration. |
| Data dictionary | Defines all raw, clean, feature, target, and output fields. |
| Feature catalog | Lists feature definitions, owners, versions, and status. |
| Model cards | Summarize each model's objective, inputs, outputs, validation, limits, and monitoring. |
| Validation report | Provides evidence stack for approval. |
| Runbook | Explains production schedule, failure handling, alerts, and escalation. |
| Change log | Records changes to data, features, models, costs, constraints, and portfolio mapping. |
| Governance minutes | Records approvals, exceptions, overrides, and retirement decisions. |

## 13.28 Part 13 Summary

Part 13 developed the institutional research pipeline and production implementation layer. The main lessons are:

1. Production-grade macro research requires more than models; it requires data lineage, point-in-time integrity, reproducibility, governance, and monitoring.
2. Raw data should be immutable, and cleaned data, features, targets, models, and outputs should be versioned.
3. Macro vintage storage must separate reference dates, release timestamps, vintage timestamps, ingestion timestamps, and decision timestamps.
4. Feature stores should record definitions, transformations, scaling rules, availability rules, data versions, code versions, owners, and quality flags.
5. Target stores should separate forward labels from features and enforce horizon availability.
6. Model registries and experiment tracking are essential for reproducibility, approval, and retirement decisions.
7. Backtests require full audit trails of inputs, models, forecasts, constraints, trades, costs, outcomes, and exceptions.
8. Production monitoring should cover data anomalies, feature drift, regime probability jumps, forecast instability, signal decay, concentration, constraints, and realized performance.
9. Safe fallbacks are required for missing data, stale data, invalid model outputs, optimizer infeasibility, and critical production failures.
10. A hybrid architecture can combine monthly macro batch processing with daily market-implied risk monitoring and event-driven macro release handling.
11. Scaling to global multi-asset universes requires canonical identifiers, partitioned data, feature registries, model registries, orchestration, monitoring, and access controls.
12. A production readiness checklist should be completed before any model becomes an approved investment-process input.

---

# Stop Point

This installment completes:

1. **Part 13: Institutional Research Pipeline and Production Implementation.**

Continue next with **Part 14: Case Studies**.
