# Institutional Macro-Regime Detection, Multi-Asset Signal Identification, and Statistical Validation Curriculum

## Installment 1: Global Assumptions, Part 0, and Part 1

**Scope of this installment.** This document begins the curriculum requested in the prompt. It covers the global assumptions, Part 0, and Part 1 only. Later installments should continue with Part 2 onward and eventually merge all parts into a consolidated manual.

**Educational boundary.** The framework is for research education, model design, and institutional portfolio-process development. It is not personalized investment advice, a live trading recommendation, or a guarantee of alpha.

---

# Global Assumptions

## G.1 Observation Frequency, Timestamping, and Forecast Horizons

1. **Base observation frequency.** The base observation frequency is monthly. Each observation is indexed by a decision timestamp $t$, normally represented as a month-end date such as 2026-05-31.
2. **Forward horizons.** The primary forward horizons are $h \in \{1,3,12\}$ months, referred to as $t+1$, $t+3$, and $t+12$.
3. **Decision timestamp.** A signal observed at timestamp $t$ must be fully available to the researcher or portfolio process before the portfolio decision associated with $t$ is made.
4. **Forward returns.** Forward returns are computed using strictly future asset returns relative to signal timestamp $t$. A feature measured at $t$ cannot use any return, macro release, data revision, ranking, scaling statistic, universe membership decision, or benchmark constituent information from $t+1$ or later.
5. **Multi-month return convention.** Unless otherwise stated, multi-month forward returns are arithmetic cumulative returns:

$$
R_{i,t\rightarrow t+h}^{\mathrm{cum}}
= \prod_{j=1}^{h}(1+r_{i,t+j}) - 1,
$$

where $R_{i,t\rightarrow t+h}^{\mathrm{cum}}$ is the cumulative forward return of asset $i$ from immediately after timestamp $t$ through the end of month $t+h$, $h$ is the horizon in months, and $r_{i,t+j}$ is the single-month arithmetic total return in month $t+j$. The interpretation is the realized return an investor would receive if a signal at $t$ were translated into an exposure held for the next $h$ months, excluding costs unless stated otherwise.

6. **Log-return convention.** When additivity is required, such as in some regressions or decompositions, the log cumulative return is:

$$
G_{i,t\rightarrow t+h}
= \sum_{j=1}^{h} g_{i,t+j},
\qquad
 g_{i,t}=\log(1+r_{i,t}),
$$

where $G_{i,t\rightarrow t+h}$ is the cumulative log return and $g_{i,t}$ is the monthly log return. The arithmetic cumulative return implied by $G$ is $\exp(G)-1$.

7. **Annualization convention.** Monthly average return $\bar r_m$ may be annualized approximately as $12\bar r_m$ or geometrically as $(1+\bar r_m)^{12}-1$. Monthly volatility $\sigma_m$ may be annualized as $\sigma_a=\sqrt{12}\sigma_m$ under the simplifying assumption of independent monthly returns. If returns are autocorrelated or overlapping, this annualization is only approximate.

## G.2 Data Availability and Point-in-Time Discipline

1. **Point-in-time features.** All features must be point-in-time and observable at the decision timestamp. The production timestamp should reflect actual availability, not the economic reference month.
2. **Macro release lags.** Macro data must account for publication lags, revisions, vintage availability, reporting calendars, holidays, and provider update times. For example, a CPI value labeled as May is often released in June and should not be used for a May-end decision unless the release date precedes the decision cutoff.
3. **Revised versus vintage macro data.** Revised macro series are generally invalid for historical forecasting unless the research explicitly models revised-data availability or uses vintage databases. A model tested on final revised data can overstate real-time efficacy.
4. **Market data availability.** Market prices, total return indices, futures settlement prices, option surfaces, and volatility indices must be aligned to the timestamp at which the signal would actually have been observable.
5. **Universe membership.** Asset universes should be constructed using point-in-time membership, inception dates, delisting information, liquidity filters, and investability constraints to reduce survivorship bias.

## G.3 Assets, Signals, and Convictions

1. **Asset classes.** The framework covers equities, equity sectors, equity countries, fixed income, sovereign duration, credit, FX, commodities, futures, derivatives, options, volatility indices, and alternative risk premia.
2. **Signal inputs.** Signals may be constructed from macro levels, differences, rates of change, year-over-year changes, rolling z-scores, expanding z-scores, percentile ranks, surprises, diffusion indices, market-implied variables, volatility measures, option surfaces, futures curves, cross-asset relative values, and alternative risk premia.
3. **Asset-level conviction definitions.** An asset-level conviction may represent one or more of the following:

| Conviction Object | Symbol | Interpretation |
|---|---:|---|
| Expected return | $\mathbb{E}_t[R_{i,t\rightarrow t+h}]$ | Conditional expected cumulative return over horizon $h$. |
| Probability of positive return | $\Pr_t(R_{i,t\rightarrow t+h}>0)$ | Estimated probability that the forward return is positive. |
| Probability of outperforming cash | $\Pr_t(R_{i,t\rightarrow t+h}-R_{c,t\rightarrow t+h}>0)$ | Estimated probability that asset $i$ beats cash. |
| Probability of outperforming benchmark | $\Pr_t(R_{i,t\rightarrow t+h}-R_{b,t\rightarrow t+h}>0)$ | Estimated probability that asset $i$ beats benchmark $b$. |
| Expected Sharpe | $\mathbb{E}_t[R^e]/\hat\sigma_t$ | Expected excess return divided by expected volatility. |
| Downside probability | $\Pr_t(R_{i,t\rightarrow t+h}<L)$ | Estimated probability of falling below loss threshold $L$. |
| Risk-adjusted expected return | $\mathbb{E}_t[R^e]-\lambda\hat\sigma_t^2$ | Expected excess return penalized by risk aversion $\lambda$. |

4. **Regime-aware allocation.** Regime-aware allocation is probabilistic, not binary. A regime model should produce uncertainty-aware probabilities rather than a single narrative label treated as truth.
5. **Friction assumptions.** Transaction costs, slippage, financing, margin, borrow costs, futures roll costs, option carry, bid-ask spreads, taxes, and liquidity constraints are excluded unless explicitly stated. Production research must later add them before economic conclusions are drawn.

## G.4 Regime Concepts

1. **Regimes are latent.** Macro regimes are not directly observable truth. They are latent, estimated, uncertain, model-dependent state descriptions.
2. **Classification versus prediction.** Contemporaneous regime classification answers, “What state does the model believe the world is in at time $t$?” Forward-looking regime prediction answers, “What state distribution does the model expect over $t+1$ to $t+h$?”
3. **Explanatory versus predictive relationships.** A variable may explain historical returns without forecasting future returns. Statistical association, Granger predictability, structural causality, and investment usefulness are different claims.
4. **Structural breaks.** Macro-asset relationships may change because of inflation regimes, central-bank reaction functions, globalization, fiscal dominance, credit constraints, regulation, market microstructure, crowding, or crises.

---

# Part 0: Executive Overview and Learning Roadmap

## 0.1 Purpose of Macro-Regime Detection in Multi-Asset Research

Macro-regime detection attempts to estimate the prevailing and prospective state of the economic and market environment so that asset-return expectations, risk expectations, and portfolio construction inputs can adapt to changing conditions. In multi-asset research, the central problem is not merely to label the economy as “expansion” or “recession.” The institutional problem is to translate noisy macro, market, and policy information into conditional expectations for assets that respond differently to growth, inflation, liquidity, policy, credit, currency, volatility, and risk appetite.

A regime framework is useful when it improves at least one of the following processes:

| Process | Core Question | Example Output |
|---|---|---|
| Regime identification | What state are we probably in now? | Probability of slowdown, reflation, inflation shock, liquidity stress. |
| Regime prediction | What state may dominate the next horizon? | Transition probability from expansion to slowdown. |
| Signal conditioning | Which signals work in this state? | Trend may dominate during persistent risk-off states; carry may fail during liquidity shocks. |
| Asset forecasting | What are conditional expected returns and risks? | $t+3$ expected return for duration, equities, credit, commodities, FX. |
| Portfolio construction | How should beliefs become constrained exposures? | Risk budget tilts, active weights, volatility-targeted exposures. |
| Risk management | What failure modes become more likely? | Liquidity shock, margin spiral, factor crash, option convexity demand. |

The objective is to produce **forward-looking asset-level convictions** over $t+1$, $t+3$, and $t+12$ horizons using monthly observations. A conviction is not simply a bullish or bearish view. It should be a calibrated and uncertainty-aware object such as an expected return, probability of positive return, probability of benchmark outperformance, expected Sharpe ratio, downside probability, or risk-adjusted return estimate.

## 0.2 Four Distinct Layers: Regimes, Signals, Forecasts, and Portfolios

A robust research process separates four layers that are often conflated.

### 0.2.1 Regime Identification

Regime identification estimates the latent state $S_t$ at time $t$ using information $\mathcal{F}_t$ available at that time:

$$
\pi_{k,t}=\Pr(S_t=k\mid\mathcal{F}_t), \qquad k=1,\ldots,K,
$$

where $S_t$ is the latent regime, $K$ is the number of regimes, and $\pi_{k,t}$ is the filtered probability that regime $k$ is active at timestamp $t$. The model can be rule-based, clustered, hidden Markov, Bayesian state-space, macroeconomic, market-based, or hybrid.

**Interpretation.** If $\pi_{\mathrm{slowdown},t}=0.65$, the model estimates a 65% probability that the current state resembles a slowdown regime under its own definitions. This is not proof that the economy is objectively in a slowdown.

### 0.2.2 Signal Generation

A signal is a feature or combination of features with a defined economic rationale, sign, horizon, universe, and validation history. Let $x_{m,t}$ be feature $m$ at time $t$. A signal may be:

$$
z_{i,t}^{(m)} = f_m(x_{m,t}, i, \mathcal{F}_t),
$$

where $z_{i,t}^{(m)}$ is the signal score for asset $i$, and $f_m(\cdot)$ is a transformation such as a z-score, rank, macro threshold rule, trend score, carry measure, volatility-risk-premium proxy, or cross-asset relative-value score.

A signal must have an explicit target. For example, a yield-curve steepening signal may be evaluated for $t+12$ duration returns, a credit-spread widening signal may be evaluated for $t+3$ equity drawdown risk, and a volatility term-structure signal may be evaluated for $t+1$ equity risk or volatility-strategy returns.

### 0.2.3 Forecasting

Forecasting maps features, signals, and regime probabilities into a forecast object:

$$
\hat y_{i,t,h}=\widehat{\mathbb{E}}_t[y_{i,t,h}],
$$

where $y_{i,t,h}$ may be cumulative return, excess return, downside indicator, benchmark-outperformance indicator, volatility, drawdown, or expected shortfall for asset $i$ over horizon $h$.

Forecasting requires strict alignment. The forecast made at $t$ can only use $\mathcal{F}_t$, while the target is realized over $t+1$ through $t+h$. This distinction is the core defense against look-ahead bias.

### 0.2.4 Portfolio Construction

Portfolio construction translates forecasts and convictions into exposures. A forecast alone is not a portfolio. Portfolio construction must account for covariance, drawdown risk, constraints, leverage, liquidity, turnover, transaction costs, margin, financing, currency exposure, duration exposure, beta exposure, and implementation instruments.

A simplified active-weight problem may be written as:

$$
\max_{w_t}\; w_t^{\top}\hat\mu_t
-\frac{\lambda}{2}w_t^{\top}\hat\Sigma_t w_t
-c(w_t,w_{t-1})
$$

subject to:

$$
\mathbf{1}^{\top}w_t=1, \qquad
w_{\min}\leq w_t\leq w_{\max}, \qquad
\mathrm{RiskBudget}(w_t)\leq B,
$$

where $w_t$ is the vector of portfolio weights, $\hat\mu_t$ is the vector of expected returns, $\hat\Sigma_t$ is the covariance matrix, $\lambda$ is risk aversion, $c(\cdot)$ is a transaction-cost or turnover penalty, and $B$ is a risk-budget limit.

## 0.3 Why Regimes Are Probabilistic Latent States

A macro regime is a summary of multiple interacting conditions rather than a directly measured object. Inflation can be falling while wage growth remains sticky; growth can slow while equity earnings remain resilient; credit spreads can widen while labor data remains strong; volatility can rise because of policy uncertainty rather than recession risk. This creates state ambiguity.

The formal approach is to treat a regime as a latent variable $S_t$ and to condition on a probability distribution:

$$
\boldsymbol{\pi}_t
=
\left[\Pr(S_t=1\mid\mathcal{F}_t),\ldots,\Pr(S_t=K\mid\mathcal{F}_t)\right]^{\top}.
$$

The probability vector $\boldsymbol{\pi}_t$ should sum to one:

$$
\sum_{k=1}^{K}\pi_{k,t}=1,
\qquad
0\leq \pi_{k,t}\leq 1.
$$

A portfolio process can then use probability-weighted expectations rather than a hard label:

$$
\hat\mu_{i,t,h}
=
\sum_{k=1}^{K}\pi_{k,t}\hat\mu_{i,k,h},
$$

where $\hat\mu_{i,k,h}$ is the estimated expected return of asset $i$ over horizon $h$ conditional on regime $k$. The interpretation is that the asset forecast is averaged across plausible regimes, weighted by the model’s current confidence in each state.

## 0.4 Why Monthly Macro Data Creates Special Challenges

Monthly data is attractive because many macro indicators are naturally monthly and because tactical asset allocation often operates on monthly or quarterly decision cycles. However, monthly data creates several important problems.

| Challenge | Why It Matters | Practical Control |
|---|---|---|
| Small sample size | 30 years of monthly data gives only 360 observations before lags and horizons. | Prefer parsimonious models, shrinkage, Bayesian priors, and robust validation. |
| Overlapping targets | $t+3$ and $t+12$ returns share future months across observations. | Use Newey-West, block bootstrap, or non-overlapping validation checks. |
| Publication lags | Macro observations are released after the reference period. | Use release calendars and vintage timestamps. |
| Revisions | Final data differ from real-time data. | Use vintage databases or conservative lagging. |
| Slow-moving signals | Macro variables can persist for years. | Control for autocorrelation and avoid overstating independent evidence. |
| Structural breaks | Relationships may change after crises or policy-regime shifts. | Use rolling stability tests, subperiod analysis, and model-risk overlays. |
| Data-mining risk | Many indicators and assets create many tests. | Use false discovery controls, White’s Reality Check, and out-of-sample testing. |
| Mixed frequencies | Daily market data and monthly macro data must be aligned. | Aggregate consistently to month-end decision timestamps. |

A monthly model should therefore be designed as a low-signal-to-noise forecasting system. The goal is not to find a single dominant variable that permanently predicts all assets. The goal is to build a disciplined framework that combines economic rationale, point-in-time data engineering, statistical validation, uncertainty estimation, and portfolio-aware implementation.

## 0.5 Macro Indicators and Cross-Asset Transmission

Macro variables affect assets through channels. The same macro release can be bullish or bearish depending on the level of valuations, policy reaction function, inflation context, risk appetite, and positioning.

| Macro Channel | Key Indicators | Equity Impact | Rates Impact | Credit Impact | FX Impact | Commodity Impact | Volatility Impact |
|---|---|---|---|---|---|---|---|
| Growth | PMI, ISM, industrial production, payrolls, GDP nowcasts | Higher growth can support earnings but raise discount rates. | Strong growth may lift yields. | Strong growth may compress spreads. | Growth differentials can support currency. | Cyclicals and energy may benefit. | Stable growth may reduce volatility. |
| Inflation | CPI, PCE, wages, breakevens, commodities | Moderate inflation can support nominal revenues; high inflation can compress multiples. | Higher inflation may lift nominal yields. | Inflation shocks can widen spreads. | Higher real-rate expectations can support currency. | Commodities can lead or respond to inflation. | Inflation uncertainty can raise volatility. |
| Policy | Policy rate, central-bank guidance, real rates | Tightening can pressure duration-sensitive equities. | Direct impact on yield curves. | Tightening can widen credit spreads. | Rate differentials affect FX. | Policy affects financing and demand. | Policy uncertainty can lift volatility. |
| Liquidity | Financial conditions, money growth, funding spreads | Abundant liquidity can support risk assets. | Liquidity affects term premia. | Funding stress can widen spreads. | Dollar funding stress can lift USD. | Liquidity affects inventories and leverage. | Liquidity shocks can spike volatility. |
| Credit | Credit spreads, defaults, lending standards | Credit stress can signal earnings risk. | Flight-to-quality can lower sovereign yields. | Direct impact on credit returns. | Risk-off may support safe havens. | Demand concerns can pressure commodities. | Credit stress often raises volatility. |
| Currency | DXY, real effective exchange rates, carry | Strong domestic currency can pressure foreign revenues. | FX can affect imported inflation. | FX stress can affect EM credit. | Direct channel. | Commodities often linked to USD. | Currency crises raise volatility. |

These channels are not mechanical. A growth acceleration with falling inflation can be risk-positive; a growth acceleration with sticky inflation and aggressive tightening can be risk-negative. A regime framework must therefore model interactions rather than relying on isolated indicator readings.

## 0.6 Defining t+1, t+3, and t+12 Asset-Level Convictions

Let $\mathcal{F}_t$ denote the information set available at decision timestamp $t$. For asset $i$ and horizon $h\in\{1,3,12\}$, an asset-level conviction should be explicitly defined.

### 0.6.1 Expected Return Conviction

$$
\mu_{i,t,h}=\mathbb{E}\left[R_{i,t\rightarrow t+h}^{\mathrm{cum}}\mid\mathcal{F}_t\right],
$$

where $\mu_{i,t,h}$ is the conditional expected cumulative arithmetic return. This can support asset allocation when paired with risk and uncertainty estimates.

### 0.6.2 Probability of Positive Return

$$
p^{+}_{i,t,h}=\Pr\left(R_{i,t\rightarrow t+h}^{\mathrm{cum}}>0\mid\mathcal{F}_t\right).
$$

This is useful when investors care about directional hit rate or when expected returns are unstable but sign probabilities are more robust.

### 0.6.3 Probability of Outperforming a Benchmark

$$
p^{b}_{i,t,h}=\Pr\left(R_{i,t\rightarrow t+h}^{\mathrm{cum}}-R_{b,t\rightarrow t+h}^{\mathrm{cum}}>0\mid\mathcal{F}_t\right),
$$

where $R_{b,t\rightarrow t+h}^{\mathrm{cum}}$ is the benchmark cumulative return. This is often more relevant for active allocation than absolute return.

### 0.6.4 Expected Sharpe Conviction

$$
\mathrm{ESharpe}_{i,t,h}=\frac{\hat\mu^e_{i,t,h}}{\hat\sigma_{i,t,h}},
$$

where $\hat\mu^e_{i,t,h}$ is expected excess return over cash or benchmark and $\hat\sigma_{i,t,h}$ is expected horizon volatility. If $h$ is monthly, annualization must be stated separately.

### 0.6.5 Downside-Aware Conviction

$$
\mathrm{DownsideProb}_{i,t,h}(L)=\Pr\left(R_{i,t\rightarrow t+h}^{\mathrm{cum}}<L\mid\mathcal{F}_t\right),
$$

where $L$ is a loss threshold such as $-5\%$ or the return of cash minus a tolerance. This is useful for stress-aware allocation.

## 0.7 Roadmap from Macro Data to Validated Signals to Portfolio-Aware Convictions

The full research process can be organized as a pipeline.

| Stage | Output | Core Controls |
|---|---|---|
| 1. Data ingestion | Point-in-time macro and market panel | Vintage timestamps, release lags, provider metadata. |
| 2. Return construction | Monthly asset returns and forward targets | Total return, futures roll, FX base, option strategy definitions. |
| 3. Feature engineering | Lagged macro and market features | Stationarity-aware transformations and historical-only scaling. |
| 4. Regime estimation | Regime probabilities and transition diagnostics | Filtered probabilities, persistence, economic interpretability. |
| 5. Signal identification | Candidate signal library | Economic rationale, sign, monotonicity, horizon specificity. |
| 6. Forecast modeling | Expected returns, probabilities, risk forecasts | Walk-forward estimation, robust errors, calibration. |
| 7. Statistical validation | Evidence quality report | Out-of-sample tests, bootstrap, multiple-testing controls. |
| 8. Conviction scoring | Asset-level conviction table | Forecast strength, uncertainty, regime confidence, liquidity. |
| 9. Portfolio integration | Tilts, weights, or risk budgets | Constraints, costs, covariance, drawdown, turnover. |
| 10. Monitoring | Live diagnostics and governance | Drift, decay, anomaly detection, audit trails. |

## 0.8 Learning Outcomes for the Full Curriculum

After completing the full curriculum, the reader should be able to:

1. Build point-in-time monthly macro and multi-asset datasets without forward-looking leakage.
2. Engineer macro, market, volatility, futures, options, and cross-asset features that are economically interpretable.
3. Construct forward return targets for $t+1$, $t+3$, and $t+12$ horizons using correct alignment.
4. Distinguish contemporaneous regime classification from forward-looking regime prediction.
5. Estimate statistical and economic regime models, including clustering, hidden Markov models, Markov-switching regressions, dynamic factor models, and Bayesian state-space models.
6. Evaluate signals using information coefficients, rank information coefficients, hit rates, conditional return spreads, payoff ratios, and horizon decay.
7. Use robust inference for overlapping returns, including Newey-West and block-bootstrap methods.
8. Control for multiple-testing bias, data snooping, overfitting, unstable narratives, and structural breaks.
9. Translate validated signals into asset-level convictions and then into portfolio-aware expected returns, active weights, or risk budgets.
10. Build reproducible Python infrastructure with audit trails, model registries, feature stores, and production monitoring.

---

# Part 1: Data Foundations, Timestamping, and Monthly Return Alignment

## 1.1 Why Data Engineering Is the First Quantitative Model

In macro-regime and multi-asset research, data alignment is not an operational detail; it is part of the model. A signal can appear powerful simply because a macro observation was used before it was released, a revised macro value was substituted for a vintage value, a delisted asset was removed from the universe, or a $t+12$ target accidentally overlapped with the feature-construction window.

A correct data foundation answers five questions for every observation:

1. **What economic period does the data describe?** Example: CPI for May.
2. **When was it released or revised?** Example: the initial release date in June and later revisions.
3. **When was it available to the model?** Example: after vendor ingestion and decision cutoff.
4. **Which portfolio decision could have used it?** Example: June-end or July-start allocation.
5. **Which future return window is being predicted?** Example: July return for $t+1$ from a June-end signal.

## 1.2 Required Data Types

The following table summarizes common data categories needed for a multi-asset macro-regime research platform.

| Data Category | Examples | Frequency | Key Timestamp | Major Bias Risk |
|---|---|---:|---|---|
| Macro levels | CPI, payrolls, PMI, industrial production, retail sales | Monthly/quarterly | Release date and vintage date | Revisions and publication lag |
| Policy data | Policy rate, central-bank balance sheet, guidance, meeting dates | Daily/monthly | Announcement timestamp | Event timing and revised histories |
| Rates and curves | Treasury yields, swap rates, real yields, breakevens | Daily/monthly | Market close | Month-end aggregation choice |
| Credit | IG spreads, HY spreads, CDS indices, lending standards | Daily/monthly/quarterly | Market close or survey release | Liquidity and index composition |
| Equities | Price indices, total return indices, sectors, countries, styles | Daily/monthly | Market close | Survivorship and dividends |
| FX | Spot, forwards, carry, real effective exchange rates | Daily/monthly | Market close | Base currency and holiday calendars |
| Commodities | Spot, futures, curve structure, inventory data | Daily/weekly/monthly | Settlement and roll schedule | Roll methodology and seasonality |
| Futures | Equity, rates, bond, FX, commodity futures | Daily/monthly | Settlement, expiry, roll rule | Back-adjustment and collateral return |
| Options | IV surface, skew, term structure, realized volatility | Daily/monthly | Surface snapshot timestamp | Stale quotes and moneyness conventions |
| Volatility | VIX, MOVE, variance swaps, vol-of-vol indices | Daily/monthly | Market close | Instrument definition changes |
| Alternatives | Trend, carry, value, risk premia, hedge-fund indices | Monthly | Provider publication date | Backfill and survivorship |
| Fundamentals | Earnings, margins, valuations, balance-sheet data | Quarterly/monthly | Filing/report date | Restatements and data availability |

## 1.3 Timestamp Convention

A production-grade dataset should separate at least four timestamps.

| Timestamp | Symbol | Definition | Example |
|---|---:|---|---|
| Reference period | $\tau^{\mathrm{ref}}$ | Economic period described by the observation. | May 2026 CPI. |
| Release timestamp | $\tau^{\mathrm{rel}}$ | When the data was first officially released. | June 2026 CPI release date. |
| Vendor availability timestamp | $\tau^{\mathrm{avail}}$ | When the data was available in the research database. | Vendor ingestion time. |
| Decision timestamp | $t$ | Portfolio signal timestamp. | 2026-06-30 month-end decision. |

A feature $x_t$ is valid for a decision at $t$ only if:

$$
\tau^{\mathrm{avail}}(x)\leq t_{\mathrm{cutoff}},
$$

where $t_{\mathrm{cutoff}}$ is the decision cutoff time. If the portfolio is formed at the close of the last trading day of the month, then market prices from that close may or may not be tradable depending on the execution convention. A conservative process often assumes signals computed using month-end close are implemented at the next month’s open or next month’s closing rebalance.

## 1.4 Point-in-Time Data and Vintage Macro Databases

Macro vintage data records what was known at a given historical date. Let $x_{q}^{(v)}$ denote a macro value for reference period $q$ as known in vintage $v$. A point-in-time feature at decision timestamp $t$ should use:

$$
x_{q,t}^{\mathrm{PIT}} = x_q^{(v^*)},
\qquad
v^* = \max\{v: v\leq t_{\mathrm{cutoff}}\}.
$$

Here, $v^*$ is the latest vintage available before the decision cutoff. The assumption is that the model can only use the most recent vintage known at the time.

### 1.4.1 Conservative Lagging When Vintage Data Is Unavailable

If vintage data is unavailable, a conservative approximation is to lag macro features by at least one publication cycle:

$$
\tilde x_t = x_{t-L},
$$

where $L$ is the number of months of assumed availability lag. This is less accurate than vintage data because it may discard valid information and still fail to capture revisions, but it is usually safer than using final revised values contemporaneously.

**Practical rule.** If a macro variable has a release lag of one month and revisions are material, test both a conservative lagged version and a vintage version if possible. Do not use final revised values as if they were known in real time.

## 1.5 Monthly Return Calculation

### 1.5.1 Monthly Arithmetic Return

For an asset price or total return index $P_{i,t}$ observed at month-end $t$, the monthly arithmetic return is:

$$
r_{i,t}=\frac{P_{i,t}}{P_{i,t-1}}-1,
$$

where $P_{i,t}$ is the investable total return index level, adjusted price, or strategy net asset value for asset $i$ at the end of month $t$. If $P$ is a price-only index, the return excludes dividends or coupons unless these are added separately.

### 1.5.2 Monthly Log Return

The monthly log return is:

$$
g_{i,t}=\log\left(\frac{P_{i,t}}{P_{i,t-1}}\right)=\log(1+r_{i,t}).
$$

Log returns are additive across time, which is convenient for multi-month decomposition, but portfolio returns are naturally arithmetic because weights compound multiplicatively.

### 1.5.3 Total Return Requirement

For equities, credit, bonds, commodities, and many alternatives, total return is usually the correct modeling target. Price returns alone can materially distort performance, especially for high-dividend equities, coupon-bearing bonds, carry strategies, and collateralized futures strategies.

## 1.6 Return Construction by Asset Type

### 1.6.1 Equity and Equity Sector Returns

Equity returns should preferably use total return indices:

$$
r_{i,t}^{\mathrm{eq}} = \frac{TRI_{i,t}}{TRI_{i,t-1}}-1,
$$

where $TRI_{i,t}$ is the total return index for equity asset $i$. If only price returns are available, dividends must be included separately:

$$
r_{i,t}^{\mathrm{eq}}=\frac{P_{i,t}+D_{i,t}}{P_{i,t-1}}-1,
$$

where $D_{i,t}$ is the dividend paid during month $t$.

### 1.6.2 Bond and Duration Returns

Bond index returns should use total return indices that include coupons and price changes. A stylized approximation for a duration asset is:

$$
r_{t}^{\mathrm{bond}} \approx y_{t-1}\Delta t - D_{t-1}\Delta y_t
+\frac{1}{2}C_{t-1}(\Delta y_t)^2,
$$

where $y_{t-1}$ is beginning yield, $\Delta t$ is the month fraction, $D_{t-1}$ is modified duration, $\Delta y_t$ is the yield change, and $C_{t-1}$ is convexity. This equation is an approximation; actual index returns depend on curve changes, coupons, roll-down, security composition, and reinvestment.

### 1.6.3 Credit Returns

Credit returns combine rate exposure, spread exposure, carry, defaults, and recovery effects. A simplified credit-index return approximation is:

$$
r_t^{\mathrm{credit}} \approx y_{t-1}\Delta t
- D^{\mathrm{rate}}_{t-1}\Delta y_t
- D^{\mathrm{spread}}_{t-1}\Delta s_t
- \mathrm{DefaultLoss}_t,
$$

where $s_t$ is the credit spread, $D^{\mathrm{spread}}$ is spread duration, and $\mathrm{DefaultLoss}_t$ is the loss from defaults net of recoveries.

### 1.6.4 FX Returns

For an investor with base currency $B$ holding foreign currency $F$, the spot FX return may be expressed as:

$$
r_{F/B,t}=\frac{S_{F/B,t}}{S_{F/B,t-1}}-1,
$$

where $S_{F/B,t}$ is the amount of base currency $B$ per unit of foreign currency $F$. If $S$ rises, the foreign currency appreciates relative to the base currency under this quotation convention. Hedged and unhedged returns must be clearly separated.

### 1.6.5 Futures Returns

A collateralized futures strategy return can be decomposed as:

$$
r_t^{\mathrm{fut,total}}
= r_t^{\mathrm{fut,price}} + r_t^{\mathrm{collateral}} - c_t^{\mathrm{roll}} - c_t^{\mathrm{fees}},
$$

where $r_t^{\mathrm{fut,price}}$ is the return from futures price changes, $r_t^{\mathrm{collateral}}$ is the return on collateral, $c_t^{\mathrm{roll}}$ represents losses or gains embedded in the roll implementation convention, and $c_t^{\mathrm{fees}}$ includes transaction and operational costs. In practice, roll yield is not merely an accounting term; it depends on curve shape, roll schedule, contract liquidity, collateral assumptions, and position direction.

### 1.6.6 Option Strategy Returns

An option strategy return must specify the strategy construction, rebalancing, delta-hedging, collateral, margin, implied-volatility surface timestamp, transaction costs, and expiration handling. A simplified one-month option strategy return can be written as:

$$
r_t^{\mathrm{opt}}=\frac{V_t - V_{t-1} - \mathrm{TC}_t + \mathrm{CollateralIncome}_t}{\mathrm{Capital}_{t-1}},
$$

where $V_t$ is strategy value, $\mathrm{TC}_t$ is transaction cost, and $\mathrm{Capital}_{t-1}$ is the capital base or margin-adjusted capital definition. Option returns are path-dependent and nonlinear; monthly endpoint returns may hide large intra-month risk.

## 1.7 Forward Return Alignment

For each asset $i$ and decision timestamp $t$, the $h$-month forward arithmetic cumulative return is:

$$
R_{i,t,h}=\prod_{j=1}^{h}(1+r_{i,t+j})-1.
$$

For $h=1$:

$$
R_{i,t,1}=r_{i,t+1}.
$$

For $h=3$:

$$
R_{i,t,3}=(1+r_{i,t+1})(1+r_{i,t+2})(1+r_{i,t+3})-1.
$$

For $h=12$:

$$
R_{i,t,12}=\prod_{j=1}^{12}(1+r_{i,t+j})-1.
$$

The corresponding excess return over cash is:

$$
R^{e}_{i,t,h}=R_{i,t,h}-R_{c,t,h},
$$

where $R_{c,t,h}$ is the cumulative cash return over the same future window.

The excess return over a benchmark $b$ is:

$$
R^{b}_{i,t,h}=R_{i,t,h}-R_{b,t,h}.
$$

**Alignment rule.** Features at row $t$ must align with target returns that begin after $t$. In a pandas DataFrame indexed by month-end, a common error is to use `rolling` or `shift` in a way that accidentally includes current or future returns. The safest pattern is to compute realized future returns explicitly using negative shifts after returns are calculated.

## 1.8 Overlapping Versus Non-Overlapping Forward Returns

For $h=3$ and $h=12$, monthly observations generate overlapping forward returns. For example, the $t+12$ return from January to next January overlaps heavily with the $t+12$ return from February to next February. This produces serial correlation in regression residuals and forecast errors.

If a predictive regression is:

$$
R_{i,t,h}=\alpha_i+\beta_i z_{i,t}+\varepsilon_{i,t,h},
$$

then $\varepsilon_{i,t,h}$ is likely serially correlated for $h>1$. Ordinary least-squares coefficients may remain useful under assumptions, but naive standard errors are typically too optimistic. Inference should use Newey-West standard errors, block bootstrap, or non-overlapping robustness checks.

A practical Newey-West lag choice for monthly overlapping returns is often related to $h-1$:

$$
L_{NW}\geq h-1,
$$

where $L_{NW}$ is the number of autocorrelation lags used in the heteroskedasticity-and-autocorrelation-consistent covariance estimate. This is a rule of thumb, not a universal optimum.

## 1.9 Currency Base and Hedged Versus Unhedged Returns

A multi-asset research system must define the base currency. Let $R_{i,t}^{\mathrm{local}}$ be the local-currency return of asset $i$ and $R_{FX,t}$ be the return of the local currency versus the investor’s base currency. The unhedged base-currency return is:

$$
1+R_{i,t}^{\mathrm{base}}
= (1+R_{i,t}^{\mathrm{local}})(1+R_{FX,t}).
$$

Thus:

$$
R_{i,t}^{\mathrm{base}}
= R_{i,t}^{\mathrm{local}}+R_{FX,t}+R_{i,t}^{\mathrm{local}}R_{FX,t}.
$$

The cross term is usually small monthly but should not be ignored in exact calculations.

For hedged returns, the hedge return depends on interest-rate differentials, forward points, hedge frequency, collateral, and hedge slippage. A simplified approximation is:

$$
R_{i,t}^{\mathrm{hedged}}
\approx R_{i,t}^{\mathrm{local}} + \mathrm{Carry}_{F/B,t} - \mathrm{HedgeCost}_t.
$$

## 1.10 Asset Universe Construction and Survivorship Bias

An asset universe $\mathcal{U}_t$ should be time-varying:

$$
\mathcal{U}_t=\{i: \mathrm{InceptionDate}_i\leq t,\; \mathrm{Tradable}_i(t)=1,\; \mathrm{Liquidity}_i(t)\geq L_{\min}\}.
$$

Using today’s universe for a historical test creates survivorship bias. For example, a country index, ETF, futures contract, or alternative risk-premia strategy that exists today may not have existed historically. Similarly, delisted assets and failed strategies should not disappear from the historical universe if they were investable at the time.

Universe filters should be lagged. If a liquidity filter is based on average volume over the prior three months, then the feature must be computed using only data available at $t$, not future liquidity.

## 1.11 Missing Data, Stale Prices, and Inception Dates

Missing data should not be filled mechanically without understanding why it is missing.

| Missingness Type | Example | Recommended Treatment |
|---|---|---|
| Not yet listed | ETF before inception | Keep as unavailable; do not backfill unless using a documented proxy. |
| Holiday mismatch | FX and futures calendar differences | Align to valid month-end business dates by market calendar. |
| Stale price | Illiquid index unchanged for several days | Flag staleness; consider excluding or using lower frequency. |
| Macro not released | Indicator unavailable at decision time | Carry last available vintage if economically justified. |
| Provider error | Bad print or missing index level | Validate with tolerance checks and audit logs. |
| Structural break | Series definition changes | Add metadata, splice carefully, or model separately. |

A production system should store both the raw value and the cleaned value, with audit metadata explaining transformations.

## 1.12 Python: Point-in-Time Monthly Data Alignment and Forward Return Construction

The following code uses synthetic data and is intended to demonstrate alignment logic. It does not use live market data. The functions are modular so they can be integrated into a larger research platform.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class AlignmentConfig:
    """Configuration for monthly signal and forward-return alignment.

    Parameters
    ----------
    horizons : tuple[int, ...]
        Forward horizons in months. Common values are (1, 3, 12).
    min_price : float
        Minimum valid price or index level. Non-positive prices are invalid
        for return calculation.
    decision_lag_months : int
        Number of months by which features are conservatively lagged after
        availability processing. Use 0 only when point-in-time availability
        is explicitly handled.
    """

    horizons: tuple[int, ...] = (1, 3, 12)
    min_price: float = 0.0
    decision_lag_months: int = 0


def _require_monthly_datetime_index(df: pd.DataFrame, name: str) -> None:
    """Validate that a DataFrame has a monotonic monthly DatetimeIndex."""
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError(f"{name} must have a pandas DatetimeIndex.")
    if not df.index.is_monotonic_increasing:
        raise ValueError(f"{name} index must be sorted in increasing order.")
    if df.index.has_duplicates:
        raise ValueError(f"{name} index contains duplicate timestamps.")
    if len(df.index) < 3:
        raise ValueError(f"{name} must contain at least 3 monthly observations.")


def compute_monthly_returns(
    prices: pd.DataFrame,
    *,
    log_returns: bool = False,
    min_price: float = 0.0,
) -> pd.DataFrame:
    """Compute monthly returns from month-end price or total return levels.

    Parameters
    ----------
    prices : pd.DataFrame
        Month-end investable levels. Columns are assets, rows are month-end
        timestamps. Prefer total return indices where possible.
    log_returns : bool
        If True, return log returns. If False, return arithmetic returns.
    min_price : float
        Minimum valid price level. Values less than or equal to this are
        treated as missing.

    Returns
    -------
    pd.DataFrame
        Monthly returns aligned to the ending month. The return at row t is
        the return from t-1 to t.
    """
    _require_monthly_datetime_index(prices, "prices")
    clean = prices.astype(float).where(prices.astype(float) > min_price)
    if log_returns:
        returns = np.log(clean / clean.shift(1))
    else:
        returns = clean.pct_change(fill_method=None)
    return returns.replace([np.inf, -np.inf], np.nan)


def make_forward_returns(
    monthly_returns: pd.DataFrame,
    horizons: Sequence[int] = (1, 3, 12),
    *,
    use_log: bool = False,
) -> dict[int, pd.DataFrame]:
    """Construct forward returns using strictly future monthly returns.

    Parameters
    ----------
    monthly_returns : pd.DataFrame
        Monthly returns where row t is the return from t-1 to t.
    horizons : Sequence[int]
        Forward horizons in months.
    use_log : bool
        If True, assume monthly_returns are log returns and sum them.
        If False, assume arithmetic returns and compound them.

    Returns
    -------
    dict[int, pd.DataFrame]
        Mapping from horizon h to a DataFrame whose row t contains the
        realized forward return from t+1 through t+h.
    """
    _require_monthly_datetime_index(monthly_returns, "monthly_returns")
    out: dict[int, pd.DataFrame] = {}

    for h in horizons:
        if h < 1:
            raise ValueError("All horizons must be positive integers.")

        if use_log:
            # Sum future log returns: g_{t+1} + ... + g_{t+h}.
            fwd = sum(monthly_returns.shift(-j) for j in range(1, h + 1))
        else:
            # Compound future arithmetic returns.
            gross = pd.DataFrame(
                1.0,
                index=monthly_returns.index,
                columns=monthly_returns.columns,
            )
            for j in range(1, h + 1):
                gross = gross * (1.0 + monthly_returns.shift(-j))
            fwd = gross - 1.0

        out[h] = fwd.replace([np.inf, -np.inf], np.nan)

    return out


def apply_publication_lag(
    macro: pd.DataFrame,
    release_lag_months: int | pd.Series | dict[str, int],
) -> pd.DataFrame:
    """Apply a conservative release lag to macro features.

    Parameters
    ----------
    macro : pd.DataFrame
        Macro data indexed by reference month. These may be final values if
        true vintage data is unavailable.
    release_lag_months : int, Series, or dict
        Lag in months. If an integer, the same lag is applied to all columns.
        If a dict or Series, each macro column can have its own lag.

    Returns
    -------
    pd.DataFrame
        Lagged macro data, aligned so row t only contains information that
        would have been available after the assumed lag.
    """
    _require_monthly_datetime_index(macro, "macro")

    if isinstance(release_lag_months, int):
        if release_lag_months < 0:
            raise ValueError("release_lag_months cannot be negative.")
        return macro.shift(release_lag_months)

    lag_map = pd.Series(release_lag_months)
    missing = set(macro.columns) - set(lag_map.index)
    if missing:
        raise ValueError(f"Missing lag values for columns: {sorted(missing)}")

    lagged = pd.DataFrame(index=macro.index, columns=macro.columns, dtype=float)
    for col in macro.columns:
        lag = int(lag_map[col])
        if lag < 0:
            raise ValueError(f"Lag for {col} cannot be negative.")
        lagged[col] = macro[col].shift(lag)
    return lagged


def align_features_and_targets(
    features: pd.DataFrame,
    fwd_returns: dict[int, pd.DataFrame],
    *,
    asset_names: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Create a long panel with features at t and asset targets after t.

    Parameters
    ----------
    features : pd.DataFrame
        Point-in-time features indexed by decision timestamp t.
    fwd_returns : dict[int, pd.DataFrame]
        Forward returns from make_forward_returns.
    asset_names : iterable[str] or None
        Optional subset of asset columns to include.

    Returns
    -------
    pd.DataFrame
        Long panel with MultiIndex (date, asset). Feature columns are observed
        at date t. Target columns are named fwd_return_{h}m.
    """
    _require_monthly_datetime_index(features, "features")
    if not fwd_returns:
        raise ValueError("fwd_returns cannot be empty.")

    common_index = features.index.copy()
    for h, target in fwd_returns.items():
        _require_monthly_datetime_index(target, f"fwd_returns[{h}]")
        common_index = common_index.intersection(target.index)

    features = features.loc[common_index].copy()
    first_target = next(iter(fwd_returns.values())).loc[common_index]
    assets = list(asset_names) if asset_names is not None else list(first_target.columns)

    records = []
    for asset in assets:
        asset_frame = features.copy()
        asset_frame["asset"] = asset
        for h, target in fwd_returns.items():
            if asset not in target.columns:
                raise ValueError(f"Asset {asset} not found in target for horizon {h}.")
            asset_frame[f"fwd_return_{h}m"] = target.loc[common_index, asset]
        records.append(asset_frame)

    panel = pd.concat(records, axis=0)
    panel["date"] = np.tile(common_index.to_numpy(), len(assets))
    panel = panel.set_index(["date", "asset"]).sort_index()
    return panel
```

## 1.13 Python: Synthetic Example of Correct Alignment

```python
import numpy as np
import pandas as pd

# Reproducible synthetic data. This is hypothetical and only demonstrates
# alignment mechanics.
rng = np.random.default_rng(42)
dates = pd.date_range("2000-01-31", periods=180, freq="M")

assets = ["Global_Equity", "US_10Y_Duration", "Commodities", "USD_Index"]
price_levels = pd.DataFrame(
    100.0 * np.exp(np.cumsum(rng.normal(0.004, 0.035, size=(len(dates), len(assets))), axis=0)),
    index=dates,
    columns=assets,
)

macro = pd.DataFrame(
    {
        "growth_pmi": 50 + rng.normal(0, 2.5, len(dates)).cumsum() / 15,
        "inflation_yoy": 2.0 + rng.normal(0, 0.25, len(dates)).cumsum() / 10,
        "credit_spread": 3.0 + rng.normal(0, 0.15, len(dates)).cumsum(),
    },
    index=dates,
)

# Step 1: compute monthly asset returns from total return levels.
monthly_returns = compute_monthly_returns(price_levels)

# Step 2: construct future return targets.
fwd = make_forward_returns(monthly_returns, horizons=(1, 3, 12), use_log=False)

# Step 3: conservatively lag macro data by one month to reflect release delay.
macro_lagged = apply_publication_lag(macro, release_lag_months=1)

# Step 4: create simple historically scaled features using only past data.
def expanding_zscore(x: pd.Series, min_periods: int = 36) -> pd.Series:
    mean = x.expanding(min_periods=min_periods).mean().shift(1)
    std = x.expanding(min_periods=min_periods).std(ddof=1).shift(1)
    return (x - mean) / std.replace(0, np.nan)

features = macro_lagged.apply(expanding_zscore)
features.columns = [f"z_{c}" for c in features.columns]

# Step 5: align point-in-time features with future returns.
panel = align_features_and_targets(features, fwd)

print(panel.dropna().head())
```

**Expected output.** The resulting panel has a MultiIndex of `(date, asset)`. Each row contains macro features known at `date` and forward returns for the specified asset after `date`. Rows near the beginning are missing because expanding z-scores require a minimum history. Rows near the end are missing because future returns cannot be computed without future months.

## 1.14 Python: Alignment Diagnostics

The following diagnostic checks are designed to catch common leakage and target-construction errors.

```python
def alignment_diagnostics(
    features: pd.DataFrame,
    fwd_returns: dict[int, pd.DataFrame],
    monthly_returns: pd.DataFrame,
) -> pd.DataFrame:
    """Return a diagnostic table for feature and target alignment.

    The diagnostics do not prove absence of leakage, but they catch common
    structural errors: unsorted dates, unexpected target availability, and
    insufficient missing values at the end for forward horizons.
    """
    _require_monthly_datetime_index(features, "features")
    _require_monthly_datetime_index(monthly_returns, "monthly_returns")

    rows = []
    for h, target in fwd_returns.items():
        _require_monthly_datetime_index(target, f"fwd_returns[{h}]")
        last_valid_by_asset = target.apply(lambda s: s.last_valid_index())
        min_tail_missing = target.tail(h).isna().sum().min()
        rows.append(
            {
                "horizon_months": h,
                "target_rows": len(target),
                "target_columns": target.shape[1],
                "min_missing_in_last_h_rows": int(min_tail_missing),
                "latest_valid_target_date_min": last_valid_by_asset.min(),
                "latest_valid_target_date_max": last_valid_by_asset.max(),
            }
        )

    return pd.DataFrame(rows)


diag = alignment_diagnostics(features, fwd, monthly_returns)
print(diag)
```

A correctly aligned $h$-month target will generally have missing values in the final $h$ rows because the future return window is unavailable at the end of the sample. If a $t+12$ target has valid values through the final month of the data, it is usually a warning sign unless the dataset includes additional future months beyond the displayed research window.

## 1.15 Python: Visualizing Feature and Forward Return Availability

The following code creates a simple availability chart. It uses `matplotlib` and avoids custom styling so it can run in basic research environments.

```python
import matplotlib.pyplot as plt


def plot_availability_matrix(df: pd.DataFrame, title: str) -> None:
    """Plot missing-data availability for a DataFrame.

    White gaps in the image indicate missing observations. This is useful for
    identifying macro release lags, asset inception dates, and target truncation.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("df cannot be empty.")

    available = df.notna().astype(int)
    fig, ax = plt.subplots(figsize=(10, max(3, 0.35 * df.shape[1])))
    ax.imshow(available.T, aspect="auto", interpolation="nearest")
    ax.set_title(title)
    ax.set_yticks(range(df.shape[1]))
    ax.set_yticklabels(df.columns)
    ax.set_xlabel("Time index")
    ax.set_ylabel("Series")
    plt.tight_layout()
    plt.show()


plot_availability_matrix(features, "Point-in-Time Feature Availability")
plot_availability_matrix(fwd[12], "t+12 Forward Return Target Availability")
```

## 1.16 Practical Data Architecture for Part 1

A production-aware data architecture should separate raw data, cleaned data, feature data, target data, and model-ready panels.

| Layer | Stored Object | Required Metadata | Example Validation |
|---|---|---|---|
| Raw data | Vendor files and API pulls | Source, pull time, vendor version | Schema and checksum checks. |
| Vintage macro | Values by reference date and vintage date | Release time, revision number | No future vintage used at decision time. |
| Clean market data | Adjusted prices and total return indices | Corporate actions, roll rules | Return outlier checks. |
| Feature store | Lagged and transformed features | Transformation, lookback, availability | Historical-only scaling tests. |
| Target store | Forward returns and labels | Horizon, compounding rule | Missing tail checks. |
| Research panel | Joined features and targets | Universe, timestamp convention | Reproducibility hash. |
| Backtest input | Signals, forecasts, constraints | Model version, run ID | Audit trail and configuration lock. |

## 1.17 Data Quality Checklist

| Check | Question | Failure Mode |
|---|---|---|
| Timestamp integrity | Are reference, release, availability, and decision dates separate? | Macro look-ahead bias. |
| Vintage integrity | Are macro values point-in-time? | Revised-data bias. |
| Return basis | Are returns total return, price return, hedged, or unhedged? | Misstated asset performance. |
| Forward alignment | Do targets begin after the signal date? | Direct leakage. |
| Tail missingness | Are final $h$ rows missing for $h$-month targets? | Future data accidentally included. |
| Universe integrity | Is universe membership known at $t$? | Survivorship bias. |
| Inception dates | Are unavailable assets excluded before inception? | Backfill bias. |
| Stale prices | Are unchanged or illiquid series flagged? | Understated volatility. |
| Calendar consistency | Are month-end dates aligned across markets? | False signal timing. |
| FX base | Is base currency explicit? | Misinterpreted international returns. |
| Cost convention | Are costs included or excluded? | Overstated implementability. |
| Auditability | Can every feature be traced to raw data? | Unrepeatable research. |

## 1.18 Bias and Leakage Checklist for Monthly Alignment

| Bias Type | Description | Control |
|---|---|---|
| Look-ahead bias | Using information unavailable at timestamp $t$. | Enforce availability timestamps and lag features. |
| Revision bias | Using final macro values rather than real-time vintages. | Use vintage databases or conservative lags. |
| Survivorship bias | Testing only assets that survived to the present. | Use point-in-time universe membership. |
| Backfill bias | Including historical data added after a strategy became successful. | Track provider backfill dates and live-start dates. |
| Scaling leakage | Standardizing using full-sample mean or volatility. | Use rolling or expanding statistics shifted by one period. |
| Ranking leakage | Ranking assets using future constituents or future data. | Rank only within $\mathcal{U}_t$ using information at $t$. |
| Target leakage | Features include components of the forward return. | Audit transformations and target windows. |
| Overlap inference error | Treating overlapping observations as independent. | Use robust standard errors and bootstrap methods. |
| Calendar leakage | Using data released after month-end decision. | Join by release timestamp, not reference month. |
| Cost omission | Ignoring costs for high-turnover or derivative strategies. | Add cost model and report gross/net results separately. |

## 1.19 Implementation Notes for Institutional Research Engineering

1. **Prefer immutable raw storage.** Raw vendor data should be stored as immutable snapshots with checksums. Never overwrite raw pulls without versioning.
2. **Store vintage macro data in long format.** A useful schema is `(series_id, reference_date, vintage_date, value, source, release_timestamp, ingestion_timestamp)`.
3. **Use explicit feature definitions.** Every feature should have a configuration object specifying source series, lag, transformation, lookback, winsorization, scaling method, and availability rule.
4. **Separate feature creation from target creation.** This reduces accidental use of target information in preprocessing.
5. **Use run manifests.** Each research run should store data version, code commit, model configuration, universe, horizons, and output hash.
6. **Validate before modeling.** Automated checks should block modeling if target tail missingness, timestamp monotonicity, universe membership, or duplicated dates fail.
7. **Design for migration.** Pandas is effective for research prototypes. Large institutional platforms may migrate feature computation to Polars, DuckDB, Spark, dbt, Airflow, Dagster, Scala, numba, C++, or cloud-native data pipelines.

## 1.20 Part 1 Summary

Part 1 established the data foundation required for macro-regime and multi-asset signal research. The key lessons are:

1. Data alignment is a modeling decision, not clerical work.
2. The decision timestamp $t$ must be separated from reference periods, release dates, vintage dates, and vendor availability timestamps.
3. Forward returns for $t+1$, $t+3$, and $t+12$ must use strictly future returns relative to the signal timestamp.
4. Multi-month horizons create overlapping returns, requiring robust inference in later validation.
5. Total return, currency base, futures roll methodology, option strategy construction, and benchmark definitions must be explicit.
6. Point-in-time universes and vintage macro data are critical defenses against overstated performance.
7. Python alignment functions should be modular, validated, auditable, and designed to prevent leakage before any model is estimated.

---

# Stop Point

This installment completes:

1. Global Assumptions.
2. Part 0: Executive Overview and Learning Roadmap.
3. Part 1: Data Foundations, Timestamping, and Monthly Return Alignment.

Continue next with **Part 2: Macro Feature Engineering and Economic Signal Design**.
