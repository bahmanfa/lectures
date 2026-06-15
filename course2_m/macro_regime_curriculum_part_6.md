# Institutional Macro-Regime Detection, Multi-Asset Signal Identification, and Statistical Validation Curriculum

## Installment 6: Part 6 - Signal Identification, Ranking, and Conviction Scoring

**Scope of this installment.** This installment continues the curriculum with **Part 6 only**. It assumes the global assumptions, timestamp conventions, feature engineering framework, return-target definitions, regime-detection concepts, and causal-channel framework established in Installments 1 through 5.

**Educational boundary.** This document is for research education, model design, and institutional portfolio-process development. It is not personalized investment advice, a live trading recommendation, or a guarantee of alpha.

---

# Part 6: Signal Identification, Ranking, and Conviction Scoring

## 6.1 Purpose of Signal Identification

Signal identification is the disciplined process of converting economically motivated, point-in-time features into validated ranking, forecasting, and conviction inputs. In an institutional macro and multi-asset setting, signal identification is not the same as searching for the highest backtest Sharpe ratio. It is the process of determining whether a feature has enough economic rationale, statistical reliability, horizon specificity, implementation feasibility, and robustness to become part of a research library.

Let $x_{m,t}$ denote a raw or transformed feature and let $s_{i,t,h}^{(m)}$ denote a signal score for asset $i$ at decision timestamp $t$ for horizon $h$. A generic signal construction is:

$$
s_{i,t,h}^{(m)}=f_{m,h}(x_{m,t}, a_{i,t}, \mathcal{F}_t),
$$

where $f_{m,h}(\cdot)$ is a pre-specified transformation, $a_{i,t}$ is asset-specific information such as duration, beta, sector exposure, FX exposure, carry, volatility, or liquidity, and $\mathcal{F}_t$ is the information set available at time $t$.

A valid signal must answer five questions:

1. **Economic mechanism.** Why should the signal forecast the target?
2. **Expected direction.** Should a higher score imply higher or lower expected return, probability of outperformance, or downside risk?
3. **Relevant horizon.** Is the signal expected to work at $t+1$, $t+3$, $t+12$, or only under specific regimes?
4. **Asset universe.** Which assets should be ranked or forecast by this signal?
5. **Validation standard.** What evidence is required before using the signal in a conviction process?

## 6.2 Feature, Signal, Forecast, and Conviction

The distinction between feature, signal, forecast, and conviction is central.

| Object | Definition | Example | Validation Question |
|---|---|---|---|
| Feature | A transformed observable variable. | 3-month change in credit spread. | Is it point-in-time and economically meaningful? |
| Signal | A feature with expected direction, target, horizon, and universe. | Credit-spread widening predicts higher equity downside risk over $t+3$. | Does it rank or forecast outcomes robustly? |
| Forecast | Model output for a return, probability, risk, or quantile target. | Expected $t+3$ excess return of credit. | Is it accurate, calibrated, and stable out of sample? |
| Conviction | Portfolio-aware belief combining forecast strength and uncertainty. | High negative conviction on risky credit. | Is it strong enough after uncertainty, costs, and constraints? |

A feature becomes a signal only after the research team specifies the hypothesis before testing. A signal becomes a forecast only after it is mapped into a quantitative target. A forecast becomes a conviction only after accounting for uncertainty, robustness, regime confidence, risk, liquidity, and implementation frictions.

## 6.3 Signal Specification Template

Every signal should have a written specification. This reduces narrative overfitting and allows governance review.

| Field | Required Content |
|---|---|
| Signal name | Stable identifier, such as `credit_impulse_equity_downside_t3`. |
| Feature inputs | Point-in-time variables, transformations, lags, and scaling. |
| Economic rationale | Channel linking the signal to asset outcomes. |
| Target | Absolute return, excess return, active return, probability, quantile, or risk measure. |
| Horizon | $t+1$, $t+3$, $t+12$, or custom horizon. |
| Universe | Assets, countries, sectors, FX pairs, futures, or strategies. |
| Expected direction | Whether higher scores imply higher expected return or higher risk. |
| Ranking rule | Cross-sectional, time-series, or hybrid ranking method. |
| Validation metrics | IC, rank IC, hit rate, spread, calibration, drawdown, turnover. |
| Failure modes | Regimes or market conditions where the signal should weaken or reverse. |
| Implementation notes | Costs, capacity, liquidity, leverage, roll, margin, or option path dependency. |
| Governance status | Research, approved, production, retired, or monitor-only. |

## 6.4 Economic Rationale Before Statistical Testing

A signal should first be justified through a causal or structural channel. The process is:

$$
\text{Macro or market condition}
\rightarrow \text{transmission channel}
\rightarrow \text{asset exposure}
\rightarrow \text{forecastable outcome}.
$$

For example:

$$
\text{Credit spread widening}
\rightarrow \text{tighter financing and lower risk appetite}
\rightarrow \text{equity and credit downside sensitivity}
\rightarrow \Pr(R_{i,t,3}<0)\uparrow.
$$

The statistical test then evaluates whether the data support the pre-specified hypothesis. If the researcher first tests thousands of features and then writes a story for the best one, the research process has data-mining risk even if the story sounds plausible.

## 6.5 Direction, Orientation, and Monotonicity

A signal score should be oriented so that larger values have a consistent interpretation. For return-seeking signals, a common convention is:

$$
s_{i,t,h}>0 \quad \Rightarrow \quad \text{higher expected return or stronger positive conviction}.
$$

For risk signals, a different convention may be used:

$$
q_{i,t,h}>0 \quad \Rightarrow \quad \text{higher expected downside risk}.
$$

If the raw feature has the opposite interpretation, multiply it by $-1$:

$$
s_{i,t,h}=o_m z_{i,t}^{(m)}, \qquad o_m\in\{-1,+1\},
$$

where $z_{i,t}^{(m)}$ is the standardized feature and $o_m$ is the orientation sign.

### 6.5.1 Monotonicity

A signal is monotonic if higher signal buckets are associated with systematically better outcomes. Let $B_q$ be bucket $q$ of the signal distribution. A monotonic return relationship satisfies approximately:

$$
\mathbb{E}[Y_{i,t,h}\mid s_{i,t}\in B_1]
\leq
\mathbb{E}[Y_{i,t,h}\mid s_{i,t}\in B_2]
\leq \cdots \leq
\mathbb{E}[Y_{i,t,h}\mid s_{i,t}\in B_Q],
$$

where $Y_{i,t,h}$ is the forward target and buckets are ordered from low to high signal. Monotonicity is not required in every month, but it is a useful stability diagnostic.

## 6.6 Horizon Specificity and Signal Decay

Signals can decay at different speeds. A short-term volatility signal may matter over $t+1$ but not $t+12$. A valuation signal may matter over $t+12$ but not $t+1$.

The horizon-specific signal efficacy can be written as:

$$
\rho_h=\mathrm{corr}(s_{i,t},Y_{i,t,h}),
\qquad h\in\{1,3,12\}.
$$

Signal decay is the pattern of $\rho_h$ across horizons. A simple decay ratio is:

$$
\mathrm{DecayRatio}_{h_2/h_1}=\frac{|\rho_{h_2}|}{|\rho_{h_1}|},
$$

where $h_2>h_1$. If the ratio is much less than one, the signal may be short-lived. If it rises with horizon, the signal may be slow-moving or valuation-like.

| Signal Type | Expected Stronger Horizon | Reason |
|---|---:|---|
| Macro surprise | $t+1$ | Release shocks are rapidly priced. |
| Credit impulse | $t+1$ to $t+3$ | Stress transmission occurs over months. |
| Trend and momentum | $t+1$ to $t+12$ | Persistence can exist but reversals matter. |
| Carry | $t+3$ to $t+12$ | Carry accrues over time but has crash risk. |
| Valuation | $t+12$ and longer | Mean reversion is slow. |
| Liquidity stress | $t+1$ to $t+3$ | Deleveraging can be abrupt. |
| Yield-curve inversion | $t+6$ to $t+12$ | Macro cycle lags are long and variable. |

## 6.7 Time-Series and Cross-Sectional Signals

A time-series signal evaluates one asset relative to its own history:

$$
s_{i,t}^{TS}=\frac{x_{i,t}-\mu_{i,t,W}}{\sigma_{i,t,W}},
$$

where $\mu_{i,t,W}$ and $\sigma_{i,t,W}$ are historical-only rolling statistics.

A cross-sectional signal evaluates an asset relative to other assets at the same timestamp:

$$
s_{i,t}^{CS}=\frac{\mathrm{rank}_t(x_{i,t})-1}{N_t-1},
$$

where $N_t$ is the point-in-time number of tradable assets. Cross-sectional ranks must only use assets in $\mathcal{U}_t$.

A hybrid signal can combine both:

$$
s_{i,t}^{Hybrid}=\omega s_{i,t}^{TS}+(1-\omega)s_{i,t}^{CS},
\qquad 0\leq\omega\leq 1.
$$

Time-series signals are useful for asset timing. Cross-sectional signals are useful for relative allocation. Hybrid signals are common in multi-asset ranking engines.

## 6.8 Information Coefficient

The information coefficient, or IC, measures the relationship between a signal and future outcomes. For a time-series signal on one asset:

$$
IC_{i,h}=\mathrm{corr}(s_{i,t},Y_{i,t,h})_{t=1}^{T},
$$

where $s_{i,t}$ is the signal and $Y_{i,t,h}$ is the forward target. For a cross-sectional signal at date $t$:

$$
IC_{t,h}=\mathrm{corr}(s_{i,t},Y_{i,t,h})_{i\in\mathcal{U}_t}.
$$

The average cross-sectional IC is:

$$
\overline{IC}_{h}=\frac{1}{T}\sum_{t=1}^{T}IC_{t,h}.
$$

The IC is scale-free and useful for ranking signals. However, an IC can be statistically significant but economically weak if turnover, costs, capacity, or risk concentration eliminate implementation value.

## 6.9 Rank Information Coefficient

The rank information coefficient uses rank correlation, typically Spearman correlation:

$$
RIC_{t,h}=\mathrm{corr}_{Spearman}(s_{i,t},Y_{i,t,h})_{i\in\mathcal{U}_t}.
$$

Rank IC is often more robust than Pearson IC because it is less sensitive to outliers and nonlinear monotonic transformations. It is particularly useful for cross-sectional asset ranking, country selection, sector rotation, commodity futures ranking, and FX carry or value signals.

A rank IC time series should be evaluated for:

1. Average level.
2. Stability through time.
3. Drawdowns in cumulative IC.
4. Regime dependence.
5. Sensitivity to outliers and universe changes.
6. Decay across $t+1$, $t+3$, and $t+12$.

## 6.10 Hit Rate, Payoff Ratio, and Conditional Spread

### 6.10.1 Hit Rate

For a directional forecast $\hat y_{i,t,h}$ and realized target $Y_{i,t,h}$, the hit indicator is:

$$
H_{i,t,h}=\mathbf{1}\{\mathrm{sign}(\hat y_{i,t,h})=\mathrm{sign}(Y_{i,t,h})\}.
$$

The hit rate is:

$$
\mathrm{HitRate}_{h}=\frac{1}{N}\sum_{i,t}H_{i,t,h}.
$$

Hit rate is intuitive but incomplete. A signal can have a hit rate below 50% and still be valuable if winners are much larger than losers. Conversely, a high hit rate can hide severe left-tail losses.

### 6.10.2 Payoff Ratio

The payoff ratio is:

$$
\mathrm{PayoffRatio}_{h}
=
\frac{\mathbb{E}[Y_{i,t,h}\mid \hat y_{i,t,h}>0, Y_{i,t,h}>0]}
{|\mathbb{E}[Y_{i,t,h}\mid \hat y_{i,t,h}>0, Y_{i,t,h}<0]|}.
$$

This measures average gain relative to average loss among positive forecasts. A robust signal should be evaluated using both hit rate and payoff ratio.

### 6.10.3 Conditional Return Spread

For a cross-sectional signal, sort assets into top and bottom quantiles. The conditional spread is:

$$
\mathrm{Spread}_{t,h}=\frac{1}{|Q^{Top}_t|}\sum_{i\in Q^{Top}_t}Y_{i,t,h}
-
\frac{1}{|Q^{Bottom}_t|}\sum_{i\in Q^{Bottom}_t}Y_{i,t,h}.
$$

The average spread is:

$$
\overline{\mathrm{Spread}}_{h}=\frac{1}{T}\sum_{t=1}^{T}\mathrm{Spread}_{t,h}.
$$

This is closer to an implementable long-short or overweight-underweight portfolio than IC, but it requires turnover, liquidity, financing, shorting, leverage, and transaction-cost assumptions before investment usefulness can be claimed.

## 6.11 Signal Stability Diagnostics

A signal should be stable across time, regimes, geographies, asset classes, and reasonable implementation choices.

| Diagnostic | Definition | Purpose |
|---|---|---|
| Rolling IC | IC estimated over rolling windows. | Detect signal decay. |
| Cumulative IC | Cumulative sum of IC values. | Visualize persistence and drawdowns. |
| Subperiod IC | IC by decade or cycle. | Detect structural breaks. |
| Regime IC | IC conditional on regime. | Identify state dependence. |
| Asset-group IC | IC by region, sector, or asset class. | Test breadth. |
| Horizon IC | IC for $t+1$, $t+3$, $t+12$. | Measure decay. |
| Quantile monotonicity | Bucket average returns. | Check ranking shape. |
| Turnover sensitivity | Signal changes through time. | Estimate cost vulnerability. |
| Outlier sensitivity | IC after winsorization or robust ranks. | Check tail dependence. |

A signal with one excellent subperiod and weak performance elsewhere should be treated as a research candidate, not a production input.

## 6.12 Signal Orthogonalization and Redundancy Analysis

Signals often overlap. Growth momentum, credit spreads, equity momentum, and volatility may all reflect the same risk-appetite cycle. Combining redundant signals can create false confidence.

Let $s_t^{new}$ be a candidate signal and let $S_t^{existing}$ be a matrix of existing signals. Orthogonalization estimates:

$$
s_t^{new}=\alpha+S_t^{existing}\gamma+u_t.
$$

The residual is:

$$
s_t^{\perp}=u_t=s_t^{new}-\hat\alpha-S_t^{existing}\hat\gamma.
$$

The incremental IC is then:

$$
IC_h^{\perp}=\mathrm{corr}(s_t^{\perp},Y_{t,h}).
$$

If $IC_h^{\perp}$ is near zero, the new signal may not add incremental information. Orthogonalization should be performed within historical training windows in a realistic validation process. Full-sample orthogonalization is a leakage risk.

### 6.12.1 Redundancy Metrics

| Metric | Formula or Concept | Interpretation |
|---|---|---|
| Signal correlation | $\rho(s^a,s^b)$ | High correlation indicates overlap. |
| Partial correlation | Correlation after controlling for other signals. | Measures incremental relation. |
| Incremental IC | IC of orthogonalized residual. | Tests incremental predictive content. |
| Variance inflation factor | $1/(1-R_m^2)$ | Detects multicollinearity. |
| Cluster grouping | Group correlated signals. | Avoids double counting. |
| PCA loading | Factor contribution. | Identifies common latent drivers. |

## 6.13 Combining Signals

Signal combination converts several imperfect signals into a composite score. Let $s_{i,t}^{(m)}$ be signal $m$ for asset $i$ at time $t$. A composite score is:

$$
S_{i,t}=\sum_{m=1}^{M}w_{m,t}s_{i,t}^{(m)},
$$

where $w_{m,t}$ are signal weights. The weights can be equal, risk-adjusted, information-ratio-based, Bayesian, regularized, or learned by an ensemble model.

### 6.13.1 Equal-Weight Combination

The simplest composite is:

$$
S_{i,t}^{EW}=\frac{1}{M}\sum_{m=1}^{M}s_{i,t}^{(m)}.
$$

Equal weighting is often a strong baseline because optimized weights are unstable in small monthly samples.

### 6.13.2 Information-Ratio Weights

Let $IR_m$ be the historical information ratio of signal $m$ estimated in a training window. A simple weight is:

$$
w_m=\frac{\max(IR_m,0)}{\sum_{j=1}^{M}\max(IR_j,0)}.
$$

This rewards historically useful signals while excluding negative signals. However, if $IR_m$ is estimated with error, this approach can overfit. Shrinkage toward equal weights is often safer:

$$
w_m^{shrunk}=\lambda\frac{1}{M}+(1-\lambda)w_m^{IR},
\qquad 0\leq\lambda\leq 1.
$$

### 6.13.3 Bayesian Model Averaging

Bayesian model averaging combines forecasts from models $\mathcal{M}_1,\ldots,\mathcal{M}_M$:

$$
\hat y_{i,t,h}^{BMA}=\sum_{m=1}^{M}p(\mathcal{M}_m\mid\mathcal{D}_t)\hat y_{i,t,h}^{(m)},
$$

where $p(\mathcal{M}_m\mid\mathcal{D}_t)$ is the posterior model probability given historical data $\mathcal{D}_t$. BMA is conceptually attractive because it accounts for model uncertainty, but posterior probabilities can be sensitive to priors and likelihood assumptions.

### 6.13.4 Regularized Regression Combination

A regularized linear model estimates:

$$
\hat\beta=
\arg\min_{\beta}
\left\{
\frac{1}{T}\sum_{t=1}^{T}(Y_{t,h}-\alpha-S_t\beta)^2
+\lambda\left[(1-\eta)\frac{1}{2}\|\beta\|_2^2+\eta\|\beta\|_1\right]
\right\},
$$

where $S_t$ is the signal vector, $\lambda\geq 0$ controls regularization strength, and $\eta\in[0,1]$ controls the mix between ridge and lasso penalties. This is the elastic-net objective. It is useful when many signals are correlated.

### 6.13.5 Tree Models and Ensembles

Tree-based models can capture nonlinearities and interactions:

$$
\hat y_{i,t,h}=\frac{1}{B}\sum_{b=1}^{B}T_b(S_{i,t}),
$$

where $T_b$ is tree $b$ and $B$ is the number of trees. Trees can detect conditional signal behavior, but they are dangerous in monthly macro data because the effective sample size is small. If used, they should be constrained, nested in walk-forward validation, and compared against simple linear baselines.

## 6.14 Mapping Signals into Forecasts

A signal score must be converted into a forecast object before it can be used in portfolio construction.

A simple linear mapping is:

$$
\hat\mu_{i,t,h}=a_{i,h}+b_{i,h}S_{i,t}.
$$

A cross-sectional rank mapping can use historical quantile returns:

$$
\hat\mu_{i,t,h}=\sum_{q=1}^{Q}\mathbf{1}\{S_{i,t}\in B_{q,t}\}\hat\mu_{q,h},
$$

where $B_{q,t}$ is signal bucket $q$ at time $t$ and $\hat\mu_{q,h}$ is the historical average forward return for that bucket estimated in a training window.

A probability mapping for positive return is:

$$
\hat p_{i,t,h}^{+}=\frac{1}{1+\exp[-(a_{i,h}+b_{i,h}S_{i,t})]}.
$$

The forecast mapping should be calibrated. A signal with high rank IC may still produce poorly calibrated probabilities or exaggerated expected returns.

## 6.15 Asset-Level Conviction Scores

A conviction score combines forecast magnitude, probability, confidence, and uncertainty. A generic conviction score can be written as:

$$
C_{i,t,h}=\underbrace{\frac{\hat\mu_{i,t,h}}{\hat\sigma_{i,t,h}}}_{\text{risk-adjusted forecast}}
\times
\underbrace{\kappa_{i,t,h}}_{\text{confidence}}
\times
\underbrace{\ell_{i,t}}_{\text{liquidity/implementation}}
\times
\underbrace{\rho_{t,h}^{regime}}_{\text{regime reliability}},
$$

where $\hat\mu_{i,t,h}$ is expected excess or active return, $\hat\sigma_{i,t,h}$ is expected horizon volatility, $\kappa_{i,t,h}\in[0,1]$ is model confidence, $\ell_{i,t}\in[0,1]$ is implementation quality, and $\rho_{t,h}^{regime}\in[0,1]$ reflects whether the current regime supports the signal.

A bounded conviction score can be:

$$
\tilde C_{i,t,h}=\tanh\left(\frac{C_{i,t,h}}{c}\right),
$$

where $c>0$ controls compression. This prevents extreme forecasts from dominating portfolio construction.

## 6.16 Confidence and Uncertainty

Confidence should not be based only on forecast magnitude. A strong forecast from an unstable or unvalidated signal should receive low confidence.

A practical confidence score can combine multiple components:

$$
\kappa_{i,t,h}=\kappa_h^{IC}\cdot\kappa_h^{stability}\cdot\kappa_{t}^{regime}\cdot\kappa_{i,t}^{data}\cdot\kappa_{i,t}^{cost},
$$

where:

| Component | Meaning |
|---|---|
| $\kappa_h^{IC}$ | Historical signal efficacy at horizon $h$. |
| $\kappa_h^{stability}$ | Stability across subperiods and regimes. |
| $\kappa_t^{regime}$ | Confidence that current regime supports the signal. |
| $\kappa_{i,t}^{data}$ | Data quality, staleness, and feature availability. |
| $\kappa_{i,t}^{cost}$ | Liquidity, turnover, transaction cost, margin, and capacity quality. |

Each component should be bounded between zero and one. This keeps conviction from rising when data quality, regime confidence, or implementation feasibility is poor.

## 6.17 Conviction Interpretation Table

| Conviction Range | Interpretation | Portfolio Use |
|---:|---|---|
| $C>0.75$ | Strong positive conviction. | Eligible for overweight or risk-budget increase if constraints allow. |
| $0.25<C\leq0.75$ | Moderate positive conviction. | Small tilt or watchlist positive. |
| $-0.25\leq C\leq0.25$ | Neutral or uncertain. | No active tilt or maintain baseline. |
| $-0.75\leq C<-0.25$ | Moderate negative conviction. | Underweight, hedge, or reduce risk. |
| $C<-0.75$ | Strong negative conviction. | Strong underweight or risk-control action subject to governance. |

The thresholds are illustrative. In production, thresholds should be calibrated to historical forecast distributions, turnover constraints, and portfolio risk budgets.

## 6.18 Conviction Versus Position Size

Conviction is not position size. A high conviction can still produce a small position if the asset is volatile, illiquid, highly correlated, expensive to trade, leverage-constrained, or outside mandate limits.

A simple active-weight mapping is:

$$
w_{i,t}^{active}=\lambda_t\frac{\tilde C_{i,t,h}}{\hat\sigma_{i,t,h}},
$$

where $\lambda_t$ scales total active risk. A constrained optimizer may then adjust the weights for covariance, transaction costs, beta, duration, FX, sector exposure, concentration, and leverage.

A transaction-cost-adjusted expected return is:

$$
\hat\mu_{i,t,h}^{net}=\hat\mu_{i,t,h}-\mathrm{TC}_{i,t}(\Delta w_{i,t})-\mathrm{Financing}_{i,t}-\mathrm{RollCost}_{i,t},
$$

where $\Delta w_{i,t}=w_{i,t}-w_{i,t-1}$. A signal should not be considered implementable if its gross forecast is smaller than realistic costs and frictions.

## 6.19 Python: Signal Metric Toolkit

The following code provides reusable signal-identification functions for time-series and cross-sectional research. It assumes point-in-time signals and correctly aligned forward targets.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, pearsonr


@dataclass(frozen=True)
class SignalMetricConfig:
    """Configuration for signal evaluation."""

    min_obs: int = 24
    top_quantile: float = 0.8
    bottom_quantile: float = 0.2


def _clean_pair(x: pd.Series, y: pd.Series) -> pd.DataFrame:
    """Align and clean two numeric series."""
    df = pd.concat([x.rename("x"), y.rename("y")], axis=1)
    return df.replace([np.inf, -np.inf], np.nan).dropna().astype(float)


def time_series_ic(
    signal: pd.Series,
    target: pd.Series,
    method: str = "pearson",
    min_obs: int = 24,
) -> float:
    """Compute time-series IC for one signal and target."""
    df = _clean_pair(signal, target)
    if len(df) < min_obs:
        return np.nan
    if method == "pearson":
        return float(pearsonr(df["x"], df["y"])[0])
    if method == "spearman":
        return float(spearmanr(df["x"], df["y"])[0])
    raise ValueError("method must be 'pearson' or 'spearman'.")


def cross_sectional_ic_by_date(
    panel: pd.DataFrame,
    signal_col: str,
    target_col: str,
    method: str = "spearman",
    min_assets: int = 5,
) -> pd.Series:
    """Compute cross-sectional IC by date.

    panel must have a MultiIndex with levels (date, asset).
    """
    if not isinstance(panel.index, pd.MultiIndex):
        raise TypeError("panel must have MultiIndex (date, asset).")
    missing = {signal_col, target_col} - set(panel.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")

    values = {}
    for date, group in panel[[signal_col, target_col]].dropna().groupby(level=0):
        if len(group) < min_assets:
            values[date] = np.nan
            continue
        x = group[signal_col].astype(float)
        y = group[target_col].astype(float)
        if method == "spearman":
            values[date] = float(spearmanr(x, y)[0])
        elif method == "pearson":
            values[date] = float(pearsonr(x, y)[0])
        else:
            raise ValueError("method must be 'pearson' or 'spearman'.")
    return pd.Series(values, name=f"{method}_ic")


def hit_rate(forecast: pd.Series, realized: pd.Series, min_obs: int = 24) -> float:
    """Compute directional hit rate."""
    df = _clean_pair(forecast, realized)
    if len(df) < min_obs:
        return np.nan
    return float((np.sign(df["x"]) == np.sign(df["y"])).mean())


def payoff_ratio(forecast: pd.Series, realized: pd.Series, min_obs: int = 24) -> float:
    """Compute payoff ratio for positive forecasts."""
    df = _clean_pair(forecast, realized)
    df = df[df["x"] > 0]
    if len(df) < min_obs:
        return np.nan
    gains = df.loc[df["y"] > 0, "y"]
    losses = df.loc[df["y"] < 0, "y"]
    if gains.empty or losses.empty:
        return np.nan
    return float(gains.mean() / abs(losses.mean()))
```

## 6.20 Python: Quantile Spread and Monotonicity Diagnostics

```python
def quantile_return_spread(
    panel: pd.DataFrame,
    signal_col: str,
    target_col: str,
    top_q: float = 0.8,
    bottom_q: float = 0.2,
    min_assets: int = 10,
) -> pd.Series:
    """Compute top-minus-bottom conditional return spread by date."""
    if not isinstance(panel.index, pd.MultiIndex):
        raise TypeError("panel must have MultiIndex (date, asset).")
    if not 0 < bottom_q < top_q < 1:
        raise ValueError("Require 0 < bottom_q < top_q < 1.")

    spreads = {}
    for date, group in panel[[signal_col, target_col]].dropna().groupby(level=0):
        if len(group) < min_assets:
            spreads[date] = np.nan
            continue
        lo = group[signal_col].quantile(bottom_q)
        hi = group[signal_col].quantile(top_q)
        top = group.loc[group[signal_col] >= hi, target_col]
        bottom = group.loc[group[signal_col] <= lo, target_col]
        spreads[date] = float(top.mean() - bottom.mean())
    return pd.Series(spreads, name="top_minus_bottom_spread")


def bucket_monotonicity_table(
    panel: pd.DataFrame,
    signal_col: str,
    target_col: str,
    n_buckets: int = 5,
) -> pd.DataFrame:
    """Compute average target by signal bucket within each date.

    Buckets are formed cross-sectionally each date, then averaged through time.
    """
    rows = []
    for date, group in panel[[signal_col, target_col]].dropna().groupby(level=0):
        if group[signal_col].nunique() < n_buckets:
            continue
        try:
            bucket = pd.qcut(
                group[signal_col],
                q=n_buckets,
                labels=False,
                duplicates="drop",
            )
        except ValueError:
            continue
        tmp = group.copy()
        tmp["bucket"] = bucket
        avg = tmp.groupby("bucket")[target_col].mean()
        for b, val in avg.items():
            rows.append({"date": date, "bucket": int(b), "avg_target": float(val)})

    if not rows:
        return pd.DataFrame(columns=["bucket", "mean_target", "n_dates"])
    df = pd.DataFrame(rows)
    return df.groupby("bucket").agg(
        mean_target=("avg_target", "mean"),
        n_dates=("avg_target", "count"),
    )
```

## 6.21 Python: Signal Decay Across Horizons

```python
def signal_decay_table(
    panel_by_horizon: dict[int, pd.DataFrame],
    signal_col: str,
    target_col: str = "target",
    method: str = "spearman",
) -> pd.DataFrame:
    """Evaluate average cross-sectional IC across multiple horizons."""
    rows = []
    for h, panel in sorted(panel_by_horizon.items()):
        ic = cross_sectional_ic_by_date(
            panel,
            signal_col=signal_col,
            target_col=target_col,
            method=method,
        )
        rows.append(
            {
                "horizon_months": h,
                "mean_ic": float(ic.mean()),
                "ic_vol": float(ic.std(ddof=1)),
                "ic_ir": float(ic.mean() / ic.std(ddof=1)) if ic.std(ddof=1) > 0 else np.nan,
                "n_dates": int(ic.notna().sum()),
            }
        )
    out = pd.DataFrame(rows)
    if not out.empty and abs(out.loc[0, "mean_ic"]) > 0:
        out["decay_vs_first"] = out["mean_ic"].abs() / abs(out.loc[0, "mean_ic"])
    else:
        out["decay_vs_first"] = np.nan
    return out
```

## 6.22 Python: Orthogonalization and Incremental IC

```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


def orthogonalize_signal(
    panel: pd.DataFrame,
    candidate_col: str,
    existing_cols: list[str],
    by_date: bool = False,
) -> pd.Series:
    """Orthogonalize a candidate signal against existing signals.

    If by_date is True, residualization is cross-sectional within each date.
    Otherwise, residualization is pooled across the panel. For production,
    residualization should be performed inside walk-forward training windows.
    """
    cols = [candidate_col] + existing_cols
    missing = set(cols) - set(panel.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")

    def _resid(df: pd.DataFrame) -> pd.Series:
        clean = df[cols].dropna().astype(float)
        out = pd.Series(np.nan, index=df.index)
        if len(clean) <= len(existing_cols) + 2:
            return out
        model = Pipeline([
            ("scaler", StandardScaler()),
            ("ols", LinearRegression()),
        ])
        model.fit(clean[existing_cols], clean[candidate_col])
        pred = model.predict(clean[existing_cols])
        out.loc[clean.index] = clean[candidate_col] - pred
        return out

    if by_date:
        residuals = []
        for _, group in panel.groupby(level=0):
            residuals.append(_resid(group))
        result = pd.concat(residuals).sort_index()
    else:
        result = _resid(panel).sort_index()
    result.name = f"{candidate_col}_orthogonal"
    return result


def incremental_rank_ic(
    panel: pd.DataFrame,
    candidate_col: str,
    existing_cols: list[str],
    target_col: str,
) -> dict[str, float]:
    """Compare raw and orthogonalized candidate signal rank IC."""
    raw_ic = cross_sectional_ic_by_date(panel, candidate_col, target_col).mean()
    residual = orthogonalize_signal(panel, candidate_col, existing_cols, by_date=True)
    tmp = panel.copy()
    tmp[residual.name] = residual
    orth_ic = cross_sectional_ic_by_date(tmp, residual.name, target_col).mean()
    return {"raw_rank_ic": float(raw_ic), "orthogonal_rank_ic": float(orth_ic)}
```

## 6.23 Python: Signal Combination Engine

```python
def historical_ic_weights(
    ic_history: pd.DataFrame,
    shrink_to_equal: float = 0.50,
    floor_negative: bool = True,
) -> pd.Series:
    """Compute shrunk IC/IR-based signal weights.

    ic_history columns are signals and rows are historical dates.
    """
    if not 0 <= shrink_to_equal <= 1:
        raise ValueError("shrink_to_equal must be between 0 and 1.")
    mean_ic = ic_history.mean(axis=0)
    vol_ic = ic_history.std(axis=0, ddof=1).replace(0.0, np.nan)
    ir = mean_ic / vol_ic
    score = ir.copy()
    if floor_negative:
        score = score.clip(lower=0.0)
    if score.fillna(0.0).sum() <= 0:
        raw_w = pd.Series(1.0 / len(score), index=score.index)
    else:
        raw_w = score.fillna(0.0) / score.fillna(0.0).sum()
    equal_w = pd.Series(1.0 / len(score), index=score.index)
    return shrink_to_equal * equal_w + (1.0 - shrink_to_equal) * raw_w


def combine_signals(
    signal_panel: pd.DataFrame,
    signal_cols: list[str],
    weights: pd.Series | None = None,
    output_col: str = "composite_signal",
) -> pd.DataFrame:
    """Combine standardized signal columns into one composite score."""
    missing = set(signal_cols) - set(signal_panel.columns)
    if missing:
        raise KeyError(f"Missing signal columns: {sorted(missing)}")
    X = signal_panel[signal_cols].astype(float)
    if weights is None:
        w = pd.Series(1.0 / len(signal_cols), index=signal_cols)
    else:
        w = weights.reindex(signal_cols).astype(float)
        if w.isna().any():
            raise ValueError("weights must include every signal column.")
        if abs(w.sum()) < 1e-12:
            raise ValueError("weights cannot sum to zero.")
        w = w / w.sum()
    out = signal_panel.copy()
    out[output_col] = X.mul(w, axis=1).sum(axis=1, min_count=1)
    return out
```

## 6.24 Python: Conviction Scoring Engine

```python
def bounded_score(x: pd.Series | pd.DataFrame, scale: float = 1.0):
    """Apply tanh compression to a score."""
    if scale <= 0:
        raise ValueError("scale must be positive.")
    return np.tanh(x / scale)


def conviction_score(
    expected_return: pd.Series,
    expected_volatility: pd.Series,
    confidence: pd.Series,
    liquidity_quality: pd.Series | None = None,
    regime_reliability: pd.Series | None = None,
    scale: float = 1.0,
) -> pd.Series:
    """Compute bounded asset-level conviction scores.

    All inputs should be indexed by asset for one decision timestamp and horizon.
    """
    df = pd.concat(
        [
            expected_return.rename("mu"),
            expected_volatility.rename("vol"),
            confidence.rename("confidence"),
        ],
        axis=1,
    )
    if liquidity_quality is not None:
        df["liquidity"] = liquidity_quality
    else:
        df["liquidity"] = 1.0
    if regime_reliability is not None:
        df["regime"] = regime_reliability
    else:
        df["regime"] = 1.0

    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    if (df["vol"] <= 0).any():
        raise ValueError("expected_volatility must be positive.")

    raw = (df["mu"] / df["vol"]) * df["confidence"] * df["liquidity"] * df["regime"]
    out = pd.Series(np.tanh(raw / scale), index=df.index, name="conviction")
    return out


def conviction_to_active_weights(
    conviction: pd.Series,
    volatility: pd.Series,
    gross_active_limit: float = 1.0,
) -> pd.Series:
    """Map conviction to simple volatility-adjusted active weights.

    This is not a full optimizer. It is a transparent pre-optimizer mapping.
    """
    if gross_active_limit <= 0:
        raise ValueError("gross_active_limit must be positive.")
    df = pd.concat([conviction.rename("c"), volatility.rename("vol")], axis=1).dropna()
    if (df["vol"] <= 0).any():
        raise ValueError("volatility must be positive.")
    raw = df["c"] / df["vol"]
    gross = raw.abs().sum()
    if gross <= 0:
        return raw.rename("active_weight")
    return (gross_active_limit * raw / gross).rename("active_weight")
```

## 6.25 Python: End-to-End Synthetic Example

```python
# Synthetic example only. Replace with point-in-time signals and aligned targets.
rng = np.random.default_rng(123)
dates = pd.date_range("2005-01-31", periods=180, freq="M")
assets = ["Equity", "Duration", "Credit", "Commodity", "FX_Carry", "Vol_Carry"]

rows = []
for date in dates:
    for asset in assets:
        rows.append({
            "date": date,
            "asset": asset,
            "trend": rng.normal(),
            "carry": rng.normal(),
            "value": rng.normal(),
            "credit_stress": rng.normal(),
        })

panel = pd.DataFrame(rows).set_index(["date", "asset"]).sort_index()

# Build a synthetic target with weak signal structure.
panel["target"] = (
    0.010 * panel["trend"]
    + 0.006 * panel["carry"]
    + 0.004 * panel["value"]
    - 0.008 * panel["credit_stress"]
    + rng.normal(0.0, 0.05, len(panel))
)

signal_cols = ["trend", "carry", "value", "credit_stress"]

# Evaluate each signal.
metrics = []
for col in signal_cols:
    ic = cross_sectional_ic_by_date(panel, col, "target", method="spearman")
    spread = quantile_return_spread(panel, col, "target")
    metrics.append({
        "signal": col,
        "mean_rank_ic": ic.mean(),
        "rank_ic_ir": ic.mean() / ic.std(ddof=1),
        "avg_spread": spread.mean(),
        "spread_tstat_simple": spread.mean() / (spread.std(ddof=1) / np.sqrt(spread.notna().sum())),
    })
metrics_df = pd.DataFrame(metrics).set_index("signal")
print(metrics_df)

# Combine signals with equal weights.
combined = combine_signals(panel, signal_cols, output_col="composite")
composite_ic = cross_sectional_ic_by_date(combined, "composite", "target")
print("Composite mean rank IC:", composite_ic.mean())

# Create a one-date conviction snapshot.
latest_date = dates[-1]
snapshot = combined.loc[latest_date]
expected_return = 0.03 * snapshot["composite"]
expected_vol = pd.Series(0.12, index=snapshot.index)
confidence = pd.Series(0.60, index=snapshot.index)
liquidity = pd.Series({
    "Equity": 1.0,
    "Duration": 1.0,
    "Credit": 0.8,
    "Commodity": 0.8,
    "FX_Carry": 0.7,
    "Vol_Carry": 0.5,
})
regime_reliability = pd.Series(0.75, index=snapshot.index)

conv = conviction_score(
    expected_return,
    expected_vol,
    confidence,
    liquidity_quality=liquidity,
    regime_reliability=regime_reliability,
    scale=1.0,
)
weights = conviction_to_active_weights(conv, expected_vol, gross_active_limit=0.30)
print(pd.concat([conv, weights], axis=1))
```

## 6.26 Visualization Code for Signal Diagnostics

```python
import matplotlib.pyplot as plt


def plot_cumulative_ic(ic: pd.Series, title: str = "Cumulative IC") -> None:
    """Plot cumulative information coefficient."""
    clean = ic.dropna()
    fig, ax = plt.subplots(figsize=(10, 4))
    clean.cumsum().plot(ax=ax)
    ax.axhline(0.0, linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative IC")
    plt.tight_layout()
    plt.show()


def plot_quantile_monotonicity(bucket_table: pd.DataFrame) -> None:
    """Plot average target return by signal bucket."""
    if "mean_target" not in bucket_table.columns:
        raise KeyError("bucket_table must include mean_target.")
    fig, ax = plt.subplots(figsize=(7, 4))
    bucket_table["mean_target"].plot(kind="bar", ax=ax)
    ax.axhline(0.0, linewidth=1)
    ax.set_title("Signal Monotonicity by Bucket")
    ax.set_xlabel("Signal bucket, low to high")
    ax.set_ylabel("Average forward target")
    plt.tight_layout()
    plt.show()


def plot_conviction_snapshot(conviction: pd.Series) -> None:
    """Plot one-date asset conviction scores."""
    fig, ax = plt.subplots(figsize=(8, 4))
    conviction.sort_values().plot(kind="barh", ax=ax)
    ax.axvline(0.0, linewidth=1)
    ax.set_title("Asset-Level Conviction Snapshot")
    ax.set_xlabel("Bounded conviction")
    plt.tight_layout()
    plt.show()


plot_cumulative_ic(composite_ic, "Composite Signal Cumulative Rank IC")
mono = bucket_monotonicity_table(combined, "composite", "target", n_buckets=5)
plot_quantile_monotonicity(mono)
plot_conviction_snapshot(conv)
```

## 6.27 Signal Validation Checklist

| Check | Required Evidence |
|---|---|
| Point-in-time construction | Feature, scaling, ranking, and universe are valid at timestamp $t$. |
| Economic rationale | Transmission channel is documented before testing. |
| Direction | Orientation sign is pre-specified and interpretable. |
| Horizon specificity | Evidence is shown for $t+1$, $t+3$, and $t+12$ separately. |
| IC and rank IC | Average, volatility, rolling history, and cumulative path are reported. |
| Conditional spread | Top-minus-bottom or high-minus-low return spread is reported. |
| Monotonicity | Signal buckets show economically sensible ordering. |
| Hit/payoff balance | Hit rate and payoff ratio are both evaluated. |
| Robust inference | Overlapping returns and serial dependence are handled later in validation. |
| Regime dependence | Signal efficacy is tested by regime probability or label. |
| Redundancy | Incremental IC versus existing signals is reported. |
| Turnover and costs | Signal change frequency and implementation cost are estimated. |
| Failure modes | Known environments of likely underperformance are documented. |
| Out-of-sample use | Walk-forward results are required before production use. |

## 6.28 Common Signal Identification Mistakes

1. **Testing before hypothesizing.** This creates narrative overfitting.
2. **Using full-sample ranks or z-scores.** This leaks future information.
3. **Ignoring horizon.** A signal may work at $t+12$ but fail at $t+1$.
4. **Confusing IC with portfolio alpha.** IC does not include costs, risk, constraints, or capacity.
5. **Double-counting correlated signals.** Redundant signals can create false confidence.
6. **Relying only on hit rate.** Payoff asymmetry and tail losses matter.
7. **Ignoring monotonicity.** A signal driven only by one extreme bucket may be fragile.
8. **Overweighting optimized combinations.** Small samples make optimized signal weights unstable.
9. **Treating conviction as position size.** Portfolio weights require risk and constraint integration.
10. **Ignoring implementation frictions.** Turnover, financing, roll, margin, and liquidity can erase gross efficacy.

## 6.29 Part 6 Summary

Part 6 developed the signal identification, ranking, and conviction-scoring layer of the macro-regime research process. The main lessons are:

1. A feature becomes a signal only when it has a pre-specified economic rationale, direction, target, horizon, universe, and validation plan.
2. Signal orientation should make higher scores consistently interpretable, either as higher return potential or higher risk.
3. Horizon specificity is essential because macro surprises, credit impulses, trend, carry, valuation, liquidity stress, and yield-curve signals decay at different speeds.
4. IC and rank IC measure the relationship between signals and future outcomes, but they do not prove implementable alpha.
5. Hit rate must be interpreted with payoff ratio and downside risk.
6. Conditional spread and quantile monotonicity help connect statistical ranking to implementable portfolio tilts.
7. Signal stability should be tested across time, regimes, horizons, geographies, asset classes, and implementation choices.
8. Orthogonalization and redundancy analysis help identify incremental information rather than repeated exposure to the same latent factor.
9. Signal combination should begin with equal weights or strongly regularized approaches; optimized weights require careful validation.
10. Conviction scores should combine expected return, risk, confidence, regime reliability, data quality, liquidity, and implementation feasibility.
11. Conviction is not position size; final weights require portfolio construction, covariance, constraints, costs, and risk management.

---

# Stop Point

This installment completes:

1. **Part 6: Signal Identification, Ranking, and Conviction Scoring.**

Continue next with **Part 7: Statistical Validation, Inference, and Robustness Testing**.
