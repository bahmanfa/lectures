# Institutional Options Greeks, Systematic Strategy, and Regime-Aware Portfolio Construction Curriculum

## Completed Installment

This installment contains:

1. Global assumptions.
2. Part 0: Executive Overview and Learning Roadmap.
3. Part 1: Foundations: Option Pricing and Core Greeks.

The document is educational and research-oriented. It is not personalized investment advice, a live trading recommendation, or a claim that any option strategy produces guaranteed alpha.

---

# 1. Global Assumptions

This curriculum uses a deliberately explicit modeling convention. Real-world institutional options research often requires changing these assumptions, validating the impact, and documenting the difference between theoretical Greeks, vendor Greeks, portfolio Greeks, and realized P&L sensitivities.

## 1.1 Option Exercise Style

Unless stated otherwise, the baseline mathematical treatment assumes **European options**, meaning the option can be exercised only at maturity $T$.

This assumption is used because the Black-Scholes-Merton closed-form pricing formulas and the closed-form Greeks in Part 1 apply directly to European calls and puts under a lognormal diffusion with continuous trading and constant parameters.

For **American options**, early exercise can matter, especially for:

- deep-in-the-money calls on dividend-paying equities near ex-dividend dates;
- deep-in-the-money puts when rates are material;
- single-stock options with discrete dividends;
- options affected by hard-to-borrow conditions, special dividends, or corporate actions.

For **Bermudan options**, exercise is allowed on a finite set of dates. For **American** and **Bermudan** contracts, lattice methods, finite-difference PDE solvers, Longstaff-Schwartz Monte Carlo, or specialized approximations may be required.

Throughout Part 1, when the text says “option” without qualification, it refers to a European option unless the context explicitly discusses implementation caveats.

## 1.2 Underlying Asset and Dividends

Let $S_t$ denote the underlying spot price at time $t$ and $K$ the strike price. The baseline model assumes a continuous dividend yield $q$, so the risk-neutral dynamics are:

$$
\frac{dS_t}{S_t} = (r - q)dt + \sigma dW_t^{\mathbb{Q}},
$$

where:

- $r$ is the continuously compounded risk-free rate, expressed as a decimal annual rate;
- $q$ is the continuously compounded dividend yield, expressed as a decimal annual rate;
- $\sigma$ is volatility, expressed as a decimal annualized volatility;
- $W_t^{\mathbb{Q}}$ is a Brownian motion under the risk-neutral measure $\mathbb{Q}$;
- $dt$ is measured in years.

For index and ETF options, dividends may be approximated using a continuous yield, embedded into a forward price, or modeled using a discrete dividend schedule. For single-stock options, discrete dividends and corporate actions can materially affect pricing and early exercise incentives. A production system should store dividend assumptions point-in-time, not overwrite history with revised dividend forecasts.

The forward price under continuous yield is:

$$
F_{t,T} = S_t e^{(r-q)\tau},
$$

where $\tau = T-t$ is time to maturity in years. The interpretation is that $F_{t,T}$ is the no-arbitrage forward price for delivery at $T$, assuming deterministic $r$ and $q$ over $[t,T]$.

## 1.3 Interest Rates

The baseline derivations assume a constant continuously compounded risk-free rate $r$ over the option maturity. In institutional systems, $r$ is usually term-structured and may be represented by an overnight indexed swap curve, Treasury curve, collateral curve, funding curve, or currency-specific discount curve.

In a term-structured deterministic-rate setting, the discount factor is:

$$
D(t,T) = e^{-\int_t^T r_u du},
$$

where $r_u$ is the instantaneous forward risk-free rate at time $u$. Under a constant rate $r$, this simplifies to:

$$
D(t,T) = e^{-r\tau}.
$$

Part 1 uses the constant-rate version for analytical clarity.

## 1.4 Volatility Assumption

Part 1 assumes a constant volatility $\sigma$ in the Black-Scholes-Merton model. This is a modeling idealization, not a description of real option markets.

In practice, volatility may be:

- **realized volatility**, estimated from historical underlying returns;
- **implied volatility**, inferred from option market prices;
- **local volatility**, where volatility depends on spot and time, $\sigma = \sigma(S,t)$;
- **stochastic volatility**, where volatility is itself a random process;
- **jump-driven**, where discontinuous price jumps affect option values;
- **surface-implied**, where market quotes define a cross-section across strikes and maturities.

The distinction matters because Black-Scholes Greeks are sensitivities under a flat-volatility assumption. Actual desk risk is often computed with surface-aware assumptions such as sticky strike, sticky delta, sticky moneyness, local-vol, or vendor-specific surface dynamics.

## 1.5 Greek Definitions and Measurement

Greeks are **partial derivatives** or higher-order sensitivities of an option value function. They are not standalone PDEs. The Black-Scholes-Merton PDE describes the dynamic no-arbitrage condition for the option value; Greeks are derivatives of the option value with respect to state variables or parameters.

This installment distinguishes among:

| Greek Type | Meaning | Typical Use | Key Limitation |
|---|---|---|---|
| Analytical Greeks | Closed-form derivatives under a model such as Black-Scholes-Merton | Teaching, fast risk checks, benchmark calculations | Depend on restrictive assumptions |
| Model-implied Greeks | Sensitivities from a pricing model calibrated to a volatility surface | Desk risk, scenario risk, portfolio analytics | Depend on model and surface dynamics |
| Vendor Greeks | Greeks reported by brokers or data vendors | Operations, monitoring, reconciliation | Methodology may be opaque |
| Finite-difference Greeks | Repricing-based sensitivities under small shocks | Flexible across complex products | Sensitive to bump size and numerical noise |
| Scenario Greeks | Sensitivities under specified large shocks | Stress testing and risk limits | Not local derivatives |
| Realized portfolio sensitivities | Ex-post P&L response to realized market moves | Performance attribution and model validation | Includes residual effects, costs, slippage, and model error |

Unless otherwise stated, Part 1 uses **analytical spot Greeks** under Black-Scholes-Merton.

## 1.6 Hedging Assumption

The Black-Scholes-Merton derivation assumes continuous trading, frictionless markets, no transaction costs, no bid-ask spreads, unlimited shorting, no funding constraints, and continuous rebalancing of the underlying hedge. These assumptions are not realistic.

In practice, hedging may be:

- continuous only as a theoretical ideal;
- discrete, such as daily, intraday, or event-driven;
- threshold-based, such as rehedging when absolute delta exceeds a limit;
- transaction-cost constrained;
- liquidity constrained;
- margin constrained;
- operationally constrained by execution windows and risk limits.

The difference between continuous and discrete hedging is central to option P&L. A short-gamma position can look stable under small moves and then experience nonlinear losses during jumps, gaps, and liquidity stress.

## 1.7 Transaction Costs, Financing, Borrow, and Margin

Unless stated otherwise in formulas, Part 1 excludes:

- bid-ask spreads;
- commissions and exchange fees;
- market impact;
- slippage;
- stock borrow costs;
- hard-to-borrow constraints;
- financing spreads;
- margin requirements;
- collateral haircuts;
- taxes;
- early assignment and exercise frictions.

These omissions are acceptable for foundational theory but unacceptable for production strategy evaluation. Later parts of the curriculum connect Greeks to transaction-cost-aware hedging, margin-aware portfolio construction, and implementation feasibility.

## 1.8 Portfolio Exposure Units

Option exposures can be measured in several ways. The same strategy can look small or large depending on the unit convention.

Common conventions include:

| Exposure Unit | Definition | Example Use |
|---|---|---|
| Per-contract exposure | Greek per listed option contract | Trade ticket checks |
| Per-option exposure | Greek per one option on one share/unit | Model formulas |
| Dollar notional | Exposure scaled by underlying price and contract multiplier | Portfolio aggregation |
| Delta-adjusted notional | $\Delta \times S \times \text{multiplier}$ | Directional exposure |
| Beta-adjusted delta | Delta adjusted by equity beta or macro factor beta | Cross-asset risk aggregation |
| Vega dollars | P&L change for a 1 volatility point move | Volatility risk limits |
| Risk units | Exposure normalized by forecast volatility, expected shortfall, margin, or risk budget | Portfolio construction |

Throughout Part 1, formulas are written per one option on one unit of the underlying unless otherwise stated. A listed U.S. equity option contract typically has a multiplier of 100 shares, so production risk must multiply per-option Greeks by contract quantity and contract multiplier.

## 1.9 Asset Class Scope

The framework is designed to be extendable across:

- index options;
- ETF options;
- single-stock options;
- futures options;
- FX options;
- rates options;
- commodity options;
- variance and volatility derivatives.

Part 1 focuses on equity-style European options with continuous dividend yield. Single-stock implementation requires additional treatment of earnings, corporate actions, borrow, takeover risk, event gaps, liquidity, and idiosyncratic jumps.

## 1.10 Educational, Research, and Production Orientation

This curriculum has three layers:

1. **Educational layer:** explain pricing theory, Greeks, intuition, and limitations.
2. **Research layer:** connect Greeks to systematic signals, regime detection, risk premia, and backtesting.
3. **Production layer:** specify data, validation, controls, monitoring, exception handling, and scalable portfolio infrastructure.

Part 1 emphasizes the educational layer while introducing the language required for later research and production layers.

---

# Part 0: Executive Overview and Learning Roadmap

## 0.1 Purpose of Options Greeks

Options are nonlinear claims. Their value depends not only on the current underlying price but also on strike, time to maturity, volatility, interest rates, dividends, funding conditions, market microstructure, and the probability distribution of future outcomes.

A stock position has a mostly linear first-order exposure to price. An option position has a changing exposure profile. If the underlying rises, the option delta changes. If time passes, theta changes. If implied volatility shifts, vega changes. If skew steepens, the sensitivity of the option to volatility may depend on moneyness and surface dynamics. This makes options fundamentally dynamic instruments.

Greeks provide a structured language for measuring these dynamics. They answer questions such as:

- How much does the option value change if the underlying moves?
- How fast does that directional exposure change?
- How much value is lost or earned from the passage of time?
- How sensitive is the option to implied volatility?
- How sensitive is the option to interest rates or dividends?
- How does the risk profile change across moneyness, maturity, and volatility regimes?
- What happens to portfolio risk if spot, volatility, skew, rates, and liquidity move together?

The core Greeks are:

| Greek | Sensitivity | High-Level Interpretation |
|---|---|---|
| Delta $\Delta$ | $\partial V / \partial S$ | Directional exposure to the underlying |
| Gamma $\Gamma$ | $\partial^2 V / \partial S^2$ | Curvature or convexity of the option value with respect to spot |
| Theta $\Theta$ | $\partial V / \partial t$ or $-\partial V/\partial \tau$ | Time decay or time carry |
| Vega $\nu$ | $\partial V / \partial \sigma$ | Sensitivity to implied volatility |
| Rho $\rho$ | $\partial V / \partial r$ | Sensitivity to interest rates |

Here $V$ is the option value, $S$ is the underlying spot price, $t$ is calendar time, $\tau=T-t$ is time to maturity, $\sigma$ is volatility, and $r$ is the risk-free rate.

The practical role of Greeks differs by function:

| Function | Role of Greeks | Example Question |
|---|---|---|
| Pricing | Link model value to market value | Is implied volatility rich or cheap relative to assumptions? |
| Hedging | Translate option risk into hedge trades | How many shares hedge this option portfolio? |
| Trading | Express views on direction, volatility, skew, carry, or jumps | Is the portfolio long realized volatility or short implied volatility? |
| Risk Management | Define limits, scenarios, and kill-switches | What happens if spot falls 5% and implied volatility rises 10 vol points? |
| Portfolio Construction | Allocate Greek exposures across strategies and regimes | How much gamma and vega should be held in a rising-volatility regime? |
| Research Engineering | Compute, store, validate, and monitor sensitivities | Are Greeks reproducible point-in-time and stable across data revisions? |

## 0.2 Greeks Are Dynamic State Variables, Not Static Textbook Numbers

A common beginner mistake is to treat a Greek as a fixed property of an option. Greeks are better understood as state variables that evolve as market conditions change.

For a European option value function:

$$
V = V(S,t,K,T,r,q,\sigma),
$$

the Greeks are local derivatives evaluated at the current state. If the state changes, the Greeks change.

For example, an at-the-money option with a delta near $0.50$ may become deep-in-the-money after a large spot rally. Its delta may rise toward $1.00$, its gamma may decline, and its theta may change. A short-dated at-the-money option can have high gamma because a small spot move can materially change the probability of finishing in-the-money. A long-dated option may have more vega because its value depends more heavily on assumptions about volatility over a longer horizon.

Greeks are also affected by the volatility surface. Two options with the same Black-Scholes delta can have different risk profiles if one is short-dated and near an earnings event while another is long-dated and exposed to broad market volatility. A model that assumes flat volatility may report a similar delta for both, but realized P&L may differ because volatility, skew, liquidity, and event risk move differently.

Thus Greeks should be treated as a dynamic risk vector:

$$
\mathbf{g}_t =
\begin{bmatrix}
\Delta_t \\
\Gamma_t \\
\Theta_t \\
\nu_t \\
\rho_t \\
\text{higher-order Greeks}_t
\end{bmatrix},
$$

where $\mathbf{g}_t$ changes with spot, time, volatility, rates, dividends, surface shape, and portfolio composition.

The institutional implication is direct: risk systems should not merely calculate Greeks once at trade entry. They should recalculate, store, explain, and monitor Greeks over time, across scenarios, and across risk buckets.

## 0.3 How Greeks Connect Microstructure, Volatility Surfaces, Macro Regimes, and Portfolio Risk

Options sit at the intersection of several layers of market structure.

### 0.3.1 Option Microstructure

Option quotes are affected by bid-ask spreads, market maker inventory, open interest, market depth, exercise style, settlement, contract multiplier, and trading hours. A quoted option can appear attractive by model value but be unusable after transaction costs and slippage.

Microstructure matters for Greeks because:

- delta hedges require trading the underlying;
- gamma scalping profitability depends on hedge frequency and transaction costs;
- vega exposures may be hard to exit in illiquid maturities;
- deep out-of-the-money options may have unreliable implied volatility marks;
- stale quotes can create false signals;
- bid-ask spread can dominate theoretical edge.

### 0.3.2 Volatility Surface

The implied volatility surface maps implied volatility across strike and maturity:

$$
\sigma_{\text{imp}} = \sigma_{\text{imp}}(K,T).
$$

It may also be represented by moneyness, log-moneyness, delta, or forward moneyness. Surface shape contains information about market pricing of downside risk, upside risk, jumps, event risk, demand for protection, supply of yield-enhancing trades, and dealer inventory.

Greeks computed under a flat-vol model do not fully capture surface risk. A portfolio may be delta-neutral and vega-neutral under a flat-vol assumption but still exposed to:

- skew steepening;
- skew flattening;
- term-structure twists;
- vol-of-vol shocks;
- local volatility effects;
- event volatility repricing;
- correlation shocks.

### 0.3.3 Macro and Cross-Asset Regimes

Macro regimes affect option risk premia through changes in growth, inflation, liquidity, credit stress, funding conditions, and risk appetite. Examples include:

- **risk-on liquidity expansion:** short-volatility carry may perform until crowding or complacency builds;
- **growth slowdown:** defensive skew demand may increase;
- **inflation shock:** rate and equity volatility may rise together;
- **credit stress:** downside skew and index volatility may reprice sharply;
- **post-shock normalization:** implied volatility may remain elevated while realized volatility declines, creating carry opportunities but with gap risk.

A regime-aware options process should not say “always sell volatility” or “always buy convexity.” Instead, it should estimate probabilities across regimes and map those probabilities to Greek budgets and strategy weights.

### 0.3.4 Portfolio Risk

At the portfolio level, Greeks are risk factors. A portfolio may contain options across many underlyings, sectors, countries, maturities, and strategies. Aggregation requires consistent units.

For a portfolio with positions $w_i$ in options $i=1,\ldots,N$, a generic portfolio Greek is:

$$
G_{p} = \sum_{i=1}^{N} w_i G_i,
$$

where:

- $G_p$ is the portfolio Greek exposure;
- $G_i$ is the Greek of option $i$ in the chosen unit convention;
- $w_i$ is the position size, including contract quantity and multiplier.

This simple summation becomes more complex when exposures are bucketed by underlying, sector, maturity, strike, delta, currency, volatility tenor, or factor mapping. Later parts develop this into Greek exposure matrices and constrained optimization.

## 0.4 Valuation, Hedging, Alpha Research, and Portfolio Construction Are Different Tasks

Options research often becomes confused when valuation, hedging, alpha research, and portfolio construction are treated as the same problem. They are related but distinct.

## 0.4.1 Option Valuation

Valuation asks: **what is the option worth under a pricing model and assumptions?**

For example, under Black-Scholes-Merton, the value is determined by spot, strike, time, rate, dividend yield, and volatility. If market price differs from model price, the difference may reflect a wrong model, wrong inputs, transaction costs, true mispricing, liquidity premium, jump risk, or market supply-demand imbalance.

Valuation is not alpha by itself. A model can say an option is expensive while the option remains expensive or becomes more expensive during stress.

## 0.4.2 Hedging

Hedging asks: **how do we reduce or transform unwanted risk exposures?**

Delta hedging uses the underlying to offset first-order directional risk. Vega hedging uses other options or volatility instruments to offset volatility exposure. Skew hedging uses options at different strikes. Term-structure hedging uses options at different maturities.

Hedging is not free. It introduces transaction costs, funding costs, operational complexity, residual risk, and model risk. A hedge can reduce one Greek while increasing another.

## 0.4.3 Alpha Research

Alpha research asks: **which risks are compensated, under what conditions, and after costs?**

Possible option-related risk premia include:

- volatility risk premium;
- skew risk premium;
- jump risk premium;
- correlation risk premium;
- liquidity premium;
- funding premium;
- convexity supply-demand imbalance;
- event volatility mispricing;
- term-structure roll-down.

However, expected return should be separated from risk exposure. A short-volatility strategy can generate positive average returns because it sells insurance, but it may have severe negative skewness and crash exposure. A long-gamma strategy can lose carry for extended periods but provide convexity during large realized moves.

## 0.4.4 Portfolio Construction

Portfolio construction asks: **how should exposures be sized and combined under expected return, risk, cost, margin, liquidity, and regime constraints?**

An institutional options portfolio may combine:

- long gamma overlays;
- short volatility carry;
- collars;
- calendar spreads;
- dispersion trades;
- skew trades;
- earnings-event trades;
- tail-risk hedges;
- volatility term-structure strategies.

Each sleeve contributes expected return, Greek exposures, tail risks, transaction costs, and margin usage. The objective is not merely to choose attractive trades, but to allocate exposures coherently across states of the world.

## 0.5 Roadmap from Basic Greeks to Systematic Regime-Aware Options Strategies

This curriculum is organized as a progression from local option sensitivities to portfolio-level regime-aware allocation.

| Part | Focus | Institutional Skill Developed |
|---|---|---|
| Part 0 | Executive overview and learning roadmap | Understand why Greeks matter beyond textbook formulas |
| Part 1 | Pricing foundations and core Greeks | Compute and interpret Black-Scholes-Merton Greeks |
| Part 2 | Higher-order Greeks and surfaces | Understand Greek instability and surface-aware risk |
| Part 3 | Hedging and trading dynamics | Decompose P&L and understand discrete hedging economics |
| Part 4 | Volatility surface and regimes | Connect skew, term structure, and volatility shocks to risk |
| Part 5 | Systematic options alpha | Translate Greeks into strategy families and signals |
| Part 6 | Regime-aware selection | Use regime probabilities to allocate across strategy sleeves |
| Part 7 | Portfolio construction | Treat Greeks as constraints and risk factors |
| Part 8 | Covariance and risk stabilization | Clean unstable risk estimates and control optimization error |
| Part 9 | Stress testing and failure modes | Evaluate nonlinear losses and tail events |
| Part 10 | Research pipeline and backtesting | Build point-in-time, bias-controlled options infrastructure |
| Part 11 | Case studies | Apply the framework to realistic strategy examples |
| Part 12 | Summary and reference manual | Consolidate formulas, checklists, and implementation rules |

The immediate goal of Part 1 is to build a reliable foundation. Without precise definitions of payoff, moneyness, implied volatility, and core Greeks, later topics such as vanna, volga, gamma scalping, skew carry, dispersion, and Greek-constrained optimization become fragile.

---

# Part 1: Foundations: Option Pricing and Core Greeks

## 1.1 Basic Option Contracts

An option is a derivative contract whose payoff depends on the value of an underlying asset. The two basic option types are calls and puts.

A **call option** gives the holder the right, but not the obligation, to buy the underlying at strike price $K$ at or before the allowed exercise date, depending on exercise style.

A **put option** gives the holder the right, but not the obligation, to sell the underlying at strike price $K$ at or before the allowed exercise date.

For a European option expiring at $T$, define:

- $S_T$: underlying price at maturity;
- $K$: strike price;
- $C_T$: call payoff at maturity;
- $P_T$: put payoff at maturity.

The European call payoff is:

$$
C_T = \max(S_T-K,0) = (S_T-K)^+,
$$

where $(x)^+ = \max(x,0)$. The payoff is positive only when $S_T>K$.

The European put payoff is:

$$
P_T = \max(K-S_T,0) = (K-S_T)^+.
$$

The payoff is positive only when $S_T<K$.

These payoff equations define terminal cash flows, not the option value before maturity. Before maturity, the option value includes both intrinsic value and time value.

## 1.2 Intrinsic Value and Time Value

For a call option at time $t$, the intrinsic value is:

$$
\text{Intrinsic Value}_{\text{call}} = \max(S_t-K,0).
$$

For a put option at time $t$, the intrinsic value is:

$$
\text{Intrinsic Value}_{\text{put}} = \max(K-S_t,0).
$$

The time value is the difference between the option price and intrinsic value:

$$
\text{Time Value} = V_t - \text{Intrinsic Value},
$$

where $V_t$ is the option price at time $t$.

Time value reflects the possibility that future underlying moves create additional payoff before expiration. A zero-intrinsic-value out-of-the-money option can have positive value because it may finish in-the-money by maturity.

Time value is affected by:

- time to maturity;
- volatility;
- interest rates;
- dividends;
- skew and surface shape;
- event risk;
- supply and demand;
- transaction costs and liquidity.

## 1.3 Moneyness, Log-Moneyness, and Forward Moneyness

Moneyness describes the relationship between spot or forward price and strike.

### 1.3.1 Spot Moneyness

Spot moneyness may be defined as:

$$
M_S = \frac{S_t}{K}.
$$

Interpretation:

- $M_S>1$: spot is above strike;
- $M_S=1$: spot equals strike;
- $M_S<1$: spot is below strike.

For calls, $M_S>1$ means in-the-money. For puts, $M_S<1$ means in-the-money.

### 1.3.2 Log-Moneyness

Log-moneyness is:

$$
k = \ln\left(\frac{K}{S_t}\right).
$$

Some practitioners instead define log-moneyness as $\ln(S_t/K)$. The sign convention must be documented. In this curriculum, unless otherwise stated, $k=\ln(K/S_t)$.

Log-moneyness is useful because log returns are central in lognormal models, and strike grids are often more stable when expressed in log space.

### 1.3.3 Forward Moneyness

Forward moneyness uses the forward price:

$$
M_F = \frac{F_{t,T}}{K},
$$

where, under continuous yield:

$$
F_{t,T}=S_t e^{(r-q)\tau}.
$$

Forward log-moneyness is:

$$
k_F = \ln\left(\frac{K}{F_{t,T}}\right).
$$

Forward moneyness is often preferable for volatility-surface work because it accounts for rates, dividends, and carry over the option horizon. Two options with the same spot moneyness but different maturities may have different forward moneyness if rates or dividends are material.

## 1.4 Discount Factor, Dividend Yield, Implied Volatility, and Realized Volatility

### 1.4.1 Discount Factor

The constant-rate discount factor from maturity $T$ to time $t$ is:

$$
D(t,T)=e^{-r\tau}.
$$

Variables:

- $D(t,T)$: present value of one unit paid at $T$;
- $r$: continuously compounded annual risk-free rate;
- $\tau=T-t$: time to maturity in years.

If $r=0.04$ and $\tau=0.5$, then $D(t,T)=e^{-0.02}$.

### 1.4.2 Dividend Yield

A continuous dividend yield $q$ reduces the expected risk-neutral growth rate of the underlying from $r$ to $r-q$. The present value of expected continuous dividend carry is embedded through $e^{-q\tau}$ in the Black-Scholes-Merton formula.

For single stocks, discrete dividend modeling may be more appropriate. Treating a large known discrete dividend as a smooth continuous yield can distort early exercise logic and near-dividend option values.

### 1.4.3 Implied Volatility

Implied volatility $\sigma_{\text{imp}}$ is the volatility input that makes a pricing model match the observed market option price.

Formally, for a market call price $C^{\text{mkt}}$, implied volatility solves:

$$
C^{\text{BSM}}(S_t,K,\tau,r,q,\sigma_{\text{imp}}) = C^{\text{mkt}}.
$$

Variables:

- $C^{\text{BSM}}$: Black-Scholes-Merton model call price;
- $C^{\text{mkt}}$: observed market call price;
- $\sigma_{\text{imp}}$: implied volatility.

Implied volatility is not a direct forecast of realized volatility. It is a model-implied transformation of option price that includes expected volatility, risk premia, jump risk, demand for convexity, liquidity, funding, and model error.

### 1.4.4 Realized Volatility

Realized volatility is estimated from historical returns. If $r_i$ are daily log returns over $n$ days, daily realized variance is:

$$
\widehat{\sigma}_{\text{daily}}^2 = \frac{1}{n-1}\sum_{i=1}^{n}(r_i-\bar r)^2,
$$

where $\bar r$ is the sample mean daily log return. Annualized realized volatility is often estimated as:

$$
\widehat{\sigma}_{\text{ann}} = \sqrt{252}\,\widehat{\sigma}_{\text{daily}},
$$

assuming 252 trading days per year. This convention should be documented. For intraday, weekly, or calendar-day data, the annualization factor changes.

## 1.5 Black-Scholes-Merton Model Assumptions

The Black-Scholes-Merton model provides a foundational no-arbitrage pricing framework. Its assumptions are powerful but restrictive.

The baseline assumptions are:

1. The underlying follows a geometric Brownian motion under the risk-neutral measure:

   $$
   \frac{dS_t}{S_t}=(r-q)dt+\sigma dW_t^{\mathbb{Q}}.
   $$

2. The risk-free rate $r$ is constant and known.
3. The dividend yield $q$ is continuous, constant, and known.
4. Volatility $\sigma$ is constant and known.
5. Markets are frictionless: no transaction costs, taxes, bid-ask spreads, or market impact.
6. Trading is continuous.
7. Short-selling is allowed without constraints.
8. There are no arbitrage opportunities.
9. The underlying price path is continuous, with no jumps.
10. The option is European.

These assumptions imply a complete market in which the option can be replicated by dynamically trading the underlying and the risk-free asset. Real markets violate these assumptions in many ways. The model remains important because it provides a common language for implied volatility and Greeks.

## 1.6 The Black-Scholes-Merton PDE

Let $V(S,t)$ be the value of a European derivative as a function of spot price $S$ and time $t$. Under the Black-Scholes-Merton assumptions with continuous dividend yield $q$, the option value satisfies:

$$
\frac{\partial V}{\partial t}
+ (r-q)S\frac{\partial V}{\partial S}
+ \frac{1}{2}\sigma^2 S^2\frac{\partial^2 V}{\partial S^2}
- rV = 0.
$$

Variables and terms:

- $V(S,t)$: option value at spot $S$ and time $t$;
- $\partial V/\partial t$: sensitivity to calendar time;
- $\partial V/\partial S$: first derivative with respect to spot, later called delta;
- $\partial^2V/\partial S^2$: second derivative with respect to spot, later called gamma;
- $r$: risk-free rate;
- $q$: dividend yield;
- $\sigma$: volatility;
- $S$: spot price.

Interpretation: the PDE is the no-arbitrage condition that arises because the option can be replicated by a self-financing portfolio of the underlying and the risk-free asset under the model assumptions.

The terminal condition for a European call is:

$$
V(S,T)=\max(S-K,0).
$$

The terminal condition for a European put is:

$$
V(S,T)=\max(K-S,0).
$$

Greeks appear in the PDE because delta and gamma are derivatives of the option value. But the Greeks themselves are not PDEs.

## 1.7 Black-Scholes-Merton European Call and Put Formulas

Define time to maturity:

$$
\tau=T-t.
$$

Assume $\tau>0$, $S>0$, $K>0$, and $\sigma>0$. Define:

$$
d_1 = \frac{\ln(S/K)+(r-q+\frac{1}{2}\sigma^2)\tau}{\sigma\sqrt{\tau}},
$$

and:

$$
d_2 = d_1 - \sigma\sqrt{\tau}.
$$

Let $N(x)$ denote the standard normal cumulative distribution function and $\phi(x)$ denote the standard normal probability density function:

$$
\phi(x)=\frac{1}{\sqrt{2\pi}}e^{-x^2/2}.
$$

The European call price with continuous dividend yield is:

$$
C = S e^{-q\tau}N(d_1)-K e^{-r\tau}N(d_2).
$$

The European put price is:

$$
P = K e^{-r\tau}N(-d_2)-S e^{-q\tau}N(-d_1).
$$

Interpretation:

- $S e^{-q\tau}N(d_1)$ is the dividend-adjusted underlying exposure term for the call;
- $K e^{-r\tau}N(d_2)$ is the discounted strike-payment term for the call;
- $N(d_1)$ is related to the option's hedge ratio under the model;
- $N(d_2)$ is related to the risk-neutral probability of finishing in-the-money under the model, though it should not be casually interpreted as a real-world probability.

The formulas are model prices, not guarantees of fair value in a broader economic sense.

## 1.8 Put-Call Parity

For European options with the same $S$, $K$, $T$, $r$, and $q$, put-call parity is:

$$
C - P = S e^{-q\tau} - K e^{-r\tau}.
$$

Variables:

- $C$: European call price;
- $P$: European put price;
- $S e^{-q\tau}$: present value of the dividend-adjusted underlying exposure;
- $K e^{-r\tau}$: present value of the strike payment.

Interpretation: a long call plus a discounted strike bond replicates a long put plus dividend-adjusted exposure to the underlying. Violations beyond transaction costs, funding costs, borrow costs, and operational constraints may indicate arbitrage or data problems.

For American options, discrete dividends, borrow costs, and early exercise rights complicate parity relationships.

## 1.9 Core Greeks as Sensitivities

Let the option value be:

$$
V=V(S,t,K,T,r,q,\sigma).
$$

The core Greeks are local sensitivities of $V$.

| Greek | Mathematical Definition | Interpretation | Common Unit |
|---|---|---|---|
| Delta $\Delta$ | $\frac{\partial V}{\partial S}$ | Price sensitivity to spot | option currency per $1 spot move |
| Gamma $\Gamma$ | $\frac{\partial^2 V}{\partial S^2}$ | Change in delta per spot move | delta per $1 spot move |
| Theta $\Theta$ | $\frac{\partial V}{\partial t}$ | Calendar-time sensitivity | option currency per year or per day |
| Vega $\nu$ | $\frac{\partial V}{\partial \sigma}$ | Sensitivity to volatility | option currency per 1.00 volatility unit |
| Rho $\rho$ | $\frac{\partial V}{\partial r}$ | Sensitivity to rate | option currency per 1.00 rate unit |
| Dividend rho / Phi $\psi$ | $\frac{\partial V}{\partial q}$ | Sensitivity to dividend yield | option currency per 1.00 yield unit |

Important scaling convention: if vega is computed as $\partial V/\partial \sigma$ with $\sigma$ in decimal units, then it is the P&L change for a volatility move of $1.00$, or 100 volatility points. Desk vega is often quoted per 1 volatility point, so:

$$
\text{Vega per vol point}=\frac{1}{100}\frac{\partial V}{\partial \sigma}.
$$

Similarly, rho per basis point is:

$$
\text{Rho per bp}=\frac{1}{10000}\frac{\partial V}{\partial r}.
$$

## 1.10 Closed-Form Black-Scholes-Merton Greeks

The formulas below assume European options, continuous dividend yield, constant $r$, constant $q$, constant $\sigma$, no transaction costs, and time to maturity $\tau>0$.

### 1.10.1 Delta

Call delta is:

$$
\Delta_C = e^{-q\tau}N(d_1).
$$

Put delta is:

$$
\Delta_P = e^{-q\tau}\left[N(d_1)-1\right].
$$

Interpretation:

- A call usually has positive delta.
- A put usually has negative delta.
- With no dividends, call delta lies between $0$ and $1$; put delta lies between $-1$ and $0$.
- With continuous dividend yield, the magnitude is scaled by $e^{-q\tau}$.

Delta is the local hedge ratio under the model. If a portfolio has call delta $0.60$, then one option on one unit of underlying behaves locally like $0.60$ units of the underlying for a small spot move. For a listed contract with multiplier 100, one contract has approximately $60$ shares of delta.

### 1.10.2 Gamma

Call and put gamma are equal under Black-Scholes-Merton:

$$
\Gamma_C=\Gamma_P=\frac{e^{-q\tau}\phi(d_1)}{S\sigma\sqrt{\tau}}.
$$

Interpretation:

- Gamma measures curvature of option value with respect to spot.
- Long vanilla calls and puts have positive gamma.
- Short vanilla options have negative gamma.
- Gamma tends to be highest near at-the-money and near expiration, assuming nonzero volatility.

Gamma is central to convexity. Positive gamma means delta increases when spot rises and decreases when spot falls, which is favorable for a dynamically hedged long option if realized volatility is sufficiently high relative to implied volatility and costs.

### 1.10.3 Theta

Using the convention $\Theta=\partial V/\partial t$, where $t$ is calendar time moving forward and $\tau=T-t$ declines, call theta is:

$$
\Theta_C =
-\frac{S e^{-q\tau}\phi(d_1)\sigma}{2\sqrt{\tau}}
- rK e^{-r\tau}N(d_2)
+ qS e^{-q\tau}N(d_1).
$$

Put theta is:

$$
\Theta_P =
-\frac{S e^{-q\tau}\phi(d_1)\sigma}{2\sqrt{\tau}}
+ rK e^{-r\tau}N(-d_2)
- qS e^{-q\tau}N(-d_1).
$$

Interpretation:

- Theta is often negative for long options because time decay erodes optionality.
- Theta can be affected by rates and dividends.
- The first term is usually the dominant time-decay term for near-the-money options.
- Quoted daily theta is often annual theta divided by 365 or 252, depending on convention.

The sign convention must be stated. Some systems define theta as $\partial V/\partial \tau$, which has the opposite sign of $\partial V/\partial t$. This curriculum uses the desk-standard time-passing convention $\Theta=\partial V/\partial t$ unless otherwise stated.

### 1.10.4 Vega

Call and put vega are equal under Black-Scholes-Merton:

$$
\nu_C=\nu_P=S e^{-q\tau}\phi(d_1)\sqrt{\tau}.
$$

Interpretation:

- Vega measures sensitivity to volatility.
- Long vanilla calls and puts have positive vega.
- Short vanilla options have negative vega.
- Vega tends to be largest near at-the-money and for longer maturities, though the exact maximum depends on parameters.

If $\nu=30$, then a change in volatility from $20\%$ to $21\%$ produces an approximate price change of:

$$
\Delta V \approx 30 \times 0.01 = 0.30.
$$

That is vega per one volatility point equals $0.30$.

### 1.10.5 Rho

Call rho is:

$$
\rho_C = K\tau e^{-r\tau}N(d_2).
$$

Put rho is:

$$
\rho_P = -K\tau e^{-r\tau}N(-d_2).
$$

Interpretation:

- Calls usually have positive rho because higher rates reduce the present value of the strike payment.
- Puts usually have negative rho because higher rates reduce the present value of the strike received in the put payoff.
- Rho is more relevant for long-dated options and rates-sensitive underlyings.

For short-dated equity options, rho is often small relative to delta, gamma, vega, and theta. For long-dated options, rates options, FX options, and structured products, rate sensitivity can be material.

### 1.10.6 Dividend Rho / Phi

Sensitivity to the continuous dividend yield $q$ is sometimes called dividend rho or phi. For a call:

$$
\psi_C = \frac{\partial C}{\partial q}
= -\tau S e^{-q\tau}N(d_1).
$$

For a put:

$$
\psi_P = \frac{\partial P}{\partial q}
= \tau S e^{-q\tau}N(-d_1).
$$

Interpretation:

- Higher dividend yield lowers call values because expected forward price is lower.
- Higher dividend yield raises put values because expected forward price is lower.
- Dividend sensitivity matters for index options, dividend-rich equities, and single stocks near ex-dividend dates.

## 1.11 Intuition, Sign, Scale, and Units of Core Greeks

The same Greek can be reported in different units. A robust research system must define scaling explicitly.

| Greek | Long Call Sign | Long Put Sign | Common Scaling | Practical Interpretation |
|---|---:|---:|---|---|
| Delta | Positive | Negative | per $1 spot move | Directional exposure |
| Gamma | Positive | Positive | per $1 spot move squared | Convexity; delta instability |
| Theta | Usually negative | Usually negative | per year or per day | Time carry/time decay |
| Vega | Positive | Positive | per 1.00 vol or 1 vol point | Volatility exposure |
| Rho | Positive | Negative | per 1.00 rate or per bp | Rate exposure |
| Dividend rho | Negative | Positive | per 1.00 yield or per bp | Dividend/carry exposure |

### 1.11.1 Delta Units

Delta is:

$$
\Delta = \frac{\partial V}{\partial S}.
$$

If $V$ and $S$ are measured in dollars, delta is dollars of option value per dollar of underlying move. For one listed equity option contract with multiplier $m=100$ and position quantity $Q$, dollar delta is often expressed as:

$$
\text{Dollar Delta}=Qm\Delta S.
$$

This approximates the dollar P&L for a 100% move in the underlying. For a small spot move $\Delta S$, first-order P&L is:

$$
\Delta \text{P\&L} \approx Qm\Delta\,\Delta S.
$$

### 1.11.2 Gamma Units

Gamma is:

$$
\Gamma = \frac{\partial \Delta}{\partial S}.
$$

For a small move $\Delta S$, the change in delta is approximately:

$$
\Delta \Delta \approx \Gamma\Delta S.
$$

The second-order gamma contribution to option P&L is:

$$
\text{Gamma P\&L} \approx \frac{1}{2}\Gamma(\Delta S)^2.
$$

For a contract position:

$$
\text{Gamma P\&L} \approx \frac{1}{2}Qm\Gamma(\Delta S)^2.
$$

### 1.11.3 Theta Units

Theta is annualized if $t$ is measured in years. Daily theta can be approximated as:

$$
\Theta_{\text{daily}} \approx \frac{\Theta_{\text{annual}}}{365}
$$

for calendar-day decay, or:

$$
\Theta_{\text{trading day}} \approx \frac{\Theta_{\text{annual}}}{252}
$$

for trading-day convention. Options decay over weekends and holidays, but market makers may distribute weekend decay unevenly in quoted implied volatility and theta. Production systems should document the convention.

### 1.11.4 Vega Units

If volatility is expressed as a decimal, vega is per 1.00 volatility unit. For one volatility point:

$$
\nu_{\text{1 vol point}}=0.01\nu.
$$

For a position:

$$
\text{Vega P\&L} \approx Qm\nu\Delta\sigma.
$$

If implied volatility rises from $20\%$ to $22\%$, then $\Delta\sigma=0.02$.

### 1.11.5 Rho Units

Rho is per 1.00 rate unit if $r$ is represented as a decimal. For one basis point:

$$
\rho_{\text{1 bp}}=0.0001\rho.
$$

Rate sensitivity is usually less important for short-dated single-stock options but can be material for long-dated index options, LEAPS, rates options, and FX options.

## 1.12 Greek Behavior Across Moneyness, Maturity, Volatility, and Rates

### 1.12.1 Behavior by Moneyness

| Moneyness | Call Delta | Put Delta | Gamma | Vega | Theta |
|---|---:|---:|---:|---:|---:|
| Deep OTM call / deep ITM put | Near 0 | Near -1 | Low | Low to moderate | Low absolute decay |
| ATM | Around 0.5 adjusted by dividends | Around -0.5 adjusted by dividends | High | High | High absolute decay |
| Deep ITM call / deep OTM put | Near 1 | Near 0 | Low | Low to moderate | Often lower optionality decay |

At-the-money options have high uncertainty about finishing in-the-money. This makes their option value highly sensitive to spot and volatility assumptions.

### 1.12.2 Behavior by Maturity

Short-dated at-the-money options often have high gamma because a small spot move can drastically change terminal payoff probability. However, they may have lower total vega than longer-dated options because there is less time for volatility to matter.

Longer-dated options generally have higher vega because volatility affects a longer horizon. Their gamma is often lower because the option has more time for future moves, so a small immediate spot move may not change the terminal distribution as sharply.

| Maturity | Gamma | Vega | Theta | Implementation Risk |
|---|---:|---:|---:|---|
| Very short-dated | Very high near ATM | Lower in total terms | Can be extremely nonlinear | Pin risk, gap risk, execution sensitivity |
| Medium-dated | Moderate | Moderate to high | Meaningful | Roll and surface risk |
| Long-dated | Lower local gamma | High | Lower daily decay but persistent | Rate, dividend, model, and liquidity risk |

### 1.12.3 Behavior by Volatility

Higher volatility spreads the risk-neutral distribution. For at-the-money options, higher volatility usually increases option value and can affect gamma concentration.

Black-Scholes gamma is:

$$
\Gamma=\frac{e^{-q\tau}\phi(d_1)}{S\sigma\sqrt{\tau}}.
$$

The denominator contains $\sigma$, so all else equal, higher volatility can reduce peak gamma by spreading probability mass across a wider range of outcomes. However, the effect also depends on $d_1$ through $\phi(d_1)$.

Vega is:

$$
\nu=S e^{-q\tau}\phi(d_1)\sqrt{\tau}.
$$

Vega is highest where $\phi(d_1)$ is high, generally near at-the-money-forward.

### 1.12.4 Behavior by Rates and Dividends

Rates and dividends affect forwards and discounting. A higher risk-free rate generally increases call values and lowers put values, all else equal. A higher dividend yield generally lowers call values and raises put values.

For equity-index options, dividends affect forward pricing and put-call parity. For single-name options, discrete dividends also affect early exercise risk for American calls.

## 1.13 Comparison of Call and Put Greeks

Under Black-Scholes-Merton with the same strike and maturity:

| Greek | Call | Put | Relationship |
|---|---|---|---|
| Delta | $e^{-q\tau}N(d_1)$ | $e^{-q\tau}[N(d_1)-1]$ | Put delta = call delta minus $e^{-q\tau}$ |
| Gamma | $\frac{e^{-q\tau}\phi(d_1)}{S\sigma\sqrt{\tau}}$ | same | Equal for same $K,T$ |
| Vega | $S e^{-q\tau}\phi(d_1)\sqrt{\tau}$ | same | Equal for same $K,T$ |
| Theta | Includes $-rK e^{-r\tau}N(d_2)+qS e^{-q\tau}N(d_1)$ | Includes $+rK e^{-r\tau}N(-d_2)-qS e^{-q\tau}N(-d_1)$ | Differs due to carry terms |
| Rho | $K\tau e^{-r\tau}N(d_2)$ | $-K\tau e^{-r\tau}N(-d_2)$ | Opposite typical signs |
| Dividend rho | $-\tau S e^{-q\tau}N(d_1)$ | $\tau S e^{-q\tau}N(-d_1)$ | Opposite typical signs |

The equality of call and put gamma and vega for same strike and maturity follows from put-call parity under the model. If market data show materially different implied volatilities for a call and put with the same strike and maturity, the difference may reflect American exercise, dividends, borrow, funding, stale quotes, bid-ask effects, or data errors.

## 1.14 Why Gamma, Theta, and Vega Concentrate Near At-the-Money Options

The standard normal density term $\phi(d_1)$ appears in gamma, vega, and the leading time-decay term. Since $\phi(d_1)$ is largest when $d_1$ is near zero, these Greeks tend to be concentrated near at-the-money-forward options.

Gamma:

$$
\Gamma=\frac{e^{-q\tau}\phi(d_1)}{S\sigma\sqrt{\tau}}.
$$

Vega:

$$
\nu=S e^{-q\tau}\phi(d_1)\sqrt{\tau}.
$$

Leading theta decay term:

$$
-\frac{S e^{-q\tau}\phi(d_1)\sigma}{2\sqrt{\tau}}.
$$

Intuition:

- Deep out-of-the-money options are unlikely to finish in-the-money, so small spot changes often have limited immediate effect.
- Deep in-the-money options behave more like the underlying or discounted strike exposure, so optionality is less sensitive to small changes.
- At-the-money options sit near the boundary between payoff and no payoff, so small changes in spot, volatility, and time strongly affect value.

This concentration is why at-the-money short-dated options are central to gamma trading, pin risk, and expiration-week risk management.

## 1.15 Time Decay, Nonlinear Decay Near Expiration, and Pin Risk

Time decay is not linear. The decay of an option's extrinsic value can accelerate near expiration, especially for near-the-money options.

For an at-the-money option, the leading theta term has the form:

$$
-\frac{S e^{-q\tau}\phi(d_1)\sigma}{2\sqrt{\tau}}.
$$

As $\tau \to 0$, the denominator $\sqrt{\tau}$ becomes small. This can make theta highly negative for near-the-money long options and highly positive for near-the-money short options, ignoring other terms.

But this high theta is inseparable from high gamma. A short at-the-money option near expiration may collect rapid time decay but has severe exposure to small spot moves and jumps.

### 1.15.1 Pin Risk

Pin risk occurs when the underlying price is close to the strike near expiration. Small price changes can determine whether an option expires in-the-money or out-of-the-money, creating uncertainty about assignment, exercise, hedge requirements, and final exposure.

Pin risk is especially relevant for:

- short-dated options;
- options near large open-interest strikes;
- single-stock options around earnings or corporate events;
- physically settled options;
- portfolios with many short strikes near spot.

A position that appears delta-neutral before expiration can become directionally exposed after assignment or exercise. Production risk systems must model exercise and assignment rules, especially for American options.

## 1.16 Greek-Based Local P&L Approximation

For a small change in spot $\Delta S$, volatility $\Delta \sigma$, rate $\Delta r$, and time passage $\Delta t$, a local Taylor approximation is:

$$
\Delta V \approx
\Delta \cdot \Delta S
+ \frac{1}{2}\Gamma(\Delta S)^2
+ \Theta \cdot \Delta t
+ \nu \cdot \Delta \sigma
+ \rho \cdot \Delta r.
$$

Variables:

- $\Delta V$: approximate change in option value;
- $\Delta$: delta;
- $\Gamma$: gamma;
- $\Theta$: theta using calendar-time convention;
- $\nu$: vega;
- $\rho$: rho;
- $\Delta S$: spot change;
- $\Delta \sigma$: volatility change in decimal units;
- $\Delta r$: rate change in decimal units;
- $\Delta t$: elapsed time in years.

Interpretation: the first-order spot effect is delta P&L, the second-order spot effect is gamma P&L, time passage contributes theta carry, implied volatility changes contribute vega P&L, and rate changes contribute rho P&L.

Limitations:

- It is local and may fail for large moves.
- It ignores changes in Greeks unless higher-order terms are included.
- It assumes a flat volatility change unless surface effects are modeled.
- It excludes transaction costs, slippage, and liquidity.
- It does not capture jumps, early exercise, or discrete dividends.

This approximation becomes more powerful later when extended to higher-order Greeks and full repricing scenario engines.

## 1.17 Practical Interpretation for Core Strategy Exposures

A simple way to understand option strategy families is to classify their core Greek exposures.

| Position | Delta | Gamma | Theta | Vega | Typical Economic Exposure |
|---|---:|---:|---:|---:|---|
| Long call | + | + | - | + | Bullish direction, long convexity, long vol |
| Long put | - | + | - | + | Bearish direction, long convexity, long vol |
| Short call | - | - | + | - | Short upside, short convexity, short vol |
| Short put | + | - | + | - | Long downside credit risk, short convexity, short vol |
| Long straddle | near 0 at initiation | + | - | + | Long realized vol / event move |
| Short straddle | near 0 at initiation | - | + | - | Short realized vol / carry |
| Covered call | positive but capped | short call gamma overlay | call theta earned | short call vega | Equity plus short upside vol |
| Protective put | positive equity plus put hedge | + from put | - from put | + from put | Downside convexity hedge |

These are stylized profiles. Actual exposures depend on strike, maturity, implied volatility, surface shape, position sizing, and hedging.

## 1.18 Common Beginner Errors

| Error | Why It Is Problematic | Better Practice |
|---|---|---|
| Treating delta as probability | Delta and risk-neutral probability are related but not identical | Use precise definitions and distinguish $N(d_1)$ from $N(d_2)$ |
| Ignoring units | Vega per 100 vol points vs per 1 vol point changes interpretation | Standardize scaling in all reports |
| Assuming theta is free income | Positive theta often comes with negative gamma or tail risk | Analyze theta-gamma trade-off |
| Using Black-Scholes Greeks as truth | Real markets have skew, jumps, stochastic vol, costs, and liquidity limits | Compare analytical, surface-aware, and scenario Greeks |
| Ignoring dividends | Dividend assumptions affect forwards, parity, and early exercise | Use point-in-time dividend inputs |
| Ignoring bid-ask spreads | Apparent mispricing may vanish after costs | Use executable prices and slippage models |
| Overusing local Greeks for large shocks | Taylor approximation may fail in nonlinear regimes | Use full repricing stress tests |
| Treating implied volatility as forecast only | Implied volatility includes risk premia and supply-demand effects | Separate forecast, premium, liquidity, and model error |

## 1.19 Python Code: Black-Scholes Pricing and Core Greeks

The following code implements European Black-Scholes-Merton prices and core Greeks with continuous dividend yield. It uses decimal annualized rates and volatility. It is designed for educational research and should be extended before production use.

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

    Parameters
    ----------
    spot:
        Current underlying spot price. Must be positive.
    strike:
        Option strike price. Must be positive.
    tau:
        Time to maturity in years. Must be positive for standard Greeks.
    rate:
        Continuously compounded risk-free rate as decimal, e.g. 0.04.
    dividend_yield:
        Continuous dividend yield as decimal, e.g. 0.02.
    volatility:
        Annualized volatility as decimal, e.g. 0.20.
    option_type:
        Either "call" or "put".
    """

    spot: float
    strike: float
    tau: float
    rate: float
    dividend_yield: float
    volatility: float
    option_type: OptionType


def _validate_inputs(x: BSMInputs) -> None:
    if x.spot <= 0 or not np.isfinite(x.spot):
        raise ValueError("spot must be positive and finite")
    if x.strike <= 0 or not np.isfinite(x.strike):
        raise ValueError("strike must be positive and finite")
    if x.tau <= 0 or not np.isfinite(x.tau):
        raise ValueError("tau must be positive and finite")
    if x.volatility <= 0 or not np.isfinite(x.volatility):
        raise ValueError("volatility must be positive and finite")
    if not np.isfinite(x.rate):
        raise ValueError("rate must be finite")
    if not np.isfinite(x.dividend_yield):
        raise ValueError("dividend_yield must be finite")
    if x.option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")


def bsm_d1_d2(x: BSMInputs) -> tuple[float, float]:
    """Return Black-Scholes-Merton d1 and d2."""
    _validate_inputs(x)
    vol_sqrt_t = x.volatility * math.sqrt(x.tau)
    d1 = (
        math.log(x.spot / x.strike)
        + (x.rate - x.dividend_yield + 0.5 * x.volatility**2) * x.tau
    ) / vol_sqrt_t
    d2 = d1 - vol_sqrt_t
    return d1, d2


def bsm_price(x: BSMInputs) -> float:
    """Return the European Black-Scholes-Merton option price."""
    d1, d2 = bsm_d1_d2(x)
    df_r = math.exp(-x.rate * x.tau)
    df_q = math.exp(-x.dividend_yield * x.tau)

    if x.option_type == "call":
        return x.spot * df_q * norm.cdf(d1) - x.strike * df_r * norm.cdf(d2)

    return x.strike * df_r * norm.cdf(-d2) - x.spot * df_q * norm.cdf(-d1)


def bsm_core_greeks(x: BSMInputs) -> dict[str, float]:
    """Return core BSM Greeks.

    Conventions
    -----------
    - Delta is per 1 unit move in spot.
    - Gamma is per 1 unit move in spot squared.
    - Theta is annualized and uses the calendar-time convention dV/dt.
    - Vega is per 1.00 volatility unit. Divide by 100 for one vol point.
    - Rho is per 1.00 rate unit. Divide by 10,000 for one basis point.
    - Dividend rho is per 1.00 dividend-yield unit.
    """
    d1, d2 = bsm_d1_d2(x)
    df_r = math.exp(-x.rate * x.tau)
    df_q = math.exp(-x.dividend_yield * x.tau)
    phi_d1 = norm.pdf(d1)

    gamma = df_q * phi_d1 / (x.spot * x.volatility * math.sqrt(x.tau))
    vega = x.spot * df_q * phi_d1 * math.sqrt(x.tau)

    common_theta = -(
        x.spot * df_q * phi_d1 * x.volatility / (2.0 * math.sqrt(x.tau))
    )

    if x.option_type == "call":
        delta = df_q * norm.cdf(d1)
        theta = (
            common_theta
            - x.rate * x.strike * df_r * norm.cdf(d2)
            + x.dividend_yield * x.spot * df_q * norm.cdf(d1)
        )
        rho = x.strike * x.tau * df_r * norm.cdf(d2)
        dividend_rho = -x.tau * x.spot * df_q * norm.cdf(d1)
    else:
        delta = df_q * (norm.cdf(d1) - 1.0)
        theta = (
            common_theta
            + x.rate * x.strike * df_r * norm.cdf(-d2)
            - x.dividend_yield * x.spot * df_q * norm.cdf(-d1)
        )
        rho = -x.strike * x.tau * df_r * norm.cdf(-d2)
        dividend_rho = x.tau * x.spot * df_q * norm.cdf(-d1)

    return {
        "price": bsm_price(x),
        "delta": delta,
        "gamma": gamma,
        "theta_annual": theta,
        "theta_calendar_day": theta / 365.0,
        "vega_per_1_vol": vega,
        "vega_per_vol_point": vega / 100.0,
        "rho_per_1_rate": rho,
        "rho_per_bp": rho / 10_000.0,
        "dividend_rho_per_1_yield": dividend_rho,
    }


example = BSMInputs(
    spot=100.0,
    strike=100.0,
    tau=0.50,
    rate=0.04,
    dividend_yield=0.01,
    volatility=0.20,
    option_type="call",
)

print(pd.Series(bsm_core_greeks(example)).round(6))
```

Expected output: a `pandas.Series` containing the model price and core Greeks for the specified European call. Exact values may vary slightly by numerical library version, but should be stable to normal floating-point precision.

## 1.20 Python Code: Greek Behavior Across Moneyness and Maturity

The next code block creates a synthetic grid of strikes and maturities and calculates core Greeks. It is useful for understanding how gamma and vega concentrate across the option surface.

```python
import numpy as np
import pandas as pd


def greek_grid(
    spot: float = 100.0,
    strikes: np.ndarray | None = None,
    maturities: np.ndarray | None = None,
    rate: float = 0.04,
    dividend_yield: float = 0.01,
    volatility: float = 0.20,
    option_type: OptionType = "call",
) -> pd.DataFrame:
    """Calculate BSM Greeks across strike and maturity grids."""
    if strikes is None:
        strikes = np.linspace(70.0, 130.0, 31)
    if maturities is None:
        maturities = np.array([7, 30, 90, 180, 365]) / 365.0

    rows = []
    for tau in maturities:
        for strike in strikes:
            inputs = BSMInputs(
                spot=spot,
                strike=float(strike),
                tau=float(tau),
                rate=rate,
                dividend_yield=dividend_yield,
                volatility=volatility,
                option_type=option_type,
            )
            greeks = bsm_core_greeks(inputs)
            rows.append(
                {
                    "spot": spot,
                    "strike": strike,
                    "moneyness_spot_over_strike": spot / strike,
                    "tau_years": tau,
                    **greeks,
                }
            )
    return pd.DataFrame(rows)


grid = greek_grid(option_type="call")
print(grid.head())

# Example pivot tables for inspection.
gamma_table = grid.pivot_table(
    index="strike",
    columns="tau_years",
    values="gamma",
)
vega_table = grid.pivot_table(
    index="strike",
    columns="tau_years",
    values="vega_per_vol_point",
)

print("Gamma table:")
print(gamma_table.round(5).head())
print("Vega per vol point table:")
print(vega_table.round(4).head())
```

This grid uses hypothetical inputs and is not calibrated to market data. In a production research environment, the same structure would be fed by point-in-time option chains, borrow assumptions, dividend curves, discount curves, and an implied-volatility surface.

## 1.21 Python Code: Plotting Price and Greek Curves

The following code creates separate plots for price, delta, gamma, theta, and vega across strike. It uses `matplotlib` and avoids fixed styling assumptions.

```python
import matplotlib.pyplot as plt


def plot_greek_vs_strike(
    df: pd.DataFrame,
    tau_years: float,
    value_column: str,
    title: str,
) -> None:
    """Plot one Greek or price column across strikes for one maturity."""
    subset = df[np.isclose(df["tau_years"], tau_years)].sort_values("strike")
    if subset.empty:
        raise ValueError("No rows found for the requested maturity")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(subset["strike"], subset[value_column])
    ax.set_xlabel("Strike")
    ax.set_ylabel(value_column)
    ax.set_title(title)
    ax.grid(True)
    plt.show()


one_month = 30 / 365
plot_greek_vs_strike(grid, one_month, "price", "Call price across strike")
plot_greek_vs_strike(grid, one_month, "delta", "Call delta across strike")
plot_greek_vs_strike(grid, one_month, "gamma", "Call gamma across strike")
plot_greek_vs_strike(grid, one_month, "theta_calendar_day", "Call daily theta across strike")
plot_greek_vs_strike(grid, one_month, "vega_per_vol_point", "Call vega per vol point across strike")
```

Expected interpretation:

- Call price decreases as strike increases.
- Call delta decreases as strike increases.
- Gamma is concentrated near at-the-money.
- Daily theta is most negative near at-the-money for long options.
- Vega per vol point is concentrated near at-the-money and usually larger for longer maturities.

## 1.22 Implementation Notes for Institutional Research Systems

The educational code above is intentionally compact. A production implementation should add several layers.

### 1.22.1 Data Validation

A production Greek engine should reject or flag:

- nonpositive spot prices;
- nonpositive strikes;
- nonpositive or missing maturities;
- invalid implied volatility;
- crossed bid-ask markets;
- stale quotes;
- options with zero bid and unreliable ask;
- options outside permitted moneyness or maturity ranges;
- missing dividend, rate, borrow, or corporate-action inputs;
- inconsistent contract multipliers.

### 1.22.2 Point-in-Time Inputs

For backtesting, all inputs must be point-in-time. This includes:

- option quotes;
- underlying prices;
- corporate actions;
- dividend forecasts;
- risk-free curves;
- borrow costs;
- earnings dates;
- index constituents;
- sector and factor classifications;
- analyst forecasts and macro variables.

A backtest that uses revised data can produce misleading results.

### 1.22.3 Batch Versus Real-Time Calculation

For a large single-stock option universe, Greek calculation may need to run across millions of option records. A production architecture may separate:

- end-of-day batch Greek generation;
- intraday incremental updates;
- real-time risk monitoring;
- scenario and stress engines;
- backtesting research jobs.

Python is useful for research. Production scaling may use vectorized NumPy, Polars, Spark, compiled libraries, C++, Scala, Rust, or GPU acceleration, depending on latency and volume requirements.

### 1.22.4 Reconciliation

Analytical Greeks should be reconciled against vendor Greeks and broker Greeks. Differences may arise from:

- volatility surface interpolation;
- American exercise models;
- discrete dividends;
- borrow and funding assumptions;
- day-count conventions;
- settlement calendars;
- stale or filtered quotes;
- contract multiplier adjustments;
- premium-adjusted delta conventions;
- sticky-delta versus sticky-strike assumptions.

Reconciliation differences should be logged and explained, not ignored.

## 1.23 Summary of Part 1

Part 1 established the foundation for the rest of the curriculum.

Key points:

1. A call payoff is $(S_T-K)^+$ and a put payoff is $(K-S_T)^+$.
2. Option value before maturity contains intrinsic value and time value.
3. Moneyness can be defined using spot, log spot, forward, or log forward conventions.
4. Black-Scholes-Merton assumes European exercise, constant volatility, continuous trading, frictionless markets, continuous dividends, and no jumps.
5. The Black-Scholes-Merton PDE is the no-arbitrage pricing equation; Greeks are sensitivities of the value function.
6. Core Greeks measure local sensitivity to spot, curvature, time, volatility, rates, and dividends.
7. Gamma, vega, and the leading theta term are concentrated near at-the-money because they depend heavily on $\phi(d_1)$.
8. Time decay is nonlinear and becomes especially important near expiration.
9. Pin risk arises when the underlying is close to strike near expiration.
10. Local Greek P&L approximations are useful but must be supplemented by full repricing, surface-aware risk, transaction costs, and stress testing.
11. Production Greek systems require point-in-time data, validation, scaling, and reconciliation.

The next installment will extend this foundation to higher-order Greeks such as vanna, volga, charm, color, speed, zomma, ultima, veta, and vera, and will explain why first-order Greeks are unstable under realistic surface dynamics.
