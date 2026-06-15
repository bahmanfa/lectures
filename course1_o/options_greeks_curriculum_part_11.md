# Institutional Options Greeks, Systematic Strategy, and Regime-Aware Portfolio Construction Curriculum

## Completed Installment

This installment contains:

- Part 11: Applied Case Studies in Greek-Aware Options Strategy Design.

The document is educational and research-oriented. It is not personalized investment advice, a live trading recommendation, or a claim that any option strategy produces guaranteed alpha.

---

# Part 11: Applied Case Studies in Greek-Aware Options Strategy Design

**Level:** Expert

## 11.1 Purpose of Part 11

Parts 1 through 10 built the analytical and implementation framework: pricing, Greeks, higher-order Greeks, hedging, volatility surfaces, alpha signals, regime-aware allocation, portfolio construction, covariance stabilization, stress testing, and backtesting architecture. Part 11 applies that framework to realistic institutional options strategy case studies.

The objective is not to recommend specific trades. The objective is to show how a professional researcher or portfolio manager would diagnose an options strategy from multiple angles:

- payoff structure;
- Greek exposures;
- volatility-surface exposure;
- regime suitability;
- expected return hypothesis;
- P&L decomposition;
- stress testing;
- implementation constraints;
- failure modes;
- governance checklist.

The central principle is:

$$
\text{A good options case study connects trade structure, Greeks, regime, implementation, and risk controls in one coherent workflow.}
$$

Each case study follows a common template:

1. Define the structure.
2. Identify the intended economic exposure.
3. Map the Greeks.
4. Specify the alpha or hedging hypothesis.
5. Identify the preferred regime.
6. Decompose expected and realized P&L.
7. Run stress scenarios.
8. List implementation and governance controls.
9. Describe failure modes.

## 11.2 Case Study Template

For any options strategy $s$, define the position vector:

$$
\mathbf{w}_{s,t}=\begin{bmatrix}w_{1,t}&w_{2,t}&\cdots&w_{N,t}\end{bmatrix}^{\top},
$$

where $w_{i,t}$ is the signed quantity of option or hedge instrument $i$.

The strategy Greek vector is:

$$
\mathbf{g}_{s,t}=\mathbf{A}_{s,t}\mathbf{w}_{s,t},
$$

where $\mathbf{A}_{s,t}$ is the exposure matrix containing delta, gamma, theta, vega, rho, vanna, volga, skew, term-vega, and other relevant risk factors.

A local P&L decomposition can be written as:

$$
\Delta V_s \approx
\Delta_s\Delta S
+\frac{1}{2}\Gamma_s(\Delta S)^2
+\Theta_s\Delta t
+\nu_s\Delta\sigma
+\text{Vanna}_s\Delta S\Delta\sigma
+\frac{1}{2}\text{Volga}_s(\Delta\sigma)^2
+\text{Residual}_s.
$$

Variables:

- $\Delta_s$ is strategy delta;
- $\Gamma_s$ is strategy gamma;
- $\Theta_s$ is strategy theta;
- $\nu_s$ is strategy vega;
- $\Delta S$ is spot movement;
- $\Delta\sigma$ is implied-volatility movement;
- $\Delta t$ is elapsed time in years;
- residual includes skew, term-structure, jumps, costs, model error, liquidity, and higher-order effects.

For stress testing, the preferred measure is full repricing:

$$
\Delta V_s^{Full}=\sum_{i=1}^{N}w_iM_i\left[V_i(\mathbf{x}_{i}^{shock})-V_i(\mathbf{x}_{i}^{base})\right]-\text{StressCosts},
$$

where $M_i$ is contract multiplier and $\mathbf{x}_i$ includes spot, implied volatility surface, rates, dividends, borrow, time, and exercise assumptions.

---

# 11.3 Case Study 1: Delta-Hedged Long Straddle

## 11.3.1 Structure

A long straddle buys a call and a put with the same strike and maturity:

$$
\text{Long Straddle}=+1C(K,T)+1P(K,T).
$$

The classic version uses an at-the-money or near-at-the-money strike. The trade is often delta-hedged to reduce first-order directional exposure and isolate realized volatility, gamma, and vega exposure.

The delta-hedged portfolio is:

$$
\Pi_t=C_t+P_t+h_tS_t+B_t,
$$

where:

$$
h_t=-(\Delta_C+\Delta_P).
$$

## 11.3.2 Intended Economic Exposure

The strategy seeks to profit when realized movement, jump movement, or implied-volatility repricing exceeds the cost of option premium, theta decay, and hedge transaction costs.

The intended exposure is:

- long gamma;
- long vega;
- usually negative theta;
- near-zero delta after hedging;
- positive exposure to realized volatility;
- positive exposure to sufficiently large events or jumps;
- possible positive volga, depending on moneyness and maturity.

## 11.3.3 Greek Profile

| Greek | Typical Sign | Interpretation |
|---|---:|---|
| Delta | near 0 after hedge | Directional risk is hedged locally |
| Gamma | positive | Benefits from large spot movement |
| Theta | negative | Pays carry to own convexity |
| Vega | positive | Benefits if implied volatility rises |
| Vanna | mixed | Spot-vol co-movement affects hedge and vega |
| Volga | often positive away from ATM | Benefits from large vol repricing |
| Skew exposure | limited for symmetric ATM | Depends on strike and surface |

The delta-hedged local P&L is approximately:

$$
\Delta\Pi
\approx
\frac{1}{2}\Gamma S^2r^2
+\Theta\Delta t
+\nu\Delta\sigma
-\text{HedgeCosts},
$$

where $r=\Delta S/S$.

## 11.3.4 Break-Even Realized Volatility

Ignoring vega changes and costs, break-even realized volatility is approximately:

$$
\sigma_{BE}\approx\sqrt{\frac{-2\Theta}{\Gamma S^2}}.
$$

This is the realized volatility required for gamma P&L to offset theta decay.

After costs, the break-even condition becomes:

$$
\frac{1}{2}\Gamma S^2\sigma_{real}^2\Delta t+\Theta\Delta t
>\text{HedgeCosts}+\text{ExecutionCosts}.
$$

Thus a long straddle is not simply a bet that volatility will be high. It is a bet that realized movement and volatility repricing will exceed the implied cost and all implementation frictions.

## 11.3.5 Preferred Regimes

The long delta-hedged straddle is more suitable when:

- implied volatility is low relative to forecast realized volatility;
- realized volatility is expected to rise;
- macro uncertainty is increasing;
- event risk is underpriced;
- the market is entering a volatility-transition regime;
- liquidity is sufficient for hedging;
- transaction costs are moderate.

It is less suitable when:

- implied volatility is already extremely rich;
- realized volatility is low and stable;
- bid-ask spreads are wide;
- the trade requires excessive hedge turnover;
- volatility is likely to collapse after an event.

## 11.3.6 P&L Attribution

A daily attribution table should include:

| Component | Formula | Interpretation |
|---|---:|---|
| Gamma P&L | $0.5\Gamma(\Delta S)^2$ | Realized movement benefit |
| Theta P&L | $\Theta\Delta t$ | Carry cost |
| Vega P&L | $\nu\Delta\sigma$ | Implied-volatility repricing |
| Hedge P&L | $h\Delta S$ | Underlying hedge result |
| Costs | spreads + slippage + hedge cost | Implementation drag |
| Residual | actual minus explained | Model, skew, jumps, data, higher-order effects |

For a well-specified short-horizon attribution, residual P&L should be explainable. Persistent residuals suggest missing surface dynamics, bad marks, incorrect hedge timing, or model error.

## 11.3.7 Stress Scenarios

| Scenario | Expected Effect | Risk Interpretation |
|---|---|---|
| Spot flat, IV flat | Loss from theta | Carry bleed |
| Spot up 3%, IV flat | Positive gamma; hedge may monetize movement | Good if movement exceeds theta and costs |
| Spot down 5%, IV up 5 vol points | Positive gamma and vega | Often favorable |
| Spot flat, IV down 5 vol points | Negative vega and theta | Vol crush loss |
| Spot jumps overnight | Option value may rise but hedge cannot rebalance continuously | Gap risk remains path-dependent |
| Liquidity spreads double | Exit and hedge costs increase | Monetization risk |

## 11.3.8 Failure Modes

Main failure modes:

1. **Overpaying for implied volatility.** Realized movement occurs but not enough to offset premium and theta.
2. **Volatility crush.** Implied volatility falls after event resolution.
3. **Poor hedge execution.** Frequent hedging costs exceed gamma scalping gains.
4. **Path mismatch.** Total realized volatility looks high, but path timing produces poor hedge outcomes.
5. **Model residuals.** Surface changes, skew shifts, and discrete dividends are not captured.
6. **Liquidity gap.** The position is theoretically profitable but difficult to monetize at fair value.

## 11.3.9 Governance Checklist

Before implementation:

- Confirm implied volatility is not rich after event adjustment.
- Estimate break-even realized volatility after hedge costs.
- Define hedge frequency or delta-band rule.
- Stress volatility crush and liquidity widening.
- Check vega and gamma concentration by maturity.
- Define stop-loss and profit-taking rules.
- Attribute P&L daily into gamma, theta, vega, costs, and residual.

---

# 11.4 Case Study 2: Short Put and Put-Spread Carry

## 11.4.1 Structure

A short put sells downside protection:

$$
\text{Short Put}=-1P(K,T).
$$

A short put spread sells a higher-strike put and buys a lower-strike put:

$$
\text{Short Put Spread}=-1P(K_1,T)+1P(K_2,T),\quad K_2<K_1.
$$

The put spread limits maximum loss but also reduces premium received.

## 11.4.2 Intended Economic Exposure

The strategy seeks to earn compensation for selling downside insurance. The expected return hypothesis is that implied downside volatility and skew are rich relative to subsequent realized downside risk.

The intended exposure is:

- positive theta;
- negative gamma;
- negative vega;
- short downside skew;
- positive delta for equity puts;
- potentially high margin usage;
- exposure to crash and gap risk.

## 11.4.3 Greek Profile

| Greek | Short Put | Short Put Spread |
|---|---:|---:|
| Delta | positive | positive but reduced |
| Gamma | negative | negative near short strike, partly offset by long put |
| Theta | positive | positive but lower than naked short put |
| Vega | negative | negative but partly offset |
| Vanna | material | reduced but still relevant |
| Volga | often short volatility convexity | lower than naked short put |
| Skew | short downside skew | short downside skew with defined loss |

The local P&L for a short put is approximately:

$$
\Delta V_{short}\approx
-\Delta_P\Delta S
-\frac{1}{2}\Gamma_P(\Delta S)^2
-\Theta_P\Delta t
-\nu_P\Delta\sigma.
$$

Because the long put has $\Gamma_P>0$, $\Theta_P<0$, and $\nu_P>0$, the short put has negative gamma, positive theta, and negative vega.

## 11.4.4 Expected Return Hypothesis

A short put carry signal may be:

$$
\text{ShortPutScore}=Z(\text{VRP})+Z(\text{SkewRichness})-Z(\text{JumpRisk})-Z(\text{LiquidityCost})-Z(\text{MarginIntensity}).
$$

Where:

- $\text{VRP}=\sigma_{imp}^2-\widehat{\sigma}_{real}^2$;
- skew richness measures downside put implied volatility relative to ATM;
- jump risk penalizes earnings, credit stress, and event gaps;
- liquidity cost penalizes wide spreads;
- margin intensity penalizes capital usage.

## 11.4.5 Preferred Regimes

More suitable:

- stable carry regime;
- implied volatility above forecast realized volatility;
- downside skew rich but not steepening;
- credit spreads stable or tightening;
- market breadth improving;
- liquidity normal;
- no near-term earnings or major event risk for single names.

Less suitable:

- rising-volatility transition;
- credit stress;
- liquidity tightening;
- high drawdown regime;
- crowded short-volatility positioning;
- single-name earnings or takeover uncertainty;
- hard-to-borrow names where hedging is difficult.

## 11.4.6 Stress Scenarios

| Scenario | Short Put | Short Put Spread |
|---|---|---|
| Spot flat, IV flat | Premium decay positive | Premium decay positive but smaller |
| Spot down 5%, IV up 5 vol points | Loss from delta, gamma, vega | Loss reduced by long lower-strike put |
| Spot down 15%, IV up 20 vol points | Severe loss and margin increase | Loss capped if far enough below long strike |
| Skew steepens | Mark-to-market loss | Smaller loss if long wing benefits |
| Liquidity spreads triple | Exit cost high | Multi-leg exit cost high |
| Margin doubles | Capital pressure | Defined-risk margin may be more stable |

## 11.4.7 Failure Modes

The main failure mode is mistaking premium income for alpha. A short put earns premium because it sells crash insurance. The rare loss is the economic reason the premium exists.

Specific failures:

- selling puts before volatility regime transition;
- ignoring skew steepening;
- sizing by premium rather than stress loss;
- ignoring margin procyclicality;
- selling options with poor liquidity;
- treating high implied volatility as automatically rich;
- ignoring earnings and credit risk in single names.

## 11.4.8 Risk Controls

Required controls:

- stress loss limit under spot down and volatility up;
- margin utilization and stress margin limit;
- maximum short gamma by maturity bucket;
- maximum short downside vega;
- single-name event exclusion or penalty;
- spread and open-interest filters;
- drawdown-based de-risking;
- defined-risk preference in high-volatility regimes.

---

# 11.5 Case Study 3: Protective Put and Collar Overlay

## 11.5.1 Structure

A protective put combines long underlying exposure with a long put:

$$
\text{Protective Put}=+1S+1P(K_P,T).
$$

A collar combines long underlying, long put, and short call:

$$
\text{Collar}=+1S+1P(K_P,T)-1C(K_C,T),\quad K_P<S<K_C.
$$

The short call helps finance the put but caps upside.

## 11.5.2 Intended Economic Exposure

A protective put is designed to reduce downside tail risk while preserving upside participation. A collar is designed to reduce protection cost by selling upside optionality.

Economic objective:

- reduce portfolio drawdown;
- improve left-tail outcome;
- maintain some upside participation;
- manage protection cost;
- convert uncertain downside into a more controlled payoff distribution.

## 11.5.3 Greek Profile

| Greek | Protective Put | Collar |
|---|---:|---:|
| Delta | positive, less than stock alone | positive but capped |
| Gamma | positive from put | mixed: long put gamma, short call gamma |
| Theta | negative from put | less negative or possibly positive |
| Vega | positive from put | mixed; depends on strikes |
| Skew | long downside skew | long downside skew, short upside skew |
| Tail exposure | improved downside | improved downside, capped upside |

## 11.5.4 Cost of Protection

The annualized protection cost can be approximated as:

$$
\text{ProtectionCost}=\frac{P(K_P,T)}{S}\cdot\frac{1}{\tau}.
$$

For a collar, net option cost is:

$$
\text{NetCollarCost}=P(K_P,T)-C(K_C,T).
$$

A zero-cost collar chooses strikes such that:

$$
P(K_P,T)\approx C(K_C,T).
$$

Zero premium does not mean zero economic cost. The cost is paid through capped upside and altered payoff distribution.

## 11.5.5 Preferred Regimes

Protective puts are more suitable when:

- downside risk is rising;
- implied protection is not excessively expensive;
- drawdown control has high utility;
- credit spreads are widening;
- macro regime probabilities shift toward risk-off;
- portfolio has large embedded gains or risk budget constraints.

Collars are more suitable when:

- protection is desired but put skew is expensive;
- upside expected return is moderate;
- call implied volatility is attractive to sell;
- investor accepts capped upside;
- mandate values drawdown reduction.

## 11.5.6 Stress Scenarios

| Scenario | Protective Put | Collar |
|---|---|---|
| Moderate rally | Participates after put cost | Participates until call cap |
| Strong rally | Participates after put cost | Underperforms due to short call |
| Moderate selloff | Put cushions loss | Put cushions loss |
| Crash | Put floor matters most | Put floor matters most |
| IV rises | Put value increases | Long put helps; short call may offset |
| IV falls | Protection mark declines | Mixed |

## 11.5.7 Failure Modes

- Paying too much for downside skew.
- Buying protection too late after volatility spike.
- Selecting a put strike too far out-of-the-money to provide useful protection.
- Selling a call strike too close and sacrificing too much upside.
- Ignoring tax, accounting, and mandate constraints.
- Treating zero-cost collars as free hedges.

## 11.5.8 Governance Checklist

- Define target drawdown reduction.
- Compare outright put, put spread, collar, and dynamic de-risking alternatives.
- Evaluate upside opportunity cost.
- Stress crash and strong-rally outcomes.
- Measure net vega and skew exposure.
- Define roll schedule and strike-selection rule.
- Monitor whether protection is still aligned with portfolio notional.

---

# 11.6 Case Study 4: Calendar Spread and Term-Structure Trade

## 11.6.1 Structure

A calendar spread usually sells a near-term option and buys a longer-term option at the same strike:

$$
\text{Long Calendar}=-1C(K,T_1)+1C(K,T_2),\quad T_2>T_1.
$$

The same structure can be built with puts. A diagonal spread uses different strikes and maturities:

$$
\text{Diagonal}=-1C(K_1,T_1)+1C(K_2,T_2),\quad T_2>T_1.
$$

## 11.6.2 Intended Economic Exposure

A long calendar often seeks to benefit from:

- selling rich front-end volatility;
- owning longer-dated vega;
- term-structure roll-down;
- spot remaining near the short strike;
- event premium in one maturity versus another.

It is not a pure volatility trade. It has path-dependent gamma and assignment risks.

## 11.6.3 Greek Profile

| Greek | Typical Long Calendar Profile |
|---|---|
| Delta | near neutral at initiation if ATM, but path-dependent |
| Gamma | often short front gamma near short expiry |
| Theta | often positive initially from short front option |
| Vega | usually positive net vega from long back option |
| Term vega | long back tenor, short front tenor |
| Vanna | material if spot moves across strike |
| Assignment risk | relevant for American short leg |

## 11.6.4 Term-Structure Signal

A term-structure richness signal can be:

$$
\text{TermScore}=Z(\sigma_{front}-\widehat{\sigma}_{front}^{fair})-Z(\sigma_{back}-\widehat{\sigma}_{back}^{fair})-Z(\text{EventRisk})-Z(\text{Cost}).
$$

Alternatively, use variance:

$$
\text{ForwardVariance}=\frac{\sigma_2^2\tau_2-\sigma_1^2\tau_1}{\tau_2-\tau_1}.
$$

Calendar trades should be analyzed in variance space because total variance is additive across time under simplified assumptions.

## 11.6.5 Preferred Regimes

More suitable:

- front implied volatility rich relative to expected near-term realized volatility;
- back implied volatility fairly priced or cheap;
- stable spot expected near strike;
- term structure expected to normalize favorably;
- liquidity sufficient in both maturities.

Less suitable:

- large spot movement expected;
- front volatility likely to spike;
- near-term event underpriced;
- short leg has assignment risk;
- bid-ask spreads are wide across legs.

## 11.6.6 Stress Scenarios

| Scenario | Expected Effect |
|---|---|
| Spot stable, front vol decays | Favorable for long calendar |
| Spot moves far from strike | Can lose as structure loses local edge |
| Front vol spikes | Short front leg hurts |
| Back vol rises more than front | Long back vega helps |
| Term structure flattens unfavorably | Loss possible |
| Short leg assigned | Operational and delta risk |

## 11.6.7 Failure Modes

- Underestimating short front gamma.
- Treating positive theta as safe carry.
- Ignoring event risk before front expiry.
- Poor execution of multi-leg spreads.
- Using calendar spreads in illiquid single-name options.
- Ignoring exercise and assignment risk.

---

# 11.7 Case Study 5: Dispersion Trade

## 11.7.1 Structure

A classic equity dispersion trade compares index volatility to single-name volatility. A common structure is:

$$
\text{Short Index Volatility}+\text{Long Single-Name Volatility Basket}.
$$

For example:

$$
-1\text{ Index Straddle}+\sum_{j=1}^{N}a_j\text{ Single-Name Straddle}_j.
$$

Weights $a_j$ may be based on index weights, vegas, variance notionals, or risk budgets.

## 11.7.2 Intended Economic Exposure

The trade is primarily a correlation risk-premium trade. Index variance depends on single-name variances and correlations:

$$
\sigma_I^2\approx\sum_{i=1}^{N}w_i^2\sigma_i^2+2\sum_{i<j}w_iw_j\rho_{ij}\sigma_i\sigma_j.
$$

If index implied volatility is rich relative to single-name implied volatility because implied correlation is high, a dispersion trade may seek to sell index correlation and buy single-name volatility.

## 11.7.3 Greek Profile

| Exposure | Typical Short-Correlation Dispersion |
|---|---|
| Index vega | short |
| Single-name vega | long |
| Net gamma | mixed |
| Correlation | short implied correlation |
| Skew | often short index skew and long single-name skew mix |
| Liquidity | many legs; execution intensive |
| Event risk | long many single-name event risks |

## 11.7.4 Implied Correlation Signal

A simplified implied correlation estimate is:

$$
\rho_{imp}\approx
\frac{\sigma_I^2-\sum_iw_i^2\sigma_i^2}
{2\sum_{i<j}w_iw_j\sigma_i\sigma_j}.
$$

A dispersion signal can be:

$$
\text{DispersionScore}=Z(\rho_{imp}-\widehat{\rho}_{real})+Z(\text{IndexVRP})-Z(\text{SingleNameEventRisk})-Z(\text{ExecutionCost}).
$$

## 11.7.5 Preferred Regimes

More suitable:

- implied correlation rich relative to forecast realized correlation;
- index protection demand high;
- single-name options not excessively expensive;
- single-name event risks diversified;
- market not entering broad correlation-spike stress;
- sufficient liquidity to manage many legs.

Less suitable:

- systemic crisis risk rising;
- correlation already rising;
- credit stress increasing;
- index skew steepening aggressively;
- single-name liquidity poor;
- many constituents have near-term earnings.

## 11.7.6 Stress Scenarios

| Scenario | Expected Effect |
|---|---|
| Realized correlation below implied | Favorable for short-correlation trade |
| Correlation spikes | Losses can be severe |
| Index sells off, skew steepens | Short index options lose |
| Single-name events diversify | Long single-name options may help |
| Single-name events cluster | Losses or gains depend on structure |
| Liquidity deteriorates | Rebalancing many legs becomes costly |

## 11.7.7 Failure Modes

- Correlation spike overwhelms single-name long-vol gains.
- Index skew steepens more than expected.
- Single-name basket is not representative of index risk.
- Earnings risk clusters in a sector.
- Execution costs across many legs consume edge.
- Margin increases on both index and single-name legs.
- Hedge ratios drift because vegas and deltas change.

## 11.7.8 Governance Checklist

- Estimate implied and forecast realized correlation.
- Control sector and factor exposures of single-name basket.
- Limit concentration in earnings windows.
- Stress index crash plus correlation spike.
- Monitor index versus single-name vega basis.
- Include realistic multi-leg execution costs.
- Track P&L by index leg, single-name leg, correlation proxy, and residual.

---

# 11.8 Case Study 6: Single-Stock Earnings Option Trade

## 11.8.1 Structure

An earnings option trade may buy or sell options expiring after a scheduled earnings announcement. Common structures include:

- long straddle;
- short straddle;
- long strangle;
- short strangle;
- call spread;
- put spread;
- calendar spread around earnings;
- iron condor.

Earnings trades are dominated by discrete event variance, not ordinary continuous diffusion.

## 11.8.2 Event Variance Decomposition

A stylized total variance decomposition is:

$$
\sigma_{imp}^2(\tau)\tau=\sigma_{diffusive}^2\tau+\omega_e^2,
$$

where:

- $\sigma_{imp}^2(\tau)\tau$ is total implied variance to maturity;
- $\sigma_{diffusive}^2$ is ordinary non-event variance;
- $\omega_e^2$ is implied earnings event variance.

The implied event move can be approximated as:

$$
\omega_e\approx\sqrt{\sigma_{post}^2\tau_{post}-\sigma_{pre}^2\tau_{pre}},
$$

when two maturities can be used to isolate the event, though real implementation requires careful interpolation and liquidity checks.

## 11.8.3 Long Earnings Straddle

A long earnings straddle buys event movement:

$$
+1C(K,T)+1P(K,T).
$$

It benefits if the realized earnings gap exceeds the implied move and if post-event volatility crush does not dominate.

Main exposures:

- long event gamma;
- long event vega before announcement;
- negative theta;
- exposed to volatility crush after earnings;
- gap-dependent payoff.

## 11.8.4 Short Earnings Straddle

A short earnings straddle sells event movement:

$$
-1C(K,T)-1P(K,T).
$$

It benefits if the realized move is smaller than the implied move and volatility collapses after the announcement.

Main exposures:

- short event gamma;
- short event vega;
- positive theta;
- exposed to large gap losses;
- high margin and liquidity risk.

## 11.8.5 Why Delta Hedging Does Not Solve Earnings Risk

Suppose a straddle is delta hedged before earnings. If the stock jumps from $S_-$ to $S_+$ overnight, the hedge was set using pre-event delta:

$$
h_-=-\Delta_-.
$$

The hedged event P&L is:

$$
\Delta\Pi^{event}=\left[V(S_+,\sigma_+,t_+)-V(S_-,\sigma_-,t_-)\right]+h_-(S_+-S_-).
$$

Because trading cannot occur continuously through the announcement gap, delta hedging does not eliminate event risk.

## 11.8.6 Preferred Regimes

Long event volatility is more suitable when:

- implied move is low relative to historical comparable earnings moves;
- uncertainty is unusually high;
- options liquidity is acceptable;
- the stock has high surprise sensitivity;
- analyst dispersion or guidance uncertainty is elevated.

Short event volatility is more suitable when:

- implied move is rich relative to robust event-move forecasts;
- event risk is diversified across many names;
- structures are defined-risk;
- liquidity is strong;
- position size is small relative to gap stress.

## 11.8.7 Failure Modes

Long event-volatility failures:

- realized move smaller than implied;
- volatility crush larger than expected;
- poor strike selection;
- spread costs too high;
- move occurs before entry or after exit.

Short event-volatility failures:

- large surprise gap;
- volatility does not crush enough;
- liquidity disappears;
- margin rises sharply;
- multiple names gap together due to macro or sector event.

## 11.8.8 Required Controls

- event calendar accuracy;
- historical event-move distribution;
- implied move calculation;
- volatility crush estimate;
- gap stress by downside and upside move;
- liquidity filter;
- defined-risk preference for short event vol;
- cap on aggregate event exposure by date and sector;
- no assumption of continuous hedging through event.

---

# 11.9 Case Study 7: Regime-Aware Options Sleeve Allocation

## 11.9.1 Structure

A regime-aware options allocation combines multiple strategy sleeves:

$$
\mathcal{S}=\{\text{long gamma},\text{short vol carry},\text{collars},\text{calendars},\text{dispersion},\text{long skew}\}.
$$

Let $w_{s,t}$ be the allocation to sleeve $s$ at time $t$.

The allocation is based on:

- strategy signal strength;
- regime probabilities;
- expected return;
- expected risk;
- Greek budgets;
- margin and liquidity limits;
- stress losses.

## 11.9.2 Regime Probability Mapping

Let $p_{k,t}$ be the probability of regime $k$, and let $\eta_{s,k}$ be the suitability of strategy sleeve $s$ in regime $k$.

The regime suitability score is:

$$
\text{Suitability}_{s,t}=\sum_{k=1}^{K}p_{k,t}\eta_{s,k}.
$$

The raw strategy allocation can be:

$$
w_{s,t}^{raw}=w_s^{max}\cdot\max(0,\text{Signal}_{s,t})\cdot\text{Suitability}_{s,t}\cdot\text{RiskScale}_{t}.
$$

Weights are normalized to target allocation:

$$
w_{s,t}=\frac{w_{s,t}^{raw}}{\sum_jw_{j,t}^{raw}}W_t^{target}.
$$

## 11.9.3 Sleeve Suitability Table

| Sleeve | Low-Vol Carry | Rising Vol | Stress | Normalization |
|---|---:|---:|---:|---:|
| Long gamma | low | high | medium-high | medium |
| Short vol carry | high | low | very low | medium-high |
| Collars | medium | high | high | medium |
| Calendars | medium-high | medium | low | high |
| Dispersion | medium | low-medium | low | medium |
| Long skew | low-medium | high | high | medium |

This table is conceptual. In production, suitability should be estimated, governed, and reviewed.

## 11.9.4 Greek Budget Constraints

Portfolio Greeks are:

$$
\mathbf{g}_{p,t}=\sum_s w_{s,t}\mathbf{g}_{s,t}.
$$

Constraints are:

$$
\mathbf{L}_{g,t}\le\mathbf{g}_{p,t}\le\mathbf{U}_{g,t}.
$$

Regime-dependent limits can be probability weighted:

$$
\mathbf{U}_{g,t}=\sum_kp_{k,t}\mathbf{U}_{g,k}.
$$

For example:

- allow more long gamma in rising-volatility regimes;
- reduce short gamma budget in stress regimes;
- reduce total margin usage when regime confidence is low;
- increase collar allocation when drawdown risk rises;
- cap negative vanna and volga in vol-of-vol expansion regimes.

## 11.9.5 Stress-Aware Allocation

A sleeve may have a high expected return but unacceptable stress loss. A stress-adjusted score is:

$$
\text{Score}_{s,t}=\frac{\widehat{\mu}_{s,t}}{\widehat{\sigma}_{s,t}+\epsilon}-\lambda_{ES}ES_{s,t}-\lambda_M\text{Margin}_{s,t}-\lambda_C\text{Cost}_{s,t}.
$$

Where:

- $\widehat{\mu}_{s,t}$ is expected return;
- $\widehat{\sigma}_{s,t}$ is expected volatility;
- $ES_{s,t}$ is expected shortfall or stress loss;
- margin and cost penalties reduce allocation.

## 11.9.6 Failure Modes

- Regime model overconfidence.
- Binary switching instead of probability-weighted allocation.
- Short-volatility sleeve dominates because of high carry.
- Long-gamma sleeve is cut too aggressively before volatility transition.
- Greek constraints satisfied in aggregate but violated by bucket.
- Stress losses ignored during optimizer allocation.
- Transaction costs from frequent regime switching destroy returns.

## 11.9.7 Governance Checklist

- Store regime probabilities and model version daily.
- Track allocation by sleeve and regime contribution.
- Monitor realized P&L versus expected regime behavior.
- Review entropy or confidence of regime model.
- Apply turnover penalty to reduce noisy reallocations.
- Validate strategy performance by realized regime, not only full sample.
- Stress all sleeves jointly under crash, volatility spike, skew steepening, and liquidity widening.

---

# 11.10 Integrated Case Study Comparison Matrix

| Strategy | Main Exposure | Preferred Regime | Main Benefit | Main Failure Mode |
|---|---|---|---|---|
| Delta-hedged long straddle | Long gamma and vega | Rising realized vol | Convexity and vol repricing | Theta bleed and vol crush |
| Short put carry | Short downside vol and skew | Stable carry | Premium income | Crash and margin spiral |
| Protective put | Long downside convexity | Rising downside risk | Drawdown protection | Expensive carry |
| Collar | Hedged equity with capped upside | Risk control regime | Lower-cost protection | Upside opportunity cost |
| Calendar | Term-structure vega | Stable spot, term mispricing | Roll and term carry | Front vol spike, short gamma |
| Dispersion | Correlation risk premium | Implied correlation rich | Relative vol/correlation alpha | Correlation spike |
| Earnings straddle | Event variance | Event mispricing | Gap exposure | Vol crush or gap surprise |
| Regime sleeve allocation | Diversified option premia | Probabilistic regimes | Adaptive exposure | Model and turnover risk |

## 11.11 Cross-Case P&L Attribution Framework

A common attribution framework supports all case studies:

At a high level:

**Total P&L = Delta P&L + Gamma P&L + Theta P&L + Vega P&L + Skew P&L + Term P&L + Rates P&L + Financing P&L + Costs P&L + Residual P&L.**

Definitions:

| Component | Meaning |
|---|---|
| Delta | Directional underlying exposure |
| Gamma | Convexity from realized movement |
| Theta | Time decay or carry |
| Vega | Parallel implied-volatility change |
| Skew | Relative volatility change across strikes |
| Term | Relative volatility change across maturities |
| Rates | Discount and forward impact |
| Financing | Cash, borrow, collateral, and margin funding |
| Costs | Spread, slippage, commissions, market impact |
| Residual | Jumps, model error, data issues, higher-order effects |

For institutional review, residual P&L should be investigated rather than ignored.

## 11.12 Cross-Case Stress Scenario Library

A practical scenario library should include:

| Scenario | Shock Design | Relevant Strategies |
|---|---|---|
| Calm decay | Spot flat, IV flat, time passes | Long gamma, protective puts |
| Moderate rally | Spot up 5%, IV down 2 vol points | Covered calls, collars, short puts |
| Moderate selloff | Spot down 5%, IV up 5 vol points | Short puts, collars, long gamma |
| Crash | Spot down 15%, IV up 20 vol points, skew steepens | Short vol, long skew, collars |
| Vol crush | IV down 8 vol points, spot stable | Long vega, earnings trades |
| Front vol spike | Front IV up 15 vol points, back IV up 5 | Calendars |
| Correlation spike | Index IV up, single-name diversification falls | Dispersion |
| Earnings gap | Single stock +/-20%, post-event IV crush | Earnings options |
| Liquidity shock | Spreads triple, impact doubles | All strategies |
| Margin shock | Required margin doubles after loss | Short gamma, short skew |

## 11.13 Python Code: Case Study Skeleton Framework

The following code provides a compact case-study engine. It is intentionally simplified and uses European Black-Scholes-Merton pricing. It is suitable for education, not production deployment.

```python
import math
from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd
from scipy.stats import norm

OptionType = Literal["call", "put"]


@dataclass(frozen=True)
class OptionSpec:
    spot: float
    strike: float
    tau: float
    rate: float
    dividend_yield: float
    volatility: float
    option_type: OptionType


@dataclass(frozen=True)
class Leg:
    name: str
    option: OptionSpec | None
    quantity: float
    multiplier: float = 100.0
    underlying_quantity: float = 0.0


@dataclass(frozen=True)
class Scenario:
    name: str
    spot_return: float = 0.0
    vol_shift: float = 0.0
    skew_shift: float = 0.0
    curvature_shift: float = 0.0
    time_passed: float = 0.0
    rate_shift: float = 0.0


def d1_d2(x: OptionSpec) -> tuple[float, float]:
    if x.spot <= 0 or x.strike <= 0 or x.tau <= 0 or x.volatility <= 0:
        raise ValueError("spot, strike, tau, and volatility must be positive")
    vol_sqrt_t = x.volatility * math.sqrt(x.tau)
    d1 = (
        math.log(x.spot / x.strike)
        + (x.rate - x.dividend_yield + 0.5 * x.volatility**2) * x.tau
    ) / vol_sqrt_t
    d2 = d1 - vol_sqrt_t
    return d1, d2


def price(x: OptionSpec) -> float:
    d1, d2 = d1_d2(x)
    df_r = math.exp(-x.rate * x.tau)
    df_q = math.exp(-x.dividend_yield * x.tau)
    if x.option_type == "call":
        return x.spot * df_q * norm.cdf(d1) - x.strike * df_r * norm.cdf(d2)
    return x.strike * df_r * norm.cdf(-d2) - x.spot * df_q * norm.cdf(-d1)


def greeks(x: OptionSpec) -> dict[str, float]:
    d1, d2 = d1_d2(x)
    df_r = math.exp(-x.rate * x.tau)
    df_q = math.exp(-x.dividend_yield * x.tau)
    phi = norm.pdf(d1)
    sqrt_t = math.sqrt(x.tau)
    gamma = df_q * phi / (x.spot * x.volatility * sqrt_t)
    vega = x.spot * df_q * phi * sqrt_t
    vanna = -df_q * phi * d2 / x.volatility
    volga = vega * d1 * d2 / x.volatility
    theta_common = -x.spot * df_q * phi * x.volatility / (2.0 * sqrt_t)
    if x.option_type == "call":
        delta = df_q * norm.cdf(d1)
        theta = theta_common - x.rate * x.strike * df_r * norm.cdf(d2) + x.dividend_yield * x.spot * df_q * norm.cdf(d1)
    else:
        delta = df_q * (norm.cdf(d1) - 1.0)
        theta = theta_common + x.rate * x.strike * df_r * norm.cdf(-d2) - x.dividend_yield * x.spot * df_q * norm.cdf(-d1)
    return {
        "price": price(x),
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "vanna": vanna,
        "volga": volga,
    }


def forward_log_moneyness(x: OptionSpec) -> float:
    fwd = x.spot * math.exp((x.rate - x.dividend_yield) * x.tau)
    return math.log(x.strike / fwd)


def shock_option(x: OptionSpec, s: Scenario) -> OptionSpec:
    k = forward_log_moneyness(x)
    new_spot = x.spot * (1.0 + s.spot_return)
    new_tau = max(x.tau - s.time_passed, 1e-8)
    new_vol = x.volatility + s.vol_shift + s.skew_shift * k + s.curvature_shift * k**2
    return OptionSpec(
        spot=new_spot,
        strike=x.strike,
        tau=new_tau,
        rate=x.rate + s.rate_shift,
        dividend_yield=x.dividend_yield,
        volatility=max(new_vol, 0.01),
        option_type=x.option_type,
    )


def evaluate_strategy(legs: list[Leg], scenarios: list[Scenario]) -> pd.DataFrame:
    rows = []
    for scn in scenarios:
        for leg in legs:
            if leg.option is None:
                base_value = leg.underlying_quantity * leg.quantity
                shocked_spot = leg.underlying_quantity * (1.0 + scn.spot_return)
                shocked_value = shocked_spot * leg.quantity
                rows.append({
                    "scenario": scn.name,
                    "leg": leg.name,
                    "base_value": base_value,
                    "shocked_value": shocked_value,
                    "full_pnl": shocked_value - base_value,
                    "delta": leg.quantity * leg.underlying_quantity,
                    "gamma": 0.0,
                    "vega_1vol": 0.0,
                    "theta_daily": 0.0,
                    "vanna_1vol": 0.0,
                    "volga_vol_point_sq": 0.0,
                })
                continue

            base = leg.option
            shocked = shock_option(base, scn)
            scale = leg.quantity * leg.multiplier
            g = greeks(base)
            rows.append({
                "scenario": scn.name,
                "leg": leg.name,
                "base_value": scale * price(base),
                "shocked_value": scale * price(shocked),
                "full_pnl": scale * (price(shocked) - price(base)),
                "delta": scale * g["delta"],
                "gamma_dollar": scale * g["gamma"] * base.spot**2,
                "vega_1vol": scale * g["vega"] / 100.0,
                "theta_daily": scale * g["theta"] / 365.0,
                "vanna_1vol": scale * g["vanna"] / 100.0,
                "volga_vol_point_sq": scale * g["volga"] / 10_000.0,
            })
    return pd.DataFrame(rows)


# Example: long ATM straddle.
base_call = OptionSpec(100, 100, 30 / 365, 0.04, 0.00, 0.20, "call")
base_put = OptionSpec(100, 100, 30 / 365, 0.04, 0.00, 0.20, "put")

long_straddle = [
    Leg("Long ATM call", base_call, quantity=10),
    Leg("Long ATM put", base_put, quantity=10),
]

scenarios = [
    Scenario("Calm decay", time_passed=1 / 365),
    Scenario("Spot up 5", spot_return=0.05, time_passed=1 / 365),
    Scenario("Spot down 5 vol up 5", spot_return=-0.05, vol_shift=0.05, time_passed=1 / 365),
    Scenario("Vol crush", vol_shift=-0.05, time_passed=1 / 365),
]

results = evaluate_strategy(long_straddle, scenarios)
print(results.groupby("scenario")[["full_pnl", "delta", "gamma_dollar", "vega_1vol", "theta_daily"]].sum().round(2))
```

## 11.14 Python Code: Case Study Ranking Table

The next code creates a high-level scorecard for multiple strategies. The weights are illustrative and should not be used without validation.

```python
def score_case_studies(strategy_features: pd.DataFrame) -> pd.DataFrame:
    """Score options strategies using stylized institutional criteria.

    Expected columns are scaled so higher is better except cost, stress_loss,
    margin, liquidity_cost, and model_risk, where higher is worse.
    """
    required = [
        "expected_return", "regime_fit", "hedging_utility", "diversification",
        "cost", "stress_loss", "margin", "liquidity_cost", "model_risk"
    ]
    missing = [c for c in required if c not in strategy_features.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = strategy_features.copy()
    df["institutional_score"] = (
        1.00 * df["expected_return"]
        + 0.80 * df["regime_fit"]
        + 0.70 * df["hedging_utility"]
        + 0.50 * df["diversification"]
        - 0.60 * df["cost"]
        - 1.00 * df["stress_loss"]
        - 0.70 * df["margin"]
        - 0.60 * df["liquidity_cost"]
        - 0.50 * df["model_risk"]
    )
    return df.sort_values("institutional_score", ascending=False)


features = pd.DataFrame(
    {
        "expected_return": [0.4, 0.7, 0.3, 0.5, 0.6],
        "regime_fit": [0.8, 0.4, 0.9, 0.6, 0.5],
        "hedging_utility": [0.9, 0.1, 0.8, 0.3, 0.2],
        "diversification": [0.6, 0.3, 0.5, 0.5, 0.7],
        "cost": [0.6, 0.3, 0.5, 0.4, 0.7],
        "stress_loss": [0.2, 0.9, 0.3, 0.5, 0.7],
        "margin": [0.3, 0.8, 0.4, 0.4, 0.7],
        "liquidity_cost": [0.4, 0.4, 0.3, 0.5, 0.8],
        "model_risk": [0.4, 0.6, 0.4, 0.5, 0.7],
    },
    index=["long_gamma", "short_put", "collar", "calendar", "dispersion"],
)

print(score_case_studies(features).round(3))
```

## 11.15 Production Case Study Checklist

Every strategy case study should include the following controls before inclusion in an institutional options program.

| Area | Required Output |
|---|---|
| Trade definition | Exact legs, strikes, maturities, quantities, hedge instruments |
| Economic hypothesis | Clear statement of risk premium or hedging utility |
| Greek profile | Delta, gamma, theta, vega, vanna, volga, skew, term exposure |
| Regime fit | Preferred and dangerous regimes |
| Expected return | Gross and net expected return estimate |
| Costs | Bid-ask, slippage, impact, hedge, financing, borrow |
| Margin | Normal and stressed margin |
| Liquidity | Open interest, volume, spread, exit horizon |
| P&L attribution | Delta, gamma, theta, vega, skew, term, costs, residual |
| Stress tests | Spot, vol, skew, term, correlation, liquidity, margin, event |
| Failure modes | Explicit list of ways the trade can lose money |
| Governance | Limits, kill switches, escalation, model versioning |

## 11.16 Summary of Part 11

Part 11 applied the full Greek-aware options framework to realistic strategy case studies.

Key points:

1. A delta-hedged long straddle is long gamma and vega but pays theta and requires realized movement or implied-volatility repricing to overcome cost.
2. Short put and put-spread carry strategies earn premium by selling downside insurance and must be managed through crash, margin, liquidity, and skew stress.
3. Protective puts and collars are portfolio insurance tools whose cost must be evaluated against drawdown reduction and upside opportunity cost.
4. Calendar spreads are term-structure trades with path-dependent gamma, vega, assignment, and event risks.
5. Dispersion trades are primarily correlation risk-premium trades, not just combinations of index and single-name volatility trades.
6. Earnings option trades are event-variance trades; continuous delta hedging does not eliminate earnings gap risk.
7. Regime-aware sleeve allocation combines signal strength, regime probabilities, strategy suitability, Greek constraints, risk scaling, and stress loss limits.
8. Across all strategies, P&L attribution should separate delta, gamma, theta, vega, skew, term, rates, financing, costs, and residuals.
9. Stress testing should use full repricing for large moves and report approximation error when Greek-based Taylor estimates are used.
10. A professional options case study must include trade structure, economic hypothesis, Greek map, regime fit, costs, margin, liquidity, stress tests, failure modes, and governance controls.

The next installment will cover Part 12: Final Reference Manual, Formula Compendium, Implementation Checklists, and Institutional Summary.
