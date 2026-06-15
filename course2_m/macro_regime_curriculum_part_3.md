# Institutional Macro-Regime Detection, Multi-Asset Signal Identification, and Statistical Validation Curriculum

## Installment 3: Part 3 - Multi-Asset Return Modeling Across Horizons

**Scope of this installment.** This installment continues the curriculum with **Part 3 only**. It assumes the global assumptions, timestamp conventions, feature-engineering conventions, and forward-return alignment rules established in Installments 1 and 2.

**Educational boundary.** This document is for research education, model design, and institutional portfolio-process development. It is not personalized investment advice, a live trading recommendation, or a guarantee of alpha.

---

# Part 3: Multi-Asset Return Modeling Across Horizons

## 3.1 Purpose of Multi-Asset Return Modeling

Multi-asset return modeling converts point-in-time features into horizon-specific forecasts for asset returns, excess returns, relative returns, downside risk, and risk-adjusted opportunities. In a macro-regime research process, return modeling sits between feature engineering and portfolio construction. It answers the question: **given the information set available at time $t$, what distribution of outcomes should be expected for asset $i$ over horizon $h$?**

The general forecasting object is:

$$
Y_{i,t,h}=g\left(R_{i,t\rightarrow t+h}, R_{b,t\rightarrow t+h}, R_{c,t\rightarrow t+h}, \sigma_{i,t\rightarrow t+h}, D_{i,t\rightarrow t+h}\right),
$$

where $Y_{i,t,h}$ is the target variable for asset $i$ at decision timestamp $t$ and horizon $h$, $R_{i,t\rightarrow t+h}$ is the cumulative asset return, $R_{b,t\rightarrow t+h}$ is a benchmark return, $R_{c,t\rightarrow t+h}$ is a cash return, $\sigma_{i,t\rightarrow t+h}$ is realized horizon volatility, and $D_{i,t\rightarrow t+h}$ is a downside or drawdown measure.

The model produces a forecast:

$$
\hat{Y}_{i,t,h}=\mathcal{M}_{h}\left(\mathcal{F}_t, i; \hat\theta_{t,h}\right),
$$

where $\mathcal{M}_{h}$ is the horizon-specific forecasting model, $\mathcal{F}_t$ is the information set available at $t$, and $\hat\theta_{t,h}$ are model parameters estimated using only information available before or at $t$.

A strong institutional process treats the model output as uncertain. The goal is not only to estimate a point forecast $\hat{Y}_{i,t,h}$, but also to estimate forecast uncertainty, stability, calibration, sensitivity to regimes, and implementation relevance.

## 3.2 Modeling Targets: What Is Being Forecast?

Return modeling begins with target definition. A model can forecast absolute returns, excess returns, relative returns, probabilities, quantiles, or full distributions.

| Target Type | Formula | Interpretation | Typical Use |
|---|---:|---|---|
| Absolute cumulative return | $R_{i,t,h}$ | Total return of asset $i$ over horizon $h$. | Strategic and tactical expected return. |
| Excess return over cash | $R^e_{i,t,h}=R_{i,t,h}-R_{c,t,h}$ | Compensation above cash. | Asset allocation and Sharpe estimation. |
| Active return versus benchmark | $R^a_{i,t,h}=R_{i,t,h}-R_{b,t,h}$ | Outperformance versus benchmark $b$. | Active allocation and ranking. |
| Positive-return indicator | $\mathbf{1}\{R_{i,t,h}>0\}$ | Whether return is positive. | Directional probability model. |
| Outperformance indicator | $\mathbf{1}\{R_{i,t,h}>R_{b,t,h}\}$ | Whether asset beats benchmark. | Cross-asset selection. |
| Downside indicator | $\mathbf{1}\{R_{i,t,h}<L\}$ | Whether return falls below threshold $L$. | Risk management and drawdown control. |
| Quantile target | $Q_\tau(R_{i,t,h}\mid\mathcal{F}_t)$ | Conditional tail or median return. | Downside-aware forecasting. |
| Expected shortfall | $\mathbb{E}[R_{i,t,h}\mid R_{i,t,h}\leq q_\alpha]$ | Expected loss conditional on tail event. | Stress-aware allocation. |
| Expected Sharpe | $\mu^e_{i,t,h}/\sigma_{i,t,h}$ | Risk-adjusted expected return. | Risk budgeting. |

A target must specify four conventions:

1. **Horizon.** $h\in\{1,3,12\}$ months.
2. **Compounding.** Arithmetic cumulative return, log cumulative return, or annualized return.
3. **Benchmark.** Cash, global benchmark, asset-class benchmark, or no benchmark.
4. **Currency basis.** Local, base-currency unhedged, or base-currency hedged.

## 3.3 Horizon-Specific Modeling Logic

The same feature can have different implications across horizons. A volatility spike may be mean-reverting over $t+1$, a credit-spread widening impulse may indicate drawdown risk over $t+3$, and valuation may matter more over $t+12$. Therefore, the model should usually be horizon-specific:

$$
\hat{Y}_{i,t,h}=\mathcal{M}_{h}(X_{i,t}),
\qquad h\in\{1,3,12\},
$$

where $X_{i,t}$ is a vector of point-in-time macro, market, asset-specific, and regime features.

| Horizon | Typical Signal Emphasis | Statistical Challenge | Portfolio Interpretation |
|---:|---|---|---|
| $t+1$ | Momentum, volatility, sentiment, positioning, macro surprises. | Low signal-to-noise, high turnover. | Tactical tilt or risk-control overlay. |
| $t+3$ | Macro momentum, credit impulse, liquidity tightening, trend, carry. | Overlapping targets and changing regimes. | Tactical allocation and risk-budget adjustment. |
| $t+12$ | Valuation, policy stance, yield curve, credit compensation, structural macro. | Small effective sample and regime breaks. | Strategic tilts, capital-market assumptions, scenario planning. |

A useful principle is to match the economic half-life of the feature to the forecast horizon. Fast-moving features should not automatically be forced into $t+12$ forecasts, and slow-moving valuation features should not be judged only on $t+1$ noise.

## 3.4 Multi-Asset Return Definitions Across Asset Classes

### 3.4.1 Equities, Sectors, Countries, and Styles

For equity asset $i$, the preferred monthly return is total return:

$$
r^{\mathrm{eq}}_{i,t}=\frac{TRI_{i,t}}{TRI_{i,t-1}}-1,
$$

where $TRI_{i,t}$ is the total return index. Equity forecasts may be driven by earnings revisions, valuation, real rates, inflation, margins, sentiment, liquidity, and regime probabilities.

A stylized equity return decomposition is:

$$
R^{\mathrm{eq}}_{i,t,h}\approx \Delta \log E_{i,t,h}+\Delta \log M_{i,t,h}+D_{i,t,h},
$$

where $\Delta \log E$ is earnings growth, $\Delta \log M$ is valuation multiple change, and $D$ is dividend contribution. This decomposition is approximate and does not fully capture buybacks, currency translation, sector composition, or index rebalancing.

### 3.4.2 Sovereign Rates and Duration

A duration asset return can be approximated by carry, roll-down, duration exposure, and convexity:

$$
R^{\mathrm{dur}}_{i,t,h}\approx \mathrm{Carry}_{i,t,h}+\mathrm{RollDown}_{i,t,h}-D_{i,t}\Delta y_{i,t,h}+\frac{1}{2}C_{i,t}(\Delta y_{i,t,h})^2,
$$

where $D_{i,t}$ is modified duration, $C_{i,t}$ is convexity, and $\Delta y_{i,t,h}$ is the yield change over the horizon. Forecasts may use growth slowdown features, inflation momentum, real-rate changes, central-bank reaction functions, yield-curve slope, and recession-risk indicators.

### 3.4.3 Credit

Credit returns combine rate exposure, spread exposure, carry, default risk, and liquidity risk:

$$
R^{\mathrm{credit}}_{i,t,h}\approx \mathrm{Carry}_{i,t,h}
-D^{\mathrm{rate}}_{i,t}\Delta y_{t,h}
-D^{\mathrm{spread}}_{i,t}\Delta s_{i,t,h}
-\mathrm{DefaultLoss}_{i,t,h}
-\mathrm{LiquidityCost}_{i,t,h}.
$$

Credit forecasting requires separating two effects. High spreads can imply attractive carry over longer horizons, while spread widening can signal near-term stress. The level and impulse of spreads can therefore have opposite signs depending on horizon.

### 3.4.4 FX

For base currency $B$ and foreign currency $F$, the FX return is:

$$
R^{FX}_{F/B,t,h}=\frac{S_{F/B,t+h}}{S_{F/B,t}}-1,
$$

where $S_{F/B}$ is units of base currency per unit of foreign currency. FX forecasts may use carry, real-rate differentials, external balances, terms of trade, commodity exposure, risk sentiment, valuation, and dollar liquidity.

A simple FX carry feature is:

$$
\mathrm{Carry}^{FX}_{F/B,t}=i_{F,t}-i_{B,t},
$$

where $i_F$ and $i_B$ are short rates. Carry is not a riskless forecast; it can be compensation for crash risk, external vulnerability, liquidity risk, or policy risk.

### 3.4.5 Commodities and Futures

A collateralized commodity futures return may be decomposed as:

$$
R^{\mathrm{fut}}_{i,t,h}=R^{\mathrm{spot}}_{i,t,h}+R^{\mathrm{roll}}_{i,t,h}+R^{\mathrm{collateral}}_{t,h}-\mathrm{Costs}_{i,t,h}.
$$

Commodity forecasts may use futures curve shape, inventories, growth momentum, inflation pressure, real rates, dollar strength, seasonality, and geopolitical supply constraints. For futures, the model should distinguish spot-price forecast from roll-yield forecast.

### 3.4.6 Options, Volatility, and Derivative Strategies

Option strategy returns require explicit construction. A one-month strategy return can be written as:

$$
R^{\mathrm{opt}}_{i,t,1}=\frac{V_{i,t+1}-V_{i,t}-\mathrm{TC}_{i,t,t+1}+\mathrm{CollateralIncome}_{t,t+1}}{\mathrm{Capital}_{i,t}},
$$

where $V$ is strategy value, $\mathrm{TC}$ is transaction cost, and $\mathrm{Capital}$ is the chosen capital base. Forecasting option strategy returns often requires implied volatility, realized volatility, variance risk premium, skew, term structure, delta-hedging assumptions, margin, and path dependency.

### 3.4.7 Alternative Risk Premia

Alternative risk premia such as trend, carry, value, merger arbitrage, equity market neutral, volatility carry, and risk parity should be modeled as strategy return streams. These returns may contain leverage, financing, embedded short-option exposure, liquidity risk, and nonlinear drawdown profiles. A monthly model should not treat them as simple unlevered asset classes unless the return series is explicitly defined that way.

## 3.5 Single-Asset Time-Series Forecasting

The simplest predictive model estimates one asset at a time. For asset $i$ and horizon $h$:

$$
Y_{i,t,h}=\alpha_{i,h}+\beta_{i,h}^{\top}X_t+\varepsilon_{i,t,h},
$$

where $Y_{i,t,h}$ is the target, $X_t$ is the feature vector available at time $t$, $\alpha_{i,h}$ is an intercept, $\beta_{i,h}$ is a coefficient vector, and $\varepsilon_{i,t,h}$ is the forecast error.

A univariate predictive regression is:

$$
Y_{i,t,h}=\alpha_{i,h}+\beta_{i,h}z_t+\varepsilon_{i,t,h},
$$

where $z_t$ is a single macro or market signal.

**Interpretation.** If $Y$ is a $t+3$ excess return and $z_t$ is a standardized credit-spread impulse, then $\beta<0$ means that credit spread widening is associated with lower future excess returns for the asset over the next three months.

**Main advantage.** The model is interpretable and easy to validate.

**Main weakness.** It ignores cross-asset information sharing and may be unstable for assets with limited histories.

## 3.6 Cross-Sectional Asset Ranking

Cross-sectional models compare assets at the same timestamp. Let $S_{i,t}$ be a signal score for asset $i$ at time $t$. A rank-based forecast can be written as:

$$
\mathrm{RankScore}_{i,t}=\frac{\mathrm{rank}_t(S_{i,t})-1}{N_t-1},
$$

where $N_t$ is the number of tradable assets in the point-in-time universe and ranks are computed only across $\mathcal{U}_t$.

A cross-sectional predictive equation is:

$$
Y_{i,t,h}=\alpha_t+\beta_h S_{i,t}+\varepsilon_{i,t,h},
\qquad i\in\mathcal{U}_t.
$$

Here $\alpha_t$ is a time fixed effect that captures the common return environment in month $t$. The coefficient $\beta_h$ measures whether assets with higher signal scores outperform lower-scored assets over horizon $h$.

Cross-sectional modeling is useful for country allocation, sector rotation, style tilts, FX ranking, commodity futures ranking, and multi-asset relative allocation. It is less useful when the universe is very small or when assets are not comparable.

## 3.7 Panel Regression and Pooled Models

A panel model pools assets and time:

$$
Y_{i,t,h}=\alpha_i+\delta_t+\beta_h^{\top}X_{i,t}+\varepsilon_{i,t,h},
$$

where $\alpha_i$ is an asset fixed effect, $\delta_t$ is a time fixed effect, and $X_{i,t}$ may include asset-specific signals, macro variables, and interactions.

A macro-interaction panel model is:

$$
Y_{i,t,h}=\alpha_i+\beta_h^{\top}Z_t+\gamma_h^{\top}A_{i,t}+\eta_h^{\top}(Z_t\otimes A_{i,t})+\varepsilon_{i,t,h},
$$

where $Z_t$ is a macro feature vector, $A_{i,t}$ is an asset-specific exposure vector, and $Z_t\otimes A_{i,t}$ represents interactions. For example, an asset with high duration exposure may respond more negatively to a real-rate shock.

Panel models can improve sample efficiency, but they introduce complications:

1. Errors may be correlated across assets at the same timestamp.
2. Errors may be serially correlated because of overlapping targets.
3. Asset histories may begin at different dates.
4. The model may impose common slopes that are economically inappropriate.
5. Cross-sectional dependence can overstate statistical significance if ignored.

Robust inference may require clustering by time, clustering by asset, two-way clustering, Newey-West style corrections, or block bootstrap methods.

## 3.8 Direct Horizon Forecasting Versus Recursive Forecasting

There are two common approaches to multi-horizon forecasting.

### 3.8.1 Direct Forecasting

Direct forecasting estimates a separate model for each horizon:

$$
Y_{i,t,h}=\alpha_{i,h}+\beta_{i,h}^{\top}X_t+\varepsilon_{i,t,h}.
$$

This is usually preferred for macro allocation because the relationship between features and returns may differ across $t+1$, $t+3$, and $t+12$.

### 3.8.2 Recursive Forecasting

Recursive forecasting models the one-month return and compounds expected one-month forecasts:

$$
\hat R_{i,t,3}^{\mathrm{rec}}=\prod_{j=1}^{3}(1+\hat r_{i,t+j\mid t})-1.
$$

The challenge is that $\hat r_{i,t+j\mid t}$ requires forecasting future features or assuming current features persist. Recursive forecasting can be useful in dynamic state-space models, but it can accumulate model error.

| Approach | Advantage | Disadvantage | Recommended Use |
|---|---|---|---|
| Direct | Horizon-specific and simple alignment. | Overlapping targets reduce effective sample. | Baseline for $t+1$, $t+3$, $t+12$. |
| Recursive | Dynamically consistent path forecasts. | Requires future feature dynamics. | Scenario models and state-space systems. |
| Hybrid | Combines direct targets with state forecasts. | More complex governance. | Regime-conditioned forecasting. |

## 3.9 Compound Forward Return Modeling

For arithmetic returns, the $h$-month target is:

$$
R_{i,t,h}=\prod_{j=1}^{h}(1+r_{i,t+j})-1.
$$

For log returns:

$$
G_{i,t,h}=\sum_{j=1}^{h}g_{i,t+j}.
$$

A linear model on log cumulative returns is often numerically convenient:

$$
G_{i,t,h}=\alpha_{i,h}+\beta_{i,h}^{\top}X_t+\varepsilon_{i,t,h}.
$$

The implied arithmetic forecast is:

$$
\widehat{R}_{i,t,h}=\exp\left(\widehat{G}_{i,t,h}+\frac{1}{2}\hat\sigma^2_{\varepsilon,i,h}\right)-1,
$$

where $\hat\sigma^2_{\varepsilon,i,h}$ is the residual variance under a lognormal approximation. The $\frac{1}{2}\sigma^2$ adjustment is model-dependent and should not be used blindly when residuals are fat-tailed or skewed.

## 3.10 Regression, Classification, Quantile, and Distributional Forecasting

### 3.10.1 Linear Regression for Expected Returns

A multivariate predictive regression is:

$$
Y_{i,t,h}=\alpha_{i,h}+\sum_{m=1}^{M}\beta_{i,m,h}x_{m,t}+\varepsilon_{i,t,h}.
$$

The forecast is:

$$
\hat Y_{i,t,h}=\hat\alpha_{i,h}+\sum_{m=1}^{M}\hat\beta_{i,m,h}x_{m,t}.
$$

Linear regression is transparent, but monthly macro samples can make coefficients unstable when $M$ is large.

### 3.10.2 Logistic Probability Model

For probability of positive return, define:

$$
D_{i,t,h}^{+}=\mathbf{1}\{R_{i,t,h}>0\}.
$$

A logistic model is:

$$
\Pr(D_{i,t,h}^{+}=1\mid X_t)=\frac{1}{1+\exp[-(\alpha_{i,h}+\beta_{i,h}^{\top}X_t)]}.
$$

This produces a probability forecast, but it must be calibrated and validated. A model that predicts 60% probability should realize positive outcomes approximately 60% of the time in comparable forecast buckets.

### 3.10.3 Quantile Regression

A quantile regression estimates the conditional quantile $Q_\tau(Y\mid X)$:

$$
Q_\tau(Y_{i,t,h}\mid X_t)=\alpha_{i,h,\tau}+\beta_{i,h,\tau}^{\top}X_t.
$$

The estimator solves:

$$
\min_{\alpha,\beta}\sum_t \rho_\tau\left(Y_{i,t,h}-\alpha-\beta^{\top}X_t\right),
$$

where the check loss is:

$$
\rho_\tau(u)=u(\tau-\mathbf{1}\{u<0\}).
$$

Quantile models are useful for downside probability, tail-aware allocation, and stress testing.

### 3.10.4 Distributional Forecasting

A distributional model estimates the full conditional distribution:

$$
F_{i,t,h}(y)=\Pr(Y_{i,t,h}\leq y\mid\mathcal{F}_t).
$$

From this distribution, the researcher can compute:

$$
\mathbb{E}_t[Y_{i,t,h}], \quad
\Pr_t(Y_{i,t,h}>0), \quad
Q_{\alpha,t}(Y_{i,t,h}), \quad
ES_{\alpha,t}(Y_{i,t,h}).
$$

Distributional forecasting is more informative than point forecasting, but it requires stronger assumptions, more validation, and careful calibration.

## 3.11 Expected Return, Downside Probability, and Expected Shortfall

Suppose the model provides a conditional normal approximation:

$$
Y_{i,t,h}\mid\mathcal{F}_t\sim \mathcal{N}(\mu_{i,t,h},\sigma^2_{i,t,h}).
$$

The probability of a positive return is:

$$
\Pr(Y_{i,t,h}>0\mid\mathcal{F}_t)=\Phi\left(\frac{\mu_{i,t,h}}{\sigma_{i,t,h}}\right),
$$

where $\Phi$ is the standard normal cumulative distribution function.

The probability of a loss below threshold $L$ is:

$$
\Pr(Y_{i,t,h}<L\mid\mathcal{F}_t)=\Phi\left(\frac{L-\mu_{i,t,h}}{\sigma_{i,t,h}}\right).
$$

The expected shortfall at lower-tail probability $\alpha$ is:

$$
ES_{\alpha,i,t,h}=\mu_{i,t,h}-\sigma_{i,t,h}\frac{\phi(z_\alpha)}{\alpha},
$$

where $z_\alpha=\Phi^{-1}(\alpha)$ and $\phi$ is the standard normal density. This formula assumes conditional normality, which can be poor for credit, options, volatility strategies, commodities, and crisis-sensitive assets. Empirical or bootstrap-based expected shortfall is often more robust.

## 3.12 Expected Sharpe Forecasting

Expected Sharpe for asset $i$ over horizon $h$ is:

$$
\widehat{SR}_{i,t,h}=\frac{\hat\mu^e_{i,t,h}}{\hat\sigma_{i,t,h}},
$$

where $\hat\mu^e_{i,t,h}$ is expected excess return and $\hat\sigma_{i,t,h}$ is expected horizon volatility. If $\hat\mu^e$ and $\hat\sigma$ are horizon returns, the Sharpe is horizon-specific. A monthly Sharpe may be annualized as:

$$
\widehat{SR}_{i,t,h}^{ann}\approx \widehat{SR}_{i,t,h}\sqrt{\frac{12}{h}},
$$

under the simplifying assumption of independent returns. This assumption is often weak for overlapping returns, trend strategies, credit, and option strategies.

Expected Sharpe forecasts are highly sensitive to small expected-return estimates. A practical approach shrinks expected returns before computing Sharpe:

$$
\tilde\mu^e_{i,t,h}=\kappa_{i,t,h}\hat\mu^e_{i,t,h},
\qquad 0\leq\kappa_{i,t,h}\leq 1,
$$

where $\kappa$ is a confidence or shrinkage factor based on estimation uncertainty, model stability, signal breadth, and regime uncertainty.

## 3.13 Forecast Uncertainty and Shrinkage

Because expected returns are noisy, forecast shrinkage is central to institutional practice. A simple shrinkage estimator is:

$$
\tilde\mu_{i,t,h}=\kappa_{i,t,h}\hat\mu_{i,t,h}+(1-\kappa_{i,t,h})\mu_{i,h}^{0},
$$

where $\mu^0$ is a prior or baseline expected return and $\kappa$ is the confidence weight. A baseline may be historical average, carry, equilibrium return, risk-premium estimate, or zero active return.

One possible confidence weight is:

$$
\kappa_{i,t,h}=\frac{\widehat{\mathrm{Var}}(\mu^0_{i,h})}{\widehat{\mathrm{Var}}(\mu^0_{i,h})+\widehat{\mathrm{Var}}(\hat\mu_{i,t,h})},
$$

which resembles Bayesian precision weighting. When model forecast uncertainty is high, $\kappa$ falls and the forecast moves toward the prior.

A practical conviction system can also cap forecast magnitudes:

$$
\tilde\mu_{i,t,h}^{cap}=\max\left(\min(\tilde\mu_{i,t,h}, U_{i,h}), L_{i,h}\right),
$$

where $U$ and $L$ are upper and lower bounds based on historical distributions, scenario analysis, and governance rules.

## 3.14 Model Families for Multi-Asset Forecasting

| Model Family | Output | Strength | Weakness | Best Use |
|---|---|---|---|---|
| Historical average | Expected return | Simple benchmark. | Slow to adapt. | Baseline prior. |
| Carry model | Expected return | Economically interpretable. | Crash risk and structural shifts. | Bonds, FX, credit, commodities. |
| Linear regression | Expected return | Transparent and testable. | Coefficient instability. | Parsimonious signal models. |
| Logistic regression | Probability | Directional probability. | Calibration risk. | Hit-rate and outperformance forecasts. |
| Quantile regression | Conditional quantile | Tail awareness. | Noisy in small samples. | Downside and stress forecasts. |
| Panel regression | Expected or active return | Shares information across assets. | Cross-sectional dependence. | Country, sector, FX, commodities. |
| Regularized regression | Expected return | Controls overfitting. | Hyperparameter uncertainty. | Many correlated features. |
| Tree models | Nonlinear forecasts | Captures interactions. | Overfit risk in monthly data. | Carefully constrained nonlinear models. |
| Bayesian model | Distribution | Priors and uncertainty. | Computational and governance burden. | Macro uncertainty and shrinkage. |
| Ensemble | Combined forecast | Diversifies model risk. | Can hide model weakness. | Production forecast blending. |

## 3.15 Baseline Models and Forecast Benchmarks

Every sophisticated model should be compared to simple baselines. Common baselines include:

1. **Zero active return:** $\hat R^a_{i,t,h}=0$.
2. **Historical mean:** $\hat R_{i,t,h}=\bar R_{i,h,t}^{exp}$ using expanding historical averages.
3. **Carry-only forecast:** expected carry or yield-based return.
4. **Random-walk forecast:** no expected price change, only income and roll.
5. **Equal-score cross-sectional forecast:** all assets receive the same active forecast.
6. **Regime-unaware model:** the same model without regime conditioning.

A forecast model has practical value only if it improves upon relevant baselines out of sample after costs, uncertainty, and risk constraints are considered.

## 3.16 Forecast Evaluation Metrics Introduced Here

Detailed inference is covered later, but Part 3 requires defining the metrics that connect forecasts to validation.

For point forecasts, mean squared error is:

$$
MSE_h=\frac{1}{T}\sum_{t=1}^{T}(Y_{t,h}-\hat Y_{t,h})^2.
$$

Mean absolute error is:

$$
MAE_h=\frac{1}{T}\sum_{t=1}^{T}|Y_{t,h}-\hat Y_{t,h}|.
$$

Out-of-sample $R^2$ versus benchmark forecast $\hat Y^0$ is:

$$
R^2_{OOS,h}=1-\frac{\sum_t(Y_{t,h}-\hat Y_{t,h})^2}{\sum_t(Y_{t,h}-\hat Y^0_{t,h})^2}.
$$

For probability forecasts $\hat p_t$, the Brier score is:

$$
\mathrm{Brier}=\frac{1}{T}\sum_{t=1}^{T}(D_t-\hat p_t)^2,
$$

where $D_t\in\{0,1\}$ is the realized event indicator.

For cross-sectional forecasts, rank information coefficient is:

$$
RIC_t=\mathrm{corr}_{\mathrm{Spearman}}\left(\hat S_{i,t},Y_{i,t,h}\right)_{i\in\mathcal{U}_t}.
$$

The average rank IC is:

$$
\overline{RIC}=\frac{1}{T}\sum_{t=1}^{T}RIC_t.
$$

## 3.17 Python: Horizon-Specific Forward Return Targets

The following code uses synthetic-compatible functions and can be integrated with the alignment utilities from earlier installments.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class TargetConfig:
    """Configuration for multi-horizon return targets.

    Parameters
    ----------
    horizons : tuple[int, ...]
        Forecast horizons in months.
    return_type : str
        One of {'arithmetic', 'log'}.
    target_type : str
        One of {'absolute', 'excess_cash', 'active_benchmark'}.
    """

    horizons: tuple[int, ...] = (1, 3, 12)
    return_type: str = "arithmetic"
    target_type: str = "absolute"


def validate_returns_frame(returns: pd.DataFrame, name: str = "returns") -> None:
    """Validate a monthly returns DataFrame."""
    if not isinstance(returns, pd.DataFrame):
        raise TypeError(f"{name} must be a pandas DataFrame.")
    if not isinstance(returns.index, pd.DatetimeIndex):
        raise TypeError(f"{name} must have a DatetimeIndex.")
    if not returns.index.is_monotonic_increasing:
        raise ValueError(f"{name} index must be sorted.")
    if returns.index.has_duplicates:
        raise ValueError(f"{name} index has duplicates.")


def forward_cumulative_returns(
    returns: pd.DataFrame,
    horizons: Sequence[int] = (1, 3, 12),
    *,
    return_type: str = "arithmetic",
) -> dict[int, pd.DataFrame]:
    """Compute forward cumulative returns from monthly returns.

    Row t contains the realized future return from t+1 through t+h.
    """
    validate_returns_frame(returns)
    out: dict[int, pd.DataFrame] = {}

    for h in horizons:
        if h < 1:
            raise ValueError("horizons must be positive integers.")
        if return_type == "arithmetic":
            gross = pd.DataFrame(1.0, index=returns.index, columns=returns.columns)
            for j in range(1, h + 1):
                gross *= 1.0 + returns.shift(-j)
            out[h] = gross - 1.0
        elif return_type == "log":
            out[h] = sum(returns.shift(-j) for j in range(1, h + 1))
        else:
            raise ValueError("return_type must be 'arithmetic' or 'log'.")

    return {h: df.replace([np.inf, -np.inf], np.nan) for h, df in out.items()}


def make_excess_or_active_targets(
    asset_fwd: dict[int, pd.DataFrame],
    cash_fwd: dict[int, pd.Series] | None = None,
    benchmark_fwd: dict[int, pd.Series] | None = None,
    *,
    target_type: str = "absolute",
) -> dict[int, pd.DataFrame]:
    """Convert absolute forward returns into excess or active targets."""
    if target_type == "absolute":
        return asset_fwd

    adjusted: dict[int, pd.DataFrame] = {}
    for h, y in asset_fwd.items():
        if target_type == "excess_cash":
            if cash_fwd is None or h not in cash_fwd:
                raise ValueError(f"Missing cash forward return for horizon {h}.")
            adjusted[h] = y.sub(cash_fwd[h], axis=0)
        elif target_type == "active_benchmark":
            if benchmark_fwd is None or h not in benchmark_fwd:
                raise ValueError(f"Missing benchmark forward return for horizon {h}.")
            adjusted[h] = y.sub(benchmark_fwd[h], axis=0)
        else:
            raise ValueError("Unknown target_type.")
    return adjusted
```

## 3.18 Python: Asset-Level Predictive Regression for t+1, t+3, and t+12

This example estimates separate linear models for each asset and horizon using expanding-window walk-forward estimation. It uses only past data to fit each forecast.

```python
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error


def make_supervised_panel(
    features: pd.DataFrame,
    targets: dict[int, pd.DataFrame],
    asset: str,
) -> dict[int, pd.DataFrame]:
    """Join feature matrix with one asset's horizon-specific targets."""
    if asset not in next(iter(targets.values())).columns:
        raise KeyError(f"Asset {asset} not found in targets.")

    out = {}
    for h, ydf in targets.items():
        joined = features.join(ydf[[asset]].rename(columns={asset: "target"}), how="inner")
        out[h] = joined.replace([np.inf, -np.inf], np.nan)
    return out


def expanding_window_forecast(
    data: pd.DataFrame,
    feature_cols: list[str],
    *,
    min_train: int = 60,
    alpha: float = 10.0,
) -> pd.DataFrame:
    """Generate expanding-window Ridge forecasts for one asset/horizon.

    Parameters
    ----------
    data : pd.DataFrame
        Contains feature columns and a column named 'target'.
    feature_cols : list[str]
        Point-in-time feature names.
    min_train : int
        Minimum number of historical observations before forecasting starts.
    alpha : float
        Ridge penalty. Larger values shrink coefficients more strongly.
    """
    required = set(feature_cols + ["target"])
    missing = required - set(data.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")

    clean = data[feature_cols + ["target"]].dropna().copy()
    if len(clean) <= min_train:
        raise ValueError("Not enough observations for the requested min_train.")

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("ridge", Ridge(alpha=alpha, fit_intercept=True)),
        ]
    )

    forecasts = []
    for loc in range(min_train, len(clean)):
        train = clean.iloc[:loc]
        test = clean.iloc[[loc]]
        model.fit(train[feature_cols], train["target"])
        pred = float(model.predict(test[feature_cols])[0])
        forecasts.append(
            {
                "date": test.index[0],
                "forecast": pred,
                "actual": float(test["target"].iloc[0]),
            }
        )

    result = pd.DataFrame(forecasts).set_index("date")
    result["error"] = result["actual"] - result["forecast"]
    return result


def evaluate_point_forecasts(forecast_df: pd.DataFrame) -> dict[str, float]:
    """Evaluate point forecasts using MSE, MAE, correlation, and sign hit rate."""
    y = forecast_df["actual"].astype(float)
    yhat = forecast_df["forecast"].astype(float)
    benchmark = pd.Series(y.expanding().mean().shift(1), index=y.index).fillna(0.0)

    mse_model = mean_squared_error(y, yhat)
    mse_bench = mean_squared_error(y, benchmark)
    oos_r2 = 1.0 - mse_model / mse_bench if mse_bench > 0 else np.nan

    return {
        "mse": float(mse_model),
        "mae": float(mean_absolute_error(y, yhat)),
        "forecast_actual_corr": float(y.corr(yhat)),
        "sign_hit_rate": float((np.sign(yhat) == np.sign(y)).mean()),
        "oos_r2_vs_expanding_mean": float(oos_r2),
    }
```

## 3.19 Python: Synthetic Example for Multi-Horizon Forecasting

```python
# Synthetic demonstration only. Replace with point-in-time features and real asset returns.
rng = np.random.default_rng(123)
dates = pd.date_range("2000-01-31", periods=240, freq="M")

features = pd.DataFrame(
    {
        "growth_score": rng.normal(size=len(dates)).cumsum() / 10,
        "inflation_score": rng.normal(size=len(dates)).cumsum() / 12,
        "credit_stress_score": rng.normal(size=len(dates)).cumsum() / 8,
        "liquidity_tightening_score": rng.normal(size=len(dates)).cumsum() / 9,
    },
    index=dates,
)

# Standardize with historical-only expanding estimates for the synthetic example.
features = (features - features.shift(1).expanding(36).mean()) / features.shift(1).expanding(36).std()

asset_returns = pd.DataFrame(
    rng.normal(0.004, 0.035, size=(len(dates), 4)),
    index=dates,
    columns=["Global_Equity", "Duration", "Credit", "Commodities"],
)

# Add a weak synthetic relationship so the example has structure.
asset_returns["Global_Equity"] += 0.006 * features["growth_score"].fillna(0) - 0.005 * features["credit_stress_score"].fillna(0)
asset_returns["Duration"] += -0.004 * features["inflation_score"].fillna(0) - 0.003 * features["growth_score"].fillna(0)

fwd_targets = forward_cumulative_returns(asset_returns, horizons=(1, 3, 12))
feature_cols = list(features.columns)

asset_data = make_supervised_panel(features, fwd_targets, asset="Global_Equity")
results = {}
for h, df in asset_data.items():
    fcst = expanding_window_forecast(df, feature_cols, min_train=72, alpha=20.0)
    results[h] = {
        "forecasts": fcst,
        "metrics": evaluate_point_forecasts(fcst),
    }
    print(f"Horizon {h} months:", results[h]["metrics"])
```

## 3.20 Python: Probability of Positive Return and Downside Probability

```python
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import calibration_curve


def expanding_logistic_probability_forecast(
    data: pd.DataFrame,
    feature_cols: list[str],
    *,
    threshold: float = 0.0,
    min_train: int = 72,
    C: float = 0.5,
) -> pd.DataFrame:
    """Forecast probability that target exceeds a threshold.

    Uses expanding-window logistic regression with scaling fit only on the
    training sample inside each window.
    """
    clean = data[feature_cols + ["target"]].dropna().copy()
    clean["event"] = (clean["target"] > threshold).astype(int)

    if clean["event"].nunique() < 2:
        raise ValueError("The event indicator has only one class.")

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("logit", LogisticRegression(C=C, penalty="l2", solver="lbfgs")),
        ]
    )

    rows = []
    for loc in range(min_train, len(clean)):
        train = clean.iloc[:loc]
        test = clean.iloc[[loc]]
        if train["event"].nunique() < 2:
            continue
        model.fit(train[feature_cols], train["event"])
        p = float(model.predict_proba(test[feature_cols])[0, 1])
        rows.append(
            {
                "date": test.index[0],
                "probability": p,
                "event": int(test["event"].iloc[0]),
                "actual": float(test["target"].iloc[0]),
            }
        )

    out = pd.DataFrame(rows).set_index("date")
    out["brier_error"] = (out["event"] - out["probability"]) ** 2
    return out


def probability_metrics(prob_df: pd.DataFrame) -> dict[str, float]:
    """Evaluate probability forecasts."""
    p = prob_df["probability"].clip(1e-6, 1 - 1e-6)
    y = prob_df["event"]
    log_loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
    return {
        "brier_score": float(np.mean((y - p) ** 2)),
        "log_loss": float(log_loss),
        "average_predicted_probability": float(p.mean()),
        "realized_event_frequency": float(y.mean()),
    }

# Example: probability that Global Equity has positive t+3 return.
prob_fcst = expanding_logistic_probability_forecast(asset_data[3], feature_cols, threshold=0.0)
print(probability_metrics(prob_fcst))
```

## 3.21 Python: Quantile Regression for Downside Forecasts

```python
import statsmodels.api as sm


def expanding_quantile_forecast(
    data: pd.DataFrame,
    feature_cols: list[str],
    *,
    quantile: float = 0.10,
    min_train: int = 72,
) -> pd.DataFrame:
    """Expanding-window quantile regression forecast.

    The forecast is the conditional quantile of the target distribution.
    """
    if not 0 < quantile < 1:
        raise ValueError("quantile must lie between 0 and 1.")

    clean = data[feature_cols + ["target"]].dropna().copy()
    rows = []

    for loc in range(min_train, len(clean)):
        train = clean.iloc[:loc]
        test = clean.iloc[[loc]]

        # Historical-only scaling inside each window.
        mu = train[feature_cols].mean()
        sd = train[feature_cols].std(ddof=1).replace(0.0, np.nan)
        X_train = (train[feature_cols] - mu) / sd
        X_test = (test[feature_cols] - mu) / sd

        X_train = sm.add_constant(X_train, has_constant="add")
        X_test = sm.add_constant(X_test, has_constant="add")

        try:
            mod = sm.QuantReg(train["target"], X_train).fit(q=quantile, max_iter=2000)
            qhat = float(mod.predict(X_test)[0])
        except Exception:
            qhat = np.nan

        rows.append(
            {
                "date": test.index[0],
                "quantile_forecast": qhat,
                "actual": float(test["target"].iloc[0]),
            }
        )

    out = pd.DataFrame(rows).set_index("date")
    out["breach"] = out["actual"] < out["quantile_forecast"]
    return out

q10_fcst = expanding_quantile_forecast(asset_data[3], feature_cols, quantile=0.10)
print("Realized breach rate:", q10_fcst["breach"].mean())
```

## 3.22 Python: Cross-Sectional Ranking Model

The following function computes rank information coefficients for cross-sectional forecasts. It assumes each date has multiple assets.

```python
from scipy.stats import spearmanr


def make_long_panel_from_targets(
    features_by_asset: pd.DataFrame,
    targets: dict[int, pd.DataFrame],
    horizon: int,
) -> pd.DataFrame:
    """Create a long panel from asset-level features and wide target returns.

    features_by_asset must have MultiIndex (date, asset). The target DataFrame
    is wide with dates as rows and assets as columns.
    """
    if not isinstance(features_by_asset.index, pd.MultiIndex):
        raise TypeError("features_by_asset must have MultiIndex (date, asset).")
    if horizon not in targets:
        raise KeyError(f"Missing horizon {horizon} in targets.")

    y = targets[horizon].stack().rename("target")
    y.index.names = ["date", "asset"]
    panel = features_by_asset.join(y, how="inner")
    return panel.replace([np.inf, -np.inf], np.nan)


def rank_ic_by_date(panel: pd.DataFrame, score_col: str, target_col: str = "target") -> pd.Series:
    """Compute Spearman rank IC by date."""
    if score_col not in panel.columns or target_col not in panel.columns:
        raise KeyError("score_col and target_col must exist in panel.")

    values = {}
    for date, group in panel[[score_col, target_col]].dropna().groupby(level="date"):
        if len(group) < 3:
            values[date] = np.nan
            continue
        rho, _ = spearmanr(group[score_col], group[target_col])
        values[date] = rho
    return pd.Series(values, name=f"rank_ic_{score_col}")

# Example synthetic cross-sectional signal: carry score for each asset.
long_rows = []
for asset in asset_returns.columns:
    tmp = pd.DataFrame(index=dates)
    tmp["asset"] = asset
    tmp["carry_score"] = rng.normal(size=len(dates))
    tmp["trend_score"] = asset_returns[asset].shift(1).rolling(6).sum()
    long_rows.append(tmp.reset_index().rename(columns={"index": "date"}))

features_by_asset = pd.concat(long_rows).set_index(["date", "asset"]).sort_index()
cs_panel = make_long_panel_from_targets(features_by_asset, fwd_targets, horizon=3)
ric = rank_ic_by_date(cs_panel, "trend_score")
print(ric.describe())
```

## 3.23 Python: Simple Panel Regression with Asset Effects

```python
import statsmodels.formula.api as smf


def fit_panel_ols_with_asset_effects(
    panel: pd.DataFrame,
    target_col: str,
    feature_cols: list[str],
    *,
    max_rows: int | None = None,
):
    """Fit an interpretable panel OLS model with asset fixed effects.

    This function is for research diagnostics. Production validation should use
    walk-forward estimation and robust inference appropriate for overlapping
    horizons and cross-sectional dependence.
    """
    if not isinstance(panel.index, pd.MultiIndex):
        raise TypeError("panel must have MultiIndex (date, asset).")
    cols = [target_col] + feature_cols
    df = panel[cols].dropna().reset_index()
    if max_rows is not None:
        df = df.tail(max_rows)

    # Q('name') protects feature names that may contain special characters.
    rhs = " + ".join([f"Q('{c}')" for c in feature_cols]) + " + C(asset)"
    formula = f"Q('{target_col}') ~ {rhs}"
    model = smf.ols(formula, data=df).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    return model

panel_model = fit_panel_ols_with_asset_effects(
    cs_panel,
    target_col="target",
    feature_cols=["carry_score", "trend_score"],
)
print(panel_model.summary().tables[1])
```

## 3.24 Visualization Code for Forecast Diagnostics

```python
import matplotlib.pyplot as plt


def plot_forecast_vs_actual(forecast_df: pd.DataFrame, title: str) -> None:
    """Plot point forecasts and realized targets."""
    required = {"forecast", "actual"}
    if not required.issubset(forecast_df.columns):
        raise KeyError("forecast_df must contain forecast and actual columns.")
    fig, ax = plt.subplots(figsize=(10, 4))
    forecast_df[["forecast", "actual"]].plot(ax=ax)
    ax.axhline(0.0, linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Return")
    plt.tight_layout()
    plt.show()


def plot_forecast_scatter(forecast_df: pd.DataFrame, title: str) -> None:
    """Scatter plot of forecast versus actual."""
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(forecast_df["forecast"], forecast_df["actual"], s=14)
    ax.axhline(0.0, linewidth=1)
    ax.axvline(0.0, linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Forecast")
    ax.set_ylabel("Actual")
    plt.tight_layout()
    plt.show()


def plot_rank_ic(rank_ic: pd.Series, window: int = 12) -> None:
    """Plot rank IC and rolling average rank IC."""
    fig, ax = plt.subplots(figsize=(10, 4))
    rank_ic.plot(ax=ax, label="Rank IC")
    rank_ic.rolling(window, min_periods=max(3, window // 2)).mean().plot(ax=ax, label="Rolling average")
    ax.axhline(0.0, linewidth=1)
    ax.set_title("Cross-Sectional Rank Information Coefficient")
    ax.set_xlabel("Date")
    ax.set_ylabel("Spearman correlation")
    ax.legend()
    plt.tight_layout()
    plt.show()

plot_forecast_vs_actual(results[3]["forecasts"], "Global Equity t+3 Forecast vs Actual")
plot_forecast_scatter(results[3]["forecasts"], "Global Equity t+3 Forecast Scatter")
plot_rank_ic(ric)
```

## 3.25 Practical Modeling Guidance by Asset Class

| Asset Class | Useful Target | Useful Features | Key Modeling Caution |
|---|---|---|---|
| Global equities | Excess or active return. | Growth, earnings, valuation, real rates, liquidity, trend. | Equity beta dominates; valuation timing is weak short term. |
| Equity sectors | Active sector return. | Rates, inflation, style, earnings revisions, commodity sensitivity. | Sector definitions and composition change. |
| Equity countries | Active country return. | FX, valuation, growth, policy, commodity exposure, political risk. | Currency basis and benchmark effects matter. |
| Sovereign duration | Total or excess return. | Inflation, growth slowdown, policy path, curve slope, real yields. | Duration and convexity change over time. |
| Credit | Excess return over duration-matched Treasuries. | Spread level, spread change, default risk, liquidity, growth. | High spreads can be both risk signal and return compensation. |
| FX | Spot or total carry-adjusted return. | Carry, real rates, valuation, external balance, risk sentiment. | Crash risk and dollar liquidity dominate in stress. |
| Commodities | Collateralized futures return. | Carry, inventories, inflation, growth, USD, seasonality. | Spot and roll components must be separated. |
| Volatility | Strategy return or vol index change. | IV/RV, term structure, skew, realized vol, liquidity. | Path dependency and nonlinear exposure. |
| Alternatives | Strategy return. | Regime, volatility, funding, trend, crowding proxies. | Backfill, leverage, liquidity, and nonlinear drawdowns. |

## 3.26 Common Return Modeling Mistakes

1. **Confusing target horizons.** A signal that works for $t+12$ may look useless at $t+1$.
2. **Using overlapping returns without robust inference.** $t+3$ and $t+12$ targets create serially correlated errors.
3. **Fitting too many predictors.** Monthly macro samples cannot support large unconstrained models.
4. **Ignoring simple baselines.** A complex model must beat carry, historical mean, or zero-active-return baselines.
5. **Treating probabilities as calibrated without testing.** Probability forecasts require calibration diagnostics.
6. **Ignoring cross-asset dependence.** Panel models need robust treatment of common shocks.
7. **Mixing local and base-currency returns.** Currency effects can dominate international assets.
8. **Using price returns when total returns are needed.** Dividends, coupons, collateral, and roll yield matter.
9. **Treating derivatives as linear assets.** Options and volatility strategies have nonlinear and path-dependent returns.
10. **Overinterpreting coefficient signs.** Coefficients can change across regimes, horizons, and sample periods.

## 3.27 Part 3 Summary

Part 3 developed the return-modeling layer of the macro-regime research process. The main lessons are:

1. Return modeling must begin with precise target definitions: absolute, excess, active, probability, quantile, or distributional.
2. The horizons $t+1$, $t+3$, and $t+12$ should usually have separate models because macro features have different economic half-lives.
3. Asset-class return construction must respect total return, duration, spread duration, currency base, futures roll, collateral, margin, and option path dependency.
4. Single-asset time-series regressions are interpretable but may be unstable in small samples.
5. Cross-sectional ranking models are useful for relative allocation, but they require point-in-time universes and rank-based validation.
6. Panel models improve sample efficiency but require robust treatment of cross-sectional and time-series dependence.
7. Direct horizon forecasting is usually the baseline for monthly macro allocation; recursive forecasting is useful when future feature paths are explicitly modeled.
8. Expected return forecasts should be complemented by probability, downside, quantile, expected shortfall, and expected Sharpe forecasts.
9. Forecast uncertainty and shrinkage are essential because expected returns are noisy and unstable.
10. Model outputs should be judged against simple baselines before being translated into conviction scores or portfolio weights.

---

# Stop Point

This installment completes:

1. **Part 3: Multi-Asset Return Modeling Across Horizons.**

Continue next with **Part 4: Statistical and Economic Regime Detection**.
