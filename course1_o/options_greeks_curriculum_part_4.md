# Institutional Options Greeks, Systematic Strategy, and Regime-Aware Portfolio Construction Curriculum

## Completed Installment

This installment contains:

- Part 4: Volatility Surface, Skew, Term Structure, and Regime Interpretation.

The document is educational and research-oriented. It is not personalized investment advice, a live trading recommendation, or a claim that any option strategy produces guaranteed alpha.

---

# Part 4: Volatility Surface, Skew, Term Structure, and Regime Interpretation

**Level:** Advanced

## 4.1 Purpose of Part 4

The Black-Scholes-Merton framework in Part 1 used one volatility input, $\sigma$, for every strike and maturity. Real option markets do not behave this way. Options with different strikes and maturities usually imply different volatilities. The collection of these implied volatilities is called the **implied volatility surface**.

The volatility surface is not a decorative chart. It is a compact representation of market prices for distributional risk, including downside protection demand, upside speculation, jump risk, event risk, liquidity, funding, dealer inventory, and risk premia. For institutional options research, the surface is a state variable that affects valuation, Greeks, hedging, P&L attribution, portfolio construction, stress testing, and regime interpretation.

Part 4 explains how to move from flat-volatility thinking to surface-aware thinking. The key message is:

$$
\text{Option risk is not only exposure to volatility level. It is exposure to the shape, dynamics, and regime behavior of the volatility surface.}
$$

## 4.2 Baseline Notation

Let:

- $S_t$ be the underlying spot price at time $t$;
- $K$ be the option strike;
- $T$ be the option maturity date;
- $\tau=T-t$ be time to maturity in years;
- $r$ be the continuously compounded risk-free rate;
- $q$ be the continuous dividend yield;
- $F_{t,T}=S_t e^{(r-q)\tau}$ be the forward price under constant $r$ and $q$;
- $\sigma_{\text{imp}}(K,T)$ be implied volatility indexed by strike and maturity;
- $k_F=\ln(K/F_{t,T})$ be forward log-moneyness;
- $\Delta$, $\Gamma$, $\Theta$, $\nu$, $\rho$ be the usual core Greeks;
- vanna and volga be higher-order spot-volatility and volatility-convexity exposures.

A volatility surface may be represented as:

$$
\sigma_{\text{imp}} = \sigma_{\text{imp}}(K,T),
$$

or, more robustly for cross-maturity comparison, as:

$$
\sigma_{\text{imp}} = \sigma_{\text{imp}}(k_F,\tau).
$$

The second representation is often preferable because it measures strike relative to the forward price. A strike that is 5% below spot may not be 5% below the forward if rates, dividends, or carry are material.

## 4.3 From Flat Volatility to an Implied Volatility Surface

## 4.3.1 Implied Volatility for One Option

For a European option with market price $V^{\text{mkt}}$, implied volatility is the value $\sigma_{\text{imp}}$ that satisfies:

$$
V^{\text{BSM}}(S_t,K,\tau,r,q,\sigma_{\text{imp}})=V^{\text{mkt}}.
$$

Variables:

- $V^{\text{BSM}}$ is the Black-Scholes-Merton model price;
- $V^{\text{mkt}}$ is the observed market price, usually bid, ask, or mid;
- $\sigma_{\text{imp}}$ is the model-implied annualized volatility in decimal units.

The important interpretation is that implied volatility is a price transformation. It is not a direct forecast of realized volatility and not a model-free truth. It reflects both expected distributional risk and compensation for bearing that risk.

## 4.3.2 Implied Volatility Across Many Options

A market option chain contains many options across strikes and maturities. After solving for implied volatility for each option, the surface is the cross-sectional object:

$$
\mathcal{S}_t = \left\{\sigma_{\text{imp},t}(K_j,T_m): j=1,\ldots,J;\; m=1,\ldots,M\right\}.
$$

Here:

- $J$ is the number of strikes;
- $M$ is the number of maturities;
- $\mathcal{S}_t$ is the surface observed or estimated at time $t$.

In practice, not every strike-maturity point is liquid. A production surface requires cleaning, interpolation, extrapolation, arbitrage checks, and smoothing.

## 4.3.3 Surface Construction Choices

A surface construction process must define:

| Design Choice | Common Alternatives | Why It Matters |
|---|---|---|
| Price input | bid, ask, mid, last, theoretical mark | Affects implied-volatility inversion and backtest realism |
| Strike coordinate | strike, spot moneyness, forward log-moneyness, delta | Affects interpolation stability and Greek interpretation |
| Maturity coordinate | calendar days, trading days, variance time | Affects annualization and forward-volatility estimates |
| Interpolation | linear, spline, SVI, SABR, parametric curves | Affects smoothness and higher-order Greeks |
| Extrapolation | flat wings, parametric wings, arbitrage-constrained wings | Affects tail options and stress tests |
| Arbitrage constraints | monotonic call prices, convexity in strike, calendar consistency | Prevents impossible prices and unstable Greeks |
| Data filters | spread, volume, open interest, stale quote rules | Prevents bad marks from driving false signals |

The volatility surface is therefore partly observed and partly modeled. Surface methodology is a source of model risk.

## 4.4 Smile, Skew, and Term Structure

## 4.4.1 Volatility Smile

A volatility smile is the pattern where implied volatility differs across strikes or moneyness. In a symmetric smile, both out-of-the-money puts and out-of-the-money calls may have higher implied volatility than at-the-money options.

A simple quadratic representation is:

$$
\sigma_{\text{imp}}(k_F,\tau)=a(\tau)+b(\tau)k_F+c(\tau)k_F^2.
$$

Variables:

- $a(\tau)$ is the at-the-money volatility level for maturity $\tau$;
- $b(\tau)$ is the skew slope;
- $c(\tau)$ is smile curvature;
- $k_F=\ln(K/F_{t,T})$ is forward log-moneyness.

If $c(\tau)>0$, implied volatility is higher in the wings than near at-the-money. This curvature often reflects jump risk, tail demand, uncertainty about the distribution, and market-maker inventory effects.

## 4.4.2 Volatility Skew

Volatility skew refers to an asymmetric slope in implied volatility across strikes. In equity index markets, downside puts often trade at higher implied volatility than upside calls. With the convention $k_F=\ln(K/F)$, lower strikes have negative $k_F$. A negative skew slope $b(\tau)<0$ implies:

$$
\sigma_{\text{imp}}(k_F<0,\tau)>\sigma_{\text{imp}}(k_F>0,\tau),
$$

assuming curvature does not dominate.

Skew can be measured by differences such as:

$$
\text{PutSkew}_{25\Delta,\tau}
=\sigma_{\text{put},25\Delta,\tau}-\sigma_{\text{ATM},\tau},
$$

or:

$$
\text{RiskReversal}_{25\Delta,\tau}
=\sigma_{\text{call},25\Delta,\tau}-\sigma_{\text{put},25\Delta,\tau}.
$$

Under this risk-reversal convention, equity index risk reversals are often negative because put implied volatility exceeds call implied volatility.

## 4.4.3 Term Structure

The volatility term structure describes implied volatility across maturities. At-the-money term structure can be written as:

$$
\tau \mapsto \sigma_{\text{ATM}}(\tau).
$$

Common shapes include:

| Term Structure Shape | Description | Common Interpretation |
|---|---|---|
| Upward sloping | Longer maturities have higher IV | Longer-term uncertainty or low near-term event risk |
| Downward sloping / inverted | Short maturities have higher IV | Near-term stress, earnings event, macro event, or crisis |
| Humped | Intermediate maturity has highest IV | Event or policy uncertainty concentrated at a specific horizon |
| Flat | Similar IV across maturities | Stable volatility expectations or lack of strong tenor segmentation |

Term structure is central to calendar spreads, diagonal spreads, volatility roll-down, event trading, and regime detection.

## 4.5 Forward Volatility

Forward volatility is the implied volatility for a future period inferred from two option maturities. It is usually derived from implied variance, not implied volatility directly.

Let $\sigma_1$ be implied volatility for maturity $\tau_1$ and $\sigma_2$ be implied volatility for maturity $\tau_2$, with $0<\tau_1<\tau_2$. Total implied variances are:

$$
W_1=\sigma_1^2\tau_1,
$$

$$
W_2=\sigma_2^2\tau_2.
$$

The forward variance between $\tau_1$ and $\tau_2$ is:

$$
\sigma_{fwd}^2(\tau_1,\tau_2)=\frac{W_2-W_1}{\tau_2-\tau_1}
=\frac{\sigma_2^2\tau_2-\sigma_1^2\tau_1}{\tau_2-\tau_1}.
$$

The forward volatility is:

$$
\sigma_{fwd}(\tau_1,\tau_2)=\sqrt{\frac{\sigma_2^2\tau_2-\sigma_1^2\tau_1}{\tau_2-\tau_1}}.
$$

Interpretation:

- If front implied volatility is very high because of a near-term event, forward volatility after the event may be much lower.
- If long-term implied volatility is high relative to short-term implied volatility, the market may be pricing persistent uncertainty.
- Forward volatility is sensitive to quote quality and interpolation, especially when maturities are close.

A no-arbitrage term structure requires nondecreasing total variance with maturity:

$$
\sigma_2^2\tau_2 \ge \sigma_1^2\tau_1.
$$

If this condition fails materially, the data or surface construction may contain calendar arbitrage.

## 4.6 Variance Risk Premium

The variance risk premium is the difference between implied variance and subsequent realized variance, or between implied variance and expected realized variance.

A simple ex-post measure is:

$$
\text{VRP}_{t,T}^{\text{ex post}}
=\sigma_{\text{imp},t,T}^2-\sigma_{\text{real},t,T}^2.
$$

A forward-looking expected version is:

$$
\text{VRP}_{t,T}^{\text{expected}}
=\sigma_{\text{imp},t,T}^2-\mathbb{E}_t^{\mathbb{P}}\left[\sigma_{\text{real},t,T}^2\right].
$$

Variables:

- $\sigma_{\text{imp},t,T}^2$ is implied variance over horizon $[t,T]$;
- $\sigma_{\text{real},t,T}^2$ is realized variance over the same horizon;
- $\mathbb{E}_t^{\mathbb{P}}$ is the real-world expectation conditional on information at time $t$.

The variance risk premium may be positive because investors demand protection and option sellers require compensation for bearing jump and volatility risk. However, it is unstable. It can compress, invert, or be overwhelmed by crash losses, transaction costs, margin stress, and liquidity shocks.

## 4.7 Equity-Index Skew Versus Single-Stock Skew

Equity-index options and single-stock options have different surface economics.

## 4.7.1 Equity-Index Skew

Equity-index downside skew is often structurally pronounced because investors use index puts for broad portfolio protection. Index skew reflects:

- demand for crash protection;
- institutional hedging flows;
- systematic put buying;
- dealer inventory and hedging constraints;
- correlation risk;
- macro downside risk;
- volatility risk premium;
- jump-to-stress risk.

Index skew is also connected to correlation. In a market selloff, single stocks often become more correlated. Index downside options therefore embed both single-name volatility risk and correlation risk.

A stylized index variance decomposition is:

$$
\sigma_{I}^{2}\approx \sum_{i=1}^{N}w_i^2\sigma_i^2
+2\sum_{i<j}w_iw_j\rho_{ij}\sigma_i\sigma_j,
$$

where:

- $\sigma_I^2$ is index variance;
- $w_i$ is index weight for stock $i$;
- $\sigma_i$ is volatility of stock $i$;
- $\rho_{ij}$ is pairwise correlation.

Index options are sensitive to both volatility and correlation. Single-name options are more directly exposed to idiosyncratic risk.

## 4.7.2 Single-Stock Skew

Single-stock skew is shaped by:

- earnings announcements;
- takeover risk;
- idiosyncratic jumps;
- borrow costs and hard-to-borrow constraints;
- short-sale constraints;
- single-name liquidity;
- retail flow and structured-product flow;
- corporate actions;
- sector-specific risks;
- balance-sheet and credit risks.

Single-stock skew can be less stable than index skew. A single stock can have upside call skew because of takeover speculation, meme-stock behavior, short squeeze risk, biotech trial risk, or commodity-linked optionality. It can also have steep downside put skew because of credit stress, earnings uncertainty, or litigation risk.

## 4.7.3 Comparison Table

| Dimension | Equity-Index Options | Single-Stock Options |
|---|---|---|
| Dominant downside risk | Macro drawdown and correlation spike | Idiosyncratic gap, earnings, credit, corporate action |
| Skew driver | Portfolio protection demand | Event risk, borrow, supply-demand, company-specific uncertainty |
| Liquidity | Usually deeper in major indices | Highly uneven across names and maturities |
| Event risk | Macro, policy, crisis | Earnings, M&A, regulatory, product-specific events |
| Correlation role | Central to index variance and dispersion | Indirect through factor and sector exposure |
| Early exercise | Relevant depending on product | Very relevant around dividends for American options |
| Surface stability | Often more systematic | Often more name-specific and regime-dependent |
| Main modeling caveat | Correlation and crash dynamics | Jumps, borrow, discrete dividends, corporate actions |

## 4.8 Earnings-Event Volatility and Single-Stock Greeks

Earnings announcements create concentrated event risk. A single-stock option expiring after earnings contains event variance that an option expiring before earnings does not.

A stylized total variance decomposition is:

$$
\sigma_{\text{imp}}^2(\tau)\tau
=\sigma_{\text{diffusive}}^2\tau + \sum_{e\in\mathcal{E}(t,T)} \omega_e^2,
$$

where:

- $\sigma_{\text{imp}}^2(\tau)\tau$ is total implied variance to maturity;
- $\sigma_{\text{diffusive}}^2$ is non-event diffusive variance;
- $\mathcal{E}(t,T)$ is the set of event dates between $t$ and $T$;
- $\omega_e^2$ is implied event variance for event $e$.

If there is one earnings event before maturity, the implied event volatility component can be approximated by comparing an option maturity that includes the event to one that does not, subject to interpolation and liquidity caveats.

## 4.8.1 Effect on Greeks

Earnings affect Greeks in several ways:

| Greek | Earnings Effect |
|---|---|
| Delta | Can be unstable because the distribution is jump-driven rather than diffusion-driven |
| Gamma | May be misleading if modeled as continuous diffusion; gap risk dominates hedgeability |
| Theta | Can appear large before the event because event premium decays after announcement |
| Vega | Can be concentrated in event volatility rather than ordinary volatility |
| Vanna | Can be large because spot and implied event volatility may interact |
| Volga | Can be material if event-vol repricing is nonlinear |
| Skew exposure | Can change sharply after earnings surprise and guidance |

The key practical point is that an earnings option is not merely a high-volatility ordinary option. It contains discrete jump risk. Delta hedging cannot continuously hedge an overnight earnings gap.

## 4.8.2 Earnings Volatility Crush

After earnings are released, implied volatility often declines because event uncertainty is resolved. This is commonly called volatility crush. For a long option position, the post-event vega P&L may be negative if implied volatility falls:

$$
\text{Vega P\&L}\approx \nu\Delta\sigma_{\text{imp}},
$$

where $\Delta\sigma_{\text{imp}}<0$ after the event. A long option can lose money from volatility crush even if the stock moves in the expected direction but not enough to offset premium and vega loss.

For short event-volatility positions, volatility crush can be favorable, but the short position is exposed to the earnings gap. A large surprise can overwhelm collected premium.

## 4.9 Volatility Carry, Roll-Down, Skew Carry, Convexity Carry, and Jump Risk

## 4.9.1 Volatility Carry

Volatility carry refers to expected return from holding a volatility exposure when implied volatility differs from expected realized volatility.

A simplified carry measure is:

$$
\text{VolCarry}_{t,T}=\sigma_{\text{imp},t,T}^2-\widehat{\sigma}_{\text{real},t,T}^2,
$$

where $\widehat{\sigma}_{\text{real},t,T}^2$ is a forecast of realized variance. A short-volatility strategy may have positive expected carry if implied variance exceeds expected realized variance, but it is exposed to jump risk and volatility spikes.

## 4.9.2 Term-Structure Roll-Down

Roll-down is the change in implied volatility or variance as an option ages along the term structure, assuming the surface is otherwise unchanged.

If an option starts at maturity $\tau$ and after a small time $\Delta t$ has maturity $\tau-\Delta t$, the roll-down in implied volatility is approximately:

$$
\text{RollDown}_{\sigma}
\approx
\sigma_{\text{imp}}(k_F,\tau-\Delta t)-\sigma_{\text{imp}}(k_F,\tau).
$$

If the term structure is upward sloping, rolling down toward shorter maturities may reduce implied volatility. If the term structure is inverted, roll-down may increase or decrease depending on the local slope.

For variance, total variance roll-down is often more stable:

$$
\text{RollDown}_{W}
\approx
\sigma_{\text{imp}}^2(k_F,\tau-\Delta t)(\tau-\Delta t)
-
\sigma_{\text{imp}}^2(k_F,\tau)\tau.
$$

Roll-down is not free alpha. The term structure can shift, realized volatility can differ from expectations, and transaction costs can consume expected carry.

## 4.9.3 Skew Carry

Skew carry refers to expected return from holding options whose implied-volatility skew is expected to normalize, persist, steepen, or flatten.

If skew slope is $\beta_{\text{skew}}(\tau)$ in the model:

$$
\sigma_{\text{imp}}(k_F,\tau)=\sigma_{\text{ATM}}(\tau)+\beta_{\text{skew}}(\tau)k_F+c(\tau)k_F^2,
$$

then skew P&L for option $i$ can be approximated as:

$$
\Delta V_i^{\text{skew}}
\approx
\nu_i k_{F,i}\Delta\beta_{\text{skew}}.
$$

A portfolio designed to harvest skew carry might sell options that appear expensive relative to skew history. The risk is that skew is expensive for a reason: crash risk, earnings risk, liquidity stress, or structural hedging demand.

## 4.9.4 Convexity Carry

Convexity carry is the cost or income associated with being long or short nonlinear exposure. A long-gamma portfolio pays theta carry but may benefit from realized movement. A short-gamma portfolio earns theta carry but is exposed to large moves.

For a delta-hedged option:

$$
\Delta \Pi
\approx
\frac{1}{2}\Gamma S^2\left(\sigma_{\text{real}}^2-\sigma_{\text{BE}}^2\right)\Delta t,
$$

where $\sigma_{\text{BE}}$ is a break-even volatility incorporating theta, financing, and costs. This expression is stylized but captures the idea that convexity carry depends on realized movement relative to what was priced.

## 4.9.5 Jump Risk

Jump risk is the risk of discontinuous price movement. A diffusion hedge assumes small continuous moves. A jump violates the continuous hedging premise.

If spot jumps from $S_-$ to $S_+$, the option repricing P&L is:

$$
\Delta V^{\text{jump}} = V(S_+,\sigma_+,t_+) - V(S_-,\sigma_-,t_-).
$$

A local Greek approximation may fail because $\Delta S=S_+-S_-$ is large and implied volatility may change discontinuously. For jump scenarios, full repricing is preferred.

Jump risk is central for:

- earnings trades;
- takeover rumors;
- macro announcements;
- central-bank events;
- geopolitical events;
- credit events;
- single-name litigation or regulatory decisions.

## 4.10 Model Intuition: Flat Vol, Local Vol, Stochastic Vol, Heston, SABR, and Jump-Diffusion

## 4.10.1 Flat-Volatility Black-Scholes-Merton

The flat-volatility model assumes:

$$
\frac{dS_t}{S_t}=(r-q)dt+\sigma dW_t^{\mathbb{Q}},
$$

with constant $\sigma$. It produces one implied volatility for all strikes and maturities if the model were exactly true.

Strengths:

- closed-form pricing for European calls and puts;
- clear Greek formulas;
- fast computation;
- common implied-volatility language.

Limitations:

- no skew;
- no stochastic volatility;
- no jumps;
- no volatility clustering;
- no event risk;
- no liquidity or funding effects.

## 4.10.2 Local Volatility

A local-volatility model assumes:

$$
\frac{dS_t}{S_t}=(r-q)dt+\sigma_{\text{loc}}(S_t,t)dW_t^{\mathbb{Q}}.
$$

Here volatility is deterministic but depends on spot and time. Local volatility can be calibrated to match a full implied volatility surface under certain assumptions.

Intuition:

- the model explains the surface by making instantaneous volatility depend on spot;
- it is useful for pricing some path-dependent derivatives;
- it can produce surface-consistent prices at calibration time.

Limitations:

- volatility is not random by itself;
- forward smile dynamics may be unrealistic;
- hedging performance can be poor if actual volatility dynamics are stochastic.

## 4.10.3 Stochastic Volatility

A stochastic-volatility model allows volatility to evolve randomly. A generic form is:

$$
\frac{dS_t}{S_t}=(r-q)dt+\sqrt{v_t}dW_t^S,
$$

$$
dv_t=\mu_v(v_t,t)dt+\sigma_v(v_t,t)dW_t^v,
$$

with instantaneous correlation:

$$
dW_t^S dW_t^v=\rho_{Sv}dt.
$$

Variables:

- $v_t$ is instantaneous variance;
- $\mu_v$ is the variance drift function;
- $\sigma_v$ is volatility of variance;
- $\rho_{Sv}$ controls spot-volatility correlation.

Stochastic volatility can generate skew because negative spot-vol correlation makes downside moves associated with higher volatility.

## 4.10.4 Heston Model

The Heston model is a widely known stochastic-volatility model:

$$
\frac{dS_t}{S_t}=(r-q)dt+\sqrt{v_t}dW_t^S,
$$

$$
dv_t=\kappa(\theta-v_t)dt+\xi\sqrt{v_t}dW_t^v,
$$

$$
dW_t^S dW_t^v=\rho dt.
$$

Variables:

- $v_t$ is instantaneous variance;
- $\kappa$ is mean-reversion speed;
- $\theta$ is long-run variance;
- $\xi$ is volatility of variance, often called vol-of-vol;
- $\rho$ is spot-variance correlation.

Intuition:

- negative $\rho$ can generate equity-like downside skew;
- higher $\xi$ increases smile curvature and vol-of-vol risk;
- mean reversion shapes the term structure.

Limitations:

- calibration may be unstable;
- pure Heston may not fit short-dated steep skew without jumps;
- parameters can be regime-dependent;
- implementation is more complex than Black-Scholes.

## 4.10.5 SABR Model

The SABR model is commonly used in rates and FX volatility modeling. A simplified form is:

$$
dF_t = \alpha_t F_t^{\beta} dW_t^F,
$$

$$
d\alpha_t = \nu \alpha_t dW_t^{\alpha},
$$

$$
dW_t^F dW_t^{\alpha}=\rho dt.
$$

Variables:

- $F_t$ is the forward price or rate;
- $\alpha_t$ is stochastic volatility level;
- $\beta$ controls elasticity;
- $\nu$ is vol-of-vol;
- $\rho$ controls correlation between forward and volatility.

SABR is useful for modeling smiles in markets where options are quoted by delta or moneyness and where forward dynamics are central.

## 4.10.6 Jump-Diffusion

A jump-diffusion model adds discontinuous jumps to diffusion dynamics. A stylized Merton jump-diffusion is:

$$
\frac{dS_t}{S_{t^-}}=(r-q-\lambda \kappa_J)dt+\sigma dW_t+dJ_t,
$$

where:

- $S_{t^-}$ is spot just before a jump;
- $\lambda$ is jump intensity;
- $J_t$ is a compound jump process;
- $\kappa_J=\mathbb{E}[e^Y-1]$ is expected proportional jump size adjustment;
- $Y$ is the random log jump size.

Jump models can generate short-dated skew and fat tails. They are important for earnings, credit events, policy shocks, and crash risk.

## 4.10.7 Model Comparison Table

| Model | Main Surface Mechanism | Strength | Weakness |
|---|---|---|---|
| Black-Scholes-Merton | Constant volatility | Simple, fast, transparent | No smile, no jumps, unrealistic dynamics |
| Local volatility | Volatility depends on spot and time | Can fit observed surface | Forward smile dynamics may be unrealistic |
| Stochastic volatility | Random variance process | Captures vol clustering and spot-vol correlation | Calibration and hedging complexity |
| Heston | Mean-reverting variance with vol-of-vol | Interpretable stochastic-vol framework | May not fit all smiles, parameters unstable |
| SABR | Stochastic vol for forwards | Useful in rates/FX smile modeling | Approximation and calibration risk |
| Jump-diffusion | Discontinuous jumps | Captures gap risk and short-dated skew | Jump parameters hard to estimate |

## 4.11 How Greek Exposures Differ Under Flat Volatility and Surface-Implied Assumptions

## 4.11.1 Flat-Volatility Greeks

A flat-volatility delta is:

$$
\Delta_{\text{flat}}=\frac{\partial V}{\partial S}\bigg|_{\sigma \text{ fixed}}.
$$

This assumes implied volatility does not change when spot changes.

## 4.11.2 Surface-Aware Delta

If implied volatility depends on spot through the surface, total delta is:

$$
\Delta_{\text{surface}}=\frac{dV}{dS}
=\frac{\partial V}{\partial S}
+\frac{\partial V}{\partial \sigma_{\text{imp}}}
\frac{\partial \sigma_{\text{imp}}}{\partial S}.
$$

Using vega $\nu$:

$$
\Delta_{\text{surface}}=\Delta_{\text{flat}}+\nu\frac{\partial\sigma_{\text{imp}}}{\partial S}.
$$

In equity markets, if spot falls and implied volatility rises, then $\partial\sigma_{\text{imp}}/\partial S$ may be negative. This adjustment can be significant for puts, collars, and skew-sensitive overlays.

## 4.11.3 Surface-Aware Gamma

Surface-aware gamma includes additional terms:

$$
\Gamma_{\text{surface}}
=
\Gamma_{\text{flat}}
+2\text{Vanna}\frac{\partial\sigma_{\text{imp}}}{\partial S}
+\text{Volga}\left(\frac{\partial\sigma_{\text{imp}}}{\partial S}\right)^2
+\nu\frac{\partial^2\sigma_{\text{imp}}}{\partial S^2}.
$$

Interpretation:

- flat gamma captures curvature if volatility is fixed;
- vanna adjusts for interaction between spot and volatility;
- volga adjusts for volatility convexity induced by spot-driven volatility changes;
- surface curvature contributes through $\partial^2\sigma_{\text{imp}}/\partial S^2$.

## 4.11.4 Surface Vega Buckets

Flat vega measures sensitivity to one volatility number. Surface-aware vega should be bucketed by tenor and moneyness:

$$
\nu_{p,b}=\sum_{i=1}^{N}w_i\nu_i\mathbf{1}\{i\in b\},
$$

where $b$ is a bucket such as 1-month ATM volatility, 3-month 25-delta put volatility, or 6-month upside-call volatility.

A portfolio may have zero total vega:

$$
\sum_b \nu_{p,b}=0,
$$

but still have large long-short exposure across buckets. Such a book is exposed to skew and term-structure changes.

## 4.12 Volatility Surface Shock Types

A surface-shock engine should test multiple dimensions of volatility risk.

## 4.12.1 Parallel Volatility Shock

A parallel shock shifts all implied volatilities by the same amount:

$$
\sigma_{\text{shock}}(k,\tau)=\sigma_{\text{base}}(k,\tau)+a_0.
$$

Here $a_0$ is a decimal volatility shift. A 5 volatility-point shock means $a_0=0.05$.

## 4.12.2 Skew Steepening and Flattening

A skew shock changes the slope of implied volatility across moneyness:

$$
\sigma_{\text{shock}}(k,\tau)=\sigma_{\text{base}}(k,\tau)+a_1 k.
$$

If $k=\ln(K/F)$, then downside puts have $k<0$. A negative $a_1$ increases implied volatility for downside strikes and lowers it for upside strikes. This is skew steepening in an equity-like convention.

## 4.12.3 Curvature Shock

A curvature shock changes wing richness:

$$
\sigma_{\text{shock}}(k,\tau)=\sigma_{\text{base}}(k,\tau)+a_2 k^2.
$$

If $a_2>0$, both downside and upside wings become richer relative to at-the-money options.

## 4.12.4 Term-Structure Shock

A term-structure shock changes volatility by maturity:

$$
\sigma_{\text{shock}}(k,\tau)=\sigma_{\text{base}}(k,\tau)+a_3 f(\tau),
$$

where $f(\tau)$ may represent a front-end shock, long-end shock, twist, or hump. For example, a front-end stress shock may use:

$$
f(\tau)=e^{-\lambda\tau},
$$

where $\lambda>0$ controls how quickly the shock decays with maturity.

## 4.12.5 Vol-of-Vol Shock

Vol-of-vol shocks change the uncertainty of volatility itself. In a surface representation, this may appear as a combined increase in curvature, instability, and scenario dispersion. A simple stress proxy is:

$$
\sigma_{\text{shock}}(k,\tau)=\sigma_{\text{base}}(k,\tau)+a_0+a_2k^2+a_4g(\tau)|k|,
$$

where $a_4$ controls wing instability and $g(\tau)$ controls tenor dependence.

This is not a structural stochastic-volatility model, but it is a practical stress-testing approximation.

## 4.13 Regime Interpretation of Surface Shapes

The volatility surface can be interpreted as a regime indicator, but not mechanically. Surface states should be combined with realized volatility, macro variables, liquidity conditions, credit spreads, trend, positioning, and event calendars.

## 4.13.1 Common Surface Regimes

| Surface Regime | Description | Possible Interpretation | Strategy Implication |
|---|---|---|---|
| Low flat volatility | Low ATM IV, muted skew, flat term structure | Complacency or genuinely stable environment | Short-vol carry may be crowded; convexity may be cheap but decay-heavy |
| Low vol with steep skew | Low ATM IV but expensive downside puts | Demand for crash protection despite calm spot | Collars and skew trades require caution |
| Inverted term structure | Front IV above back IV | Near-term event or stress | Calendar trades depend on event resolution and roll risk |
| High parallel vol | IV elevated across tenors | Broad uncertainty or crisis | Short-vol carry risky; long-vol may already be expensive |
| Steep downside skew | OTM puts rich versus ATM | Crash fear, hedging pressure, dealer constraints | Short-skew trades face tail risk |
| Wing-rich smile | Both tails expensive | Jump uncertainty or event risk | Long/short convexity must account for jump distribution |
| Post-shock normalization | Front IV falling, skew stabilizing | Stress decays but risk remains | Carry may improve, but aftershocks possible |

## 4.13.2 Surface Features as Regime Inputs

Useful surface features include:

$$
\text{ATMVol}_t=\sigma_{\text{imp},t}(k_F=0,\tau=30/365),
$$

$$
\text{SkewSlope}_t=\frac{\sigma_{\text{imp},t}(k_2,\tau)-\sigma_{\text{imp},t}(k_1,\tau)}{k_2-k_1},
$$

$$
\text{TermSlope}_t=\sigma_{\text{ATM},t}(\tau_2)-\sigma_{\text{ATM},t}(\tau_1),
$$

$$
\text{Curvature}_t=\sigma_{\text{imp},t}(k_-,\tau)+\sigma_{\text{imp},t}(k_+,\tau)-2\sigma_{\text{ATM},t}(\tau).
$$

These features can be standardized using rolling z-scores:

$$
z_{x,t}=\frac{x_t-\mu_{x,t}^{(L)}}{s_{x,t}^{(L)}},
$$

where $\mu_{x,t}^{(L)}$ and $s_{x,t}^{(L)}$ are rolling mean and standard deviation over lookback window $L$.

A regime model should treat these as probabilistic evidence, not deterministic trading rules.

## 4.14 Practical Surface Data Issues

## 4.14.1 Stale Quotes and Wide Markets

Illiquid options may display stale quotes. Implied volatility inversion on stale mid prices can create artificial smile kinks and false signals.

Filters often include:

- positive bid and ask;
- ask greater than bid;
- maximum bid-ask spread percentage;
- minimum option price;
- minimum volume or open interest;
- maximum age of quote;
- valid implied-volatility range;
- no static arbitrage violations.

## 4.14.2 Interpolation Risk

Interpolation can create smooth-looking surfaces with unstable derivatives. Greeks such as vanna, volga, and surface-adjusted gamma require derivatives of the surface, so interpolation quality matters.

A surface used for pricing may not be suitable for higher-order Greek calculation unless it is sufficiently smooth and arbitrage-aware.

## 4.14.3 Extrapolation Risk

Tail strikes are often illiquid. Extrapolated wing volatility can dominate tail-risk estimates, margin, expected shortfall, and stress losses. Production systems should cap extrapolation assumptions, document tail behavior, and run sensitivity analysis.

## 4.14.4 American Exercise and Discrete Dividends

Single-stock options are often American-style and affected by discrete dividends. A naive European implied-volatility surface can be distorted if early exercise value and dividend timing are ignored.

For single stocks, a production system should explicitly store:

- dividend amount and ex-date;
- special dividend flags;
- borrow cost;
- hard-to-borrow status;
- corporate-action adjustments;
- earnings date;
- option exercise style.

## 4.15 Python Code: Synthetic Implied Volatility Surface Generator and Visualization

The following code constructs a synthetic implied volatility surface over forward log-moneyness and maturity. It is not calibrated to live data. It is designed for educational visualization and testing of surface-aware Greeks.

```python
import math
from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

OptionType = Literal["call", "put"]


def synthetic_iv_surface(
    k_f: np.ndarray,
    tau: np.ndarray,
    base_vol: float = 0.20,
    skew_short: float = -0.35,
    skew_long: float = -0.15,
    curvature: float = 0.65,
    term_slope: float = 0.04,
    front_event: float = 0.03,
) -> np.ndarray:
    """Return a synthetic implied volatility surface.

    Parameters
    ----------
    k_f:
        Forward log-moneyness grid, log(K / F).
    tau:
        Maturity grid in years.
    base_vol:
        Baseline ATM volatility level.
    skew_short:
        Skew slope for short maturities.
    skew_long:
        Skew slope for long maturities.
    curvature:
        Smile curvature coefficient.
    term_slope:
        Upward term-structure component.
    front_event:
        Front-end event premium that decays with maturity.

    Returns
    -------
    Implied volatility as decimal annualized values.
    """
    k_f = np.asarray(k_f, dtype=float)
    tau = np.asarray(tau, dtype=float)
    if np.any(tau <= 0):
        raise ValueError("all maturities must be positive")

    # Maturity-dependent skew: steeper in the front end.
    skew_tau = skew_long + (skew_short - skew_long) * np.exp(-4.0 * tau)

    iv = (
        base_vol
        + term_slope * np.sqrt(tau)
        + front_event * np.exp(-10.0 * tau)
        + skew_tau * k_f
        + curvature * k_f**2
    )
    return np.maximum(iv, 0.03)


# Build grid.
k_values = np.linspace(-0.35, 0.35, 81)
tau_values = np.linspace(7 / 365, 2.0, 80)
K_GRID, T_GRID = np.meshgrid(k_values, tau_values)
IV_GRID = synthetic_iv_surface(K_GRID, T_GRID)

# Plot surface.
fig = plt.figure(figsize=(9, 6))
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(K_GRID, T_GRID, IV_GRID, linewidth=0, antialiased=True)
ax.set_xlabel("Forward log-moneyness log(K/F)")
ax.set_ylabel("Maturity in years")
ax.set_zlabel("Implied volatility")
ax.set_title("Synthetic implied volatility surface")
plt.show()

# Plot selected maturity slices.
for tau_target in [30 / 365, 90 / 365, 365 / 365, 2.0]:
    idx = int(np.argmin(np.abs(tau_values - tau_target)))
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(k_values, IV_GRID[idx, :])
    ax.set_xlabel("Forward log-moneyness log(K/F)")
    ax.set_ylabel("Implied volatility")
    ax.set_title(f"Synthetic smile slice, tau={tau_values[idx]:.3f} years")
    ax.grid(True)
    plt.show()
```

Expected interpretation:

- downside strikes have higher implied volatility when skew is negative;
- curvature makes both wings richer than at-the-money;
- front-end event premium elevates short maturities;
- term slope raises longer maturities depending on parameter choice.

## 4.16 Python Code: Surface Feature Extraction

The next code extracts ATM volatility, skew slope, curvature, and term slope from a surface grid.

```python
def nearest_value(array: np.ndarray, target: float) -> int:
    """Return index of array value nearest to target."""
    return int(np.argmin(np.abs(np.asarray(array) - target)))


def extract_surface_features(
    k_values: np.ndarray,
    tau_values: np.ndarray,
    iv_grid: np.ndarray,
    short_tau: float = 30 / 365,
    long_tau: float = 180 / 365,
    k_put: float = -0.10,
    k_call: float = 0.10,
) -> dict[str, float]:
    """Extract simple volatility surface features from a grid.

    Parameters
    ----------
    k_values:
        One-dimensional grid of forward log-moneyness values.
    tau_values:
        One-dimensional grid of maturity values in years.
    iv_grid:
        Two-dimensional array with shape (len(tau_values), len(k_values)).
    short_tau:
        Short maturity used for ATM, skew, and curvature features.
    long_tau:
        Longer maturity used for term slope.
    k_put:
        Downside log-moneyness point.
    k_call:
        Upside log-moneyness point.
    """
    if iv_grid.shape != (len(tau_values), len(k_values)):
        raise ValueError("iv_grid shape must be (len(tau_values), len(k_values))")

    i_short = nearest_value(tau_values, short_tau)
    i_long = nearest_value(tau_values, long_tau)
    j_atm = nearest_value(k_values, 0.0)
    j_put = nearest_value(k_values, k_put)
    j_call = nearest_value(k_values, k_call)

    atm_short = float(iv_grid[i_short, j_atm])
    atm_long = float(iv_grid[i_long, j_atm])
    put_iv = float(iv_grid[i_short, j_put])
    call_iv = float(iv_grid[i_short, j_call])

    skew_slope = (call_iv - put_iv) / (k_values[j_call] - k_values[j_put])
    curvature = put_iv + call_iv - 2.0 * atm_short
    term_slope = atm_long - atm_short

    return {
        "atm_short_iv": atm_short,
        "atm_long_iv": atm_long,
        "put_wing_iv": put_iv,
        "call_wing_iv": call_iv,
        "skew_slope": float(skew_slope),
        "curvature": float(curvature),
        "term_slope": float(term_slope),
    }


features = extract_surface_features(k_values, tau_values, IV_GRID)
print(pd.Series(features).round(6))
```

These features can become inputs into regime classifiers, signal models, or risk dashboards. They should be computed using consistent moneyness and maturity conventions.

## 4.17 Python Code: Black-Scholes Pricing and Greeks for Surface Stress Testing

The following code provides Black-Scholes functions used in the surface-shock engine.

```python
@dataclass(frozen=True)
class BSMInputs:
    spot: float
    strike: float
    tau: float
    rate: float
    dividend_yield: float
    volatility: float
    option_type: OptionType


def validate_bsm(x: BSMInputs) -> None:
    if x.spot <= 0 or x.strike <= 0:
        raise ValueError("spot and strike must be positive")
    if x.tau <= 0:
        raise ValueError("tau must be positive")
    if x.volatility <= 0:
        raise ValueError("volatility must be positive")
    if x.option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")


def bsm_d1_d2(x: BSMInputs) -> tuple[float, float]:
    validate_bsm(x)
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


def bsm_greeks(x: BSMInputs) -> dict[str, float]:
    d1, d2 = bsm_d1_d2(x)
    df_r = math.exp(-x.rate * x.tau)
    df_q = math.exp(-x.dividend_yield * x.tau)
    phi = norm.pdf(d1)
    sqrt_tau = math.sqrt(x.tau)

    gamma = df_q * phi / (x.spot * x.volatility * sqrt_tau)
    vega = x.spot * df_q * phi * sqrt_tau
    vanna = -df_q * phi * d2 / x.volatility
    volga = vega * d1 * d2 / x.volatility

    common_theta = -x.spot * df_q * phi * x.volatility / (2.0 * sqrt_tau)
    if x.option_type == "call":
        delta = df_q * norm.cdf(d1)
        theta = (
            common_theta
            - x.rate * x.strike * df_r * norm.cdf(d2)
            + x.dividend_yield * x.spot * df_q * norm.cdf(d1)
        )
    else:
        delta = df_q * (norm.cdf(d1) - 1.0)
        theta = (
            common_theta
            + x.rate * x.strike * df_r * norm.cdf(-d2)
            - x.dividend_yield * x.spot * df_q * norm.cdf(-d1)
        )

    return {
        "price": bsm_price(x),
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "vanna": vanna,
        "volga": volga,
    }
```

## 4.18 Python Code: Volatility-Surface Shock Engine

The following code applies parallel, skew, curvature, term-structure, and front-end shocks to a synthetic volatility surface. It compares full repricing P&L to a local Greek approximation.

```python
def forward_log_moneyness(
    spot: float,
    strike: float,
    tau: float,
    rate: float,
    dividend_yield: float,
) -> float:
    """Compute forward log-moneyness log(K / F)."""
    forward = spot * math.exp((rate - dividend_yield) * tau)
    return math.log(strike / forward)


def shocked_iv(
    k_f: float,
    tau: float,
    parallel_shift: float = 0.0,
    skew_shock: float = 0.0,
    curvature_shock: float = 0.0,
    front_shock: float = 0.0,
    long_shock: float = 0.0,
) -> float:
    """Return shocked synthetic implied volatility.

    All shocks are decimal volatility units. A 5 vol-point shock is 0.05.
    The front shock decays with maturity. The long shock increases with maturity.
    """
    base = float(synthetic_iv_surface(np.array(k_f), np.array(tau)))
    front_component = front_shock * math.exp(-8.0 * tau)
    long_component = long_shock * (1.0 - math.exp(-2.0 * tau))
    shocked = (
        base
        + parallel_shift
        + skew_shock * k_f
        + curvature_shock * k_f**2
        + front_component
        + long_component
    )
    return max(shocked, 0.03)


def stress_one_option_surface(
    option: BSMInputs,
    spot_return: float = 0.0,
    parallel_shift: float = 0.0,
    skew_shock: float = 0.0,
    curvature_shock: float = 0.0,
    front_shock: float = 0.0,
    long_shock: float = 0.0,
) -> dict[str, float]:
    """Stress one option using full repricing and Greek approximation."""
    if spot_return <= -1.0:
        raise ValueError("spot_return must be greater than -100%")

    k0 = forward_log_moneyness(
        option.spot, option.strike, option.tau, option.rate, option.dividend_yield
    )
    iv0 = shocked_iv(k0, option.tau)
    base_option = BSMInputs(
        spot=option.spot,
        strike=option.strike,
        tau=option.tau,
        rate=option.rate,
        dividend_yield=option.dividend_yield,
        volatility=iv0,
        option_type=option.option_type,
    )
    base_greeks = bsm_greeks(base_option)
    base_price = base_greeks["price"]

    shocked_spot = option.spot * (1.0 + spot_return)
    k1 = forward_log_moneyness(
        shocked_spot, option.strike, option.tau, option.rate, option.dividend_yield
    )
    iv1 = shocked_iv(
        k1,
        option.tau,
        parallel_shift=parallel_shift,
        skew_shock=skew_shock,
        curvature_shock=curvature_shock,
        front_shock=front_shock,
        long_shock=long_shock,
    )
    stressed_option = BSMInputs(
        spot=shocked_spot,
        strike=option.strike,
        tau=option.tau,
        rate=option.rate,
        dividend_yield=option.dividend_yield,
        volatility=iv1,
        option_type=option.option_type,
    )
    stressed_price = bsm_price(stressed_option)

    d_s = shocked_spot - option.spot
    d_vol = iv1 - iv0
    greek_approx = (
        base_greeks["delta"] * d_s
        + 0.5 * base_greeks["gamma"] * d_s**2
        + base_greeks["vega"] * d_vol
        + base_greeks["vanna"] * d_s * d_vol
        + 0.5 * base_greeks["volga"] * d_vol**2
    )

    return {
        "base_price": base_price,
        "stressed_price": stressed_price,
        "full_repricing_pnl": stressed_price - base_price,
        "greek_approx_pnl": greek_approx,
        "approximation_error": (stressed_price - base_price) - greek_approx,
        "base_iv": iv0,
        "stressed_iv": iv1,
        "spot_change": d_s,
        "vol_change": d_vol,
        "base_delta": base_greeks["delta"],
        "base_gamma": base_greeks["gamma"],
        "base_vega": base_greeks["vega"],
        "base_vanna": base_greeks["vanna"],
        "base_volga": base_greeks["volga"],
    }


example_put = BSMInputs(
    spot=100.0,
    strike=90.0,
    tau=60 / 365,
    rate=0.04,
    dividend_yield=0.01,
    volatility=0.20,
    option_type="put",
)

stress_result = stress_one_option_surface(
    example_put,
    spot_return=-0.07,
    parallel_shift=0.04,
    skew_shock=-0.15,
    curvature_shock=0.20,
    front_shock=0.03,
)
print(pd.Series(stress_result).round(6))
```

Expected interpretation:

- full repricing captures nonlinear changes in spot, volatility, skew, and curvature;
- Greek approximation is useful for attribution but can diverge under large shocks;
- vanna and volga become material when spot and volatility move together;
- downside puts can be strongly affected by skew steepening during selloffs.

## 4.19 Python Code: Portfolio-Level Surface Stress Test

The next example applies the surface-shock engine to a simple hypothetical option portfolio. It aggregates P&L and Greek exposures across positions.

```python
@dataclass(frozen=True)
class OptionPosition:
    option: BSMInputs
    quantity: float
    multiplier: float = 100.0
    label: str = ""


def stress_option_portfolio(
    positions: list[OptionPosition],
    spot_return: float = 0.0,
    parallel_shift: float = 0.0,
    skew_shock: float = 0.0,
    curvature_shock: float = 0.0,
    front_shock: float = 0.0,
    long_shock: float = 0.0,
) -> pd.DataFrame:
    """Stress a list of option positions and return position-level results."""
    rows = []
    for pos in positions:
        res = stress_one_option_surface(
            pos.option,
            spot_return=spot_return,
            parallel_shift=parallel_shift,
            skew_shock=skew_shock,
            curvature_shock=curvature_shock,
            front_shock=front_shock,
            long_shock=long_shock,
        )
        scale = pos.quantity * pos.multiplier
        rows.append(
            {
                "label": pos.label,
                "quantity": pos.quantity,
                "strike": pos.option.strike,
                "tau": pos.option.tau,
                "option_type": pos.option.option_type,
                "position_full_pnl": scale * res["full_repricing_pnl"],
                "position_greek_approx_pnl": scale * res["greek_approx_pnl"],
                "position_approx_error": scale * res["approximation_error"],
                "position_delta": scale * res["base_delta"],
                "position_gamma": scale * res["base_gamma"],
                "position_vega": scale * res["base_vega"],
                "position_vanna": scale * res["base_vanna"],
                "position_volga": scale * res["base_volga"],
            }
        )
    return pd.DataFrame(rows)


portfolio = [
    OptionPosition(
        BSMInputs(100.0, 95.0, 45 / 365, 0.04, 0.01, 0.20, "put"),
        quantity=20,
        label="Long downside puts",
    ),
    OptionPosition(
        BSMInputs(100.0, 105.0, 45 / 365, 0.04, 0.01, 0.20, "call"),
        quantity=-15,
        label="Short upside calls",
    ),
    OptionPosition(
        BSMInputs(100.0, 100.0, 180 / 365, 0.04, 0.01, 0.20, "call"),
        quantity=10,
        label="Long 6m ATM calls",
    ),
]

portfolio_stress = stress_option_portfolio(
    portfolio,
    spot_return=-0.05,
    parallel_shift=0.03,
    skew_shock=-0.10,
    curvature_shock=0.15,
    front_shock=0.02,
)

print(portfolio_stress.round(4))
print("\nAggregated exposures and P&L:")
print(
    portfolio_stress[
        [
            "position_full_pnl",
            "position_greek_approx_pnl",
            "position_approx_error",
            "position_delta",
            "position_gamma",
            "position_vega",
            "position_vanna",
            "position_volga",
        ]
    ].sum().round(4)
)
```

This example is deliberately simple. A production portfolio stress engine should handle different underlyings, different spot shocks by underlying, volatility shocks by surface bucket, dividends, rates, borrow costs, transaction costs, and liquidity assumptions.

## 4.20 Practical Surface Risk Dashboard

An institutional surface dashboard should monitor at least the following:

| Dashboard Item | Measurement | Use |
|---|---|---|
| ATM volatility by tenor | $\sigma_{\text{ATM}}(\tau)$ | Volatility level and term structure |
| Put skew | OTM put IV minus ATM IV | Downside protection demand |
| Risk reversal | Call wing IV minus put wing IV | Asymmetry and skew pressure |
| Curvature | Wing IVs minus ATM IV | Tail richness and vol-of-vol proxy |
| Forward volatility | Variance between maturities | Event and forward uncertainty |
| VRP estimate | Implied variance minus forecast realized variance | Carry and risk premium context |
| Surface z-scores | Standardized features | Regime detection |
| Bucketed vega | Vega by tenor and moneyness | Surface shock exposure |
| Vanna and volga | Higher-order exposures | Spot-vol and vol-convexity risk |
| Surface stress P&L | Full repricing under shocks | Loss estimation and limits |
| Liquidity metrics | Spread, volume, open interest | Tradability and capacity |

## 4.21 Common Implementation Errors

| Error | Why It Matters | Better Practice |
|---|---|---|
| Treating all options as having one volatility | Misses skew, term, and event risk | Build and store surface-aware marks |
| Using stale mids | Creates false smile signals | Apply quote freshness and spread filters |
| Interpolating by strike without forward adjustment | Distorts cross-maturity comparisons | Use forward log-moneyness or delta conventions |
| Ignoring total variance monotonicity | Allows calendar arbitrage | Check $\sigma^2\tau$ across maturities |
| Using flat vega for all risk | Misses skew and term-structure shocks | Bucket vega by moneyness and tenor |
| Relying only on local Greeks for stress | Underestimates nonlinear losses | Use full repricing scenarios |
| Ignoring earnings dates | Misclassifies event volatility as normal volatility | Separate event and diffusive variance |
| Ignoring borrow and dividends | Distorts single-stock surfaces | Use point-in-time borrow and dividend inputs |
| Treating skew richness as free carry | Skew may compensate for crash risk | Stress skew steepening and jumps |
| Overfitting surface features | Regime relations change | Use robust validation and conservative inference |

## 4.22 Summary of Part 4

Part 4 extended the curriculum from flat-volatility Greeks to volatility-surface-aware risk.

Key points:

1. Implied volatility is a model-based transformation of option price, not a direct forecast.
2. The volatility surface maps implied volatility across strike, moneyness, and maturity.
3. Smile, skew, curvature, and term structure encode market pricing of distributional risk.
4. Forward volatility should be derived from total implied variance, not by subtracting volatilities.
5. The variance risk premium is unstable and must be evaluated after costs, jumps, and drawdown risk.
6. Equity-index skew is strongly connected to portfolio protection demand and correlation risk.
7. Single-stock skew is heavily affected by earnings, borrow, corporate actions, liquidity, and idiosyncratic jumps.
8. Earnings options contain discrete event variance; ordinary diffusion Greeks may understate gap risk.
9. Volatility carry, roll-down, skew carry, and convexity carry are risk premia, not guaranteed returns.
10. Flat-volatility Greeks can materially differ from surface-aware Greeks.
11. Sticky-strike, sticky-moneyness, sticky-delta, and empirical surface dynamics lead to different risk estimates.
12. Surface shocks should include parallel volatility, skew, curvature, term-structure, and vol-of-vol dimensions.
13. Full repricing is preferred for large shocks; Greek approximations are useful for attribution but not sufficient for stress risk.
14. Production surface systems require quote cleaning, arbitrage checks, interpolation controls, versioning, and liquidity-aware implementation.

The next installment will cover Part 5: Systematic Alpha Generation Using Greeks, including volatility risk premium, skew premium, term-structure carry, realized-implied spread, jump premium, convexity demand, correlation risk premium, liquidity premium, and strategy-family Greek profiles.
