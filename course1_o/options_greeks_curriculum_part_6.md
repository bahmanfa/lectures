# Institutional Options Greeks, Systematic Strategy, and Regime-Aware Portfolio Construction Curriculum

## Completed Installment

This installment contains:

- Part 6: Regime-Aware Options Strategy Selection.

The document is educational and research-oriented. It is not personalized investment advice, a live trading recommendation, or a claim that any option strategy produces guaranteed alpha.

---

# Part 6: Regime-Aware Options Strategy Selection

**Level:** Expert

## 6.1 Purpose of Part 6

Options strategies are strongly regime-dependent. A short-volatility strategy that appears stable during a low-volatility carry regime can experience sudden nonlinear losses during a volatility transition. A long-gamma strategy can look unattractive during calm markets because of persistent theta decay, but it can become valuable when realized volatility rises, jumps occur, or liquidity deteriorates. A collar can look expensive when downside protection demand is high, but it may improve portfolio utility when drawdown control is the objective.

The purpose of regime-aware options strategy selection is to connect three layers:

1. **Market state identification:** estimate the probability that the market is in each volatility, macro, liquidity, credit, and cross-asset regime.
2. **Strategy suitability:** estimate which option strategy families are structurally suited to each regime.
3. **Greek-aware allocation:** translate regime probabilities into probability-weighted strategy weights and Greek budgets.

The key principle is:

$$
\text{Regime-aware options allocation should be probabilistic, not binary.}
$$

A robust process should avoid statements such as “risk-on means sell volatility” or “risk-off means buy puts” as deterministic rules. Instead, it should estimate regime probabilities, condition expected returns and risks on those probabilities, and allocate with constraints on delta, gamma, vega, theta, vanna, volga, skew, liquidity, margin, and drawdown.

## 6.2 Why Regime Awareness Matters More for Options Than for Linear Assets

Linear assets such as equities and bonds have risk profiles that are often dominated by first-order exposures. Options are nonlinear. Their risks change with spot, volatility, time, skew, liquidity, and event states. This means regime shifts affect options through multiple channels at once.

During a risk-off transition, for example:

- spot may fall;
- implied volatility may rise;
- downside skew may steepen;
- correlations may increase;
- bid-ask spreads may widen;
- margin requirements may increase;
- short-gamma hedging demand may become one-sided;
- dealer balance-sheet capacity may fall;
- realized volatility may become jump-dominated.

A local Greek approximation may treat these as separate shocks. A regime-aware process recognizes them as jointly distributed features of a state transition.

For an option portfolio with state vector $\mathbf{x}_t$, a general regime-conditioned return model is:

$$
\mathbb{E}_t[R_{p,t+h}]
=\sum_{k=1}^{K}p_{k,t}\,\mathbb{E}_t[R_{p,t+h}\mid z_{t+h}=k],
$$

where:

- $R_{p,t+h}$ is portfolio return or P&L over horizon $h$;
- $z_{t+h}\in\{1,\ldots,K\}$ is the future regime state;
- $p_{k,t}=\mathbb{P}(z_{t+h}=k\mid\mathcal{F}_t)$ is the probability of regime $k$ conditional on current information $\mathcal{F}_t$;
- $K$ is the number of regimes.

This equation is central: expected return is not estimated under one assumed regime. It is averaged over possible regimes using probabilities.

## 6.3 Volatility Regimes

Volatility regimes describe the behavior of realized volatility, implied volatility, volatility-of-volatility, skew, and volatility term structure. They are directly relevant to option strategy selection because they affect gamma, theta, vega, vanna, volga, and margin.

## 6.3.1 Low-Volatility Carry Regime

A low-volatility carry regime is characterized by:

- low realized volatility;
- low or moderate implied volatility;
- stable or gently upward-sloping volatility term structure;
- limited realized jumps;
- contained bid-ask spreads;
- low cross-asset stress;
- positive carry for option sellers if implied volatility remains above realized volatility.

Typical strategy implications:

| Dimension | Interpretation |
|---|---|
| Short gamma | May earn theta if realized volatility remains low, but crash risk can be underpriced |
| Long gamma | Often suffers theta decay unless convexity is unusually cheap |
| Short vega | Can work if implied volatility is rich versus expected realized volatility |
| Long skew | May be inexpensive in calm markets but timing is uncertain |
| Covered calls | Can monetize call premium but cap upside |
| Collars | Protection may be cheaper, but opportunity cost depends on call sale |

The main failure mode is complacency. Low volatility can persist, but it can also precede abrupt volatility expansion.

## 6.3.2 Stable Carry Regime

A stable carry regime is not necessarily extremely low volatility. It is a regime where realized volatility is predictable, liquidity is adequate, and implied volatility compensates option sellers after expected costs.

Characteristics:

- realized volatility is moderate and mean-reverting;
- implied-realized spread is positive;
- volatility term structure is orderly;
- skew is not steepening aggressively;
- correlation is stable;
- liquidity is sufficient for hedging and rolling.

Typical strategy implications:

- defined-risk short premium may be preferable to naked short options;
- short-volatility exposure should be sized to margin and stress constraints;
- calendars and diagonals may benefit if term structure is stable;
- covered calls and collars may be useful overlays;
- long-gamma exposure can be maintained as a small hedge sleeve rather than a dominant allocation.

## 6.3.3 Rising-Volatility Transition Regime

A rising-volatility transition regime is often the most dangerous regime for naive short-volatility strategies. It occurs when markets move from calm to unstable conditions.

Characteristics:

- realized volatility rises from a low or moderate base;
- implied volatility rises faster than recent realized volatility;
- downside skew steepens;
- cross-asset correlations increase;
- credit spreads widen;
- liquidity begins to deteriorate;
- macro uncertainty becomes more important.

Typical strategy implications:

| Exposure | Regime Suitability |
|---|---|
| Long gamma | More attractive if realized volatility is expected to exceed implied carry cost |
| Long vega | Attractive if implied volatility is expected to keep rising |
| Long downside skew | Useful for crash convexity and portfolio hedging |
| Short gamma | Dangerous unless tightly defined-risk and small |
| Short skew | High risk because skew may steepen further |
| Calendars | Sensitive to front-end repricing; structure must be event-aware |

The key implementation challenge is timing. Long-volatility positions can still lose if entered after implied volatility has already repriced too far.

## 6.3.4 High-Volatility Stress Regime

A high-volatility stress regime is characterized by crisis or near-crisis conditions.

Features include:

- high realized volatility;
- high implied volatility;
- inverted volatility term structure;
- wide bid-ask spreads;
- unstable intraday liquidity;
- high margin requirements;
- steep downside skew;
- high correlation;
- frequent gap moves.

Typical strategy implications:

- capital preservation and liquidity management become central;
- long convexity may help but can be expensive if purchased late;
- adding short volatility too early can be hazardous;
- defined-risk structures are preferable to open-ended short options;
- hedging assumptions should be stress-tested with wider spreads and delayed execution;
- gross exposure should often be reduced.

The main failure mode is assuming that high implied volatility is automatically rich. In stress regimes, high implied volatility can still be too low if realized volatility, jumps, and liquidity costs are extreme.

## 6.3.5 Post-Shock Normalization Regime

Post-shock normalization occurs after a volatility spike when uncertainty begins to decline.

Characteristics:

- implied volatility declines from elevated levels;
- realized volatility may remain high but begins to stabilize;
- front-end term structure may normalize from inversion;
- skew may flatten but remain elevated;
- liquidity improves gradually;
- risk appetite returns unevenly.

Typical strategy implications:

- selective short vega may become attractive;
- calendars can benefit from term-structure normalization;
- covered calls may monetize elevated call premiums;
- collars may be restructured as protection costs decline;
- long-volatility hedges should be reviewed for carry drag.

The failure mode is selling volatility too aggressively before aftershocks have passed.

## 6.3.6 Crash Convexity Regime

A crash convexity regime is a state where large downside moves, jumps, and liquidity gaps dominate ordinary volatility metrics.

Characteristics:

- large negative returns;
- discontinuous price moves;
- sharp implied-volatility spikes;
- extreme downside skew;
- high correlation;
- funding and margin stress;
- reduced market depth.

Typical strategy implications:

- long downside gamma and long skew are most directly useful;
- short puts, short variance, and short skew are most dangerous;
- hedge instruments may become difficult to trade;
- full repricing is required because local Greeks can be unreliable;
- risk systems should prioritize survival and liquidity.

## 6.3.7 Vol-of-Vol Expansion Regime

Vol-of-vol expansion occurs when implied volatility itself becomes highly unstable.

Characteristics:

- large moves in implied volatility;
- unstable skew and curvature;
- frequent surface parameter jumps;
- large vanna and volga effects;
- vega-neutral books becoming exposed after shocks;
- model calibration instability.

Typical strategy implications:

- volga and vanna risk should be explicitly constrained;
- simple vega neutrality is insufficient;
- long wing convexity may be useful;
- short-volatility structures with hidden short volga are dangerous;
- scenario analysis should include parallel vol, skew, curvature, and term shocks.

## 6.4 Macro Regimes

Volatility regimes describe market pricing of uncertainty. Macro regimes describe the economic and policy environment that can drive risk premia, earnings expectations, rates, liquidity, and cross-asset correlations.

## 6.4.1 Growth Acceleration

Growth acceleration is characterized by improving economic activity, stronger earnings expectations, and often stronger risk appetite.

Potential indicators:

- rising PMI;
- improving earnings revisions;
- tightening credit spreads;
- positive equity momentum;
- stable or rising real yields if growth-led;
- improving financial conditions.

Options implications:

- covered calls may underperform in strong upside rallies;
- short put strategies may benefit if downside risk declines, but gap risk remains;
- upside call demand may rise;
- volatility can remain low if growth is stable;
- long gamma may need specific catalysts.

## 6.4.2 Growth Slowdown

Growth slowdown is characterized by weaker activity and deteriorating earnings expectations.

Potential indicators:

- falling PMI;
- rising unemployment claims;
- negative earnings revisions;
- widening credit spreads;
- declining cyclical equity leadership;
- flattening or inverted yield curve.

Options implications:

- downside skew may become more valuable;
- protective puts and collars may improve portfolio utility;
- short-volatility strategies require caution;
- dispersion may change as idiosyncratic and sector risks rise;
- long gamma can become more attractive if realized volatility rises.

## 6.4.3 Inflation Shock

An inflation shock occurs when inflation surprises higher or becomes more persistent.

Potential indicators:

- CPI and core CPI surprises;
- rising inflation expectations;
- rising nominal yields;
- rising breakeven inflation;
- central-bank tightening expectations;
- commodity strength.

Options implications:

- equity and rate volatility may rise together;
- discount-rate-sensitive equities may show higher volatility;
- volatility term structure may reprice around central-bank meetings;
- rate-sensitive option rho and equity-index vega can interact;
- short-volatility strategies can be vulnerable if inflation triggers policy uncertainty.

## 6.4.4 Disinflation

Disinflation is a regime where inflation pressure declines.

Potential indicators:

- falling CPI trend;
- declining breakevens;
- easing supply-chain pressure;
- lower commodity inflation;
- central-bank tightening expectations falling.

Options implications depend on whether disinflation is growth-friendly or recessionary:

- growth-friendly disinflation may support risk assets and reduce volatility;
- recessionary disinflation may coincide with credit stress and downside risk;
- regime classification should avoid treating all disinflation as risk-on.

## 6.4.5 Liquidity Expansion

Liquidity expansion is characterized by easier financial conditions and increased risk appetite.

Potential indicators:

- narrowing credit spreads;
- easier financial conditions indices;
- central-bank balance-sheet expansion or reduced tightening pressure;
- lower funding stress;
- rising market breadth;
- lower volatility.

Options implications:

- volatility carry may perform, but crowding risk can build;
- upside call demand may increase;
- downside skew may cheapen;
- long-volatility hedges can bleed;
- short-volatility sizing should still account for abrupt liquidity reversals.

## 6.4.6 Liquidity Tightening

Liquidity tightening is characterized by reduced market liquidity, tighter credit, and higher funding pressure.

Potential indicators:

- widening credit spreads;
- higher funding spreads;
- tighter financial conditions;
- rising real yields;
- deteriorating market breadth;
- reduced dealer balance-sheet capacity.

Options implications:

- downside skew and implied volatility can rise;
- short gamma can become dangerous;
- bid-ask spreads widen;
- margin and financing costs rise;
- long convexity and collars may improve portfolio utility.

## 6.4.7 Credit Stress

Credit stress directly affects equity volatility, correlation, skew, and liquidity.

Potential indicators:

- high-yield spreads widening;
- investment-grade spreads widening;
- default risk rising;
- bank equity underperformance;
- funding market stress;
- deteriorating credit availability.

Options implications:

- downside equity skew often steepens;
- single-name options on levered firms can become jump-risk dominated;
- put spreads may be preferable to outright puts if skew is very expensive;
- short put strategies require strong controls;
- dispersion trades can be exposed to correlation spikes.

## 6.4.8 Risk-On and Risk-Off Regimes

Risk-on and risk-off are broad cross-asset states rather than precise macro regimes.

A risk-on regime may include:

- positive equity momentum;
- narrowing credit spreads;
- declining implied volatility;
- improving breadth;
- pro-cyclical sector leadership;
- stable funding conditions.

A risk-off regime may include:

- equity drawdowns;
- widening credit spreads;
- rising implied volatility;
- defensive sector leadership;
- rising dollar or safe-haven assets;
- higher correlation and lower liquidity.

Options strategy selection should not reduce to “risk-on equals short volatility” and “risk-off equals long volatility.” A risk-on regime with extremely cheap convexity may still justify long optionality. A risk-off regime with extremely expensive implied volatility may justify selective defined-risk short premium after stress controls.

## 6.5 Indicator Set for Regime Detection

A practical regime system should combine market-implied, realized market, macroeconomic, and liquidity indicators.

## 6.5.1 Market-Implied Indicators

| Indicator | Example Measurement | Options Relevance |
|---|---|---|
| Implied volatility level | ATM IV by tenor | Vega, volatility carry, stress |
| Volatility term structure | 3m IV minus 1m IV; VIX futures slope | Roll-down, stress, normalization |
| Downside skew | 25-delta put IV minus ATM IV | Crash demand and skew risk |
| Smile curvature | Wing IVs minus ATM IV | Tail richness and vol-of-vol proxy |
| Implied correlation | Index variance versus single-name variance | Dispersion and correlation risk |
| Option volume and open interest | Contract-level metrics | Liquidity and crowding |

## 6.5.2 Realized Market Indicators

| Indicator | Example Measurement | Options Relevance |
|---|---|---|
| Realized volatility | 10d, 21d, 63d realized vol | Gamma scalping, VRP |
| Realized skewness | Rolling return skewness | Tail behavior |
| Jump frequency | Large return count | Gap risk |
| Trend | 3m/12m momentum | Directional and risk-on/off state |
| Drawdown | Current drawdown from trailing high | Stress state |
| Correlation | Rolling average pairwise correlation | Dispersion and index options |
| Cross-asset momentum | Equity, rates, credit, FX, commodities | Macro regime context |

## 6.5.3 Macro Indicators

| Indicator | Example Use | Options Relevance |
|---|---|---|
| CPI and core CPI | Inflation pressure and surprises | Rate volatility, equity vol, policy uncertainty |
| Unemployment and claims | Labor-market deterioration | Growth slowdown and recession risk |
| PMI | Growth acceleration or slowdown | Cyclical risk and earnings uncertainty |
| Credit spreads | Credit stress and liquidity | Downside skew and correlation |
| Yield curve | Growth and policy expectations | Macro regime, rates-equity interaction |
| Liquidity conditions | Financial conditions indices, funding spreads | Volatility and margin stress |
| Earnings revisions | Forward profit cycle | Single-name and sector risk |
| Real rates | Discount-rate pressure | Equity duration and vol sensitivity |

## 6.5.4 Data Frequency and Release Timing

Regime systems must respect data timing. Market data can be daily or intraday. Macro data are released monthly, weekly, or quarterly, often with revisions. A point-in-time regime system should use only information available at the decision time.

For macro indicator $x_t$ released with lag $\ell$, the available value at time $t$ is:

$$
x^{\text{available}}_t=x_{t-\ell}^{\text{vintage}},
$$

where $x_{t-\ell}^{\text{vintage}}$ is the value from the historical data vintage available at time $t$. Using revised data creates look-ahead bias.

## 6.6 Hidden Markov Models for Volatility Regime Detection

## 6.6.1 HMM Structure

A Hidden Markov Model assumes that observed data are generated by an unobserved state process. Let:

- $z_t\in\{1,\ldots,K\}$ be the hidden regime at time $t$;
- $\mathbf{y}_t$ be the observed feature vector at time $t$;
- $A$ be the transition matrix;
- $\pi$ be the initial state probability vector;
- $f_k(\mathbf{y}_t)$ be the emission density in state $k$.

The transition probabilities are:

$$
A_{ij}=\mathbb{P}(z_t=j\mid z_{t-1}=i),
$$

where each row satisfies:

$$
\sum_{j=1}^{K}A_{ij}=1.
$$

The initial probabilities are:

$$
\pi_k=\mathbb{P}(z_1=k),\quad \sum_{k=1}^{K}\pi_k=1.
$$

If emissions are Gaussian:

$$
\mathbf{y}_t\mid z_t=k \sim \mathcal{N}(\boldsymbol{\mu}_k,\boldsymbol{\Sigma}_k),
$$

where $\boldsymbol{\mu}_k$ is the state mean vector and $\boldsymbol{\Sigma}_k$ is the state covariance matrix.

## 6.6.2 HMM Likelihood

The likelihood of observations $\mathbf{y}_{1:T}$ is:

$$
\mathcal{L}(\theta)=
\sum_{z_1=1}^{K}\cdots\sum_{z_T=1}^{K}
\pi_{z_1}f_{z_1}(\mathbf{y}_1)
\prod_{t=2}^{T}A_{z_{t-1},z_t}f_{z_t}(\mathbf{y}_t),
$$

where $\theta=\{\pi,A,\boldsymbol{\mu}_1,\ldots,\boldsymbol{\mu}_K,\boldsymbol{\Sigma}_1,\ldots,\boldsymbol{\Sigma}_K\}$ is the parameter set.

The direct summation over all state paths is computationally infeasible for large $T$, so the forward algorithm is used.

## 6.6.3 Forward Filtering

Define the filtered probability:

$$
\alpha_t(k)=\mathbb{P}(z_t=k,\mathbf{y}_{1:t}\mid\theta).
$$

The recursion is:

$$
\alpha_t(k)=f_k(\mathbf{y}_t)\sum_{j=1}^{K}\alpha_{t-1}(j)A_{jk}.
$$

The normalized filtered probability is:

$$
p_{t}(k)=\mathbb{P}(z_t=k\mid\mathbf{y}_{1:t})
=\frac{\alpha_t(k)}{\sum_{m=1}^{K}\alpha_t(m)}.
$$

These filtered probabilities are the regime probabilities used for allocation. They should be used as continuous weights, not hard labels.

## 6.6.4 Example Volatility HMM States

A three-state volatility HMM might identify:

| State | Typical Features | Interpretation |
|---|---|---|
| State 1 | Low realized vol, low IV, positive carry | Low-vol carry |
| State 2 | Rising realized vol, IV rising, skew steepening | Transition |
| State 3 | High vol, inverted term structure, high correlation | Stress |

A four- or five-state model may separate post-shock normalization, crash convexity, or vol-of-vol expansion. More states can improve interpretation but increase estimation error and instability.

## 6.7 Markov-Switching Models

A Markov-switching model allows return or volatility dynamics to change by regime. For example, an asset return model may be:

$$
R_t = \mu_{z_t}+\sigma_{z_t}\varepsilon_t,
$$

where:

- $R_t$ is asset return;
- $z_t$ is the latent regime;
- $\mu_{z_t}$ is regime-specific expected return;
- $\sigma_{z_t}$ is regime-specific volatility;
- $\varepsilon_t\sim\mathcal{N}(0,1)$.

For options, a more relevant model may define regime-specific dynamics for realized volatility, implied volatility changes, and skew:

$$
\begin{bmatrix}
\Delta \sigma^{\text{imp}}_t \\
\sigma^{\text{real}}_t \\
\Delta \text{Skew}_t
\end{bmatrix}
=
\boldsymbol{\mu}_{z_t}
+\boldsymbol{\varepsilon}_{t,z_t},
$$

where $\boldsymbol{\varepsilon}_{t,z_t}$ has regime-specific covariance.

This directly supports strategy selection because the expected P&L of gamma, vega, and skew exposures depends on the regime-specific distribution of realized variance and implied-volatility changes.

## 6.8 Bayesian Filtering

Bayesian filtering updates regime probabilities as new observations arrive.

Let $p_{t-1}(j)$ be the previous regime probability. The one-step predicted probability is:

$$
\tilde{p}_{t}(k)=\sum_{j=1}^{K}p_{t-1}(j)A_{jk}.
$$

After observing $\mathbf{y}_t$, Bayes' rule gives:

$$
p_t(k)=\frac{f_k(\mathbf{y}_t)\tilde{p}_t(k)}{\sum_{m=1}^{K}f_m(\mathbf{y}_t)\tilde{p}_t(m)}.
$$

Variables:

- $p_t(k)$ is the posterior probability of regime $k$ at time $t$;
- $\tilde{p}_t(k)$ is the predicted probability before observing $\mathbf{y}_t$;
- $f_k(\mathbf{y}_t)$ is the likelihood of observing $\mathbf{y}_t$ under regime $k$;
- $A_{jk}$ is the transition probability from regime $j$ to regime $k$.

This equation is a practical foundation for online regime detection. It also makes uncertainty explicit. If probabilities are diffuse, the allocation engine should reduce confidence and avoid over-concentrated regime bets.

## 6.9 State-Space Models

State-space models represent hidden states that evolve through time and generate observations. A linear Gaussian state-space model is:

$$
\mathbf{x}_t = \mathbf{F}\mathbf{x}_{t-1}+\mathbf{u}_t,
$$

$$
\mathbf{y}_t = \mathbf{H}\mathbf{x}_t+\mathbf{v}_t,
$$

where:

- $\mathbf{x}_t$ is the latent state vector;
- $\mathbf{y}_t$ is the observed data vector;
- $\mathbf{F}$ is the state transition matrix;
- $\mathbf{H}$ is the observation matrix;
- $\mathbf{u}_t\sim\mathcal{N}(0,\mathbf{Q})$ is state noise;
- $\mathbf{v}_t\sim\mathcal{N}(0,\mathbf{R})$ is observation noise.

In options research, the latent state vector might include:

$$
\mathbf{x}_t=\begin{bmatrix}
\text{VolLevel}_t \\
\text{VolTrend}_t \\
\text{SkewPressure}_t \\
\text{LiquidityStress}_t \\
\text{MacroGrowthState}_t
\end{bmatrix}.
$$

State-space models are useful because they can smooth noisy observations and combine mixed-frequency indicators. For example, daily market data can be combined with monthly CPI and PMI releases if release lags are handled correctly.

## 6.10 Dynamic Model Averaging

Dynamic model averaging combines multiple forecasting models using time-varying model probabilities.

Suppose there are $M$ models. Model $m$ produces a forecast $\widehat{R}_{m,t+1}$ for strategy return. The combined forecast is:

$$
\widehat{R}_{t+1}^{\text{DMA}}=\sum_{m=1}^{M}\omega_{m,t}\widehat{R}_{m,t+1},
$$

where:

- $\omega_{m,t}\ge 0$ is the time-varying weight on model $m$;
- $\sum_{m=1}^{M}\omega_{m,t}=1$.

Model weights can be updated based on predictive likelihood:

$$
\omega_{m,t}\propto \omega_{m,t-1}^{\lambda} \cdot p_m(y_t\mid\mathcal{F}_{t-1}),
$$

where:

- $\lambda\in(0,1]$ is a forgetting factor;
- $p_m(y_t\mid\mathcal{F}_{t-1})$ is the predictive likelihood of observation $y_t$ under model $m$.

For options strategies, candidate models may include:

- volatility HMM;
- macro regime model;
- credit stress model;
- trend and momentum model;
- liquidity stress model;
- event-risk model.

Dynamic model averaging is useful because no single regime model is reliable across all environments.

## 6.11 System Dynamics and Macro Causal Loop Systems

Statistical regime models detect patterns in data. System Dynamics models represent causal mechanisms and feedback loops. In macro-options research, the two approaches can complement each other.

A simplified macro causal loop may include:

$$
\text{Inflation Pressure} \rightarrow \text{Central Bank Tightening} \rightarrow \text{Real Rates} \rightarrow \text{Equity Valuation Pressure} \rightarrow \text{Volatility Demand}.
$$

Another loop may be:

$$
\text{Credit Stress} \rightarrow \text{Funding Pressure} \rightarrow \text{Risk Reduction} \rightarrow \text{Equity Drawdown} \rightarrow \text{Volatility Spike} \rightarrow \text{Margin Pressure}.
$$

A simple linear system representation is:

$$
\mathbf{x}_{t+1}=\mathbf{A}\mathbf{x}_t+\mathbf{B}\mathbf{s}_t+\boldsymbol{\varepsilon}_{t+1},
$$

where:

- $\mathbf{x}_t$ is a vector of macro and market state variables;
- $\mathbf{A}$ captures propagation among endogenous variables;
- $\mathbf{B}$ maps exogenous shocks into the system;
- $\mathbf{s}_t$ is a vector of shocks such as inflation shock, credit shock, liquidity shock, or growth shock;
- $\boldsymbol{\varepsilon}_{t+1}$ is residual innovation.

A regime probability can be linked to the system state through a softmax mapping:

$$
p_{k,t}=\frac{\exp(a_k+\mathbf{b}_k^{\top}\mathbf{x}_t)}{\sum_{j=1}^{K}\exp(a_j+\mathbf{b}_j^{\top}\mathbf{x}_t)}.
$$

This maps macro state variables into regime probabilities while preserving probabilistic allocation.

## 6.12 Mapping Regime Probabilities to Strategy Expected Returns

Let $s\in\{1,\ldots,S\}$ index strategy sleeves and $k\in\{1,\ldots,K\}$ index regimes. Let $\mu_{s,k}$ be the expected return of strategy $s$ conditional on regime $k$:

$$
\mu_{s,k}=\mathbb{E}[R_{s,t+h}\mid z_t=k].
$$

Given regime probabilities $p_{k,t}$, the probability-weighted expected return is:

$$
\widehat{\mu}_{s,t}=\sum_{k=1}^{K}p_{k,t}\mu_{s,k}.
$$

Similarly, regime-conditioned variance can be approximated as:

$$
\widehat{\sigma}_{s,t}^{2}
=\sum_{k=1}^{K}p_{k,t}\left(\sigma_{s,k}^{2}+\mu_{s,k}^{2}\right)-\widehat{\mu}_{s,t}^{2},
$$

where $\sigma_{s,k}^{2}$ is the conditional variance of strategy $s$ in regime $k$.

A risk-adjusted strategy score can be defined as:

$$
\text{Score}_{s,t}=\frac{\widehat{\mu}_{s,t}}{\widehat{\sigma}_{s,t}+\epsilon}-\lambda_c\widehat{C}_{s,t}-\lambda_m\widehat{M}_{s,t},
$$

where:

- $\epsilon>0$ prevents division by zero;
- $\widehat{C}_{s,t}$ is expected transaction and hedging cost;
- $\widehat{M}_{s,t}$ is margin intensity or capital usage;
- $\lambda_c$ and $\lambda_m$ are penalty weights.

This score is not a trade recommendation. It is an input to constrained allocation.

## 6.13 Probability-Weighted Allocation Equation

Let $w_{s,t}$ be the allocation weight to strategy sleeve $s$. A basic probability-weighted allocation is:

$$
w_{s,t}^{\text{raw}}
= w_s^{\max}\cdot \max(0,\text{Score}_{s,t})\cdot \left(\sum_{k=1}^{K}p_{k,t}\eta_{s,k}\right),
$$

where:

- $w_s^{\max}$ is the maximum allowed sleeve weight;
- $\eta_{s,k}\in[0,1]$ is suitability of sleeve $s$ in regime $k$;
- $p_{k,t}$ is current probability of regime $k$;
- $\text{Score}_{s,t}$ is the risk-adjusted attractiveness score.

Weights are then normalized:

$$
w_{s,t}=\frac{w_{s,t}^{\text{raw}}}{\sum_{j=1}^{S}w_{j,t}^{\text{raw}}}\cdot W_t^{\text{target}},
$$

where $W_t^{\text{target}}$ is the total target allocation to options strategies after risk scaling.

If all raw scores are zero, the allocation should be zero or assigned to a defensive default sleeve, depending on mandate.

## 6.14 Probability-Weighted Greek Budget Constraints

Regime-aware allocation must also control Greek exposures. Let $G_{s}^{(m)}$ be the exposure of strategy sleeve $s$ to Greek or risk factor $m$, such as delta, gamma, vega, theta, vanna, volga, skew, or margin. Portfolio exposure is:

$$
G_{p,t}^{(m)}=\sum_{s=1}^{S}w_{s,t}G_{s,t}^{(m)}.
$$

A static Greek budget constraint is:

$$
L^{(m)}\le G_{p,t}^{(m)}\le U^{(m)},
$$

where $L^{(m)}$ and $U^{(m)}$ are lower and upper bounds.

A regime-dependent Greek budget allows exposure limits to change with regime probabilities:

$$
U_t^{(m)}=\sum_{k=1}^{K}p_{k,t}U_{k}^{(m)},
$$

$$
L_t^{(m)}=\sum_{k=1}^{K}p_{k,t}L_{k}^{(m)}.
$$

Then:

$$
L_t^{(m)}\le \sum_{s=1}^{S}w_{s,t}G_{s,t}^{(m)}\le U_t^{(m)}.
$$

Interpretation:

- In rising-volatility regimes, the upper bound on long gamma or long vega may increase.
- In low-volatility carry regimes, the allowed short gamma budget may increase but must remain stress-limited.
- In high-volatility stress regimes, gross exposure and margin usage limits may tighten.
- In vol-of-vol expansion, vanna and volga limits may become more restrictive.

This approach avoids deterministic switching while adapting risk budgets to state probabilities.

## 6.15 Strategy Suitability Matrix

A stylized regime-to-strategy suitability matrix is shown below. Values are conceptual and should be calibrated or governed through research validation.

| Strategy Sleeve | Low-Vol Carry | Stable Carry | Rising Vol | High-Vol Stress | Post-Shock Normalization | Crash Convexity | Vol-of-Vol Expansion |
|---|---:|---:|---:|---:|---:|---:|---:|
| Long gamma | 0.25 | 0.35 | 0.90 | 0.70 | 0.40 | 1.00 | 0.80 |
| Short gamma carry | 0.75 | 0.85 | 0.15 | 0.00 | 0.35 | 0.00 | 0.05 |
| Long vega | 0.30 | 0.35 | 0.85 | 0.55 | 0.20 | 0.70 | 0.85 |
| Short vega carry | 0.70 | 0.80 | 0.20 | 0.05 | 0.75 | 0.00 | 0.10 |
| Protective puts | 0.35 | 0.45 | 0.85 | 0.80 | 0.45 | 1.00 | 0.70 |
| Collars | 0.55 | 0.70 | 0.75 | 0.70 | 0.65 | 0.75 | 0.55 |
| Calendars | 0.60 | 0.75 | 0.45 | 0.25 | 0.85 | 0.20 | 0.35 |
| Dispersion | 0.55 | 0.65 | 0.35 | 0.15 | 0.55 | 0.10 | 0.30 |
| Short skew | 0.55 | 0.60 | 0.10 | 0.00 | 0.35 | 0.00 | 0.05 |
| Long skew | 0.30 | 0.40 | 0.85 | 0.80 | 0.45 | 1.00 | 0.75 |

The matrix should not be treated as universal. It depends on market, asset class, valuation, mandate, cost, and risk tolerance.

## 6.16 Regime-Conditioned Greek Expectations

For each strategy sleeve $s$, define expected Greek exposure under regime $k$:

$$
\bar{G}_{s,k}^{(m)}=\mathbb{E}[G_{s,t+h}^{(m)}\mid z_t=k].
$$

The probability-weighted expected Greek is:

$$
\widehat{G}_{s,t}^{(m)}=\sum_{k=1}^{K}p_{k,t}\bar{G}_{s,k}^{(m)}.
$$

This matters because Greeks themselves are dynamic. A short strangle may have moderate gamma today, but under a rising-volatility or crash regime, expected gamma, vanna, and margin exposure can become much larger in absolute value.

A regime-aware system should therefore forecast not only returns but also future exposures:

$$
\mathbb{E}_t[\mathbf{G}_{p,t+h}]
=\sum_{k=1}^{K}p_{k,t}\mathbb{E}[\mathbf{G}_{p,t+h}\mid z_{t+h}=k].
$$

This is especially important for short-dated options, short gamma, and single-name event risk.

## 6.17 Regime Confidence and De-Risking

When regime probabilities are diffuse, the model is uncertain. A useful uncertainty measure is entropy:

$$
H_t=-\sum_{k=1}^{K}p_{k,t}\log(p_{k,t}).
$$

Maximum entropy occurs when probabilities are equal across regimes. A confidence score can be defined as:

$$
\text{Confidence}_t=1-\frac{H_t}{\log K}.
$$

This score lies between 0 and 1:

- near 1 means one regime dominates;
- near 0 means probabilities are diffuse.

A risk scale can be defined as:

$$
\text{RiskScale}_t=\min\left(1,\max\left(0, a+b\cdot\text{Confidence}_t-c\cdot\text{Stress}_t\right)\right),
$$

where $a$, $b$, and $c$ are parameters and $\text{Stress}_t$ is a normalized stress indicator. This prevents the allocation engine from taking large positions when the regime model is uncertain or stress is elevated.

## 6.18 Single-Stock Regime Considerations

Single-stock options require additional regime layers beyond index volatility and macro state.

Important single-name regimes include:

| Single-Stock State | Indicators | Options Implication |
|---|---|---|
| Pre-earnings | Earnings within next $D$ days | Event variance and volatility crush dominate |
| Post-earnings | Earnings just released | Implied vol normalization; gap realized |
| Takeover speculation | Abnormal call skew, news, sector M&A | Upside jump risk; short calls dangerous |
| Credit deterioration | CDS/spread widening, equity drawdown | Downside put skew and jump-to-default risk |
| Hard-to-borrow | High borrow cost, low availability | Put-call parity distortions and short hedge cost |
| Crowded retail flow | High option volume, call skew, social attention | Squeeze and gap risk |
| Corporate action | Splits, special dividends, spin-offs | Contract adjustment and model risk |

A single-name regime probability can be combined with macro regime probabilities. For example:

$$
p_{j,k,t}^{\text{combined}} \propto p_{k,t}^{\text{macro}}\cdot p_{j,t}^{\text{name event}}.
$$

After normalization, the combined probability should be used to adjust strategy suitability and risk limits for that stock.

## 6.19 Python Code: Simple HMM-Based Volatility Regime Classifier

The following code provides a reproducible HMM-style volatility regime classifier. It first attempts to use `hmmlearn` if available. If `hmmlearn` is unavailable, it falls back to a Gaussian mixture approximation with simple transition estimates. The fallback is not a full HMM, but it preserves the interface for research prototyping.

```python
import numpy as np
import pandas as pd


def make_vol_regime_features(price: pd.Series, implied_vol: pd.Series | None = None) -> pd.DataFrame:
    """Create volatility-regime features from prices and optional implied volatility.

    Parameters
    ----------
    price:
        Price series indexed by date. Must be positive.
    implied_vol:
        Optional implied volatility series in decimal annualized units.

    Returns
    -------
    DataFrame with realized volatility, drawdown, return, and optional IV features.
    """
    if (price <= 0).any():
        raise ValueError("price must be positive")

    px = price.astype(float).dropna()
    ret = np.log(px).diff()
    rv_10 = ret.rolling(10).std() * np.sqrt(252)
    rv_21 = ret.rolling(21).std() * np.sqrt(252)
    rv_63 = ret.rolling(63).std() * np.sqrt(252)
    drawdown = px / px.cummax() - 1.0

    features = pd.DataFrame(
        {
            "return_1d": ret,
            "rv_10": rv_10,
            "rv_21": rv_21,
            "rv_63": rv_63,
            "drawdown": drawdown,
            "abs_return": ret.abs(),
        }
    )

    if implied_vol is not None:
        iv = implied_vol.reindex(features.index).astype(float)
        features["implied_vol"] = iv
        features["iv_rv_spread"] = iv - features["rv_21"]
        features["iv_change_5d"] = iv.diff(5)

    return features.dropna()


def standardize_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Standardize features using full-sample mean and std for demonstration.

    Production systems should fit scalers only on training data in each
    walk-forward window to avoid look-ahead bias.
    """
    mu = df.mean()
    sigma = df.std().replace(0.0, np.nan)
    z = (df - mu) / sigma
    return z.replace([np.inf, -np.inf], np.nan).dropna(), mu, sigma


def fit_hmm_or_fallback(features: pd.DataFrame, n_states: int = 3, seed: int = 42) -> pd.DataFrame:
    """Fit a simple volatility regime classifier.

    The preferred implementation uses hmmlearn.GaussianHMM. If hmmlearn is not
    installed, a GaussianMixture fallback is used. The fallback does not model
    Markov transitions during fitting and should be treated as a prototype.
    """
    if n_states < 2:
        raise ValueError("n_states must be at least 2")

    z, _, _ = standardize_features(features)
    x = z.to_numpy()

    try:
        from hmmlearn.hmm import GaussianHMM

        model = GaussianHMM(
            n_components=n_states,
            covariance_type="full",
            n_iter=500,
            random_state=seed,
        )
        model.fit(x)
        probs = model.predict_proba(x)
        states = probs.argmax(axis=1)
        transition_matrix = model.transmat_
    except Exception:
        from sklearn.mixture import GaussianMixture

        model = GaussianMixture(n_components=n_states, covariance_type="full", random_state=seed)
        model.fit(x)
        probs = model.predict_proba(x)
        states = probs.argmax(axis=1)

        # Estimate empirical transitions from classified states.
        transition_counts = np.ones((n_states, n_states)) * 1e-6
        for a, b in zip(states[:-1], states[1:]):
            transition_counts[a, b] += 1.0
        transition_matrix = transition_counts / transition_counts.sum(axis=1, keepdims=True)

    out = pd.DataFrame(index=z.index)
    for k in range(n_states):
        out[f"p_state_{k}"] = probs[:, k]
    out["state"] = states

    # Order states by average 21-day realized volatility for interpretation.
    state_rv = features.reindex(out.index).groupby(out["state"])["rv_21"].mean().sort_values()
    order_map = {old_state: new_rank for new_rank, old_state in enumerate(state_rv.index)}
    out["state_ordered_by_vol"] = out["state"].map(order_map)

    out.attrs["transition_matrix"] = transition_matrix
    out.attrs["state_rv_order"] = state_rv.to_dict()
    return out


# Example with synthetic data.
def simulate_regime_price_path(n: int = 1000, seed: int = 7) -> pd.Series:
    """Simulate a price path with changing volatility regimes."""
    rng = np.random.default_rng(seed)
    vols = np.r_[np.repeat(0.10, 300), np.repeat(0.25, 300), np.repeat(0.45, 200), np.repeat(0.15, 200)]
    daily_vols = vols / np.sqrt(252)
    returns = rng.normal(0.0002, daily_vols[:n])
    price = 100 * np.exp(np.cumsum(returns))
    dates = pd.bdate_range("2020-01-01", periods=n)
    return pd.Series(price, index=dates, name="price")


price = simulate_regime_price_path()
features = make_vol_regime_features(price)
regimes = fit_hmm_or_fallback(features, n_states=3)
print(regimes.tail())
print("Transition matrix:")
print(np.round(regimes.attrs["transition_matrix"], 3))
print("State realized-vol ordering:")
print(regimes.attrs["state_rv_order"])
```

## 6.20 Python Code: Regime-to-Strategy Allocation Engine

The following code maps regime probabilities to strategy allocations using suitability weights, strategy scores, risk scaling, and Greek constraints.

```python
import numpy as np
import pandas as pd


def entropy_confidence(probabilities: pd.Series) -> float:
    """Compute normalized confidence from regime probabilities."""
    p = probabilities.astype(float).clip(lower=0)
    p = p / p.sum()
    k = len(p)
    entropy = -(p * np.log(p + 1e-12)).sum()
    return float(1.0 - entropy / np.log(k))


def probability_weighted_scores(
    strategy_scores: pd.Series,
    regime_probs: pd.Series,
    suitability: pd.DataFrame,
) -> pd.Series:
    """Combine strategy alpha scores with regime suitability.

    suitability rows are strategies and columns are regimes.
    """
    if not strategy_scores.index.equals(suitability.index):
        raise ValueError("strategy_scores index must match suitability rows")
    if not regime_probs.index.equals(suitability.columns):
        raise ValueError("regime_probs index must match suitability columns")

    p = regime_probs / regime_probs.sum()
    regime_fit = suitability @ p
    raw = strategy_scores.clip(lower=0.0) * regime_fit
    return raw


def normalize_weights(raw_scores: pd.Series, total_weight: float) -> pd.Series:
    """Normalize nonnegative raw scores to a target total weight."""
    raw = raw_scores.clip(lower=0.0).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    if raw.sum() <= 0 or total_weight <= 0:
        return pd.Series(0.0, index=raw.index)
    return total_weight * raw / raw.sum()


def apply_greek_constraints_iterative(
    weights: pd.Series,
    greek_exposures: pd.DataFrame,
    lower_bounds: pd.Series,
    upper_bounds: pd.Series,
    max_iter: int = 100,
) -> pd.Series:
    """Simple heuristic to scale weights until aggregate Greek constraints are met.

    This is not a full optimizer. It is a transparent fallback for research
    prototypes. Production systems should use constrained optimization.
    """
    w = weights.copy().astype(float)

    for _ in range(max_iter):
        portfolio_greeks = greek_exposures.T @ w
        violations = []

        for greek in portfolio_greeks.index:
            value = portfolio_greeks[greek]
            lb = lower_bounds.get(greek, -np.inf)
            ub = upper_bounds.get(greek, np.inf)
            if value < lb:
                violations.append((greek, value, lb, "lower"))
            elif value > ub:
                violations.append((greek, value, ub, "upper"))

        if not violations:
            return w

        # Conservative global scaling. More advanced methods should identify
        # which sleeves drive each violation and solve a constrained problem.
        w *= 0.95

    return w


def allocate_regime_aware_options(
    strategy_scores: pd.Series,
    regime_probs: pd.Series,
    suitability: pd.DataFrame,
    greek_exposures: pd.DataFrame,
    lower_bounds: pd.Series,
    upper_bounds: pd.Series,
    base_total_weight: float = 0.50,
    stress_score: float = 0.0,
) -> pd.Series:
    """Allocate options strategy sleeves using regime probabilities and constraints."""
    confidence = entropy_confidence(regime_probs)
    risk_scale = np.clip(0.50 + 0.50 * confidence - 0.50 * stress_score, 0.0, 1.0)
    target_weight = base_total_weight * risk_scale

    raw = probability_weighted_scores(strategy_scores, regime_probs, suitability)
    weights = normalize_weights(raw, target_weight)
    constrained = apply_greek_constraints_iterative(weights, greek_exposures, lower_bounds, upper_bounds)
    return constrained


# Example setup.
strategies = pd.Index(["long_gamma", "short_vega", "collar", "calendar", "long_skew"])
regimes = pd.Index(["low_vol", "rising_vol", "stress", "normalization"])

strategy_scores = pd.Series(
    [0.40, 0.70, 0.55, 0.60, 0.50],
    index=strategies,
)

regime_probs = pd.Series(
    [0.20, 0.35, 0.25, 0.20],
    index=regimes,
)

suitability = pd.DataFrame(
    {
        "low_vol": [0.25, 0.80, 0.60, 0.70, 0.30],
        "rising_vol": [0.90, 0.15, 0.75, 0.45, 0.85],
        "stress": [0.70, 0.05, 0.75, 0.25, 0.90],
        "normalization": [0.40, 0.75, 0.65, 0.85, 0.45],
    },
    index=strategies,
)

greek_exposures = pd.DataFrame(
    {
        "delta": [0.05, 0.02, 0.20, 0.03, -0.10],
        "gamma": [0.80, -0.60, 0.10, -0.05, 0.50],
        "vega": [0.70, -0.80, 0.05, 0.60, 0.50],
        "theta": [-0.50, 0.60, 0.05, 0.10, -0.35],
        "vanna": [0.30, -0.25, 0.10, 0.15, 0.35],
        "volga": [0.40, -0.35, 0.05, 0.20, 0.45],
    },
    index=strategies,
)

lower_bounds = pd.Series({"delta": -0.10, "gamma": -0.15, "vega": -0.20, "theta": -0.30})
upper_bounds = pd.Series({"delta": 0.25, "gamma": 0.35, "vega": 0.40, "theta": 0.35})

weights = allocate_regime_aware_options(
    strategy_scores=strategy_scores,
    regime_probs=regime_probs,
    suitability=suitability,
    greek_exposures=greek_exposures,
    lower_bounds=lower_bounds,
    upper_bounds=upper_bounds,
    base_total_weight=0.60,
    stress_score=0.25,
)

print("Weights:")
print(weights.round(4))
print("Portfolio Greeks:")
print((greek_exposures.T @ weights).round(4))
```

## 6.21 Production Considerations for Regime-Aware Options Allocation

## 6.21.1 Walk-Forward Estimation

Regime models must be trained and evaluated in a walk-forward framework. At each rebalance date $t$, the model should be estimated only using data available before or at $t$.

A simplified walk-forward loop is:

$$
\text{Train on }[t_0,t]\;\rightarrow\;\text{estimate }p_{k,t}\;\rightarrow\;\text{allocate}\;\rightarrow\;\text{observe }R_{t,t+h}.
$$

Then advance the window and repeat.

## 6.21.2 Regime Label Instability

HMM state labels can switch across refits. State 0 in one training window may not correspond to state 0 in another. Labels should be ordered or mapped by interpretable statistics such as:

- average realized volatility;
- average implied volatility;
- average drawdown;
- average credit spread;
- average skew;
- average liquidity stress.

## 6.21.3 Mixed-Frequency Data

Macro data may be monthly or quarterly, while options and market data are daily or intraday. The regime system should align data by availability date, not observation date. Revised data must not be used unless the backtest is explicitly designed as a revised-data study.

## 6.21.4 Cost and Liquidity Regime Dependence

Transaction costs are regime-dependent. A spread cost model can be written as:

$$
\widehat{C}_{i,t}=C_{i,0}\left(1+a_1\text{VolRegimeStress}_t+a_2\text{LiquidityStress}_t+a_3\text{JumpRisk}_{i,t}\right),
$$

where $C_{i,0}$ is baseline cost and $a_1,a_2,a_3$ are nonnegative sensitivity parameters.

A strategy that appears attractive using normal-market costs may be unattractive after stress-cost adjustment.

## 6.21.5 Governance and Override Rules

Regime-aware systems should include governance rules:

| Governance Item | Purpose |
|---|---|
| Model versioning | Reproduce historical regime probabilities |
| Feature versioning | Track changes in indicator definitions |
| Data vintage storage | Avoid look-ahead bias in macro data |
| Stress overrides | Reduce risk when market conditions exceed model training range |
| Human review thresholds | Escalate unusual regime probabilities or allocations |
| Kill-switch rules | Stop trading or reduce exposure after drawdown, margin, or liquidity breach |
| Residual monitoring | Detect model failure through unexplained P&L |

## 6.22 Common Errors in Regime-Aware Options Research

| Error | Why It Is Dangerous | Better Practice |
|---|---|---|
| Binary regime switching | Creates overconfidence and turnover | Use probability-weighted allocation |
| Ignoring regime uncertainty | Allocates too aggressively when model is unsure | Use entropy/confidence scaling |
| Training on revised macro data | Creates look-ahead bias | Use point-in-time vintages |
| Using too many regimes | Overfits noise and unstable labels | Prefer parsimonious interpretable states |
| Assuming high IV is always rich | Stress IV can still be too low | Compare to jump, liquidity, and realized risk |
| Assuming low IV is always cheap | Low IV can persist and long options can bleed | Include carry and catalyst analysis |
| Ignoring liquidity regimes | Underestimates cost in stress | Use regime-dependent cost models |
| Ignoring margin regimes | Misses forced deleveraging risk | Stress margin and liquidity jointly |
| Ignoring single-name events | Misclassifies event risk as volatility premium | Separate earnings, borrow, and corporate actions |
| No P&L attribution | Cannot detect model failure | Attribute by Greeks, surface, costs, and residuals |

## 6.23 Summary of Part 6

Part 6 developed a regime-aware framework for options strategy selection.

Key points:

1. Options strategies are highly regime-dependent because Greeks, volatility surfaces, liquidity, and margin change across states.
2. Regime-aware allocation should be probabilistic, not binary.
3. Volatility regimes include low-vol carry, stable carry, rising-vol transition, high-vol stress, post-shock normalization, crash convexity, and vol-of-vol expansion.
4. Macro regimes include growth acceleration, growth slowdown, inflation shock, disinflation, liquidity expansion, liquidity tightening, credit stress, risk-on, and risk-off.
5. Useful regime indicators include CPI, unemployment, PMI, credit spreads, yield curve, liquidity conditions, earnings revisions, realized volatility, implied volatility, cross-asset momentum, and financial conditions.
6. Hidden Markov Models estimate latent volatility states from observed features and produce filtered regime probabilities.
7. Bayesian filtering updates regime probabilities as new observations arrive.
8. State-space models can combine noisy and mixed-frequency indicators.
9. Dynamic model averaging reduces dependence on a single regime model.
10. System Dynamics and macro causal loops can complement statistical regime models by representing propagation channels.
11. Strategy expected returns should be conditioned on regime probabilities.
12. Greek budgets should also be regime-dependent and probability-weighted.
13. Entropy can measure regime uncertainty and support de-risking.
14. Single-stock options require additional event, borrow, takeover, credit, crowding, and corporate-action regimes.
15. Production regime systems require walk-forward estimation, point-in-time data, regime label mapping, cost modeling, governance, and P&L attribution.

The next installment will cover Part 7: Greek-Aware Multi-Asset and Single-Stock Options Portfolio Construction, including portfolio-level Greek aggregation, exposure matrices, single-name risks, sector and factor aggregation, Greek constraints, optimization objectives, margin constraints, and transaction-cost-aware construction.
