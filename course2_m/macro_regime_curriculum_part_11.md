# Institutional Macro-Regime Detection, Multi-Asset Signal Identification, and Statistical Validation Curriculum

## Installment 11: Part 11 - Derivatives, Options, Futures, and Volatility Regime Signals

**Scope of this installment.** This installment continues the curriculum with **Part 11 only**. It assumes the global assumptions, timestamp conventions, feature engineering framework, return-target definitions, regime-detection concepts, causal-channel framework, signal-scoring framework, validation framework, machine-learning controls, regime-conditioned forecasting framework, and portfolio-integration framework established in Installments 1 through 10.

**Educational boundary.** This document is for research education, model design, and institutional portfolio-process development. It is not personalized investment advice, a live trading recommendation, or a guarantee of alpha.

---

# Part 11: Derivatives, Options, Futures, and Volatility Regime Signals

## 11.1 Purpose of Derivatives and Volatility Signal Research

Derivatives and volatility markets provide information that is not fully visible in cash asset returns. Futures curves reveal carry, scarcity, collateral, funding, inventory pressure, and hedging demand. Options surfaces reveal implied volatility, skew, term structure, convexity demand, event risk, and the market price of insurance. Volatility indices, variance swaps, and option strategy returns reveal how investors price uncertainty, tail risk, and path dependency.

In a macro-regime framework, derivatives signals serve four roles:

| Role | Question | Example Output |
|---|---|---|
| Market-implied macro information | What is the market pricing about growth, inflation, policy, or stress? | Futures curve steepening, rates-forward repricing, volatility term inversion. |
| Asset-level return forecast | Does a derivative signal forecast future returns? | Commodity backwardation as a futures return signal. |
| Risk and convexity forecast | Is downside convexity or volatility compensation attractive or dangerous? | Variance risk premium, skew premium, realized-volatility forecast. |
| Portfolio implementation input | What are the costs, margins, liquidity, nonlinear exposures, and roll dynamics? | Roll schedule, margin usage, theta decay, vega exposure, gamma risk. |

The central principle is that derivatives are not merely alternative instruments for expressing linear views. They are state-contingent contracts whose returns depend on path, carry, convexity, volatility, margin, financing, liquidity, and market microstructure. Therefore, derivative-based signals require more precise definitions than cash-asset signals.

## 11.2 Derivatives Data Foundation

A derivative research system must distinguish instrument data, curve data, surface data, strategy data, and risk data.

| Data Type | Examples | Key Fields | Main Bias Risk |
|---|---|---|---|
| Futures contracts | Equity index, rates, bond, FX, commodity futures | Contract code, expiry, price, volume, open interest, margin | Bad continuous-series construction and future-known roll rules. |
| Futures curves | Nearby to deferred contracts | Tenor, maturity, slope, carry, calendar spread | Liquidity differs across maturities. |
| FX forwards | Outright forwards, swaps, cross-currency basis | Spot, forward points, tenor, interest-rate differential | Holiday calendars and funding basis. |
| Options chains | Listed calls and puts | Strike, expiry, bid, ask, volume, open interest | Stale quotes and survivorship filters. |
| Volatility surfaces | IV by moneyness and maturity | Delta, strike, tenor, IV, skew, smile | Surface interpolation may use future data if rebuilt retrospectively. |
| Variance products | Variance swaps, VIX futures, volatility ETFs | Variance strike, realized variance, futures term structure | Product definitions and roll mechanics. |
| Greeks and risk | Delta, gamma, vega, theta, rho, vanna, volga | Model assumptions and surface timestamp | Greeks change with path and model choice. |
| Strategy returns | Covered calls, puts, straddles, delta-hedged options | Rebalance rule, collateral, margin, transaction cost | Missing intra-period path and execution assumptions. |

Every derivative signal must specify the timestamp of the quote, the construction convention, and the implementable exposure. A volatility surface observed after the close should not be used to trade at the same close unless the execution convention explicitly permits it.

## 11.3 Futures Return Decomposition

A collateralized futures position has return components that differ from spot asset returns. For a long futures strategy on contract $c$ from $t$ to $t+1$:

$$
r_{c,t+1}^{fut}=rac{F_{c,t+1}-F_{c,t}}{F_{c,t}},
$$

where $F_{c,t}$ is the futures price. A collateralized total return is:

$$
r_{t+1}^{collat	ext{-}fut}=r_{c,t+1}^{fut}+r_{t+1}^{collateral}-TC_{t+1},
$$

where $r^{collateral}$ is collateral return and $TC$ includes transaction costs, exchange fees, roll costs, slippage, and implementation frictions.

For a strategy that rolls from near contract $1$ to deferred contract $2$, a simplified expected roll yield proxy is:

$$
RY_t^{1,2}=\frac{F_{1,t}-F_{2,t}}{F_{1,t}},
$$

where $RY_t^{1,2}>0$ indicates backwardation under this convention and $RY_t^{1,2}<0$ indicates contango. The sign convention must always be stated because some systems define slope as $F_2/F_1-1$.

A stylized expected futures return can be written as:

$$
\mathbb{E}_t[R_{i,t,h}^{fut}]
=\mathbb{E}_t[R_{i,t,h}^{spot}]
+\mathbb{E}_t[R_{i,t,h}^{roll}]
+\mathbb{E}_t[R_{t,h}^{collateral}]
-\mathbb{E}_t[Costs_{i,t,h}].
$$

This equation clarifies that a futures signal may forecast spot movement, roll yield, collateral return, or some combination of all three.

## 11.4 Backwardation, Contango, Carry, and Collateral Return

Backwardation and contango are not trading signals by themselves. They are curve states that may reflect storage costs, convenience yield, scarcity, inventory pressure, financing, seasonality, hedging demand, and risk premia.

| Curve State | Simple Condition | Interpretation | Potential Signal Use | Failure Mode |
|---|---:|---|---|---|
| Backwardation | $F_{near}<F_{spot}$ or $F_{deferred}<F_{near}$ depending convention | Near-term scarcity or high convenience yield | Positive roll-yield candidate for long futures | Scarcity may resolve abruptly. |
| Contango | $F_{deferred}>F_{near}$ | Storage, financing, abundant supply, weak nearby demand | Negative roll warning for long futures | Contango can coexist with rising spot prices. |
| Steepening curve | Deferred price rises relative to nearby | Changing inventory or inflation expectations | Macro regime indicator | Seasonal effects can dominate. |
| Flattening curve | Near and deferred prices converge | Normalization or demand shock | Carry and transition signal | Contract liquidity distortions. |
| Collateral support | Cash yield is high | Futures total return boosted by collateral | Rates-linked return component | Collateral assumptions differ by vehicle. |

A generic carry signal for futures can be defined as:

$$
Carry_{i,t}=RY_{i,t}^{roll}+r_t^{collateral}-ExpectedCost_{i,t}.
$$

For cross-sectional ranking, the carry score is often standardized across contracts:

$$
s_{i,t}^{carry}=\frac{Carry_{i,t}-\mathrm{median}_{j\in\mathcal{U}_t}(Carry_{j,t})}{\mathrm{MAD}_{j\in\mathcal{U}_t}(Carry_{j,t})},
$$

where $\mathcal{U}_t$ is the point-in-time futures universe and $\mathrm{MAD}$ is median absolute deviation.

## 11.5 Rates Futures, Bond Futures, and Policy Signals

Rates futures and OIS curves embed market expectations for policy paths, term premia, liquidity, and risk compensation. A policy-rate expectation for horizon $h$ may be proxied by futures-implied rates:

$$
\hat i_{t+h|t}^{mkt}=f_{t,h},
$$

where $f_{t,h}$ is the market-implied forward rate. A policy repricing signal can be:

$$
\Delta f_{t}^{(k,h)}=f_{t,h}-f_{t-k,h}.
$$

A hawkish repricing feature may be positive when front-end implied rates rise:

$$
PolicyTighteningSignal_t=z_t(\Delta f_t^{(3,12)}),
$$

where $z_t(\cdot)$ is a historical-only standardization. This signal may affect duration, equity styles, FX carry, gold, and credit through real-rate and liquidity channels.

For bond futures, the deliverable basket and cheapest-to-deliver option must be considered. A bond futures return is not simply the return of a constant-maturity cash bond. It can be affected by conversion factors, delivery optionality, basis, financing, repo specialness, and roll.

## 11.6 Equity Index Futures and Dividend-Implied Signals

Equity index futures embed financing, dividends, and index carry. Under a simplified cost-of-carry model:

$$
F_t=S_t e^{(r_t-q_t)(T-t)},
$$

where $F_t$ is futures price, $S_t$ is spot index level, $r_t$ is financing rate, $q_t$ is dividend yield, and $T-t$ is time to maturity in years. The implied dividend yield can be approximated as:

$$
q_t \approx r_t - \frac{1}{T-t}\log\left(\frac{F_t}{S_t}\right).
$$

Dividend-implied signals can matter for equity valuation and sector rotation, but they are sensitive to financing rates, index dividend assumptions, tax effects, and contract conventions.

Equity futures also provide information about positioning and liquidity through volume, open interest, basis, and roll pressure. However, open interest should not be interpreted mechanically; it reflects both long and short positions and can rise during hedging or speculative activity.

## 11.7 Commodity Futures Signals

Commodity futures signals often include carry, curve slope, inventory pressure, seasonality, trend, inflation sensitivity, and dollar sensitivity.

A curve slope feature for commodity $i$ can be:

$$
Slope_{i,t}^{1,6}=\frac{F_{i,t}^{6m}}{F_{i,t}^{1m}}-1.
$$

A backwardation score using the opposite orientation can be:

$$
BackwardationScore_{i,t}=-z_t(Slope_{i,t}^{1,6}).
$$

A commodity carry and trend composite may be:

$$
Signal_{i,t}^{cmdty}=w_c s_{i,t}^{carry}+w_m s_{i,t}^{momentum}+w_v s_{i,t}^{inventory},
$$

where weights are pre-specified or estimated in a walk-forward process.

Commodity signals are highly regime-dependent. Carry can work during stable inventory cycles but fail during supply shocks, geopolitical disruptions, or sharp demand collapses. Inflation regimes can support commodity risk premia, while liquidity tightening can pressure leveraged commodity exposures.

## 11.8 FX Forwards and Currency Carry

FX forward pricing links spot exchange rates and interest-rate differentials. Under covered interest parity in simplified form:

$$
F_{F/B,t}=S_{F/B,t}\frac{1+i_F\Delta t}{1+i_B\Delta t},
$$

where $F_{F/B,t}$ is the forward rate, $S_{F/B,t}$ is spot, $i_F$ is foreign interest rate, $i_B$ is base-currency interest rate, and $\Delta t$ is the year fraction.

FX carry for foreign currency $F$ versus base $B$ is:

$$
Carry_{F/B,t}\approx i_F-i_B-basis_{F/B,t}-TC_{F/B,t},
$$

where $basis$ captures deviations from covered-interest parity and funding frictions. A carry signal may be profitable in calm regimes but vulnerable during dollar funding stress, risk-off shocks, and deleveraging.

A regime-conditioned FX carry signal can be written as:

$$
\hat\mu_{F/B,t,h}^{carry}=\beta_h Carry_{F/B,t}\cdot (1-\pi_{stress,t}),
$$

where $\pi_{stress,t}$ is the probability of liquidity or risk-off stress. This reduces carry conviction when stress probability is high.

## 11.9 Options Surface Basics

An option surface maps implied volatility across strike or delta and maturity. Let $\sigma_{imp}(K,T)$ denote implied volatility for strike $K$ and maturity $T$. Common surface features include:

| Surface Feature | Formula or Proxy | Interpretation |
|---|---:|---|
| ATM implied volatility | $\sigma_{ATM,t}(T)$ | Price of near-the-money uncertainty. |
| Realized volatility | $RV_{t,W}$ | Recent actual volatility. |
| Variance risk premium | $IV_t^2-RV_t^2$ | Implied variance compensation over realized variance proxy. |
| Skew | $\sigma_{25\Delta put}-\sigma_{25\Delta call}$ | Downside insurance demand. |
| Term structure | $\sigma_{short}-\sigma_{long}$ | Near-term event risk or stress. |
| Vol-of-vol | Volatility of implied volatility | Instability of uncertainty pricing. |
| Smile convexity | Curvature across strikes | Tail demand or jump-risk pricing. |

Surface construction must specify whether moneyness is strike-based, forward-moneyness-based, delta-based, or standardized by volatility. Delta conventions differ across asset classes and vendors.

## 11.10 Implied Volatility, Realized Volatility, and Variance Risk Premium

Realized variance over $W$ daily observations can be estimated as:

$$
RV_{t,W}^2=\frac{A}{W}\sum_{j=1}^{W}r_{t-j+1}^{2},
$$

where $A$ is the annualization factor and $r$ is daily log return. Implied variance is approximately:

$$
IV_t^2=\sigma_{imp,t}^2.
$$

A variance risk premium proxy is:

$$
VRP_t=IV_t^2-RV_{t,W}^2.
$$

A positive $VRP_t$ may indicate that option sellers are compensated for bearing variance risk. It may also indicate that crash insurance is expensive because tail risk is elevated. Therefore, VRP is not automatically a short-volatility signal.

A forecast target for variance strategy returns might be:

$$
Y_{t,h}^{var}=RV_{t\rightarrow t+h}^2-IV_t^2-Cost_t,
$$

for long variance exposure, or the negative of this value for short variance exposure. The exact payoff depends on the variance swap or option strategy construction.

## 11.11 Skew Premium and Tail-Risk Demand

Equity index skew often reflects demand for downside protection. A simple skew feature is:

$$
Skew_t=\sigma_{25\Delta put,t}-\sigma_{25\Delta call,t}.
$$

A standardized skew pressure signal is:

$$
SkewPressure_t=z_t(Skew_t).
$$

High skew may imply expensive downside insurance. But it can also warn that investors are worried about tail risk. The investment meaning depends on whether the strategy is selling skew, buying protection, or using skew as a risk-off indicator.

| Skew Signal Use | Possible Interpretation | Main Risk |
|---|---|---|
| Sell expensive puts | Collect skew premium | Crash risk and negative convexity. |
| Buy cheap calls/puts | Convexity may be underpriced | Persistent theta bleed. |
| Risk-off indicator | High skew signals hedging demand | Skew can remain high for long periods. |
| Regime input | Tail demand reflects stress probability | Surface distortions and liquidity effects. |

## 11.12 Volatility Term Structure and Stress Regimes

Volatility term structure compares short-tenor and long-tenor implied volatility:

$$
VTS_t=\sigma_{short,t}-\sigma_{long,t}.
$$

When short implied volatility exceeds long implied volatility, the term structure is inverted:

$$
VTS_t>0.
$$

This often indicates near-term stress, event risk, or hedging pressure. A volatility stress probability can be modeled as:

$$
\Pr(Stress_t=1)=\frac{1}{1+\exp[-(\alpha+\beta_1 z(VTS_t)+\beta_2 z(Skew_t)+\beta_3 z(CreditImpulse_t))]}.
$$

Volatility term-structure signals are useful for equity drawdown risk, volatility strategy allocation, and risk-budget scaling. However, they can be unstable around known events such as elections, central-bank meetings, earnings seasons, and geopolitical deadlines.

## 11.13 Delta-Hedged Option Returns

A delta-hedged option return attempts to isolate volatility and convexity exposure from directional exposure. For option value $V(S_t,\sigma_t,t)$, a discrete delta-hedged P&L approximation is:

$$
\Delta \Pi_t \approx \Delta V_t - \Delta_{t-1}\Delta S_t - TC_t.
$$

Using Greeks, the option value change can be approximated as:

$$
\Delta V_t \approx
\Delta\Delta S_t + \frac{1}{2}\Gamma(\Delta S_t)^2 + \nu\Delta\sigma_t + \Theta\Delta t + \rho\Delta r_t.
$$

After delta hedging, the directional term is reduced, leaving:

$$
\Delta \Pi_t \approx \frac{1}{2}\Gamma(\Delta S_t)^2 + \nu\Delta\sigma_t + \Theta\Delta t + \rho\Delta r_t - TC_t + HedgeError_t.
$$

This expression clarifies why delta-hedged returns depend on realized volatility, implied volatility changes, time decay, rates, transaction costs, hedge frequency, jumps, and discrete hedging error.

## 11.14 Option Strategy Returns as Asset-Level Observations

Option strategies can be modeled as asset return series if their construction is fully specified. Examples include covered calls, put writing, protective puts, collars, straddles, strangles, butterflies, variance carry, dispersion, and volatility trend strategies.

A generic option strategy return is:

$$
R_{s,t+1}^{opt}=\frac{NAV_{s,t+1}-NAV_{s,t}+CollateralIncome_t-Fees_t}{Capital_{s,t}},
$$

where $s$ identifies the strategy, $NAV$ is marked strategy value, and $Capital$ may be premium, margin, notional, or risk-budget capital. The capital definition must be explicit.

| Strategy | Primary Exposure | Common Signal | Key Failure Mode |
|---|---|---|---|
| Put writing | Short downside convexity | High skew or VRP | Large crash loss. |
| Covered call | Equity beta plus short call | High call IV | Upside truncation in rallies. |
| Long straddle | Long volatility and convexity | Low IV versus expected RV | Theta decay. |
| Short straddle | Short volatility | High IV versus expected RV | Jump and gap risk. |
| Collar | Long equity with downside hedge | Skew and carry balance | Costly protection or capped upside. |
| Dispersion | Index-versus-single-name vol | Correlation risk premium | Correlation spike. |
| Variance carry | Short variance premium | Positive VRP | Volatility shock. |

## 11.15 Volatility Regime Signals and Macro Regimes

Volatility regimes interact with macro regimes. A low-volatility expansion is very different from a low-volatility late-cycle liquidity bubble. A high-volatility disinflationary recession is different from a high-volatility inflation shock.

A volatility regime vector can be:

$$
Z_t^{vol}=\left[z(IV_t),z(RV_t),z(VRP_t),z(Skew_t),z(VTS_t),z(Corr_t)\right].
$$

A combined macro-volatility regime probability can be:

$$
\Pr(S_t=k,V_t=l\mid\mathcal{F}_t)=\Pr(S_t=k\mid\mathcal{F}_t)\Pr(V_t=l\mid S_t=k,\mathcal{F}_t),
$$

where $S_t$ is macro regime and $V_t$ is volatility regime. This structure allows volatility signals to be conditioned on the macro backdrop.

| Macro Regime | Volatility State | Strategy Implication |
|---|---|---|
| Disinflationary expansion | Low vol, positive VRP | Carry and equity risk may be supported, but complacency risk should be monitored. |
| Growth slowdown | Rising vol, widening credit | Reduce short-convexity exposure and monitor drawdown risk. |
| Inflation shock | Rates vol and FX vol elevated | Duration and currency option signals become more important. |
| Liquidity stress | Vol term inversion, high skew | De-risk short-vol and levered carry; convex hedges may be valuable despite cost. |

## 11.16 Convexity Demand and Regime Transitions

Convexity demand measures the market's willingness to pay for nonlinear payoff protection or upside participation. It can be proxied by implied volatility, skew, kurtosis pricing, variance swap levels, option volume, put-call ratios, and dealer gamma exposure.

A convexity demand score might be:

$$
CD_t=w_1z(IV_t)+w_2z(Skew_t)+w_3z(VTS_t)+w_4z(PutCall_t)+w_5z(VolOfVol_t),
$$

with weights $w_j$ pre-specified or estimated with strong validation controls. High convexity demand may indicate stress, expensive insurance, or approaching regime transition. Low convexity demand may indicate complacency, cheap optionality, or genuinely stable conditions.

Convexity demand should not be used alone. It should be interpreted alongside realized volatility, liquidity, credit stress, macro momentum, and policy risk.

## 11.17 Margin, Liquidity, Financing, and Path Dependency

Derivative strategies are strongly affected by implementation frictions.

| Friction | Definition | Portfolio Effect |
|---|---|---|
| Initial margin | Capital posted to initiate a position | Reduces leverage capacity. |
| Variation margin | Daily mark-to-market cash flow | Creates liquidity needs during losses. |
| Bid-ask spread | Difference between buy and sell quotes | Reduces expected return, especially for options. |
| Market impact | Price concession from trading size | Limits capacity. |
| Financing | Cost of collateral, borrow, or leverage | Changes net carry. |
| Roll cost | Cost of moving exposure across maturities | Important for futures and volatility products. |
| Discrete hedging | Hedge error from non-continuous rebalancing | Important for delta-hedged options. |
| Gap risk | Price jump between hedge times | Creates losses beyond model estimates. |
| Path dependency | Outcome depends on sequence, not only endpoint | Critical for options, volatility, and leveraged products. |

A net expected return should be:

$$
\hat\mu_{net}=\hat\mu_{gross}-TC-BidAsk-MarketImpact-Financing-MarginCost-RollCost-HedgeCost.
$$

If this adjustment turns the forecast negative, the signal may still be informative but not implementable.

## 11.18 Derivatives Signal Taxonomy

| Signal Family | Features | Target | Horizon | Main Risk |
|---|---|---|---:|---|
| Futures carry | Roll yield, collateral, curve slope | Futures return | $t+1$ to $t+12$ | Curve state reflects crash risk. |
| Commodity scarcity | Backwardation, inventories, spreads | Commodity futures return | $t+1$ to $t+6$ | Seasonality and supply shocks. |
| FX carry | Rate differential, basis, risk appetite | FX total return | $t+1$ to $t+12$ | Funding stress and crash risk. |
| Policy repricing | Rates futures changes | Duration, FX, equity style | $t+1$ to $t+6$ | Expectations already priced. |
| VRP | IV minus expected RV | Variance strategy return | $t+1$ | Tail risk and jumps. |
| Skew premium | Put-call IV spread | Skew-selling or risk-off target | $t+1$ to $t+3$ | Crash loss. |
| Vol term structure | Short minus long IV | Drawdown and vol strategy return | $t+1$ | Event-specific distortions. |
| Convexity demand | IV, skew, vol-of-vol, option volume | Regime transition and hedge value | $t+1$ to $t+3$ | Expensive insurance may stay expensive. |
| Correlation premium | Index vol versus component vol | Dispersion return | $t+1$ to $t+3$ | Correlation spike. |
| Dealer gamma proxy | Estimated dealer gamma exposure | Intraday realized volatility | Short horizon | Positioning estimates are noisy. |

## 11.19 Python: Futures Curve and Carry Signal Construction

```python
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class FuturesCurveConfig:
    """Configuration for futures curve signals."""
    near_tenor: str = "1m"
    deferred_tenor: str = "6m"
    min_obs: int = 36
    z_window: int = 60


def validate_panel(df: pd.DataFrame, name: str = "df") -> None:
    """Validate a date-asset MultiIndex panel."""
    if not isinstance(df.index, pd.MultiIndex):
        raise TypeError(f"{name} must have MultiIndex(date, asset).")
    if df.index.names[0] != "date":
        raise ValueError("First index level should be named 'date'.")
    if df.empty:
        raise ValueError(f"{name} cannot be empty.")


def robust_zscore_by_asset(x: pd.Series, window: int = 60, min_obs: int = 36) -> pd.Series:
    """Compute historical-only robust z-score by asset."""
    def _one_asset(s: pd.Series) -> pd.Series:
        hist = s.shift(1)
        med = hist.rolling(window, min_periods=min_obs).median()
        mad = (hist - med).abs().rolling(window, min_periods=min_obs).median()
        return (s - med) / (1.4826 * mad.replace(0.0, np.nan))
    return x.groupby(level="asset", group_keys=False).apply(_one_asset)


def futures_curve_signals(curve_panel: pd.DataFrame, cfg: FuturesCurveConfig) -> pd.DataFrame:
    """Create futures curve slope, backwardation, and carry proxy signals.

    curve_panel must have MultiIndex(date, asset) and columns for tenors such
    as '1m', '3m', '6m'. Prices should be point-in-time futures prices.
    """
    validate_panel(curve_panel, "curve_panel")
    needed = {cfg.near_tenor, cfg.deferred_tenor}
    missing = needed - set(curve_panel.columns)
    if missing:
        raise KeyError(f"Missing tenor columns: {sorted(missing)}")

    out = pd.DataFrame(index=curve_panel.index)
    near = curve_panel[cfg.near_tenor].astype(float)
    deferred = curve_panel[cfg.deferred_tenor].astype(float)
    out["curve_slope"] = deferred / near - 1.0
    out["backwardation_raw"] = -out["curve_slope"]
    out["backwardation_z"] = robust_zscore_by_asset(
        out["backwardation_raw"], window=cfg.z_window, min_obs=cfg.min_obs
    )
    return out.replace([np.inf, -np.inf], np.nan)
```

## 11.20 Python: Volatility Surface Signal Construction

```python
def volatility_surface_signals(surface: pd.DataFrame, min_obs: int = 36) -> pd.DataFrame:
    """Construct IV, skew, term-structure, and VRP signals.

    surface is indexed by date and may contain columns:
    atm_1m_iv, atm_3m_iv, put_25d_1m_iv, call_25d_1m_iv, realized_vol_1m.
    Volatility inputs should be annualized decimal values, not percentages.
    """
    required = ["atm_1m_iv", "atm_3m_iv", "put_25d_1m_iv", "call_25d_1m_iv", "realized_vol_1m"]
    missing = set(required) - set(surface.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")
    if not isinstance(surface.index, pd.DatetimeIndex):
        raise TypeError("surface must have DatetimeIndex.")

    x = surface.astype(float).copy()
    out = pd.DataFrame(index=x.index)
    out["iv_level"] = x["atm_1m_iv"]
    out["vrp"] = x["atm_1m_iv"] ** 2 - x["realized_vol_1m"] ** 2
    out["skew"] = x["put_25d_1m_iv"] - x["call_25d_1m_iv"]
    out["vol_term_structure"] = x["atm_1m_iv"] - x["atm_3m_iv"]

    hist = out.shift(1)
    mu = hist.rolling(60, min_periods=min_obs).mean()
    sd = hist.rolling(60, min_periods=min_obs).std(ddof=1).replace(0.0, np.nan)
    z = (out - mu) / sd
    z.columns = [f"{c}_z" for c in z.columns]
    return pd.concat([out, z], axis=1).replace([np.inf, -np.inf], np.nan)
```

## 11.21 Python: Delta-Hedged Option P&L Approximation

```python
def delta_hedged_option_pnl(
    option_value: pd.Series,
    underlying_price: pd.Series,
    delta: pd.Series,
    transaction_cost: pd.Series | float = 0.0,
) -> pd.Series:
    """Approximate discrete delta-hedged option P&L.

    The hedge uses prior-period delta. Positive P&L means the option position
    plus hedge gained value. Inputs must be aligned and point-in-time.
    """
    df = pd.concat(
        [
            option_value.rename("option_value"),
            underlying_price.rename("underlying"),
            delta.rename("delta"),
        ],
        axis=1,
    ).dropna().astype(float)
    if isinstance(transaction_cost, pd.Series):
        df["tc"] = transaction_cost.reindex(df.index).fillna(0.0).astype(float)
    else:
        df["tc"] = float(transaction_cost)

    dV = df["option_value"].diff()
    dS = df["underlying"].diff()
    hedge_pnl = -df["delta"].shift(1) * dS
    pnl = dV + hedge_pnl - df["tc"]
    return pnl.rename("delta_hedged_pnl")
```

## 11.22 Python: Option Strategy Return Engine

```python
def option_strategy_returns(
    nav: pd.Series,
    capital: pd.Series,
    collateral_income: pd.Series | float = 0.0,
    fees: pd.Series | float = 0.0,
) -> pd.Series:
    """Compute option strategy returns from NAV and capital base."""
    df = pd.concat([nav.rename("nav"), capital.rename("capital")], axis=1).dropna().astype(float)
    if (df["capital"] <= 0).any():
        raise ValueError("capital must be positive.")
    if isinstance(collateral_income, pd.Series):
        df["collateral"] = collateral_income.reindex(df.index).fillna(0.0).astype(float)
    else:
        df["collateral"] = float(collateral_income)
    if isinstance(fees, pd.Series):
        df["fees"] = fees.reindex(df.index).fillna(0.0).astype(float)
    else:
        df["fees"] = float(fees)

    ret = (df["nav"].diff() + df["collateral"] - df["fees"]) / df["capital"].shift(1)
    return ret.replace([np.inf, -np.inf], np.nan).rename("strategy_return")
```

## 11.23 Python: Volatility-Regime Classifier

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture


def fit_volatility_regime_model(vol_features: pd.DataFrame, n_states: int = 3, random_state: int = 42):
    """Fit a Gaussian mixture volatility-regime model.

    For production, this model should be fit inside a walk-forward loop. This
    function is a diagnostic prototype using available historical features.
    """
    x = vol_features.replace([np.inf, -np.inf], np.nan).dropna().astype(float)
    if len(x) < 60:
        raise ValueError("At least 60 observations are recommended.")
    scaler = StandardScaler()
    z = scaler.fit_transform(x)
    model = GaussianMixture(
        n_components=n_states,
        covariance_type="full",
        reg_covar=1e-5,
        n_init=20,
        random_state=random_state,
    )
    labels = model.fit_predict(z)
    probs = model.predict_proba(z)
    prob_df = pd.DataFrame(probs, index=x.index, columns=[f"vol_state_{k}_prob" for k in range(n_states)])
    label_s = pd.Series(labels, index=x.index, name="vol_state")
    return {"scaler": scaler, "model": model, "labels": label_s, "probabilities": prob_df}
```

## 11.24 Python: Regime-Conditioned Derivatives Conviction

```python
def derivatives_conviction_score(
    expected_return: pd.Series,
    expected_vol: pd.Series,
    carry_score: pd.Series,
    convexity_risk: pd.Series,
    liquidity_score: pd.Series,
    stress_probability: float,
    scale: float = 1.0,
) -> pd.Series:
    """Compute a bounded derivatives conviction score.

    Higher convexity_risk reduces conviction for short-convexity strategies.
    stress_probability should be between 0 and 1.
    """
    if not 0 <= stress_probability <= 1:
        raise ValueError("stress_probability must be between 0 and 1.")
    df = pd.concat(
        [
            expected_return.rename("mu"),
            expected_vol.rename("vol"),
            carry_score.rename("carry"),
            convexity_risk.rename("convexity_risk"),
            liquidity_score.rename("liquidity"),
        ],
        axis=1,
    ).replace([np.inf, -np.inf], np.nan).dropna()
    if (df["vol"] <= 0).any():
        raise ValueError("expected_vol must be positive.")

    stress_penalty = 1.0 - stress_probability
    raw = (df["mu"] / df["vol"]) * (1.0 + 0.25 * df["carry"]) * df["liquidity"]
    raw = raw - 0.50 * df["convexity_risk"].clip(lower=0.0)
    raw = raw * stress_penalty
    return pd.Series(np.tanh(raw / scale), index=df.index, name="derivatives_conviction")
```

## 11.25 Visualization Code for Derivatives Signals

```python
import matplotlib.pyplot as plt


def plot_futures_curve(curve_row: pd.Series, title: str = "Futures Curve") -> None:
    """Plot one futures curve snapshot."""
    fig, ax = plt.subplots(figsize=(8, 4))
    curve_row.astype(float).plot(marker="o", ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Tenor")
    ax.set_ylabel("Futures price")
    plt.tight_layout()
    plt.show()


def plot_vol_surface_signals(signals: pd.DataFrame, cols: list[str]) -> None:
    """Plot selected volatility surface signals."""
    fig, ax = plt.subplots(figsize=(10, 4))
    signals[cols].dropna().plot(ax=ax)
    ax.axhline(0.0, linewidth=1)
    ax.set_title("Volatility Surface Signals")
    ax.set_xlabel("Date")
    plt.tight_layout()
    plt.show()


def plot_regime_probabilities(prob: pd.DataFrame, title: str = "Volatility Regime Probabilities") -> None:
    """Plot volatility regime probabilities."""
    fig, ax = plt.subplots(figsize=(10, 4))
    prob.plot(ax=ax)
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Probability")
    plt.tight_layout()
    plt.show()
```

## 11.26 Validation Requirements for Derivative Signals

Derivative signals require all validation controls from Part 7, plus additional instrument-specific checks.

| Validation Area | Required Check |
|---|---|
| Curve construction | Continuous futures series uses realistic roll rules and no future-known contract selection. |
| Surface construction | IV surface inputs are timestamped, tradable, and not retrospectively smoothed with future information. |
| Transaction costs | Bid-ask, slippage, commissions, exchange fees, and market impact included or disclosed. |
| Margin and capital | Returns are calculated relative to an explicit capital base. |
| Collateral | Collateral return convention is specified. |
| Liquidity | Volume, open interest, stale quote, and capacity filters are point-in-time. |
| Path dependency | Intra-period risk is considered for options and leveraged products. |
| Tail risk | Skew, kurtosis, gap risk, and stress losses are evaluated. |
| Regime dependence | Signal performance is tested by macro, volatility, liquidity, and credit regimes. |
| Roll sensitivity | Alternative roll schedules are tested. |
| Model Greeks | Greek estimates are tied to a documented pricing model and surface. |
| Backtest realism | Execution timing, hedge frequency, and rebalance rules are explicit. |

## 11.27 Common Failure Modes

1. **Treating futures carry as free yield.** Carry may compensate for crash risk, inventory risk, liquidity risk, or financing constraints.
2. **Ignoring roll methodology.** Continuous futures returns are highly sensitive to roll schedule and contract selection.
3. **Using stale option quotes.** Illiquid strikes can distort skew and implied volatility features.
4. **Overlooking bid-ask spreads.** Option strategies can look attractive gross and fail net of spreads.
5. **Misdefining capital base.** Premium return, notional return, margin return, and risk-budget return are different.
6. **Assuming delta hedging is continuous.** Discrete hedging creates jump and path risk.
7. **Interpreting high VRP as automatically attractive.** High insurance premium may signal genuine tail risk.
8. **Ignoring margin calls.** Variation margin can force liquidation at the worst time.
9. **Using smoothed surfaces.** Retrospective interpolation can hide real-time quote uncertainty.
10. **Treating volatility products as spot volatility.** VIX futures and volatility ETFs have roll and path mechanics.
11. **Ignoring regime interactions.** Short-vol and carry signals often fail during liquidity stress.
12. **Confusing hedge value with expected return.** A hedge may have negative expected return and still improve portfolio utility.

## 11.28 Production Checklist for Derivatives Research

| Checklist Item | Required Standard |
|---|---|
| Instrument master | Contract identifiers, expiries, multipliers, tick values, calendars, and margin rules. |
| Curve builder | Point-in-time roll rules, liquidity filters, and back-adjustment policy. |
| Option chain cleaner | Bid-ask filters, stale quote detection, no-arbitrage checks, moneyness mapping. |
| Surface builder | Timestamped interpolation with documented delta and tenor conventions. |
| Greeks engine | Pricing model, rates, dividends, forwards, and volatility inputs documented. |
| Strategy simulator | Rebalance, hedge, collateral, margin, and cost assumptions explicit. |
| Risk engine | Delta, gamma, vega, theta, skew, convexity, and stress exposures reported. |
| Validation module | IC, spread, OOS, bootstrap, stress, and regime-conditioned diagnostics. |
| Governance | Frozen specifications, model registry, audit logs, and monitoring alerts. |
| Monitoring | Quote quality, margin changes, liquidity drops, surface jumps, and signal decay. |

## 11.29 Part 11 Summary

Part 11 developed the derivatives, options, futures, and volatility-signal layer of the macro-regime research process. The main lessons are:

1. Derivatives signals contain market-implied information about carry, scarcity, policy expectations, volatility, skew, convexity, liquidity, and tail demand.
2. Futures returns must separate spot movement, roll yield, collateral return, transaction cost, and financing assumptions.
3. Backwardation and contango are curve states, not automatic signals; their meaning depends on inventory, hedging demand, seasonality, and regime context.
4. Rates futures, bond futures, equity futures, FX forwards, and commodity futures each require instrument-specific construction and risk controls.
5. Option signals require full surface definitions, including implied volatility, realized volatility, variance risk premium, skew, term structure, vol-of-vol, and moneyness convention.
6. Delta-hedged option returns depend on realized volatility, implied-volatility changes, theta, rates, discrete hedging, transaction costs, and gap risk.
7. Option strategy returns can be treated as asset-level observations only when strategy construction, capital base, margin, collateral, and costs are explicit.
8. Volatility regimes interact with macro regimes; short-volatility, carry, and convexity-selling signals are especially vulnerable during liquidity and credit stress.
9. Convexity demand can signal stress, expensive insurance, or regime transition, but it must be interpreted with macro, credit, liquidity, and realized-volatility context.
10. Derivative signal validation must include cost realism, margin, path dependency, liquidity, stale quotes, roll sensitivity, surface quality, and regime-stratified performance.

---

# Stop Point

This installment completes:

1. **Part 11: Derivatives, Options, Futures, and Volatility Regime Signals.**

Continue next with **Part 12: Risk Management, Stress Testing, and Failure Modes**.
