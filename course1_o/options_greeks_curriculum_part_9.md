# Institutional Options Greeks, Systematic Strategy, and Regime-Aware Portfolio Construction Curriculum

## Completed Installment

This installment contains:

- Part 9: Risk Management, Stress Testing, and Failure Modes.

The document is educational and research-oriented. It is not personalized investment advice, a live trading recommendation, or a claim that any option strategy produces guaranteed alpha.

---

# Part 9: Risk Management, Stress Testing, and Failure Modes

**Level:** Expert

## 9.1 Purpose of Part 9

Options risk management is different from linear-asset risk management because option portfolios can change risk profile rapidly as spot, volatility, time, skew, liquidity, correlation, and margin conditions change. A portfolio can look diversified and stable under current Greeks while being fragile under a combined stress of spot movement, volatility repricing, skew steepening, liquidity deterioration, and margin expansion.

The purpose of Part 9 is to build a practical institutional risk-management and stress-testing framework. The focus is not only on measuring current Greeks, but on asking what can go wrong when the state of the world changes discontinuously.

The central principle is:

$$
\text{Options risk management must combine local Greeks, full repricing, stress scenarios, liquidity controls, and failure-mode analysis.}
$$

A robust options risk process should answer:

- What are the current portfolio Greeks and where are they concentrated?
- How much can the portfolio lose under spot, volatility, skew, rate, dividend, correlation, liquidity, borrow, and jump shocks?
- Are losses dominated by one strategy sleeve, one underlying, one sector, one maturity, one strike cluster, or one volatility-surface bucket?
- How do margin requirements and liquidity needs change during stress?
- Which risks are hedgeable and which are not hedgeable after a gap?
- When should risk be reduced automatically through kill-switch rules?
- When does a Taylor approximation fail and require full repricing?

Risk management is not a separate reporting layer added after portfolio construction. It must be embedded in trade selection, sizing, hedging, execution, and monitoring.

## 9.2 Risk Taxonomy for Options Portfolios

An institutional options portfolio is exposed to several categories of risk.

| Risk Type | Description | Typical Measurement | Main Failure Mode |
|---|---|---|---|
| Delta risk | First-order directional exposure to underlying price | Dollar delta, beta-adjusted delta | Unintended market or factor bet |
| Gamma risk | Convexity exposure to spot movement | Gamma dollars, scenario gamma P&L | Nonlinear losses for short gamma |
| Theta risk | Time decay or time carry | Daily theta, theta by maturity | Carry illusion and decay drag |
| Vega risk | Exposure to implied-volatility changes | Vega per vol point by tenor | Volatility spike or vol crush |
| Vanna risk | Spot-volatility interaction | Vanna by underlying and maturity | Delta/vega changes when spot and vol co-move |
| Volga risk | Volatility convexity | Volga by surface bucket | Vega-neutral book becomes exposed after vol shock |
| Skew risk | Exposure to relative volatility across strikes | Skew shock P&L | Downside skew steepens in stress |
| Term-structure risk | Exposure to volatility tenor changes | Term-vega buckets | Calendar spread basis loss |
| Correlation risk | Exposure to correlation among underlyings | Dispersion stress, implied correlation | Correlation spike during selloff |
| Jump/gap risk | Discontinuous spot movement | Jump scenarios, event loss | Hedge cannot be adjusted through gap |
| Liquidity risk | Inability to trade at assumed prices | Spread, volume, OI, market depth | Exit cost explodes in stress |
| Margin risk | Increase in required capital | Margin usage, stress margin | Forced deleveraging |
| Borrow risk | Cost or availability of short stock | Borrow rate, locate availability | Hedge becomes costly or impossible |
| Assignment/exercise risk | Early exercise or assignment uncertainty | In-the-money short options near ex-dividend/expiry | Unexpected underlying position |
| Model risk | Pricing or Greek model error | Model comparison, residual P&L | Misestimated exposures |
| Operational risk | Data, execution, or process failure | Exceptions, breaks, reconciliations | Incorrect trades or reports |

These risks interact. A short-put portfolio can simultaneously have positive theta, negative gamma, negative vega, short skew, negative liquidity exposure, and procyclical margin. The combination matters more than any one Greek.

## 9.3 Limit Framework

A risk limit is a pre-committed boundary on exposure, loss, liquidity usage, margin, concentration, or model uncertainty. Limits should be defined before stress occurs. A limit that is created after losses begin is usually a discretionary reaction, not a risk control.

## 9.3.1 Greek Limits

Let $G_p^{(m)}$ be portfolio exposure to Greek or risk factor $m$. A generic Greek limit is:

$$
L^{(m)} \le G_p^{(m)} \le U^{(m)},
$$

where:

- $L^{(m)}$ is the lower bound;
- $U^{(m)}$ is the upper bound;
- $m$ can be delta, gamma, vega, theta, rho, vanna, volga, skew exposure, or term-vega exposure.

Examples include:

$$
|\text{BetaAdjustedDollarDelta}_p| \le D_{\max},
$$

$$
G_{\min}^{\Gamma} \le \text{GammaDollar}_p \le G_{\max}^{\Gamma},
$$

$$
|\nu_{p,1m,ATM}^{1\text{ vol point}}| \le V_{1m,ATM}^{\max},
$$

$$
|\text{Vanna}_{p}| \le A_{\max},
$$

$$
|\text{Volga}_{p}| \le O_{\max}.
$$

Greek limits should exist at multiple levels:

- total portfolio;
- strategy sleeve;
- underlying;
- sector;
- country;
- maturity bucket;
- moneyness or delta bucket;
- event bucket;
- liquidity tier.

A portfolio can satisfy total vega limits but violate short-dated downside-put vega limits. A limit framework that only checks total Greeks is incomplete.

## 9.3.2 Drawdown Limits

Let $W_t$ be portfolio wealth or cumulative P&L and let:

$$
H_t=\max_{u\le t}W_u
$$

be the running high-water mark. Drawdown is:

$$
D_t=\frac{W_t}{H_t}-1.
$$

A drawdown limit is:

$$
D_t \ge -D_{\max}.
$$

For example, if $D_{\max}=0.10$, the strategy must not continue operating normally after a 10% drawdown without a pre-defined risk reduction, review, or kill-switch action.

A staged drawdown policy may be:

| Drawdown Level | Action |
|---:|---|
| $-3\%$ | Review P&L attribution and residuals |
| $-5\%$ | Reduce gross exposure or stop adding risk |
| $-7.5\%$ | Cut short convexity and high-margin positions |
| $-10\%$ | Activate portfolio-level kill switch |

The thresholds depend on mandate, capital base, strategy volatility, liquidity, and investor tolerance.

## 9.3.3 Margin Limits

Let $\mathcal{M}_t$ be required margin and $C_t$ be available capital or liquidity. Margin utilization is:

$$
U_t^{\mathcal{M}}=\frac{\mathcal{M}_t}{C_t}.
$$

A margin limit is:

$$
U_t^{\mathcal{M}} \le U_{\max}^{\mathcal{M}}.
$$

A stress margin limit applies after shocks:

$$
\frac{\mathcal{M}(S_t+\Delta S,\sigma_t+\Delta\sigma,\text{stress})}{C_t+\Delta \Pi_{stress}} \le U_{\max}^{\mathcal{M},stress}.
$$

This equation is critical because stress simultaneously changes the numerator and denominator:

- required margin rises;
- portfolio capital falls because of losses;
- liquidity deteriorates;
- financing haircuts may increase.

A portfolio that is acceptable under normal margin can become infeasible after a volatility shock.

## 9.3.4 Liquidity Limits

Liquidity limits prevent the portfolio from becoming too large relative to tradable market depth. For option $i$:

$$
|w_i| \le \lambda_{OI} OI_i,
$$

$$
|w_i| \le \lambda_{Vol}\text{Volume}_{i}^{(L)},
$$

$$
\text{BidAskPct}_{i} \le s_{\max},
$$

where:

- $OI_i$ is open interest;
- $\text{Volume}_{i}^{(L)}$ is average volume over lookback $L$;
- $\lambda_{OI}$ and $\lambda_{Vol}$ are capacity fractions;
- $\text{BidAskPct}_i$ is bid-ask spread divided by mid price.

A liquidation horizon constraint can be:

$$
\text{DaysToExit}_i=\frac{|w_i|}{\eta \cdot \text{ADV}_i} \le H_{\max},
$$

where $\eta$ is the assumed participation rate in market volume.

For single-name options, liquidity constraints should be stricter around earnings, market stress, and expiration.

## 9.3.5 Concentration Limits

Concentration limits control exposure to one underlying, sector, maturity, strategy, or risk factor.

Underlying concentration:

$$
\frac{|\text{StressLoss}_{j}|}{\sum_{k}|\text{StressLoss}_{k}|} \le c_{j}^{\max}.
$$

Sector concentration:

$$
|\text{SectorDelta}_{c}| \le D_c^{\max},
$$

$$
|\text{SectorVega}_{c}| \le V_c^{\max}.
$$

Maturity concentration:

$$
|\nu_{p,m}| \le V_m^{\max},
$$

where $m$ is a maturity bucket such as 0-7 days, 8-30 days, 31-90 days, 91-365 days, or longer than one year.

Strike concentration is especially important near expiration:

$$
\sum_{i:|K_i-S|/S\le \epsilon}|w_iM_i\Gamma_iS^2| \le G_{near\ strike}^{\max}.
$$

This controls pin risk and concentrated gamma near spot.

## 9.3.6 Scenario Limits

Scenario limits constrain losses under specified shocks. Let $\Delta V_{p,s}^{Full}$ be portfolio P&L under scenario $s$ computed by full repricing. A scenario limit is:

$$
\Delta V_{p,s}^{Full} \ge -L_s^{\max},\quad s=1,\ldots,S.
$$

Examples:

- equity down 5%, implied volatility up 5 vol points;
- equity down 10%, implied volatility up 15 vol points, skew steepens;
- single stock down 20% on earnings and implied volatility collapses;
- rates up 100 bps and equity volatility rises;
- liquidity spread doubles or triples;
- correlation spikes in dispersion book.

Scenario limits should include both historical scenarios and hypothetical forward-looking scenarios.

## 9.3.7 Kill-Switch Rules

A kill switch is a pre-defined action that reduces risk or stops trading when specified conditions occur. Kill switches should be rule-based, documented, and auditable.

Examples:

| Trigger | Possible Action |
|---|---|
| Intraday loss exceeds threshold | Stop adding risk; reduce gross exposure |
| Drawdown exceeds limit | Cut positions by pre-defined fraction |
| Margin utilization exceeds limit | Close highest-margin or least-liquid positions |
| Stress scenario loss exceeds limit | Reduce exposures driving scenario loss |
| Residual P&L unexplained beyond threshold | Pause strategy and investigate model/data issues |
| Bid-ask spreads exceed liquidity threshold | Stop initiating new trades in affected bucket |
| Data quality breach | Freeze automated trading or use fallback marks |
| Borrow unavailable | Stop strategies requiring short hedge |
| Regime model confidence collapses | Reduce risk scale |

A kill switch should not require subjective debate during a crisis. It should define who is notified, what is reduced, how quickly, and how reactivation occurs.

## 9.4 Stress Shock Types

Stress testing should include shocks to all major state variables. A one-dimensional stress such as “spot down 5%” is not enough for options.

## 9.4.1 Spot Shocks

A spot shock changes the underlying price:

$$
S_{j}^{shock}=S_j(1+r_j^{shock}),
$$

where $r_j^{shock}$ is the shocked return for underlying $j$.

Common spot shock types:

- parallel equity index shock;
- sector-specific shock;
- single-name earnings gap;
- factor shock such as momentum unwind or value rotation;
- currency shock for FX-sensitive assets;
- commodity shock for commodity-linked equities.

For options, spot shocks should be combined with volatility and skew shocks because spot and volatility are not independent during stress.

## 9.4.2 Volatility Shocks

A parallel implied-volatility shock is:

$$
\sigma_{i}^{shock}=\max(\sigma_{floor},\sigma_i+\Delta\sigma),
$$

where $\Delta\sigma$ is measured in decimal volatility units. A 10 vol-point shock means $\Delta\sigma=0.10$.

Volatility shocks can be:

- parallel across all strikes and maturities;
- larger in the front end;
- larger in downside strikes;
- larger for single stocks than indices;
- larger for illiquid names;
- regime-dependent.

## 9.4.3 Skew Shocks

Let $k_i=\ln(K_i/F_i)$ be forward log-moneyness. A skew shock can be represented as:

$$
\sigma_i^{shock}=\sigma_i+a_1 k_i.
$$

If $a_1<0$, downside options with $k_i<0$ receive positive volatility shocks and upside options with $k_i>0$ receive negative volatility shocks. This is an equity-like downside skew steepening.

A more complete shock is:

$$
\sigma_i^{shock}=\sigma_i+a_0+a_1k_i+a_2k_i^2,
$$

where:

- $a_0$ is the parallel volatility shock;
- $a_1$ is the skew slope shock;
- $a_2$ is the curvature or wing-richness shock.

## 9.4.4 Rate Shocks

A rate shock changes discount rates and forwards. A simple parallel rate shock is:

$$
r^{shock}=r+\Delta r.
$$

For term-structured rates, a curve shock is:

$$
r^{shock}(\tau)=r(\tau)+\Delta r(\tau).
$$

Rate shocks matter for:

- long-dated equity options;
- index options through forward pricing;
- FX options through interest-rate differentials;
- rates options directly;
- macro regimes where rates and equity volatility move together.

A rate shock may also affect implied volatility, not only discounting.

## 9.4.5 Dividend Shocks

Dividend shocks change forward prices and early exercise incentives. With continuous dividend yield:

$$
q^{shock}=q+\Delta q.
$$

For discrete dividends, shocks may affect dividend amount or ex-date:

$$
D_{m}^{shock}=D_m+\Delta D_m.
$$

Dividend shocks matter for:

- index options with uncertain dividends;
- single-stock options around ex-dividend dates;
- American calls where early exercise may become optimal;
- option parity and synthetic forwards.

## 9.4.6 Correlation Shocks

Correlation shocks are central for index options and dispersion trades. A simple average correlation shock is:

$$
\rho_{ij}^{shock}=\rho_{ij}+\Delta\rho(1-\rho_{ij}),
$$

where $\Delta\rho\in[0,1]$ pushes correlations toward one.

Index variance is approximately:

$$
\sigma_I^2\approx\sum_{i=1}^{N}w_i^2\sigma_i^2+2\sum_{i<j}w_iw_j\rho_{ij}\sigma_i\sigma_j.
$$

When correlations rise, index variance can increase even if single-name variances do not rise proportionally. A dispersion book that is short index volatility and long single-name volatility is exposed to correlation spikes.

## 9.4.7 Liquidity Shocks

Liquidity shocks increase spreads, reduce executable size, and increase impact. A spread shock can be:

$$
\text{Spread}_i^{shock}=\text{Spread}_i(1+\lambda_{liq}),
$$

where $\lambda_{liq}>0$ is the spread widening multiplier.

An impact shock can be:

$$
\eta_i^{shock}=\eta_i(1+\lambda_{impact}).
$$

Liquidity shock P&L is not only mark-to-market loss. It affects exit cost, hedge cost, and ability to reduce risk.

## 9.4.8 Borrow Shocks

Borrow shocks affect strategies requiring short stock hedges. Borrow rate shock:

$$
b_j^{shock}=b_j+\Delta b_j.
$$

Locate availability shock:

$$
\text{LocateAvailable}_{j}^{shock}<|h_j^{-}|.
$$

If locate availability becomes insufficient, a delta hedge may become impossible. This risk is particularly important for hard-to-borrow single stocks, merger situations, distressed equities, and crowded shorts.

## 9.4.9 Jump Shocks

Jump shocks model discontinuous moves:

$$
S_{j}^{shock}=S_j(1+J_j),
$$

where $J_j$ is a jump return such as $-20\%$, $+30\%$, or a distributional draw.

Jump shocks should often include volatility repricing:

$$
\sigma_{j}^{shock}=\sigma_j+g(J_j),
$$

where $g(J_j)$ maps jump direction and magnitude to implied-volatility change. For equity downside jumps, $g(J_j)$ is often positive before liquidity and skew adjustments.

For earnings events, implied volatility may collapse after the jump:

$$
\sigma_{post}^{shock}=\sigma_{pre}-\Delta\sigma_{event},
$$

even when spot jumps sharply. This makes earnings stress different from market crash stress.

## 9.5 Nonlinear Risk Under Large Moves

Local Greeks are derivatives evaluated at the current state. They are useful for small moves. Large moves require full repricing because Greeks change as the state changes.

A second-order Taylor approximation is:

$$
\Delta V^{Taylor}
=\Delta\Delta S+rac{1}{2}\Gamma(\Delta S)^2+
u\Delta\sigma+\Theta\Delta t+\rho\Delta r.
$$

A higher-order approximation adds:

$$
\text{Vanna}\Delta S\Delta\sigma+rac{1}{2}\text{Volga}(\Delta\sigma)^2+rac{1}{6}\text{Speed}(\Delta S)^3+\cdots.
$$

Full repricing is:

$$
\Delta V^{Full}=V(S+\Delta S,K,T-\Delta t,r+\Delta r,q+\Delta q,\sigma^{shock})-V(S,K,T,r,q,\sigma).
$$

The approximation error is:

$$
\varepsilon^{Taylor}=\Delta V^{Full}-\Delta V^{Taylor}.
$$

Large approximation errors occur when:

- options are near expiration;
- options are near the strike;
- spot shocks are large;
- implied volatility shocks are large;
- skew changes materially;
- jumps occur;
- early exercise or assignment matters;
- options are deeply in- or out-of-the-money;
- the pricing model is nonlinear or path-dependent.

The risk process should report approximation error in stress testing. If the error is large, relying on local Greeks for that scenario is not acceptable.

## 9.6 Key Failure Modes

## 9.6.1 Gap Risk

Gap risk is the risk that the underlying moves discontinuously before the hedge can be adjusted. If spot jumps from $S_-$ to $S_+$, the actual option P&L is:

$$
\Delta V^{gap}=V(S_+,\sigma_+,t_+)-V(S_-,\sigma_-,t_-).
$$

A pre-gap delta hedge $h_-=-\Delta_-$ generates hedge P&L:

$$
\Delta H^{gap}=h_-(S_+-S_-).
$$

The hedged gap P&L is:

$$
\Delta \Pi^{gap}=\Delta V^{gap}+\Delta H^{gap}.
$$

This can be very different from continuous-hedging expectations. Gap risk dominates earnings trades, takeover events, macro announcements, and crisis opens.

## 9.6.2 Volatility-of-Volatility Risk

Vol-of-vol risk is the risk that implied volatility changes are themselves volatile and nonlinear. A vega-neutral portfolio can still lose money if it is short volga:

$$
\Delta V_{vol}
\approx
\nu\Delta\sigma+rac{1}{2}\text{Volga}(\Delta\sigma)^2.
$$

If $\nu\approx0$ but $\text{Volga}<0$, a large volatility shock can produce losses through the second term. Volga and vanna limits are therefore necessary for books that claim to be vega-neutral.

## 9.6.3 Correlation Breakdown

Correlation breakdown occurs when historical correlations fail to describe stress co-movement. Diversification assumptions can fail because:

- correlations rise toward one in equity selloffs;
- single-name idiosyncratic events dominate correlations;
- index options reprice correlation risk faster than single-name options;
- liquidity-driven selling creates common movement;
- hedging flows become one-sided.

For dispersion trades, a correlation spike can cause losses even if individual single-name volatility positions appear reasonable.

## 9.6.4 Crowded Trade Unwind

Crowded trades are vulnerable because many participants may need to reduce similar exposures simultaneously. Common crowded option exposures include:

- short index volatility;
- short downside skew;
- covered-call overwriting;
- short-dated option selling;
- dispersion carry;
- yield-enhancement notes;
- volatility-control fund de-risking;
- dealer gamma hedging around large strikes.

Crowded unwind risk is difficult to measure directly. Proxies include option volume, open interest concentration, dealer gamma estimates, structured product issuance, short interest, ETF flows, and abnormal skew richness.

## 9.6.5 Early Assignment and Exercise Risk

American options can be exercised early. Short option positions can be assigned. Early exercise is especially relevant for:

- deep-in-the-money calls before ex-dividend dates;
- deep-in-the-money puts when rates and borrow matter;
- hard-to-borrow names;
- options near expiration;
- special dividends or corporate actions.

Unexpected assignment can create:

- long or short stock positions;
- borrow needs;
- financing needs;
- tax and operational issues;
- unwanted delta exposure.

A short call near ex-dividend may be assigned if early exercise is economically rational for the holder. A risk system should flag short American options with high assignment probability.

## 9.6.6 Model Risk

Model risk occurs when the pricing model, volatility surface, dividend input, rate curve, borrow assumption, or Greek calculation is wrong or inappropriate.

Examples:

- using European Black-Scholes for American single-stock options with discrete dividends;
- ignoring borrow costs in hard-to-borrow names;
- using flat volatility Greeks for a skewed surface;
- treating stale quotes as executable marks;
- using current index constituents in historical backtests;
- using revised macro data in regime signals;
- assuming continuous hedging through overnight events.

Model risk should be monitored through independent price checks, vendor comparison, P&L attribution residuals, and stress tests.

## 9.6.7 Why Short-Volatility Strategies Can Look Stable Until They Break

Short-volatility strategies often have return profiles with many small gains and rare large losses. This creates misleading historical statistics.

A simplified return distribution may be:

$$
R_t=\begin{cases}
+c, & \text{with probability }1-p, \\
-L, & \text{with probability }p,
\end{cases}
$$

where $c>0$ is small carry, $L>0$ is a large loss, and $p$ is small. The expected return is:

$$
\mathbb{E}[R]=(1-p)c-pL.
$$

Even if historical observations show many $+c$ outcomes, the strategy can have negative expected return if $pL$ is underestimated. The sample Sharpe ratio may look high before the rare loss occurs.

This is why short-volatility evaluation must include:

- expected shortfall;
- worst historical windows;
- hypothetical crash scenarios;
- margin stress;
- liquidity stress;
- skew steepening;
- jump risk;
- drawdown recovery time.

## 9.7 Scenario Tables by Strategy Type

The following tables summarize stylized stress behavior. Actual results depend on strikes, maturities, hedge rules, volatility surface, sizing, and costs.

## 9.7.1 Long Gamma Strategy

| Scenario | Expected Effect | Key Risk |
|---|---|---|
| Spot moves sharply, IV stable | Positive gamma P&L if hedged effectively | Hedge execution cost |
| Spot flat, IV stable | Negative theta | Carry bleed |
| Spot falls, IV rises | Often favorable for long puts/straddles | Entry vol may have been expensive |
| IV falls sharply | Negative vega P&L | Vol crush |
| Liquidity worsens | Exit and hedge costs rise | Monetization risk |
| Jump occurs | Can be favorable if long appropriate tail | Hedge may not capture full theoretical value |

## 9.7.2 Short Gamma Strategy

| Scenario | Expected Effect | Key Risk |
|---|---|---|
| Spot stable, IV stable | Positive theta | Carry can create complacency |
| Spot moves sharply | Negative gamma P&L | Loss accelerates |
| Spot falls, IV rises | Negative gamma and negative vega | Crash loss |
| Skew steepens | Loss for short downside options | Tail repricing |
| Liquidity worsens | Exit cost rises | Forced hold or expensive unwind |
| Margin rises | Capital pressure | Forced deleveraging |

## 9.7.3 Long Vega Strategy

| Scenario | Expected Effect | Key Risk |
|---|---|---|
| IV rises | Positive vega P&L | Vol increase may already be priced |
| IV falls | Negative vega P&L | Vol crush |
| Spot moves but IV falls | Mixed; gamma may help, vega hurts | Event risk after resolution |
| Term structure shifts | Depends on tenor exposure | Term basis |
| Vol-of-vol rises | Positive if long volga | Model and execution risk |
| Time passes quietly | Often negative carry | Theta bleed |

## 9.7.4 Short Vega Strategy

| Scenario | Expected Effect | Key Risk |
|---|---|---|
| IV falls | Positive vega P&L | Crowded post-shock short vol |
| IV rises | Negative vega P&L | Vol spike |
| Spot falls and IV rises | Often severe loss | Equity stress beta |
| Skew steepens | Loss if short downside vol | Crash skew |
| Liquidity worsens | Mark and exit cost worsen | Liquidity gap |
| Margin rises | Capital usage increases | Procyclical deleveraging |

## 9.7.5 Collars

| Scenario | Expected Effect | Key Risk |
|---|---|---|
| Moderate rally | Underperforms due to short call | Opportunity cost |
| Large rally | Upside capped | Assignment/roll decision |
| Moderate selloff | Put protection helps | Put strike may be too low |
| Crash | Protection depends on put strike and liquidity | Gap below hedge design |
| Skew steepens | Long put gains, short call may fall | Mark-to-market complexity |
| IV falls | Mixed vega exposure | Hedge value decays |

## 9.7.6 Calendars

| Scenario | Expected Effect | Key Risk |
|---|---|---|
| Spot stable | Often favorable near short strike | Pin and assignment risk |
| Large spot move | Can lose as short leg becomes problematic | Path dependence |
| Front IV rises | Can hurt if short front vol | Event repricing |
| Back IV rises | Helps if long back vol | Term basis uncertainty |
| Term structure normalizes | Depends on structure | Roll assumption failure |
| Liquidity worsens | Multi-leg unwind costly | Execution risk |

## 9.7.7 Dispersion

| Scenario | Expected Effect | Key Risk |
|---|---|---|
| Realized correlation below implied | Favorable for short-correlation dispersion | Single-name event losses |
| Correlation spike | Loss for short-correlation trade | Crisis co-movement |
| Index skew steepens | Loss if short index downside | Crash risk |
| Single-name IV rises | Helps long single-name vol leg | Event concentration |
| Liquidity worsens | Many legs become costly | Rebalancing and exit complexity |
| Index gap | Short index gamma can dominate | Tail loss |

## 9.7.8 Short-Skew Strategy

| Scenario | Expected Effect | Key Risk |
|---|---|---|
| Skew flattens | Favorable | Carry may be small after costs |
| Spot stable | Theta may help | Hidden tail exposure |
| Spot falls | Loss on downside options | Negative convexity |
| Skew steepens | Large mark-to-market loss | Crash protection repricing |
| Liquidity worsens | Exit becomes expensive | One-sided market |
| Jump down | Severe loss | Gap and margin risk |

## 9.8 Full Repricing Versus Taylor Approximation

## 9.8.1 Taylor Approximation

A Taylor approximation uses local Greeks to approximate P&L:

$$
\Delta V_i^{Taylor}
=\Delta_i\Delta S_i+rac{1}{2}\Gamma_i(\Delta S_i)^2+
u_i\Delta\sigma_i+ho_i\Delta r_i+\Theta_i\Delta t.
$$

A higher-order approximation is:

$$
\Delta V_i^{Taylor2}
=\Delta V_i^{Taylor}
+\text{Vanna}_i\Delta S_i\Delta\sigma_i
+\frac{1}{2}\text{Volga}_i(\Delta\sigma_i)^2.
$$

Taylor approximations are useful for:

- daily P&L attribution;
- local exposure reporting;
- fast pre-trade checks;
- optimizer constraints;
- explaining small moves.

They are weak for:

- large spot moves;
- large volatility moves;
- options near expiration;
- discontinuous jumps;
- surface reshaping;
- American exercise;
- path-dependent derivatives;
- illiquid options with unreliable marks.

## 9.8.2 Full Repricing

Full repricing recalculates option value under the shocked state:

$$
\Delta V_i^{Full}=V_i(\mathbf{x}_{i}^{shock})-V_i(\mathbf{x}_{i}^{base}),
$$

where $\mathbf{x}_i$ includes spot, volatility surface, rates, dividends, borrow, time, and exercise assumptions.

Full repricing is preferred for stress testing because it captures nonlinear changes in option value. It should be used for:

- portfolio stress tests;
- scenario limits;
- margin stress;
- jump scenarios;
- earnings scenarios;
- liquidity-adjusted exit analysis;
- risk committee reporting.

## 9.8.3 Approximation Error Report

For each scenario $s$, report:

$$
\varepsilon_{p,s}=\Delta V_{p,s}^{Full}-\Delta V_{p,s}^{Taylor}.
$$

A useful diagnostic is relative error:

$$
\text{RelativeError}_{p,s}=\frac{|\varepsilon_{p,s}|}{|\Delta V_{p,s}^{Full}|+\epsilon},
$$

where $\epsilon>0$ prevents division by zero.

If relative error is large, the scenario should be explained using full repricing rather than local Greeks.

## 9.9 Python Code: Pricing and Greek Building Blocks

The following code implements European Black-Scholes-Merton pricing and Greeks needed for stress testing. It is educational and does not handle American exercise, discrete dividends, borrow, or corporate actions.

```python
import math
from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd
from scipy.stats import norm

OptionType = Literal["call", "put"]


@dataclass(frozen=True)
class BSMOption:
    """European option input for stress testing.

    Parameters
    ----------
    spot:
        Underlying spot price. Must be positive.
    strike:
        Strike price. Must be positive.
    tau:
        Time to maturity in years. Must be positive.
    rate:
        Continuously compounded risk-free rate as decimal.
    dividend_yield:
        Continuous dividend yield as decimal.
    volatility:
        Annualized implied volatility as decimal.
    option_type:
        "call" or "put".
    """

    spot: float
    strike: float
    tau: float
    rate: float
    dividend_yield: float
    volatility: float
    option_type: OptionType


def validate_option(x: BSMOption) -> None:
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


def replace_option(x: BSMOption, **updates) -> BSMOption:
    data = x.__dict__.copy()
    data.update(updates)
    return BSMOption(**data)


def bsm_d1_d2(x: BSMOption) -> tuple[float, float]:
    validate_option(x)
    vol_sqrt_tau = x.volatility * math.sqrt(x.tau)
    d1 = (
        math.log(x.spot / x.strike)
        + (x.rate - x.dividend_yield + 0.5 * x.volatility**2) * x.tau
    ) / vol_sqrt_tau
    d2 = d1 - vol_sqrt_tau
    return d1, d2


def bsm_price(x: BSMOption) -> float:
    d1, d2 = bsm_d1_d2(x)
    df_r = math.exp(-x.rate * x.tau)
    df_q = math.exp(-x.dividend_yield * x.tau)
    if x.option_type == "call":
        return x.spot * df_q * norm.cdf(d1) - x.strike * df_r * norm.cdf(d2)
    return x.strike * df_r * norm.cdf(-d2) - x.spot * df_q * norm.cdf(-d1)


def bsm_greeks(x: BSMOption) -> dict[str, float]:
    """Return core and selected higher-order Greeks.

    Conventions
    -----------
    - Theta is annualized calendar-time theta, dV/dt.
    - Vega is per 1.00 volatility unit.
    - Rho is per 1.00 rate unit.
    - Vanna is per 1 spot unit and 1.00 volatility unit.
    - Volga is per 1.00 volatility unit squared.
    """
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
        "vanna": vanna,
        "volga": volga,
    }
```

## 9.10 Python Code: Portfolio Stress Testing Using Full Repricing and Greek Approximation

The next code defines option positions and stress scenarios. It calculates both full repricing P&L and Taylor-approximation P&L.

```python
@dataclass(frozen=True)
class OptionPosition:
    """Option position for stress testing."""

    option: BSMOption
    quantity: float
    multiplier: float = 100.0
    underlying: str = "UNKNOWN"
    sector: str = "UNKNOWN"
    label: str = ""


@dataclass(frozen=True)
class StressScenario:
    """Stress scenario specification.

    All shocks use decimal units. A 5% spot drop is spot_return=-0.05.
    A 10 vol-point volatility shock is vol_shift=0.10.
    A 100 bp rate shock is rate_shift=0.01.
    """

    name: str
    spot_return: float = 0.0
    vol_shift: float = 0.0
    skew_slope_shift: float = 0.0
    curvature_shift: float = 0.0
    rate_shift: float = 0.0
    dividend_yield_shift: float = 0.0
    time_passed: float = 0.0
    liquidity_spread_multiplier: float = 1.0


def forward_log_moneyness(option: BSMOption) -> float:
    forward = option.spot * math.exp((option.rate - option.dividend_yield) * option.tau)
    return math.log(option.strike / forward)


def apply_scenario_to_option(option: BSMOption, scenario: StressScenario) -> BSMOption:
    """Return shocked option inputs under a scenario."""
    if scenario.spot_return <= -1.0:
        raise ValueError("spot_return must be greater than -100%")

    shocked_spot = option.spot * (1.0 + scenario.spot_return)
    shocked_tau = max(option.tau - scenario.time_passed, 1e-8)
    shocked_rate = option.rate + scenario.rate_shift
    shocked_dividend = option.dividend_yield + scenario.dividend_yield_shift

    # Use current forward log-moneyness for stylized skew and curvature shock.
    k = forward_log_moneyness(option)
    shocked_vol = (
        option.volatility
        + scenario.vol_shift
        + scenario.skew_slope_shift * k
        + scenario.curvature_shift * k**2
    )
    shocked_vol = max(shocked_vol, 0.01)

    return replace_option(
        option,
        spot=shocked_spot,
        tau=shocked_tau,
        rate=shocked_rate,
        dividend_yield=shocked_dividend,
        volatility=shocked_vol,
    )


def greek_taylor_pnl(option: BSMOption, scenario: StressScenario) -> dict[str, float]:
    """Calculate Greek-based Taylor P&L approximation for one option."""
    g = bsm_greeks(option)
    shocked = apply_scenario_to_option(option, scenario)

    d_s = shocked.spot - option.spot
    d_vol = shocked.volatility - option.volatility
    d_rate = shocked.rate - option.rate
    d_time = scenario.time_passed

    delta_pnl = g["delta"] * d_s
    gamma_pnl = 0.5 * g["gamma"] * d_s**2
    theta_pnl = g["theta"] * d_time
    vega_pnl = g["vega"] * d_vol
    rho_pnl = g["rho"] * d_rate
    vanna_pnl = g["vanna"] * d_s * d_vol
    volga_pnl = 0.5 * g["volga"] * d_vol**2

    first_second_order = delta_pnl + gamma_pnl + theta_pnl + vega_pnl + rho_pnl
    higher_order = vanna_pnl + volga_pnl

    return {
        "delta_pnl": delta_pnl,
        "gamma_pnl": gamma_pnl,
        "theta_pnl": theta_pnl,
        "vega_pnl": vega_pnl,
        "rho_pnl": rho_pnl,
        "vanna_pnl": vanna_pnl,
        "volga_pnl": volga_pnl,
        "taylor_pnl_core": first_second_order,
        "taylor_pnl_with_vanna_volga": first_second_order + higher_order,
    }


def stress_position(position: OptionPosition, scenario: StressScenario) -> dict[str, float | str]:
    """Stress one option position using full repricing and Taylor approximation."""
    base = position.option
    shocked = apply_scenario_to_option(base, scenario)
    base_price = bsm_price(base)
    shocked_price = bsm_price(shocked)
    full_pnl_per_option = shocked_price - base_price
    taylor = greek_taylor_pnl(base, scenario)
    scale = position.quantity * position.multiplier

    # Stylized liquidity exit cost. For production, use option bid/ask and market depth.
    liquidity_cost = abs(scale) * base_price * max(scenario.liquidity_spread_multiplier - 1.0, 0.0) * 0.005

    full_position_pnl = scale * full_pnl_per_option - liquidity_cost
    taylor_core = scale * taylor["taylor_pnl_core"] - liquidity_cost
    taylor_vv = scale * taylor["taylor_pnl_with_vanna_volga"] - liquidity_cost

    return {
        "scenario": scenario.name,
        "label": position.label,
        "underlying": position.underlying,
        "sector": position.sector,
        "quantity": position.quantity,
        "base_price": base_price,
        "shocked_price": shocked_price,
        "full_pnl": full_position_pnl,
        "taylor_core_pnl": taylor_core,
        "taylor_vanna_volga_pnl": taylor_vv,
        "approx_error_core": full_position_pnl - taylor_core,
        "approx_error_vanna_volga": full_position_pnl - taylor_vv,
        "liquidity_cost": liquidity_cost,
        "base_delta": scale * bsm_greeks(base)["delta"],
        "base_gamma_dollar": scale * bsm_greeks(base)["gamma"] * base.spot**2,
        "base_vega_1vol": scale * bsm_greeks(base)["vega"] / 100.0,
        "base_theta_daily": scale * bsm_greeks(base)["theta"] / 365.0,
    }


def stress_portfolio(positions: list[OptionPosition], scenarios: list[StressScenario]) -> pd.DataFrame:
    """Stress a portfolio across scenarios."""
    rows = []
    for scenario in scenarios:
        for position in positions:
            rows.append(stress_position(position, scenario))
    return pd.DataFrame(rows)


# Example portfolio and scenarios.
positions = [
    OptionPosition(
        option=BSMOption(100.0, 95.0, 45 / 365, 0.04, 0.01, 0.24, "put"),
        quantity=20,
        multiplier=100,
        underlying="INDEX",
        sector="Index",
        label="Long downside puts",
    ),
    OptionPosition(
        option=BSMOption(100.0, 105.0, 45 / 365, 0.04, 0.01, 0.20, "call"),
        quantity=-15,
        multiplier=100,
        underlying="INDEX",
        sector="Index",
        label="Short upside calls",
    ),
    OptionPosition(
        option=BSMOption(100.0, 100.0, 180 / 365, 0.04, 0.01, 0.22, "call"),
        quantity=10,
        multiplier=100,
        underlying="INDEX",
        sector="Index",
        label="Long 6m ATM calls",
    ),
]

scenarios = [
    StressScenario(name="Spot down 5, vol up 5", spot_return=-0.05, vol_shift=0.05),
    StressScenario(
        name="Crash: spot down 15, vol up 20, skew steepens",
        spot_return=-0.15,
        vol_shift=0.20,
        skew_slope_shift=-0.20,
        curvature_shift=0.15,
        liquidity_spread_multiplier=3.0,
    ),
    StressScenario(name="Vol crush", spot_return=0.00, vol_shift=-0.08, time_passed=1 / 365),
    StressScenario(name="Rates up 100bp", rate_shift=0.01),
]

stress_df = stress_portfolio(positions, scenarios)
print(stress_df.round(4))

scenario_summary = stress_df.groupby("scenario")[[
    "full_pnl", "taylor_core_pnl", "taylor_vanna_volga_pnl",
    "approx_error_core", "approx_error_vanna_volga", "liquidity_cost"
]].sum()
print(scenario_summary.round(2))
```

## 9.11 Python Code: Scenario Limits and Kill-Switch Diagnostics

The following code converts stress results into limit diagnostics.

```python
def evaluate_scenario_limits(
    stress_results: pd.DataFrame,
    scenario_loss_limits: dict[str, float],
) -> pd.DataFrame:
    """Evaluate full repricing P&L against scenario loss limits.

    scenario_loss_limits maps scenario name to maximum allowed loss as a
    positive number. For example, {"Crash": 50000} means full P&L must be
    greater than or equal to -50000.
    """
    summary = stress_results.groupby("scenario")["full_pnl"].sum().to_frame("full_pnl")
    rows = []
    for scenario, row in summary.iterrows():
        limit = scenario_loss_limits.get(scenario, np.inf)
        pnl = row["full_pnl"]
        rows.append(
            {
                "scenario": scenario,
                "full_pnl": pnl,
                "max_allowed_loss": limit,
                "limit_breached": pnl < -limit,
                "excess_loss": max(0.0, -pnl - limit),
            }
        )
    return pd.DataFrame(rows)


def kill_switch_diagnostics(
    current_drawdown: float,
    margin_utilization: float,
    scenario_limit_results: pd.DataFrame,
    unexplained_pnl_ratio: float,
    drawdown_limit: float = 0.10,
    margin_limit: float = 0.75,
    unexplained_pnl_limit: float = 0.25,
) -> dict[str, object]:
    """Return simple kill-switch diagnostics.

    current_drawdown is positive for loss from high-water mark. For example,
    0.08 means an 8% drawdown.
    """
    breached_scenarios = scenario_limit_results[scenario_limit_results["limit_breached"]]
    triggers = []

    if current_drawdown >= drawdown_limit:
        triggers.append("drawdown_limit")
    if margin_utilization >= margin_limit:
        triggers.append("margin_limit")
    if len(breached_scenarios) > 0:
        triggers.append("scenario_limit")
    if unexplained_pnl_ratio >= unexplained_pnl_limit:
        triggers.append("unexplained_pnl_limit")

    if not triggers:
        action = "normal_monitoring"
    elif "drawdown_limit" in triggers or "margin_limit" in triggers:
        action = "reduce_risk_immediately"
    elif "scenario_limit" in triggers:
        action = "reduce_scenario_exposure"
    else:
        action = "pause_and_investigate"

    return {
        "triggers": triggers,
        "recommended_action": action,
        "breached_scenarios": breached_scenarios["scenario"].tolist(),
    }


limits = {
    "Spot down 5, vol up 5": 25_000,
    "Crash: spot down 15, vol up 20, skew steepens": 75_000,
    "Vol crush": 20_000,
    "Rates up 100bp": 10_000,
}

limit_results = evaluate_scenario_limits(stress_df, limits)
print(limit_results)

ks = kill_switch_diagnostics(
    current_drawdown=0.06,
    margin_utilization=0.68,
    scenario_limit_results=limit_results,
    unexplained_pnl_ratio=0.12,
)
print(ks)
```

## 9.12 Python Code: Jump Scenario Engine for Single-Stock Options

This example stresses a single-stock option book around an earnings-like event. It allows spot to jump and implied volatility to collapse after the event.

```python
@dataclass(frozen=True)
class EventScenario:
    name: str
    jump_return: float
    post_event_vol_shift: float
    time_passed: float = 1 / 365
    liquidity_spread_multiplier: float = 2.0


def stress_event_position(position: OptionPosition, event: EventScenario) -> dict[str, float | str]:
    base = position.option
    if event.jump_return <= -1.0:
        raise ValueError("jump_return must be greater than -100%")

    shocked = replace_option(
        base,
        spot=base.spot * (1.0 + event.jump_return),
        volatility=max(base.volatility + event.post_event_vol_shift, 0.01),
        tau=max(base.tau - event.time_passed, 1e-8),
    )

    base_price = bsm_price(base)
    shocked_price = bsm_price(shocked)
    scale = position.quantity * position.multiplier
    full_pnl = scale * (shocked_price - base_price)

    # Approximate pre-event delta hedge P&L if hedged at initial delta.
    initial_delta = bsm_greeks(base)["delta"]
    hedge_units = -scale * initial_delta
    hedge_pnl = hedge_units * (shocked.spot - base.spot)
    hedged_full_pnl = full_pnl + hedge_pnl

    liquidity_cost = abs(scale) * base_price * max(event.liquidity_spread_multiplier - 1.0, 0.0) * 0.005

    return {
        "event": event.name,
        "label": position.label,
        "underlying": position.underlying,
        "jump_return": event.jump_return,
        "base_price": base_price,
        "shocked_price": shocked_price,
        "unhedged_full_pnl": full_pnl - liquidity_cost,
        "hedge_pnl": hedge_pnl,
        "delta_hedged_full_pnl": hedged_full_pnl - liquidity_cost,
        "liquidity_cost": liquidity_cost,
        "base_delta": scale * initial_delta,
        "base_vega_1vol": scale * bsm_greeks(base)["vega"] / 100.0,
    }


def stress_event_portfolio(positions: list[OptionPosition], events: list[EventScenario]) -> pd.DataFrame:
    rows = []
    for event in events:
        for position in positions:
            rows.append(stress_event_position(position, event))
    return pd.DataFrame(rows)


single_name_book = [
    OptionPosition(
        option=BSMOption(50.0, 50.0, 10 / 365, 0.04, 0.00, 0.80, "call"),
        quantity=-50,
        multiplier=100,
        underlying="SINGLE_A",
        sector="Technology",
        label="Short pre-earnings ATM calls",
    ),
    OptionPosition(
        option=BSMOption(50.0, 45.0, 10 / 365, 0.04, 0.00, 0.90, "put"),
        quantity=-40,
        multiplier=100,
        underlying="SINGLE_A",
        sector="Technology",
        label="Short pre-earnings downside puts",
    ),
]

events = [
    EventScenario("Earnings up 15 vol crush", jump_return=0.15, post_event_vol_shift=-0.35),
    EventScenario("Earnings down 20 vol crush", jump_return=-0.20, post_event_vol_shift=-0.30),
    EventScenario("Earnings down 35 panic", jump_return=-0.35, post_event_vol_shift=0.05, liquidity_spread_multiplier=4.0),
]

event_results = stress_event_portfolio(single_name_book, events)
print(event_results.round(2))
print(event_results.groupby("event")[["unhedged_full_pnl", "delta_hedged_full_pnl", "liquidity_cost"]].sum().round(2))
```

Expected interpretation:

- Delta hedging before an event does not remove jump risk.
- Short event-volatility positions can benefit from volatility crush in small moves but lose severely in large jumps.
- Liquidity cost and spread widening should be part of event stress.
- A symmetric implied move assumption may understate asymmetric downside risk.

## 9.13 Python Code: Stress Dashboard Summary

A simple dashboard summarizes exposure, stress P&L, approximation error, and limit status.

```python
def build_stress_dashboard(stress_results: pd.DataFrame, limit_results: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Build summary tables for risk review."""
    scenario_summary = stress_results.groupby("scenario").agg(
        full_pnl=("full_pnl", "sum"),
        taylor_core_pnl=("taylor_core_pnl", "sum"),
        taylor_vanna_volga_pnl=("taylor_vanna_volga_pnl", "sum"),
        liquidity_cost=("liquidity_cost", "sum"),
    )
    scenario_summary["core_approx_error"] = scenario_summary["full_pnl"] - scenario_summary["taylor_core_pnl"]
    scenario_summary["vv_approx_error"] = scenario_summary["full_pnl"] - scenario_summary["taylor_vanna_volga_pnl"]
    scenario_summary["relative_core_error"] = (
        scenario_summary["core_approx_error"].abs() / (scenario_summary["full_pnl"].abs() + 1e-8)
    )

    by_label = stress_results.groupby(["scenario", "label"])["full_pnl"].sum().reset_index()
    worst_positions = by_label.sort_values("full_pnl").groupby("scenario").head(3)

    by_sector = stress_results.groupby(["scenario", "sector"])["full_pnl"].sum().reset_index()

    return {
        "scenario_summary": scenario_summary.reset_index(),
        "worst_positions": worst_positions,
        "sector_summary": by_sector,
        "limit_results": limit_results,
    }


dashboard = build_stress_dashboard(stress_df, limit_results)
for name, table in dashboard.items():
    print(f"\n{name}")
    print(table.round(4))
```

A production dashboard should include:

- current Greeks;
- bucketed Greeks;
- stress P&L by scenario;
- full repricing versus approximation error;
- margin usage and stress margin;
- liquidity and days-to-exit;
- top loss contributors;
- breached limits;
- required actions and escalation status.

## 9.14 Risk-Management Checklist

| Area | Control Question |
|---|---|
| Current Greeks | Are delta, gamma, theta, vega, vanna, volga, skew, and term exposures within limits? |
| Bucketed Greeks | Are exposures concentrated by underlying, sector, maturity, strike, event, or liquidity tier? |
| Scenario loss | Are full-repricing losses within scenario limits? |
| Approximation error | Are Taylor approximations reliable for reported scenarios? |
| Drawdown | Is current drawdown within the allowed range? |
| Margin | Is normal and stress margin within liquidity capacity? |
| Liquidity | Can the book be reduced within the required exit horizon? |
| Event risk | Are earnings, dividends, macro events, and corporate actions controlled? |
| Borrow | Are short hedges feasible and borrow costs updated? |
| Assignment | Are short American options near ex-dividend or expiry flagged? |
| Model risk | Are pricing models, surface marks, and Greeks reconciled? |
| Residual P&L | Is unexplained P&L within tolerance? |
| Crowding | Are crowded exposures and dealer-flow risks monitored? |
| Kill switches | Are triggers and actions pre-defined and auditable? |

## 9.15 Production Requirements for Stress Testing

A production stress-testing system should include:

1. **Point-in-time data:** option chains, underlying prices, rates, dividends, borrow, corporate actions, and earnings dates.
2. **Model versioning:** pricing model, surface model, Greek engine, scenario generator, and margin model.
3. **Scenario library:** historical, hypothetical, regulatory, strategy-specific, and event-specific scenarios.
4. **Full repricing engine:** reprice all instruments under shocked states.
5. **Greek approximation engine:** explain local P&L and identify approximation error.
6. **Liquidity model:** stress spreads, impact, and days-to-exit.
7. **Margin model:** normal and stressed margin calculations.
8. **Limit engine:** evaluate Greek, scenario, liquidity, margin, concentration, and drawdown limits.
9. **Attribution engine:** identify top contributors by underlying, sector, strategy, and risk factor.
10. **Escalation workflow:** alerts, approvals, kill-switch actions, and audit trail.
11. **Backtesting of stress forecasts:** compare predicted stress sensitivity to realized crisis P&L when possible.
12. **Exception handling:** missing prices, bad quotes, stale data, model failures, and corporate-action breaks.

## 9.16 Common Risk-Management Errors

| Error | Why It Is Dangerous | Better Practice |
|---|---|---|
| Relying only on current Greeks | Greeks change after shocks | Use full repricing and projected Greeks |
| Stressing spot only | Options also respond to vol, skew, liquidity, and margin | Use multi-factor scenarios |
| Ignoring liquidity costs | Theoretical exits may be impossible | Stress spreads and market impact |
| Ignoring margin expansion | Losses and margin calls occur together | Model stress margin and available liquidity |
| Treating vega as one number | Skew and term shifts can dominate | Bucket vega and stress surface shape |
| Ignoring vanna and volga | Vega neutrality can fail after shocks | Add higher-order limits |
| Ignoring assignment | Unexpected stock positions can appear | Flag short American options near exercise triggers |
| Using Taylor approximation for crashes | Local approximation fails | Use full repricing for large moves |
| Ignoring borrow | Hedge may be impossible | Include borrow rates and locate availability |
| Evaluating short vol by Sharpe only | Rare crashes dominate true risk | Use expected shortfall and stress losses |
| No kill switch | Crisis response becomes discretionary | Predefine triggers and actions |
| No residual monitoring | Model failures remain hidden | Track unexplained P&L and escalate |

## 9.17 Summary of Part 9

Part 9 developed a risk-management and stress-testing framework for options portfolios.

Key points:

1. Options risk management must combine local Greeks, full repricing, stress scenarios, liquidity controls, margin controls, and failure-mode analysis.
2. Greek limits should be applied at total portfolio, strategy, underlying, sector, maturity, moneyness, event, and liquidity-bucket levels.
3. Drawdown limits, margin limits, liquidity limits, concentration limits, scenario limits, and kill-switch rules are essential for institutional control.
4. Stress testing must include spot shocks, volatility shocks, skew shocks, rate shocks, dividend shocks, correlation shocks, liquidity shocks, borrow shocks, and jump shocks.
5. Large moves require full repricing because local Greeks are evaluated only at the current state.
6. Approximation error between Taylor P&L and full repricing P&L should be measured and reported.
7. Gap risk cannot be eliminated by continuous-hedging assumptions because real hedging is discrete.
8. Vol-of-vol risk can create losses in apparently vega-neutral books through volga and vanna exposure.
9. Correlation breakdown can invalidate diversification and damage dispersion trades.
10. Crowded trade unwinds can amplify losses through one-sided hedging and liquidity deterioration.
11. Early assignment and exercise risk matter for American options, especially around dividends and expiration.
12. Model risk arises from wrong pricing assumptions, stale data, surface errors, dividend mistakes, borrow omissions, and inappropriate Greek conventions.
13. Short-volatility strategies can appear stable because they earn frequent small gains while hiding rare but severe losses.
14. Scenario tables help connect strategy families to expected stress behavior and failure modes.
15. A production stress-testing system should include full repricing, Greek attribution, scenario limits, margin stress, liquidity stress, event stress, exception handling, and governance.

The next installment will cover Part 10: Institutional Research Pipeline and Backtesting Framework, including required data, point-in-time controls, survivorship and look-ahead bias, option-chain cleaning, universe selection, liquidity filters, execution assumptions, validation, performance metrics, backtesting pseudocode, and production readiness.
