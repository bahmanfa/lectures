# Institutional Options Greeks, Systematic Strategy, and Regime-Aware Portfolio Construction Curriculum

## Completed Installment

This installment contains:

- Part 12: Summary, Formula Reference, Governance Checklist, and Implementation Manual.

The document is educational and research-oriented. It is not personalized investment advice, a live trading recommendation, or a claim that any option strategy produces guaranteed alpha.

---

# Part 12: Summary, Formula Reference, Governance Checklist, and Implementation Manual

**Level:** Expert / Reference Manual

## 12.1 Purpose of Part 12

Part 12 consolidates the full curriculum into a practical reference manual. The previous parts developed the theory and implementation of option Greeks, higher-order sensitivities, hedging, volatility surfaces, systematic alpha, regime-aware allocation, portfolio construction, covariance stabilization, risk management, backtesting, and case studies. This final part provides a compact institutional operating framework.

The purpose is to answer three questions:

1. **What should an institutional options researcher remember?**
2. **What formulas, definitions, and diagnostics should be available at all times?**
3. **What production controls are required before a Greek-aware options strategy should be trusted?**

The central principle is:

$$
\text{Institutional options research requires consistent definitions, point-in-time data, cost-aware implementation, regime-aware risk, and continuous validation.}
$$

A strong options process should be able to connect every position to:

- payoff logic;
- pricing assumptions;
- Greek exposures;
- volatility-surface exposures;
- expected return hypothesis;
- regime suitability;
- portfolio constraints;
- stress losses;
- transaction costs;
- margin usage;
- data lineage;
- post-trade P&L attribution.

If a strategy cannot explain these items, it is not yet production-ready.

---

## 12.2 Full Curriculum Map

| Part | Topic | Main Institutional Skill |
|---|---|---|
| Part 0 | Executive overview and learning roadmap | Understand why Greeks matter beyond formulas |
| Part 1 | Option pricing and core Greeks | Price European options and interpret delta, gamma, theta, vega, rho |
| Part 2 | Higher-order Greeks and dynamic Greek surfaces | Understand vanna, volga, charm, color, speed, zomma, veta, vera, and surface-aware risk |
| Part 3 | Practical hedging dynamics | Decompose hedged P&L and understand gamma scalping, discrete hedging, and costs |
| Part 4 | Volatility surface, skew, and term structure | Treat implied volatility as a surface and regime variable |
| Part 5 | Systematic alpha generation using Greeks | Convert Greek exposures into research hypotheses and strategy families |
| Part 6 | Regime-aware strategy selection | Map volatility and macro regimes to strategy suitability and Greek budgets |
| Part 7 | Greek-aware portfolio construction | Aggregate and optimize nonlinear exposures across instruments and sleeves |
| Part 8 | Covariance estimation and risk stabilization | Stabilize covariance estimates using shrinkage, factor models, and RMT concepts |
| Part 9 | Risk management and stress testing | Control nonlinear losses, margin, liquidity, jumps, and approximation error |
| Part 10 | Institutional research pipeline and backtesting | Build point-in-time, cost-aware, validated options backtests |
| Part 11 | Applied case studies | Diagnose realistic strategies using Greeks, regimes, stress tests, and attribution |
| Part 12 | Reference manual and governance checklist | Consolidate formulas, workflows, controls, and production standards |

---

## 12.3 Core Notation Reference

| Symbol | Meaning |
|---|---|
| $S_t$ | Underlying spot price at time $t$ |
| $K$ | Strike price |
| $T$ | Maturity date |
| $\tau=T-t$ | Time to maturity in years |
| $r$ | Continuously compounded risk-free rate |
| $q$ | Continuous dividend yield |
| $\sigma$ | Volatility, usually annualized decimal volatility |
| $\sigma_{imp}$ | Implied volatility |
| $\sigma_{real}$ | Realized volatility |
| $F_{t,T}$ | Forward price for maturity $T$ |
| $V$ | Option value |
| $C$ | Call option value |
| $P$ | Put option value |
| $N(x)$ | Standard normal cumulative distribution function |
| $\phi(x)$ | Standard normal probability density function |
| $M$ | Contract multiplier |
| $Q$ | Number of contracts |
| $w_i$ | Signed portfolio weight or position size |

The continuous-yield forward price is:

$$
F_{t,T}=S_t e^{(r-q)\tau}.
$$

Forward log-moneyness is:

$$
k_F=\ln\left(\frac{K}{F_{t,T}}\right).
$$

Spot moneyness is:

$$
M_S=\frac{S_t}{K}.
$$

---

## 12.4 Payoff Reference

European call payoff:

$$
C_T=(S_T-K)^+=\max(S_T-K,0).
$$

European put payoff:

$$
P_T=(K-S_T)^+=\max(K-S_T,0).
$$

Call intrinsic value:

$$
\text{Intrinsic}_{call}=\max(S_t-K,0).
$$

Put intrinsic value:

$$
\text{Intrinsic}_{put}=\max(K-S_t,0).
$$

Time value:

$$
\text{Time Value}=V_t-\text{Intrinsic Value}.
$$

---

## 12.5 Black-Scholes-Merton Pricing Reference

Under the European, continuous-dividend, constant-rate, constant-volatility assumptions:

$$
d_1=\frac{\ln(S/K)+(r-q+\frac{1}{2}\sigma^2)\tau}{\sigma\sqrt{\tau}},
$$

$$
d_2=d_1-\sigma\sqrt{\tau}.
$$

European call:

$$
C=S e^{-q\tau}N(d_1)-K e^{-r\tau}N(d_2).
$$

European put:

$$
P=K e^{-r\tau}N(-d_2)-S e^{-q\tau}N(-d_1).
$$

Put-call parity:

$$
C-P=S e^{-q\tau}-K e^{-r\tau}.
$$

Black-Scholes-Merton PDE:

$$
\frac{\partial V}{\partial t}+(r-q)S\frac{\partial V}{\partial S}+\frac{1}{2}\sigma^2S^2\frac{\partial^2V}{\partial S^2}-rV=0.
$$

In Greek notation:

$$
\Theta+(r-q)S\Delta+\frac{1}{2}\sigma^2S^2\Gamma-rV=0.
$$

---

## 12.6 Core Greek Reference

| Greek | Definition | Interpretation |
|---|---:|---|
| Delta | $\Delta=\partial V/\partial S$ | First-order spot exposure |
| Gamma | $\Gamma=\partial^2V/\partial S^2$ | Spot convexity; delta instability |
| Theta | $\Theta=\partial V/\partial t$ | Time-passing sensitivity |
| Vega | $\nu=\partial V/\partial\sigma$ | Implied-volatility sensitivity |
| Rho | $\rho=\partial V/\partial r$ | Interest-rate sensitivity |
| Dividend rho | $\psi=\partial V/\partial q$ | Dividend-yield sensitivity |

Call delta:

$$
\Delta_C=e^{-q\tau}N(d_1).
$$

Put delta:

$$
\Delta_P=e^{-q\tau}[N(d_1)-1].
$$

Call and put gamma:

$$
\Gamma=\frac{e^{-q\tau}\phi(d_1)}{S\sigma\sqrt{\tau}}.
$$

Call and put vega:

$$
\nu=S e^{-q\tau}\phi(d_1)\sqrt{\tau}.
$$

Call theta:

$$
\Theta_C=-\frac{S e^{-q\tau}\phi(d_1)\sigma}{2\sqrt{\tau}}-rK e^{-r\tau}N(d_2)+qS e^{-q\tau}N(d_1).
$$

Put theta:

$$
\Theta_P=-\frac{S e^{-q\tau}\phi(d_1)\sigma}{2\sqrt{\tau}}+rK e^{-r\tau}N(-d_2)-qS e^{-q\tau}N(-d_1).
$$

Call rho:

$$
\rho_C=K\tau e^{-r\tau}N(d_2).
$$

Put rho:

$$
\rho_P=-K\tau e^{-r\tau}N(-d_2).
$$

Call dividend rho:

$$
\psi_C=-\tau S e^{-q\tau}N(d_1).
$$

Put dividend rho:

$$
\psi_P=\tau S e^{-q\tau}N(-d_1).
$$

---

## 12.7 Higher-Order Greek Reference

| Greek | Definition | Main Use |
|---|---:|---|
| Vanna | $\partial^2V/(\partial S\partial\sigma)$ | Spot-volatility interaction |
| Volga / Vomma | $\partial^2V/\partial\sigma^2$ | Volatility convexity |
| Charm | $\partial\Delta/\partial t$ | Delta decay through time |
| Color | $\partial\Gamma/\partial t$ | Gamma decay through time |
| Speed | $\partial\Gamma/\partial S$ | Gamma migration with spot |
| Zomma | $\partial\Gamma/\partial\sigma$ | Gamma sensitivity to volatility |
| Ultima | $\partial\text{Volga}/\partial\sigma$ | Third-order volatility convexity |
| Veta | $\partial\nu/\partial t$ | Vega decay through time |
| Vera | $\partial^2V/(\partial\sigma\partial r)$ | Vega-rate interaction |

Black-Scholes-Merton vanna:

$$
\text{Vanna}=-e^{-q\tau}\phi(d_1)\frac{d_2}{\sigma}.
$$

Volga:

$$
\text{Volga}=\nu\frac{d_1d_2}{\sigma}.
$$

Speed:

$$
\text{Speed}=-\frac{\Gamma}{S}\left(1+\frac{d_1}{\sigma\sqrt{\tau}}\right).
$$

Zomma:

$$
\text{Zomma}=\Gamma\frac{d_1d_2-1}{\sigma}.
$$

Ultima:

$$
\text{Ultima}=-\frac{\nu}{\sigma^2}\left[d_1d_2(1-d_1d_2)+d_1^2+d_2^2\right].
$$

A useful first-order Greek evolution approximation is:

$$
d\Delta\approx \Gamma dS+\text{Vanna}d\sigma+\text{Charm}dt.
$$

Vega evolution approximation:

$$
d\nu\approx \text{Vanna}dS+\text{Volga}d\sigma+\text{Veta}dt+\text{Vera}dr.
$$

Gamma evolution approximation:

$$
d\Gamma\approx \text{Speed}dS+\text{Zomma}d\sigma+\text{Color}dt.
$$

---

## 12.8 Scaling and Unit Conventions

Incorrect scaling is one of the most common practical sources of option-risk errors.

| Quantity | Raw Mathematical Unit | Desk-Friendly Unit |
|---|---|---|
| Delta | per $1 spot unit | contract delta = raw delta times multiplier |
| Dollar delta | $\Delta S$ | approximate exposure for 100% underlying move |
| Gamma | per $1 spot unit squared | gamma dollars = $\Gamma S^2$ times position scale |
| Vega | per 1.00 volatility unit | divide by 100 for one volatility point |
| Volga | per $(1.00)^2$ volatility unit | divide by 10,000 for vol-point squared |
| Vanna | per $1 spot and 1.00 volatility | divide by 100 for spot and one vol point |
| Theta | per year if time in years | divide by 365 or 252 depending on convention |
| Rho | per 1.00 rate unit | divide by 10,000 for one basis point |

For a position with quantity $Q$ and multiplier $M$:

$$
\text{DollarDelta}=QM\Delta S.
$$

Gamma dollars:

$$
\text{GammaDollar}=QM\Gamma S^2.
$$

Vega per one volatility point:

$$
\nu^{1vol}=\frac{QM\nu}{100}.
$$

Daily theta under a calendar-day convention:

$$
\Theta^{daily}=\frac{QM\Theta}{365}.
$$

Rho per basis point:

$$
\rho^{1bp}=\frac{QM\rho}{10000}.
$$

---

## 12.9 Local P&L Decomposition Reference

For a small move in spot, volatility, rates, and time:

$$
\Delta V\approx
\Delta\Delta S
+\frac{1}{2}\Gamma(\Delta S)^2
+\Theta\Delta t
+\nu\Delta\sigma
+\rho\Delta r.
$$

Including vanna and volga:

$$
\Delta V\approx
\Delta\Delta S
+\frac{1}{2}\Gamma(\Delta S)^2
+\Theta\Delta t
+\nu\Delta\sigma
+\rho\Delta r
+\text{Vanna}\Delta S\Delta\sigma
+\frac{1}{2}\text{Volga}(\Delta\sigma)^2.
$$

For a delta-hedged option, the first-order delta term is approximately offset:

$$
\Delta\Pi\approx
\frac{1}{2}\Gamma(\Delta S)^2
+\Theta\Delta t
+\nu\Delta\sigma.
$$

Gamma P&L in return form:

$$
\text{Gamma P\&L}\approx\frac{1}{2}\Gamma S^2 r_S^2.
$$

Break-even realized volatility for a delta-hedged long option, ignoring vega and costs:

$$
\sigma_{BE}\approx\sqrt{\frac{-2\Theta}{\Gamma S^2}}.
$$

---

## 12.10 Volatility Surface Reference

The implied volatility surface is:

$$
\sigma_{imp}=\sigma_{imp}(K,T),
$$

or more robustly:

$$
\sigma_{imp}=\sigma_{imp}(k_F,\tau).
$$

A simple smile model is:

$$
\sigma_{imp}(k_F,\tau)=a(\tau)+b(\tau)k_F+c(\tau)k_F^2.
$$

Here:

- $a(\tau)$ is at-the-money volatility level;
- $b(\tau)$ is skew slope;
- $c(\tau)$ is curvature.

Forward variance between two maturities:

$$
\sigma_{fwd}^2(\tau_1,\tau_2)=\frac{\sigma_2^2\tau_2-\sigma_1^2\tau_1}{\tau_2-\tau_1}.
$$

Variance risk premium:

$$
\text{VRP}_{t,T}=\sigma_{imp,t,T}^2-\widehat{\sigma}_{real,t,T}^2.
$$

Surface-aware delta:

$$
\Delta_{surface}=\Delta_{flat}+\nu\frac{\partial\sigma_{imp}}{\partial S}.
$$

Surface-aware gamma:

$$
\Gamma_{surface}=\Gamma_{flat}
+2\text{Vanna}\frac{\partial\sigma_{imp}}{\partial S}
+\text{Volga}\left(\frac{\partial\sigma_{imp}}{\partial S}\right)^2
+\nu\frac{\partial^2\sigma_{imp}}{\partial S^2}.
$$

---

## 12.11 Strategy Greek Profile Reference

| Strategy | Delta | Gamma | Theta | Vega | Main Exposure | Main Failure Mode |
|---|---:|---:|---:|---:|---|---|
| Long call | + | + | - | + | Direction + convexity | Theta decay and vol crush |
| Long put | - | + | - | + | Downside convexity | Expensive protection and timing |
| Short call | - | - | + | - | Short upside convexity | Upside gap and short squeeze |
| Short put | + | - | + | - | Short downside convexity | Crash and margin expansion |
| Long straddle | near 0 initially | + | - | + | Realized/event volatility | Insufficient move and vol crush |
| Short straddle | near 0 initially | - | + | - | Volatility carry | Large move and vol spike |
| Covered call | + capped | - | + | - | Equity plus short upside vol | Strong rally underperformance |
| Protective put | + reduced | + | - | + | Equity downside hedge | Persistent premium bleed |
| Collar | + bounded | mixed | mixed | mixed | Downside hedge financed by upside sale | Upside cap or insufficient protection |
| Calendar | path-dependent | mixed | mixed | term vega | Term-structure exposure | Front vol repricing and path risk |
| Risk reversal | directional | mixed | mixed | mixed | Skew and direction | Sold tail realizes |
| Dispersion | hedged | mixed | mixed | index vs single-name vega | Correlation risk premium | Correlation spike |
| Short variance | near 0 if hedged | - | + | - | Variance risk premium | Volatility explosion and jumps |
| Long wings | low initially | + in tails | - | + | Tail convexity | Carry bleed and poor timing |

---

## 12.12 Regime-to-Strategy Reference

| Regime | More Suitable Exposures | Exposures Requiring Caution |
|---|---|---|
| Low-vol carry | Defined-risk short premium, covered calls, selective collars | Excessive naked short gamma, crowded short vol |
| Stable carry | Short vega with limits, calendars, overwriting | Long gamma without catalyst |
| Rising-vol transition | Long gamma, long vega, long skew, protective puts | Short skew, short straddles, short puts |
| High-vol stress | Liquidity preservation, defined-risk convexity, reduced gross | Adding short vol too early |
| Post-shock normalization | Selective short vega, calendars, term-structure trades | Long vol after extreme repricing |
| Crash convexity | Long downside gamma, long skew, tail hedges | Short puts, short variance, short downside skew |
| Vol-of-vol expansion | Long volga, long wings, vanna-aware hedges | Vega-neutral books with hidden short volga |

Regime-aware allocation should use probabilities:

$$
\widehat{\mu}_{s,t}=\sum_{k=1}^{K}p_{k,t}\mu_{s,k}.
$$

Regime-conditioned variance:

$$
\widehat{\sigma}_{s,t}^{2}=\sum_{k=1}^{K}p_{k,t}(\sigma_{s,k}^{2}+\mu_{s,k}^{2})-\widehat{\mu}_{s,t}^{2}.
$$

Entropy-based confidence:

$$
H_t=-\sum_{k=1}^{K}p_{k,t}\log(p_{k,t}),
$$

$$
\text{Confidence}_t=1-\frac{H_t}{\log K}.
$$

---

## 12.13 Portfolio Construction Reference

Let $\mathbf{w}\in\mathbb{R}^{N}$ be portfolio weights and $\mathbf{A}\in\mathbb{R}^{M\times N}$ be the Greek exposure matrix. Portfolio exposures are:

$$
\mathbf{g}_p=\mathbf{A}\mathbf{w}.
$$

A Greek-constrained mean-variance objective is:

$$
\max_{\mathbf{w}}\quad
\boldsymbol{\mu}^{\top}\mathbf{w}-\frac{\lambda}{2}\mathbf{w}^{\top}\boldsymbol{\Sigma}\mathbf{w}-\text{TC}(\mathbf{w},\mathbf{w}^{old})
$$

subject to:

$$
\mathbf{L}_g\le\mathbf{A}\mathbf{w}\le\mathbf{U}_g,
$$

$$
\mathbf{l}\le\mathbf{w}\le\mathbf{u},
$$

$$
\mathcal{M}(\mathbf{w})\le M_{max},
$$

$$
\sum_i |w_i-w_i^{old}|\le T_{max}.
$$

Expected shortfall objective:

$$
\max_{\mathbf{w}}\quad
\boldsymbol{\mu}^{\top}\mathbf{w}-\lambda ES_{\alpha}(\mathbf{w})-\text{TC}(\mathbf{w},\mathbf{w}^{old}).
$$

Risk contribution:

$$
RC_i=w_i\frac{(\boldsymbol{\Sigma}\mathbf{w})_i}{\sqrt{\mathbf{w}^{\top}\boldsymbol{\Sigma}\mathbf{w}}}.
$$

---

## 12.14 Covariance and Risk Model Reference

Sample covariance:

$$
\widehat{\boldsymbol{\Sigma}}=\frac{1}{T-1}\sum_{t=1}^{T}(\mathbf{r}_t-\bar{\mathbf{r}})(\mathbf{r}_t-\bar{\mathbf{r}})^\top.
$$

EWMA covariance:

$$
\widehat{\boldsymbol{\Sigma}}_t^{EWMA}=\lambda\widehat{\boldsymbol{\Sigma}}_{t-1}^{EWMA}+(1-\lambda)\mathbf{x}_t\mathbf{x}_t^\top.
$$

Linear shrinkage:

$$
\widehat{\boldsymbol{\Sigma}}_{shrink}=\delta\mathbf{F}+(1-\delta)\widehat{\boldsymbol{\Sigma}}_{sample}.
$$

Factor covariance:

$$
\boldsymbol{\Sigma}_{opt}=\mathbf{B}\boldsymbol{\Sigma}_{f}\mathbf{B}^{\top}+\boldsymbol{\Sigma}_{\epsilon}.
$$

Marchenko-Pastur bounds using $q=N/T$:

$$
\lambda_-=(1-\sqrt{q})^2,
$$

$$
\lambda_+=(1+\sqrt{q})^2.
$$

Regime-conditioned covariance:

$$
\widehat{\boldsymbol{\Sigma}}_t=\sum_{k=1}^{K}p_{k,t}\boldsymbol{\Sigma}_k.
$$

Full mixture covariance with regime means:

$$
\widehat{\boldsymbol{\Sigma}}_t=\sum_{k=1}^{K}p_{k,t}\left[\boldsymbol{\Sigma}_k+(\boldsymbol{\mu}_k-\widehat{\boldsymbol{\mu}})(\boldsymbol{\mu}_k-\widehat{\boldsymbol{\mu}})^\top\right].
$$

---

## 12.15 Risk and Stress Testing Reference

Full repricing scenario P&L:

$$
\Delta V_{p,s}^{Full}=\sum_i w_iM_i\left[V_i(\mathbf{x}_{i,s})-V_i(\mathbf{x}_{i,0})\right].
$$

Greek approximation scenario P&L:

$$
\Delta V_{p,s}^{Greek}=\sum_i w_iM_i\left[
\Delta_i\Delta S_{i,s}+\frac{1}{2}\Gamma_i(\Delta S_{i,s})^2+\nu_i\Delta\sigma_{i,s}+\text{Vanna}_i\Delta S_{i,s}\Delta\sigma_{i,s}+\frac{1}{2}\text{Volga}_i(\Delta\sigma_{i,s})^2
\right].
$$

Approximation error:

$$
\varepsilon_{p,s}=\Delta V_{p,s}^{Full}-\Delta V_{p,s}^{Greek}.
$$

Relative approximation error:

$$
\text{RelativeError}_{p,s}=\frac{|\varepsilon_{p,s}|}{|\Delta V_{p,s}^{Full}|+\epsilon}.
$$

Drawdown:

$$
D_t=\frac{W_t}{\max_{u\le t}W_u}-1.
$$

Margin utilization:

$$
U_t^{\mathcal{M}}=\frac{\mathcal{M}_t}{C_t}.
$$

Stress margin condition:

$$
\frac{\mathcal{M}(S_t+\Delta S,\sigma_t+\Delta\sigma,\text{stress})}{C_t+\Delta\Pi_{stress}}\le U_{max}^{\mathcal{M},stress}.
$$

---

## 12.16 Backtesting Reference

A valid options backtest must be point-in-time. At decision time $t$, the strategy may use only information available at $t$.

A standard backtest loop is:

$$
\text{Data}_{\le t}\rightarrow\text{Signals}_t\rightarrow\text{Portfolio}_t\rightarrow\text{Execution}_{t}\rightarrow\text{P\&L}_{t,t+h}\rightarrow\text{Attribution}_{t,t+h}.
$$

Key biases:

| Bias | Description | Control |
|---|---|---|
| Look-ahead bias | Using data not known at trade time | Use availability timestamps and vintages |
| Survivorship bias | Excluding delisted names or expired option chains | Use historical universe membership |
| Selection bias | Testing only successful structures | Predefine universe and strategy rules |
| Mid-price bias | Assuming execution at mid | Use bid/ask, slippage, and impact assumptions |
| Stale quote bias | Treating stale marks as executable | Quote freshness filters |
| Corporate-action bias | Ignoring contract adjustments | Historical corporate-action processing |
| Macro revision bias | Using revised CPI, GDP, PMI, etc. | Point-in-time macro vintages |
| Rebalance timing bias | Assuming same-day impossible execution | Decision/execution timestamp separation |

Minimum performance metrics:

- total and annualized return;
- volatility;
- Sharpe ratio and Sortino ratio;
- maximum drawdown;
- expected shortfall;
- hit rate;
- average win and average loss;
- skewness and kurtosis;
- turnover;
- transaction costs;
- margin utilization;
- stress losses;
- P&L attribution by Greek and strategy sleeve.

For short-volatility strategies, Sharpe ratio is not enough. Expected shortfall, drawdown, crash loss, margin expansion, and liquidity stress are essential.

---

## 12.17 Data Requirements Checklist

| Data Category | Required Fields |
|---|---|
| Option chain | bid, ask, mid, last, volume, open interest, strike, expiry, option type, style, multiplier |
| Underlying | price, corporate actions, dividends, borrow, sector, country, currency, factor exposures |
| Volatility surface | implied vol, moneyness, delta, tenor, skew, curvature, term structure |
| Rates | risk-free curves, discount factors, collateral assumptions, currency curves |
| Dividends | discrete dividends, ex-dates, forecast dividends, special dividend flags |
| Borrow | borrow rate, locate availability, hard-to-borrow flag |
| Events | earnings dates, macro releases, central-bank meetings, corporate actions, M&A flags |
| Liquidity | spreads, volume, open interest, quote age, depth, market-impact proxy |
| Macro | CPI, PMI, GDP, unemployment, credit spreads, yield curve, financial conditions |
| Risk | historical returns, vol changes, skew changes, correlation, liquidity stress |
| Execution | commissions, slippage, fill rules, trade timestamps, hedge prices |
| Margin | broker margin, clearing margin, stress margin, collateral and liquidity capacity |

---

## 12.18 Option-Chain Cleaning Checklist

A production option-chain process should reject or flag:

- nonpositive bid or ask when inappropriate;
- ask lower than bid;
- stale quotes;
- zero volume and zero open interest where liquidity is required;
- extremely wide bid-ask spreads;
- invalid implied volatility;
- prices violating no-arbitrage bounds;
- calendar arbitrage in total variance;
- butterfly arbitrage across strikes;
- missing contract multiplier;
- missing or incorrect corporate-action adjustment;
- missing dividend or borrow assumptions;
- American options treated as European without justification;
- options too close to expiration for the intended strategy;
- options with unreliable settlement or exercise rules.

---

## 12.19 Production Architecture Reference

A production-grade options research platform should have the following modules:

| Module | Function |
|---|---|
| Data ingestion | Load option chains, underlyings, rates, dividends, borrow, macro, events |
| Data validation | Clean bad quotes, stale data, corporate actions, missing fields |
| Surface builder | Construct arbitrage-aware implied-volatility surfaces |
| Pricing engine | Price options under selected models |
| Greek engine | Compute core, higher-order, surface-aware, and finite-difference Greeks |
| Signal engine | Compute VRP, skew, term, event, liquidity, and regime signals |
| Regime engine | Estimate volatility and macro regime probabilities |
| Portfolio optimizer | Allocate under expected return, covariance, Greek, margin, and liquidity constraints |
| Stress engine | Full repricing under spot, vol, skew, rate, liquidity, jump, and correlation shocks |
| Backtester | Run point-in-time historical simulations with realistic execution |
| Attribution engine | Decompose P&L by Greeks, surface, costs, residuals, and sleeves |
| Risk dashboard | Monitor exposures, limits, stress losses, margin, and liquidity |
| Governance layer | Version models, inputs, overrides, approvals, and audit logs |

---

## 12.20 Institutional Readiness Checklist

Before deployment, the strategy should pass the following checks.

### Research Validity

| Check | Required Standard |
|---|---|
| Economic rationale | Strategy has a clear risk-premium, hedging, or inefficiency hypothesis |
| Point-in-time data | All signals use only historically available information |
| Cost model | Bid-ask, slippage, commissions, impact, borrow, financing, and hedge costs included |
| Robustness | Results survive alternate windows, universes, costs, and parameter choices |
| Regime analysis | Performance measured across volatility and macro regimes |
| Tail analysis | Expected shortfall, drawdown, crash windows, and jump scenarios evaluated |
| Capacity | Liquidity, open interest, volume, and days-to-exit constraints tested |
| Attribution | P&L decomposed by delta, gamma, theta, vega, skew, costs, and residuals |

### Risk Control

| Check | Required Standard |
|---|---|
| Greek limits | Total and bucketed Greek limits defined |
| Stress limits | Full repricing losses within scenario limits |
| Margin limits | Normal and stress margin within capital capacity |
| Liquidity limits | Exit horizon and spread-widening assumptions acceptable |
| Event limits | Earnings, dividends, corporate actions, and macro events controlled |
| Borrow controls | Hard-to-borrow and locate constraints included |
| Kill switches | Drawdown, margin, liquidity, residual, and data triggers defined |
| Monitoring | Daily or intraday dashboard available |

### Governance

| Check | Required Standard |
|---|---|
| Model versioning | Pricing, surface, Greek, signal, and optimizer versions stored |
| Data lineage | Every input can be traced to source and timestamp |
| Override logs | Manual overrides recorded and justified |
| Exception handling | Missing data, stale quotes, and model failures handled |
| Independent review | Code, model assumptions, and results reviewed |
| Reconciliation | Broker/vendor marks and Greeks reconciled where possible |
| Documentation | Strategy methodology and operating procedures documented |

---

## 12.21 Common Red Flags

| Red Flag | Why It Matters |
|---|---|
| Strategy works only at mid prices | Gross edge may disappear after execution costs |
| Positive Sharpe with hidden crash losses | Short-volatility risk may be undermeasured |
| Total Greeks look neutral but bucketed Greeks are concentrated | False diversification |
| Vega-neutral but large vanna or volga | Exposure can reappear after spot or volatility shocks |
| High premium yield screens dominate | Likely selects event, distress, or illiquidity risk |
| Backtest uses current constituents | Survivorship and look-ahead bias |
| Earnings dates are not point-in-time | Event strategy results may be biased |
| American options priced as European near dividends | Exercise risk and pricing error |
| No margin stress | Forced deleveraging risk ignored |
| No residual P&L monitoring | Model failure may remain hidden |
| Covariance matrix nearly singular | Optimizer likely exploiting noise |
| Regime model used as binary switch | Overconfidence and excess turnover |

---

## 12.22 Practical Implementation Roadmap

A realistic institutional implementation can be staged.

### Stage 1: Research Prototype

- Build clean option-chain parser.
- Implement Black-Scholes-Merton pricing and Greeks.
- Compute implied volatility and simple surface features.
- Create liquidity filters and basic universe rules.
- Backtest one or two strategy families with conservative costs.
- Build simple P&L attribution.

### Stage 2: Robust Backtesting

- Add point-in-time corporate actions, dividends, borrow, and earnings dates.
- Add surface-aware Greeks.
- Add realistic bid-ask and slippage rules.
- Add walk-forward parameter estimation.
- Add full-repricing stress tests.
- Evaluate regime-conditioned performance.

### Stage 3: Portfolio Construction

- Add Greek exposure matrix.
- Add constraints by underlying, sector, maturity, moneyness, and strategy sleeve.
- Add covariance stabilization and factor covariance.
- Add margin and liquidity constraints.
- Add turnover and transaction-cost penalties.
- Add expected shortfall and stress-loss constraints.

### Stage 4: Production Risk Platform

- Automate data ingestion and validation.
- Version all models, data, and signals.
- Reconcile broker and vendor marks.
- Build daily risk dashboard.
- Add alerts and kill-switch rules.
- Add governance workflow and audit trail.
- Monitor live P&L attribution and residuals.

### Stage 5: Continuous Improvement

- Compare expected versus realized P&L by Greek.
- Recalibrate cost and slippage models.
- Review failure cases and missed risks.
- Update regime models and scenario libraries.
- Validate out-of-sample performance and turnover.
- Retire signals that no longer work.

---

## 12.23 Minimal Institutional Python Package Structure

A practical research repository might use:

```text
options_research/
  data/
    loaders.py
    validators.py
    corporate_actions.py
    earnings.py
    borrow.py
  pricing/
    bsm.py
    american.py
    implied_vol.py
    surfaces.py
    greeks.py
  signals/
    vrp.py
    skew.py
    term_structure.py
    event_vol.py
    liquidity.py
    regimes.py
  portfolio/
    exposures.py
    constraints.py
    optimizer.py
    margin.py
    transaction_costs.py
  risk/
    stress.py
    scenarios.py
    expected_shortfall.py
    covariance.py
    attribution.py
  backtest/
    engine.py
    execution.py
    accounting.py
    metrics.py
  reports/
    dashboards.py
    tearsheets.py
  tests/
    test_pricing.py
    test_greeks.py
    test_surface.py
    test_backtest_no_lookahead.py
    test_risk_limits.py
```

Minimum tests should verify:

- put-call parity;
- analytical Greeks versus finite differences;
- implied-volatility inversion accuracy;
- no look-ahead in signal construction;
- option-chain filters behave as intended;
- corporate-action adjustments do not break multipliers;
- stress scenarios reprice all positions;
- optimizer respects Greek and margin constraints;
- P&L accounting reconciles trade, mark, hedge, and cost components.

---

## 12.24 Final Synthesis

The main lessons of the curriculum are:

1. **Greeks are local sensitivities, not complete risk measures.** They are essential, but they must be supplemented with surface-aware risk and full repricing.
2. **Higher-order Greeks matter because first-order Greeks are unstable.** Vanna, volga, charm, color, speed, and related exposures explain how risk changes.
3. **Volatility is a surface, not a number.** Skew, curvature, term structure, event variance, and correlation risk drive real option P&L.
4. **Hedging is discrete and costly.** Continuous hedging is a theoretical benchmark, not a real implementation plan.
5. **Short-volatility strategies require special skepticism.** They often earn frequent small gains while hiding rare nonlinear losses.
6. **Regime awareness should be probabilistic.** Strategies should scale with regime probabilities and uncertainty, not binary labels.
7. **Portfolio construction must control nonlinear risk factors.** Delta neutrality is not enough; gamma, vega, skew, vanna, volga, liquidity, margin, and events matter.
8. **Covariance estimates are fragile.** Shrinkage, factor models, RMT cleaning, and regime-conditioned covariance can improve stability, but cannot replace stress testing.
9. **Backtests are easy to bias.** Point-in-time data, realistic execution, survivorship controls, and event timing are non-negotiable.
10. **Production requires governance.** Versioning, monitoring, reconciliation, exception handling, and kill-switches are part of the strategy, not administrative afterthoughts.

The final institutional standard is not whether a strategy looks profitable in a clean historical simulation. The standard is whether its exposures, costs, risks, data lineage, failure modes, and governance are understood well enough to survive live implementation.

---

## 12.25 Final Reference: One-Page Operating Checklist

Before approving any options strategy, answer the following:

| Question | Pass Requirement |
|---|---|
| What exposure is being monetized? | Clear risk premium or hedging rationale |
| What are the current Greeks? | Total and bucketed exposures documented |
| What happens if spot moves sharply? | Full repricing stress tested |
| What happens if volatility rises or falls? | Vega, vanna, volga, skew, and term shocks tested |
| What happens if liquidity disappears? | Exit cost and days-to-exit modeled |
| What happens to margin? | Stress margin within capital capacity |
| Are events handled? | Earnings, dividends, borrow, corporate actions included |
| Are costs realistic? | Bid/ask, slippage, impact, financing, borrow included |
| Is the backtest point-in-time? | No survivorship, look-ahead, or revised-data bias |
| Does P&L attribution explain results? | Delta, gamma, theta, vega, skew, costs, residuals reported |
| Are limits defined? | Greek, stress, drawdown, liquidity, margin, and concentration limits set |
| Are kill switches defined? | Pre-committed triggers and actions documented |
| Is the strategy robust by regime? | Performance and losses evaluated across states |
| Is governance complete? | Data, model, signal, execution, and override logs retained |

If any answer is weak, the strategy should remain in research or paper-trading mode until the gap is closed.

---

# End of Curriculum

This concludes the institutional curriculum on options Greeks, systematic strategy design, volatility-surface risk, regime-aware allocation, portfolio construction, covariance stabilization, stress testing, backtesting, and production governance.
