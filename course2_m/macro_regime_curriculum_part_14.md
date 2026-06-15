# Institutional Macro-Regime Detection, Multi-Asset Signal Identification, and Statistical Validation Curriculum

## Installment 14: Part 14 - Case Studies

**Scope of this installment.** This installment provides applied case studies for the macro-regime detection, signal identification, validation, conviction-scoring, portfolio integration, derivatives, and risk-management framework developed in Parts 0 through 13.

**Educational boundary.** This document is for research education, model design, and institutional portfolio-process development. It is not personalized investment advice, a live trading recommendation, or a guarantee of alpha.

---

# Part 14: Case Studies

## 14.1 Purpose of the Case Studies

The previous parts developed the building blocks of an institutional macro-regime research process: point-in-time data alignment, macro feature engineering, multi-asset return modeling, regime detection, causal channels, signal ranking, statistical validation, machine learning, regime-conditioned forecasting, portfolio integration, derivatives signals, risk management, and production implementation. Part 14 shows how these pieces fit together in applied research designs.

Each case study follows the same template:

1. **Market setup.** A stylized macro-financial environment.
2. **Macro indicators used.** Point-in-time variables and transformations.
3. **Regime classification.** How the state is estimated or interpreted.
4. **Signal construction.** How the investable signal is built.
5. **Forward horizon target.** Which $t+1$, $t+3$, or $t+12$ outcome is studied.
6. **Asset-level conviction output.** How forecasts become positive, negative, or neutral convictions.
7. **Validation evidence.** What evidence would be required before use.
8. **Portfolio implication.** How the result can inform risk budgets or tilts.
9. **Risk-management rules.** How to control model, market, and implementation risk.
10. **Failure modes.** When the signal or regime narrative may break down.
11. **Implementation notes.** Engineering, timestamp, and governance details.
12. **Python code or pseudocode.** Reproducible implementation patterns.

Throughout the case studies, let $R_{i,t,h}$ denote the forward cumulative arithmetic return for asset $i$ over horizon $h$, computed strictly from $t+1$ through $t+h$:

$$
R_{i,t,h}=\prod_{j=1}^{h}(1+r_{i,t+j})-1.
$$

Let $\mathcal{F}_t$ denote the information set available at the decision timestamp $t$. Every signal must satisfy:

$$
s_{i,t,h}=f(X_t, A_{i,t}, \mathcal{F}_t),
$$

where $X_t$ is the point-in-time macro and market feature set and $A_{i,t}$ represents asset-specific exposures such as beta, duration, spread duration, commodity sensitivity, FX exposure, liquidity, or option Greeks.

---

## 14.2 Shared Case Study Data Model

A practical research platform should represent each case study with a common schema.

| Object | Example Columns | Notes |
|---|---|---|
| Monthly features | `growth_score`, `inflation_score`, `credit_impulse`, `liquidity_tightening` | All point-in-time and lagged for release availability. |
| Regime probabilities | `slowdown_prob`, `inflation_shock_prob`, `risk_off_prob` | Filtered probabilities only for backtests. |
| Asset exposures | `duration`, `equity_beta`, `credit_beta`, `commodity_beta`, `fx_beta` | Exposures can be static or time-varying. |
| Forward targets | `fwd_return_1m`, `fwd_return_3m`, `fwd_return_12m` | Strictly future returns. |
| Signal scores | `signal_score`, `risk_score`, `conviction_score` | Oriented and documented. |
| Validation outputs | `rank_ic`, `hit_rate`, `spread`, `nw_t`, `bootstrap_ci` | Reported by horizon and regime. |
| Portfolio outputs | `active_weight`, `risk_budget`, `hedge_ratio` | Subject to constraints and costs. |

A general conviction mapping used across cases is:

$$
C_{i,t,h}=\tanh\left(
\frac{1}{c}
\frac{\hat\mu_{i,t,h}^{net}}{\hat\sigma_{i,t,h}}
\kappa_{i,t,h}
\ell_{i,t}
\rho_{t,h}^{regime}
\right),
$$

where $C_{i,t,h}$ is bounded conviction, $\hat\mu_{i,t,h}^{net}$ is transaction-cost-adjusted expected return, $\hat\sigma_{i,t,h}$ is expected horizon volatility, $\kappa$ is model confidence, $\ell$ is implementation quality, $\rho^{regime}$ is regime reliability, and $c>0$ controls compression.

---

# Case Study 1: Growth Slowdown Regime and Asset-Level t+3 Convictions

## 14.3 Market Setup

A growth slowdown regime occurs when real-activity momentum weakens, labor conditions soften, credit conditions deteriorate, and earnings revisions decline. Inflation may be stable or falling, allowing sovereign duration to hedge risky assets. This case focuses on $t+3$ asset-level convictions because growth slowdowns often transmit over several months through earnings expectations, credit risk, and policy expectations.

A stylized growth slowdown is not necessarily a recession. It is a probabilistic state in which growth momentum is negative and downside risk to cyclical assets has increased.

## 14.4 Macro Indicators Used

| Category | Indicator | Feature Transformation | Interpretation |
|---|---|---|---|
| Growth | PMI or ISM | Level and 3-month change | Activity level and momentum. |
| Labor | Unemployment, claims | 3-month change, z-score | Labor deterioration. |
| Credit | HY/IG spreads | Level and 3-month impulse | Financing stress. |
| Earnings | EPS revision breadth | Rolling z-score | Profit-cycle deterioration. |
| Policy | 2-year yield change | 3-month change | Expected policy easing or tightening. |
| Market | Equity trend | 6-month trend score | Market confirmation. |

A composite slowdown score can be defined as:

$$
\mathrm{SlowdownScore}_t
= -z_t(\Delta PMI_{3m})
+ z_t(\Delta U_{3m})
+ z_t(\Delta s^{HY}_{3m})
- z_t(\mathrm{EPSRevBreadth}_t)
- z_t(\mathrm{EquityTrend}_{6m}).
$$

Higher values imply greater slowdown pressure. All $z_t(\cdot)$ values are historical-only rolling or expanding standardizations.

## 14.5 Regime Classification

A soft slowdown probability can be produced by:

$$
\pi^{slow}_t=\frac{1}{1+\exp[-a(\mathrm{SlowdownScore}_t-b)]},
$$

where $a>0$ controls transition sharpness and $b$ is a threshold calibrated using only training data. The model may also combine this rule-based probability with HMM or GMM probabilities:

$$
\pi^{combined}_{slow,t}=\omega\pi^{rule}_{slow,t}+(1-\omega)\pi^{HMM}_{slow,t}.
$$

## 14.6 Signal Construction

For each asset $i$, define slowdown sensitivity $\beta_i^{slow}$, estimated from historical regression, risk-model exposure, or pre-specified asset-class knowledge. The slowdown signal is:

$$
s_{i,t}^{slow}= -\pi^{slow}_t\beta_i^{cyclical}+\pi^{slow}_t\beta_i^{defensive},
$$

where $\beta_i^{cyclical}$ measures exposure to growth-sensitive risk and $\beta_i^{defensive}$ measures defensive or duration-hedging exposure. A higher score is positive.

Typical stylized signs:

| Asset | Slowdown Sensitivity | Expected t+3 Conviction |
|---|---:|---|
| Global equities | Negative | Lower conviction. |
| Cyclical sectors | Strongly negative | Lower conviction. |
| High yield credit | Negative | Lower conviction. |
| Sovereign duration | Positive if inflation is falling | Higher conviction. |
| Defensive equity sectors | Mildly positive or neutral | Relative positive conviction. |
| USD or safe-haven FX | Positive in risk-off slowdown | Conditional positive conviction. |

## 14.7 Forward Horizon Target

The primary target is $t+3$ cumulative excess return:

$$
Y_{i,t,3}=R_{i,t,3}-R_{cash,t,3}.
$$

For relative allocation, use active return versus a benchmark:

$$
Y^a_{i,t,3}=R_{i,t,3}-R_{b,t,3}.
$$

## 14.8 Asset-Level Conviction Output

A slowdown-aware expected return can be written as:

$$
\hat\mu_{i,t,3}=\mu^0_{i,3}+\gamma_i s_{i,t}^{slow},
$$

where $\mu^0_{i,3}$ is a baseline expected return and $\gamma_i$ maps the signal into expected return units. Conviction is reduced when inflation pressure is high because duration hedges may fail:

$$
\rho^{regime}_{t,3}=\pi^{slow}_t(1-\pi^{inflation\ shock}_t).
$$

## 14.9 Validation Evidence

Required evidence includes:

| Validation Area | Required Test |
|---|---|
| Horizon specificity | $t+1$, $t+3$, and $t+12$ IC comparison. |
| Direction | Cyclical assets should show lower forward returns when slowdown probability rises. |
| Defensive behavior | Duration or defensive assets should improve only when inflation pressure is not dominant. |
| Robust inference | Newey-West or block bootstrap for overlapping $t+3$ targets. |
| Regime validation | Test efficacy in slowdown and non-slowdown environments. |
| Portfolio validation | Net drawdown reduction and turnover-adjusted performance. |

## 14.10 Portfolio Implication

The portfolio implication is not simply to sell all risk assets. A research process may:

1. Reduce cyclical equity and lower-quality credit risk budgets.
2. Increase high-quality duration only if inflation and term-premium signals permit.
3. Rotate toward defensive equity sectors or lower-beta exposures.
4. Reduce leverage in carry and short-volatility strategies.
5. Increase liquidity buffer and rebalance frequency monitoring.

## 14.11 Risk-Management Rules

| Rule | Rationale |
|---|---|
| Cap duration overweight when inflation score is high. | Stagflation can break duration hedges. |
| Require confirmation from credit impulse or earnings revisions. | Avoid reacting to one noisy growth indicator. |
| Apply turnover limit. | Slowdown probability can oscillate around threshold. |
| De-risk more aggressively when liquidity stress is rising. | Liquidity stress increases gap and drawdown risk. |
| Use confidence decay when indicators disagree. | Mixed regimes should produce lower conviction. |

## 14.12 Failure Modes

1. Growth data may be revised or released with lags.
2. Equity markets may rally on expected policy easing despite weak growth.
3. Duration may fail if inflation or term premium rises.
4. Credit spreads may already price the slowdown.
5. The slowdown may be shallow and short-lived.
6. Defensive rotations can become crowded.

## 14.13 Implementation Notes

The production implementation should store feature release dates, vintage macro values, signal version, model version, and regime probability timestamp. If the slowdown score uses PMI data, the value must be joined by release date, not reference month. If earnings revisions come from vendor data, revision timestamp and universe coverage must be documented.

## 14.14 Python Pseudocode

```python
import numpy as np
import pandas as pd


def logistic(x, slope=1.0, threshold=0.0):
    return 1.0 / (1.0 + np.exp(-slope * (x - threshold)))


def build_slowdown_score(features):
    required = [
        "pmi_3m_change_z", "unemployment_3m_change_z",
        "hy_spread_3m_change_z", "eps_revision_breadth_z",
        "equity_trend_6m_z"
    ]
    missing = set(required) - set(features.columns)
    if missing:
        raise KeyError(f"Missing features: {sorted(missing)}")
    score = (
        -features["pmi_3m_change_z"]
        + features["unemployment_3m_change_z"]
        + features["hy_spread_3m_change_z"]
        - features["eps_revision_breadth_z"]
        - features["equity_trend_6m_z"]
    ) / np.sqrt(len(required))
    return score.rename("slowdown_score")


def slowdown_convictions(features, exposures, baseline_mu, vol):
    score = build_slowdown_score(features)
    slow_prob = logistic(score, slope=1.2, threshold=0.5).rename("slowdown_prob")
    latest_prob = slow_prob.iloc[-1]
    cyc = exposures["cyclical_beta"]
    defensive = exposures.get("defensive_beta", pd.Series(0.0, index=exposures.index))
    signal = -latest_prob * cyc + latest_prob * defensive
    expected_return = baseline_mu + 0.02 * signal
    raw_conviction = expected_return / vol.replace(0.0, np.nan)
    return np.tanh(raw_conviction).rename("t3_conviction")
```

---

# Case Study 2: Inflation Shock Regime and Cross-Asset Return Dispersion

## 14.15 Market Setup

An inflation shock regime occurs when inflation level, momentum, breadth, or surprise exceeds what markets and policymakers expected. The key asset-market issue is cross-asset dispersion: nominal duration, growth equities, commodities, inflation-linked bonds, FX, and volatility exposures may respond differently depending on whether the inflation shock is demand-driven or supply-driven.

## 14.16 Macro Indicators Used

| Category | Indicator | Feature | Purpose |
|---|---|---|---|
| Inflation level | CPI/PCE YoY | Historical z-score | Persistent inflation state. |
| Inflation momentum | 3m annualized CPI/PCE | Difference versus YoY | Acceleration. |
| Inflation breadth | Share of components above threshold | Rolling percentile | Breadth and persistence. |
| Inflation surprise | Actual minus survey | Standardized surprise | Unexpected component. |
| Market pricing | Breakevens, inflation swaps | 3m change | Market-implied repricing. |
| Policy response | Real yield change | 3m change | Tightening pressure. |

Inflation pressure can be summarized as:

$$
I_t=w_1z_t(\pi^{YoY}_t)+w_2z_t(\pi^{3m,ann}_t-\pi^{YoY}_t)
+w_3z_t(\mathrm{InflBreadth}_t)+w_4z_t(\mathrm{InflSurprise}_t).
$$

## 14.17 Regime Classification

A two-dimensional inflation regime can separate inflation pressure from growth resilience:

$$
\mathrm{InflationShockProb}_t=\sigma(a(I_t-b_I)),
$$

$$
\mathrm{StagflationProb}_t=\sigma(a(I_t-b_I))\sigma(a(-G_t-b_G)),
$$

where $G_t$ is a growth score. This matters because demand-driven inflation and stagflationary inflation have different cross-asset implications.

## 14.18 Signal Construction

Inflation shock sensitivity for each asset can be decomposed:

$$
s_{i,t}^{infl}=\pi^{infl}_t
\left(
\beta_i^{commodity}
+\beta_i^{inflation\ hedge}
-\beta_i^{duration}
-\beta_i^{valuation\ duration}
-\beta_i^{margin\ risk}
\right).
$$

The model should treat nominal duration and long-duration equities as vulnerable when real yields rise:

$$
\mathrm{RealRateShock}_t=\Delta y^{real}_{10y,t,3m}.
$$

## 14.19 Forward Horizon Target

The primary target is cross-sectional $t+3$ active return:

$$
Y^a_{i,t,3}=R_{i,t,3}-R_{multiasset,t,3}.
$$

The secondary target is return dispersion:

$$
\mathrm{Dispersion}_{t,3}=\sqrt{\frac{1}{N_t-1}\sum_{i\in\mathcal{U}_t}(R_{i,t,3}-\bar R_{t,3})^2}.
$$

## 14.20 Asset-Level Conviction Output

| Asset Class | Inflation Shock Conviction | Conditioning Variable |
|---|---|---|
| Nominal duration | Negative | Stronger if real yields rise. |
| Inflation-linked bonds | Positive relative to nominal duration | Stronger if breakevens rise less than realized inflation. |
| Commodities | Positive if supply/inflation shock supports spot and carry | Curve and inventory conditions. |
| Gold | Mixed | Positive if inflation shock lowers real confidence; negative if real yields rise sharply. |
| Growth equities | Negative | Stronger if valuation duration is high. |
| Value/cyclical equities | Mixed | Depends on growth resilience and margin pressure. |
| USD | Positive if policy response is hawkish | Relative real-rate differential. |

## 14.21 Validation Evidence

Required evidence includes cross-sectional rank IC by inflation-shock months, top-minus-bottom inflation sensitivity spread, and stress-period analysis. The validation should separate inflation level from inflation surprise because expected inflation may already be priced.

## 14.22 Portfolio Implication

Potential implications include reducing nominal duration, reducing long-duration equity style exposure, increasing inflation-linked or commodity risk budgets subject to curve/carry conditions, and using options overlays when inflation uncertainty raises volatility.

## 14.23 Risk-Management Rules

1. Do not increase commodities solely on CPI if futures curves imply negative roll yield.
2. Cap gold conviction when real yields rise sharply.
3. Separate supply-driven inflation from demand-driven reflation.
4. Stress test simultaneous equity and bond losses.
5. Monitor volatility and margin pressure in commodity futures.

## 14.24 Failure Modes

Inflation surprises may be quickly reversed, policy credibility may reduce long-term inflation repricing, commodities may be supply-constrained but expensive to roll, and growth deterioration may dominate inflation-hedge logic.

## 14.25 Python Pseudocode

```python
import numpy as np
import pandas as pd


def inflation_pressure(features):
    cols = [
        "inflation_yoy_z", "inflation_acceleration_z",
        "inflation_breadth_z", "inflation_surprise_z"
    ]
    return features[cols].mean(axis=1).rename("inflation_pressure")


def inflation_shock_conviction(features, asset_exposures, baseline_mu, vol):
    pressure = inflation_pressure(features)
    infl_prob = 1.0 / (1.0 + np.exp(-1.5 * (pressure - 0.75)))
    latest_prob = infl_prob.iloc[-1]
    real_rate_shock = features["real_yield_3m_change_z"].iloc[-1]
    raw_signal = (
        asset_exposures["commodity_beta"]
        + asset_exposures["inflation_linked_beta"]
        - asset_exposures["duration"] * max(real_rate_shock, 0.0)
        - asset_exposures["valuation_duration"]
        - asset_exposures["margin_risk"]
    )
    mu = baseline_mu + 0.015 * latest_prob * raw_signal
    return np.tanh((mu / vol).replace([np.inf, -np.inf], np.nan))
```

---

# Case Study 3: Liquidity Tightening and Risk-Off Asset Behavior

## 14.26 Market Setup

Liquidity tightening occurs when funding costs rise, financial conditions tighten, central-bank liquidity declines, dealer balance-sheet capacity weakens, or market depth deteriorates. Liquidity tightening can convert moderate macro weakness into risk-off behavior through leverage constraints and forced selling.

## 14.27 Macro Indicators Used

| Indicator | Feature | Interpretation |
|---|---|---|
| Financial conditions index | 3m change z-score | Broad tightening. |
| Funding spread | Level and change | Funding stress. |
| Cross-currency basis | Level z-score | Dollar funding pressure. |
| Central-bank reserves | 3m growth, oriented negative | System liquidity. |
| Credit spreads | 1m and 3m impulse | Risk premia and financing. |
| Volatility term structure | Front minus back | Hedging demand. |
| Bid-ask or liquidity proxy | Level z-score | Market depth. |

A liquidity tightening score is:

$$
L_t=z_t(\Delta FCI_{3m})+z_t(\Delta FundingSpread_{3m})
-z_t(\Delta Reserves_{3m})+z_t(\Delta CreditSpread_{3m})+z_t(VolTermStress_t).
$$

## 14.28 Regime Classification

A risk-off liquidity regime can be represented as:

$$
\pi^{liqstress}_t=\sigma(a(L_t-b_L)).
$$

A stronger regime condition requires both liquidity tightening and volatility confirmation:

$$
\pi^{riskoff}_t=\pi^{liqstress}_t\cdot\sigma(a(V_t-b_V)),
$$

where $V_t$ is a volatility stress score.

## 14.29 Signal Construction

The liquidity stress signal penalizes assets with high leverage, low liquidity, credit beta, short-volatility exposure, or high beta:

$$
s_{i,t}^{liq}= -\pi^{riskoff}_t
(\beta_i^{equity}+\beta_i^{credit}+\beta_i^{illiquidity}+\beta_i^{shortvol}+\beta_i^{leverage}).
$$

Defensive assets can receive positive scores if they historically provide liquidity or convexity:

$$
s_{i,t}^{def}=\pi^{riskoff}_t(\beta_i^{safe\ duration}+\beta_i^{longvol}+\beta_i^{cashlike}).
$$

## 14.30 Forward Horizon Target

The primary target is $t+1$ and $t+3$ downside probability:

$$
D_{i,t,h}(L)=\mathbf{1}\{R_{i,t,h}<L\},
$$

where $L$ is a loss threshold such as $-5\%$ for risky assets or an asset-specific percentile.

## 14.31 Asset-Level Conviction Output

Conviction is more about risk reduction than expected return maximization. A liquidity-adjusted conviction can be:

$$
C_{i,t,h}^{liq}=-\Pr_t(R_{i,t,h}<L)\cdot\mathrm{LossGivenStress}_{i,t,h}.
$$

Positive defensive conviction is assigned only if the asset has historically performed well in liquidity stress and remains liquid in implementation.

## 14.32 Validation Evidence

Validation should emphasize drawdown avoidance, downside hit rate, expected shortfall reduction, turnover cost, and false-alarm rate. False alarms are important because repeated de-risking can create large opportunity costs.

## 14.33 Portfolio Implication

1. Reduce gross and net leverage.
2. Reduce high-yield credit, small-cap equity, carry, and short-volatility exposure.
3. Raise cash or cash-like collateral.
4. Increase long-volatility or option convexity only if pricing is acceptable.
5. Review margin and collateral requirements.

## 14.34 Risk-Management Rules

| Rule | Purpose |
|---|---|
| Liquidity-stress kill switch | Prevents forced deleveraging during funding shock. |
| Turnover budget override | Allows urgent risk reduction. |
| Minimum cash buffer | Preserves optionality and margin capacity. |
| Cost-aware hedge rule | Avoids buying extremely expensive protection automatically. |
| Re-entry discipline | Prevents immediate re-risking after one calm month. |

## 14.35 Failure Modes

Liquidity tightening signals can trigger too early, central-bank intervention may rapidly reverse stress, long-volatility hedges may be overpriced, and safe assets may fail if inflation or fiscal-risk shocks dominate.

## 14.36 Python Pseudocode

```python
import numpy as np
import pandas as pd


def liquidity_stress_probability(features):
    cols = [
        "fci_3m_change_z", "funding_spread_3m_change_z",
        "reserves_3m_growth_z", "credit_spread_3m_change_z",
        "vol_term_stress_z"
    ]
    score = (
        features["fci_3m_change_z"]
        + features["funding_spread_3m_change_z"]
        - features["reserves_3m_growth_z"]
        + features["credit_spread_3m_change_z"]
        + features["vol_term_stress_z"]
    ) / np.sqrt(len(cols))
    return 1.0 / (1.0 + np.exp(-1.25 * (score - 0.5)))


def liquidity_risk_scores(features, exposures):
    p = liquidity_stress_probability(features).iloc[-1]
    vulnerable = (
        exposures["equity_beta"] + exposures["credit_beta"]
        + exposures["illiquidity"] + exposures["short_vol_beta"]
        + exposures["leverage_beta"]
    )
    defensive = exposures.get("safe_duration_beta", 0.0) + exposures.get("long_vol_beta", 0.0)
    score = -p * vulnerable + p * defensive
    return score.rename("liquidity_regime_score")
```

---

# Case Study 4: Yield-Curve Signal for Duration, Equity Style, and FX Exposure

## 14.37 Market Setup

Yield-curve signals summarize policy expectations, term premia, growth expectations, and inflation risk. A curve inversion may signal future growth weakness, but a bear steepening may signal inflation or fiscal risk. This case separates curve level, curve change, and curve composition.

## 14.38 Macro Indicators Used

| Indicator | Feature | Interpretation |
|---|---|---|
| 10y-2y slope | Level and percentile | Inversion or steepness. |
| 10y yield change | 3m change | Long-end repricing. |
| 2y yield change | 3m change | Policy path repricing. |
| Real yield slope | Level/change | Real policy and term-premium conditions. |
| Breakeven slope | Level/change | Inflation-risk pricing. |
| Growth score | Composite | Context for inversion. |
| Inflation score | Composite | Context for bear steepening. |

## 14.39 Regime Classification

Curve regimes can be classified by slope and yield-change composition:

| Curve State | Condition | Interpretation |
|---|---|---|
| Bull steepening | $\Delta y_{2y}<0$, slope rises | Policy easing or growth concern. |
| Bear steepening | $\Delta y_{10y}>0$, slope rises | Term premium, inflation, fiscal pressure. |
| Bull flattening | $\Delta y_{10y}<0$, slope falls | Long-end rally, disinflation. |
| Bear flattening | $\Delta y_{2y}>0$, slope falls | Hawkish policy repricing. |
| Inversion | slope below zero | Tight policy relative to long-term expectations. |

## 14.40 Signal Construction

A duration signal can be:

$$
s_{duration,t}= -z_t(\Delta y^{real}_{10y,3m}) - z_t(\Delta \pi^{breakeven}_{10y,3m}) + z_t(\mathrm{SlowdownProb}_t).
$$

An equity style signal can be:

$$
s_{growth\ vs\ value,t}= -z_t(\Delta y^{real}_{10y,3m}) - z_t(\Delta y_{2y,3m}).
$$

An FX signal can use relative real-rate differentials:

$$
s_{FX,t}^{F/B}=z_t(\Delta r^{real}_{F,t}-\Delta r^{real}_{B,t})+z_t(Carry_{F/B,t}).
$$

## 14.41 Forward Horizon Target

The primary horizons are $t+3$ for duration and equity style, and $t+1$ to $t+3$ for FX:

$$
Y^{dur}_{t,3}=R^{duration}_{t,3}-R^{cash}_{t,3},
$$

$$
Y^{style}_{t,3}=R^{growth}_{t,3}-R^{value}_{t,3},
$$

$$
Y^{FX}_{F/B,t,3}=R^{FX}_{F/B,t,3}.
$$

## 14.42 Asset-Level Conviction Output

| Signal Condition | Duration | Growth Equity | Value/Cyclicals | FX |
|---|---|---|---|---|
| Bull steepening with slowdown | Positive | Mixed | Negative | Safe-haven FX positive. |
| Bear flattening | Negative | Negative | Mixed | Hawkish currency positive. |
| Bear steepening with inflation | Negative | Negative | Mixed to negative | Terms-of-trade and real-rate dependent. |
| Inversion with falling inflation | Positive at medium horizon | Defensive tilt | Cyclical underweight | Safe-haven bias. |

## 14.43 Validation Evidence

Validate curve features separately by regime because the same curve move can have different meanings. Required tests include duration return regression, equity-style spread tests, FX carry and rate-differential rank IC, and subperiod stability around policy-cycle changes.

## 14.44 Portfolio Implication

Curve signals can inform duration budget, equity style tilt, and FX exposure. The portfolio should avoid double-counting: long duration, long growth stocks, and long gold may all share real-rate exposure.

## 14.45 Risk-Management Rules

1. Decompose nominal yield changes into real-yield and breakeven components.
2. Limit curve-signal strength when inflation and fiscal-risk indicators conflict.
3. Monitor duration exposure across bonds, equities, alternatives, and options.
4. Apply currency carry crash-risk controls.

## 14.46 Failure Modes

The yield curve can invert long before recession, term premium can dominate expected short rates, central-bank reaction functions can change, and curve signals can be distorted by quantitative easing, fiscal issuance, or regulatory demand for duration.

## 14.47 Python Pseudocode

```python
import numpy as np
import pandas as pd


def classify_curve_state(curve):
    slope_change = curve["slope_10y2y"].diff(3)
    dy10 = curve["y10"].diff(3)
    dy2 = curve["y2"].diff(3)
    state = pd.Series("neutral", index=curve.index)
    state[(slope_change > 0) & (dy2 < 0)] = "bull_steepening"
    state[(slope_change > 0) & (dy10 > 0)] = "bear_steepening"
    state[(slope_change < 0) & (dy10 < 0)] = "bull_flattening"
    state[(slope_change < 0) & (dy2 > 0)] = "bear_flattening"
    state[curve["slope_10y2y"] < 0] = "inversion"
    return state


def curve_based_duration_signal(features):
    signal = (
        -features["real_yield_10y_3m_change_z"]
        -features["breakeven_10y_3m_change_z"]
        +features["slowdown_probability_z"]
    )
    return signal.rename("duration_signal")
```

---

# Case Study 5: Credit Spread Widening as a Regime Transition Indicator

## 14.48 Market Setup

Credit spreads often widen before broader risk-off environments become obvious in macro data. Spread widening can reflect default risk, liquidity stress, risk-aversion repricing, or declining dealer balance-sheet capacity. This case treats credit spread widening as a transition indicator rather than only an expected-return signal.

## 14.49 Macro Indicators Used

| Indicator | Feature | Purpose |
|---|---|---|
| HY spread | 1m and 3m change z-score | Fast credit impulse. |
| IG spread | 3m change z-score | Higher-quality confirmation. |
| CDS index | Level and change | Market-implied credit risk. |
| Lending standards | Change | Bank credit channel. |
| Equity volatility | Level and term structure | Risk confirmation. |
| Equity breadth | Deterioration | Market confirmation. |
| Default expectations | Level/change | Fundamental credit risk. |

## 14.50 Regime Classification

A credit transition probability can be:

$$
\pi^{credit\ transition}_t=\sigma\left(a[z_t(\Delta s^{HY}_{3m})+z_t(\Delta s^{IG}_{3m})+z_t(VIXTermStress_t)-b]\right).
$$

This probability is not the same as credit distress. It is a signal that the system may be moving from benign risk conditions toward stress.

## 14.51 Signal Construction

The transition signal can be applied to multiple assets:

$$
s_{i,t}^{credit}= -\pi^{credit\ transition}_t
(\beta_i^{credit}+\beta_i^{equity}+\beta_i^{liquidity}+\beta_i^{carry}).
$$

A separate long-duration or defensive signal may be allowed only if inflation pressure is contained:

$$
s_{duration,t}^{credit}=\pi^{credit\ transition}_t(1-\pi^{inflation\ shock}_t).
$$

## 14.52 Forward Horizon Target

Primary targets include:

$$
D^{equity}_{t,3}=\mathbf{1}\{R^{equity}_{t,3}<0\},
$$

$$
Y^{credit}_{t,3}=R^{credit}_{t,3}-R^{duration\ matched\ treasury}_{t,3},
$$

and cross-asset drawdown probability.

## 14.53 Asset-Level Conviction Output

| Asset | Credit Transition Effect |
|---|---|
| High yield | Strong negative. |
| Investment grade | Moderate negative, duration interaction. |
| Equities | Negative, strongest for small caps and cyclicals. |
| Defensive equities | Relative positive. |
| Sovereign duration | Positive only if inflation is not dominant. |
| Short-volatility/carry | Negative. |

## 14.54 Validation Evidence

Evidence should include lead-lag analysis, Granger predictability screens, regime transition confusion matrices, downside probability calibration, and stress-period behavior. Avoid using revised default data unavailable at the decision timestamp.

## 14.55 Portfolio Implication

Credit spread widening can trigger de-risking, credit quality upgrade, reduction in carry strategies, and stronger monitoring of liquidity and volatility. It can also increase hedge budgets.

## 14.56 Risk-Management Rules

1. Use spread changes, not just spread levels.
2. Distinguish high spread compensation from widening impulse.
3. Confirm with volatility or equity breadth before major de-risking.
4. Avoid adding credit exposure solely because spreads are high during liquidity stress.

## 14.57 Failure Modes

Credit spreads may widen due to technical factors without broad macro stress. Central-bank support can compress spreads quickly. Spread levels may become attractive after large widening, creating reversal risk for underweights.

## 14.58 Python Pseudocode

```python
import numpy as np
import pandas as pd


def credit_transition_probability(features):
    score = (
        features["hy_spread_3m_change_z"]
        + features["ig_spread_3m_change_z"]
        + features["vix_term_stress_z"]
        - features["equity_breadth_z"]
    ) / 2.0
    return 1.0 / (1.0 + np.exp(-1.3 * (score - 0.5)))


def credit_transition_signal(features, exposures):
    p = credit_transition_probability(features).iloc[-1]
    vulnerable = (
        exposures["credit_beta"]
        + exposures["equity_beta"]
        + exposures["illiquidity"]
        + exposures["carry_beta"]
    )
    return (-p * vulnerable).rename("credit_transition_signal")
```

---

# Case Study 6: Volatility Term Structure and Equity Drawdown Risk

## 14.59 Market Setup

The volatility term structure reflects hedging demand, near-term uncertainty, and the pricing of volatility risk. When front-end implied volatility rises above longer-dated volatility, markets often indicate immediate stress. This case uses volatility term structure to forecast $t+1$ and $t+3$ equity drawdown risk.

## 14.60 Macro and Market Indicators Used

| Indicator | Feature | Purpose |
|---|---|---|
| VIX front-month | Level percentile | Near-term implied risk. |
| VIX 3m or 6m | Level | Medium-term uncertainty. |
| VIX term spread | Front minus back | Inversion/stress. |
| Realized volatility | Short-term realized vol | Actual instability. |
| Variance risk premium | IV squared minus RV squared | Insurance premium. |
| Skew | Put skew percentile | Downside demand. |
| Credit impulse | 3m spread change | Confirmation. |

## 14.61 Regime Classification

A volatility stress probability is:

$$
\pi^{volstress}_t=\sigma\left(a[z_t(VIX_{front}-VIX_{3m})+z_t(Skew_t)+z_t(RVShock_t)-b]\right).
$$

A severe stress state can be defined when both term structure is inverted and credit spreads widen.

## 14.62 Signal Construction

Equity drawdown risk forecast:

$$
\Pr_t(R^{equity}_{t,h}<L)=\sigma(\alpha_h+\beta_1\mathrm{VolStress}_t+\beta_2\mathrm{CreditImpulse}_t+\beta_3\mathrm{LiquidityTight}_t).
$$

For asset-level scores:

$$
s_{i,t}^{volrisk}= -\Pr_t(R^{equity}_{t,h}<L)\beta_i^{equity\ beta}+\pi^{volstress}_t\beta_i^{longvol}.
$$

## 14.63 Forward Horizon Target

Primary targets are:

$$
D_{t,1}=\mathbf{1}\{R^{equity}_{t,1}<L_1\},
$$

$$
D_{t,3}=\mathbf{1}\{R^{equity}_{t,3}<L_3\},
$$

where $L_1$ and $L_3$ are drawdown thresholds.

## 14.64 Asset-Level Conviction Output

Equity beta, high-yield credit, short-volatility, and levered risk-premia receive negative risk convictions. Long-volatility or convexity strategies may receive positive risk-hedge conviction, but only after considering option carry and premium.

## 14.65 Validation Evidence

Calibration is crucial. If the model predicts a 30% probability of drawdown, realized drawdown frequency should be close to 30% in comparable forecast buckets. Validate Brier score, log loss, reliability plots, drawdown reduction, hedge cost, and false positive rate.

## 14.66 Portfolio Implication

1. Reduce equity beta and credit beta.
2. Reduce short-volatility and carry exposures.
3. Add option convexity only if expected hedge benefit exceeds premium.
4. Temporarily tighten drawdown and turnover controls.

## 14.67 Risk-Management Rules

1. Avoid buying volatility mechanically after extreme spikes.
2. Differentiate high implied volatility that is overpriced from high volatility that signals crash risk.
3. Use position sizing based on premium-at-risk.
4. Monitor margin and gap risk for option strategies.

## 14.68 Failure Modes

Volatility spikes can mean-revert quickly. Long-volatility hedges can bleed. Volatility term structure can invert after losses have already occurred. Volatility products may have roll costs, liquidity constraints, and path dependency.

## 14.69 Python Pseudocode

```python
import numpy as np
import pandas as pd


def volatility_stress_score(features):
    score = (
        features["vix_front_minus_3m_z"]
        + features["skew_percentile_z"]
        + features["realized_vol_shock_z"]
        + features["credit_spread_1m_change_z"]
    ) / 2.0
    return score.rename("vol_stress_score")


def drawdown_probability(features, coef):
    score = volatility_stress_score(features)
    x = coef["intercept"] + coef["vol_stress"] * score
    if "liquidity_tightening_z" in features:
        x = x + coef.get("liquidity", 0.0) * features["liquidity_tightening_z"]
    return (1.0 / (1.0 + np.exp(-x))).rename("drawdown_probability")
```

---

# Case Study 7: Commodity Futures Carry Under Inflation and Growth Regimes

## 14.70 Market Setup

Commodity futures carry depends on curve shape, storage conditions, inventory scarcity, collateral return, seasonality, and macro regime. Backwardation may indicate scarcity and positive roll yield, while contango may imply negative roll yield. However, commodity carry behaves differently under inflation shocks, growth slowdowns, and USD liquidity stress.

## 14.71 Indicators Used

| Indicator | Feature | Purpose |
|---|---|---|
| Futures curve slope | Front-to-next or multi-contract slope | Carry and roll yield. |
| Inventory level | Percentile | Scarcity or abundance. |
| Spot trend | 6m or 12m trend | Price momentum. |
| Inflation pressure | Composite score | Macro support. |
| Growth score | Composite score | Demand support. |
| USD trend | 3m or 6m change | Currency pressure. |
| Real rates | Change | Opportunity cost and dollar channel. |

## 14.72 Regime Classification

Commodity carry is conditioned on growth and inflation:

| Regime | Carry Interpretation |
|---|---|
| Reflation | Backwardation and demand support can reinforce. |
| Inflation shock | Supply scarcity can dominate, but volatility rises. |
| Growth slowdown | Carry can fail if demand collapses. |
| USD liquidity stress | Commodities can fall despite inflation narrative. |

## 14.73 Signal Construction

Commodity futures carry score:

$$
Carry_{i,t}= -\left(\frac{F_{i,2,t}}{F_{i,1,t}}-1\right),
$$

where $F_{i,1,t}$ is the near contract and $F_{i,2,t}$ is the next contract. Under this convention, backwardation gives positive carry.

A regime-conditioned commodity signal is:

$$
s_{i,t}^{cmdty}=z_t(Carry_{i,t})+z_t(Trend_{i,t})+\beta_i^{infl}\pi^{infl}_t+\beta_i^{growth}\pi^{growth}_t-\beta_i^{USD}\mathrm{USDStress}_t.
$$

## 14.74 Forward Horizon Target

The primary target is collateralized futures return:

$$
Y_{i,t,h}=R^{spot}_{i,t,h}+R^{roll}_{i,t,h}+R^{collateral}_{t,h}-Costs_{i,t,h}.
$$

Use $t+1$, $t+3$, and $t+12$ because carry can accrue slowly but crashes can occur quickly.

## 14.75 Asset-Level Conviction Output

| Commodity Group | Carry Signal Interpretation | Regime Filter |
|---|---|---|
| Energy | Backwardation can be strong but volatile | Inventory and geopolitical filters. |
| Metals | Growth and USD sensitive | Growth and real-rate filters. |
| Agriculture | Seasonal and weather-sensitive | Seasonality and inventory filters. |
| Precious metals | Real-rate and USD sensitive | Real-rate and risk-off filters. |

## 14.76 Validation Evidence

Validate net futures returns, not spot returns. Include roll schedule, collateral return, transaction costs, contract liquidity, and seasonal effects. Use cross-sectional rank IC across commodities and time-series tests within each commodity.

## 14.77 Portfolio Implication

Commodity carry can support alternative risk premia allocation, inflation-sensitive risk budgets, or tactical commodity sleeve tilts. Volatility targeting is important because commodity returns can be highly volatile and gap-prone.

## 14.78 Risk-Management Rules

1. Use position limits by commodity and sector.
2. Include roll liquidity and contract expiry rules.
3. Volatility-target exposures.
4. Stress test USD shock and growth slowdown.
5. Avoid excessive exposure to one curve signal.

## 14.79 Failure Modes

Backwardation can reflect severe scarcity and crash risk after normalization. Contango can persist for long periods. Futures returns can differ materially from spot returns. Policy, geopolitics, weather, and inventory data quality can dominate macro signals.

## 14.80 Python Pseudocode

```python
import numpy as np
import pandas as pd


def commodity_carry(front, second):
    curve_slope = second / front - 1.0
    return (-curve_slope).replace([np.inf, -np.inf], np.nan)


def commodity_signal(curves, features, exposures):
    carry = commodity_carry(curves["front"], curves["second"])
    trend = curves["spot_total_return_index"].pct_change(6)
    latest_macro = features.iloc[-1]
    signal = (
        carry.rank(pct=True)
        + trend.rank(pct=True)
        + exposures["inflation_beta"] * latest_macro["inflation_prob"]
        + exposures["growth_beta"] * latest_macro["growth_prob"]
        - exposures["usd_beta"] * latest_macro["usd_stress"]
    )
    return signal.rename("commodity_signal")
```

---

# Case Study 8: Combining Macro, Trend, Carry, and Volatility Signals into Asset-Level Conviction

## 14.81 Market Setup

The final case combines multiple signal families into a unified asset-level conviction framework. This is closest to a production multi-asset process. The objective is not to find one perfect signal but to combine economically distinct evidence while controlling redundancy, uncertainty, regime dependence, and implementation frictions.

## 14.82 Signal Families Used

| Signal Family | Example Features | Primary Horizon |
|---|---|---|
| Macro regime | Growth, inflation, credit, liquidity probabilities | $t+3$, $t+12$ |
| Trend | 6m, 12m-1m momentum, moving-average trend | $t+1$, $t+3$, $t+12$ |
| Carry | Bond yield, FX carry, futures carry, credit carry | $t+3$, $t+12$ |
| Value | Equity yield, real yield, PPP, spread compensation | $t+12$ |
| Volatility | Realized vol, implied vol, skew, term structure | $t+1$, $t+3$ |
| Risk appetite | Credit, breadth, cross-asset correlation, flows | $t+1$, $t+3$ |

## 14.83 Regime Classification

Use a probability vector:

$$
\boldsymbol{\pi}_t=(\pi^{expansion}_t,\pi^{slowdown}_t,\pi^{inflation}_t,\pi^{liquidity\ stress}_t).
$$

The probability-weighted expected return is:

$$
\hat\mu_{i,t,h}^{regime}=\sum_{k=1}^{K}\pi_{k,t}\hat\mu_{i,k,h}.
$$

## 14.84 Signal Construction

Define standardized signal families:

$$
S_{i,t,h}^{macro},\quad S_{i,t,h}^{trend},\quad S_{i,t,h}^{carry},\quad S_{i,t,h}^{value},\quad S_{i,t,h}^{vol}.
$$

A composite score is:

$$
S_{i,t,h}=w_M S_{i,t,h}^{macro}+w_T S_{i,t,h}^{trend}+w_C S_{i,t,h}^{carry}+w_V S_{i,t,h}^{value}+w_{Vol}S_{i,t,h}^{vol}.
$$

Weights should start equal or shrink strongly toward equal weights:

$$
w_m^{shrunk}=\lambda\frac{1}{M}+(1-\lambda)w_m^{estimated}.
$$

## 14.85 Forward Horizon Target

The model should produce separate targets by horizon:

$$
\hat\mu_{i,t,1},\quad \hat\mu_{i,t,3},\quad \hat\mu_{i,t,12}.
$$

Horizon-specific composite scores are required because the signal families decay differently.

## 14.86 Asset-Level Conviction Output

The final conviction combines expected return, probability, and uncertainty:

$$
C_{i,t,h}=\tanh\left(\frac{\hat\mu_{i,t,h}^{net}}{\hat\sigma_{i,t,h}}\kappa_{i,t,h}\ell_{i,t}\right).
$$

The confidence term is:

$$
\kappa_{i,t,h}=\kappa^{IC}_{h}\kappa^{stability}_{h}\kappa^{regime}_{t}\kappa^{data}_{i,t}\kappa^{cost}_{i,t}.
$$

## 14.87 Validation Evidence

The combined model must be validated against:

1. Equal-weight signal composite.
2. Macro-only model.
3. Trend-only model.
4. Carry-only model.
5. Zero active-return benchmark.
6. Historical mean or carry prior.
7. Regime-unaware model.

The combined model should improve robustness, not merely maximize in-sample performance.

## 14.88 Portfolio Implication

A conviction-aware portfolio may use:

$$
\max_{w_t}\; w_t^\top\hat\mu_t
-\frac{\lambda}{2}w_t^\top\hat\Sigma_t w_t
-\tau\|w_t-w_{t-1}\|_1,
$$

subject to leverage, liquidity, concentration, beta, duration, FX, credit, commodity, volatility, and turnover constraints.

## 14.89 Risk-Management Rules

1. Cap signal contribution by family to prevent one theme dominating.
2. Apply redundancy control using signal correlation or PCA.
3. Shrink expected returns toward priors.
4. Reduce conviction when regime probabilities are diffuse.
5. Report exposures before and after optimization.
6. Monitor live signal decay.
7. Apply kill switches for liquidity stress and model instability.

## 14.90 Failure Modes

The composite model can hide weak components, double-count correlated signals, overfit estimated weights, respond too slowly to regime breaks, and produce false diversification if all signals share liquidity or risk-appetite exposure.

## 14.91 Implementation Notes

A production system should maintain feature-store versioning, model registry entries, validation artifacts, forecast snapshots, portfolio optimizer configurations, and daily/monthly monitoring reports. Every conviction should be traceable back to feature values, signal weights, regime probabilities, and model versions.

## 14.92 Python Pseudocode

```python
import numpy as np
import pandas as pd


def shrink_weights(estimated_weights, shrink=0.70):
    estimated_weights = estimated_weights.astype(float)
    estimated_weights = estimated_weights / estimated_weights.abs().sum()
    equal = pd.Series(1.0 / len(estimated_weights), index=estimated_weights.index)
    return shrink * equal + (1.0 - shrink) * estimated_weights


def combine_signal_families(signal_panel, family_cols, weights=None):
    if weights is None:
        weights = pd.Series(1.0 / len(family_cols), index=family_cols)
    weights = weights.reindex(family_cols)
    composite = signal_panel[family_cols].mul(weights, axis=1).sum(axis=1)
    return composite.rename("composite_signal")


def final_conviction(expected_return, volatility, confidence, liquidity_quality):
    raw = (expected_return / volatility.replace(0.0, np.nan)) * confidence * liquidity_quality
    return np.tanh(raw).rename("final_conviction")


def pre_optimizer_weights(conviction, volatility, gross_limit=0.50):
    raw = conviction / volatility.replace(0.0, np.nan)
    raw = raw.replace([np.inf, -np.inf], np.nan).dropna()
    if raw.abs().sum() == 0:
        return raw.rename("active_weight")
    return (gross_limit * raw / raw.abs().sum()).rename("active_weight")
```

---

# 14.93 Cross-Case Comparison Matrix

| Case Study | Primary Regime | Main Signal Type | Main Horizon | Main Portfolio Use | Main Failure Mode |
|---|---|---|---:|---|---|
| Growth slowdown | Growth weakening | Macro + credit + earnings | $t+3$ | Reduce cyclicality, manage duration hedge | Inflation prevents duration hedge. |
| Inflation shock | Inflation pressure | Inflation breadth/surprise + real rates | $t+3$ | Reduce nominal duration, assess inflation hedges | Real-rate shock hurts hedges. |
| Liquidity tightening | Funding stress | Liquidity + volatility + credit | $t+1$, $t+3$ | De-risk leverage and illiquidity | Central-bank intervention reverses stress. |
| Yield curve | Policy and term premium | Curve slope/decomposition | $t+3$, $t+12$ | Duration, style, and FX tilts | Term premium or QE distorts signal. |
| Credit transition | Credit stress | Spread impulse | $t+1$, $t+3$ | Early warning and de-risking | Spread widening is technical or overprices risk. |
| Vol term structure | Volatility stress | IV curve, skew, realized vol | $t+1$, $t+3$ | Drawdown and hedge control | Volatility mean-reverts quickly. |
| Commodity carry | Inflation/growth mix | Futures curve + macro | $t+1$, $t+3$, $t+12$ | Commodity sleeve and inflation beta | Spot and futures returns diverge. |
| Combined conviction | Multi-regime | Macro + trend + carry + vol | All | Portfolio-aware allocation | Signal redundancy and overfitting. |

---

# 14.94 Practical Case Study Checklist

| Checklist Item | Required Standard |
|---|---|
| State the market setup | Identify the macro regime and asset transmission logic. |
| Define indicators | Specify raw source, transformation, lag, and availability. |
| Define regime classification | Use filtered real-time probabilities or pre-specified rules. |
| Define signal direction | Higher score must have consistent interpretation. |
| Define target | Absolute, excess, active, probability, quantile, or stress target. |
| Define horizon | $t+1$, $t+3$, $t+12$, or custom horizon. |
| Validate statistically | IC, rank IC, hit rate, spread, calibration, robust inference. |
| Validate economically | Turnover, costs, liquidity, drawdown, capacity, and constraints. |
| Identify failure modes | State when the model should lose confidence. |
| Define portfolio use | Risk budget, active tilt, hedge, or monitoring signal. |
| Store governance artifacts | Data version, model version, run manifest, validation report. |

---

# 14.95 Part 14 Summary

Part 14 translated the framework into eight applied case studies. The main lessons are:

1. Case studies should integrate macro reasoning, signal design, validation, portfolio implications, and risk management.
2. Growth slowdown signals are most useful when they distinguish disinflationary slowdowns from stagflationary slowdowns.
3. Inflation shock signals must separate inflation level, momentum, breadth, surprise, and policy reaction.
4. Liquidity tightening signals are often more valuable for drawdown control and leverage management than for mean-return forecasting.
5. Yield-curve signals require decomposition into real yields, breakevens, front-end policy expectations, and term premia.
6. Credit spread widening is often a transition indicator and should be modeled with both level and impulse features.
7. Volatility term structure is useful for equity drawdown risk but must be interpreted with option carry, skew, and hedge cost.
8. Commodity futures signals must distinguish spot returns from roll yield and collateral return.
9. Combined conviction models should diversify signal families while controlling redundancy, overfitting, and implementation frictions.
10. A production case study should always specify data availability, horizon, validation standard, portfolio use, risk controls, failure modes, and monitoring requirements.

---

# Stop Point

This installment completes:

1. **Part 14: Case Studies.**

Continue next with **Part 15: Summary, Glossary, and Practical Checklists**.
