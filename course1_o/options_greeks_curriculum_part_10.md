# Institutional Options Greeks, Systematic Strategy, and Regime-Aware Portfolio Construction Curriculum

## Completed Installment

This installment contains:

- Part 10: Institutional Research Pipeline and Backtesting Framework.

The document is educational and research-oriented. It is not personalized investment advice, a live trading recommendation, or a claim that any option strategy produces guaranteed alpha.

---

# Part 10: Institutional Research Pipeline and Backtesting Framework

**Level:** Expert

## 10.1 Purpose of Part 10

Parts 1 through 9 developed the theoretical and portfolio-risk foundation for options research: pricing, Greeks, higher-order sensitivities, hedging, volatility surfaces, systematic alpha hypotheses, regime-aware allocation, portfolio construction, covariance stabilization, and stress testing. Part 10 turns those components into an institutional research and backtesting workflow.

The purpose of an options backtest is not merely to ask whether a strategy had attractive historical returns. A proper backtest should answer a stronger question:

$$
\text{Could this strategy have been identified, traded, hedged, funded, risk-managed, and monitored using only information available at the time?}
$$

This question is harder for options than for many linear assets because options data are high-dimensional, path-dependent, sparse, noisy, and sensitive to implementation assumptions. A small error in timestamping, dividend treatment, contract adjustment, implied-volatility inversion, bid-ask execution, or earnings-date availability can completely change research conclusions.

The core principle of Part 10 is:

$$
\text{Options backtesting must be point-in-time, executable, cost-aware, path-aware, and risk-attributed.}
$$

An institutional-grade research pipeline should produce not only a performance series, but also:

- clean option-chain data;
- validated implied volatilities and Greeks;
- point-in-time signal values;
- trade decisions and rejected candidates;
- execution assumptions;
- hedge trades;
- cash, financing, borrow, and margin accounting;
- P&L attribution;
- risk limit usage;
- stress-test outputs;
- audit logs;
- reproducible model versions.

## 10.2 Backtesting Philosophy: What Is Being Tested?

A common mistake is to backtest a vague strategy label such as "sell expensive options" or "buy convexity when volatility is cheap." Institutional research must define the exact object being tested.

A complete options strategy definition includes:

| Component | Required Definition |
|---|---|
| Universe | Which underlyings, exchanges, option types, maturities, strikes, and liquidity filters are eligible? |
| Signal | What point-in-time variables rank or select trades? |
| Position construction | Which option legs are bought or sold, at what strikes and maturities? |
| Sizing | How are positions scaled by premium, notional, Greek exposure, margin, or risk? |
| Execution | Are trades done at bid, ask, mid, midpoint plus slippage, or modelled limit fills? |
| Hedging | Is delta hedged? How often? Using what instrument and cost model? |
| Rebalancing | When are trades opened, rolled, adjusted, stopped, or closed? |
| Risk limits | What Greek, loss, margin, liquidity, and concentration constraints apply? |
| Accounting | How are cash, premium, financing, borrow, fees, and margin handled? |
| Attribution | How is P&L decomposed into delta, gamma, theta, vega, skew, costs, and residuals? |
| Validation | Which out-of-sample periods, stress periods, and robustness tests are required? |

Without these definitions, a backtest is not a research result. It is a historical simulation with hidden assumptions.

## 10.3 Required Data for Institutional Options Research

Options research requires multiple synchronized datasets. The data requirement is broader than option prices.

## 10.3.1 Option Chain Data

At minimum, each option quote record should include:

| Field | Description |
|---|---|
| timestamp | Exact quote timestamp or end-of-day timestamp |
| underlying_id | Stable identifier for the underlying |
| option_id | Stable option contract identifier |
| root_symbol | Option root |
| expiration | Expiration date |
| strike | Strike price |
| option_type | Call or put |
| exercise_style | European, American, Bermudan, or other |
| settlement_type | Physical or cash settlement |
| multiplier | Contract multiplier |
| bid | Best bid or closing bid |
| ask | Best ask or closing ask |
| last | Last traded price if available |
| volume | Option volume |
| open_interest | Open interest |
| quote_condition | Validity or exchange quote condition |
| exchange | Listing exchange or consolidated source |

For robust research, option-chain data should also include quote timestamp quality, stale-quote flags, and corporate-action adjustment history.

## 10.3.2 Underlying Price Data

Underlying data should include:

- open, high, low, close, and adjusted close;
- intraday prices if hedging is intraday;
- volume and dollar volume;
- corporate actions;
- splits;
- dividends;
- identifier mapping through ticker changes;
- delisting returns;
- index membership and weights if relevant.

The underlying price used for option pricing should be timestamp-aligned with the option quote. A mismatch between option close and underlying close can create false implied-volatility signals.

## 10.3.3 Rates, Dividends, Borrow, and Funding

Pricing and hedging require carry inputs:

| Input | Why It Matters |
|---|---|
| risk-free curve | Discounting, forward pricing, rho |
| dividend forecasts | Equity forwards, early exercise, put-call parity |
| realized dividends | Ex-post validation and corporate-action checks |
| borrow rates | Short-stock hedge cost and hard-to-borrow parity effects |
| funding rates | Premium financing and cash account returns |
| margin rates | Capital cost and leverage constraints |

For single-stock options, discrete dividends and borrow costs should not be treated as minor details. They can materially affect option values, early exercise, and synthetic forward relationships.

## 10.3.4 Event Data

Event data are essential for single-stock options and macro-sensitive option strategies.

Required event datasets may include:

- earnings announcement dates and times;
- ex-dividend dates and dividend amounts;
- special dividends;
- stock splits;
- mergers, spin-offs, and corporate actions;
- index inclusion or deletion events;
- macro release calendars;
- central-bank meetings;
- futures expiries;
- option expiration calendars;
- holidays and trading sessions.

The critical requirement is timestamp availability. If an earnings date was revised later, the backtest must know what date was known at the time of trade.

## 10.3.5 Volatility Surface Data

A volatility surface dataset may be built internally from option chains or obtained from a vendor. It should contain:

- implied volatility by strike and maturity;
- surface construction method;
- interpolation and extrapolation rules;
- arbitrage-cleaning flags;
- at-the-money volatility;
- skew features;
- curvature features;
- term-structure features;
- model version;
- timestamp.

Surface data must be reproducible. If a vendor updates historical surfaces, the research database should store the version used in each backtest.

## 10.3.6 Execution and Liquidity Data

Execution assumptions require liquidity data:

- bid-ask spreads;
- option volume;
- open interest;
- underlying volume;
- market depth if available;
- intraday spread profiles;
- realized slippage;
- commissions and exchange fees;
- borrow and locate availability;
- hard-to-borrow flags;
- margin requirements.

A strategy that only works at mid prices is usually not robust. Options backtests should be run under multiple execution assumptions, including conservative fills.

## 10.4 Point-in-Time Data Controls

Point-in-time control means every decision in the backtest uses only information that would have been available at the decision timestamp.

Let $\mathcal{F}_t$ be the information set available at time $t$. A signal is valid only if:

$$
\text{Signal}_t = f(\mathcal{F}_t),
$$

not:

$$
\text{Signal}_t = f(\mathcal{F}_{t+1},\mathcal{F}_{t+2},\ldots).
$$

This sounds obvious, but options research has many subtle look-ahead traps.

## 10.4.1 Examples of Look-Ahead Bias

| Bias | Example | Correct Treatment |
|---|---|---|
| Future earnings date | Using final earnings calendar known after revisions | Use earnings date known at trade time |
| Revised macro data | Using final CPI, GDP, or PMI values | Use data vintage and release timestamp |
| Survivor universe | Testing only stocks that exist today | Include delisted and historical constituents |
| Future option availability | Selecting strikes that are known later but unavailable at signal time | Use actual chain available at trade time |
| Future liquidity | Filtering by future volume or OI | Filter only on current or lagged liquidity |
| Future corporate actions | Adjusting contracts with later knowledge | Use point-in-time corporate-action records |
| Future surface | Using end-of-day surface to trade earlier intraday | Align signal, quote, and execution timestamps |
| Future borrow | Using borrow rates revised after the fact | Use borrow known at trade time |

A backtest with look-ahead bias may appear highly predictive because it accidentally uses future information.

## 10.4.2 Availability Timestamp

Every dataset should distinguish observation date from availability date.

For macro variable $x$:

$$
x_{obs} = \text{economic value for period } obs,
$$

while:

$$
x_{avail} = \text{date and time when the value became available to the market}.
$$

A valid historical feature at trade time $t$ is:

$$
x_t^{valid}=x_{obs}\quad \text{only if}\quad x_{avail}\le t.
$$

This same concept applies to earnings dates, dividends, borrow costs, index weights, ratings, analyst forecasts, and corporate actions.

## 10.5 Universe Construction

Universe selection should be defined before signal testing. Poor universe design can create hidden biases.

## 10.5.1 Underlying Universe

An equity options universe may start with:

- index constituents at each historical date;
- ETF option underlyings;
- liquid single-name option underlyings;
- minimum market capitalization;
- minimum underlying dollar volume;
- minimum price threshold;
- exclusion of merger targets or special situations if required by mandate.

A survivorship-safe universe uses historical membership:

$$
\mathcal{U}_t = \{j: j \text{ is eligible at time } t \text{ using information known at } t\}.
$$

It should not be:

$$
\mathcal{U}_t = \{j: j \text{ is in today\'s index membership}\}.
$$

## 10.5.2 Option Contract Universe

Eligible option contracts can be filtered by:

- option type: call, put, or both;
- exercise style;
- maturity range;
- delta range;
- moneyness range;
- minimum bid price;
- maximum bid-ask spread;
- minimum volume;
- minimum open interest;
- maximum quote age;
- no corporate-action adjustment issues;
- no imminent expiration unless strategy explicitly trades short-dated options.

A typical liquid equity option filter may require:

$$
\text{Bid}_i > 0,
$$

$$
\text{Ask}_i > \text{Bid}_i,
$$

$$
\frac{\text{Ask}_i-\text{Bid}_i}{(\text{Ask}_i+\text{Bid}_i)/2} \le s_{max},
$$

$$
OI_i \ge OI_{min},
$$

$$
\tau_{min}\le \tau_i \le \tau_{max}.
$$

The filter should be applied using data available before trade entry.

## 10.6 Option-Chain Cleaning

Raw option-chain data can contain stale quotes, crossed markets, zero bids, bad strikes, duplicate records, incorrect multipliers, and corporate-action issues. Cleaning is a model step and must be documented.

## 10.6.1 Basic Quote Filters

Common filters include:

| Filter | Rule | Reason |
|---|---:|---|
| Positive strike | $K>0$ | Prevent invalid contracts |
| Positive maturity | $\tau>0$ | Avoid expired contracts |
| Valid bid-ask | $0\le Bid\le Ask$ | Remove crossed quotes |
| Positive ask | $Ask>0$ | Required for buy execution |
| Minimum mid | $Mid\ge P_{min}$ | Avoid unstable penny options |
| Maximum spread | $(Ask-Bid)/Mid\le s_{max}$ | Control execution cost |
| Valid multiplier | $M>0$ | Correct scaling |
| Quote freshness | age below threshold | Avoid stale marks |
| OI and volume | above threshold if required | Avoid untradeable contracts |

## 10.6.2 No-Arbitrage Checks

European option prices should satisfy basic static bounds. For calls with continuous dividend yield:

$$
C \ge \max(S e^{-q\tau}-K e^{-r\tau},0),
$$

$$
C \le S e^{-q\tau}.
$$

For puts:

$$
P \ge \max(K e^{-r\tau}-S e^{-q\tau},0),
$$

$$
P \le K e^{-r\tau}.
$$

Put-call parity for European options is:

$$
C-P=S e^{-q\tau}-K e^{-r\tau}.
$$

For American options, discrete dividends, borrow, and early exercise complicate these checks. Still, severe violations can indicate data problems.

## 10.6.3 Implied-Volatility Inversion Failures

Implied-volatility inversion can fail because:

- price violates arbitrage bounds;
- option price is too close to intrinsic value;
- quote is stale;
- bid-ask spread is too wide;
- dividend or rate input is wrong;
- option is American but European formula is used;
- corporate action changed the contract specification.

The pipeline should not silently fill failed implied volatilities with arbitrary values. It should flag failures, exclude affected contracts when appropriate, and report failure rates.

## 10.7 Signal Construction

Signal construction should be reproducible and point-in-time. A signal should have a documented economic hypothesis, data source, formula, timestamp, and fallback rule.

## 10.7.1 Volatility Risk Premium Signal

A volatility risk premium signal can be:

$$
\text{VRP}_{i,t}=\sigma_{imp,i,t}^{2}-\widehat{\sigma}_{real,j,t\rightarrow t+h}^{2}.
$$

Here option $i$ is on underlying $j$. The realized volatility forecast must be available at time $t$.

A backward-looking proxy is:

$$
\text{IVRV}_{i,t}=\sigma_{imp,i,t}-\sigma_{real,j,t}^{(L)}.
$$

This is easier to compute but less forward-looking.

## 10.7.2 Skew Signal

A downside skew signal may be:

$$
\text{PutSkew}_{j,t}=\sigma_{25\Delta put,j,t}-\sigma_{ATM,j,t}.
$$

A z-scored richness measure is:

$$
Z_{j,t}^{skew}=\frac{\text{PutSkew}_{j,t}-\mu_{j,t}^{(L)}}{s_{j,t}^{(L)}}.
$$

The rolling mean and standard deviation must be computed using only historical values up to time $t$.

## 10.7.3 Term-Structure Signal

A term-slope signal can be:

$$
\text{TermSlope}_{j,t}=\sigma_{ATM,j,t}(\tau_2)-\sigma_{ATM,j,t}(\tau_1),\quad \tau_2>\tau_1.
$$

A forward-volatility signal is:

$$
\sigma_{fwd,t}(\tau_1,\tau_2)=\sqrt{\frac{\sigma_{2,t}^2\tau_2-\sigma_{1,t}^2\tau_1}{\tau_2-\tau_1}}.
$$

If total variance decreases with maturity, the surface may contain calendar arbitrage or bad data.

## 10.7.4 Liquidity-Adjusted Signal

A gross signal should be penalized for execution costs and liquidity:

$$
\text{NetScore}_{i,t}=\text{GrossScore}_{i,t}-\lambda_s\text{SpreadCost}_{i,t}-\lambda_l\text{LiquidityPenalty}_{i,t}-\lambda_m\text{MarginPenalty}_{i,t}.
$$

For short-option strategies, the signal should also penalize jump and event risk:

$$
\text{ShortVolScore}_{i,t}=a_1Z(\text{VRP}_{i,t})+a_2Z(\text{Liquidity}_{i,t})-a_3Z(\text{JumpRisk}_{j,t})-a_4Z(\text{EventRisk}_{j,t}).
$$

## 10.8 Trade Construction and Lifecycle

A backtest must define how selected signals become actual trades.

## 10.8.1 Opening Trades

For each candidate trade, define:

- entry date and time;
- option leg selection rule;
- target delta or strike;
- target maturity;
- contract quantity;
- execution price;
- initial hedge;
- margin requirement;
- reason code for trade entry.

Example: a 30-day 25-delta short put strategy might define the selected contract as:

$$
i^*_{j,t}=\arg\min_i |\Delta_{i,t}+0.25|,
$$

subject to:

$$
25/365\le \tau_i\le45/365,
$$

and liquidity filters.

## 10.8.2 Holding and Rebalancing

The strategy must define whether it holds to expiration, closes after a fixed number of days, rolls at a maturity threshold, delta-hedges, or adjusts strikes.

Examples:

| Lifecycle Rule | Description |
|---|---|
| Hold to expiry | Position remains until expiration unless risk limit is breached |
| Fixed holding period | Close after $H$ trading days |
| Maturity roll | Roll when time to maturity falls below threshold |
| Profit take | Close when a percentage of premium is earned |
| Stop loss | Close when loss exceeds threshold |
| Delta band | Hedge when delta exposure breaches band |
| Regime exit | Reduce or close when regime probability changes |
| Event exit | Close before earnings or macro event |

Rules should be specified before testing and should not be optimized excessively.

## 10.8.3 Closing Trades

Closing execution must be realistic:

- a short option is bought back at ask or ask-adjusted price;
- a long option is sold at bid or bid-adjusted price;
- multi-leg trades require leg-level or package execution assumptions;
- liquidation during stress should widen costs.

Marking a strategy at mid prices but executing at bid/ask can overstate returns.

## 10.9 Execution Assumptions

Execution assumptions are often the difference between a plausible strategy and an illusion.

## 10.9.1 Bid-Ask Execution

For option mid price:

$$
Mid_i=\frac{Bid_i+Ask_i}{2}.
$$

A conservative buy price may be:

$$
P_i^{buy}=Mid_i+\alpha\frac{Ask_i-Bid_i}{2},
$$

and sell price:

$$
P_i^{sell}=Mid_i-\alpha\frac{Ask_i-Bid_i}{2},
$$

where $\alpha\in[0,1]$ determines how much spread is paid. If $\alpha=1$, the strategy crosses the full half-spread. If $\alpha=0$, it executes at mid, which may be too optimistic.

## 10.9.2 Market Impact

A stylized option impact model is:

$$
\text{ImpactCost}_i=\eta_i\left(\frac{|Q_i|}{ADV_i}\right)^{\beta_i}|Q_i|M_iP_i,
$$

where:

- $Q_i$ is contract quantity;
- $ADV_i$ is average daily option volume;
- $M_i$ is contract multiplier;
- $P_i$ is option premium;
- $\eta_i$ and $\beta_i$ are impact parameters.

Impact assumptions should become more conservative during high-volatility or low-liquidity regimes.

## 10.9.3 Underlying Hedge Execution

If a strategy delta hedges using the underlying, hedge execution requires:

- hedge price;
- hedge spread;
- commission;
- market impact;
- borrow cost if short;
- financing on cash balance;
- hedge timing.

A hedge cost for trade size $\Delta h_t$ can be:

$$
TC_t^{hedge}=c_t|\Delta h_t|S_t,
$$

where $c_t$ is proportional hedge cost.

## 10.10 P&L Accounting

P&L accounting should separate realized and unrealized components.

For option position $i$:

$$
\Delta P\&L_{i,t}=Q_iM_i(P_{i,t}-P_{i,t-1})+\text{CashFlows}_{i,t}-\text{Costs}_{i,t}.
$$

For a delta hedge:

$$
\Delta P\&L_{hedge,t}=h_{t-1}(S_t-S_{t-1})-TC_{hedge,t}+\text{Financing}_{t}-\text{BorrowCost}_{t}.
$$

Total strategy P&L is:

$$
\Delta P\&L_{strategy,t}=\sum_i\Delta P\&L_{i,t}+\Delta P\&L_{hedge,t}+\Delta P\&L_{cash,t}.
$$

The backtest should track:

- option mark-to-market P&L;
- realized closing P&L;
- hedge P&L;
- premium received or paid;
- commissions;
- spread cost;
- slippage;
- borrow cost;
- financing income or cost;
- margin usage;
- assignment or exercise cash flows.

## 10.11 Greek-Based P&L Attribution

Daily P&L should be decomposed using beginning-of-period Greeks:

$$
\Delta V_t \approx
\Delta_t\Delta S_t
+\frac{1}{2}\Gamma_t(\Delta S_t)^2
+\Theta_t\Delta t
+\nu_t\Delta\sigma_t
+\rho_t\Delta r_t
+\text{Vanna}_t\Delta S_t\Delta\sigma_t
+\frac{1}{2}\text{Volga}_t(\Delta\sigma_t)^2
+\text{Residual}_t.
$$

Residual P&L is:

$$
\text{Residual}_t=\Delta V_t-\widehat{\Delta V}_t^{Greek}.
$$

Large residuals can indicate:

- surface movement not captured by the model;
- stale marks;
- execution slippage;
- assignment or exercise;
- dividend or borrow changes;
- corporate-action adjustment;
- incorrect contract multiplier;
- model misspecification;
- data timestamp mismatch.

A production backtest should report residual P&L as a diagnostic, not hide it.

## 10.12 Performance Metrics

Options strategies require a broader set of metrics than annualized return and Sharpe ratio.

## 10.12.1 Return and Risk Metrics

| Metric | Formula or Description | Use |
|---|---|---|
| Annualized return | compounded or arithmetic annualization | Overall return |
| Annualized volatility | standard deviation of returns times annualization factor | Risk scale |
| Sharpe ratio | excess return divided by volatility | Risk-adjusted return |
| Sortino ratio | excess return divided by downside deviation | Downside risk |
| Maximum drawdown | worst peak-to-trough decline | Path risk |
| Calmar ratio | annualized return divided by absolute max drawdown | Drawdown efficiency |
| Skewness | third standardized moment | Asymmetry |
| Excess kurtosis | fourth standardized moment minus 3 | Tail thickness |
| Value at Risk | loss quantile | Tail threshold |
| Expected shortfall | average loss beyond VaR | Tail severity |
| Hit rate | fraction of profitable periods | Stability diagnostic |
| Profit factor | gross gains divided by gross losses | Trade-level quality |

## 10.12.2 Options-Specific Metrics

| Metric | Description |
|---|---|
| Average delta exposure | Directional bias |
| Average gamma dollars | Convexity profile |
| Average vega per vol point | Volatility exposure |
| Average daily theta | Carry or decay profile |
| Vega by tenor | Term-structure exposure |
| Skew exposure | Downside or upside vol exposure |
| Hedge turnover | Underlying trading burden |
| Option turnover | Roll and signal trading burden |
| Average spread paid | Execution realism |
| Margin utilization | Capital intensity |
| Stress loss | Scenario robustness |
| P&L attribution share | Which Greeks drive returns |
| Residual P&L share | Model misspecification diagnostic |

A strategy with a high Sharpe ratio but large negative skew, high expected shortfall, high margin utilization, and poor liquidity may be unacceptable.

## 10.13 Biases and Backtest Failure Modes

## 10.13.1 Survivorship Bias

Survivorship bias occurs when only securities that survive to the present are included. This is especially dangerous in single-stock option research because delisted or distressed names may have had high option premia before severe losses.

Correct treatment:

$$
\mathcal{U}_t = \text{historical eligible universe at time } t.
$$

Not:

$$
\mathcal{U}_t = \text{current liquid option universe}.
$$

## 10.13.2 Look-Ahead Bias

Look-ahead bias occurs when future data influence past decisions. In options research, examples include future earnings dates, future open interest, future volatility surfaces, revised macro data, and future index membership.

## 10.13.3 Stale Quote Bias

Illiquid option quotes may not update when the underlying moves. A backtest using stale mid prices may show artificial profits. Stale quotes can understate realized volatility, distort implied volatility, and create false arbitrage.

## 10.13.4 Mid-Price Bias

Using mid prices for all entries and exits is often optimistic. If a strategy trades frequently or uses illiquid options, mid-price bias can dominate returns.

A robust process should test:

- mid execution;
- half-spread execution;
- full bid/ask execution;
- stress widened spread execution.

## 10.13.5 Overfitting

Options data provide many dimensions: strike, maturity, delta, skew, term, volatility, event windows, and regimes. This creates enormous overfitting risk. Excessive parameter tuning can produce attractive historical results that fail out of sample.

Controls include:

- pre-specified hypotheses;
- train/validation/test splits;
- walk-forward testing;
- parameter stability analysis;
- transaction-cost sensitivity;
- regime robustness;
- false-discovery controls;
- simple benchmark strategies.

## 10.13.6 Rebalancing and Roll Bias

Option strategy returns can be highly sensitive to roll rules. A strategy that rolls from 30 days to 45 days may behave very differently from one that rolls from 21 days to 35 days. Roll rules should be economically motivated, not optimized until the best historical result is found.

## 10.14 Walk-Forward Validation

A walk-forward backtest repeatedly trains on historical data and tests on future periods.

A simple walk-forward structure is:

$$
\text{Train on }[t_0,t_1]\rightarrow \text{Test on }(t_1,t_2],
$$

then:

$$
\text{Train on }[t_0,t_2]\rightarrow \text{Test on }(t_2,t_3],
$$

or using a rolling window:

$$
\text{Train on }[t_{k-L},t_k]\rightarrow \text{Test on }(t_k,t_{k+1}].
$$

Walk-forward validation should re-estimate:

- signal parameters;
- volatility forecasts;
- covariance models;
- regime models;
- transaction-cost models if they are adaptive;
- portfolio constraints if they are data-driven.

The backtest should not fit parameters once using the full sample and then claim the entire period is out of sample.

## 10.15 Benchmarking

Every options strategy needs benchmarks.

Potential benchmarks include:

| Strategy Type | Benchmark |
|---|---|
| Short volatility | naive short straddle or variance risk premium index |
| Long gamma | always-long straddle with same maturity and delta hedge |
| Covered call | standard covered-call index or fixed-delta overwriting rule |
| Protective put | fixed-delta put overlay |
| Collar | fixed-strike or fixed-delta collar benchmark |
| Dispersion | static index-versus-single-name volatility basket |
| Regime strategy | non-regime version of the same strategy |
| Cross-sectional ranking | equal-weight eligible trade basket |

The benchmark should share similar implementation constraints so that performance differences reflect the signal or portfolio method, not different cost assumptions.

## 10.16 Python Code: Data Schemas

The following code defines lightweight schemas for option quotes, positions, and trades. In production, these would be enforced through data contracts, database constraints, or validation libraries.

```python
from dataclasses import dataclass
from typing import Literal
import math
import numpy as np
import pandas as pd

OptionType = Literal["call", "put"]
Side = Literal["buy", "sell"]


@dataclass(frozen=True)
class OptionQuote:
    timestamp: pd.Timestamp
    underlying: str
    option_id: str
    expiration: pd.Timestamp
    strike: float
    option_type: OptionType
    bid: float
    ask: float
    volume: float
    open_interest: float
    underlying_price: float
    multiplier: float = 100.0
    exercise_style: str = "American"


@dataclass(frozen=True)
class Trade:
    timestamp: pd.Timestamp
    option_id: str
    side: Side
    quantity: float
    price: float
    transaction_cost: float
    reason: str
```

## 10.17 Python Code: Option-Chain Cleaning

```python
def clean_option_chain(
    chain: pd.DataFrame,
    min_mid: float = 0.05,
    max_bid_ask_pct: float = 0.50,
    min_open_interest: float = 10,
    min_days_to_expiry: int = 7,
    max_days_to_expiry: int = 365,
) -> pd.DataFrame:
    """Clean an option chain using basic institutional filters.

    Expected columns
    ----------------
    timestamp, underlying, option_id, expiration, strike, option_type,
    bid, ask, volume, open_interest, underlying_price, multiplier.
    """
    required = [
        "timestamp", "underlying", "option_id", "expiration", "strike", "option_type",
        "bid", "ask", "volume", "open_interest", "underlying_price", "multiplier",
    ]
    missing = [c for c in required if c not in chain.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = chain.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["expiration"] = pd.to_datetime(df["expiration"])
    df["days_to_expiry"] = (df["expiration"] - df["timestamp"]).dt.days
    df["mid"] = (df["bid"] + df["ask"]) / 2.0
    df["bid_ask_pct"] = (df["ask"] - df["bid"]) / df["mid"].replace(0.0, np.nan)

    mask = (
        (df["strike"] > 0)
        & (df["underlying_price"] > 0)
        & (df["multiplier"] > 0)
        & (df["bid"] >= 0)
        & (df["ask"] >= df["bid"])
        & (df["ask"] > 0)
        & (df["mid"] >= min_mid)
        & (df["bid_ask_pct"] <= max_bid_ask_pct)
        & (df["open_interest"] >= min_open_interest)
        & (df["days_to_expiry"] >= min_days_to_expiry)
        & (df["days_to_expiry"] <= max_days_to_expiry)
        & (df["option_type"].isin(["call", "put"]))
    )
    return df.loc[mask].reset_index(drop=True)
```

## 10.18 Python Code: Black-Scholes Utilities and Implied Volatility

```python
from scipy.stats import norm
from scipy.optimize import brentq


def bsm_price(
    spot: float,
    strike: float,
    tau: float,
    rate: float,
    dividend_yield: float,
    volatility: float,
    option_type: OptionType,
) -> float:
    if spot <= 0 or strike <= 0 or tau <= 0 or volatility <= 0:
        raise ValueError("spot, strike, tau, and volatility must be positive")
    vol_sqrt = volatility * math.sqrt(tau)
    d1 = (math.log(spot / strike) + (rate - dividend_yield + 0.5 * volatility**2) * tau) / vol_sqrt
    d2 = d1 - vol_sqrt
    df_r = math.exp(-rate * tau)
    df_q = math.exp(-dividend_yield * tau)
    if option_type == "call":
        return spot * df_q * norm.cdf(d1) - strike * df_r * norm.cdf(d2)
    return strike * df_r * norm.cdf(-d2) - spot * df_q * norm.cdf(-d1)


def implied_volatility(
    market_price: float,
    spot: float,
    strike: float,
    tau: float,
    rate: float,
    dividend_yield: float,
    option_type: OptionType,
    lower: float = 0.0001,
    upper: float = 5.0,
) -> float | np.nan:
    """Invert Black-Scholes implied volatility using Brent's method."""
    if market_price <= 0 or spot <= 0 or strike <= 0 or tau <= 0:
        return np.nan

    def objective(vol: float) -> float:
        return bsm_price(spot, strike, tau, rate, dividend_yield, vol, option_type) - market_price

    try:
        f_low = objective(lower)
        f_high = objective(upper)
        if f_low * f_high > 0:
            return np.nan
        return float(brentq(objective, lower, upper, maxiter=100))
    except Exception:
        return np.nan


def add_implied_vols(chain: pd.DataFrame, rate: float, dividend_yield: float) -> pd.DataFrame:
    """Add mid implied volatility to a cleaned option chain."""
    df = chain.copy()
    tau = df["days_to_expiry"] / 365.0
    ivs = []
    for row, tau_i in zip(df.itertuples(index=False), tau):
        ivs.append(
            implied_volatility(
                market_price=float(row.mid),
                spot=float(row.underlying_price),
                strike=float(row.strike),
                tau=float(tau_i),
                rate=rate,
                dividend_yield=dividend_yield,
                option_type=row.option_type,
            )
        )
    df["implied_vol"] = ivs
    return df.dropna(subset=["implied_vol"]).reset_index(drop=True)
```

## 10.19 Python Code: Strategy Candidate Selection

The following example selects a target-delta put for each underlying. This is a simplified example and should be extended for surface-aware Greeks, American exercise, discrete dividends, borrow, and event filters.

```python
def approximate_delta(
    spot: float,
    strike: float,
    tau: float,
    rate: float,
    dividend_yield: float,
    volatility: float,
    option_type: OptionType,
) -> float:
    vol_sqrt = volatility * math.sqrt(tau)
    d1 = (math.log(spot / strike) + (rate - dividend_yield + 0.5 * volatility**2) * tau) / vol_sqrt
    df_q = math.exp(-dividend_yield * tau)
    if option_type == "call":
        return df_q * norm.cdf(d1)
    return df_q * (norm.cdf(d1) - 1.0)


def select_target_delta_options(
    chain: pd.DataFrame,
    target_delta: float = -0.25,
    target_days: int = 30,
    rate: float = 0.04,
    dividend_yield: float = 0.0,
) -> pd.DataFrame:
    """Select one option per underlying nearest target delta and maturity."""
    df = chain.copy()
    df["tau"] = df["days_to_expiry"] / 365.0
    df["model_delta"] = [
        approximate_delta(
            spot=row.underlying_price,
            strike=row.strike,
            tau=row.tau,
            rate=rate,
            dividend_yield=dividend_yield,
            volatility=row.implied_vol,
            option_type=row.option_type,
        )
        for row in df.itertuples(index=False)
    ]
    df["selection_distance"] = (df["model_delta"] - target_delta).abs() + 0.01 * (df["days_to_expiry"] - target_days).abs()
    idx = df.groupby("underlying")["selection_distance"].idxmin()
    return df.loc[idx].reset_index(drop=True)
```

## 10.20 Python Code: Minimal Backtest Loop Skeleton

This skeleton illustrates the sequencing of a point-in-time options backtest. It is not a complete production engine, but it shows the required structure.

```python
class OptionsBacktester:
    """Minimal event-driven options backtest skeleton.

    This skeleton emphasizes sequencing and accounting discipline. Production
    use requires database access, robust margin, corporate actions, assignment,
    American exercise, and execution-management logic.
    """

    def __init__(self, initial_cash: float = 1_000_000.0):
        self.cash = initial_cash
        self.positions: dict[str, float] = {}
        self.trade_log: list[dict] = []
        self.daily_log: list[dict] = []

    def execute_trade(self, timestamp, option_id: str, side: Side, quantity: float, price: float, multiplier: float, cost: float, reason: str):
        signed_qty = quantity if side == "buy" else -quantity
        cash_flow = -signed_qty * price * multiplier - cost
        self.cash += cash_flow
        self.positions[option_id] = self.positions.get(option_id, 0.0) + signed_qty
        self.trade_log.append(
            {
                "timestamp": timestamp,
                "option_id": option_id,
                "side": side,
                "quantity": quantity,
                "price": price,
                "multiplier": multiplier,
                "transaction_cost": cost,
                "cash_flow": cash_flow,
                "reason": reason,
            }
        )

    def mark_to_market(self, timestamp, chain: pd.DataFrame) -> float:
        marks = chain.set_index("option_id")
        value = self.cash
        for option_id, qty in self.positions.items():
            if abs(qty) < 1e-12:
                continue
            if option_id not in marks.index:
                continue
            row = marks.loc[option_id]
            value += qty * row["mid"] * row["multiplier"]
        self.daily_log.append({"timestamp": timestamp, "portfolio_value": value, "cash": self.cash})
        return value

    def run_one_day(self, timestamp, raw_chain: pd.DataFrame, signal_function, sizing_function, rate: float, dividend_yield: float):
        clean = clean_option_chain(raw_chain)
        clean = add_implied_vols(clean, rate=rate, dividend_yield=dividend_yield)
        candidates = signal_function(clean)

        for row in candidates.itertuples(index=False):
            quantity = sizing_function(row)
            if quantity == 0:
                continue
            # Conservative short-option entry: sell at bid.
            side: Side = "sell"
            price = float(row.bid)
            cost = 0.65 + 0.001 * abs(quantity) * row.multiplier * price
            self.execute_trade(
                timestamp=timestamp,
                option_id=row.option_id,
                side=side,
                quantity=abs(quantity),
                price=price,
                multiplier=row.multiplier,
                cost=cost,
                reason="signal_entry",
            )

        return self.mark_to_market(timestamp, clean)
```

## 10.21 Python Code: Performance Metrics

```python
def performance_metrics(equity_curve: pd.Series, periods_per_year: int = 252) -> pd.Series:
    """Compute common performance metrics from an equity curve."""
    curve = equity_curve.dropna().astype(float)
    if len(curve) < 3:
        raise ValueError("equity_curve must have at least 3 observations")
    returns = curve.pct_change().dropna()
    total_return = curve.iloc[-1] / curve.iloc[0] - 1.0
    years = len(returns) / periods_per_year
    ann_return = (1.0 + total_return) ** (1.0 / years) - 1.0 if years > 0 else np.nan
    ann_vol = returns.std(ddof=1) * math.sqrt(periods_per_year)
    sharpe = ann_return / ann_vol if ann_vol > 0 else np.nan

    downside = returns[returns < 0]
    downside_dev = downside.std(ddof=1) * math.sqrt(periods_per_year) if len(downside) > 1 else np.nan
    sortino = ann_return / downside_dev if downside_dev and downside_dev > 0 else np.nan

    running_max = curve.cummax()
    drawdown = curve / running_max - 1.0
    max_dd = drawdown.min()
    calmar = ann_return / abs(max_dd) if max_dd < 0 else np.nan

    var_95 = returns.quantile(0.05)
    es_95 = returns[returns <= var_95].mean()

    return pd.Series(
        {
            "total_return": total_return,
            "annualized_return": ann_return,
            "annualized_volatility": ann_vol,
            "sharpe_ratio": sharpe,
            "sortino_ratio": sortino,
            "max_drawdown": max_dd,
            "calmar_ratio": calmar,
            "skewness": returns.skew(),
            "excess_kurtosis": returns.kurtosis(),
            "daily_var_95": var_95,
            "daily_expected_shortfall_95": es_95,
            "hit_rate": (returns > 0).mean(),
        }
    )
```

## 10.22 Validation and Robustness Tests

An institutional backtest should test robustness across:

| Test | Purpose |
|---|---|
| Alternative execution assumptions | Determine sensitivity to spread and slippage |
| Alternative maturity buckets | Ensure result is not one roll-date artifact |
| Alternative delta targets | Test strike-selection robustness |
| Excluding earnings windows | Identify event-risk dependence |
| Crisis subperiods | Evaluate stress behavior |
| Low-volatility subperiods | Evaluate carry behavior |
| High-rate and low-rate environments | Test rate sensitivity |
| Sector exclusions | Identify concentration |
| Liquidity filters | Test capacity and tradability |
| Walk-forward windows | Test parameter stability |
| Randomized entry dates | Detect calendar artifacts |
| Signal decay tests | Measure predictive horizon |
| Bootstrap or block bootstrap | Evaluate sampling uncertainty |

A strategy whose performance disappears under modestly more conservative execution assumptions is not robust.

## 10.23 Research Documentation Requirements

Every completed strategy research package should document:

1. Strategy hypothesis.
2. Universe definition.
3. Data sources and data versions.
4. Point-in-time controls.
5. Cleaning and filtering rules.
6. Signal formulas.
7. Trade construction rules.
8. Execution assumptions.
9. Hedging assumptions.
10. Margin and financing assumptions.
11. Risk limits.
12. Backtest period and rebalance frequency.
13. Performance results.
14. P&L attribution.
15. Stress-test results.
16. Robustness tests.
17. Known weaknesses.
18. Production requirements.
19. Monitoring plan.
20. Approval and governance notes.

Research that cannot be reproduced from documentation should not be considered production-ready.

## 10.24 Production Architecture

A production-grade options research platform can be organized into layers.

| Layer | Function |
|---|---|
| Data ingestion | Load option chains, underlyings, rates, dividends, borrow, events |
| Data validation | Check schema, missing values, stale quotes, corporate actions |
| Surface engine | Build implied volatility surfaces and features |
| Greek engine | Compute core, higher-order, and surface-aware Greeks |
| Signal engine | Generate point-in-time alpha and risk signals |
| Portfolio engine | Apply construction rules and optimization |
| Execution simulator | Apply bid-ask, slippage, impact, and fill assumptions |
| Hedging engine | Simulate delta or vega hedging rules |
| Accounting engine | Track positions, cash, margin, financing, borrow, and P&L |
| Risk engine | Calculate Greeks, stress tests, limits, and expected shortfall |
| Attribution engine | Decompose P&L by Greek and risk factor |
| Reporting engine | Produce dashboards, logs, and audit outputs |
| Monitoring engine | Detect data breaks, model errors, and limit breaches |

The architecture should be modular. A change in the implied-volatility surface model should not silently change execution assumptions or portfolio accounting.

## 10.25 Monitoring After Backtest Deployment

Backtesting does not end when a strategy goes live. Live monitoring should compare actual behavior against backtest expectations.

Key monitoring items include:

- realized fills versus assumed fills;
- actual spreads versus backtest spreads;
- actual hedge turnover versus expected hedge turnover;
- P&L attribution versus backtest attribution;
- residual P&L size;
- Greeks versus intended Greek budgets;
- stress losses versus expected stress profile;
- margin utilization;
- liquidity and days-to-exit;
- signal distribution drift;
- data quality exceptions;
- model-version changes.

A live strategy should have decommission criteria. If live residual P&L is persistently large or execution costs exceed backtest assumptions, the strategy should be paused or redesigned.

## 10.26 Production Readiness Checklist

| Area | Requirement |
|---|---|
| Data | Point-in-time option chains, underlying data, rates, dividends, borrow, events |
| Cleaning | Documented quote filters, no-arbitrage checks, stale-quote controls |
| Surface | Reproducible implied-volatility surface and feature construction |
| Greeks | Core, higher-order, and surface-aware Greeks with documented units |
| Signals | Point-in-time formulas and versioned parameters |
| Backtest | Event-driven or path-aware simulation with realistic lifecycle rules |
| Execution | Bid-ask, slippage, impact, commissions, and liquidity assumptions |
| Hedging | Defined hedge instrument, frequency, thresholds, and costs |
| Accounting | Cash, premium, financing, borrow, margin, exercise, and assignment |
| Risk | Greek limits, stress tests, drawdown, margin, liquidity, and kill-switch rules |
| Attribution | Delta, gamma, theta, vega, skew, cost, financing, and residual P&L |
| Validation | Walk-forward, robustness, stress periods, and benchmark comparison |
| Governance | Documentation, audit logs, model versions, approvals, and monitoring |

## 10.27 Common Backtesting Errors

| Error | Why It Is Dangerous | Better Practice |
|---|---|---|
| Trading at mid prices | Overstates returns, especially for illiquid options | Test bid/ask and conservative slippage |
| Ignoring stale quotes | Creates false implied-volatility signals | Enforce freshness and spread filters |
| Using current universe | Creates survivorship bias | Use historical eligible universe |
| Ignoring delistings | Understates losses in distressed names | Include delisting and corporate-action history |
| Using revised macro data | Look-ahead bias | Use vintage data and release timestamps |
| Ignoring earnings timestamps | Misclassifies event risk | Use point-in-time earnings calendars |
| Treating American options as European without checks | Misprices dividend and exercise-sensitive contracts | Use appropriate model or filters |
| Ignoring borrow | Overstates hedge feasibility | Include borrow and locate constraints |
| Ignoring assignment | Misses operational and delta risk | Simulate assignment rules or flag exposures |
| Over-optimizing parameters | Produces fragile historical fit | Use walk-forward and robustness tests |
| No P&L attribution | Cannot diagnose why strategy worked | Attribute returns by Greek and cost bucket |
| No stress testing | Hidden crash risk remains | Add full repricing stress scenarios |
| Ignoring margin | Overstates capacity | Model normal and stress margin |
| Ignoring capacity | Strategy cannot scale | Apply OI, volume, and impact constraints |

## 10.28 Summary of Part 10

Part 10 developed an institutional research pipeline and backtesting framework for options strategies.

Key points:

1. Options backtesting must be point-in-time, executable, cost-aware, path-aware, and risk-attributed.
2. A strategy must define universe, signal, trade construction, sizing, execution, hedging, rebalancing, risk limits, accounting, attribution, and validation.
3. Required data include option chains, underlying prices, rates, dividends, borrow, funding, events, volatility surfaces, and execution/liquidity data.
4. Point-in-time controls must distinguish observation date from availability date.
5. Option-chain cleaning should handle invalid quotes, stale markets, wide spreads, low liquidity, arbitrage violations, and implied-volatility inversion failures.
6. Signals should be economically motivated, point-in-time, cost-adjusted, and robust to alternate definitions.
7. Trade lifecycle rules must define entry, holding, rolling, hedging, closing, stops, events, and regime exits.
8. Execution assumptions should include bid-ask, slippage, impact, commissions, hedge costs, and stress spread widening.
9. P&L accounting should separate option mark-to-market, hedge P&L, premium, financing, borrow, margin, transaction costs, and exercise or assignment effects.
10. Greek-based P&L attribution is essential for understanding whether returns come from delta, gamma, theta, vega, skew, costs, financing, or residual effects.
11. Performance metrics should include drawdown, expected shortfall, skewness, kurtosis, margin utilization, turnover, spread paid, stress loss, and residual P&L, not only Sharpe ratio.
12. Survivorship bias, look-ahead bias, stale quote bias, mid-price bias, and overfitting are especially dangerous in options research.
13. Walk-forward validation is required for models, signals, covariance estimates, and regime classifiers.
14. Benchmarks should match the strategy's implementation constraints.
15. Production readiness requires modular architecture, versioned models, audit logs, monitoring, kill switches, and live-versus-backtest comparison.

The next installment will cover Part 11: Case Studies and Institutional Strategy Templates, including long-gamma overlays, short-volatility carry, collars, covered calls, earnings-event volatility, dispersion, calendar spreads, skew trades, and regime-conditioned multi-sleeve allocation examples.
