# Institutional Macro-Regime Detection, Multi-Asset Signal Identification, and Statistical Validation Curriculum

## Installment 2: Part 2 - Macro Feature Engineering and Economic Signal Design

**Scope of this installment.** This installment continues the curriculum with **Part 2 only**. It assumes the global assumptions, timestamp conventions, forward-return definitions, and monthly alignment rules established in Installment 1.

**Educational boundary.** This document is for research education, model design, and institutional portfolio-process development. It is not personalized investment advice, a live trading recommendation, or a guarantee of alpha.

---

# Part 2: Macro Feature Engineering and Economic Signal Design

## 2.1 Purpose of Macro Feature Engineering

Macro feature engineering converts raw economic and market observations into model-ready variables that can be used for regime detection, signal identification, forecasting, and portfolio construction. Raw macro series are rarely suitable inputs without transformation. Inflation may be reported as an index level, a monthly change, or a year-over-year rate. PMI data may be naturally stationary around a diffusion threshold. Credit spreads may be persistent, skewed, and crisis-sensitive. Real rates may matter through level, change, slope, and interaction with growth. Equity valuations may be slow-moving and useful mainly at long horizons.

A feature is a transformed observation. A signal is a feature, or combination of features, with an explicit economic rationale, expected direction, horizon, universe, implementation convention, and validation record. The distinction matters:

| Object | Definition | Example | Research Requirement |
|---|---|---|---|
| Raw variable | Original economic or market observation. | 10-year Treasury yield. | Timestamp, source, unit, release availability. |
| Feature | Transformed variable designed for modeling. | 12-month change in 10-year yield. | Transformation, lag, scaling, stationarity treatment. |
| Signal | Feature with investment hypothesis and target. | Rising real yields are negative for long-duration equities over $t+3$. | Economic rationale, sign, horizon, validation evidence. |
| Forecast | Model output for a target. | Expected $t+3$ equity sector excess return. | Walk-forward model, uncertainty, calibration. |
| Conviction | Portfolio-aware belief object. | Strong negative conviction on duration-sensitive equities. | Magnitude, confidence, risk, liquidity, failure modes. |

The feature-engineering problem is therefore not only statistical. It is also economic. A statistically convenient transformation that destroys the meaning of a macro variable can create a model that looks precise but cannot be interpreted, stress-tested, or governed.

## 2.2 Timestamp Discipline for Features

Let $x_{m,q}$ denote raw macro variable $m$ for economic reference month $q$. Let $t$ denote the decision timestamp. A valid feature $z_{m,t}$ must satisfy:

$$
z_{m,t}=f_m\left(\{x_{m,q}^{(v)}: \tau^{\mathrm{avail}}(x_{m,q}^{(v)})\leq t_{\mathrm{cutoff}}\}\right),
$$

where $f_m(\cdot)$ is the feature transformation, $v$ is the vintage, $\tau^{\mathrm{avail}}$ is the availability timestamp, and $t_{\mathrm{cutoff}}$ is the cutoff for the portfolio decision. The equation states that every input used in a feature at $t$ must have been available before the decision was made.

A common conservative approximation when release calendars are unavailable is:

$$
z_{m,t}=f_m\left(x_{m,t-L_m},x_{m,t-L_m-1},\ldots\right),
$$

where $L_m$ is a variable-specific publication lag in months. This approach is imperfect because it does not fully solve data revisions, but it is safer than using final values as if they were known in real time.

## 2.3 Transformation Taxonomy

The same raw series can generate multiple features. Each transformation should be tied to an economic interpretation and a forecast horizon.

| Transformation | Formula | Typical Use | Main Risk |
|---|---:|---|---|
| Level | $x_t$ | Policy rate, unemployment, PMI, credit spread. | Nonstationarity or regime-dependent scale. |
| Difference | $x_t-x_{t-k}$ | Yield changes, spread changes, inflation acceleration. | Noisy when $k$ is short. |
| Percent change | $x_t/x_{t-k}-1$ | Money supply, earnings, production. | Invalid near zero or negative values. |
| Log change | $\log x_t-\log x_{t-k}$ | Positive index levels, prices, production. | Requires positive observations. |
| Year-over-year change | $x_t/x_{t-12}-1$ | CPI, wages, sales, production. | Slow response and base effects. |
| Rolling z-score | $(x_t-\mu_{t,W})/\sigma_{t,W}$ | Relative extremes versus recent history. | Lookback sensitivity. |
| Expanding z-score | $(x_t-\mu_{t}^{exp})/\sigma_{t}^{exp}$ | Long-history standardization. | Structural-break contamination. |
| Percentile rank | $\mathrm{rank}_W(x_t)$ | Robust nonlinear thresholding. | Discrete and sample-dependent. |
| Surprise | $x_t-\mathbb{E}_{t^-}[x_t]$ | Data-release shock modeling. | Survey availability and timestamping. |
| Diffusion index | Share of indicators improving. | Breadth of macro improvement. | Indicator correlation and double counting. |
| Regime threshold | $\mathbf{1}\{x_t>c\}$ | PMI above 50, curve inversion. | Brittle thresholds. |
| Interaction | $z_{a,t}z_{b,t}$ | Growth-inflation mix, policy-real-rate stress. | Overfitting and interpretability. |

Here $W$ is the rolling lookback window, $k$ is the transformation horizon in months, $\mu$ is the historical mean, and $\sigma$ is the historical standard deviation. Every rolling or expanding statistic must be estimated using only observations available before or at the decision timestamp, and, for predictive modeling, the scaling statistics are often shifted by one period to avoid using the contemporaneous value in its own normalization.

## 2.4 Levels, Differences, Percent Changes, and Log Changes

### 2.4.1 Level Features

A level feature is:

$$
z_t^{\mathrm{level}}=x_t.
$$

This is appropriate when the economic meaning of the level is stable. Examples include PMI relative to 50, unemployment rate relative to estimated full employment, real policy rate, credit spread level, or yield-curve slope. Level features are often meaningful for state classification, but not always for return prediction.

**Interpretation.** If $x_t$ is the high-yield credit spread in percentage points, a high level may indicate elevated credit stress or higher future carry. The sign of its asset-return implication depends on horizon and whether the spread is high because of compensation or because default risk is rising.

### 2.4.2 Difference Features

A $k$-month difference is:

$$
z_t^{\Delta,k}=x_t-x_{t-k}.
$$

This measures the direction and magnitude of change in the original units of $x$. It is appropriate for yields, spreads, policy rates, unemployment rates, diffusion indices, and valuation spreads.

**Example.** If $x_t$ is the unemployment rate, $x_t-x_{t-3}>0$ indicates labor-market deterioration over the last quarter. This may matter more for risk assets over $t+3$ than the unemployment level alone.

### 2.4.3 Percent Change Features

For strictly positive series, a $k$-month percent change is:

$$
z_t^{\%,k}=\frac{x_t}{x_{t-k}}-1.
$$

This is commonly used for industrial production, money supply, earnings, sales, and price indices. It should not be used for variables that can be zero, negative, or close to zero.

### 2.4.4 Log Change Features

For strictly positive series, the $k$-month log change is:

$$
z_t^{\log,k}=\log(x_t)-\log(x_{t-k}).
$$

When multiplied by 100, this approximates a percentage change for small moves. Log changes are additive over time and often useful for macro indices and price levels.

## 2.5 Year-over-Year Changes and Base Effects

A year-over-year growth rate is:

$$
z_t^{\mathrm{YoY}}=\frac{x_t}{x_{t-12}}-1,
$$

or, for log values:

$$
z_t^{\mathrm{YoY,log}}=\log(x_t)-\log(x_{t-12}).
$$

Year-over-year transformations reduce seasonality and are common for CPI, wages, retail sales, industrial production, money supply, earnings, and revenue. However, year-over-year features can be distorted by base effects. A high year-over-year inflation rate may reflect a low comparison base rather than current inflation momentum.

A useful decomposition is to compare year-over-year inflation with shorter-horizon annualized inflation:

$$
\pi_t^{3m,ann}=\left(\frac{P_t}{P_{t-3}}\right)^4-1,
$$

where $P_t$ is a price index and $\pi_t^{3m,ann}$ is the three-month annualized inflation rate. This feature responds faster than year-over-year inflation but is noisier.

## 2.6 Rolling and Expanding Z-Scores

### 2.6.1 Rolling Z-Score

A rolling z-score using a historical window $W$ is:

$$
z_t^{\mathrm{roll}}=\frac{x_t-\mu_{t,W}}{\sigma_{t,W}},
$$

where:

$$
\mu_{t,W}=\frac{1}{W}\sum_{j=1}^{W}x_{t-j},
$$

and:

$$
\sigma_{t,W}=\sqrt{\frac{1}{W-1}\sum_{j=1}^{W}(x_{t-j}-\mu_{t,W})^2}.
$$

The statistics are computed using $x_{t-1},\ldots,x_{t-W}$ rather than including $x_t$. This convention makes the standardization strictly historical relative to $x_t$.

**Interpretation.** A rolling z-score of $+2$ means the current value is two trailing-window standard deviations above the prior-window mean.

### 2.6.2 Expanding Z-Score

An expanding z-score is:

$$
z_t^{\mathrm{exp}}=\frac{x_t-\mu_t^{\mathrm{exp}}}{\sigma_t^{\mathrm{exp}}},
$$

where:

$$
\mu_t^{\mathrm{exp}}=\frac{1}{t-t_0}\sum_{s=t_0}^{t-1}x_s,
$$

and $\sigma_t^{\mathrm{exp}}$ is the sample standard deviation over $x_{t_0},\ldots,x_{t-1}$. Expanding z-scores use more data and are less noisy than short rolling z-scores, but they are vulnerable to structural breaks.

### 2.6.3 Robust Z-Score

For skewed or crisis-sensitive variables such as credit spreads, volatility indices, and funding spreads, a robust z-score can be useful:

$$
z_t^{\mathrm{robust}}=\frac{x_t-\mathrm{median}_{t,W}(x)}{1.4826\cdot \mathrm{MAD}_{t,W}(x)},
$$

where $\mathrm{MAD}$ is the median absolute deviation over the trailing window. The factor 1.4826 scales MAD to approximate standard deviation under normality.

## 2.7 Percentile Ranks and Threshold Features

A rolling percentile-rank feature is:

$$
z_t^{\mathrm{pct},W}=\frac{1}{W}\sum_{j=1}^{W}\mathbf{1}\{x_{t-j}\leq x_t\}.
$$

This maps the current observation to $[0,1]$ relative to a trailing historical window. It is often more robust than a z-score for non-Gaussian variables.

A threshold feature is:

$$
z_t^{\mathrm{thr}}=\mathbf{1}\{x_t>c\},
$$

where $c$ is an economically meaningful threshold. Examples include PMI above 50, yield curve below zero, credit spread above a crisis percentile, or inflation above the central-bank target range.

Thresholds are interpretable but brittle. A PMI of 49.9 and 50.1 may not imply materially different regimes. A smoother alternative is a logistic threshold:

$$
z_t^{\mathrm{soft}}=\frac{1}{1+\exp[-a(x_t-c)]},
$$

where $a>0$ controls threshold sharpness.

## 2.8 Stationarity Testing and Transformation Choices

Many macro series are persistent and may be nonstationary. Predictive modeling with nonstationary variables can produce spurious relationships if not handled carefully. Stationarity testing should guide transformations, but it should not be applied mechanically.

### 2.8.1 Conceptual Definitions

A series $x_t$ is weakly stationary if its mean, variance, and autocovariance structure do not depend on time:

$$
\mathbb{E}[x_t]=\mu,
$$

$$
\mathrm{Var}(x_t)=\sigma^2,
$$

$$
\mathrm{Cov}(x_t,x_{t-k})=\gamma_k.
$$

If a series has a unit root, shocks can have permanent effects. A simple unit-root process is:

$$
x_t=x_{t-1}+\varepsilon_t,
$$

where $\varepsilon_t$ is a zero-mean innovation. In this case, the level is nonstationary while the first difference $\Delta x_t=x_t-x_{t-1}$ may be stationary.

### 2.8.2 Common Tests

| Test | Null Hypothesis | Alternative | Practical Use |
|---|---|---|---|
| ADF | Unit root / nonstationary | Stationary | Tests whether differencing may be needed. |
| KPSS | Stationary | Unit root or trend-stationary violation | Complements ADF because null is reversed. |
| Phillips-Perron | Unit root | Stationary | Robusts to some serial correlation and heteroskedasticity. |
| Zivot-Andrews | Unit root with break | Stationary with one break | Useful when structural breaks are suspected. |

Stationarity tests have low power in short monthly samples. A feature should be chosen using both statistical diagnostics and economic meaning.

### 2.8.3 Transformation Decision Table

| Series Type | Example | Likely Feature Set | Comments |
|---|---|---|---|
| Naturally bounded diffusion | PMI, survey breadth | Level, change, threshold, z-score. | Level around threshold is meaningful. |
| Persistent rate | Unemployment, policy rate | Level, change, gap versus neutral. | Level can define state; change can forecast transitions. |
| Positive index level | CPI index, production index | MoM, 3m annualized, YoY, log change. | Avoid raw level unless modeling long-run trend. |
| Yield or spread | 10Y yield, credit spread | Level, change, slope, percentile, robust z-score. | Level and change both have economic meaning. |
| Valuation ratio | P/E, CAPE, earnings yield | Level, z-score, percentile, relative spread. | More useful at $t+12$ than $t+1$. |
| Volatility index | VIX, MOVE | Level, change, term structure, percentile. | Skewed and crisis-sensitive. |
| Balance-sheet quantity | money supply, reserves | Growth rate, change, ratio to GDP. | Regime shifts and definitional changes matter. |
| Price-like market series | equity index, commodity price | Return, trend, drawdown, momentum. | Raw level generally not comparable over time. |

## 2.9 Macro Indicator Categories

A macro-regime model should not rely on one indicator family. A balanced framework uses multiple categories so that the state estimate is not dominated by one noisy release.

| Category | Representative Variables | Feature Examples | Main Asset Channels |
|---|---|---|---|
| Growth | PMI, ISM, industrial production, GDP nowcast, retail sales. | Level, 3m change, diffusion breadth. | Earnings, commodities, credit, cyclicals. |
| Inflation | CPI, PCE, wages, breakevens, inflation swaps. | YoY, 3m annualized, surprise, breadth. | Rates, equities, commodities, FX, volatility. |
| Labor | Payrolls, unemployment, jobless claims, participation. | Change, gap, claims momentum. | Policy reaction, income, consumption. |
| Credit | IG/HY spreads, default rates, lending standards. | Spread level, spread change, percentile. | Risk appetite, financing, equity drawdowns. |
| Liquidity | reserves, money growth, funding spreads, financial conditions. | Growth, z-score, stress threshold. | Multiples, volatility, leverage, USD. |
| Monetary policy | policy rate, real rate, yield curve, central-bank balance sheet. | Real-rate level, policy impulse, curve slope. | Duration, equity multiples, FX carry. |
| Fiscal policy | deficit, debt issuance, fiscal impulse, tax receipts. | Fiscal impulse, issuance pressure. | Term premia, growth, inflation, crowding out. |
| Earnings | EPS revisions, margins, sales growth. | Revision breadth, margin change. | Equity returns, credit quality. |
| Valuation | earnings yield, term premium, equity risk premium. | Percentile, spread versus rates. | Long-horizon expected return. |
| Volatility | realized vol, implied vol, vol term structure. | Level, change, VRP, skew. | Risk management, options, deleveraging. |
| Sentiment | surveys, positioning, flows, risk appetite. | Contrarian percentile, flow momentum. | Short-horizon risk appetite. |

## 2.10 Growth Features

Growth features aim to measure the level, momentum, and breadth of real activity. Common growth indicators include manufacturing PMI, services PMI, industrial production, retail sales, real income, housing activity, and GDP nowcasts.

A generic growth momentum feature can be defined as:

$$
\mathrm{GrowthMom}_{t}^{(k)}=\frac{1}{M}\sum_{m=1}^{M}\mathrm{standardize}_t\left(x_{m,t}-x_{m,t-k}\right),
$$

where $M$ is the number of growth indicators and $k$ is the lookback horizon in months. The standardization function must use only historical data.

A growth breadth feature is:

$$
\mathrm{GrowthBreadth}_t=\frac{1}{M}\sum_{m=1}^{M}\mathbf{1}\{x_{m,t}-x_{m,t-k}>0\}.
$$

**Interpretation.** A breadth value of 0.75 means 75% of the included growth indicators improved over the chosen lookback window.

**Portfolio relevance.** Growth acceleration often supports cyclical equities, credit, industrial commodities, and high-beta FX, but the implication can reverse if stronger growth raises real yields or central-bank tightening risk.

## 2.11 Inflation Features

Inflation features should separate level, momentum, breadth, and surprise. A single year-over-year CPI number can be misleading.

### 2.11.1 Inflation Level and Momentum

Let $P_t$ be a price index. Monthly inflation is:

$$
\pi_t^{1m}=\frac{P_t}{P_{t-1}}-1.
$$

Three-month annualized inflation is:

$$
\pi_t^{3m,ann}=\left(\frac{P_t}{P_{t-3}}\right)^4-1.
$$

Year-over-year inflation is:

$$
\pi_t^{12m}=\frac{P_t}{P_{t-12}}-1.
$$

Inflation acceleration can be represented as:

$$
\Delta \pi_t=\pi_t^{3m,ann}-\pi_t^{12m}.
$$

A positive value indicates that recent inflation momentum exceeds the trailing year-over-year pace.

### 2.11.2 Inflation Breadth

If $\pi_{j,t}$ is the inflation rate of component $j$, inflation breadth above a threshold $c$ is:

$$
\mathrm{InflBreadth}_t(c)=\frac{1}{J}\sum_{j=1}^{J}\mathbf{1}\{\pi_{j,t}>c\}.
$$

This measures whether inflation pressure is narrow or broad.

**Portfolio relevance.** Inflation shocks can pressure nominal duration, compress equity multiples, support inflation-linked bonds and some commodities, and raise volatility if policy reaction becomes uncertain.

## 2.12 Labor-Market Features

Labor features are important because labor tightness influences income, consumption, wage inflation, and monetary policy. Typical features include unemployment-rate changes, payroll surprises, jobless-claims momentum, wage growth, vacancies, and participation.

A labor deterioration feature can be defined as:

$$
\mathrm{LaborDeterioration}_t
= z_t(\Delta U_{t}^{3m}) + z_t(\Delta C_{t}^{3m}) - z_t(\Delta P_{t}^{3m}),
$$

where $\Delta U_{t}^{3m}$ is the three-month change in unemployment rate, $\Delta C_{t}^{3m}$ is the three-month change in jobless claims, $\Delta P_{t}^{3m}$ is payroll growth, and $z_t(\cdot)$ denotes historical-only standardization. Higher values indicate weaker labor conditions.

**Portfolio relevance.** Deteriorating labor conditions can signal slower growth and credit stress, but they may also lower policy-rate expectations, supporting duration.

## 2.13 Credit Features

Credit spreads combine risk compensation, default expectations, liquidity premia, and risk appetite. Both spread levels and spread changes matter.

A credit stress level feature is:

$$
\mathrm{CreditStressLevel}_t=z_t(s_t),
$$

where $s_t$ is the spread level.

A credit stress impulse feature is:

$$
\mathrm{CreditStressImpulse}_t=z_t(s_t-s_{t-3}).
$$

A nonlinear crisis-sensitive feature can be:

$$
\mathrm{CreditTail}_t=\mathbf{1}\{\mathrm{pctRank}_{60}(s_t)>0.90\},
$$

where the percentile rank is computed over the trailing 60 months. This indicates whether spreads are above the 90th percentile of recent history.

**Portfolio relevance.** Spread widening is often more important for short-horizon risk-off signals than spread level alone. Very high spread levels may eventually imply high forward carry, but only if default and liquidity losses are adequately compensated.

## 2.14 Liquidity and Financial Conditions Features

Liquidity features attempt to measure the ease of financing, market depth, availability of risk capital, and monetary conditions. Examples include financial conditions indices, funding spreads, central-bank reserves, money growth, repo stress, cross-currency basis, and dealer balance-sheet constraints.

A generic liquidity tightening feature is:

$$
\mathrm{LiqTight}_t
= z_t(\Delta \mathrm{FCI}_t^{3m})
+ z_t(\Delta \mathrm{FundingSpread}_t^{3m})
- z_t(\Delta \mathrm{Reserves}_t^{3m}),
$$

where higher financial conditions index values and higher funding spreads indicate tighter conditions, while rising reserves indicate easier liquidity.

**Portfolio relevance.** Liquidity tightening can be especially damaging for levered risk premia, credit, small-cap equities, carry strategies, and short-volatility strategies. Liquidity features may be more relevant for drawdown and volatility forecasts than for mean-return forecasts.

## 2.15 Monetary Policy, Real Rates, and Yield-Curve Features

### 2.15.1 Real Policy Rate

A stylized real policy-rate feature is:

$$
r_t^{\mathrm{real}}=i_t-\pi_t^{e},
$$

where $i_t$ is the nominal policy rate and $\pi_t^{e}$ is expected inflation. Expected inflation can be proxied by surveys, breakevens, inflation swaps, or model estimates, each with limitations.

### 2.15.2 Yield-Curve Slope

A common slope feature is:

$$
\mathrm{Slope}_{10y2y,t}=y_{10y,t}-y_{2y,t},
$$

where $y_{10y,t}$ and $y_{2y,t}$ are the 10-year and 2-year yields. Inversion occurs when this value is below zero.

### 2.15.3 Curve Change and Bear/Bull Steepening

Curve change is:

$$
\Delta \mathrm{Slope}_{t}^{(k)}=\mathrm{Slope}_{t}-\mathrm{Slope}_{t-k}.
$$

A steepening can be bullish or bearish depending on whether it is driven by front-end yield declines or long-end yield increases. A simple decomposition is:

$$
\Delta \mathrm{Slope}_{10y2y,t}=\Delta y_{10y,t}-\Delta y_{2y,t}.
$$

If $\Delta y_{10y,t}>0$ and $\Delta y_{2y,t}$ is stable or falling, the steepening may reflect higher term premium or inflation risk. If $\Delta y_{2y,t}<0$ and $\Delta y_{10y,t}$ is stable, the steepening may reflect expected easing.

**Portfolio relevance.** Real-rate shocks affect duration, equity style, gold, FX, and valuation-sensitive assets. Yield-curve signals often matter at $t+3$ and $t+12$ horizons rather than only at $t+1$.

## 2.16 Breakeven Inflation, Real Yields, and Inflation-Risk Pricing

Breakeven inflation is commonly approximated as:

$$
\mathrm{BEI}_{n,t}=y_{n,t}^{\mathrm{nominal}}-y_{n,t}^{\mathrm{real}},
$$

where $y_{n,t}^{\mathrm{nominal}}$ is the nominal yield for maturity $n$ and $y_{n,t}^{\mathrm{real}}$ is the inflation-linked real yield. Breakevens reflect expected inflation plus inflation-risk premia and liquidity premia.

A real-yield shock feature is:

$$
\Delta y_{n,t}^{\mathrm{real},k}=y_{n,t}^{\mathrm{real}}-y_{n,t-k}^{\mathrm{real}}.
$$

A breakeven shock feature is:

$$
\Delta \mathrm{BEI}_{n,t}^{k}=\mathrm{BEI}_{n,t}-\mathrm{BEI}_{n,t-k}.
$$

**Portfolio relevance.** Rising real yields can pressure long-duration equities and gold, while rising breakevens can support inflation-sensitive assets if not accompanied by aggressive real-rate tightening.

## 2.17 Earnings, Valuation, and Equity-Risk-Premium Features

Macro regimes affect equities through earnings, discount rates, risk premia, and positioning. Equity valuation features are usually slow-moving and more relevant for $t+12$ than $t+1$.

An earnings-yield feature is:

$$
\mathrm{EY}_t=\frac{E_t}{P_t},
$$

where $E_t$ is expected or trailing earnings and $P_t$ is the equity price index level.

A simple equity-risk-premium proxy is:

$$
\mathrm{ERP}_t=\mathrm{EY}_t-y_{10y,t}^{\mathrm{real}},
$$

or, alternatively, versus nominal yields depending on the research design. This proxy is imperfect because earnings yields are not bond yields and expected earnings are uncertain.

An earnings revision breadth feature is:

$$
\mathrm{RevBreadth}_t=\frac{\#\{\mathrm{UpwardRevisions}_t\}}{\#\{\mathrm{UpwardRevisions}_t\}+\#\{\mathrm{DownwardRevisions}_t\}}.
$$

**Portfolio relevance.** Valuation signals may forecast long-horizon expected returns but often have weak short-horizon timing power. Earnings revisions can be more responsive and may help sector and country allocation.

## 2.18 Volatility and Sentiment Features

Volatility and sentiment features often capture risk appetite, hedging demand, leverage pressure, and market fragility.

Realized volatility over $W$ months can be estimated as:

$$
\sigma_{i,t,W}=\sqrt{12}\cdot \mathrm{Std}(r_{i,t-W+1},\ldots,r_{i,t}),
$$

where $r_{i,t}$ is monthly return and $\sqrt{12}$ annualizes monthly volatility under the simplifying assumption of independent monthly returns.

A variance risk premium proxy is:

$$
\mathrm{VRP}_t=\mathrm{IV}_t^2-\mathrm{RV}_{t,W}^2,
$$

where $\mathrm{IV}_t$ is implied volatility and $\mathrm{RV}_{t,W}$ is realized volatility over a historical window. Both should be expressed in comparable annualized variance units.

A risk-appetite composite can be:

$$
\mathrm{RiskAppetite}_t
= \frac{1}{M}\sum_{m=1}^{M} s_m z_{m,t},
$$

where $s_m\in\{-1,+1\}$ orients each standardized component so that higher values represent stronger risk appetite.

**Portfolio relevance.** Volatility term structure, implied-versus-realized volatility, skew, and cross-asset correlations are critical for options, volatility strategies, drawdown risk, and deleveraging regimes.

## 2.19 Macro Surprises

A macro surprise compares an actual data release with the expectation immediately before the release:

$$
\mathrm{Surprise}_{m,t}=x_{m,t}^{\mathrm{actual}}-\mathbb{E}_{t^-}[x_{m,t}],
$$

where $\mathbb{E}_{t^-}[x_{m,t}]$ is the market or survey expectation before release. A standardized surprise is:

$$
\mathrm{StdSurprise}_{m,t}=\frac{x_{m,t}^{\mathrm{actual}}-\mathbb{E}_{t^-}[x_{m,t}]}{\hat\sigma_{m,t}^{\mathrm{surprise}}},
$$

where $\hat\sigma_{m,t}^{\mathrm{surprise}}$ is a historical standard deviation of release surprises, estimated without future data.

Macro surprises are especially relevant for event windows and short-horizon asset reactions. For monthly allocation, the cumulative surprise over a month can be defined as:

$$
\mathrm{CumSurprise}_{c,t}=\sum_{m\in c}\omega_m\mathrm{StdSurprise}_{m,t},
$$

where $c$ is a category such as inflation or growth and $\omega_m$ is a pre-specified weight.

**Key caution.** Macro-surprise data has strict timestamp requirements. A surprise cannot be used in a month-end feature if the release occurred after the decision cutoff.

## 2.20 Diffusion Indices and Breadth Indicators

Diffusion indices measure the breadth of improvement or deterioration across indicators. Suppose $x_{m,t}$ is indicator $m$ and $d_{m,t}$ is an improvement indicator:

$$
d_{m,t}=\mathbf{1}\{x_{m,t}-x_{m,t-k}>0\}.
$$

The diffusion index is:

$$
D_t=\frac{1}{M}\sum_{m=1}^{M}d_{m,t}.
$$

If lower values of some indicators are better, such as unemployment or credit spreads, orientation must be applied:

$$
d_{m,t}=\mathbf{1}\{s_m(x_{m,t}-x_{m,t-k})>0\},
$$

where $s_m=+1$ if an increase is improvement and $s_m=-1$ if a decrease is improvement.

Diffusion indices are useful because they reduce reliance on any one release. However, the indicators may be highly correlated. Treating 20 similar manufacturing indicators as independent breadth evidence can overstate confidence.

## 2.21 Cross-Asset Signal Features

Macro-regime research should incorporate market-implied information because markets often respond faster than official macro data. Cross-asset features can include momentum, carry, value, trend, volatility, correlation, skew, term structure, and risk appetite.

### 2.21.1 Momentum and Trend

A $k$-month momentum feature excluding the most recent month is:

$$
\mathrm{Mom}_{i,t}^{12-1}=\prod_{j=2}^{12}(1+r_{i,t-j+1})-1.
$$

This uses returns from $t-12$ through $t-1$ and excludes the most recent month to reduce short-term reversal effects. For monthly asset allocation, trend can also be measured by moving-average signals or time-series momentum.

A simple trend sign is:

$$
\mathrm{Trend}_{i,t}=\mathbf{1}\{P_{i,t}>\mathrm{MA}_{i,t,W}\}-\mathbf{1}\{P_{i,t}\leq \mathrm{MA}_{i,t,W}\}.
$$

### 2.21.2 Carry

Carry is the expected return from holding an asset if prices and curves do not change materially. Examples include bond yield carry, FX interest-rate differential, commodity futures roll yield, credit spread carry, and option carry.

A generic carry signal is:

$$
\mathrm{Carry}_{i,t}=\frac{\mathrm{Income}_{i,t}+\mathrm{RollDown}_{i,t}+\mathrm{Collateral}_{i,t}-\mathrm{Financing}_{i,t}}{\mathrm{Capital}_{i,t}}.
$$

The components depend on asset class. Carry is not free yield. It is often compensation for crash risk, liquidity risk, inflation risk, or negative convexity.

### 2.21.3 Value

A cross-sectional value feature can be expressed as:

$$
\mathrm{Value}_{i,t}=z_t\left(\frac{\mathrm{Fundamental}_{i,t}}{\mathrm{Price}_{i,t}}\right),
$$

where the fundamental variable may be earnings, book value, yield, purchasing-power parity value, or commodity inventory-adjusted fair value. Value features are usually more useful at medium-to-long horizons than at one month.

### 2.21.4 Volatility, Correlation, and Risk Appetite

A cross-asset correlation feature can measure whether diversification is deteriorating:

$$
\bar\rho_t=\frac{2}{N(N-1)}\sum_{i<j}\rho_{ij,t,W},
$$

where $\rho_{ij,t,W}$ is the trailing correlation between assets $i$ and $j$ over window $W$. Rising average correlation often indicates risk-off or deleveraging conditions.

A volatility shock feature is:

$$
\mathrm{VolShock}_{i,t}=\frac{\sigma_{i,t,W_s}-\sigma_{i,t,W_l}}{\sigma_{i,t,W_l}},
$$

where $W_s$ is a short window and $W_l$ is a long window.

## 2.22 Feature Lagging Rules to Avoid Look-Ahead Bias

Every feature should have an explicit availability rule. A generic rule is:

$$
z_{m,t}^{\mathrm{valid}}=z_{m,\ell(t,m)},
$$

where $\ell(t,m)$ is the latest observation of variable $m$ available at decision timestamp $t$.

Practical lagging rules:

| Data Type | Recommended Rule | Common Error |
|---|---|---|
| Official macro data | Join by release timestamp or lag conservatively. | Joining by reference month. |
| Survey data | Use release date and cutoff time. | Assuming survey month equals availability month. |
| Daily market data | Use month-end close only if execution convention permits. | Trading at the same close used to create the signal. |
| Fundamentals | Use filing/report date, not fiscal period end. | Using restated or future-known fundamentals. |
| Options surfaces | Use timestamped surface snapshots. | Using interpolated surfaces built later. |
| Futures curves | Use contract prices available at signal time. | Using final continuous futures series with future roll knowledge. |
| Cross-sectional ranks | Rank only within point-in-time universe. | Ranking assets that did not yet exist. |
| Scaling statistics | Use rolling/expanding historical statistics. | Full-sample z-scores. |

## 2.23 Historical-Only Standardization

Full-sample standardization is one of the most common leakage errors. The invalid full-sample z-score is:

$$
z_t^{\mathrm{invalid}}=\frac{x_t-\bar x_{1:T}}{s_{1:T}},
$$

where $\bar x_{1:T}$ and $s_{1:T}$ use observations after $t$. A valid expanding z-score is:

$$
z_t^{\mathrm{valid}}=\frac{x_t-\bar x_{1:t-1}}{s_{1:t-1}}.
$$

A valid rolling z-score is:

$$
z_t^{\mathrm{valid,roll}}=\frac{x_t-\bar x_{t-W:t-1}}{s_{t-W:t-1}}.
$$

Winsorization must also be historical. A valid rolling winsorization rule is:

$$
x_t^{\mathrm{win}}=
\min\left(\max(x_t,Q_{\alpha,t,W}),Q_{1-\alpha,t,W}\right),
$$

where $Q_{\alpha,t,W}$ and $Q_{1-\alpha,t,W}$ are historical quantiles computed from $x_{t-W},\ldots,x_{t-1}$.

## 2.24 Economic Signal Design Principles

A candidate macro signal should satisfy five conditions before being included in a research library.

| Condition | Required Question | Example |
|---|---|---|
| Economic rationale | Why should this variable forecast returns? | Credit spreads proxy funding stress and default risk. |
| Horizon specificity | At which horizon should it work? | Valuation may matter at $t+12$, not $t+1$. |
| Directional hypothesis | What sign is expected? | Rising real yields may pressure long-duration equities. |
| Implementation feasibility | Can exposure be implemented net of costs? | Futures carry must include roll and collateral assumptions. |
| Failure modes | When should it fail? | Carry can crash during liquidity stress. |

A signal specification should be written before testing. This reduces narrative overfitting after seeing results.

## 2.25 From Features to Composite Macro State Scores

Composite macro scores combine multiple oriented features. Let $z_{m,t}$ be standardized feature $m$, and let $s_m\in\{-1,+1\}$ orient the feature so that higher values indicate more of a concept such as growth strength, inflation pressure, or credit stress. A composite score is:

$$
C_{c,t}=\sum_{m\in c}w_m s_m z_{m,t},
$$

where $c$ is a category, $w_m$ are pre-specified or estimated weights, and $\sum_{m\in c}|w_m|=1$. Equal weights are often more robust than optimized weights in small monthly samples.

A bounded score can be generated using:

$$
\tilde C_{c,t}=\tanh(C_{c,t}/a),
$$

where $a>0$ controls compression. Bounded scores are useful for preventing extreme feature values from creating unstable convictions.

## 2.26 Feature Interactions and Macro Mixes

Some asset outcomes depend on macro combinations rather than single variables. A growth-inflation mix can be represented with two standardized composites:

$$
G_t=\mathrm{GrowthScore}_t,
\qquad
I_t=\mathrm{InflationScore}_t.
$$

A simple four-quadrant macro map is:

| Growth Score | Inflation Score | Stylized Macro Mix | Potential Research Focus |
|---:|---:|---|---|
| $G_t>0$ | $I_t<0$ | Disinflationary expansion | Equities, credit, duration balance. |
| $G_t>0$ | $I_t>0$ | Reflation or overheating | Commodities, cyclicals, real-rate risk. |
| $G_t<0$ | $I_t<0$ | Deflationary slowdown | Duration, defensive assets, credit risk. |
| $G_t<0$ | $I_t>0$ | Stagflation pressure | Inflation hedges, equity multiple risk. |

A continuous interaction feature is:

$$
\mathrm{StagflationPressure}_t=I_t-G_t.
$$

Higher values indicate inflation pressure exceeding growth strength. This may be more stable than a hard regime label.

## 2.27 Feature Orthogonalization and Redundancy Control

Macro features are often redundant. For example, PMI, industrial production, earnings revisions, and credit spreads may all reflect growth conditions. A simple orthogonalization of feature $x_t$ against feature matrix $Z_t$ is:

$$
x_t = Z_t\gamma + u_t,
$$

where $u_t$ is the residual. The orthogonalized feature is:

$$
x_t^{\perp}=u_t=x_t-Z_t\hat\gamma.
$$

The regression used to estimate $\hat\gamma$ must be fit only on historical data in a walk-forward setting. Orthogonalization can help identify incremental information but can also reduce interpretability. It should not be used automatically.

A redundancy diagnostic is the feature correlation matrix:

$$
\rho_{mn}=\frac{\mathrm{Cov}(z_m,z_n)}{\sigma_m\sigma_n}.
$$

Highly correlated features should be grouped, averaged, regularized, or subjected to dimensionality reduction.

## 2.28 Python: Robust Monthly Macro Feature Engineering

The following code is a reproducible feature-engineering toolkit using synthetic-friendly, model-ready functions. It emphasizes lagging, historical-only scaling, stationarity-aware transformations, and input validation.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss


TransformName = Literal[
    "level", "diff", "pct_change", "log_change", "yoy", "yoy_log"
]


@dataclass(frozen=True)
class FeatureSpec:
    """Specification for a single macro feature.

    Parameters
    ----------
    source : str
        Column name in the raw macro DataFrame.
    transform : TransformName
        Transformation type.
    lookback : int
        Lookback horizon in months for differencing or percent changes.
    release_lag : int
        Conservative release lag in months. Use vintage timestamps when available.
    standardize : str
        One of {"none", "rolling", "expanding", "robust_rolling"}.
    standardize_window : int
        Rolling window for standardization when applicable.
    min_periods : int
        Minimum historical observations required for scaling.
    winsorize : bool
        Whether to apply historical rolling winsorization before standardization.
    winsor_alpha : float
        Tail probability for winsorization, such as 0.01 or 0.025.
    orientation : int
        +1 if higher feature values mean more of the concept, -1 otherwise.
    """

    source: str
    transform: TransformName = "level"
    lookback: int = 1
    release_lag: int = 1
    standardize: Literal["none", "rolling", "expanding", "robust_rolling"] = "rolling"
    standardize_window: int = 60
    min_periods: int = 36
    winsorize: bool = False
    winsor_alpha: float = 0.01
    orientation: int = 1


def validate_monthly_frame(df: pd.DataFrame, name: str = "df") -> None:
    """Validate basic structure for monthly time-series data."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"{name} must be a pandas DataFrame.")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError(f"{name} must have a DatetimeIndex.")
    if not df.index.is_monotonic_increasing:
        raise ValueError(f"{name} index must be sorted in increasing order.")
    if df.index.has_duplicates:
        raise ValueError(f"{name} index contains duplicate timestamps.")
    if df.empty:
        raise ValueError(f"{name} cannot be empty.")


def apply_transform(x: pd.Series, transform: TransformName, lookback: int) -> pd.Series:
    """Apply a macro transformation to one series."""
    if lookback < 1:
        raise ValueError("lookback must be a positive integer.")
    x = x.astype(float)

    if transform == "level":
        return x.copy()
    if transform == "diff":
        return x - x.shift(lookback)
    if transform == "pct_change":
        return x.pct_change(lookback, fill_method=None)
    if transform == "log_change":
        safe = x.where(x > 0)
        return np.log(safe) - np.log(safe.shift(lookback))
    if transform == "yoy":
        return x.pct_change(12, fill_method=None)
    if transform == "yoy_log":
        safe = x.where(x > 0)
        return np.log(safe) - np.log(safe.shift(12))
    raise ValueError(f"Unknown transform: {transform}")


def rolling_winsorize_historical(
    x: pd.Series,
    window: int,
    alpha: float = 0.01,
    min_periods: int = 36,
) -> pd.Series:
    """Winsorize using trailing historical quantiles excluding current value."""
    if not 0 < alpha < 0.5:
        raise ValueError("alpha must lie between 0 and 0.5.")
    hist = x.shift(1)
    lo = hist.rolling(window, min_periods=min_periods).quantile(alpha)
    hi = hist.rolling(window, min_periods=min_periods).quantile(1 - alpha)
    return x.clip(lower=lo, upper=hi)


def historical_zscore(
    x: pd.Series,
    method: str = "rolling",
    window: int = 60,
    min_periods: int = 36,
) -> pd.Series:
    """Compute leak-safe z-scores using only historical values."""
    x = x.astype(float)
    hist = x.shift(1)

    if method == "none":
        return x
    if method == "rolling":
        mu = hist.rolling(window, min_periods=min_periods).mean()
        sd = hist.rolling(window, min_periods=min_periods).std(ddof=1)
        return (x - mu) / sd.replace(0.0, np.nan)
    if method == "expanding":
        mu = hist.expanding(min_periods=min_periods).mean()
        sd = hist.expanding(min_periods=min_periods).std(ddof=1)
        return (x - mu) / sd.replace(0.0, np.nan)
    if method == "robust_rolling":
        median = hist.rolling(window, min_periods=min_periods).median()
        mad = (hist - median).abs().rolling(window, min_periods=min_periods).median()
        return (x - median) / (1.4826 * mad.replace(0.0, np.nan))

    raise ValueError(f"Unknown standardization method: {method}")


def build_feature(raw: pd.DataFrame, spec: FeatureSpec) -> pd.Series:
    """Build one point-in-time macro feature from a FeatureSpec."""
    validate_monthly_frame(raw, "raw")
    if spec.source not in raw.columns:
        raise KeyError(f"Missing source column: {spec.source}")
    if spec.release_lag < 0:
        raise ValueError("release_lag cannot be negative.")
    if spec.orientation not in (-1, 1):
        raise ValueError("orientation must be +1 or -1.")

    # Conservative lag approximates availability. True production systems should
    # join by release and vintage timestamps instead of using a fixed lag.
    x = raw[spec.source].shift(spec.release_lag)
    y = apply_transform(x, spec.transform, spec.lookback)

    if spec.winsorize:
        y = rolling_winsorize_historical(
            y,
            window=spec.standardize_window,
            alpha=spec.winsor_alpha,
            min_periods=spec.min_periods,
        )

    z = historical_zscore(
        y,
        method=spec.standardize,
        window=spec.standardize_window,
        min_periods=spec.min_periods,
    )
    return spec.orientation * z


def build_feature_matrix(raw: pd.DataFrame, specs: dict[str, FeatureSpec]) -> pd.DataFrame:
    """Build a feature matrix from named feature specifications."""
    features = {}
    for name, spec in specs.items():
        features[name] = build_feature(raw, spec)
    return pd.DataFrame(features, index=raw.index).replace([np.inf, -np.inf], np.nan)


def stationarity_report(x: pd.Series, min_obs: int = 48) -> dict[str, float | str]:
    """Run basic stationarity diagnostics using ADF and KPSS tests.

    The tests are only diagnostics. They should not mechanically determine the
    final feature set, especially in short monthly samples.
    """
    clean = x.dropna().astype(float)
    if len(clean) < min_obs:
        return {"status": "insufficient_observations", "nobs": len(clean)}

    out: dict[str, float | str] = {"status": "ok", "nobs": len(clean)}
    try:
        adf_stat, adf_p, *_ = adfuller(clean, autolag="AIC")
        out["adf_stat"] = float(adf_stat)
        out["adf_pvalue"] = float(adf_p)
    except Exception as exc:
        out["adf_error"] = str(exc)

    try:
        kpss_stat, kpss_p, *_ = kpss(clean, regression="c", nlags="auto")
        out["kpss_stat"] = float(kpss_stat)
        out["kpss_pvalue"] = float(kpss_p)
    except Exception as exc:
        out["kpss_error"] = str(exc)

    return out
```

## 2.29 Python: Example Feature Library for Monthly Macro Data

```python
# Synthetic example. Replace the DataFrame with point-in-time macro data in production.
rng = np.random.default_rng(7)
dates = pd.date_range("2000-01-31", periods=240, freq="M")
raw_macro = pd.DataFrame(
    {
        "pmi": 50 + rng.normal(0, 1.5, len(dates)).cumsum() / 8,
        "cpi_index": 100 * np.exp(np.cumsum(rng.normal(0.002, 0.002, len(dates)))),
        "unemployment_rate": 5 + rng.normal(0, 0.08, len(dates)).cumsum(),
        "hy_spread": 4 + rng.normal(0, 0.18, len(dates)).cumsum(),
        "ten_year_yield": 3 + rng.normal(0, 0.10, len(dates)).cumsum(),
        "two_year_yield": 2.5 + rng.normal(0, 0.12, len(dates)).cumsum(),
        "financial_conditions": rng.normal(0, 0.15, len(dates)).cumsum(),
    },
    index=dates,
)

# Derived raw features can be created first, then lagged and standardized.
raw_macro["curve_10y2y"] = raw_macro["ten_year_yield"] - raw_macro["two_year_yield"]

specs = {
    "growth_pmi_level_z": FeatureSpec(
        source="pmi", transform="level", release_lag=1,
        standardize="rolling", standardize_window=60, orientation=1,
    ),
    "growth_pmi_3m_change_z": FeatureSpec(
        source="pmi", transform="diff", lookback=3, release_lag=1,
        standardize="rolling", standardize_window=60, orientation=1,
    ),
    "inflation_yoy_z": FeatureSpec(
        source="cpi_index", transform="yoy", release_lag=1,
        standardize="rolling", standardize_window=84, orientation=1,
    ),
    "labor_deterioration_z": FeatureSpec(
        source="unemployment_rate", transform="diff", lookback=3, release_lag=1,
        standardize="rolling", standardize_window=60, orientation=1,
    ),
    "credit_stress_level_z": FeatureSpec(
        source="hy_spread", transform="level", release_lag=0,
        standardize="robust_rolling", standardize_window=60, orientation=1,
        winsorize=True, winsor_alpha=0.025,
    ),
    "credit_stress_impulse_z": FeatureSpec(
        source="hy_spread", transform="diff", lookback=3, release_lag=0,
        standardize="robust_rolling", standardize_window=60, orientation=1,
    ),
    "curve_slope_z": FeatureSpec(
        source="curve_10y2y", transform="level", release_lag=0,
        standardize="rolling", standardize_window=120, orientation=1,
    ),
    "fci_tightening_z": FeatureSpec(
        source="financial_conditions", transform="diff", lookback=3, release_lag=0,
        standardize="rolling", standardize_window=60, orientation=1,
    ),
}

features = build_feature_matrix(raw_macro, specs)
print(features.tail())

# Stationarity diagnostics for raw and transformed series.
for col in ["pmi", "cpi_index", "hy_spread", "curve_10y2y"]:
    print(col, stationarity_report(raw_macro[col]))
```

## 2.30 Python: Composite Growth, Inflation, Credit, and Liquidity Scores

```python
def composite_score(
    features: pd.DataFrame,
    columns: Iterable[str],
    weights: dict[str, float] | None = None,
    squash: bool = True,
    squash_scale: float = 2.0,
) -> pd.Series:
    """Create a composite score from standardized, oriented features.

    Parameters
    ----------
    features : pd.DataFrame
        Feature matrix with standardized and directionally oriented columns.
    columns : iterable[str]
        Columns to combine.
    weights : dict[str, float] or None
        Optional weights. If None, equal absolute weights are used.
    squash : bool
        If True, apply tanh compression to reduce outlier impact.
    squash_scale : float
        Positive scale for tanh compression.
    """
    cols = list(columns)
    if not cols:
        raise ValueError("columns cannot be empty.")
    missing = set(cols) - set(features.columns)
    if missing:
        raise KeyError(f"Missing feature columns: {sorted(missing)}")
    if squash_scale <= 0:
        raise ValueError("squash_scale must be positive.")

    X = features[cols].astype(float)
    if weights is None:
        w = pd.Series(1.0 / len(cols), index=cols)
    else:
        w = pd.Series(weights, dtype=float).reindex(cols)
        if w.isna().any():
            raise ValueError("weights must be supplied for every selected column.")
        denom = w.abs().sum()
        if denom == 0:
            raise ValueError("At least one weight must be nonzero.")
        w = w / denom

    score = X.mul(w, axis=1).sum(axis=1, min_count=1)
    if squash:
        score = np.tanh(score / squash_scale)
    return score

macro_scores = pd.DataFrame(index=features.index)
macro_scores["growth_score"] = composite_score(
    features,
    ["growth_pmi_level_z", "growth_pmi_3m_change_z"],
)
macro_scores["inflation_score"] = features["inflation_yoy_z"].pipe(lambda s: np.tanh(s / 2.0))
macro_scores["credit_stress_score"] = composite_score(
    features,
    ["credit_stress_level_z", "credit_stress_impulse_z"],
)
macro_scores["liquidity_tightening_score"] = features["fci_tightening_z"].pipe(lambda s: np.tanh(s / 2.0))
macro_scores["stagflation_pressure"] = macro_scores["inflation_score"] - macro_scores["growth_score"]

print(macro_scores.dropna().tail())
```

## 2.31 Python: Rolling Percentile Ranks and Diffusion Indices

```python
def rolling_percentile_rank(
    x: pd.Series,
    window: int = 60,
    min_periods: int = 36,
) -> pd.Series:
    """Compute leak-safe rolling percentile rank of current value versus history."""
    if window < 2:
        raise ValueError("window must be at least 2.")

    def pct_rank(arr: np.ndarray) -> float:
        # Last value is current x_t; previous values are historical values.
        current = arr[-1]
        hist = arr[:-1]
        if np.isnan(current) or np.isnan(hist).all():
            return np.nan
        hist = hist[~np.isnan(hist)]
        if len(hist) == 0:
            return np.nan
        return float(np.mean(hist <= current))

    # Include current value in the rolling object, but compare it only against
    # the prior observations inside the function.
    return x.rolling(window + 1, min_periods=min_periods + 1).apply(pct_rank, raw=True)


def diffusion_index(
    data: pd.DataFrame,
    columns: Iterable[str],
    lookback: int = 3,
    orientation: dict[str, int] | None = None,
) -> pd.Series:
    """Compute a diffusion index of improving indicators.

    orientation[col] should be +1 when an increase is improvement and -1 when
    a decrease is improvement.
    """
    cols = list(columns)
    if not cols:
        raise ValueError("columns cannot be empty.")
    missing = set(cols) - set(data.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")
    if lookback < 1:
        raise ValueError("lookback must be positive.")

    orient = pd.Series(1, index=cols)
    if orientation is not None:
        orient.update(pd.Series(orientation))
    if not orient.isin([-1, 1]).all():
        raise ValueError("All orientation values must be +1 or -1.")

    changes = data[cols].diff(lookback).mul(orient, axis=1)
    improving = changes > 0
    return improving.sum(axis=1) / changes.notna().sum(axis=1).replace(0, np.nan)

raw_macro["hy_spread_pct_rank"] = rolling_percentile_rank(raw_macro["hy_spread"], window=60)
raw_macro["growth_diffusion"] = diffusion_index(
    raw_macro,
    columns=["pmi", "unemployment_rate", "financial_conditions"],
    lookback=3,
    orientation={"pmi": 1, "unemployment_rate": -1, "financial_conditions": -1},
)

print(raw_macro[["hy_spread_pct_rank", "growth_diffusion"]].tail())
```

## 2.32 Python: Cross-Asset Market-Implied Features

```python
def trailing_momentum(
    returns: pd.DataFrame,
    lookback: int = 12,
    skip_recent: int = 1,
) -> pd.DataFrame:
    """Compute compounded trailing momentum using only past returns.

    The value at t uses returns ending at t-skip_recent. For 12-1 momentum,
    use lookback=11 and skip_recent=1, or use a 12-month window excluding the
    most recent month depending on the research convention.
    """
    if lookback < 1 or skip_recent < 0:
        raise ValueError("lookback must be positive and skip_recent non-negative.")
    shifted = returns.shift(skip_recent)
    gross = (1.0 + shifted).rolling(lookback, min_periods=lookback).apply(np.prod, raw=True)
    return gross - 1.0


def realized_volatility(
    returns: pd.DataFrame,
    window: int = 12,
    annualization: int = 12,
) -> pd.DataFrame:
    """Compute trailing annualized realized volatility."""
    if window < 2:
        raise ValueError("window must be at least 2.")
    return returns.rolling(window, min_periods=window).std(ddof=1) * np.sqrt(annualization)


def average_pairwise_correlation(
    returns: pd.DataFrame,
    window: int = 12,
    min_assets: int = 3,
) -> pd.Series:
    """Compute rolling average pairwise correlation across assets."""
    if returns.shape[1] < min_assets:
        raise ValueError("Not enough assets for a cross-asset correlation measure.")

    values = []
    idx = []
    for end in range(window, len(returns) + 1):
        block = returns.iloc[end - window:end]
        corr = block.corr()
        mask = np.triu(np.ones(corr.shape, dtype=bool), k=1)
        vals = corr.where(mask).stack().dropna()
        values.append(vals.mean() if len(vals) else np.nan)
        idx.append(returns.index[end - 1])
    return pd.Series(values, index=idx, name="avg_pairwise_corr")

# Synthetic asset returns for demonstration.
asset_returns = pd.DataFrame(
    rng.normal(0.004, 0.04, size=(len(dates), 4)),
    index=dates,
    columns=["Equity", "Duration", "Credit", "Commodity"],
)

market_features = pd.concat(
    {
        "mom_12_1": trailing_momentum(asset_returns, lookback=11, skip_recent=1).stack(),
        "vol_12m": realized_volatility(asset_returns, window=12).stack(),
    },
    axis=1,
)
market_features.index.names = ["date", "asset"]

avg_corr = average_pairwise_correlation(asset_returns, window=12)
print(market_features.dropna().head())
print(avg_corr.dropna().tail())
```

## 2.33 Visualization Code for Macro Feature Diagnostics

The following plot functions can be used to inspect feature histories, composites, percentile ranks, and macro-state scores. They use `matplotlib` and avoid custom styling.

```python
import matplotlib.pyplot as plt


def plot_feature_history(features: pd.DataFrame, column: str, title: str | None = None) -> None:
    """Plot one feature history with a zero line."""
    if column not in features.columns:
        raise KeyError(f"Column not found: {column}")
    fig, ax = plt.subplots(figsize=(10, 4))
    features[column].plot(ax=ax)
    ax.axhline(0.0, linewidth=1)
    ax.set_title(title or column)
    ax.set_xlabel("Date")
    ax.set_ylabel("Feature value")
    plt.tight_layout()
    plt.show()


def plot_composite_scores(scores: pd.DataFrame, columns: list[str]) -> None:
    """Plot selected composite macro scores."""
    missing = set(columns) - set(scores.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")
    fig, ax = plt.subplots(figsize=(10, 5))
    scores[columns].plot(ax=ax)
    ax.axhline(0.0, linewidth=1)
    ax.set_title("Composite Macro Scores")
    ax.set_xlabel("Date")
    ax.set_ylabel("Score")
    plt.tight_layout()
    plt.show()


def plot_macro_quadrants(scores: pd.DataFrame) -> None:
    """Scatter plot of growth versus inflation scores."""
    needed = {"growth_score", "inflation_score"}
    missing = needed - set(scores.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")
    clean = scores.dropna(subset=["growth_score", "inflation_score"])
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(clean["growth_score"], clean["inflation_score"], s=12)
    ax.axhline(0.0, linewidth=1)
    ax.axvline(0.0, linewidth=1)
    ax.set_xlabel("Growth score")
    ax.set_ylabel("Inflation score")
    ax.set_title("Growth-Inflation Macro Map")
    plt.tight_layout()
    plt.show()


plot_feature_history(features, "credit_stress_impulse_z")
plot_composite_scores(macro_scores, ["growth_score", "inflation_score", "credit_stress_score"])
plot_macro_quadrants(macro_scores)
```

## 2.34 Practical Signal Examples by Horizon

| Signal Concept | Feature | Expected Useful Horizon | Typical Target | Failure Mode |
|---|---|---:|---|---|
| Growth acceleration | PMI 3m change, growth diffusion. | $t+1$ to $t+3$ | Cyclical equity and credit returns. | Tightening response offsets growth. |
| Inflation acceleration | 3m annualized CPI minus YoY CPI. | $t+1$ to $t+3$ | Duration, commodities, equity styles. | Supply shock reverses quickly. |
| Real-rate shock | 3m change in real yield. | $t+1$ to $t+3$ | Duration-sensitive equities, gold, FX. | Growth optimism absorbs rate shock. |
| Curve inversion | 10y-2y slope below zero. | $t+6$ to $t+12$ | Recession risk, duration, defensives. | Long and variable lags. |
| Credit widening | HY spread 3m change. | $t+1$ to $t+3$ | Equity drawdown, credit underperformance. | Spread widening already priced. |
| Valuation extreme | Earnings yield percentile. | $t+12+$ | Equity expected return. | Timing power weak at short horizons. |
| Volatility term stress | VIX curve inversion, high IV percentile. | $t+1$ | Equity drawdown and vol strategies. | Vol spike may be mean-reverting. |
| Commodity carry | Futures backwardation/contango. | $t+1$ to $t+12$ | Commodity futures returns. | Curve shape reflects inventory stress or crash risk. |

## 2.35 Feature Documentation Template

Every feature in an institutional library should have a written specification.

| Field | Required Content |
|---|---|
| Feature name | Stable name, such as `inflation_cpi_3m_ann_z`. |
| Raw source | Vendor, series ID, field, unit, currency, country. |
| Economic meaning | What the feature is intended to measure. |
| Transformation | Formula, lookback, scaling, winsorization. |
| Availability rule | Release lag, vintage rule, vendor ingestion rule. |
| Orientation | Whether higher means more growth, more stress, more inflation, etc. |
| Expected sign | Expected relationship with target assets. |
| Expected horizon | $t+1$, $t+3$, $t+12$, or other. |
| Target universe | Asset classes or instruments where it is relevant. |
| Validation status | In-sample, out-of-sample, stability, robustness. |
| Failure modes | Macro conditions where signal may fail. |
| Owner and version | Research owner, approval status, change history. |

## 2.36 Common Feature Engineering Mistakes

1. **Using final revised macro data as real-time data.** This can create materially overstated predictability.
2. **Standardizing with the full sample.** Full-sample means and standard deviations use future information.
3. **Confusing reference month with availability month.** A CPI value for May is not necessarily available for a May-end decision.
4. **Using raw levels for nonstationary index series.** CPI index level or nominal GDP level usually needs transformation.
5. **Over-optimizing lookbacks.** Testing many windows without correction creates data-mining bias.
6. **Ignoring sign orientation.** Composite scores become meaningless when components have inconsistent directions.
7. **Double counting correlated indicators.** Many macro variables measure the same underlying cycle.
8. **Treating threshold labels as truth.** A hard threshold can create false precision near the boundary.
9. **Ignoring asset-specific channels.** A growth signal may affect equities, bonds, credit, FX, and commodities differently.
10. **Failing to document implementation assumptions.** Without feature specifications, research cannot be reproduced or governed.

## 2.37 Part 2 Summary

Part 2 developed the macro feature-engineering layer needed for regime detection and multi-asset signal research. The central principles are:

1. Features must be point-in-time, availability-aware, and historically standardized.
2. Transformation choice should reflect both statistical properties and economic meaning.
3. Levels, changes, percent changes, log changes, z-scores, percentile ranks, surprises, thresholds, and diffusion indices each answer different questions.
4. Stationarity tests are useful diagnostics but should not mechanically dictate transformations in short monthly samples.
5. Macro categories should include growth, inflation, labor, credit, liquidity, monetary policy, fiscal policy, earnings, valuation, volatility, and sentiment.
6. Market-implied features such as momentum, carry, volatility, correlation, skew, and term structure complement official macro data.
7. Feature lagging, vintage data, and historical-only scaling are essential defenses against look-ahead bias.
8. Composite macro scores should use oriented, documented, and preferably parsimonious inputs.
9. Signal design should start with economic rationale, expected sign, relevant horizon, implementation feasibility, and failure modes before statistical testing.
10. Production-quality feature libraries require formal documentation, versioning, validation status, and governance.

---

# Stop Point

This installment completes:

1. **Part 2: Macro Feature Engineering and Economic Signal Design.**

Continue next with **Part 3: Multi-Asset Return Modeling Across Horizons**.
