# Institutional Options Greeks, Systematic Strategy, and Regime-Aware Portfolio Construction Curriculum

## Completed Installment

This installment contains:

- Part 5: Systematic Alpha Generation Using Greeks.

The document is educational and research-oriented. It is not personalized investment advice, a live trading recommendation, or a claim that any option strategy produces guaranteed alpha.

---

# Part 5: Systematic Alpha Generation Using Greeks

**Level:** Expert

## 5.1 Purpose of Part 5

Parts 1 through 4 developed option pricing, core Greeks, higher-order Greeks, hedging mechanics, and volatility-surface structure. Part 5 turns those tools into a research framework for systematic options strategies.

The institutional objective is not to say that a Greek itself is alpha. Greeks are **state variables** describing exposures. Alpha research asks whether certain exposures are compensated after costs, under which regimes, with which implementation constraints, and with what tail risks.

A systematic options strategy should therefore distinguish among:

- the **risk exposure** being held, such as gamma, vega, skew, jump, correlation, or liquidity exposure;
- the **risk premium** potentially earned for supplying or demanding that exposure;
- the **forecast signal** used to estimate expected return or expected hedging utility;
- the **portfolio construction rule** used to size positions;
- the **risk-management framework** used to survive adverse states;
- the **implementation layer** used to execute, hedge, and monitor the strategy.

The central principle is:

$$
\text{Greek-aware alpha research} = \text{exposure measurement} + \text{risk-premium hypothesis} + \text{regime conditioning} + \text{cost-aware implementation}.
$$

No strategy family in this part should be interpreted as a live trade recommendation. Each strategy is discussed as a research object with assumptions, risks, liquidity constraints, and failure modes.

## 5.2 Greeks as State Variables in Systematic Options Research

A systematic options research process can treat each option or strategy sleeve as an observation with a state vector. For option $i$ at time $t$, define:

$$
\mathbf{x}_{i,t}=\begin{bmatrix}
\Delta_{i,t} \\
\Gamma_{i,t} \\
\Theta_{i,t} \\
\nu_{i,t} \\
\rho_{i,t} \\
\text{Vanna}_{i,t} \\
\text{Volga}_{i,t} \\
\text{SkewExposure}_{i,t} \\
\text{TermVega}_{i,t} \\
\text{Liquidity}_{i,t} \\
\text{EventRisk}_{i,t}
\end{bmatrix}.
$$

Variables:

- $\Delta_{i,t}$ is directional exposure;
- $\Gamma_{i,t}$ is spot convexity;
- $\Theta_{i,t}$ is time carry using the stated theta convention;
- $\nu_{i,t}$ is implied-volatility exposure;
- $\rho_{i,t}$ is rate sensitivity;
- $\text{Vanna}_{i,t}$ is spot-volatility interaction;
- $\text{Volga}_{i,t}$ is volatility convexity;
- $\text{SkewExposure}_{i,t}$ measures sensitivity to skew slope or downside-volatility repricing;
- $\text{TermVega}_{i,t}$ measures exposure to maturity-specific volatility shocks;
- $\text{Liquidity}_{i,t}$ contains spread, open interest, volume, and depth features;
- $\text{EventRisk}_{i,t}$ includes earnings, macro-event, dividend, corporate-action, or jump indicators.

A strategy-level state vector aggregates options and hedges:

$$
\mathbf{x}_{s,t}=\sum_{i\in\mathcal{S}_s} w_{i,t}\mathbf{x}_{i,t},
$$

where:

- $s$ is the strategy sleeve;
- $\mathcal{S}_s$ is the set of positions in sleeve $s$;
- $w_{i,t}$ is the signed position size, including contract quantity and multiplier.

The research problem is to estimate whether a function of this state vector predicts future risk-adjusted returns, hedging benefits, or portfolio utility:

$$
\mathbb{E}_t[R_{s,t+1}] = f(\mathbf{x}_{s,t},\mathbf{z}_t,\mathbf{c}_{s,t}),
$$

where:

- $R_{s,t+1}$ is the future strategy return or P&L normalized by capital, margin, premium, or risk;
- $\mathbf{z}_t$ contains regime variables such as realized volatility, implied volatility, credit spreads, PMI, liquidity, and trend;
- $\mathbf{c}_{s,t}$ contains costs, margin, liquidity, borrow, and implementation constraints.

## 5.3 Alpha, Carry, and Risk Premia: Required Distinctions

Options strategies often mix several return sources. A rigorous process separates them.

| Return Source | Definition | Example Exposure | Main Risk |
|---|---|---|---|
| Expected return | Statistical or model-implied expected P&L after costs | Strategy forecast | Estimation error and overfitting |
| Carry | P&L expected if market state remains broadly unchanged | Short theta-positive option | Regime break and jump losses |
| Convexity | Nonlinear payoff from large moves | Long gamma or long wings | Persistent negative carry |
| Volatility risk premium | Compensation for selling implied variance above expected realized variance | Short straddle or variance exposure | Crash and volatility spike |
| Skew risk premium | Compensation for selling expensive downside or upside tail volatility | Short put skew, risk reversal | Tail event and skew steepening |
| Correlation risk premium | Compensation for selling index correlation versus single-name volatility | Dispersion | Correlation spike |
| Jump premium | Compensation for bearing gap risk | Short event volatility | Discontinuous loss |
| Liquidity premium | Compensation for providing liquidity in less liquid options | Wide-spread single-name options | Inability to exit during stress |
| Financing premium | Return linked to funding, margin, collateral, or borrow | Synthetic financing trades | Funding shock and borrow squeeze |
| Model error premium | Apparent edge from model disagreement | Mispriced surface by model | False alpha from wrong model |

The phrase “alpha” should be used conservatively. A strategy may have positive average historical returns because it sells crash insurance. That is not necessarily alpha; it may be compensation for bearing a systematic risk that realizes infrequently.

## 5.4 General Expected P&L Framework

For option position $i$, a local expected P&L model over horizon $h$ can be written as:

$$
\mathbb{E}_t[\Delta V_{i,t+h}]
\approx
\Delta_{i,t}\mathbb{E}_t[\Delta S]
+\frac{1}{2}\Gamma_{i,t}\mathbb{E}_t[(\Delta S)^2]
+\Theta_{i,t}h
+\nu_{i,t}\mathbb{E}_t[\Delta\sigma]
+\text{Vanna}_{i,t}\mathbb{E}_t[\Delta S\Delta\sigma]
+\frac{1}{2}\text{Volga}_{i,t}\mathbb{E}_t[(\Delta\sigma)^2]
-\mathbb{E}_t[\text{Costs}]
-\mathbb{E}_t[\text{Financing}].
$$

Variables:

- $h$ is the forecast horizon in years;
- $\Delta S$ is the underlying price change;
- $\Delta\sigma$ is the implied-volatility change;
- $\mathbb{E}_t[(\Delta S)^2]$ is linked to expected realized variance;
- $\mathbb{E}_t[\Delta S\Delta\sigma]$ captures spot-volatility co-movement;
- $\mathbb{E}_t[(\Delta\sigma)^2]$ captures volatility-of-volatility;
- costs include bid-ask spreads, commissions, slippage, market impact, borrow, and operational costs.

For a delta-hedged strategy with small residual delta, the directional term is reduced:

$$
\mathbb{E}_t[\Delta \Pi_{i,t+h}]
\approx
\frac{1}{2}\Gamma_{i,t}S_t^2\mathbb{E}_t[(r^S)^2]
+\Theta_{i,t}h
+\nu_{i,t}\mathbb{E}_t[\Delta\sigma]
+\text{surface and higher-order terms}
-\mathbb{E}_t[\text{Costs}],
$$

where $r^S=\Delta S/S_t$ is the underlying return.

This equation is the bridge between Greeks and systematic alpha research. It shows that a strategy's expected P&L depends on forecasts of realized variance, implied-volatility change, surface movement, costs, and hedge performance.

## 5.5 Alpha Signals from the Volatility Risk Premium

## 5.5.1 Definition

A basic variance risk premium signal compares implied variance with a forecast of realized variance:

$$
\text{VRP}_{i,t}=\sigma_{\text{imp},i,t}^{2}-\widehat{\sigma}_{\text{real},i,t\rightarrow t+h}^{2}.
$$

Variables:

- $\sigma_{\text{imp},i,t}^{2}$ is implied variance for option or maturity $i$;
- $\widehat{\sigma}_{\text{real},i,t\rightarrow t+h}^{2}$ is the forecast of future realized variance over horizon $h$;
- both quantities must use consistent annualization and horizon conventions.

If $\text{VRP}_{i,t}>0$, implied variance exceeds forecast realized variance. A short-volatility strategy may appear attractive, but only after accounting for jump risk, skew, transaction costs, margin, and drawdown exposure.

## 5.5.2 Realized-Implied Spread

A simpler signal uses realized volatility instead of forecast realized volatility:

$$
\text{IVRVSpread}_{i,t}=\sigma_{\text{imp},i,t}-\sigma_{\text{real},i,t}^{(L)},
$$

where $\sigma_{\text{real},i,t}^{(L)}$ is realized volatility estimated over lookback window $L$.

This signal is easy to compute but can be naive. Realized volatility is backward-looking and may be low before a volatility regime shift. A production signal should test multiple lookbacks, robust estimators, event filters, and regime-conditioned forecasts.

## 5.5.3 Delta-Hedged Expected Carry Approximation

For a short delta-hedged option, expected gamma-theta carry can be approximated as:

$$
\mathbb{E}_t[\Delta \Pi^{\text{short}}]
\approx
-\frac{1}{2}\Gamma_t S_t^2\widehat{\sigma}_{\text{real}}^2 h
-\Theta_t h
-\mathbb{E}_t[\text{Costs}],
$$

where $\Gamma_t$ and $\Theta_t$ refer to the long option. Since a short option has negative gamma and positive theta, this expression is written from the perspective of shorting the long-option exposure.

A short-volatility position is attractive only if:

$$
-\Theta_t h
>
\frac{1}{2}\Gamma_t S_t^2\widehat{\sigma}_{\text{real}}^2 h
+\mathbb{E}_t[\text{Costs}]
+\text{Required Tail Compensation}.
$$

The final term is essential. Without it, the model may systematically underestimate rare but severe crash losses.

## 5.6 Alpha Signals from Skew Premium

## 5.6.1 Skew Richness Signal

Let downside skew for maturity $\tau$ be:

$$
\text{PutSkew}_{t,\tau}=\sigma_{25\Delta\text{ put},t,\tau}-\sigma_{\text{ATM},t,\tau}.
$$

A standardized skew richness signal is:

$$
Z^{\text{skew}}_{t,\tau}=\frac{\text{PutSkew}_{t,\tau}-\mu^{(L)}_{\text{PutSkew},t,\tau}}{s^{(L)}_{\text{PutSkew},t,\tau}},
$$

where:

- $\mu^{(L)}$ is a rolling historical mean over lookback $L$;
- $s^{(L)}$ is a rolling historical standard deviation;
- all values should be computed point-in-time.

A high positive $Z^{\text{skew}}$ means downside puts are rich relative to their own history. A researcher may test whether selling downside skew, buying call skew, or structuring collars has positive expected return after tail-risk adjustment. This is not automatic alpha because skew often becomes rich before stress.

## 5.6.2 Skew Risk Premium Versus Crash Risk

The expected P&L from shorting skew can be decomposed as:

$$
\mathbb{E}[R^{\text{short skew}}]
=\text{SkewCarry}-\text{ExpectedCrashLoss}-\text{TransactionCosts}-\text{MarginCost}-\text{ModelError}.
$$

Skew carry is the apparent premium earned if skew normalizes or decays. Expected crash loss is hard to estimate because it depends on rare events, correlation spikes, liquidity gaps, and market depth.

A robust skew strategy should therefore include:

- crash scenarios;
- skew steepening shocks;
- liquidity stress;
- margin stress;
- stop-loss or de-risking rules;
- regime filters;
- concentration limits by underlying and sector.

## 5.7 Alpha Signals from Term-Structure Carry

## 5.7.1 Term Slope Signal

An at-the-money volatility term slope can be defined as:

$$
\text{TermSlope}_{t}=\sigma_{\text{ATM},t}(\tau_2)-\sigma_{\text{ATM},t}(\tau_1),\quad \tau_2>\tau_1.
$$

A variance-based slope is often more stable:

$$
\text{VarianceSlope}_{t}=\sigma_{\text{ATM},t}^{2}(\tau_2)\tau_2-\sigma_{\text{ATM},t}^{2}(\tau_1)\tau_1.
$$

A forward-volatility signal is:

$$
\sigma_{fwd,t}(\tau_1,\tau_2)=
\sqrt{\frac{\sigma_{2,t}^{2}\tau_2-\sigma_{1,t}^{2}\tau_1}{\tau_2-\tau_1}}.
$$

The term structure can support calendar spreads, diagonal spreads, or volatility roll-down trades. The central research question is whether the term structure is too steep or too flat relative to expected future volatility and event risk.

## 5.7.2 Roll-Down Expected Return

For an option whose maturity declines from $\tau$ to $\tau-h$, a simplified roll-down signal is:

$$
\text{RollDown}_{t}=\sigma_{\text{imp},t}(k,\tau-h)-\sigma_{\text{imp},t}(k,\tau).
$$

If a short-volatility position is short a maturity expected to roll down to lower implied volatility, the roll-down may be favorable. But if the surface shifts upward, the realized P&L may be negative.

A calendar-spread expected return can be stylized as:

$$
\mathbb{E}_t[R^{\text{calendar}}]
= a_1\text{TermMispricing}_{t}+a_2\text{RollDown}_{t}+a_3\text{EventPremium}_{t}-a_4\text{VegaBasisRisk}_{t}-a_5\text{Costs}_{t},
$$

where $a_j$ are estimated or assigned weights. This equation is a research model, not a pricing identity.

## 5.8 Alpha Signals from Jump Premium

Jump premium is compensation for bearing discontinuous price moves that cannot be hedged continuously. It is especially relevant for earnings, macro announcements, biotech events, litigation decisions, central-bank decisions, and takeover risk.

A stylized event variance decomposition is:

$$
\sigma_{\text{imp}}^2(\tau)\tau
=\sigma_{\text{diffusive}}^2\tau+\sum_{e\in\mathcal{E}(t,T)}\omega_e^2,
$$

where $\omega_e^2$ is implied event variance for event $e$.

An event-volatility richness signal can be written as:

$$
\text{EventRichness}_{i,t}
=\omega_{i,t}^{\text{imp}}-\widehat{\omega}_{i,t}^{\text{real}},
$$

where:

- $\omega_{i,t}^{\text{imp}}$ is implied event move or event volatility;
- $\widehat{\omega}_{i,t}^{\text{real}}$ is a forecast of realized event move based on historical earnings moves, options-implied distributions, analyst uncertainty, or other features.

Shorting event volatility can earn premium when implied event moves exceed realized event moves. The failure mode is a large gap that overwhelms collected premium. Buying event volatility can benefit from underpriced gaps but may lose from volatility crush if the move is insufficient.

## 5.9 Alpha Signals from Convexity Demand

Convexity demand refers to market willingness to pay for nonlinear payoff exposure. It can be driven by:

- institutional demand for crash protection;
- structured-product issuance;
- dealer hedging pressure;
- volatility-control strategies;
- target-volatility funds;
- pension hedging;
- retail call buying;
- event-driven speculation;
- regulatory capital or risk constraints.

A convexity richness signal can compare option convexity cost to expected convexity benefit:

$$
\text{ConvexityScore}_{i,t}=rac{\Gamma_{i,t}S_{i,t}^{2}}{|\Theta_{i,t}|+\epsilon},
$$

where $\epsilon>0$ prevents division by zero. This score measures gamma exposure per unit of theta cost. It is a structural descriptor, not a standalone buy signal.

A more complete long-convexity attractiveness measure is:

$$
\text{LongGammaAttractiveness}_{i,t}
= b_1\widehat{\sigma}_{\text{real},i,t\rightarrow t+h}^{2}
-b_2\sigma_{\text{imp},i,t}^{2}
+b_3\text{JumpRiskForecast}_{i,t}
-b_4\text{SpreadCost}_{i,t}
-b_5\text{ThetaDrag}_{i,t},
$$

where $b_j$ are model weights. The signal is positive when expected realized variance and jump risk appear high relative to implied variance and costs.

## 5.10 Alpha Signals from Correlation Risk Premium

Correlation risk premium is central to dispersion trading. Index variance depends on single-name variances and correlations:

$$
\sigma_I^2\approx \sum_{i=1}^{N}w_i^2\sigma_i^2+2\sum_{i<j}w_iw_j\rho_{ij}\sigma_i\sigma_j.
$$

A dispersion trade typically sells index volatility and buys single-name volatility, or the reverse. The classic short-correlation exposure is:

- short index options or variance;
- long weighted basket of single-name options or variance.

The trade profits if implied index correlation is rich relative to realized correlation and single-name realized volatility.

A simplified implied correlation estimate is:

$$
\rho_{\text{imp}}
\approx
\frac{\sigma_I^2-\sum_i w_i^2\sigma_i^2}{2\sum_{i<j}w_iw_j\sigma_i\sigma_j}.
$$

Variables:

- $\sigma_I^2$ is index implied variance;
- $\sigma_i^2$ is single-name implied variance;
- $w_i$ are index weights.

A correlation risk premium signal is:

$$
\text{CorrRP}_t=\rho_{\text{imp},t}-\widehat{\rho}_{\text{real},t\rightarrow t+h}.
$$

If implied correlation exceeds forecast realized correlation, short index volatility versus long single-name volatility may appear attractive. The failure mode is correlation spike during market stress, when index options can lose more than single-name hedges gain.

## 5.11 Alpha Signals from Liquidity Premium

Options with wider spreads or lower liquidity may offer apparent compensation, but liquidity premium is difficult to harvest systematically because entry and exit costs are high.

A liquidity-adjusted expected return can be written as:

$$
\mathbb{E}_t[R^{\text{net}}_{i,t+h}]
=\mathbb{E}_t[R^{\text{gross}}_{i,t+h}]
-\text{HalfSpread}_{i,t}^{\text{entry}}
-\mathbb{E}_t[\text{ExitCost}_{i,t+h}]
-\mathbb{E}_t[\text{MarketImpact}_{i,t}].
$$

A liquidity score might combine:

$$
\text{LiquidityScore}_{i,t}
= c_1\log(1+\text{OpenInterest}_{i,t})
+c_2\log(1+\text{Volume}_{i,t})
-c_3\text{BidAskPct}_{i,t}
-c_4\text{QuoteAge}_{i,t}
-c_5\text{MarketImpactProxy}_{i,t}.
$$

This score should be used as a constraint and cost adjustment, not merely as a return predictor.

## 5.12 Strategy Families and Greek Profiles

This section classifies major options strategy families by payoff profile, Greek exposure, alpha source, regime preference, and failure mode.

## 5.12.1 Long Gamma Strategies

Long gamma strategies buy convexity. Examples include long straddles, long strangles, long puts, long calls, and dynamically hedged long options.

| Dimension | Description |
|---|---|
| Payoff profile | Benefits from sufficiently large moves; can be directionally neutral if constructed as straddle/strangle |
| Greek profile | Positive gamma, positive vega, negative theta, often material vanna/volga |
| Alpha source | Realized volatility above implied volatility; underpriced jump risk; crisis convexity |
| Regime preference | Rising realized volatility, transition regimes, event uncertainty, crash convexity regimes |
| Carry profile | Negative theta and premium decay |
| Liquidity concern | Frequent hedging and option spread costs |
| Margin profile | Premium paid; lower gap liability than short options but capital still tied up |
| Failure mode | Realized moves too small, implied volatility falls, theta decay persists, overpaying for convexity |

A long-gamma expected P&L approximation is:

$$
\mathbb{E}[\Delta \Pi]
\approx
\frac{1}{2}\Gamma S^2\widehat{\sigma}_{\text{real}}^2h
+\Theta h
+\nu\mathbb{E}[\Delta\sigma]
-\text{Costs}.
$$

Since $\Theta<0$, the strategy needs realized movement, volatility repricing, or jump payoff to overcome carry cost.

## 5.12.2 Short Gamma Strategies

Short gamma strategies sell convexity. Examples include short straddles, short strangles, short puts, short calls, iron condors, and some covered-call overlays.

| Dimension | Description |
|---|---|
| Payoff profile | Earns premium if underlying remains within range; losses grow with large moves |
| Greek profile | Negative gamma, negative vega, positive theta |
| Alpha source | Volatility risk premium, theta carry, range-bound realized market |
| Regime preference | Stable low-to-moderate realized volatility, declining implied volatility, strong liquidity |
| Carry profile | Positive theta but crash-sensitive |
| Liquidity concern | Exit costs rise in stress; hedging trades are adverse |
| Margin profile | Margin can rise sharply during stress |
| Failure mode | Gap move, volatility spike, skew steepening, liquidity evaporation, margin spiral |

A short-gamma strategy should never be evaluated only by average return or Sharpe ratio. It requires drawdown, expected shortfall, crash stress, margin stress, and liquidity stress.

## 5.12.3 Long Vega Strategies

Long vega strategies benefit from increases in implied volatility. They can be implemented through long options, calendars, long variance exposure, or volatility products.

| Dimension | Description |
|---|---|
| Payoff profile | Benefits from implied-volatility increases, sometimes independent of immediate spot move |
| Greek profile | Positive vega; gamma and theta depend on structure |
| Alpha source | Underpriced volatility, expected vol repricing, regime transition, event uncertainty |
| Regime preference | Rising-volatility transition, pre-event repricing, liquidity stress |
| Carry profile | Often negative carry if implemented through long options |
| Liquidity concern | Long-dated and wing options may be expensive to trade |
| Margin profile | Usually premium paid for long options; product-specific for futures/swaps |
| Failure mode | Volatility fails to rise, term structure rolls against position, volatility crush |

## 5.12.4 Short Vega Strategies

Short vega strategies benefit from falling or stable implied volatility. They include short options, short calendars, short variance exposure, and certain yield-enhancement overlays.

| Dimension | Description |
|---|---|
| Payoff profile | Earns premium or carry when implied volatility declines or remains high relative to realized volatility |
| Greek profile | Negative vega; often negative gamma and positive theta |
| Alpha source | Volatility risk premium and volatility mean reversion |
| Regime preference | Post-shock normalization, stable carry, high implied versus expected realized volatility |
| Carry profile | Positive carry but short stress convexity |
| Liquidity concern | Losses occur when liquidity worsens |
| Margin profile | Potentially high and procyclical |
| Failure mode | Volatility spike, crash, skew steepening, forced deleveraging |

## 5.12.5 Long Skew Strategies

Long skew strategies buy relatively expensive or cheap tail asymmetry depending on implementation. A typical long-downside-skew position may own puts or put spreads versus calls.

| Dimension | Description |
|---|---|
| Payoff profile | Benefits from downside tail repricing or crash movement |
| Greek profile | Negative delta or hedged delta, positive downside convexity, often positive vega and vanna |
| Alpha source | Underpriced downside risk, hedging utility, crash convexity |
| Regime preference | Rising macro stress, credit deterioration, liquidity tightening, risk-off transition |
| Carry profile | Usually negative carry |
| Liquidity concern | Downside options may be expensive and crowded |
| Margin profile | Premium paid if long options; spreads reduce premium but cap payoff |
| Failure mode | Persistent calm market, skew decay, expensive protection, poor timing |

## 5.12.6 Short Skew Strategies

Short skew strategies sell relatively rich downside or upside skew. For equity indices, this often means selling downside puts or put spreads, possibly hedged with other options.

| Dimension | Description |
|---|---|
| Payoff profile | Earns skew premium if tail event does not occur and skew normalizes |
| Greek profile | Short downside convexity; negative vega to downside skew; often negative gamma |
| Alpha source | Skew risk premium and protection-demand imbalance |
| Regime preference | Stable carry, improving liquidity, declining stress |
| Carry profile | Positive carry if skew remains rich and realized tails are muted |
| Liquidity concern | Exit costs can explode during selloffs |
| Margin profile | Tail-sensitive and procyclical |
| Failure mode | Crash, skew steepening, gap down, liquidity vacuum |

## 5.12.7 Covered Calls

A covered call combines long underlying exposure with short call exposure.

| Dimension | Description |
|---|---|
| Payoff profile | Equity upside is capped beyond strike; premium cushions modest downside |
| Greek profile | Positive net delta, negative call gamma, positive theta from short call, negative vega |
| Alpha source | Call overwriting premium, volatility risk premium, behavioral demand for upside calls |
| Regime preference | Range-bound or modestly rising markets; implied volatility rich versus realized upside movement |
| Carry profile | Positive option premium carry |
| Liquidity concern | Rolling costs and assignment risk |
| Margin profile | Often efficient if underlying is held; depends on account and regulation |
| Failure mode | Strong upside rally underperforms; downside loss remains mostly equity-like |

Covered calls are not pure income. They exchange uncertain upside for premium and retain substantial downside exposure.

## 5.12.8 Protective Puts

A protective put combines long underlying exposure with a long put.

| Dimension | Description |
|---|---|
| Payoff profile | Downside floor below strike, upside participation retained |
| Greek profile | Positive equity delta offset by negative put delta, positive gamma, positive vega, negative theta |
| Alpha source | Hedging utility; underpriced downside convexity if protection is cheap |
| Regime preference | Rising downside risk, risk-off transition, high uncertainty |
| Carry profile | Negative carry from put premium |
| Liquidity concern | Put skew can be expensive and spreads widen in stress |
| Margin profile | Premium paid; hedge may reduce portfolio risk capital |
| Failure mode | Persistent premium bleed if drawdown does not occur |

## 5.12.9 Collars

A collar typically combines long underlying, long put, and short call.

| Dimension | Description |
|---|---|
| Payoff profile | Downside protected below put strike; upside capped above call strike |
| Greek profile | Reduced delta, positive put gamma, negative call gamma, mixed vega, lower theta cost than protective put |
| Alpha source | Hedging efficiency; monetizing call skew to finance put skew |
| Regime preference | Investors seeking drawdown control with limited upside expectations |
| Carry profile | Can be low-cost or zero-cost depending on strikes and skew |
| Liquidity concern | Two option legs increase execution complexity |
| Margin profile | Usually defined-risk if structured properly |
| Failure mode | Underperformance in strong rallies; protection gap if put strike too low |

## 5.12.10 Straddles and Strangles

A straddle buys or sells a call and put at the same strike. A strangle uses different strikes.

| Strategy | Greek Profile | Alpha Hypothesis | Main Failure Mode |
|---|---|---|---|
| Long straddle | Long gamma, long vega, short theta | Realized/event move exceeds implied | Vol crush and insufficient move |
| Short straddle | Short gamma, short vega, long theta | Implied exceeds realized | Large move or vol spike |
| Long strangle | Long wing convexity, lower premium than straddle | Large tail move | Needs larger move to profit |
| Short strangle | Short tail risk, positive theta | Range-bound market | Gap loss and margin expansion |

## 5.12.11 Butterflies

A long call butterfly can be constructed as:

$$
+1C(K_1)-2C(K_2)+1C(K_3),\quad K_1<K_2<K_3.
$$

It profits if the underlying finishes near the middle strike. A butterfly has localized exposure to the terminal distribution.

| Dimension | Description |
|---|---|
| Payoff profile | Limited risk and limited reward; peak near body strike |
| Greek profile | Local gamma and theta depend on spot relative to body and wings |
| Alpha source | Distributional view, pinning, overpriced wings or body |
| Regime preference | Range-bound markets, event distribution mispricing |
| Carry profile | Structure-dependent |
| Liquidity concern | Multi-leg execution and strike liquidity |
| Margin profile | Defined risk if constructed as debit butterfly |
| Failure mode | Underlying moves away from body; execution costs dominate |

## 5.12.12 Calendars and Diagonals

A calendar spread trades options with different maturities. A diagonal spread trades different strikes and maturities.

| Dimension | Description |
|---|---|
| Payoff profile | Exposure to term structure and path around short-leg expiry |
| Greek profile | Often long back-month vega and short front-month gamma/theta, depending on structure |
| Alpha source | Term-structure mispricing, event premium, roll-down |
| Regime preference | Stable spot with favorable term-structure dynamics |
| Carry profile | Depends on front versus back implied volatility and decay |
| Liquidity concern | Maturity basis and multi-leg execution |
| Margin profile | Spread margin; may change if legs move differently |
| Failure mode | Large spot move, front vol spike, term structure shifts adversely |

## 5.12.13 Risk Reversals

An equity risk reversal often buys a call and sells a put or buys a put and sells a call. The structure expresses skew and directional views.

| Dimension | Description |
|---|---|
| Payoff profile | Asymmetric directional exposure financed by opposite tail sale |
| Greek profile | Delta, skew, vanna, and tail exposure are central |
| Alpha source | Skew mispricing, directional view, financing asymmetry |
| Regime preference | Depends on direction and skew view |
| Carry profile | Can be premium-neutral but not risk-neutral |
| Liquidity concern | Wing liquidity and skew execution |
| Margin profile | Short wing can create substantial margin |
| Failure mode | Sold tail realizes; skew moves against structure |

## 5.12.14 Dispersion Trades

A dispersion trade compares index volatility to single-name volatility.

| Dimension | Description |
|---|---|
| Payoff profile | Exposed to correlation and relative volatility |
| Greek profile | Short or long index vega/gamma versus opposite single-name basket exposure |
| Alpha source | Correlation risk premium, index protection demand, single-name richness/cheapness |
| Regime preference | Stable or declining correlation for short-correlation dispersion |
| Carry profile | Often positive when index implied correlation is rich |
| Liquidity concern | Many legs, single-name liquidity, rebalancing complexity |
| Margin profile | Portfolio margin may help but stress margin can rise |
| Failure mode | Correlation spike, single-name event losses, index crash |

## 5.12.15 Variance Swaps and Variance Replication

A variance swap pays realized variance minus a fixed variance strike:

$$
\text{Payoff}=N_{var}\left(\sigma_{\text{real}}^2-K_{var}\right),
$$

where:

- $N_{var}$ is variance notional;
- $\sigma_{\text{real}}^2$ is realized variance over the contract period;
- $K_{var}$ is the variance strike.

Variance exposure can be approximated by a strip of options across strikes. In practice, listed option replication faces truncation, liquidity, and discrete strike issues.

| Dimension | Description |
|---|---|
| Payoff profile | Direct exposure to realized variance versus variance strike |
| Greek profile | Strong exposure to volatility and convexity; path-dependent realized variance |
| Alpha source | Variance risk premium |
| Regime preference | Depends on long or short variance position |
| Carry profile | Short variance often positive carry but crash-sensitive |
| Liquidity concern | OTC terms or option strip liquidity |
| Margin profile | Potentially significant under stress |
| Failure mode | Volatility explosion and jump risk for short variance |

## 5.12.16 Corridor Variance

Corridor variance counts realized variance only when the underlying remains within a specified corridor:

$$
\text{CorridorVariance}=rac{A}{n}\sum_{j=1}^{n}r_j^2\mathbf{1}\{L<S_{t_j}<U\},
$$

where:

- $A$ is an annualization factor;
- $r_j$ is the return over observation interval $j$;
- $L$ and $U$ are lower and upper corridor barriers;
- $\mathbf{1}\{\cdot\}$ is an indicator function.

Corridor variance can isolate volatility in a specific price region. It is useful for advanced volatility research but can be complex to implement and hedge.

## 5.12.17 Conditional Option Overlays

A conditional overlay changes option exposure based on signals or regimes. For example:

$$
w_{s,t}=w_{s}^{\max}\cdot p_{\text{regime},t}\cdot \text{SignalStrength}_{s,t}\cdot \text{RiskScale}_{t},
$$

where:

- $w_{s,t}$ is allocation to strategy sleeve $s$;
- $w_s^{\max}$ is maximum sleeve weight;
- $p_{\text{regime},t}$ is probability of a favorable regime;
- $\text{SignalStrength}_{s,t}$ is a normalized alpha or carry signal;
- $\text{RiskScale}_t$ reduces exposure when volatility, liquidity, margin, or drawdown risk is elevated.

This framework avoids binary all-in/all-out timing and connects directly to Part 6.

## 5.13 Option Strategy Greek Exposure Matrix

A simplified strategy-to-Greek matrix is shown below. Actual signs can change with strikes, maturities, hedge rules, and market state.

| Strategy Family | Delta | Gamma | Theta | Vega | Vanna | Volga | Skew Exposure | Main Risk Premium |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Long call | + | + | - | + | mixed | mixed | upside | Direction + convexity |
| Long put | - | + | - | + | mixed | mixed | downside | Hedge/crash convexity |
| Short straddle | near 0 initially | - | + | - | mixed | -/mixed | ATM vol | Volatility risk premium |
| Long straddle | near 0 initially | + | - | + | mixed | +/mixed | ATM vol | Realized/event volatility |
| Covered call | + capped | - | + | - | mixed | mixed | upside short | Call premium |
| Protective put | + reduced | + | - | + | downside | mixed | downside long | Hedge utility |
| Collar | + bounded | mixed | mixed | mixed | mixed | mixed | long downside, short upside | Hedged carry |
| Calendar | path-dependent | mixed | mixed | term vega | mixed | mixed | tenor | Term premium |
| Risk reversal | directional | mixed | mixed | mixed | high | mixed | skew | Skew premium/directional |
| Dispersion | hedged | mixed | mixed | index vs single-name | mixed | mixed | correlation | Correlation premium |
| Short variance | near 0 if hedged | - | + | - | material | material | variance strip | Variance risk premium |
| Long wings | low initially | + in tails | - | + | high | high | tail long | Jump/tail convexity |

## 5.14 Ranking Individual Stock Options

Single-stock option ranking requires more than implied-versus-realized volatility. A robust ranking model must address liquidity, event risk, borrow, idiosyncratic jumps, factor exposure, and corporate actions.

## 5.14.1 Candidate Features

For stock $j$ and option $i$, define feature groups:

### Volatility Features

$$
\text{IVRV}_{i,t}=\sigma_{\text{imp},i,t}-\sigma_{\text{real},j,t}^{(L)}.
$$

$$
\text{VRP}_{i,t}=\sigma_{\text{imp},i,t}^{2}-\widehat{\sigma}_{\text{real},j,t\rightarrow t+h}^{2}.
$$

### Skew Features

$$
\text{PutSkew}_{j,t}=\sigma_{25\Delta\text{ put},j,t}-\sigma_{\text{ATM},j,t}.
$$

$$
\text{SkewZ}_{j,t}=\frac{\text{PutSkew}_{j,t}-\mu_{j,t}^{(L)}}{s_{j,t}^{(L)}}.
$$

### Term-Structure Features

$$
\text{TermSlope}_{j,t}=\sigma_{\text{ATM},j,t}(\tau_2)-\sigma_{\text{ATM},j,t}(\tau_1).
$$

### Earnings Proximity

$$
\text{DaysToEarnings}_{j,t}=\min_{e\in\mathcal{E}_j}(e-t).
$$

An earnings indicator can be:

$$
\text{PreEarnings}_{j,t}=\mathbf{1}\{0<\text{DaysToEarnings}_{j,t}\le D\}.
$$

### Borrow and Short-Constraint Features

$$
\text{BorrowCost}_{j,t}=b_{j,t}.
$$

$$
\text{HardToBorrow}_{j,t}=\mathbf{1}\{b_{j,t}>b^*\;\text{or locate unavailable}\}.
$$

### Liquidity Features

$$
\text{BidAskPct}_{i,t}=\frac{\text{Ask}_{i,t}-\text{Bid}_{i,t}}{(\text{Ask}_{i,t}+\text{Bid}_{i,t})/2}.
$$

$$
\text{LiquidityScore}_{i,t}=c_1\log(1+OI_{i,t})+c_2\log(1+Vol_{i,t})-c_3\text{BidAskPct}_{i,t}.
$$

### Factor Exposure Features

For stock return $R_{j,t}$ and factor returns $F_{k,t}$:

$$
R_{j,t}=\alpha_j+\sum_{k=1}^{K}\beta_{j,k}F_{k,t}+\varepsilon_{j,t}.
$$

The factor beta vector is:

$$
\boldsymbol{\beta}_{j}=\begin{bmatrix}\beta_{j,1}&\cdots&\beta_{j,K}\end{bmatrix}^{\top}.
$$

Options on high-beta, high-idiosyncratic-volatility, or event-sensitive stocks should be ranked differently from options on stable mega-cap stocks.

## 5.14.2 Composite Ranking Score

A generic short-volatility attractiveness score for option $i$ on stock $j$ can be written as:

$$
\text{ShortVolScore}_{i,t}
= a_1Z(\text{VRP}_{i,t})
+a_2Z(\text{SkewRichness}_{i,t})
+a_3Z(\text{LiquidityScore}_{i,t})
-a_4Z(\text{JumpRisk}_{j,t})
-a_5Z(\text{BorrowCost}_{j,t})
-a_6Z(\text{EarningsRisk}_{j,t})
-a_7Z(\text{Crowding}_{j,t}).
$$

Variables:

- $Z(\cdot)$ denotes cross-sectional or time-series standardization;
- $a_1,\ldots,a_7$ are research weights estimated or assigned under validation controls;
- jump risk, borrow cost, earnings risk, and crowding reduce attractiveness for short-volatility trades.

A long-convexity score might reverse some terms:

$$
\text{LongConvexityScore}_{i,t}
= b_1Z(\widehat{\sigma}_{\text{real}}^2-\sigma_{\text{imp}}^2)
+b_2Z(\text{JumpRiskForecast}_{j,t})
+b_3Z(\text{ConvexityScore}_{i,t})
-b_4Z(\text{SpreadCost}_{i,t})
-b_5Z(\text{ThetaDrag}_{i,t}).
$$

## 5.15 Why Naive High-Yield Short-Volatility Strategies Are Dangerous

A naive strategy may sell options with the highest annualized premium yield:

$$
\text{PremiumYield}_{i,t}=\frac{\text{OptionPremium}_{i,t}}{S_{j,t}}\cdot\frac{1}{\tau_i}.
$$

High premium yield can indicate opportunity, but it can also indicate severe risk. Reasons include:

- upcoming earnings announcement;
- takeover, litigation, regulatory, or credit event;
- hard-to-borrow stock;
- meme-stock or short-squeeze risk;
- illiquid options with stale quotes;
- wide bid-ask spreads;
- distressed equity with jump-to-default risk;
- corporate action uncertainty;
- extremely high margin requirements;
- crowded short-volatility positioning.

A safer research score penalizes risk-adjusted yield:

$$
\text{RiskAdjustedPremium}_{i,t}
=\frac{\text{PremiumYield}_{i,t}}
{1+\lambda_1\text{JumpRisk}_{j,t}+\lambda_2\text{SpreadCost}_{i,t}+\lambda_3\text{MarginIntensity}_{i,t}+\lambda_4\text{BorrowCost}_{j,t}}.
$$

Even this score is only a screen. It does not replace scenario analysis, liquidity checks, and tail-risk controls.

## 5.16 Regime Dependency of Strategy Families

Systematic options strategies are regime-dependent. A strategy that performs in one environment may fail in another.

| Regime | Preferred Exposures | Strategies Often Considered | Strategies Requiring Caution |
|---|---|---|---|
| Low-vol carry | Controlled short gamma, short vega, theta carry | Covered calls, defined-risk short premium, calendars | Unhedged short straddles if complacency is extreme |
| Stable carry | Short vol with strict risk limits | Iron condors, collars, overwriting | Long gamma with expensive theta |
| Rising-vol transition | Long vega, long gamma, long skew | Long puts, straddles, put spreads, protective overlays | Short skew and naked short gamma |
| High-vol stress | Defined-risk convexity, liquidity preservation | Put spreads, collars, reduced gross exposure | Adding short vol too early |
| Post-shock normalization | Selective short vega, term-structure trades | Calendars, short vol with crash limits | Long vol after premium spikes |
| Crash convexity | Long downside gamma and skew | Tail hedges, long wings | Short puts, short variance |
| Vol-of-vol expansion | Long volga, long wings | Convex structures, optionality on volatility | Vega-neutral books with hidden short volga |

Regime labels should be probabilistic. A portfolio should map regime probabilities to exposures rather than switch all capital between strategies.

## 5.17 Implementation Pseudocode: Cross-Sectional Option Signal Ranking

The following pseudocode outlines a research pipeline for ranking individual stock options. It is intentionally simplified but executable in principle after replacing data-loading functions with production data access.

```python
import numpy as np
import pandas as pd


def zscore_cross_section(series: pd.Series, winsor: float = 3.0) -> pd.Series:
    """Robust cross-sectional z-score with winsorization."""
    x = series.astype(float).replace([np.inf, -np.inf], np.nan)
    med = x.median(skipna=True)
    mad = (x - med).abs().median(skipna=True)
    scale = 1.4826 * mad if mad and mad > 0 else x.std(skipna=True)
    if not scale or not np.isfinite(scale) or scale == 0:
        return pd.Series(0.0, index=series.index)
    z = (x - med) / scale
    return z.clip(-winsor, winsor).fillna(0.0)


def compute_option_ranking_features(option_df: pd.DataFrame) -> pd.DataFrame:
    """Compute stylized option ranking features.

    Expected columns
    ----------------
    implied_vol, forecast_realized_vol, put_skew, bid, ask,
    open_interest, volume, days_to_earnings, borrow_cost,
    jump_risk_score, crowding_score, theta, gamma, spot.
    """
    required = [
        "implied_vol",
        "forecast_realized_vol",
        "put_skew",
        "bid",
        "ask",
        "open_interest",
        "volume",
        "days_to_earnings",
        "borrow_cost",
        "jump_risk_score",
        "crowding_score",
        "theta",
        "gamma",
        "spot",
    ]
    missing = [c for c in required if c not in option_df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = option_df.copy()
    mid = (df["bid"] + df["ask"]) / 2.0
    df["bid_ask_pct"] = (df["ask"] - df["bid"]) / mid.replace(0.0, np.nan)
    df["vrp"] = df["implied_vol"] ** 2 - df["forecast_realized_vol"] ** 2
    df["liquidity_score"] = (
        np.log1p(df["open_interest"].clip(lower=0))
        + 0.5 * np.log1p(df["volume"].clip(lower=0))
        - 5.0 * df["bid_ask_pct"].fillna(1.0)
    )
    df["pre_earnings"] = ((df["days_to_earnings"] > 0) & (df["days_to_earnings"] <= 10)).astype(float)
    df["convexity_per_theta"] = (
        df["gamma"] * df["spot"] ** 2 / (df["theta"].abs() + 1e-8)
    )

    for col in [
        "vrp",
        "put_skew",
        "liquidity_score",
        "borrow_cost",
        "jump_risk_score",
        "crowding_score",
        "pre_earnings",
        "convexity_per_theta",
    ]:
        df[f"z_{col}"] = zscore_cross_section(df[col])

    return df


def score_short_vol_candidates(option_df: pd.DataFrame) -> pd.DataFrame:
    """Rank short-volatility candidates with risk penalties."""
    df = compute_option_ranking_features(option_df)
    df["short_vol_score"] = (
        1.00 * df["z_vrp"]
        + 0.35 * df["z_put_skew"]
        + 0.75 * df["z_liquidity_score"]
        - 0.75 * df["z_borrow_cost"]
        - 1.00 * df["z_jump_risk_score"]
        - 0.75 * df["z_pre_earnings"]
        - 0.50 * df["z_crowding_score"]
    )
    return df.sort_values("short_vol_score", ascending=False)


def score_long_convexity_candidates(option_df: pd.DataFrame) -> pd.DataFrame:
    """Rank long-convexity candidates with cost penalties."""
    df = compute_option_ranking_features(option_df)
    df["long_convexity_score"] = (
        -1.00 * df["z_vrp"]
        + 0.75 * df["z_jump_risk_score"]
        + 0.50 * df["z_pre_earnings"]
        + 0.50 * df["z_convexity_per_theta"]
        + 0.50 * df["z_liquidity_score"]
        - 0.50 * df["z_crowding_score"]
    )
    return df.sort_values("long_convexity_score", ascending=False)
```

Important implementation notes:

- The scoring weights above are illustrative and must be validated.
- Features should be computed point-in-time.
- Universe filters should be applied before ranking.
- Scores must be tested after realistic transaction costs.
- Earnings and corporate-action dates must be historically accurate.
- Short-volatility rankings require margin and tail-risk constraints.

## 5.18 Implementation Pseudocode: Strategy-Level Allocation

A systematic strategy allocation engine can combine signals, regime probabilities, and Greek budgets.

```python
import numpy as np
import pandas as pd


def normalize_positive_weights(raw_scores: pd.Series, max_weight: float) -> pd.Series:
    """Convert positive scores into weights capped by max total allocation."""
    scores = raw_scores.clip(lower=0.0).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    total = scores.sum()
    if total <= 0:
        return pd.Series(0.0, index=raw_scores.index)
    return max_weight * scores / total


def allocate_strategy_sleeves(
    sleeve_scores: pd.Series,
    regime_probabilities: pd.Series,
    sleeve_regime_loadings: pd.DataFrame,
    max_total_weight: float = 1.0,
    risk_scale: float = 1.0,
) -> pd.Series:
    """Allocate across option strategy sleeves.

    Parameters
    ----------
    sleeve_scores:
        Expected attractiveness score by sleeve.
    regime_probabilities:
        Probability of each regime. Index must match columns of sleeve_regime_loadings.
    sleeve_regime_loadings:
        Matrix where rows are sleeves and columns are regimes. Positive values
        indicate suitability of a sleeve for a regime.
    max_total_weight:
        Maximum total allocation across sleeves.
    risk_scale:
        Multiplier between 0 and 1 that reduces allocation under high risk.
    """
    if not sleeve_regime_loadings.columns.equals(regime_probabilities.index):
        raise ValueError("Regime probability index must match loading columns")
    if not sleeve_regime_loadings.index.equals(sleeve_scores.index):
        raise ValueError("Sleeve score index must match loading rows")
    if not (0 <= risk_scale <= 1):
        raise ValueError("risk_scale must be between 0 and 1")

    regime_suitability = sleeve_regime_loadings @ regime_probabilities
    combined_score = sleeve_scores * regime_suitability
    return normalize_positive_weights(combined_score, max_total_weight * risk_scale)


# Example sleeves and regimes.
sleeves = pd.Index(["long_gamma", "short_vega_carry", "collars", "calendars"])
regimes = pd.Index(["low_vol_carry", "rising_vol", "stress", "normalization"])

sleeve_scores = pd.Series(
    [0.4, 0.7, 0.5, 0.6],
    index=sleeves,
)

regime_probs = pd.Series(
    [0.25, 0.30, 0.20, 0.25],
    index=regimes,
)

loadings = pd.DataFrame(
    {
        "low_vol_carry": [0.2, 1.0, 0.4, 0.7],
        "rising_vol": [1.0, 0.1, 0.8, 0.5],
        "stress": [0.8, 0.0, 1.0, 0.2],
        "normalization": [0.3, 0.8, 0.5, 1.0],
    },
    index=sleeves,
)

weights = allocate_strategy_sleeves(
    sleeve_scores=sleeve_scores,
    regime_probabilities=regime_probs,
    sleeve_regime_loadings=loadings,
    max_total_weight=0.60,
    risk_scale=0.80,
)
print(weights.round(4))
```

This example is deliberately simplified. A production allocation engine must also impose Greek constraints, margin constraints, liquidity limits, turnover limits, and drawdown controls.

## 5.19 Research Validation Standards

A Greek-based alpha model should be evaluated under robust validation standards.

| Validation Area | Required Control |
|---|---|
| Point-in-time data | Use only data known at the decision timestamp |
| Survivorship bias | Include delisted stocks and historical option availability |
| Look-ahead bias | Avoid revised earnings dates, revised constituents, or future corporate actions |
| Transaction costs | Include spreads, slippage, commissions, impact, borrow, and financing |
| Liquidity | Enforce volume, open interest, spread, and capacity filters |
| Margin | Compute returns on margin or economic capital, not only premium |
| Regime stability | Test performance by volatility, macro, liquidity, and drawdown regimes |
| Tail risk | Report expected shortfall, worst windows, crash scenarios, and gap losses |
| Turnover | Measure hedge turnover, option roll turnover, and signal turnover |
| Robustness | Test alternate lookbacks, definitions, ranking weights, and rebalance schedules |
| Explainability | Attribute P&L to Greeks, surface moves, carry, costs, and residuals |
| Implementation feasibility | Confirm that trades can be executed at assumed prices and sizes |

## 5.20 Failure Modes of Systematic Options Alpha Research

| Failure Mode | Description | Mitigation |
|---|---|---|
| Selling hidden crash beta | Strategy appears market-neutral but loses in crashes | Stress beta, skew, correlation, and liquidity jointly |
| Overfitting surface features | Complex signals fit noise in historical surfaces | Use simple hypotheses, holdout periods, and regime tests |
| Ignoring costs | Gross edge disappears after spreads and hedging | Conservative execution model |
| Misclassifying event volatility | Earnings premium treated as ordinary VRP | Separate event and diffusive variance |
| Using stale quotes | False implied-volatility signals | Quote filters and execution validation |
| Ignoring borrow | Short hedges or synthetic shorts become expensive | Borrow cost and locate constraints |
| Assuming stable correlations | Dispersion fails during correlation spikes | Correlation stress and exposure caps |
| Ignoring margin | Strategy forced to delever during stress | Margin stress and liquidity reserve |
| Treating regimes as binary | Overtrading and false confidence | Probability-weighted regime allocation |
| Ignoring residual P&L | Model misses important risk drivers | P&L attribution and residual escalation |

## 5.21 Summary of Part 5

Part 5 translated Greeks into a systematic alpha research framework.

Key points:

1. Greeks are state variables, not alpha by themselves.
2. Alpha research must distinguish expected return, carry, risk premia, convexity, liquidity premium, financing premium, and model error.
3. Volatility risk premium strategies compare implied variance with expected realized variance but are exposed to crashes and volatility spikes.
4. Skew premium strategies may earn compensation for selling expensive protection but can fail severely during tail events.
5. Term-structure strategies depend on forward volatility, roll-down, event timing, and tenor-specific vega basis.
6. Jump premium is central for earnings, macro events, and single-stock gap risk.
7. Convexity demand can make options expensive or cheap relative to expected realized movement and hedging utility.
8. Dispersion trades are correlation-risk trades, not merely collections of volatility trades.
9. Liquidity premium must be evaluated net of realistic entry, exit, impact, and stress costs.
10. Strategy families should be described by payoff, Greeks, alpha source, carry, liquidity, margin, and failure mode.
11. Single-stock option ranking requires volatility, skew, term structure, earnings, borrow, liquidity, idiosyncratic risk, and factor exposure features.
12. Naive high-yield short-volatility strategies are dangerous because high premium often signals high hidden risk.
13. Strategy allocation should combine signal strength with regime probabilities and risk scaling, not binary switches.
14. Institutional validation requires point-in-time data, transaction costs, liquidity constraints, margin modeling, stress testing, and P&L attribution.

The next installment will cover Part 6: Regime-Aware Options Strategy Selection, including volatility regimes, macro regimes, Hidden Markov Models, Bayesian filtering, system dynamics, probability-weighted allocation, and Greek budget constraints.
