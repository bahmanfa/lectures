# Institutional Macro-Regime Detection, Multi-Asset Signal Identification, and Statistical Validation Curriculum

## Installment 9: Part 9 - Regime-Conditioned Forecasting and Dynamic Convictions

**Scope of this installment.** This installment continues the curriculum with **Part 9 only**. It assumes the global assumptions, timestamp conventions, feature engineering framework, return-target definitions, regime-detection concepts, causal-channel framework, signal-scoring framework, validation standards, and machine-learning controls established in Installments 1 through 8.

**Educational boundary.** This document is for research education, model design, and institutional portfolio-process development. It is not personalized investment advice, a live trading recommendation, or a guarantee of alpha.

---

# Part 9: Regime-Conditioned Forecasting and Dynamic Convictions

## 9.1 Purpose of Regime-Conditioned Forecasting

Regime-conditioned forecasting links the latent-state view of the macro-financial environment to asset-level forecasts and portfolio-aware convictions. The basic idea is that expected returns, volatility, correlations, signal efficacy, drawdown probabilities, and implementation risks are not constant across environments. A trend signal may behave differently during liquidity stress than during a stable expansion. Credit carry may look attractive in normal environments but become fragile when funding conditions deteriorate. Duration may hedge equity risk in a disinflationary slowdown but fail as a hedge during an inflation shock.

Let $S_t \in \{1,\ldots,K\}$ denote a latent regime at decision timestamp $t$, and let $\pi_{k,t}$ denote the filtered probability of regime $k$:

$$
\pi_{k,t}=\Pr(S_t=k\mid\mathcal{F}_t),
\qquad
\sum_{k=1}^{K}\pi_{k,t}=1.
$$

The objective is to transform the regime probability vector $\boldsymbol{\pi}_t$ into forecasts for each asset $i$ and horizon $h\in\{1,3,12\}$:

$$
\hat\mu_{i,t,h},\quad
\hat\sigma_{i,t,h},\quad
\hat\Sigma_{t,h},\quad
\hat p_{i,t,h}^{+},\quad
\hat q_{i,t,h}^{\alpha},\quad
C_{i,t,h}.
$$

Here $\hat\mu$ is expected return, $\hat\sigma$ is expected volatility, $\hat\Sigma$ is the covariance matrix, $\hat p^+$ is probability of positive return, $\hat q^\alpha$ is a lower-tail quantile forecast, and $C$ is a conviction score.

Regime conditioning should not mean replacing statistical discipline with regime narratives. A regime is useful only if it improves forecasting, risk estimation, signal reliability assessment, or portfolio construction relative to a regime-unaware benchmark.

## 9.2 Regime-Conditioned Expected Returns

The simplest regime-conditioned expected return estimates a separate average return for each asset, horizon, and regime. If $R_{i,t,h}$ is the forward cumulative return of asset $i$ from $t+1$ through $t+h$, a probability-weighted regime mean is:

$$
\hat\mu_{i,k,h}=
\frac{\sum_{t=1}^{T}\pi_{k,t}R_{i,t,h}}
{\sum_{t=1}^{T}\pi_{k,t}}.
$$

The numerator weights each forward return by the probability that regime $k$ was active at the decision timestamp. The denominator is the effective probability mass assigned to that regime.

The current regime-conditioned forecast is:

$$
\hat\mu_{i,t,h}^{reg}=
\sum_{k=1}^{K}\pi_{k,t}\hat\mu_{i,k,h}.
$$

**Interpretation.** If the model estimates a 70% probability of a growth-slowdown regime and a 30% probability of an inflation-shock regime, the asset forecast is an average of the asset's slowdown-conditioned and inflation-shock-conditioned expected returns.

### 9.2.1 Effective Sample Size

A regime with low probability mass has few effective observations. The effective sample size of regime $k$ can be approximated as:

$$
N_{eff,k}=\frac{\left(\sum_{t=1}^{T}\pi_{k,t}\right)^2}
{\sum_{t=1}^{T}\pi_{k,t}^{2}}.
$$

If $N_{eff,k}$ is small, $\hat\mu_{i,k,h}$ is noisy and should be heavily shrunk toward a prior.

### 9.2.2 Shrinkage Toward Unconditional Mean

A shrinkage estimator is:

$$
\tilde\mu_{i,k,h}=
\lambda_{k,h}\hat\mu_{i,k,h}
+(1-\lambda_{k,h})\hat\mu_{i,h}^{0},
$$

where $\hat\mu_{i,h}^{0}$ is an unconditional or baseline expected return and $\lambda_{k,h}\in[0,1]$ is a confidence weight. One practical choice is:

$$
\lambda_{k,h}=\frac{N_{eff,k}}{N_{eff,k}+\tau_h},
$$

where $\tau_h>0$ controls shrinkage strength. Larger $\tau_h$ means more shrinkage, especially for sparse regimes.

## 9.3 Regime-Conditioned Volatility and Covariance

Expected returns are only one part of regime conditioning. Risk often changes more reliably than mean returns. Let $R_{t,h}$ be the $N\times1$ vector of asset forward returns at timestamp $t$ and horizon $h$. The regime-conditioned mean vector is $\hat\mu_{k,h}$. A probability-weighted covariance estimate is:

$$
\hat\Sigma_{k,h}=
\frac{
\sum_{t=1}^{T}\pi_{k,t}
(R_{t,h}-\hat\mu_{k,h})(R_{t,h}-\hat\mu_{k,h})^{\top}
}{
\sum_{t=1}^{T}\pi_{k,t}
}.
$$

The current probability-weighted covariance is:

$$
\hat\Sigma_{t,h}^{reg}=
\sum_{k=1}^{K}\pi_{k,t}\hat\Sigma_{k,h}.
$$

This mixture covariance captures within-regime covariance. A full mixture-distribution covariance also includes uncertainty about regime means:

$$
\hat\Sigma_{t,h}^{mix}=
\sum_{k=1}^{K}\pi_{k,t}
\left[
\hat\Sigma_{k,h}
+
(\hat\mu_{k,h}-\hat\mu_{t,h}^{reg})
(\hat\mu_{k,h}-\hat\mu_{t,h}^{reg})^{\top}
\right].
$$

The second term adds dispersion across regime mean forecasts. This term can matter when plausible regimes imply very different asset outcomes.

### 9.3.1 Regime-Conditioned Correlation Breakdown

During stress, correlations often rise and diversification can fail. If $\hat\Sigma_{k,h}$ is the covariance matrix in regime $k$, the corresponding correlation is:

$$
\hat\rho_{ij,k,h}=
\frac{\hat\Sigma_{ij,k,h}}
{\sqrt{\hat\Sigma_{ii,k,h}\hat\Sigma_{jj,k,h}}}.
$$

A portfolio that appears diversified using unconditional covariance may become concentrated when the relevant stress-regime covariance is used. Regime-conditioned covariance is therefore essential for drawdown-aware allocation and stress testing.

## 9.4 Conditional Signal Efficacy by Regime

A signal can have different efficacy across regimes. Let $s_{i,t}$ be a signal and $Y_{i,t,h}$ be a forward target. A regime-weighted information coefficient can be estimated as:

$$
IC_{k,h}=\mathrm{corr}_{w_k}(s_{i,t},Y_{i,t,h}),
\qquad w_{k,t}=\pi_{k,t},
$$

where $\mathrm{corr}_{w_k}$ is a weighted correlation using regime probabilities as weights.

For cross-sectional rank IC at each date, define $RIC_{t,h}$. A regime-weighted average rank IC is:

$$
\overline{RIC}_{k,h}=
\frac{\sum_{t=1}^{T}\pi_{k,t}RIC_{t,h}}
{\sum_{t=1}^{T}\pi_{k,t}}.
$$

A signal reliability score can then be mapped from regime-conditioned efficacy:

$$
\rho_{s,t,h}^{regime}=
\sum_{k=1}^{K}\pi_{k,t}g(\overline{RIC}_{s,k,h}),
$$

where $g(\cdot)$ maps historical efficacy into $[0,1]$. For example:

$$
g(x)=\min\left(1,\max\left(0,\frac{x}{x^{target}}\right)\right),
$$

where $x^{target}$ is a governance threshold for a strong positive rank IC.

### 9.4.1 Signal Gating Versus Signal Scaling

Regime information can be used in two ways:

| Approach | Formula | Interpretation | Risk |
|---|---:|---|---|
| Hard gate | $s_{t}^{adj}=s_t\mathbf{1}\{\pi_{k,t}>c\}$ | Signal is active only above a regime threshold. | Brittle and threshold-sensitive. |
| Soft scaling | $s_{t}^{adj}=s_t\sum_k\pi_{k,t}\rho_{s,k}$ | Signal is scaled by regime-conditioned reliability. | More stable but may dilute strong state-specific signals. |

Soft scaling is usually more appropriate for institutional macro research because regime probabilities are uncertain.

## 9.5 Probability-Weighted Expected Returns Across Regimes

If each regime produces its own forecast model $\mathcal{M}_k$, then the regime-conditioned expected return is:

$$
\hat\mu_{i,t,h}=
\sum_{k=1}^{K}\pi_{k,t}\hat\mu_{i,t,h}^{(k)},
$$

where:

$$
\hat\mu_{i,t,h}^{(k)}=
\mathcal{M}_{k,h}(X_{i,t}).
$$

This formulation is more flexible than a static regime mean. It allows each regime to have different signal coefficients:

$$
R_{i,t,h}=\alpha_{i,k,h}+\beta_{k,h}^{\top}X_{i,t}+\varepsilon_{i,t,h},
\qquad S_t=k.
$$

The probability-weighted forecast is then:

$$
\hat R_{i,t,h}=\sum_{k=1}^{K}\pi_{k,t}
\left(\hat\alpha_{i,k,h}+\hat\beta_{k,h}^{\top}X_{i,t}\right).
$$

**Practical caution.** Estimating a full model per regime can be unstable because each regime has fewer effective observations. A practical compromise is to use common coefficients plus regime interactions:

$$
R_{i,t,h}=\alpha_i+\beta^{\top}X_{i,t}
+\sum_{k=1}^{K}\pi_{k,t}\gamma_k^{\top}X_{i,t}
+\varepsilon_{i,t,h}.
$$

This allows signal efficacy to vary by regime without requiring fully separate models.

## 9.6 Dynamic Model Averaging

Dynamic model averaging combines several forecasting models using time-varying weights. Let $\hat y_{i,t,h}^{(m)}$ be the forecast from model $m\in\{1,\ldots,M\}$. The ensemble forecast is:

$$
\hat y_{i,t,h}^{DMA}=\sum_{m=1}^{M}w_{m,t,h}\hat y_{i,t,h}^{(m)},
\qquad
\sum_{m=1}^{M}w_{m,t,h}=1.
$$

Model weights can be updated using recent predictive likelihoods:

$$
w_{m,t,h}\propto
w_{m,t-1,h}^{\delta}
\cdot
p_m(Y_{t,h}\mid\mathcal{F}_{t-h}),
$$

where $0<\delta\leq1$ is a forgetting factor and $p_m(\cdot)$ is the predictive likelihood of the realized outcome under model $m$. The weights are normalized to sum to one.

A regime-aware version makes model weights depend on the regime vector:

$$
w_{m,t,h}=\sum_{k=1}^{K}\pi_{k,t}w_{m,k,h},
$$

where $w_{m,k,h}$ is the historical or learned weight of model $m$ in regime $k$.

### 9.6.1 Model Families in Dynamic Averaging

| Model | Forecast Object | Typical Role |
|---|---|---|
| Carry model | Expected return from yield, roll, or income. | Baseline for bonds, FX, credit, commodities. |
| Trend model | Return continuation or risk-on/risk-off signal. | Tactical timing and cross-asset momentum. |
| Macro model | Forecast from growth, inflation, policy, and credit features. | Regime-aware expected return. |
| Volatility model | Risk and drawdown forecast. | Exposure scaling and downside control. |
| Valuation model | Long-horizon return expectation. | Strategic $t+12$ tilt. |
| ML ensemble | Nonlinear forecast. | Interaction discovery with strict validation. |

Dynamic model averaging should be benchmarked against equal weights. If dynamic weights do not improve out-of-sample performance, the added complexity is not justified.

## 9.7 Bayesian Updating of Regime Probabilities

Regime probabilities can be updated as new evidence arrives. Suppose $\pi_{k,t|t-1}$ is the prior probability of regime $k$ before observing new data $x_t$. The Bayesian update is:

$$
\pi_{k,t|t}=\frac{p(x_t\mid S_t=k)\pi_{k,t|t-1}}
{\sum_{j=1}^{K}p(x_t\mid S_t=j)\pi_{j,t|t-1}}.
$$

The prior can come from a transition matrix:

$$
\boldsymbol{\pi}_{t|t-1}=P^{\top}\boldsymbol{\pi}_{t-1|t-1},
$$

where $P$ is the $K\times K$ transition matrix. The likelihood $p(x_t\mid S_t=k)$ measures how consistent new evidence $x_t$ is with regime $k$.

### 9.7.1 Incorporating Market-Implied Evidence

Official macro data is slow. Market-implied data can update regime probabilities between macro releases. Let $x_t$ include credit-spread changes, volatility term structure, yield-curve shifts, FX stress, and commodity shocks. A combined likelihood is:

$$
p(x_t\mid S_t=k)=p(x_t^{macro}\mid S_t=k)
\cdot p(x_t^{market}\mid S_t=k),
$$

if the components are conditionally independent given the regime. This assumption is often too strong, but it clarifies the modeling choice. In production, the likelihood may use a multivariate distribution with regularized covariance.

## 9.8 Regime Uncertainty and Conviction Decay

Conviction should decay when regime uncertainty is high. One measure of regime uncertainty is entropy:

$$
H_t=-\sum_{k=1}^{K}\pi_{k,t}\log(\pi_{k,t}).
$$

The maximum entropy is $\log K$, which occurs when all regimes have equal probability. A normalized certainty score is:

$$
\zeta_t=1-\frac{H_t}{\log K}.
$$

Here $\zeta_t\in[0,1]$. A value near one means one regime dominates. A value near zero means high regime uncertainty.

A conviction decay rule is:

$$
C_{i,t,h}^{adj}=C_{i,t,h}^{raw}\cdot
\left[\zeta_t+(1-\zeta_t)\eta\right],
\qquad 0\leq\eta\leq1.
$$

If $\eta=0$, conviction goes to zero when regime uncertainty is maximal. If $\eta>0$, some conviction remains even under uncertainty.

### 9.8.1 Disagreement Across Regime Forecasts

Another uncertainty measure is forecast dispersion across regimes:

$$
D_{i,t,h}^{reg}=\sqrt{
\sum_{k=1}^{K}\pi_{k,t}
\left(\hat\mu_{i,t,h}^{(k)}-\hat\mu_{i,t,h}\right)^2
}.
$$

A dispersion-adjusted expected return is:

$$
\hat\mu_{i,t,h}^{adj}=\hat\mu_{i,t,h}
-\lambda_D\operatorname{sign}(\hat\mu_{i,t,h})D_{i,t,h}^{reg},
$$

where $\lambda_D\geq0$ penalizes forecast disagreement. This reduces the magnitude of expected returns when plausible regimes disagree sharply.

## 9.9 Stress Adjustment of Convictions

A forecast can be adjusted for stress risk by combining expected return with downside scenarios. Let $\hat\mu_{i,t,h}$ be the base expected return and $L_{i,t,h}^{stress}$ be the stress loss under an adverse scenario. A stress-adjusted forecast can be:

$$
\hat\mu_{i,t,h}^{stressAdj}=\hat\mu_{i,t,h}
-\lambda_S\Pr_t(\mathrm{Stress})\cdot |L_{i,t,h}^{stress}|,
$$

where $\lambda_S\geq0$ controls stress aversion and $\Pr_t(\mathrm{Stress})$ is the probability of a stress regime or scenario.

If regime $k^*$ represents liquidity stress or crisis volatility, then:

$$
\Pr_t(\mathrm{Stress})=\pi_{k^*,t}.
$$

For multiple stress regimes:

$$
\Pr_t(\mathrm{Stress})=\sum_{k\in\mathcal{K}_{stress}}\pi_{k,t}.
$$

### 9.9.1 Conviction Under Tail Risk

A downside-aware conviction can use expected shortfall:

$$
C_{i,t,h}^{tail}=\frac{\hat\mu_{i,t,h}}
{|	ilde{ES}_{i,t,h}^{\alpha}|},
$$

where $\tilde{ES}^{\alpha}$ is a regime-weighted expected shortfall estimate at tail probability $\alpha$. This score favors assets with better expected return per unit of tail risk.

## 9.10 Mapping Regime Probabilities to Asset-Level Forecasts

An institutional regime-conditioned forecast table should include at least:

| Output | Formula | Use |
|---|---:|---|
| Expected return | $\sum_k\pi_{k,t}\hat\mu_{i,k,h}$ | Return forecast. |
| Volatility | $\sqrt{\hat\Sigma_{ii,t,h}}$ | Risk scaling. |
| Covariance | $\sum_k\pi_{k,t}\hat\Sigma_{k,h}$ | Portfolio construction. |
| Positive probability | $\sum_k\pi_{k,t}\hat p_{i,k,h}^{+}$ | Directional confidence. |
| Downside probability | $\sum_k\pi_{k,t}\hat p_{i,k,h}^{down}$ | Risk management. |
| Signal reliability | $\sum_k\pi_{k,t}\rho_{s,k,h}$ | Signal scaling. |
| Regime certainty | $1-H_t/\log K$ | Conviction decay. |
| Stress probability | $\sum_{k\in\mathcal{K}_{stress}}\pi_{k,t}$ | Tail adjustment. |

A complete asset-level conviction can be written as:

$$
C_{i,t,h}=\tanh\left(
\frac{1}{c}
\cdot
\frac{\hat\mu_{i,t,h}^{stressAdj}}
{\hat\sigma_{i,t,h}}
\cdot
\kappa_{i,t,h}
\cdot
\rho_{i,t,h}^{regime}
\cdot
\ell_{i,t}
\cdot
\zeta_t
\right),
$$

where $c>0$ is a scaling parameter, $\kappa$ is model confidence, $\rho^{regime}$ is regime-conditioned signal reliability, $\ell$ is liquidity or implementation quality, and $\zeta_t$ is regime certainty.

## 9.11 Regime-Conditioned Forecasting Workflow

A practical workflow is:

1. Build point-in-time macro and market features.
2. Estimate filtered regime probabilities using only information available at $t$.
3. Estimate regime-conditioned return, volatility, covariance, and signal efficacy using walk-forward or expanding historical windows.
4. Shrink sparse regime estimates toward unconditional or structurally motivated priors.
5. Combine regime-specific forecasts using current probabilities.
6. Penalize forecasts for regime entropy, forecast dispersion, stress risk, and weak validation.
7. Convert forecasts into asset-level conviction scores.
8. Pass convictions to portfolio construction with constraints, covariance, cost estimates, and risk budgets.
9. Monitor realized performance by regime and update confidence scores.

## 9.12 Required Data Structures

A regime-conditioned forecasting engine usually requires the following model-ready objects:

| Object | Shape | Description |
|---|---:|---|
| `returns_fwd[h]` | date $\times$ asset | Forward returns for horizon $h$. |
| `features` | date $\times$ feature | Point-in-time macro and market features. |
| `signals` | date $\times$ asset $\times$ signal | Asset-level signal scores. |
| `regime_probs` | date $\times$ regime | Filtered regime probabilities. |
| `stress_map` | regime list | Regimes treated as stress states. |
| `liquidity_scores` | date $\times$ asset | Implementation quality scores. |
| `cost_estimates` | date $\times$ asset | Transaction and financing cost estimates. |
| `validation_stats` | signal $\times$ regime $\times$ horizon | IC, spread, calibration, and stability diagnostics. |

The engine should preserve the decision timestamp of every forecast and the model version used to produce it.

## 9.13 Python: Regime-Conditioned Expected Return and Covariance

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RegimeForecastConfig:
    """Configuration for regime-conditioned forecast estimation."""

    min_effective_obs: float = 24.0
    shrink_tau: float = 36.0
    covariance_shrinkage: float = 0.25
    entropy_floor: float = 0.25
    stress_penalty: float = 0.50
    conviction_scale: float = 1.0


def _align_returns_and_probs(
    returns: pd.DataFrame,
    regime_probs: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Align forward returns and regime probabilities by date."""
    common = returns.index.intersection(regime_probs.index)
    if common.empty:
        raise ValueError("No overlapping dates between returns and regimes.")
    R = returns.loc[common].astype(float)
    P = regime_probs.loc[common].astype(float).clip(lower=0.0)
    P = P.div(P.sum(axis=1).replace(0.0, np.nan), axis=0)
    return R, P


def effective_sample_size(weights: pd.Series) -> float:
    """Compute probability-weighted effective sample size."""
    w = weights.dropna().astype(float).clip(lower=0.0)
    denom = float((w ** 2).sum())
    if denom <= 0.0:
        return 0.0
    return float((w.sum() ** 2) / denom)


def regime_conditioned_means(
    returns: pd.DataFrame,
    regime_probs: pd.DataFrame,
    config: RegimeForecastConfig = RegimeForecastConfig(),
) -> pd.DataFrame:
    """Estimate shrunk regime-conditioned expected returns.

    Parameters
    ----------
    returns:
        Forward return matrix with dates as rows and assets as columns.
    regime_probs:
        Filtered regime probability matrix with dates as rows.
    config:
        Shrinkage settings.

    Returns
    -------
    pd.DataFrame
        Rows are regimes and columns are assets.
    """
    R, P = _align_returns_and_probs(returns, regime_probs)
    unconditional = R.mean(axis=0)
    rows = []

    for regime in P.columns:
        w = P[regime]
        denom = w.sum()
        if denom <= 0:
            mu = pd.Series(np.nan, index=R.columns)
            n_eff = 0.0
        else:
            mu = R.mul(w, axis=0).sum(axis=0) / denom
            n_eff = effective_sample_size(w)

        lam = n_eff / (n_eff + config.shrink_tau)
        if n_eff < config.min_effective_obs:
            lam *= n_eff / max(config.min_effective_obs, 1.0)
        mu_shrunk = lam * mu + (1.0 - lam) * unconditional
        mu_shrunk.name = regime
        rows.append(mu_shrunk)

    return pd.DataFrame(rows)


def regime_conditioned_covariances(
    returns: pd.DataFrame,
    regime_probs: pd.DataFrame,
    config: RegimeForecastConfig = RegimeForecastConfig(),
) -> dict[str, pd.DataFrame]:
    """Estimate shrunk regime-conditioned covariance matrices."""
    R, P = _align_returns_and_probs(returns, regime_probs)
    unconditional_cov = R.cov()
    out: dict[str, pd.DataFrame] = {}

    for regime in P.columns:
        w = P[regime]
        denom = w.sum()
        if denom <= 0:
            out[regime] = unconditional_cov.copy()
            continue
        mu = R.mul(w, axis=0).sum(axis=0) / denom
        X = R.sub(mu, axis=1)
        cov = X.mul(w, axis=0).T.dot(X) / denom
        cov = pd.DataFrame(cov, index=R.columns, columns=R.columns)
        cov = (
            (1.0 - config.covariance_shrinkage) * cov
            + config.covariance_shrinkage * unconditional_cov
        )
        out[regime] = cov
    return out
```

## 9.14 Python: Probability-Weighted Forecasts and Mixture Covariance

```python
def probability_weighted_mean_forecast(
    current_probs: pd.Series,
    regime_means: pd.DataFrame,
) -> pd.Series:
    """Compute current probability-weighted expected returns."""
    p = current_probs.astype(float).clip(lower=0.0)
    p = p / p.sum()
    common = regime_means.index.intersection(p.index)
    if common.empty:
        raise ValueError("No common regimes between probabilities and means.")
    return regime_means.loc[common].mul(p.loc[common], axis=0).sum(axis=0)


def probability_weighted_covariance(
    current_probs: pd.Series,
    regime_covs: dict[str, pd.DataFrame],
    regime_means: pd.DataFrame | None = None,
    include_mean_dispersion: bool = True,
) -> pd.DataFrame:
    """Compute probability-weighted covariance matrix.

    If regime_means is supplied and include_mean_dispersion is True,
    the function adds the between-regime mean-dispersion term.
    """
    regimes = [r for r in current_probs.index if r in regime_covs]
    if not regimes:
        raise ValueError("No common regimes in current_probs and regime_covs.")
    p = current_probs.loc[regimes].astype(float).clip(lower=0.0)
    p = p / p.sum()

    assets = regime_covs[regimes[0]].index
    cov = pd.DataFrame(0.0, index=assets, columns=assets)
    for r in regimes:
        cov = cov + p[r] * regime_covs[r].loc[assets, assets]

    if include_mean_dispersion and regime_means is not None:
        mu_mix = regime_means.loc[regimes, assets].mul(p, axis=0).sum(axis=0)
        between = pd.DataFrame(0.0, index=assets, columns=assets)
        for r in regimes:
            diff = (regime_means.loc[r, assets] - mu_mix).to_numpy()
            between += p[r] * np.outer(diff, diff)
        cov = cov + between
    return cov


def regime_entropy(current_probs: pd.Series) -> float:
    """Compute normalized regime entropy in [0, 1]."""
    p = current_probs.dropna().astype(float).clip(lower=0.0)
    p = p / p.sum()
    p = p[p > 0]
    if len(p) <= 1:
        return 0.0
    entropy = -float((p * np.log(p)).sum())
    return entropy / np.log(len(p))


def regime_certainty(current_probs: pd.Series) -> float:
    """Return 1 - normalized entropy."""
    return 1.0 - regime_entropy(current_probs)
```

## 9.15 Python: Regime-Conditioned Signal Efficacy

```python
from scipy.stats import spearmanr


def cross_sectional_rank_ic_by_date(
    panel: pd.DataFrame,
    signal_col: str,
    target_col: str,
    min_assets: int = 5,
) -> pd.Series:
    """Compute cross-sectional Spearman rank IC by date.

    The panel index must be MultiIndex(date, asset).
    """
    if not isinstance(panel.index, pd.MultiIndex):
        raise TypeError("panel must have MultiIndex(date, asset).")
    out = {}
    for date, group in panel[[signal_col, target_col]].dropna().groupby(level=0):
        if len(group) < min_assets:
            out[date] = np.nan
        else:
            out[date] = float(spearmanr(group[signal_col], group[target_col])[0])
    return pd.Series(out, name=f"rank_ic_{signal_col}")


def regime_weighted_signal_efficacy(
    ic_series: pd.Series,
    regime_probs: pd.DataFrame,
) -> pd.Series:
    """Compute regime-weighted average IC for each regime."""
    common = ic_series.index.intersection(regime_probs.index)
    ic = ic_series.loc[common].astype(float)
    P = regime_probs.loc[common].astype(float).clip(lower=0.0)
    out = {}
    for regime in P.columns:
        w = P[regime]
        valid = ic.notna() & w.notna()
        if valid.sum() == 0 or w.loc[valid].sum() <= 0:
            out[regime] = np.nan
        else:
            out[regime] = float((ic.loc[valid] * w.loc[valid]).sum()
                                / w.loc[valid].sum())
    return pd.Series(out, name="regime_weighted_ic")


def reliability_from_efficacy(
    efficacy: pd.Series,
    target_ic: float = 0.05,
    floor: float = 0.0,
    cap: float = 1.0,
) -> pd.Series:
    """Map regime IC estimates into [floor, cap] reliability scores."""
    if target_ic <= 0:
        raise ValueError("target_ic must be positive.")
    rel = efficacy / target_ic
    return rel.clip(lower=floor, upper=cap).fillna(floor)


def current_regime_reliability(
    current_probs: pd.Series,
    regime_reliability: pd.Series,
) -> float:
    """Probability-weighted reliability for current regime mix."""
    common = current_probs.index.intersection(regime_reliability.index)
    p = current_probs.loc[common].astype(float).clip(lower=0.0)
    p = p / p.sum()
    r = regime_reliability.loc[common].astype(float)
    return float((p * r).sum())
```

## 9.16 Python: Stress-Adjusted Dynamic Conviction Scoring

```python
def stress_probability(
    current_probs: pd.Series,
    stress_regimes: Sequence[str],
) -> float:
    """Compute total probability assigned to stress regimes."""
    p = current_probs.astype(float).clip(lower=0.0)
    p = p / p.sum()
    stress = [r for r in stress_regimes if r in p.index]
    if not stress:
        return 0.0
    return float(p.loc[stress].sum())


def dynamic_conviction_scores(
    expected_returns: pd.Series,
    covariance: pd.DataFrame,
    current_probs: pd.Series,
    model_confidence: pd.Series,
    liquidity_score: pd.Series | None = None,
    regime_reliability: float | pd.Series = 1.0,
    stress_loss: pd.Series | None = None,
    stress_prob: float = 0.0,
    config: RegimeForecastConfig = RegimeForecastConfig(),
) -> pd.DataFrame:
    """Compute dynamic, regime-aware asset conviction scores."""
    assets = expected_returns.index
    vol = pd.Series(
        np.sqrt(np.diag(covariance.loc[assets, assets])),
        index=assets,
        name="expected_volatility",
    )
    mu = expected_returns.astype(float).rename("expected_return")

    if stress_loss is not None:
        loss = stress_loss.reindex(assets).fillna(0.0).abs()
        mu_adj = mu - config.stress_penalty * stress_prob * loss
    else:
        mu_adj = mu.copy()
    mu_adj.name = "stress_adjusted_return"

    conf = model_confidence.reindex(assets).fillna(0.0).clip(0.0, 1.0)
    conf.name = "model_confidence"

    if liquidity_score is None:
        liq = pd.Series(1.0, index=assets, name="liquidity_score")
    else:
        liq = liquidity_score.reindex(assets).fillna(0.0).clip(0.0, 1.0)
        liq.name = "liquidity_score"

    if isinstance(regime_reliability, pd.Series):
        rel = regime_reliability.reindex(assets).fillna(0.0).clip(0.0, 1.0)
    else:
        rel = pd.Series(float(regime_reliability), index=assets)
    rel.name = "regime_reliability"

    certainty = regime_certainty(current_probs)
    entropy_scale = config.entropy_floor + (1.0 - config.entropy_floor) * certainty

    raw = (mu_adj / vol.replace(0.0, np.nan)) * conf * liq * rel * entropy_scale
    conviction = np.tanh(raw / config.conviction_scale)
    conviction.name = "conviction"

    return pd.concat(
        [mu, mu_adj, vol, conf, liq, rel, conviction],
        axis=1,
    )
```

## 9.17 Python: End-to-End Synthetic Example

```python
# Synthetic demonstration only. Replace with point-in-time data in production.
rng = np.random.default_rng(42)
dates = pd.date_range("2005-01-31", periods=216, freq="M")
assets = ["Global_Equity", "Duration", "Credit", "Commodity", "USD"]
regimes = ["expansion", "slowdown", "inflation_shock", "liquidity_stress"]

# Synthetic regime probabilities.
raw_probs = pd.DataFrame(
    rng.gamma(shape=2.0, scale=1.0, size=(len(dates), len(regimes))),
    index=dates,
    columns=regimes,
)
regime_probs = raw_probs.div(raw_probs.sum(axis=1), axis=0)

# Synthetic forward returns with weak regime structure.
base = pd.DataFrame(
    rng.normal(0.002, 0.035, size=(len(dates), len(assets))),
    index=dates,
    columns=assets,
)
regime_effects = pd.DataFrame(
    {
        "Global_Equity": [0.015, -0.010, -0.015, -0.030],
        "Duration": [-0.004, 0.012, -0.020, 0.006],
        "Credit": [0.009, -0.008, -0.012, -0.035],
        "Commodity": [0.004, -0.006, 0.025, -0.010],
        "USD": [-0.003, 0.004, 0.008, 0.018],
    },
    index=regimes,
)
returns_fwd_3m = base.copy()
for r in regimes:
    returns_fwd_3m += regime_probs[r].to_numpy()[:, None] * regime_effects.loc[r]

cfg = RegimeForecastConfig(
    min_effective_obs=24,
    shrink_tau=36,
    covariance_shrinkage=0.35,
    entropy_floor=0.35,
    stress_penalty=0.40,
    conviction_scale=0.75,
)

regime_means = regime_conditioned_means(returns_fwd_3m, regime_probs, cfg)
regime_covs = regime_conditioned_covariances(returns_fwd_3m, regime_probs, cfg)

current_probs = regime_probs.iloc[-1]
mu_now = probability_weighted_mean_forecast(current_probs, regime_means)
cov_now = probability_weighted_covariance(
    current_probs,
    regime_covs,
    regime_means=regime_means,
    include_mean_dispersion=True,
)

model_conf = pd.Series(0.65, index=assets)
liq_score = pd.Series(
    {
        "Global_Equity": 1.00,
        "Duration": 0.95,
        "Credit": 0.80,
        "Commodity": 0.75,
        "USD": 0.90,
    }
)
stress_loss = pd.Series(
    {
        "Global_Equity": 0.18,
        "Duration": 0.06,
        "Credit": 0.14,
        "Commodity": 0.12,
        "USD": 0.04,
    }
)
p_stress = stress_probability(current_probs, ["liquidity_stress"])

conviction_table = dynamic_conviction_scores(
    expected_returns=mu_now,
    covariance=cov_now,
    current_probs=current_probs,
    model_confidence=model_conf,
    liquidity_score=liq_score,
    regime_reliability=0.70,
    stress_loss=stress_loss,
    stress_prob=p_stress,
    config=cfg,
)

print("Current regime probabilities:")
print(current_probs.round(3))
print("\nConviction table:")
print(conviction_table.round(4))
```

## 9.18 Visualization Code for Dynamic Convictions

```python
import matplotlib.pyplot as plt


def plot_regime_probabilities(regime_probs: pd.DataFrame) -> None:
    """Plot regime probability history."""
    fig, ax = plt.subplots(figsize=(10, 5))
    regime_probs.plot(ax=ax)
    ax.set_title("Filtered Regime Probabilities")
    ax.set_xlabel("Date")
    ax.set_ylabel("Probability")
    ax.set_ylim(0.0, 1.0)
    plt.tight_layout()
    plt.show()


def plot_conviction_table(conviction_table: pd.DataFrame) -> None:
    """Plot one-date conviction snapshot."""
    fig, ax = plt.subplots(figsize=(8, 4))
    conviction_table["conviction"].sort_values().plot(kind="barh", ax=ax)
    ax.axvline(0.0, linewidth=1)
    ax.set_title("Regime-Adjusted Conviction Snapshot")
    ax.set_xlabel("Conviction")
    plt.tight_layout()
    plt.show()


def plot_covariance_heatmap(covariance: pd.DataFrame) -> None:
    """Plot covariance matrix as a heatmap."""
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(covariance.to_numpy(), aspect="auto")
    ax.set_title("Probability-Weighted Covariance Matrix")
    ax.set_xticks(range(covariance.shape[1]))
    ax.set_xticklabels(covariance.columns, rotation=45, ha="right")
    ax.set_yticks(range(covariance.shape[0]))
    ax.set_yticklabels(covariance.index)
    fig.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.show()


plot_regime_probabilities(regime_probs)
plot_conviction_table(conviction_table)
plot_covariance_heatmap(cov_now)
```

## 9.19 Regime-Conditioned Validation

A regime-conditioned model must be validated against a regime-unaware benchmark. Important comparisons include:

| Validation Question | Diagnostic |
|---|---|
| Does regime conditioning improve return forecasts? | OOS $R^2$ versus unconditional model. |
| Does it improve risk forecasts? | Volatility forecast error and covariance stability. |
| Does it improve drawdown control? | Stress-period loss and expected shortfall. |
| Does it improve signal timing? | Regime-weighted IC and signal decay. |
| Does it reduce overtrading? | Turnover versus forecast improvement. |
| Does it create false confidence? | Entropy and forecast-dispersion diagnostics. |
| Does it survive real-time use? | Walk-forward filtered probabilities only. |

The validation should report separate results for $t+1$, $t+3$, and $t+12$. A regime model may improve $t+3$ risk control while adding little value to $t+1$ mean-return forecasts.

## 9.20 Common Failure Modes

| Failure Mode | Description | Control |
|---|---|---|
| Smoothed-probability leakage | Using ex-post regime probabilities in a backtest. | Use filtered probabilities only. |
| Sparse regimes | Rare regimes produce unstable means. | Effective sample size and shrinkage. |
| Overconfident hard labels | One label drives binary allocation. | Probability-weighted forecasts. |
| Regime narrative overfit | States are named after realized returns. | Label by feature profiles first. |
| Mean-return overfitting | Regime means are noisy. | Emphasize risk conditioning and shrinkage. |
| Covariance instability | Regime covariance is poorly estimated. | Shrinkage and stress covariance overlays. |
| Signal gating whipsaw | Hard gates turn signals on/off too often. | Soft scaling and turnover penalties. |
| Ignoring entropy | Ambiguous regimes still generate strong tilts. | Conviction decay by entropy. |
| Ignoring stress dispersion | Forecasts disagree across plausible regimes. | Penalize regime forecast dispersion. |
| Unvalidated complexity | Regime model adds no OOS value. | Benchmark against simple models. |

## 9.21 Practical Checklist

| Check | Requirement |
|---|---|
| Regime probabilities | Filtered, point-in-time, nonnegative, sum to one. |
| Regime labels | Based on feature profiles, not realized returns. |
| Return estimates | Shrunk by effective sample size. |
| Volatility estimates | Regime-conditioned and covariance-shrunk. |
| Signal reliability | Tested by regime and horizon. |
| Forecast combination | Probability-weighted, not hard-labeled. |
| Uncertainty penalty | Entropy and forecast dispersion included. |
| Stress adjustment | Stress-regime probability affects conviction. |
| Validation | Compared against regime-unaware benchmark. |
| Governance | Model version, data vintage, and run manifest stored. |

## 9.22 Part 9 Summary

Part 9 developed the regime-conditioned forecasting and dynamic conviction layer of the macro-regime research process. The main lessons are:

1. Regime conditioning should transform uncertain regime probabilities into expected returns, risk forecasts, signal reliability estimates, and portfolio-aware conviction scores.
2. Regime-conditioned expected returns should be probability-weighted and shrunk toward unconditional priors when effective sample size is low.
3. Regime-conditioned covariance often matters more reliably than regime-conditioned mean returns because risk and correlation states can change sharply.
4. Signal efficacy should be evaluated by regime and horizon; signals should usually be softly scaled rather than hard-gated.
5. Probability-weighted forecasts are preferable to binary regime labels because regimes are latent and uncertain.
6. Dynamic model averaging can combine macro, carry, trend, valuation, volatility, and machine-learning forecasts, but it must be benchmarked against equal-weight and simple alternatives.
7. Bayesian updating provides a coherent framework for updating regime probabilities as new macro and market evidence arrives.
8. Convictions should decay when regime entropy is high or when plausible regimes imply conflicting forecasts.
9. Stress-adjusted convictions penalize expected returns for stress-regime probability and estimated stress losses.
10. A complete dynamic conviction score should combine expected return, expected volatility, model confidence, regime reliability, liquidity, regime certainty, and stress adjustment.
11. Regime-conditioned models must be validated against regime-unaware benchmarks using walk-forward, point-in-time testing.

---

# Stop Point

This installment completes:

1. **Part 9: Regime-Conditioned Forecasting and Dynamic Convictions.**

Continue next with **Part 10: Portfolio Integration, Risk Budgets, and Allocation Inputs**.
