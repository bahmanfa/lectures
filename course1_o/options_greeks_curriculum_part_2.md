# Institutional Options Greeks, Systematic Strategy, and Regime-Aware Portfolio Construction Curriculum

## Completed Installment

This installment contains:

- Part 2: Higher-Order Greeks and Dynamic Greek Surfaces.

The document is educational and research-oriented. It is not personalized investment advice, a live trading recommendation, or a claim that any option strategy produces guaranteed alpha.

---

# Part 2: Higher-Order Greeks and Dynamic Greek Surfaces

**Level:** Intermediate to Advanced

## 2.1 Why Higher-Order Greeks Matter

Core Greeks such as delta, gamma, theta, vega, and rho describe local first- and second-order sensitivities of an option value function. They are essential, but they are not sufficient for institutional options risk management. A portfolio can appear controlled under first-order Greeks and still be unstable because the Greeks themselves change rapidly when spot, time, volatility, rates, dividends, and surface shape move.

Higher-order Greeks measure this instability. They answer questions such as:

- How quickly will delta change if implied volatility changes?
- How quickly will vega change if spot moves?
- How sensitive is gamma to volatility?
- How fast does gamma decay or explode as expiration approaches?
- How does vega decay through time?
- How does the portfolio behave if spot and volatility move together, as they often do during equity stress?
- How does risk change under skew steepening, skew flattening, or term-structure shocks?

For a general option value function:

$$
V = V(S,t,K,T,r,q,\sigma),
$$

where $S$ is spot, $t$ is calendar time, $K$ is strike, $T$ is maturity, $r$ is the risk-free rate, $q$ is the dividend yield, and $\sigma$ is volatility, the higher-order Greeks are derivatives of core Greeks with respect to the same or additional variables.

They are not separate pricing theories. They are local sensitivity measures. Their interpretation depends on the pricing model, the volatility-surface assumption, and the scaling convention.

## 2.2 Baseline Conventions for Part 2

Unless otherwise stated, Part 2 uses the same baseline assumptions as Part 1:

- European options;
- continuous dividend yield $q$;
- constant risk-free rate $r$;
- constant Black-Scholes-Merton volatility $\sigma$;
- no transaction costs, funding spreads, borrow costs, margin constraints, or market impact;
- analytical spot Greeks under the Black-Scholes-Merton model;
- time to maturity $\tau=T-t$ measured in years;
- volatility and rates expressed in decimal annualized units.

The Black-Scholes-Merton definitions are:

$$
d_1 = \frac{\ln(S/K)+(r-q+\frac{1}{2}\sigma^2)\tau}{\sigma\sqrt{\tau}},
$$

$$
d_2 = d_1-\sigma\sqrt{\tau},
$$

and:

$$
\phi(d_1)=\frac{1}{\sqrt{2\pi}}e^{-d_1^2/2}.
$$

The core Black-Scholes-Merton gamma and vega are:

$$
\Gamma = \frac{e^{-q\tau}\phi(d_1)}{S\sigma\sqrt{\tau}},
$$

$$
\nu = S e^{-q\tau}\phi(d_1)\sqrt{\tau}.
$$

The formulas in this part are per one option on one unit of the underlying. For listed equity options, production exposure must multiply by contract quantity and contract multiplier.

## 2.3 A Taxonomy of Higher-Order Greeks

Higher-order Greeks can be grouped by the type of instability they measure.

| Greek | Mathematical Definition | Informal Meaning | Primary Risk Question |
|---|---:|---|---|
| Vanna | $\frac{\partial^2 V}{\partial S\partial\sigma}$ | Delta sensitivity to volatility or vega sensitivity to spot | How does spot-vol co-movement affect hedging? |
| Volga / Vomma | $\frac{\partial^2 V}{\partial \sigma^2}$ | Vega sensitivity to volatility | How nonlinear is volatility exposure? |
| Charm | $\frac{\partial \Delta}{\partial t}$ | Delta decay through time | How much will delta drift if spot does not move? |
| Color | $\frac{\partial \Gamma}{\partial t}$ | Gamma decay through time | How unstable is gamma near expiry? |
| Speed | $\frac{\partial \Gamma}{\partial S}$ | Gamma sensitivity to spot | How quickly does convexity migrate across strikes? |
| Zomma | $\frac{\partial \Gamma}{\partial \sigma}$ | Gamma sensitivity to volatility | How does vol repricing affect gamma? |
| Ultima | $\frac{\partial \text{Volga}}{\partial \sigma}$ | Volga sensitivity to volatility | How unstable is volatility convexity? |
| Veta | $\frac{\partial \nu}{\partial t}$ | Vega decay through time | How quickly does volatility exposure decay? |
| Vera | $\frac{\partial^2 V}{\partial \sigma\partial r}$ | Vega sensitivity to rates or rho sensitivity to vol | How do rates and volatility interact? |

The definitions above use the calendar-time convention for time derivatives: $\partial/\partial t$ means time passes and $\tau=T-t$ declines. Some vendors define charm, color, and veta with respect to $\tau$ instead of $t$, which reverses the sign. A production system must store the convention explicitly.

## 2.4 Higher-Order Greeks as Derivatives of the Value Function

A compact way to organize Greeks is through gradients and Hessians.

Let the state vector be:

$$
\mathbf{x}=\begin{bmatrix}S & \sigma & r & q & t\end{bmatrix}^{\top}.
$$

The first-order sensitivity vector is:

$$
\nabla V(\mathbf{x}) =
\begin{bmatrix}
\frac{\partial V}{\partial S} \\
\frac{\partial V}{\partial \sigma} \\
\frac{\partial V}{\partial r} \\
\frac{\partial V}{\partial q} \\
\frac{\partial V}{\partial t}
\end{bmatrix}
=
\begin{bmatrix}
\Delta \\
\nu \\
\rho \\
\psi \\
\Theta
\end{bmatrix},
$$

where $\psi=\partial V/\partial q$ is dividend rho.

The second-order sensitivity matrix, or Hessian, is:

$$
\mathbf{H}_V(\mathbf{x})=
\begin{bmatrix}
\frac{\partial^2 V}{\partial S^2} & \frac{\partial^2 V}{\partial S\partial\sigma} & \frac{\partial^2 V}{\partial S\partial r} & \frac{\partial^2 V}{\partial S\partial q} & \frac{\partial^2 V}{\partial S\partial t} \\
\frac{\partial^2 V}{\partial \sigma\partial S} & \frac{\partial^2 V}{\partial \sigma^2} & \frac{\partial^2 V}{\partial \sigma\partial r} & \frac{\partial^2 V}{\partial \sigma\partial q} & \frac{\partial^2 V}{\partial \sigma\partial t} \\
\frac{\partial^2 V}{\partial r\partial S} & \frac{\partial^2 V}{\partial r\partial \sigma} & \frac{\partial^2 V}{\partial r^2} & \frac{\partial^2 V}{\partial r\partial q} & \frac{\partial^2 V}{\partial r\partial t} \\
\frac{\partial^2 V}{\partial q\partial S} & \frac{\partial^2 V}{\partial q\partial \sigma} & \frac{\partial^2 V}{\partial q\partial r} & \frac{\partial^2 V}{\partial q^2} & \frac{\partial^2 V}{\partial q\partial t} \\
\frac{\partial^2 V}{\partial t\partial S} & \frac{\partial^2 V}{\partial t\partial \sigma} & \frac{\partial^2 V}{\partial t\partial r} & \frac{\partial^2 V}{\partial t\partial q} & \frac{\partial^2 V}{\partial t^2}
\end{bmatrix}.
$$

The most commonly monitored entries include:

- $\Gamma=\partial^2V/\partial S^2$;
- $\text{Vanna}=\partial^2V/(\partial S\partial\sigma)$;
- $\text{Volga}=\partial^2V/\partial\sigma^2$;
- $\text{Vera}=\partial^2V/(\partial\sigma\partial r)$;
- $\text{Charm}=\partial^2V/(\partial S\partial t)$;
- $\text{Veta}=\partial^2V/(\partial\sigma\partial t)$.

Under sufficiently smooth model assumptions, cross-partials are symmetric. For example:

$$
\frac{\partial^2 V}{\partial S\partial\sigma}
=
\frac{\partial^2 V}{\partial\sigma\partial S}.
$$

This means vanna can be interpreted either as the sensitivity of delta to volatility or the sensitivity of vega to spot. In real-world implementation, numerical finite differences, interpolation noise, American exercise features, and discontinuities in market data can break this symmetry approximately.

## 2.5 Vanna

## 2.5.1 Definition

Vanna is the cross-sensitivity of option value to spot and volatility:

$$
\text{Vanna} = \frac{\partial^2 V}{\partial S\partial\sigma}.
$$

Equivalently:

$$
\text{Vanna}=\frac{\partial \Delta}{\partial \sigma}
=\frac{\partial \nu}{\partial S}.
$$

Under Black-Scholes-Merton with continuous dividend yield:

$$
\text{Vanna}= -e^{-q\tau}\phi(d_1)\frac{d_2}{\sigma}.
$$

Variables:

- $e^{-q\tau}$ is the dividend discount factor;
- $\phi(d_1)$ is the standard normal density evaluated at $d_1$;
- $d_2=d_1-\sigma\sqrt{\tau}$;
- $\sigma$ is annualized volatility in decimal units.

## 2.5.2 Intuition

Vanna measures how delta changes when implied volatility changes. It also measures how vega changes when spot changes.

This is important because equity markets often display negative spot-volatility correlation. During equity selloffs, implied volatility often rises. A position's P&L therefore depends not only on delta and vega separately, but on the interaction between spot and volatility.

A local second-order approximation includes the cross term:

$$
\Delta V_{S,\sigma} \approx \text{Vanna}\,\Delta S\,\Delta\sigma.
$$

where $\Delta S$ is the spot move and $\Delta\sigma$ is the volatility move in decimal units.

If spot falls and implied volatility rises, the sign of vanna can materially affect P&L. This is especially important for skew trades, risk reversals, collars, and portfolios containing options across different deltas.

## 2.5.3 Practical Use

Vanna is central to:

- skew-aware hedging;
- spot-vol correlation risk;
- risk reversals;
- collars;
- dispersion trading;
- option overlays where downside moves and volatility spikes are expected to occur together;
- dealer positioning analysis, because vanna exposure can influence hedging flows.

Vanna is not a pure alpha signal. It is an exposure that may or may not be compensated depending on market regime, surface richness, transaction costs, and portfolio context.

## 2.6 Volga / Vomma

## 2.6.1 Definition

Volga, also called vomma, is the second derivative of option value with respect to volatility:

$$
\text{Volga}=\frac{\partial^2 V}{\partial\sigma^2}=\frac{\partial\nu}{\partial\sigma}.
$$

Under Black-Scholes-Merton:

$$
\text{Volga}=\nu\frac{d_1d_2}{\sigma},
$$

where $\nu$ is Black-Scholes-Merton vega.

## 2.6.2 Intuition

Volga measures the convexity of option value with respect to volatility. Positive volga means vega increases when volatility rises. Negative volga means vega decreases when volatility rises.

Volga is especially important for out-of-the-money options and volatility-of-volatility exposure. A portfolio can be close to vega-neutral at initiation but still have material volatility convexity. If implied volatility moves sharply, the vega-neutrality can disappear.

The second-order volatility P&L approximation is:

$$
\Delta V_{\sigma} \approx \nu\Delta\sigma + \frac{1}{2}\text{Volga}(\Delta\sigma)^2.
$$

Here $\Delta\sigma$ is a volatility move in decimal units. A 5 volatility-point shock is $\Delta\sigma=0.05$.

## 2.6.3 Practical Use

Volga matters in:

- long-volatility portfolios;
- tail-risk hedges;
- volatility call spreads;
- options on volatility indices;
- long-dated convexity trades;
- stress testing of vega-neutral books;
- volatility surface shock analysis.

Short-volatility strategies can have negative volga or unfavorable volatility convexity. This means losses can accelerate when volatility rises, especially when combined with negative gamma and adverse skew movement.

## 2.7 Charm

## 2.7.1 Definition

Charm measures the sensitivity of delta to the passage of calendar time:

$$
\text{Charm}=\frac{\partial\Delta}{\partial t}.
$$

Because $\tau=T-t$, this is:

$$
\frac{\partial\Delta}{\partial t}=-\frac{\partial\Delta}{\partial\tau}.
$$

Define:

$$
A_{\tau}=\frac{\partial d_1}{\partial\tau}
=\frac{2(r-q)\tau-d_2\sigma\sqrt{\tau}}{2\tau\sigma\sqrt{\tau}}.
$$

For a European call:

$$
\text{Charm}_C
= q e^{-q\tau}N(d_1)-e^{-q\tau}\phi(d_1)A_{\tau}.
$$

For a European put:

$$
\text{Charm}_P
= q e^{-q\tau}\left[N(d_1)-1\right]-e^{-q\tau}\phi(d_1)A_{\tau}.
$$

These formulas use the calendar-time convention. If a system defines charm as $\partial\Delta/\partial\tau$, the signs are reversed.

## 2.7.2 Intuition

Charm measures delta drift if spot and volatility do not move. This matters because an option portfolio can become directionally exposed simply because time passes.

For example, a short-dated out-of-the-money call may have low delta today. If spot remains near strike as expiration approaches, its delta can change rapidly. A delta-neutral book can become directionally exposed overnight even without a large spot move.

## 2.7.3 Practical Use

Charm is important for:

- daily hedge planning;
- intraday delta drift forecasting;
- expiration-week risk;
- market-maker inventory management;
- portfolios with many short-dated options;
- option overlays that rebalance on a schedule rather than continuously.

Charm is not usually traded directly. It is a risk-control measure and a predictor of hedge turnover.

## 2.8 Color

## 2.8.1 Definition

Color measures the sensitivity of gamma to the passage of calendar time:

$$
\text{Color}=\frac{\partial\Gamma}{\partial t}.
$$

Since $\partial/\partial t=-\partial/\partial\tau$, and:

$$
\Gamma = \frac{e^{-q\tau}\phi(d_1)}{S\sigma\sqrt{\tau}},
$$

calendar-time color can be written compactly as:

$$
\text{Color}
=\Gamma\left(q+\frac{1}{2\tau}+d_1A_{\tau}\right),
$$

where:

$$
A_{\tau}=\frac{2(r-q)\tau-d_2\sigma\sqrt{\tau}}{2\tau\sigma\sqrt{\tau}}.
$$

This is the calendar-time convention. If color is defined as $\partial\Gamma/\partial\tau$, the sign is reversed.

## 2.8.2 Intuition

Color explains how quickly gamma changes as expiration approaches. Near expiration, gamma can rise dramatically for near-the-money options and collapse for options that move far in- or out-of-the-money.

This makes color particularly important for:

- zero-days-to-expiration and very short-dated options;
- expiration-week books;
- concentrated strike exposures;
- pin risk;
- short-gamma risk limits;
- dynamic hedging cost forecasts.

A portfolio can be within gamma limits today but exceed them tomorrow if color is large and time decay concentrates gamma near spot.

## 2.9 Speed

## 2.9.1 Definition

Speed is the sensitivity of gamma to spot:

$$
\text{Speed}=\frac{\partial\Gamma}{\partial S}.
$$

Under Black-Scholes-Merton:

$$
\text{Speed}
= -\frac{\Gamma}{S}\left(1+\frac{d_1}{\sigma\sqrt{\tau}}\right).
$$

## 2.9.2 Intuition

Speed measures how quickly convexity changes as the underlying moves. Gamma is not constant. When spot moves away from a strike, the concentration of gamma migrates across the strike grid.

A trader who is short gamma near the current spot may find that the worst gamma exposure changes as spot moves. This is especially relevant for books with multiple strikes, barriers, or large short option positions around crowded strikes.

## 2.9.3 Practical Use

Speed matters for:

- large spot stress scenarios;
- strike concentration monitoring;
- gamma scalping simulations;
- expiration risk;
- hedging rules that depend on projected delta change;
- local Taylor expansions beyond gamma.

A P&L approximation including speed is:

$$
\Delta V \approx \Delta\Delta S + \frac{1}{2}\Gamma(\Delta S)^2 + \frac{1}{6}\text{Speed}(\Delta S)^3.
$$

This approximation remains local. For large spot moves, full repricing is preferable.

## 2.10 Zomma

## 2.10.1 Definition

Zomma measures the sensitivity of gamma to volatility:

$$
\text{Zomma}=\frac{\partial\Gamma}{\partial\sigma}.
$$

Under Black-Scholes-Merton:

$$
\text{Zomma}=\Gamma\frac{d_1d_2-1}{\sigma}.
$$

## 2.10.2 Intuition

Zomma explains how convexity changes when implied volatility changes. This matters because volatility changes often occur simultaneously with spot moves.

For near-the-money options, an increase in volatility may spread the probability distribution and reduce peak gamma. For far out-of-the-money options, an increase in volatility may bring more probability mass into payoff-relevant regions, changing gamma differently.

## 2.10.3 Practical Use

Zomma matters for:

- short-gamma books during volatility shocks;
- stress testing under simultaneous spot and volatility moves;
- gamma risk limits calibrated to current implied volatility;
- volatility surface scenario analysis;
- hedging books where gamma is expected to change after vol repricing.

A book that is gamma-neutral at the current volatility may not remain gamma-neutral after a volatility shock.

## 2.11 Ultima

## 2.11.1 Definition

Ultima measures the sensitivity of volga to volatility:

$$
\text{Ultima}=\frac{\partial\text{Volga}}{\partial\sigma}
=\frac{\partial^3V}{\partial\sigma^3}.
$$

Under Black-Scholes-Merton, a common expression is:

$$
\text{Ultima}
= -\frac{\nu}{\sigma^2}
\left[d_1d_2(1-d_1d_2)+d_1^2+d_2^2\right].
$$

## 2.11.2 Intuition

Ultima is a third-order volatility sensitivity. It measures how unstable volatility convexity is when volatility itself changes.

In many ordinary equity-option workflows, ultima is less central than vega, volga, vanna, and gamma. However, it becomes more relevant when:

- volatility shocks are large;
- the portfolio is designed to be vega-neutral but not volga-neutral;
- the book contains far out-of-the-money convexity;
- volatility-of-volatility is a key risk driver;
- options on volatility products are included.

## 2.11.3 Practical Use

Ultima is mostly used in advanced volatility books, exotic derivatives, and stress testing. It should not create a false sense of precision. Third-order approximations can be numerically unstable and highly model-dependent.

For large volatility moves, full repricing under a surface-shock model is usually superior to relying on ultima alone.

## 2.12 Veta

## 2.12.1 Definition

Veta measures the sensitivity of vega to calendar time:

$$
\text{Veta}=\frac{\partial\nu}{\partial t}.
$$

Using:

$$
\nu = S e^{-q\tau}\phi(d_1)\sqrt{\tau},
$$

calendar-time veta can be expressed as:

$$
\text{Veta}=\nu\left(q+d_1A_{\tau}-\frac{1}{2\tau}\right),
$$

where:

$$
A_{\tau}=\frac{2(r-q)\tau-d_2\sigma\sqrt{\tau}}{2\tau\sigma\sqrt{\tau}}.
$$

Again, this is the calendar-time convention. If a vendor defines veta as $\partial\nu/\partial\tau$, the sign is reversed.

## 2.12.2 Intuition

Veta describes how volatility exposure decays as time passes. A long-dated option generally has more vega than a short-dated option. As maturity declines, vega usually decays, but the path can depend on moneyness.

For systematic options portfolios, veta helps forecast:

- how quickly volatility exposure rolls down;
- how frequently positions must be rolled to maintain a vega target;
- how term-structure trades lose or gain exposure through time;
- how vega budgets evolve between rebalances.

## 2.13 Vera

## 2.13.1 Definition

Vera is the cross-sensitivity of option value to volatility and interest rates:

$$
\text{Vera}=\frac{\partial^2 V}{\partial\sigma\partial r}
=\frac{\partial\nu}{\partial r}
=\frac{\partial\rho}{\partial\sigma}.
$$

Under Black-Scholes-Merton, for both European calls and puts with the same strike and maturity:

$$
\text{Vera}= -K\tau e^{-r\tau}\phi(d_2)\frac{d_1}{\sigma}.
$$

## 2.13.2 Intuition

Vera is usually less important for short-dated equity options, but it can matter for:

- long-dated options;
- rates-sensitive underlyings;
- FX options;
- structured products;
- macro environments with large rate-volatility co-movement;
- portfolios where discounting and volatility repricing occur together.

For equity-index options, rate shocks can coincide with volatility shocks during inflation, central-bank, or liquidity regimes. Vera helps identify whether a book's rho exposure changes when implied volatility changes.

## 2.14 Cross-Greeks Beyond the Standard List

Institutional risk systems may monitor additional cross-Greeks beyond the common named set.

Examples include:

| Cross-Greek | Definition | Interpretation |
|---|---:|---|
| Delta-rho cross | $\frac{\partial^2 V}{\partial S\partial r}$ | How delta changes with rates |
| Delta-dividend cross | $\frac{\partial^2 V}{\partial S\partial q}$ | How delta changes with dividend assumptions |
| Vega-dividend cross | $\frac{\partial^2 V}{\partial \sigma\partial q}$ | How vega changes with dividend yield |
| Rho convexity | $\frac{\partial^2 V}{\partial r^2}$ | Nonlinear rate exposure |
| Theta convexity | $\frac{\partial^2 V}{\partial t^2}$ | Nonlinear time decay |
| Skew delta | $\frac{\partial V}{\partial \text{skew}}$ | Sensitivity to skew-slope shock |
| Term-structure vega | $\frac{\partial V}{\partial \sigma(T_j)}$ | Sensitivity to tenor-specific volatility shock |

The last two are not pure Black-Scholes Greeks because they require a volatility surface representation. They are often more relevant for real portfolios than some theoretical higher-order Greeks.

## 2.15 Higher-Order Greek Interpretation Table

| Greek | Long Vanilla Option Typical Exposure | Where It Is Largest | Main Failure Mode if Ignored |
|---|---:|---|---|
| Vanna | Can be positive or negative depending on moneyness | Around wings and transition zones | Spot-vol co-movement surprises delta and vega hedges |
| Volga | Often positive in wings, can vary by moneyness | Away from ATM and longer tenors | Vega-neutral book becomes exposed after vol shock |
| Charm | Sign depends on option type and moneyness | Short-dated options near strike | Delta drifts without spot move |
| Color | Large near expiration near ATM | Short-dated ATM options | Gamma limits breached as time passes |
| Speed | High near steep gamma gradients | Near ATM and near expiry | Convexity migrates after spot move |
| Zomma | Depends on moneyness | Short-dated and wing options | Gamma changes after volatility repricing |
| Ultima | Model-sensitive | Vol-convex books and wings | Volga estimate unstable in large vol shock |
| Veta | Usually important for term structure | Medium- to long-dated options | Vega budgets decay or roll unexpectedly |
| Vera | Usually modest for short equity options | Long-dated/rate-sensitive options | Rate-vol interaction missed |

## 2.16 How Higher-Order Greeks Measure Instability in First-Order Greeks

A first-order Greek is a local slope. A higher-order Greek is a measure of how that slope changes.

For delta:

$$
d\Delta \approx \Gamma dS + \text{Vanna} d\sigma + \text{Charm} dt.
$$

Interpretation:

- $\Gamma dS$ is the change in delta caused by spot movement;
- $\text{Vanna}d\sigma$ is the change in delta caused by volatility movement;
- $\text{Charm}dt$ is the change in delta caused by time passing.

For vega:

$$
d\nu \approx \text{Vanna} dS + \text{Volga} d\sigma + \text{Veta} dt + \text{Vera} dr.
$$

Interpretation:

- vanna links vega to spot movement;
- volga links vega to volatility movement;
- veta links vega to time decay;
- vera links vega to rates.

For gamma:

$$
d\Gamma \approx \text{Speed}dS + \text{Zomma}d\sigma + \text{Color}dt.
$$

Interpretation:

- speed explains spot-driven gamma migration;
- zomma explains volatility-driven gamma change;
- color explains time-driven gamma change.

These equations make clear why static Greek reporting is insufficient. A portfolio's current delta, vega, or gamma can be acceptable while its projected delta, vega, or gamma after realistic market moves is not acceptable.

## 2.17 Higher-Order Taylor Expansion of Option P&L

A second-order approximation in spot and volatility is:

$$
\Delta V \approx
\Delta\Delta S
+\nu\Delta\sigma
+\Theta\Delta t
+\frac{1}{2}\Gamma(\Delta S)^2
+\text{Vanna}\Delta S\Delta\sigma
+\frac{1}{2}\text{Volga}(\Delta\sigma)^2.
$$

Variables:

- $\Delta V$ is approximate option P&L;
- $\Delta S$ is the spot change;
- $\Delta\sigma$ is the implied volatility change in decimal units;
- $\Delta t$ is elapsed calendar time in years;
- $\Delta$, $\nu$, $\Theta$, $\Gamma$, vanna, and volga are evaluated at the initial state.

A third-order extension in spot and volatility may include:

$$
\Delta V \approx
\Delta\Delta S
+\nu\Delta\sigma
+\Theta\Delta t
+\frac{1}{2}\Gamma(\Delta S)^2
+\text{Vanna}\Delta S\Delta\sigma
+\frac{1}{2}\text{Volga}(\Delta\sigma)^2
+\frac{1}{6}\text{Speed}(\Delta S)^3
+\frac{1}{2}\text{Zomma}(\Delta S)^2\Delta\sigma
+\frac{1}{2}\text{Ultima}(\Delta\sigma)^3.
$$

The exact coefficients depend on which variables are included and how mixed derivatives are defined. The expression above is a stylized local expansion, not a substitute for full repricing under large moves.

In production stress testing, the preferred hierarchy is:

1. Full repricing under a specified scenario.
2. Surface-aware Greek approximation.
3. Flat-vol Greek approximation.
4. First-order-only approximation.

The larger the shock, the more important full repricing becomes.

## 2.18 Greek Surfaces as Multidimensional Sensitivity Maps

A Greek surface is a map of a Greek across option state variables. For example, a delta surface may be represented as:

$$
\Delta = \Delta(S,K,\tau,r,q,\sigma).
$$

A vega surface may be represented as:

$$
\nu = \nu(S,K,\tau,r,q,\sigma).
$$

In market practice, volatility is not constant. The implied volatility surface may be written as:

$$
\sigma_{\text{imp}}=\sigma_{\text{imp}}(K,T),
$$

or alternatively:

$$
\sigma_{\text{imp}}=\sigma_{\text{imp}}(k_F,T),
$$

where forward log-moneyness is:

$$
k_F = \ln\left(\frac{K}{F_{t,T}}\right).
$$

Under a surface-implied framework, option value becomes:

$$
V = V\left(S,K,T,r,q,\sigma_{\text{imp}}(K,T)\right).
$$

If the surface is parameterized by moneyness, the surface itself changes when spot changes because moneyness changes. This is the origin of surface-aware Greeks.

## 2.19 Flat-Vol Greeks Versus Surface-Aware Greeks

A flat-vol Black-Scholes delta is:

$$
\Delta_{\text{flat}}=\frac{\partial V}{\partial S}\bigg|_{\sigma \text{ fixed}}.
$$

A surface-aware or smile-adjusted delta accounts for the fact that implied volatility may change when spot changes:

$$
\Delta_{\text{smile}}
=\frac{dV}{dS}
=\frac{\partial V}{\partial S}
+\frac{\partial V}{\partial\sigma_{\text{imp}}}
\frac{\partial\sigma_{\text{imp}}}{\partial S}.
$$

Using vega:

$$
\Delta_{\text{smile}}
=\Delta_{\text{flat}}+\nu\frac{\partial\sigma_{\text{imp}}}{\partial S}.
$$

Interpretation:

- $\Delta_{\text{flat}}$ is the spot sensitivity holding implied volatility fixed;
- $\nu\partial\sigma_{\text{imp}}/\partial S$ is the adjustment for implied volatility changing as spot changes;
- the adjustment can be material for skewed surfaces, especially equity index options.

Similarly, a smile-adjusted gamma includes additional terms:

$$
\Gamma_{\text{smile}}
=\frac{d^2V}{dS^2}
=\Gamma_{\text{flat}}
+2\text{Vanna}\frac{\partial\sigma_{\text{imp}}}{\partial S}
+\text{Volga}\left(\frac{\partial\sigma_{\text{imp}}}{\partial S}\right)^2
+\nu\frac{\partial^2\sigma_{\text{imp}}}{\partial S^2}.
$$

This equation shows why vanna and volga become essential under surface-aware risk. Even if the option is evaluated with Black-Scholes locally, the surface dynamics introduce additional exposure terms.

## 2.20 Sticky-Strike, Sticky-Delta, Sticky-Moneyness, and Sticky-Local-Vol Assumptions

Surface-aware Greeks require an assumption about how the implied volatility surface moves when spot changes. Different assumptions produce different Greeks.

## 2.20.1 Sticky-Strike

Under a sticky-strike assumption, implied volatility for a fixed strike and maturity remains unchanged when spot moves:

$$
\frac{\partial\sigma_{\text{imp}}(K,T)}{\partial S}=0.
$$

Then:

$$
\Delta_{\text{smile}}=\Delta_{\text{flat}}.
$$

Sticky-strike is simple and often used for local risk checks. It can be unrealistic in equity markets where implied volatility often rises when spot falls.

## 2.20.2 Sticky-Delta

Under a sticky-delta assumption, implied volatility is stable by option delta bucket. If spot moves, the strike corresponding to a given delta changes, and the volatility assigned to the option may shift according to the surface.

Conceptually:

$$
\sigma_{\text{imp}} = \sigma_{\text{imp}}(\Delta_{\text{option}},T).
$$

Sticky-delta is common in FX options markets, where volatility quotes are often organized by delta. It can produce materially different risk from sticky-strike.

## 2.20.3 Sticky-Moneyness

Under a sticky-moneyness assumption, implied volatility is stable by moneyness or log-moneyness:

$$
\sigma_{\text{imp}} = \sigma_{\text{imp}}(k_F,T),
$$

where:

$$
k_F=\ln\left(\frac{K}{F_{t,T}}\right).
$$

For fixed $K$ and constant $r,q$ over a small move:

$$
\frac{\partial k_F}{\partial S}= -\frac{1}{S}.
$$

Therefore:

$$
\frac{\partial\sigma_{\text{imp}}}{\partial S}
=\frac{\partial\sigma_{\text{imp}}}{\partial k_F}
\frac{\partial k_F}{\partial S}
=-\frac{1}{S}\frac{\partial\sigma_{\text{imp}}}{\partial k_F}.
$$

The smile-adjusted delta becomes:

$$
\Delta_{\text{smile}}
=\Delta_{\text{flat}}
-\frac{\nu}{S}\frac{\partial\sigma_{\text{imp}}}{\partial k_F}.
$$

This adjustment is important when skew slope is steep.

## 2.20.4 Sticky-Local-Vol

Sticky-local-vol assumptions arise from local volatility models where instantaneous volatility depends on spot and time:

$$
\sigma_{\text{local}}=\sigma_{\text{local}}(S,t).
$$

Local-vol dynamics can imply different smile movements from sticky-strike or sticky-delta assumptions. Under local volatility, implied volatility may move in a way constrained by the calibrated local-vol surface and the forward distribution.

Sticky-local-vol is more model-dependent and less transparent than sticky-strike or sticky-moneyness, but it can be useful for exotic derivatives and path-dependent products.

## 2.20.5 Comparison Table

| Surface Dynamic Assumption | What Is Held Fixed? | Common Use | Main Risk |
|---|---|---|---|
| Sticky strike | Vol at fixed $K,T$ | Simple equity risk checks | Understates spot-vol interaction under skew |
| Sticky delta | Vol at fixed delta bucket | FX options, delta-quoted surfaces | Depends on delta convention and premium adjustment |
| Sticky moneyness | Vol at fixed moneyness or log-moneyness | Equity and index scenario analysis | Requires stable moneyness parameterization |
| Sticky local vol | Local volatility function | Exotic and path-dependent books | Model-dependent and less intuitive |
| Empirical beta surface | Vol response estimated statistically | Systematic risk and stress models | Estimation error and regime instability |

## 2.21 Smile-Adjusted Vanna and Volga

When a volatility surface is present, vanna and volga can refer to different things.

The **flat-vol vanna** is:

$$
\text{Vanna}_{\text{flat}}=\frac{\partial^2V}{\partial S\partial\sigma}.
$$

The **surface-aware delta change with volatility** may include how the surface slope itself changes:

$$
\frac{d\Delta_{\text{smile}}}{d\sigma}
=\frac{\partial\Delta}{\partial\sigma}
+\frac{\partial}{\partial\sigma}\left(\nu\frac{\partial\sigma_{\text{imp}}}{\partial S}\right).
$$

This can include terms involving:

- flat-vol vanna;
- volga;
- skew slope;
- skew curvature;
- surface parameter sensitivity;
- empirical spot-vol beta.

The practical implication is that reported vanna may not fully capture real smile risk unless the surface dynamics are specified. For systematic research, it is usually safer to store both:

1. model Greeks under documented assumptions;
2. scenario P&L under explicit surface shocks.

## 2.22 How Greeks Evolve When Multiple Inputs Change Simultaneously

Real markets rarely move one variable at a time. In equity stress, spot may fall, implied volatility may rise, skew may steepen, correlation may increase, and liquidity may deteriorate simultaneously.

Let the state change be:

$$
d\mathbf{x}=\begin{bmatrix}dS & d\sigma & dr & dq & dt\end{bmatrix}^{\top}.
$$

A second-order local approximation is:

$$
dV \approx \nabla V^{\top}d\mathbf{x}+rac{1}{2}d\mathbf{x}^{\top}\mathbf{H}_Vd\mathbf{x}.
$$

This equation defines all variables:

- $dV$ is the approximate change in option value;
- $\nabla V$ is the vector of first-order Greeks;
- $d\mathbf{x}$ is the vector of state changes;
- $\mathbf{H}_V$ is the Hessian of second-order sensitivities.

For spot and volatility only, this reduces to:

$$
dV \approx \Delta dS + \nu d\sigma
+\frac{1}{2}\Gamma(dS)^2
+\text{Vanna}dSd\sigma
+\frac{1}{2}\text{Volga}(d\sigma)^2.
$$

The cross term $\text{Vanna}dSd\sigma$ is essential when spot and volatility are correlated.

If empirical spot-vol co-movement is approximated by:

$$
d\sigma \approx \beta_{\sigma,S}\frac{dS}{S},
$$

then the spot-vol cross contribution becomes:

$$
\text{Vanna}dS d\sigma
\approx
\text{Vanna}\,dS\,\beta_{\sigma,S}\frac{dS}{S}.
$$

This shows that vanna can effectively modify realized curvature under empirical surface dynamics.

## 2.23 Why Two Options with Similar Delta Can Have Very Different Risk

Delta alone is an incomplete description of option risk. Two options may both have delta near $0.30$ but have very different gamma, vega, vanna, volga, liquidity, and event exposure.

## 2.23.1 Example Comparison

| Attribute | Option A | Option B | Risk Implication |
|---|---|---|---|
| Underlying | Broad equity index | Single stock near earnings | Single stock has idiosyncratic gap risk |
| Delta | $0.30$ | $0.30$ | Similar first-order directional exposure |
| Maturity | 7 days | 180 days | Short option has higher gamma; long option has higher vega |
| Moneyness | Slightly OTM | Farther OTM but high vol | Similar delta can arise from different distributions |
| Gamma | High | Lower | Option A delta changes faster with spot |
| Vega | Low to moderate | High | Option B more exposed to IV repricing |
| Vanna | Material near skew transition | Material due to high event vol | Spot-vol interaction differs |
| Volga | Moderate | Potentially high | Long-dated/event option can have volatility convexity |
| Liquidity | Tight index market | Wider single-name market | Execution quality differs |
| Failure mode | Pin/gamma risk | Earnings crush or gap risk | Same delta does not imply same P&L behavior |

## 2.23.2 Mathematical Explanation

Delta is:

$$
\Delta_C=e^{-q\tau}N(d_1).
$$

For a target call delta $\Delta_C^*$, many combinations of $K$, $\tau$, $\sigma$, $r$, and $q$ can produce the same $d_1$ and similar delta. However, gamma and vega are:

$$
\Gamma=\frac{e^{-q\tau}\phi(d_1)}{S\sigma\sqrt{\tau}},
$$

$$
\nu=S e^{-q\tau}\phi(d_1)\sqrt{\tau}.
$$

For similar $d_1$, gamma scales roughly like:

$$
\Gamma \propto \frac{1}{S\sigma\sqrt{\tau}},
$$

while vega scales roughly like:

$$
\nu \propto S\sqrt{\tau}.
$$

Thus, shorter maturity increases gamma and decreases vega, while longer maturity decreases gamma and increases vega. Similar delta does not imply similar convexity or volatility exposure.

## 2.24 Dynamic Greek Surfaces and Risk Buckets

A production options system should not merely report aggregate portfolio delta and vega. It should bucket exposures across dimensions that explain risk.

Common Greek buckets include:

| Dimension | Example Buckets | Why It Matters |
|---|---|---|
| Underlying | ticker, index, ETF, future | Directional and liquidity risk |
| Sector | GICS sector or internal sector | Sector concentration and factor risk |
| Country / region | US, Canada, Europe, Japan, EM | Macro and currency risk |
| Currency | USD, CAD, EUR, JPY | FX and funding risk |
| Maturity | 0-7d, 8-30d, 31-90d, 91-365d, 1y+ | Term-structure exposure |
| Delta bucket | 5-delta, 10-delta, 25-delta, ATM | Skew and wing exposure |
| Moneyness | OTM put, ATM, OTM call | Crash/upside convexity |
| Volatility tenor | 1m, 3m, 6m, 1y | Vega curve exposure |
| Event status | pre-earnings, post-earnings, no event | Event-volatility risk |
| Liquidity | tight, medium, wide spread | Implementation feasibility |

A portfolio Greek tensor may be represented as:

$$
G_{b_1,b_2,\ldots,b_m}^{(k)}
=\sum_{i\in\mathcal{B}(b_1,b_2,\ldots,b_m)} Q_i M_i G_i^{(k)},
$$

where:

- $G_{b_1,b_2,\ldots,b_m}^{(k)}$ is Greek $k$ aggregated over a bucket combination;
- $Q_i$ is the signed contract quantity of option $i$;
- $M_i$ is the contract multiplier;
- $G_i^{(k)}$ is the per-option Greek;
- $\mathcal{B}(b_1,b_2,\ldots,b_m)$ is the set of options belonging to the specified bucket combination.

This representation is essential for risk limits. A book can be vega-neutral in aggregate while heavily long short-dated single-name vega and short long-dated index vega. Aggregate neutrality can hide basis risk.

## 2.25 Greek Surfaces for Research Signals

Higher-order Greeks can be used as state variables in systematic research, but they must be handled carefully.

Examples of research features include:

$$
\text{VannaIntensity}_{i,t}=\frac{|\text{Vanna}_{i,t}|}{|\Delta_{i,t}|+\epsilon},
$$

where $\epsilon>0$ prevents division by zero. This feature measures the instability of delta with respect to volatility relative to current delta magnitude.

A volga-to-vega ratio can be defined as:

$$
\text{VolgaVegaRatio}_{i,t}=\frac{\text{Volga}_{i,t}}{|\nu_{i,t}|+\epsilon}.
$$

This measures the convexity of volatility exposure relative to first-order volatility exposure.

A gamma-theta efficiency feature can be defined as:

$$
\text{GammaThetaEfficiency}_{i,t}=\frac{\Gamma_{i,t}S_{i,t}^2}{|\Theta_{i,t}|+\epsilon}.
$$

This compares convexity exposure to time decay cost. It is not automatically an alpha signal; it is a structural descriptor that may be used in screening, ranking, or portfolio construction.

A systematic process should test whether such features predict subsequent risk-adjusted returns after transaction costs, slippage, borrow costs, and realistic execution assumptions. Higher-order Greeks are not magic predictors. They are risk descriptors that may help condition strategy selection.

## 2.26 Implementation Caveats for Higher-Order Greeks

## 2.26.1 Numerical Instability

Higher-order Greeks can be numerically unstable, especially near expiration, deep in the wings, or for options with very low prices. Finite-difference estimates are sensitive to bump size.

For a generic finite-difference estimate of vega:

$$
\nu \approx \frac{V(\sigma+h)-V(\sigma-h)}{2h},
$$

where $h$ is the volatility bump. If $h$ is too small, floating-point noise may dominate. If $h$ is too large, the estimate is no longer local.

## 2.26.2 Stale and Bad Quotes

Higher-order Greeks amplify data errors. A stale implied volatility mark can produce distorted vanna, volga, and zomma. Before computing higher-order Greeks, a data pipeline should filter:

- crossed markets;
- zero bids where inappropriate;
- extremely wide spreads;
- stale quotes;
- arbitrage violations;
- impossible implied volatilities;
- options with unreliable open interest or volume.

## 2.26.3 Model Dependence

Higher-order Greeks are model-dependent. A Black-Scholes vanna differs from a local-vol vanna or a stochastic-volatility vanna. A vendor Greek may include surface dynamics that are not documented in raw data.

A production system should store:

- pricing model version;
- surface construction method;
- interpolation method;
- extrapolation rules;
- rate and dividend inputs;
- Greek bump sizes if finite differences are used;
- timestamp and data source.

## 2.26.4 Scaling and Reporting

Vega, volga, vanna, and other Greeks may be reported per decimal volatility unit or per volatility point. Inconsistent scaling can create major risk-reporting errors.

Recommended convention:

| Quantity | Raw Mathematical Unit | Desk-Friendly Unit |
|---|---|---|
| Vega | per 1.00 volatility | per 1 vol point = raw vega / 100 |
| Volga | per $(1.00)^2$ volatility | per vol-point squared = raw volga / 10,000 |
| Vanna | per $1 spot \times 1.00 vol$ | per $1 spot \times 1 vol point$ = raw vanna / 100 |
| Rho | per 1.00 rate | per bp = raw rho / 10,000 |
| Charm | delta change per year | delta change per day = raw charm / 365 |
| Color | gamma change per year | gamma change per day = raw color / 365 |

The annualization denominator for time Greeks may be 365 or 252 depending on system convention. Options decay over calendar time, but risk reports often use business-day approximations. The choice should be explicit.

## 2.27 Python Code: Analytical Higher-Order Greeks

The following code implements selected analytical higher-order Greeks under Black-Scholes-Merton. It builds on the same conventions used in Part 1.

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
    """Inputs for European Black-Scholes-Merton pricing and Greeks.

    Parameters
    ----------
    spot:
        Current underlying spot price. Must be positive.
    strike:
        Option strike price. Must be positive.
    tau:
        Time to maturity in years. Must be positive.
    rate:
        Continuously compounded risk-free rate as decimal.
    dividend_yield:
        Continuous dividend yield as decimal.
    volatility:
        Annualized volatility as decimal.
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


def validate_bsm_inputs(x: BSMInputs) -> None:
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
    validate_bsm_inputs(x)
    vol_sqrt_tau = x.volatility * math.sqrt(x.tau)
    d1 = (
        math.log(x.spot / x.strike)
        + (x.rate - x.dividend_yield + 0.5 * x.volatility**2) * x.tau
    ) / vol_sqrt_tau
    d2 = d1 - vol_sqrt_tau
    return d1, d2


def bsm_price(x: BSMInputs) -> float:
    d1, d2 = bsm_d1_d2(x)
    df_r = math.exp(-x.rate * x.tau)
    df_q = math.exp(-x.dividend_yield * x.tau)
    if x.option_type == "call":
        return x.spot * df_q * norm.cdf(d1) - x.strike * df_r * norm.cdf(d2)
    return x.strike * df_r * norm.cdf(-d2) - x.spot * df_q * norm.cdf(-d1)


def core_and_higher_greeks(x: BSMInputs) -> dict[str, float]:
    """Return selected core and higher-order BSM Greeks.

    Conventions
    -----------
    - Vega is per 1.00 volatility unit.
    - Volga is per 1.00 volatility unit squared.
    - Vanna is per 1 spot unit and per 1.00 volatility unit.
    - Charm, color, and veta use calendar-time convention d/dt.
    - Daily versions use a 365-day calendar convention.
    """
    d1, d2 = bsm_d1_d2(x)
    s, k, tau = x.spot, x.strike, x.tau
    r, q, sigma = x.rate, x.dividend_yield, x.volatility
    sqrt_tau = math.sqrt(tau)
    df_r = math.exp(-r * tau)
    df_q = math.exp(-q * tau)
    phi_d1 = norm.pdf(d1)
    phi_d2 = norm.pdf(d2)

    gamma = df_q * phi_d1 / (s * sigma * sqrt_tau)
    vega = s * df_q * phi_d1 * sqrt_tau

    if x.option_type == "call":
        delta = df_q * norm.cdf(d1)
        theta = (
            -s * df_q * phi_d1 * sigma / (2.0 * sqrt_tau)
            - r * k * df_r * norm.cdf(d2)
            + q * s * df_q * norm.cdf(d1)
        )
        rho = k * tau * df_r * norm.cdf(d2)
        charm = q * df_q * norm.cdf(d1)
    else:
        delta = df_q * (norm.cdf(d1) - 1.0)
        theta = (
            -s * df_q * phi_d1 * sigma / (2.0 * sqrt_tau)
            + r * k * df_r * norm.cdf(-d2)
            - q * s * df_q * norm.cdf(-d1)
        )
        rho = -k * tau * df_r * norm.cdf(-d2)
        charm = q * df_q * (norm.cdf(d1) - 1.0)

    # d(d1)/d(tau). Calendar-time derivatives are negative of tau derivatives.
    a_tau = (2.0 * (r - q) * tau - d2 * sigma * sqrt_tau) / (
        2.0 * tau * sigma * sqrt_tau
    )

    vanna = -df_q * phi_d1 * d2 / sigma
    volga = vega * d1 * d2 / sigma
    charm = charm - df_q * phi_d1 * a_tau
    color = gamma * (q + 1.0 / (2.0 * tau) + d1 * a_tau)
    speed = -(gamma / s) * (1.0 + d1 / (sigma * sqrt_tau))
    zomma = gamma * (d1 * d2 - 1.0) / sigma
    ultima = -(vega / sigma**2) * (
        d1 * d2 * (1.0 - d1 * d2) + d1**2 + d2**2
    )
    veta = vega * (q + d1 * a_tau - 1.0 / (2.0 * tau))
    vera = -k * tau * df_r * phi_d2 * d1 / sigma

    return {
        "price": bsm_price(x),
        "delta": delta,
        "gamma": gamma,
        "theta_annual": theta,
        "vega_per_1_vol": vega,
        "rho_per_1_rate": rho,
        "vanna_per_1_spot_1_vol": vanna,
        "vanna_per_1_spot_1_vol_point": vanna / 100.0,
        "volga_per_1_vol_squared": volga,
        "volga_per_vol_point_squared": volga / 10_000.0,
        "charm_annual": charm,
        "charm_daily": charm / 365.0,
        "color_annual": color,
        "color_daily": color / 365.0,
        "speed": speed,
        "zomma_per_1_vol": zomma,
        "ultima_per_1_vol_cubed": ultima,
        "veta_annual": veta,
        "veta_daily": veta / 365.0,
        "vera_per_1_rate_1_vol": vera,
    }


example = BSMInputs(
    spot=100.0,
    strike=100.0,
    tau=30 / 365,
    rate=0.04,
    dividend_yield=0.01,
    volatility=0.20,
    option_type="call",
)

print(pd.Series(core_and_higher_greeks(example)).round(8))
```

## 2.28 Python Code: Finite-Difference Cross-Checks

Analytical higher-order Greeks should be tested against finite-difference approximations. The following code provides a generic central-difference checker.

```python
def replace_input(x: BSMInputs, **updates) -> BSMInputs:
    """Return a new BSMInputs object with selected fields replaced."""
    data = x.__dict__.copy()
    data.update(updates)
    return BSMInputs(**data)


def central_difference_first(
    x: BSMInputs,
    field: str,
    bump: float,
    value_func=bsm_price,
) -> float:
    """Central finite difference for first derivative with respect to one field."""
    if bump <= 0:
        raise ValueError("bump must be positive")
    x_up = replace_input(x, **{field: getattr(x, field) + bump})
    x_dn = replace_input(x, **{field: getattr(x, field) - bump})
    return (value_func(x_up) - value_func(x_dn)) / (2.0 * bump)


def central_difference_second(
    x: BSMInputs,
    field: str,
    bump: float,
    value_func=bsm_price,
) -> float:
    """Central finite difference for second derivative with respect to one field."""
    if bump <= 0:
        raise ValueError("bump must be positive")
    x_up = replace_input(x, **{field: getattr(x, field) + bump})
    x_dn = replace_input(x, **{field: getattr(x, field) - bump})
    return (value_func(x_up) - 2.0 * value_func(x) + value_func(x_dn)) / bump**2


def central_difference_cross(
    x: BSMInputs,
    field_1: str,
    field_2: str,
    bump_1: float,
    bump_2: float,
    value_func=bsm_price,
) -> float:
    """Central finite difference for a mixed second derivative."""
    if bump_1 <= 0 or bump_2 <= 0:
        raise ValueError("bumps must be positive")

    x_pp = replace_input(
        x,
        **{
            field_1: getattr(x, field_1) + bump_1,
            field_2: getattr(x, field_2) + bump_2,
        },
    )
    x_pm = replace_input(
        x,
        **{
            field_1: getattr(x, field_1) + bump_1,
            field_2: getattr(x, field_2) - bump_2,
        },
    )
    x_mp = replace_input(
        x,
        **{
            field_1: getattr(x, field_1) - bump_1,
            field_2: getattr(x, field_2) + bump_2,
        },
    )
    x_mm = replace_input(
        x,
        **{
            field_1: getattr(x, field_1) - bump_1,
            field_2: getattr(x, field_2) - bump_2,
        },
    )

    return (value_func(x_pp) - value_func(x_pm) - value_func(x_mp) + value_func(x_mm)) / (
        4.0 * bump_1 * bump_2
    )


analytic = core_and_higher_greeks(example)
checks = {
    "delta_fd": central_difference_first(example, "spot", 0.01),
    "gamma_fd": central_difference_second(example, "spot", 0.01),
    "vega_fd": central_difference_first(example, "volatility", 0.0001),
    "volga_fd": central_difference_second(example, "volatility", 0.0001),
    "vanna_fd": central_difference_cross(example, "spot", "volatility", 0.01, 0.0001),
}

comparison = pd.DataFrame(
    {
        "analytic": {
            "delta": analytic["delta"],
            "gamma": analytic["gamma"],
            "vega": analytic["vega_per_1_vol"],
            "volga": analytic["volga_per_1_vol_squared"],
            "vanna": analytic["vanna_per_1_spot_1_vol"],
        },
        "finite_difference": {
            "delta": checks["delta_fd"],
            "gamma": checks["gamma_fd"],
            "vega": checks["vega_fd"],
            "volga": checks["volga_fd"],
            "vanna": checks["vanna_fd"],
        },
    }
)
comparison["absolute_error"] = (
    comparison["analytic"] - comparison["finite_difference"]
).abs()
print(comparison)
```

Finite-difference tests should be part of model validation, but they are not definitive proof of correctness. They depend on bump sizes, numerical precision, and the smoothness of the pricing function.

## 2.29 Python Code: Greek Surface Visualization Across Strike and Maturity

The following code generates surfaces for delta, gamma, vega, theta, vanna, and volga over strike and maturity using synthetic inputs.

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def build_greek_surface_data(
    spot: float = 100.0,
    strikes: np.ndarray | None = None,
    maturities: np.ndarray | None = None,
    rate: float = 0.04,
    dividend_yield: float = 0.01,
    volatility: float = 0.20,
    option_type: OptionType = "call",
) -> pd.DataFrame:
    """Create a grid of core and higher-order Greeks across strike and maturity."""
    if strikes is None:
        strikes = np.linspace(70.0, 130.0, 61)
    if maturities is None:
        maturities = np.linspace(7 / 365, 365 / 365, 50)

    if spot <= 0:
        raise ValueError("spot must be positive")
    if np.any(strikes <= 0):
        raise ValueError("all strikes must be positive")
    if np.any(maturities <= 0):
        raise ValueError("all maturities must be positive")

    rows = []
    for tau in maturities:
        for strike in strikes:
            x = BSMInputs(
                spot=spot,
                strike=float(strike),
                tau=float(tau),
                rate=rate,
                dividend_yield=dividend_yield,
                volatility=volatility,
                option_type=option_type,
            )
            g = core_and_higher_greeks(x)
            rows.append(
                {
                    "strike": float(strike),
                    "tau_years": float(tau),
                    "forward_moneyness": spot * math.exp((rate - dividend_yield) * tau) / strike,
                    **g,
                }
            )
    return pd.DataFrame(rows)


def plot_surface(
    df: pd.DataFrame,
    z_column: str,
    title: str,
) -> None:
    """Plot a 3D surface for one Greek across strike and maturity."""
    pivot = df.pivot_table(index="tau_years", columns="strike", values=z_column)
    x_values = pivot.columns.values
    y_values = pivot.index.values
    x_grid, y_grid = np.meshgrid(x_values, y_values)
    z_grid = pivot.values

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(x_grid, y_grid, z_grid, linewidth=0, antialiased=True)
    ax.set_xlabel("Strike")
    ax.set_ylabel("Maturity in years")
    ax.set_zlabel(z_column)
    ax.set_title(title)
    plt.show()


surface_df = build_greek_surface_data(option_type="call")

plot_surface(surface_df, "delta", "Call delta surface")
plot_surface(surface_df, "gamma", "Call gamma surface")
plot_surface(surface_df, "vega_per_1_vol", "Call vega surface")
plot_surface(surface_df, "theta_annual", "Call theta surface")
plot_surface(surface_df, "vanna_per_1_spot_1_vol", "Call vanna surface")
plot_surface(surface_df, "volga_per_1_vol_squared", "Call volga surface")
```

Expected observations:

- Delta transitions from near one to near zero as strike increases for calls.
- Gamma is concentrated near at-the-money and short maturities.
- Vega is generally larger for longer maturities and near at-the-money-forward.
- Theta is most negative where time value is most exposed to decay.
- Vanna changes sign and magnitude across moneyness and maturity.
- Volga is often more relevant away from at-the-money regions and for volatility-convex positions.

## 2.30 Python Code: Synthetic Smile-Adjusted Delta

The following example constructs a simple synthetic implied volatility smile as a function of forward log-moneyness and computes a smile-adjusted delta under a sticky-moneyness assumption.

The synthetic surface is not market calibrated. It is for educational illustration.

```python
def synthetic_iv_from_log_moneyness(
    k_f: np.ndarray | float,
    tau: np.ndarray | float,
    base_vol: float = 0.20,
    skew: float = -0.30,
    curvature: float = 0.50,
    term_slope: float = 0.02,
) -> np.ndarray | float:
    """Synthetic implied volatility function.

    Parameters
    ----------
    k_f:
        Forward log-moneyness, log(K / F).
    tau:
        Maturity in years.
    base_vol:
        ATM baseline volatility.
    skew:
        Linear slope with respect to forward log-moneyness.
        Negative skew means lower strikes have higher implied volatility.
    curvature:
        Smile curvature.
    term_slope:
        Simple term-structure slope.

    Returns
    -------
    Synthetic implied volatility as a decimal annualized number.
    """
    iv = base_vol + skew * k_f + curvature * np.asarray(k_f) ** 2 + term_slope * np.sqrt(tau)
    return np.maximum(iv, 0.03)


def synthetic_iv_slope_k(
    k_f: np.ndarray | float,
    skew: float = -0.30,
    curvature: float = 0.50,
) -> np.ndarray | float:
    """Derivative of synthetic IV with respect to forward log-moneyness."""
    return skew + 2.0 * curvature * np.asarray(k_f)


def smile_adjusted_delta_sticky_moneyness(x: BSMInputs) -> dict[str, float]:
    """Compute flat and smile-adjusted delta under synthetic sticky-moneyness IV.

    The option is repriced with the synthetic implied volatility at its current
    forward log-moneyness. The smile adjustment uses:
        delta_smile = delta_flat - vega / S * d sigma / d k_f.
    """
    forward = x.spot * math.exp((x.rate - x.dividend_yield) * x.tau)
    k_f = math.log(x.strike / forward)
    iv = float(synthetic_iv_from_log_moneyness(k_f, x.tau))
    iv_slope = float(synthetic_iv_slope_k(k_f))

    x_iv = replace_input(x, volatility=iv)
    greeks = core_and_higher_greeks(x_iv)
    delta_flat = greeks["delta"]
    vega = greeks["vega_per_1_vol"]
    delta_smile = delta_flat - (vega / x.spot) * iv_slope

    return {
        "forward_log_moneyness": k_f,
        "synthetic_iv": iv,
        "iv_slope_to_k": iv_slope,
        "delta_flat": delta_flat,
        "delta_smile_sticky_moneyness": delta_smile,
        "smile_adjustment": delta_smile - delta_flat,
    }


x = BSMInputs(
    spot=100.0,
    strike=95.0,
    tau=60 / 365,
    rate=0.04,
    dividend_yield=0.01,
    volatility=0.20,  # replaced internally by synthetic IV
    option_type="put",
)

print(pd.Series(smile_adjusted_delta_sticky_moneyness(x)).round(6))
```

The output compares flat-vol delta and sticky-moneyness smile-adjusted delta. In a real system, the synthetic volatility function would be replaced by a calibrated implied-volatility surface with controlled interpolation and extrapolation.

## 2.31 Python Code: Surface Shock Engine for Higher-Order Risk

This example applies simple volatility surface shocks and compares full repricing to a Greek approximation using vega, vanna, and volga.

```python
def price_with_synthetic_surface(x: BSMInputs) -> float:
    """Price an option using the synthetic IV surface."""
    forward = x.spot * math.exp((x.rate - x.dividend_yield) * x.tau)
    k_f = math.log(x.strike / forward)
    iv = float(synthetic_iv_from_log_moneyness(k_f, x.tau))
    return bsm_price(replace_input(x, volatility=iv))


def shocked_surface_iv(
    k_f: float,
    tau: float,
    parallel_shift: float = 0.0,
    skew_shock: float = 0.0,
    curvature_shock: float = 0.0,
) -> float:
    """Return synthetic IV after parallel, skew, and curvature shocks.

    Shocks are in decimal volatility units. For example, 0.05 is 5 vol points.
    The skew shock multiplies log-moneyness and therefore steepens or flattens
    the smile depending on sign.
    """
    base = synthetic_iv_from_log_moneyness(k_f, tau)
    shocked = base + parallel_shift + skew_shock * k_f + curvature_shock * k_f**2
    return float(max(shocked, 0.03))


def surface_shock_reprice(
    x: BSMInputs,
    spot_return: float,
    parallel_vol_shift: float,
    skew_shock: float = 0.0,
    curvature_shock: float = 0.0,
) -> dict[str, float]:
    """Compare full repricing and local Greek approximation under a surface shock."""
    if spot_return <= -1.0:
        raise ValueError("spot_return must be greater than -100%")

    forward_0 = x.spot * math.exp((x.rate - x.dividend_yield) * x.tau)
    k_f_0 = math.log(x.strike / forward_0)
    iv_0 = float(synthetic_iv_from_log_moneyness(k_f_0, x.tau))
    x0 = replace_input(x, volatility=iv_0)
    p0 = bsm_price(x0)
    g0 = core_and_higher_greeks(x0)

    new_spot = x.spot * (1.0 + spot_return)
    forward_1 = new_spot * math.exp((x.rate - x.dividend_yield) * x.tau)
    k_f_1 = math.log(x.strike / forward_1)
    iv_1 = shocked_surface_iv(
        k_f_1,
        x.tau,
        parallel_shift=parallel_vol_shift,
        skew_shock=skew_shock,
        curvature_shock=curvature_shock,
    )
    x1 = replace_input(x, spot=new_spot, volatility=iv_1)
    p1 = bsm_price(x1)

    d_s = new_spot - x.spot
    d_vol = iv_1 - iv_0
    greek_approx = (
        g0["delta"] * d_s
        + g0["vega_per_1_vol"] * d_vol
        + 0.5 * g0["gamma"] * d_s**2
        + g0["vanna_per_1_spot_1_vol"] * d_s * d_vol
        + 0.5 * g0["volga_per_1_vol_squared"] * d_vol**2
    )

    return {
        "initial_price": p0,
        "repriced_price": p1,
        "full_repricing_pnl": p1 - p0,
        "greek_approx_pnl": greek_approx,
        "approximation_error": (p1 - p0) - greek_approx,
        "initial_iv": iv_0,
        "shocked_iv": iv_1,
        "spot_change": d_s,
        "vol_change": d_vol,
    }


shock_example = BSMInputs(
    spot=100.0,
    strike=95.0,
    tau=90 / 365,
    rate=0.04,
    dividend_yield=0.01,
    volatility=0.20,
    option_type="put",
)

result = surface_shock_reprice(
    shock_example,
    spot_return=-0.05,
    parallel_vol_shift=0.04,
    skew_shock=-0.10,
    curvature_shock=0.20,
)
print(pd.Series(result).round(6))
```

The approximation error should be expected to grow as shocks become larger, surface curvature becomes stronger, or the option approaches expiration.

## 2.32 Production Notes: Higher-Performance Implementations

The Python examples are designed for clarity. Institutional-scale systems require additional engineering.

## 2.32.1 Vectorization

For large option universes, compute Greeks in vectorized arrays rather than Python loops. Inputs can be stored in arrays:

$$
\mathbf{S},\mathbf{K},\boldsymbol{\tau},\mathbf{r},\mathbf{q},\boldsymbol{\sigma} \in \mathbb{R}^N.
$$

The vectorized $d_1$ calculation is:

$$
\mathbf{d}_1=rac{\ln(\mathbf{S}/\mathbf{K})+(\mathbf{r}-\mathbf{q}+\frac{1}{2}\boldsymbol{\sigma}^2)\boldsymbol{\tau}}{\boldsymbol{\sigma}\sqrt{\boldsymbol{\tau}}}.
$$

Vectorization reduces runtime and improves reproducibility.

## 2.32.2 Scaling Beyond Pandas

For millions of option records, consider:

- NumPy for dense vectorized computation;
- Numba for JIT compilation of pricing kernels;
- Polars for faster tabular transformations;
- PyArrow or Parquet for columnar storage;
- Spark for distributed historical backtests;
- C++ or Rust for low-latency intraday risk engines;
- Scala or Java for enterprise integration;
- GPU acceleration only if data transfer and memory layout justify it.

## 2.32.3 Monitoring

Higher-order Greek engines should monitor:

- number of options successfully priced;
- number of rejected quotes;
- implied-volatility inversion failures;
- extreme Greek values;
- stale quote counts;
- missing dividend or rate inputs;
- surface calibration errors;
- reconciliation differences versus vendor Greeks;
- runtime and memory usage;
- versioned model and surface parameters.

## 2.33 Quality-Control Checklist for Part 2 Concepts

| Check | Why It Matters |
|---|---|
| Are time-Greek sign conventions documented? | Charm, color, and veta signs differ across vendors |
| Are vega and volga scaling conventions explicit? | Decimal-vol versus vol-point scaling can differ by 100x or 10,000x |
| Are surface dynamics specified? | Sticky-strike and sticky-moneyness Greeks can differ materially |
| Are higher-order Greeks reconciled to finite differences? | Analytical implementation errors are common |
| Are bad quotes filtered before computing higher-order Greeks? | Higher-order Greeks amplify data errors |
| Are large shocks evaluated by full repricing? | Taylor approximations fail under nonlinear moves |
| Are single-stock event risks separated? | Earnings and corporate actions can dominate model Greeks |
| Are bucketed exposures reviewed? | Aggregate neutrality can hide concentrated risk |
| Are model versions stored? | Reproducibility requires versioned methodology |
| Are vendor differences explained? | Greek definitions vary across systems |

## 2.34 Summary of Part 2

Part 2 extended the core Greek framework into higher-order sensitivities and dynamic Greek surfaces.

Key points:

1. Higher-order Greeks measure the instability of first-order Greeks.
2. Vanna links spot and volatility risk; it is essential when spot and volatility co-move.
3. Volga measures volatility convexity and can destabilize vega-neutral books.
4. Charm measures delta drift through time.
5. Color measures gamma drift through time, especially near expiration.
6. Speed measures how gamma changes as spot moves.
7. Zomma measures how gamma changes as volatility changes.
8. Ultima measures instability in volatility convexity.
9. Veta measures the decay of vega through time.
10. Vera measures rate-volatility interaction.
11. Greek surfaces map sensitivities across strike, maturity, moneyness, volatility, and rates.
12. Smile-adjusted Greeks require assumptions about surface dynamics.
13. Sticky-strike, sticky-delta, sticky-moneyness, and sticky-local-vol assumptions can produce different risk estimates.
14. Similar delta does not imply similar gamma, vega, vanna, volga, liquidity, or event risk.
15. Production systems should combine analytical Greeks, finite-difference checks, bucketed exposure aggregation, and full repricing scenario analysis.

The next installment will cover Part 3: Practical Hedging Dynamics and Greek-Based Trading, including delta hedging, gamma scalping, theta-gamma trade-offs, vega and skew hedging, discrete hedging error, transaction costs, and Greek-based P&L decomposition.
