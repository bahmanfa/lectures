# Institutional Options Greeks, Systematic Strategy, and Regime-Aware Portfolio Construction Curriculum

## Completed Installment

This installment contains:

- Part 3: Practical Hedging Dynamics and Greek-Based Trading.

The document is educational and research-oriented. It is not personalized investment advice, a live trading recommendation, or a claim that any option strategy produces guaranteed alpha.

---

# Part 3: Practical Hedging Dynamics and Greek-Based Trading

**Level:** Intermediate to Advanced

## 3.1 Purpose of Part 3

Parts 1 and 2 defined option values and Greeks as local sensitivities of a pricing function. Part 3 moves from static sensitivity measurement to dynamic hedging and trading mechanics. The central idea is that an option portfolio does not earn or lose money because of a Greek alone. P&L emerges from the interaction among:

- realized underlying paths;
- implied-volatility changes;
- volatility-surface changes;
- passage of time;
- hedge timing;
- transaction costs;
- liquidity and market impact;
- financing and borrow costs;
- margin requirements;
- model error and residual risk.

The most important practical distinction is between **owning an option** and **owning a dynamically hedged option strategy**. A long call without hedging is directionally bullish and long convexity. A delta-hedged long call is closer to a long-gamma, long-vega, negative-theta position. A short straddle without risk controls is short volatility, short convexity, and exposed to jumps. A delta-hedged short straddle is still exposed to realized volatility, gap risk, volatility repricing, and transaction costs.

Part 3 develops a rigorous framework for understanding these dynamics.

## 3.2 Baseline Notation and Conventions

Let:

- $V_t$ be the option value at time $t$;
- $S_t$ be the underlying spot price;
- $K$ be the strike;
- $T$ be maturity;
- $	au_t=T-t$ be time to maturity;
- $r_t$ be the risk-free rate;
- $q_t$ be the dividend yield;
- $	heta_t$ be the option theta under the convention $	heta_t=\partial V/\partial t$;
- $\Delta_t$ be delta;
- $\Gamma_t$ be gamma;
- $\nu_t$ be vega;
- $\rho_t$ be rho;
- $\sigma^{\text{imp}}_t$ be implied volatility;
- $\sigma^{\text{real}}_t$ be realized volatility;
- $h_t$ be the number of underlying shares or units used as hedge;
- $Q$ be the number of option contracts;
- $M$ be the contract multiplier.

Unless otherwise stated, formulas are first written per one option on one unit of underlying. For listed equity options, multiply by $QM$.

A local change in option value can be approximated by:

$$
\Delta V_t \approx
\Delta_t\Delta S_t
+\frac{1}{2}\Gamma_t(\Delta S_t)^2
+\theta_t\Delta t
+\nu_t\Delta\sigma_t
+\rho_t\Delta r_t
+\text{higher-order and residual terms}.
$$

Here:

- $\Delta S_t=S_{t+\Delta t}-S_t$;
- $\Delta\sigma_t=\sigma^{\text{imp}}_{t+\Delta t}-\sigma^{\text{imp}}_t$;
- $\Delta r_t=r_{t+\Delta t}-r_t$;
- $\Delta t$ is measured in years.

This approximation is useful for attribution but incomplete. It becomes less reliable for large spot moves, jumps, large implied-volatility shocks, strong skew changes, near-expiration discontinuities, and illiquid markets.

## 3.3 Delta Hedging: Core Mechanics

## 3.3.1 Definition of Delta Hedging

Delta hedging attempts to offset the first-order exposure of an option or option portfolio to the underlying asset.

For a single option position with quantity $Q$ and multiplier $M$, the option delta exposure is:

$$
\Delta^{\text{pos}}_t = QM\Delta_t.
$$

A delta-neutral hedge using the underlying requires holding:

$$
h_t = -QM\Delta_t
$$

units of the underlying.

The combined portfolio value is:

$$
\Pi_t = QM V_t + h_t S_t + B_t,
$$

where:

- $\Pi_t$ is the hedged portfolio value;
- $B_t$ is the cash account, including proceeds from hedge trades, financing, and interest;
- $h_tS_t$ is the market value of the underlying hedge.

If $h_t=-QM\Delta_t$, the first-order spot sensitivity of the combined option-plus-hedge portfolio is approximately zero:

$$
\frac{\partial \Pi_t}{\partial S_t}
=QM\Delta_t+h_t \approx 0.
$$

This neutrality is local. After spot moves, delta changes because gamma is nonzero.

## 3.3.2 Delta Hedge Rebalancing

Suppose the option delta changes from $\Delta_t$ to $\Delta_{t+1}$. The hedge must be adjusted from:

$$
h_t=-QM\Delta_t
$$

to:

$$
h_{t+1}=-QM\Delta_{t+1}.
$$

The hedge trade is:

$$
\Delta h_{t+1}=h_{t+1}-h_t=-QM(\Delta_{t+1}-\Delta_t).
$$

If the position is long gamma, delta rises when spot rises and falls when spot falls. The hedge therefore tends to sell after spot rises and buy after spot falls. This is the mechanical basis of gamma scalping.

If the position is short gamma, delta falls when spot rises and rises when spot falls. The hedge tends to buy after spot rises and sell after spot falls. This creates adverse rebalancing and can amplify losses during volatile markets.

## 3.3.3 Delta Hedging Is Not Risk Elimination

Delta hedging removes only local first-order spot exposure. It does not eliminate:

- gamma risk;
- jump risk;
- vega risk;
- skew risk;
- correlation risk;
- liquidity risk;
- financing risk;
- borrow risk;
- dividend risk;
- model risk;
- discrete hedging error.

A delta-neutral book can lose money if realized volatility is too low for a long-gamma position, too high for a short-gamma position, or if implied volatility moves against the position.

## 3.4 Continuous-Time Hedging Intuition

Under the Black-Scholes-Merton assumptions, a continuously delta-hedged option can be replicated by trading the underlying and a cash account. The option value satisfies:

$$
\frac{\partial V}{\partial t}
+(r-q)S\frac{\partial V}{\partial S}
+\frac{1}{2}\sigma^2S^2\frac{\partial^2V}{\partial S^2}
-rV=0.
$$

Using Greek notation:

$$
\theta +(r-q)S\Delta+\frac{1}{2}\sigma^2S^2\Gamma-rV=0.
$$

Rearranging:

$$
\theta +\frac{1}{2}\sigma^2S^2\Gamma = rV-(r-q)S\Delta.
$$

Interpretation:

- The option's theta and gamma are linked by no-arbitrage under the assumed implied volatility.
- For a delta-hedged option, gamma exposure is financed by theta decay and funding terms.
- Long gamma generally comes with negative theta.
- Short gamma generally comes with positive theta.

This relation is exact only under the model assumptions. In real markets, the realized hedge P&L depends on the difference between realized variance and the implied variance embedded in the option price, plus costs and residual effects.

## 3.5 Delta-Hedged P&L Approximation

Consider a delta-hedged option over a short interval. If the hedge at the start of the interval is $h_t=-\Delta_t$ per option, the option-plus-hedge spot P&L is approximately:

$$
\Delta \Pi_t
\approx
\left[\Delta_t\Delta S_t+\frac{1}{2}\Gamma_t(\Delta S_t)^2+\theta_t\Delta t+\nu_t\Delta\sigma_t\right]
-\Delta_t\Delta S_t.
$$

The delta terms cancel, giving:

$$
\Delta \Pi_t
\approx
\frac{1}{2}\Gamma_t(\Delta S_t)^2
+\theta_t\Delta t
+\nu_t\Delta\sigma_t.
$$

This is the basic local delta-hedged P&L equation.

If implied volatility does not change, rates do not change, and higher-order terms are ignored:

$$
\Delta \Pi_t
\approx
\frac{1}{2}\Gamma_t(\Delta S_t)^2
+\theta_t\Delta t.
$$

For a long option:

- $\Gamma_t>0$;
- $\theta_t$ is usually negative;
- P&L is positive if realized spot movement is large enough to overcome time decay.

For a short option:

- $\Gamma_t<0$;
- $\theta_t$ is usually positive;
- P&L is positive if realized spot movement is small enough that time decay exceeds gamma losses.

## 3.6 Gamma Scalping

## 3.6.1 Basic Concept

Gamma scalping is the process of dynamically delta hedging a long-gamma option position to harvest realized volatility. The mechanical intuition is:

- after spot rises, long gamma makes delta more positive, so the hedge sells underlying;
- after spot falls, long gamma makes delta less positive or more negative, so the hedge buys underlying;
- this creates a buy-low/sell-high pattern in the hedge.

However, the option holder pays for this convexity through theta decay and option premium. Gamma scalping is profitable only if realized movement is sufficiently high relative to implied volatility and transaction costs.

## 3.6.2 Delta-Hedged Gamma P&L and Realized Variance

Let the underlying return over a short interval be:

$$
r_t^S=\frac{\Delta S_t}{S_t}.
$$

Then:

$$
(\Delta S_t)^2=S_t^2(r_t^S)^2.
$$

The gamma P&L is approximately:

$$
\text{Gamma P\&L}_t
\approx
\frac{1}{2}\Gamma_tS_t^2(r_t^S)^2.
$$

Over many hedge intervals $t=1,\ldots,n$, cumulative gamma P&L is approximately:

$$
\sum_{t=1}^{n}\frac{1}{2}\Gamma_tS_t^2(r_t^S)^2.
$$

If gamma is treated as locally stable, this is proportional to realized variance:

$$
\sum_{t=1}^{n}(r_t^S)^2.
$$

This is why delta-hedged long-gamma positions are often described as long realized volatility or long realized variance. The description is approximate because gamma changes through time and with spot.

## 3.6.3 Break-Even Realized Volatility

Ignoring financing, dividends, transaction costs, and vega changes, a delta-hedged option approximately breaks even over a short interval when:

$$
\frac{1}{2}\Gamma_tS_t^2\sigma_{\text{real}}^2\Delta t + \theta_t\Delta t = 0.
$$

Solving for break-even realized volatility:

$$
\sigma_{\text{BE}}
\approx
\sqrt{\frac{-2\theta_t}{\Gamma_tS_t^2}}.
$$

Variables:

- $\sigma_{\text{BE}}$ is annualized break-even realized volatility;
- $\theta_t$ is annualized theta under the time-passing convention;
- $\Gamma_t$ is gamma;
- $S_t$ is spot.

For a long option with $\theta_t<0$ and $\Gamma_t>0$, the expression is positive. If realized volatility exceeds $\sigma_{\text{BE}}$, the delta-hedged long option may earn positive gamma-scalping P&L before costs and vega effects. If realized volatility is below $\sigma_{\text{BE}}$, theta decay dominates.

Under Black-Scholes-Merton assumptions, this break-even volatility is closely related to the implied volatility used to price the option. In real markets, discrete hedging, surface changes, and transaction costs shift the realized break-even threshold.

## 3.6.4 Transaction-Cost-Adjusted Break-Even

Let $c_t$ denote proportional transaction cost per dollar traded in the underlying. If the hedge change is $\Delta h_t$, transaction cost is approximately:

$$
\text{TC}_t = c_t |\Delta h_t|S_t.
$$

A transaction-cost-adjusted delta-hedged P&L approximation is:

$$
\Delta\Pi_t
\approx
\frac{1}{2}\Gamma_t(\Delta S_t)^2
+\theta_t\Delta t
- c_t |\Delta h_t|S_t.
$$

A practical break-even condition is:

$$
\frac{1}{2}\Gamma_tS_t^2\sigma_{\text{real}}^2\Delta t
+\theta_t\Delta t
> c_t |\Delta h_t|S_t.
$$

This inequality shows why hedge frequency is not trivial. More frequent hedging reduces unhedged delta error but increases trading costs. Less frequent hedging reduces transaction costs but increases path-dependent hedging error and jump exposure.

## 3.7 Hedge Frequency and Discrete Hedging Error

## 3.7.1 Why Continuous Hedging Is Unrealistic

Continuous hedging is a mathematical ideal. Real hedging is discrete because:

- markets are not open continuously;
- bid-ask spreads and commissions exist;
- execution has market impact;
- systems have latency;
- portfolio managers impose turnover limits;
- hedge instruments may be illiquid;
- trading may be restricted around events;
- shorting and borrow may be constrained;
- margin requirements can change.

Thus every real delta hedge leaves residual risk between hedge times.

## 3.7.2 Discrete Hedging Error

Let the hedge be set at time $t_i$ and held until $t_{i+1}$. The hedge uses $\Delta_{t_i}$, but the option's true delta changes during the interval. The hedging error over the interval can be written approximately as:

$$
\varepsilon_i
=\Delta V_i-\Delta_{t_i}\Delta S_i
-\left(\frac{1}{2}\Gamma_{t_i}(\Delta S_i)^2+\theta_{t_i}\Delta t_i+\nu_{t_i}\Delta\sigma_i\right).
$$

Here $\varepsilon_i$ is residual error due to:

- higher-order Greeks;
- jumps;
- volatility-surface movement;
- stale Greeks;
- finite rebalancing;
- numerical model error;
- execution effects not included in the equation.

A more explicit source of discrete delta hedging error is:

$$
\text{Delta Error}_i
\approx
\int_{t_i}^{t_{i+1}}\left(\Delta_u-\Delta_{t_i}\right)dS_u.
$$

This term is zero only if delta is constant or hedging is continuous. For options with high gamma, near expiration, or around events, this error can be large.

## 3.7.3 Scheduled Versus Threshold Hedging

Hedging policies can be classified as follows:

| Hedge Policy | Rule | Advantages | Weaknesses |
|---|---|---|---|
| Fixed-time hedging | Rebalance every fixed interval | Simple, auditable | Ignores market movement between intervals |
| Delta-band hedging | Rebalance when net delta exceeds a threshold | Reduces unnecessary trades | Can trade heavily during volatile periods |
| Volatility-aware hedging | Hedge more frequently when realized or implied vol rises | Adapts to risk | Requires robust volatility estimates |
| Cost-aware hedging | Hedge only when expected risk reduction exceeds cost | Economically disciplined | Requires cost model and risk forecast |
| Event-aware hedging | Adjust hedge rules around earnings or macro events | Controls gap risk | Event outcomes remain discontinuous |

A production system should simulate hedge policies under realistic spreads, market impact, and event gaps rather than assume a single idealized frequency.

## 3.8 Theta-Gamma Trade-Off

## 3.8.1 Structural Relation

Long vanilla options generally have positive gamma and negative theta. Short vanilla options generally have negative gamma and positive theta. This is not accidental. Optionality has value because it provides convexity, and convexity has a carrying cost.

Under a simplified delta-hedged approximation:

$$
\Delta\Pi_t
\approx
\frac{1}{2}\Gamma_tS_t^2(r_t^S)^2+\theta_t\Delta t.
$$

For long gamma:

$$
\Gamma_t>0,\quad \theta_t<0.
$$

For short gamma:

$$
\Gamma_t<0,\quad \theta_t>0.
$$

The economic question is not whether positive theta is good or negative theta is bad. The question is whether the compensation for selling convexity is adequate relative to realized volatility, jump risk, liquidity risk, and tail risk.

## 3.8.2 Short Convexity as Insurance Selling

Short-gamma positions often resemble selling insurance. They may earn small positive returns in stable markets but can lose sharply during large moves. The apparent stability of short-volatility strategies can be misleading because losses are episodic, nonlinear, and clustered in stress regimes.

The key failure mode is that realized volatility is not normally distributed. It clusters, jumps, and rises during market stress. Transaction costs and liquidity costs also rise when hedging is most needed.

## 3.8.3 Long Convexity as Insurance Buying

Long-gamma positions often lose theta in quiet markets. Their value is realized when actual price movement, volatility repricing, or jumps exceed what was priced into the option. Long convexity can therefore be useful as a hedge or crisis alpha component, but persistent carry cost can create long drawdowns.

The key failure mode is overpaying for convexity. A long-gamma strategy can be directionally correct about future volatility but still lose money if implied volatility was too expensive, if hedging costs are high, or if realized moves do not occur soon enough.

## 3.9 Vega Hedging

## 3.9.1 Basic Vega Hedge

Vega hedging attempts to reduce sensitivity to implied-volatility changes. For an option portfolio with positions $w_i$, portfolio vega is:

$$
\nu_p=\sum_{i=1}^{N}w_i\nu_i.
$$

To hedge vega using another option $j$ with vega $\nu_j$, the hedge quantity is:

$$
w_j^{\text{hedge}}=-\frac{\nu_p}{\nu_j}.
$$

This simple formula assumes:

- the hedge option's implied volatility moves one-for-one with the portfolio's implied volatility;
- maturities and strikes have the same volatility shock exposure;
- skew and term-structure changes are irrelevant;
- transaction costs and margin are ignored.

These assumptions are rarely valid in full.

## 3.9.2 Term-Structure Vega Hedging

A portfolio may be neutral to a parallel volatility shock but exposed to volatility term-structure changes.

Let $\nu_{p,j}$ be portfolio vega exposure to volatility tenor bucket $j$, such as 1-month, 3-month, 6-month, and 1-year implied volatility. A tenor-bucketed vega vector is:

$$
\boldsymbol{\nu}_p=
\begin{bmatrix}
\nu_{p,1m} \\
\nu_{p,3m} \\
\nu_{p,6m} \\
\nu_{p,1y}
\end{bmatrix}.
$$

A hedge matrix using hedge instruments $1,\ldots,H$ is:

$$
\mathbf{A}_{j,h}=\nu_{h,j},
$$

where $\nu_{h,j}$ is the exposure of hedge instrument $h$ to volatility bucket $j$. Hedge weights $\mathbf{x}$ can be chosen to solve:

$$
\min_{\mathbf{x}}\left\|\boldsymbol{\nu}_p+\mathbf{A}\mathbf{x}\right\|_2^2
+\lambda\|\mathbf{x}\|_2^2,
$$

where $\lambda\ge 0$ penalizes large hedge trades. This is a regularized least-squares hedge.

Interpretation: instead of hedging only total vega, the portfolio hedges the shape of volatility exposure across maturities.

## 3.9.3 Skew Hedging

Skew hedging addresses sensitivity to changes in volatility across strike or delta buckets. For example, an equity-index portfolio may be exposed to downside skew steepening, where out-of-the-money put implied volatility rises relative to at-the-money volatility.

Let the volatility surface shock be decomposed into factors:

$$
\Delta\boldsymbol{\sigma}
= a_0\mathbf{1}+a_1\mathbf{b}_{\text{skew}}+a_2\mathbf{b}_{\text{curvature}}+a_3\mathbf{b}_{\text{term}}+\boldsymbol{\eta}.
$$

Variables:

- $a_0$ is the parallel volatility shock coefficient;
- $a_1$ is the skew shock coefficient;
- $a_2$ is the curvature shock coefficient;
- $a_3$ is the term-structure shock coefficient;
- $\mathbf{b}_{\text{skew}}$, $\mathbf{b}_{\text{curvature}}$, and $\mathbf{b}_{\text{term}}$ are predefined surface shock basis vectors;
- $\boldsymbol{\eta}$ is residual shock not explained by the basis.

A skew hedge seeks to reduce P&L sensitivity to $a_1$, not merely total vega. This often requires options at different strikes.

## 3.10 Vanna and Volga Hedging Under Skewed Surfaces

## 3.10.1 Why Vega-Neutral Is Not Enough

A book can be vega-neutral and still lose money under a volatility shock because vega changes as spot and volatility change. The relevant approximation is:

$$
d\nu \approx \text{Vanna}\,dS+\text{Volga}\,d\sigma+\text{Veta}\,dt.
$$

If a portfolio has zero current vega but large positive or negative vanna and volga, its future vega after a spot or volatility move can become material.

## 3.10.2 Vanna Hedge

Portfolio vanna is:

$$
\text{Vanna}_p=\sum_{i=1}^{N}w_i\text{Vanna}_i.
$$

A vanna hedge using hedge option $j$ is approximately:

$$
w_j^{\text{hedge}}=-\frac{\text{Vanna}_p}{\text{Vanna}_j}.
$$

In practice, one usually hedges delta, vega, and vanna jointly using multiple hedge instruments:

$$
\min_{\mathbf{x}}\left\|
\begin{bmatrix}
\Delta_p \\
\nu_p \\
\text{Vanna}_p
\end{bmatrix}
+
\mathbf{A}\mathbf{x}
\right\|_2^2,
$$

where each column of $\mathbf{A}$ contains the delta, vega, and vanna exposures of one hedge instrument.

## 3.10.3 Volga Hedge

Portfolio volga is:

$$
\text{Volga}_p=\sum_{i=1}^{N}w_i\text{Volga}_i.
$$

A volga hedge controls curvature to volatility shocks. This is important for books that are close to vega-neutral but exposed to large volatility moves. Tail hedges, wing options, and long-dated options can have significant volga.

A joint vega-volga hedge can be formulated as:

$$
\min_{\mathbf{x}}\left\|
\begin{bmatrix}
\nu_p \\
\text{Volga}_p
\end{bmatrix}
+
\mathbf{A}\mathbf{x}
\right\|_2^2
+\lambda\mathbf{x}^{\top}\mathbf{C}\mathbf{x},
$$

where $\mathbf{C}$ may represent transaction-cost or liquidity penalties.

## 3.10.4 Surface-Aware Caveat

Under a skewed implied-volatility surface, vanna and volga hedging should not rely only on flat-vol Black-Scholes Greeks. A surface-aware delta is:

$$
\Delta_{\text{smile}}
=\Delta_{\text{flat}}+\nu\frac{\partial\sigma_{\text{imp}}}{\partial S}.
$$

A surface-aware gamma includes:

$$
\Gamma_{\text{smile}}
=\Gamma_{\text{flat}}
+2\text{Vanna}\frac{\partial\sigma_{\text{imp}}}{\partial S}
+\text{Volga}\left(\frac{\partial\sigma_{\text{imp}}}{\partial S}\right)^2
+\nu\frac{\partial^2\sigma_{\text{imp}}}{\partial S^2}.
$$

Thus vanna and volga become part of effective spot exposure when the volatility surface moves with spot.

## 3.11 Path Dependency in Hedged Option P&L

Delta-hedged P&L is path-dependent. Two underlying paths can start and end at the same price but generate different hedge P&L because the sequence of moves changes rebalancing trades.

For a long-gamma position:

- a choppy path with large alternating moves can produce positive gamma-scalping P&L;
- a smooth path with little realized variance may not offset theta decay;
- a large jump can create positive option value but may be difficult to hedge at expected prices;
- a one-directional trend can create hedge losses or gains depending on hedge timing and residual delta.

For a short-gamma position:

- low realized volatility can allow theta to dominate;
- choppy markets force repeated adverse hedge trades;
- gaps can produce losses that cannot be hedged continuously;
- liquidity can deteriorate exactly when hedge demand increases.

Path dependency means that average realized volatility alone is not enough. The distribution of returns, serial correlation, jump behavior, intraday path, and execution assumptions all matter.

## 3.12 Greek-Based P&L Decomposition

## 3.12.1 Local Decomposition

A practical daily P&L decomposition may use:

$$
\Delta V_t
\approx
\underbrace{\Delta_t\Delta S_t}_{\text{Delta P\&L}}
+\underbrace{\frac{1}{2}\Gamma_t(\Delta S_t)^2}_{\text{Gamma P\&L}}
+\underbrace{\theta_t\Delta t}_{\text{Theta carry}}
+\underbrace{\nu_t\Delta\sigma_t}_{\text{Vega P\&L}}
+\underbrace{\rho_t\Delta r_t}_{\text{Rate P\&L}}
+\underbrace{\text{Residual}_t}_{\text{Unexplained}}.
$$

For a portfolio:

$$
\Delta V_{p,t}
\approx
\sum_{i=1}^{N}w_{i,t}
\left[
\Delta_{i,t}\Delta S_{i,t}
+\frac{1}{2}\Gamma_{i,t}(\Delta S_{i,t})^2
+\theta_{i,t}\Delta t
+\nu_{i,t}\Delta\sigma_{i,t}
+\rho_{i,t}\Delta r_t
\right]
+\text{Residual}_{p,t}.
$$

The residual is not a garbage term. It is an important diagnostic. Large residuals may indicate:

- missing skew effects;
- missing term-structure effects;
- stale Greeks;
- poor implied-volatility marks;
- discrete dividends;
- early exercise effects;
- transaction costs;
- jumps;
- model misspecification;
- incorrect multipliers or corporate actions;
- data timestamp mismatch.

## 3.12.2 Delta P&L

Delta P&L is:

$$
\text{Delta P\&L}_t=\Delta_t\Delta S_t.
$$

For an option portfolio, delta P&L measures first-order directional exposure. A portfolio intended to be volatility-focused should monitor whether delta P&L dominates total P&L. If it does, the strategy may be unintentionally directional.

## 3.12.3 Gamma P&L

Gamma P&L is:

$$
\text{Gamma P\&L}_t=\frac{1}{2}\Gamma_t(\Delta S_t)^2.
$$

Gamma P&L is always positive for long gamma under small continuous spot moves and always negative for short gamma, before hedge costs and other effects. It is proportional to squared spot movement.

## 3.12.4 Theta Carry

Theta carry is:

$$
\text{Theta P\&L}_t=\theta_t\Delta t.
$$

Long options often have negative theta P&L. Short options often have positive theta P&L. But positive theta is compensation for assuming convexity and tail risk.

## 3.12.5 Vega P&L

Vega P&L is:

$$
\text{Vega P\&L}_t=\nu_t\Delta\sigma_t.
$$

If vega is quoted per one volatility point, then:

$$
\text{Vega P\&L}_t=\nu^{\text{1 vol point}}_t\Delta\sigma^{\text{vol points}}_t.
$$

A change from 20% to 23% implied volatility is $3$ volatility points or $0.03$ in decimal units.

## 3.12.6 Skew P&L

Skew P&L arises from changes in relative implied volatility across strikes. A simple linear skew factor can be represented as:

$$
\sigma_{\text{imp}}(k,T)=\sigma_{\text{ATM}}(T)+\beta_{\text{skew}}(T)k+\epsilon(k,T),
$$

where:

- $k=\ln(K/F_{t,T})$ is forward log-moneyness;
- $\beta_{\text{skew}}(T)$ is the skew slope for maturity $T$;
- $\epsilon(k,T)$ is residual surface curvature.

The approximate skew P&L for option $i$ is:

$$
\text{Skew P\&L}_{i,t}
\approx
\nu_{i,t}\,k_{i,t}\,\Delta\beta_{\text{skew},t}.
$$

This is a simplified factor approximation. A production system should use a calibrated surface shock engine and full repricing.

## 3.12.7 Financing P&L

Financing P&L includes the cost or income from cash balances, option premium funding, margin, collateral, and underlying hedge financing.

If $B_t$ is the cash account and $r^{\text{cash}}_t$ is the applicable cash rate, then:

$$
\text{Cash Financing P\&L}_t\approx B_t r^{\text{cash}}_t\Delta t.
$$

If a short stock hedge incurs borrow cost $b_t$, the borrow cost is approximately:

$$
\text{Borrow Cost}_t\approx |h_t^{-}|S_t b_t\Delta t,
$$

where $h_t^{-}=\min(h_t,0)$ is the short underlying position. For hard-to-borrow single stocks, borrow can materially affect option strategy economics.

## 3.13 Transaction Costs, Bid-Ask Spreads, Market Impact, and Slippage

## 3.13.1 Spread Cost

If an option has bid $B$ and ask $A$, the quoted mid is:

$$
M=\frac{A+B}{2}.
$$

The half-spread is:

$$
\text{HalfSpread}=\frac{A-B}{2}.
$$

Crossing the spread to buy costs approximately half the spread relative to mid. Crossing to sell also costs approximately half the spread relative to mid. For quantity $Q$ and multiplier $M_c$, option spread cost is approximately:

$$
\text{Spread Cost}\approx |Q|M_c\frac{A-B}{2}.
$$

Wide option spreads can dominate theoretical edge, especially in single-name options, far out-of-the-money options, long-dated options, and stressed markets.

## 3.13.2 Market Impact

A simple impact model is:

$$
\text{Impact Cost}_t = \eta S_t\left(\frac{|\Delta h_t|}{\text{ADV}_t}\right)^\alpha |\Delta h_t|,
$$

where:

- $\eta>0$ is an impact coefficient;
- $\text{ADV}_t$ is average daily volume of the hedge instrument;
- $\alpha$ is usually between $0.5$ and $1.0$ in stylized models;
- $|\Delta h_t|$ is the hedge trade size.

This is a simplified model. Real impact depends on intraday liquidity, urgency, market conditions, volatility, order type, venue, and crowding.

## 3.13.3 Slippage

Slippage is the difference between expected execution price and actual execution price. It may reflect:

- latency;
- market movement during execution;
- insufficient displayed liquidity;
- adverse selection;
- volatility spikes;
- poor order placement;
- trading during illiquid periods.

Slippage should be modeled conservatively in backtests. A strategy that survives only under mid-price execution is usually not institutional-grade.

## 3.14 Borrow Costs, Financing Costs, and Margin

## 3.14.1 Borrow Costs

Delta hedging with short stock may require borrowing shares. For single stocks, borrow cost can be high, unstable, or unavailable. If borrow cost is omitted, backtests may overstate profitability for strategies requiring short hedges.

Borrow cost over a period is approximately:

$$
\text{Borrow Cost}_{[t,t+\Delta t]}
= |h_t^{-}|S_t b_t\Delta t.
$$

where $b_t$ is the annualized borrow rate.

## 3.14.2 Financing Costs

Options require premium outlay or generate premium proceeds. Underlying hedges create cash balances. Margin requirements can tie up capital. A capital-aware return should be computed on economic capital, not simply option premium.

If a strategy uses margin $\mathcal{M}_t$, a margin-normalized return may be:

$$
R^{\text{margin}}_t=\frac{\Delta\Pi_t}{\mathcal{M}_t}.
$$

This differs from return on premium and return on notional.

## 3.14.3 Margin Procyclicality

Margin often rises during stress, precisely when short-volatility portfolios are losing money. This can force deleveraging at unfavorable prices. A risk system should stress both P&L and margin:

$$
\text{Available Liquidity}_t
=\text{Cash}_t+\text{Credit Capacity}_t-\text{Required Margin}_t.
$$

A strategy can be theoretically profitable over the full path but fail if interim margin demands exceed available liquidity.

## 3.15 Practical Hedging Instruments

Hedging instruments include:

| Risk | Common Hedge Instrument | Practical Issue |
|---|---|---|
| Delta | Underlying stock, ETF, future | Borrow, basis, trading hours, liquidity |
| Index delta | Index futures or ETFs | Futures basis, dividend assumptions |
| Vega | Options at similar maturity | Strike and surface basis risk |
| Term vega | Calendar spreads, variance swaps, VIX futures | Roll, convexity, settlement basis |
| Skew | Risk reversals, put spreads, collars | Strike liquidity and skew dynamics |
| Gamma | Options near target maturity and moneyness | Theta cost and liquidity |
| Rate risk | Rates futures, swaps, Treasury futures | Curve basis and collateral assumptions |
| FX risk | FX forwards or futures | Cross-currency funding and settlement |

A hedge instrument can reduce one risk while introducing another. For example, using an index option to hedge single-name vega introduces correlation and dispersion basis risk.

## 3.16 Failure Modes of Greek-Based Trading

Greek-based trading fails when the realized world differs from the local model in economically important ways.

| Failure Mode | Description | Typical Mitigation |
|---|---|---|
| Jump risk | Spot gaps before hedge can be adjusted | Gap scenarios, position limits, event filters |
| Volatility regime shift | Realized and implied vol rise abruptly | Regime-aware sizing, stress testing |
| Skew repricing | Downside IV rises faster than ATM IV | Skew shock scenarios |
| Liquidity evaporation | Spreads widen and depth disappears | Liquidity-adjusted sizing |
| Crowded unwind | Similar strategies hedge in same direction | Crowding indicators and conservative limits |
| Borrow squeeze | Short hedge becomes expensive or unavailable | Borrow constraints and hard-to-borrow filters |
| Model misspecification | Greeks do not reflect actual risk | Full repricing and model comparison |
| Over-hedging | Excessive turnover destroys edge | Cost-aware hedge thresholds |
| Under-hedging | Residual delta dominates P&L | Delta bands and stress limits |
| Margin spiral | Losses increase margin requirements | Liquidity and margin stress tests |

## 3.17 Python Code: Black-Scholes Building Blocks

The following code provides pricing and Greeks required for hedging simulations. The implementation uses continuous dividend yield and European options.

```python
import math
from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd
from scipy.stats import norm

OptionType = Literal["call", "put"]


@dataclass(frozen=True)
class BSMInputs:
    """Inputs for European Black-Scholes-Merton pricing.

    Rates and volatility are decimal annualized numbers.
    Time to maturity is measured in years.
    """

    spot: float
    strike: float
    tau: float
    rate: float
    dividend_yield: float
    volatility: float
    option_type: OptionType


def validate_inputs(x: BSMInputs) -> None:
    if x.spot <= 0 or not np.isfinite(x.spot):
        raise ValueError("spot must be positive and finite")
    if x.strike <= 0 or not np.isfinite(x.strike):
        raise ValueError("strike must be positive and finite")
    if x.tau <= 0 or not np.isfinite(x.tau):
        raise ValueError("tau must be positive and finite")
    if x.volatility <= 0 or not np.isfinite(x.volatility):
        raise ValueError("volatility must be positive and finite")
    if x.option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")


def d1_d2(x: BSMInputs) -> tuple[float, float]:
    validate_inputs(x)
    vol_sqrt_tau = x.volatility * math.sqrt(x.tau)
    d1 = (
        math.log(x.spot / x.strike)
        + (x.rate - x.dividend_yield + 0.5 * x.volatility**2) * x.tau
    ) / vol_sqrt_tau
    d2 = d1 - vol_sqrt_tau
    return d1, d2


def bsm_price(x: BSMInputs) -> float:
    d1, d2 = d1_d2(x)
    df_r = math.exp(-x.rate * x.tau)
    df_q = math.exp(-x.dividend_yield * x.tau)
    if x.option_type == "call":
        return x.spot * df_q * norm.cdf(d1) - x.strike * df_r * norm.cdf(d2)
    return x.strike * df_r * norm.cdf(-d2) - x.spot * df_q * norm.cdf(-d1)


def bsm_greeks(x: BSMInputs) -> dict[str, float]:
    """Return BSM price and core Greeks.

    Theta is annualized calendar-time theta, dV/dt.
    Vega is per 1.00 volatility unit, not per vol point.
    """
    d1, d2 = d1_d2(x)
    df_r = math.exp(-x.rate * x.tau)
    df_q = math.exp(-x.dividend_yield * x.tau)
    phi = norm.pdf(d1)
    sqrt_tau = math.sqrt(x.tau)

    gamma = df_q * phi / (x.spot * x.volatility * sqrt_tau)
    vega = x.spot * df_q * phi * sqrt_tau
    common_theta = -x.spot * df_q * phi * x.volatility / (2.0 * sqrt_tau)

    if x.option_type == "call":
        delta = df_q * norm.cdf(d1)
        theta = (
            common_theta
            - x.rate * x.strike * df_r * norm.cdf(d2)
            + x.dividend_yield * x.spot * df_q * norm.cdf(d1)
        )
        rho = x.strike * x.tau * df_r * norm.cdf(d2)
    else:
        delta = df_q * (norm.cdf(d1) - 1.0)
        theta = (
            common_theta
            + x.rate * x.strike * df_r * norm.cdf(-d2)
            - x.dividend_yield * x.spot * df_q * norm.cdf(-d1)
        )
        rho = -x.strike * x.tau * df_r * norm.cdf(-d2)

    return {
        "price": bsm_price(x),
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho,
    }
```

## 3.18 Python Code: Simulating Delta Hedging Under Different Realized Volatility Paths

This simulation compares delta-hedged P&L for a long option under different realized volatility assumptions. It uses synthetic paths and constant implied volatility for clarity.

```python
def simulate_gbm_paths(
    spot0: float,
    mu: float,
    realized_vol: float,
    years: float,
    steps: int,
    n_paths: int,
    seed: int = 42,
) -> np.ndarray:
    """Simulate geometric Brownian motion paths.

    Parameters
    ----------
    spot0:
        Initial spot price.
    mu:
        Annualized drift as decimal.
    realized_vol:
        Annualized realized volatility as decimal.
    years:
        Horizon in years.
    steps:
        Number of time steps.
    n_paths:
        Number of simulated paths.
    seed:
        Random seed for reproducibility.
    """
    if spot0 <= 0:
        raise ValueError("spot0 must be positive")
    if realized_vol < 0:
        raise ValueError("realized_vol must be nonnegative")
    if years <= 0 or steps <= 0 or n_paths <= 0:
        raise ValueError("years, steps, and n_paths must be positive")

    rng = np.random.default_rng(seed)
    dt = years / steps
    shocks = rng.normal(size=(n_paths, steps))
    log_returns = (mu - 0.5 * realized_vol**2) * dt + realized_vol * math.sqrt(dt) * shocks
    log_paths = np.cumsum(log_returns, axis=1)
    paths = spot0 * np.exp(np.column_stack([np.zeros(n_paths), log_paths]))
    return paths


def delta_hedge_one_path(
    spot_path: np.ndarray,
    strike: float,
    maturity_years: float,
    rate: float,
    dividend_yield: float,
    implied_vol: float,
    option_type: OptionType = "call",
    transaction_cost_bps: float = 0.0,
) -> pd.DataFrame:
    """Delta hedge one long option along a spot path.

    The position is long one option on one unit of underlying.
    The hedge is rebalanced at each path observation.
    Transaction cost is proportional to dollar value traded in the hedge.
    """
    if np.any(spot_path <= 0):
        raise ValueError("spot_path must contain positive prices")
    if maturity_years <= 0:
        raise ValueError("maturity_years must be positive")
    if transaction_cost_bps < 0:
        raise ValueError("transaction_cost_bps must be nonnegative")

    n_steps = len(spot_path) - 1
    dt = maturity_years / n_steps
    tc_rate = transaction_cost_bps / 10_000.0

    rows = []
    cash = 0.0
    hedge_units = 0.0

    # Buy option at initial model price.
    x0 = BSMInputs(
        spot=float(spot_path[0]),
        strike=strike,
        tau=maturity_years,
        rate=rate,
        dividend_yield=dividend_yield,
        volatility=implied_vol,
        option_type=option_type,
    )
    g0 = bsm_greeks(x0)
    option_price0 = g0["price"]
    cash -= option_price0

    # Initial hedge: short delta units of underlying for long option.
    target_hedge = -g0["delta"]
    trade_units = target_hedge - hedge_units
    trade_value = trade_units * spot_path[0]
    cash -= trade_value
    cash -= abs(trade_value) * tc_rate
    hedge_units = target_hedge

    previous_option_price = option_price0
    previous_greeks = g0

    for step in range(1, n_steps + 1):
        tau = max(maturity_years - step * dt, 1e-8)
        spot_prev = float(spot_path[step - 1])
        spot_now = float(spot_path[step])

        x_now = BSMInputs(
            spot=spot_now,
            strike=strike,
            tau=tau,
            rate=rate,
            dividend_yield=dividend_yield,
            volatility=implied_vol,
            option_type=option_type,
        )
        g_now = bsm_greeks(x_now)
        option_price_now = g_now["price"]

        option_pnl = option_price_now - previous_option_price
        hedge_pnl = hedge_units * (spot_now - spot_prev)

        # Rebalance hedge at current spot.
        target_hedge = -g_now["delta"]
        trade_units = target_hedge - hedge_units
        trade_value = trade_units * spot_now
        tc = abs(trade_value) * tc_rate
        cash -= trade_value
        cash -= tc
        hedge_units = target_hedge

        portfolio_value = option_price_now + hedge_units * spot_now + cash

        rows.append(
            {
                "step": step,
                "spot": spot_now,
                "tau": tau,
                "option_price": option_price_now,
                "delta": g_now["delta"],
                "gamma": g_now["gamma"],
                "theta": g_now["theta"],
                "vega": g_now["vega"],
                "option_pnl": option_pnl,
                "hedge_pnl_before_rebalance": hedge_pnl,
                "transaction_cost": tc,
                "portfolio_value": portfolio_value,
                "local_gamma_pnl_estimate": 0.5
                * previous_greeks["gamma"]
                * (spot_now - spot_prev) ** 2,
                "local_theta_estimate": previous_greeks["theta"] * dt,
            }
        )

        previous_option_price = option_price_now
        previous_greeks = g_now

    return pd.DataFrame(rows)


# Example experiment.
spot0 = 100.0
strike = 100.0
maturity = 30 / 365
implied_vol = 0.20
rate = 0.04
dividend_yield = 0.00
steps = 30

results = []
for rv in [0.10, 0.20, 0.35]:
    paths = simulate_gbm_paths(
        spot0=spot0,
        mu=0.0,
        realized_vol=rv,
        years=maturity,
        steps=steps,
        n_paths=100,
        seed=int(rv * 1000),
    )
    terminal_pnls = []
    for path in paths:
        hedge_df = delta_hedge_one_path(
            path,
            strike=strike,
            maturity_years=maturity,
            rate=rate,
            dividend_yield=dividend_yield,
            implied_vol=implied_vol,
            option_type="call",
            transaction_cost_bps=1.0,
        )
        terminal_pnls.append(hedge_df["portfolio_value"].iloc[-1])
    results.append(
        {
            "realized_vol": rv,
            "mean_terminal_pnl": float(np.mean(terminal_pnls)),
            "median_terminal_pnl": float(np.median(terminal_pnls)),
            "p05_terminal_pnl": float(np.percentile(terminal_pnls, 5)),
            "p95_terminal_pnl": float(np.percentile(terminal_pnls, 95)),
        }
    )

print(pd.DataFrame(results).round(6))
```

Expected interpretation:

- When realized volatility is below implied volatility, the delta-hedged long option tends to lose money before favorable vega effects.
- When realized volatility is near implied volatility, average P&L may be close to break-even before costs, but discrete hedging and costs matter.
- When realized volatility is above implied volatility, the long-gamma position tends to benefit, although path dependency remains material.

## 3.19 Python Code: Plotting Delta-Hedging Results

The following code plots a single hedged path and decomposes the daily local gamma and theta estimates. Each chart is separate.

```python
import matplotlib.pyplot as plt

# Generate one example path.
path = simulate_gbm_paths(
    spot0=100.0,
    mu=0.0,
    realized_vol=0.30,
    years=30 / 365,
    steps=30,
    n_paths=1,
    seed=7,
)[0]

hedge_df = delta_hedge_one_path(
    path,
    strike=100.0,
    maturity_years=30 / 365,
    rate=0.04,
    dividend_yield=0.00,
    implied_vol=0.20,
    option_type="call",
    transaction_cost_bps=1.0,
)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(hedge_df["step"], hedge_df["spot"])
ax.set_title("Underlying path")
ax.set_xlabel("Step")
ax.set_ylabel("Spot")
ax.grid(True)
plt.show()

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(hedge_df["step"], hedge_df["delta"])
ax.set_title("Option delta through time")
ax.set_xlabel("Step")
ax.set_ylabel("Delta")
ax.grid(True)
plt.show()

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(hedge_df["step"], hedge_df["portfolio_value"])
ax.set_title("Delta-hedged portfolio value")
ax.set_xlabel("Step")
ax.set_ylabel("Portfolio value")
ax.grid(True)
plt.show()

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(hedge_df["step"], hedge_df["local_gamma_pnl_estimate"].cumsum())
ax.set_title("Cumulative local gamma P&L estimate")
ax.set_xlabel("Step")
ax.set_ylabel("Cumulative gamma estimate")
ax.grid(True)
plt.show()

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(hedge_df["step"], hedge_df["local_theta_estimate"].cumsum())
ax.set_title("Cumulative local theta estimate")
ax.set_xlabel("Step")
ax.set_ylabel("Cumulative theta estimate")
ax.grid(True)
plt.show()
```

The charts are based on synthetic data. They should be used to understand mechanics, not to infer expected returns for any live market.

## 3.20 Python Code: Greek P&L Decomposition

The following function decomposes option P&L into delta, gamma, theta, vega, rho, and residual components using beginning-of-period Greeks.

```python
def decompose_option_pnl(
    observations: pd.DataFrame,
    strike: float,
    rate_col: str,
    dividend_yield_col: str,
    implied_vol_col: str,
    spot_col: str,
    tau_col: str,
    option_type: OptionType,
) -> pd.DataFrame:
    """Decompose option P&L using beginning-of-period BSM Greeks.

    The input DataFrame must be sorted by time and contain spot, tau, rate,
    dividend yield, and implied volatility columns. Rates and volatilities are
    decimal annualized values. Tau is in years.
    """
    required = [rate_col, dividend_yield_col, implied_vol_col, spot_col, tau_col]
    missing = [col for col in required if col not in observations.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if len(observations) < 2:
        raise ValueError("observations must contain at least two rows")

    df = observations.copy().reset_index(drop=True)

    prices = []
    greeks = []
    for _, row in df.iterrows():
        x = BSMInputs(
            spot=float(row[spot_col]),
            strike=strike,
            tau=max(float(row[tau_col]), 1e-8),
            rate=float(row[rate_col]),
            dividend_yield=float(row[dividend_yield_col]),
            volatility=float(row[implied_vol_col]),
            option_type=option_type,
        )
        g = bsm_greeks(x)
        prices.append(g["price"])
        greeks.append(g)

    gdf = pd.DataFrame(greeks)
    df["model_price"] = prices
    df = pd.concat([df, gdf.add_prefix("greek_")], axis=1)

    rows = []
    for i in range(len(df) - 1):
        row0 = df.iloc[i]
        row1 = df.iloc[i + 1]

        d_spot = row1[spot_col] - row0[spot_col]
        d_vol = row1[implied_vol_col] - row0[implied_vol_col]
        d_rate = row1[rate_col] - row0[rate_col]
        d_time = row0[tau_col] - row1[tau_col]  # elapsed time in years

        actual_pnl = row1["model_price"] - row0["model_price"]
        delta_pnl = row0["greek_delta"] * d_spot
        gamma_pnl = 0.5 * row0["greek_gamma"] * d_spot**2
        theta_pnl = row0["greek_theta"] * d_time
        vega_pnl = row0["greek_vega"] * d_vol
        rho_pnl = row0["greek_rho"] * d_rate
        explained = delta_pnl + gamma_pnl + theta_pnl + vega_pnl + rho_pnl
        residual = actual_pnl - explained

        rows.append(
            {
                "period": i,
                "actual_pnl": actual_pnl,
                "delta_pnl": delta_pnl,
                "gamma_pnl": gamma_pnl,
                "theta_pnl": theta_pnl,
                "vega_pnl": vega_pnl,
                "rho_pnl": rho_pnl,
                "explained_pnl": explained,
                "residual_pnl": residual,
                "d_spot": d_spot,
                "d_vol": d_vol,
                "d_rate": d_rate,
                "elapsed_time": d_time,
            }
        )

    return pd.DataFrame(rows)


# Synthetic example observations.
obs = pd.DataFrame(
    {
        "spot": [100.0, 101.0, 99.5, 102.0, 101.2],
        "tau": [30 / 365, 29 / 365, 28 / 365, 27 / 365, 26 / 365],
        "rate": [0.04, 0.0401, 0.0400, 0.0398, 0.0402],
        "dividend_yield": [0.00, 0.00, 0.00, 0.00, 0.00],
        "implied_vol": [0.20, 0.205, 0.215, 0.210, 0.200],
    }
)

decomp = decompose_option_pnl(
    obs,
    strike=100.0,
    rate_col="rate",
    dividend_yield_col="dividend_yield",
    implied_vol_col="implied_vol",
    spot_col="spot",
    tau_col="tau",
    option_type="call",
)
print(decomp.round(6))
print(decomp[["delta_pnl", "gamma_pnl", "theta_pnl", "vega_pnl", "rho_pnl", "residual_pnl"]].sum().round(6))
```

Expected interpretation:

- The residual should be small for small moves if the model and inputs are internally consistent.
- The residual grows when moves are large, Greeks change quickly, or important risk factors are omitted.
- In real data, residuals often reveal surface effects, data errors, transaction costs, and model misspecification.

## 3.21 Python Code: Cost-Aware Hedge Threshold Rule

A simple cost-aware hedging rule rebalances only when the absolute delta mismatch exceeds a threshold.

```python
def delta_band_hedge_one_path(
    spot_path: np.ndarray,
    strike: float,
    maturity_years: float,
    rate: float,
    dividend_yield: float,
    implied_vol: float,
    option_type: OptionType = "call",
    delta_band: float = 0.05,
    transaction_cost_bps: float = 1.0,
) -> pd.DataFrame:
    """Delta hedge only when hedge error exceeds a delta band.

    The hedge error is target hedge units minus current hedge units.
    For one option on one unit of underlying, a delta_band of 0.05 means
    the hedge is adjusted when hedge mismatch exceeds 0.05 underlying units.
    """
    if delta_band < 0:
        raise ValueError("delta_band must be nonnegative")

    n_steps = len(spot_path) - 1
    dt = maturity_years / n_steps
    tc_rate = transaction_cost_bps / 10_000.0
    cash = 0.0
    hedge_units = 0.0
    rows = []

    x0 = BSMInputs(
        spot=float(spot_path[0]),
        strike=strike,
        tau=maturity_years,
        rate=rate,
        dividend_yield=dividend_yield,
        volatility=implied_vol,
        option_type=option_type,
    )
    g0 = bsm_greeks(x0)
    cash -= g0["price"]
    target = -g0["delta"]
    trade = target - hedge_units
    cash -= trade * spot_path[0]
    cash -= abs(trade * spot_path[0]) * tc_rate
    hedge_units = target
    previous_option_price = g0["price"]

    for step in range(1, n_steps + 1):
        tau = max(maturity_years - step * dt, 1e-8)
        spot_now = float(spot_path[step])
        spot_prev = float(spot_path[step - 1])
        x_now = BSMInputs(
            spot=spot_now,
            strike=strike,
            tau=tau,
            rate=rate,
            dividend_yield=dividend_yield,
            volatility=implied_vol,
            option_type=option_type,
        )
        g_now = bsm_greeks(x_now)
        option_price_now = g_now["price"]
        hedge_pnl = hedge_units * (spot_now - spot_prev)

        target = -g_now["delta"]
        hedge_error = target - hedge_units
        did_trade = abs(hedge_error) > delta_band
        tc = 0.0
        trade = 0.0
        if did_trade:
            trade = hedge_error
            cash -= trade * spot_now
            tc = abs(trade * spot_now) * tc_rate
            cash -= tc
            hedge_units = target

        portfolio_value = option_price_now + hedge_units * spot_now + cash
        rows.append(
            {
                "step": step,
                "spot": spot_now,
                "delta": g_now["delta"],
                "target_hedge": target,
                "actual_hedge": hedge_units,
                "hedge_error_before_trade": hedge_error,
                "did_trade": did_trade,
                "trade_units": trade,
                "transaction_cost": tc,
                "option_pnl": option_price_now - previous_option_price,
                "hedge_pnl": hedge_pnl,
                "portfolio_value": portfolio_value,
            }
        )
        previous_option_price = option_price_now

    return pd.DataFrame(rows)
```

This threshold approach often reduces turnover but increases residual delta exposure. The optimal threshold is not universal. It depends on volatility, liquidity, spread, gamma, risk tolerance, and operational constraints.

## 3.22 Institutional Checklist for Hedging and Greek-Based Trading

| Area | Questions to Answer Before Deployment |
|---|---|
| Objective | Is the strategy seeking direction, carry, convexity, volatility, skew, or hedging utility? |
| Greek targets | What are the target and limit ranges for delta, gamma, theta, vega, vanna, and volga? |
| Hedge policy | Is hedging scheduled, threshold-based, volatility-aware, or cost-aware? |
| Cost model | Are spreads, commissions, impact, borrow, financing, and slippage included? |
| Surface risk | Are parallel vol, skew, curvature, and term-structure shocks tested? |
| Event risk | Are earnings, macro events, dividends, and corporate actions handled? |
| Liquidity | Are open interest, volume, spread, depth, and time-to-exit constraints modeled? |
| Margin | Are initial margin, variation margin, and stress margin included? |
| Attribution | Does P&L decomposition explain most P&L under normal conditions? |
| Residuals | Are unexplained P&L residuals monitored and escalated? |
| Stress testing | Are full repricing scenarios used for large moves? |
| Governance | Are model versions, data timestamps, and hedge decisions auditable? |

## 3.23 Summary of Part 3

Part 3 connected Greeks to practical hedging, trading, and P&L mechanics.

Key points:

1. Delta hedging offsets local first-order spot exposure but does not eliminate risk.
2. A delta-hedged option's local P&L is driven by gamma, theta, vega, and residual effects.
3. Long gamma tends to buy low and sell high through hedge rebalancing, but it pays theta.
4. Short gamma earns theta but loses from large realized movement and adverse hedging.
5. Gamma scalping profitability depends on realized volatility, implied volatility, hedge frequency, and transaction costs.
6. Continuous hedging is unrealistic; discrete hedging error is central to real P&L.
7. Vega hedging must consider term-structure and skew basis, not only total vega.
8. Vanna and volga explain why vega-neutral and delta-neutral books can become exposed after spot or volatility moves.
9. P&L decomposition should include delta, gamma, theta, vega, skew, financing, transaction costs, and residuals.
10. Residual P&L is a diagnostic signal, not an accounting nuisance.
11. Transaction costs, bid-ask spreads, market impact, borrow, financing, and margin can dominate theoretical edge.
12. Robust option strategy research requires path-based simulation, cost-aware hedging rules, full repricing stress tests, and careful attribution.

The next installment will cover Part 4: Volatility Surface, Skew, Term Structure, and Regime Interpretation.
