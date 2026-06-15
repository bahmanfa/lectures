# Institutional Options Greeks, Systematic Strategy, and Regime-Aware Portfolio Construction Curriculum

## Completed Installment

This installment contains:

- Part 7: Greek-Aware Multi-Asset and Single-Stock Options Portfolio Construction.

The document is educational and research-oriented. It is not personalized investment advice, a live trading recommendation, or a claim that any option strategy produces guaranteed alpha.

---

# Part 7: Greek-Aware Multi-Asset and Single-Stock Options Portfolio Construction

**Level:** Expert

## 7.1 Purpose of Part 7

Parts 1 through 6 developed pricing foundations, core Greeks, higher-order Greeks, hedging dynamics, volatility-surface structure, systematic alpha signals, and regime-aware strategy selection. Part 7 turns these components into a portfolio construction framework.

The institutional problem is not merely to identify attractive option trades. The institutional problem is to decide how many trades to hold, how large each trade should be, how Greeks should net across instruments, how much margin and liquidity the portfolio can support, how to control single-name and sector concentration, and how to maintain exposures across changing regimes.

A Greek-aware options portfolio construction process treats option sensitivities as risk factors. It asks:

- What is the portfolio's total delta, gamma, theta, vega, rho, vanna, volga, charm, and skew exposure?
- How are these exposures distributed across underlying assets, sectors, maturities, strikes, countries, currencies, and volatility-surface buckets?
- Which exposures intentionally represent alpha or hedging utility, and which are accidental residual risks?
- How do single-stock event risks, borrow costs, earnings gaps, liquidity, and corporate actions change the portfolio's risk profile?
- What constraints are required to prevent hidden crash beta, excessive margin usage, crowded short-volatility exposure, or unhedgeable idiosyncratic jump risk?
- How should expected return, covariance, transaction costs, margin, and Greek budgets interact inside an optimizer?

The central principle is:

$$
\text{Options portfolio construction is constrained allocation across nonlinear risk factors, not simple position sizing by premium or notional.}
$$

## 7.2 Greeks as Portfolio Risk Factors

For a portfolio with $N$ option positions, let $w_i$ denote the signed position size of instrument $i$. The sign convention is:

- $w_i>0$ for a long option position;
- $w_i<0$ for a short option position.

If position $i$ has contract multiplier $M_i$ and per-option Greek $G_i^{(m)}$ for Greek or risk factor $m$, the portfolio exposure to Greek $m$ is:

$$
G_p^{(m)}=\sum_{i=1}^{N} w_i M_i G_i^{(m)}.
$$

Variables:

- $G_p^{(m)}$ is the portfolio-level exposure to Greek $m$;
- $G_i^{(m)}$ is the per-option exposure of instrument $i$;
- $w_i$ is signed number of contracts or model units;
- $M_i$ is the contract multiplier;
- $m$ may represent delta, gamma, theta, vega, rho, vanna, volga, charm, skew exposure, term-vega exposure, or margin exposure.

The same aggregation logic applies to any risk factor that is additive under position scaling. For example:

$$
\Delta_p=\sum_{i=1}^{N}w_iM_i\Delta_i,
$$

$$
\Gamma_p=\sum_{i=1}^{N}w_iM_i\Gamma_i,
$$

$$
\nu_p=\sum_{i=1}^{N}w_iM_i\nu_i,
$$

$$
\Theta_p=\sum_{i=1}^{N}w_iM_i\Theta_i.
$$

The interpretation depends on units. Vega per 1.00 volatility unit must not be mixed with vega per one volatility point. Theta per year must not be mixed with theta per day. Delta per contract must not be mixed with dollar delta.

## 7.3 Exposure Units and Scaling

Institutional systems should define exposure units before optimization. A portfolio can look conservative under one unit convention and aggressive under another.

| Exposure | Formula | Interpretation | Common Constraint Use |
|---|---:|---|---|
| Share delta | $\sum_i w_iM_i\Delta_i$ | Equivalent shares or units of underlying | Delta neutrality and hedge sizing |
| Dollar delta | $\sum_i w_iM_i\Delta_iS_i$ | Approximate P&L for 100% underlying move | Directional risk budget |
| Beta-adjusted delta | $\sum_i w_iM_i\Delta_iS_i\beta_i$ | Equity-market-equivalent exposure | Market beta control |
| Gamma dollars | $\sum_i w_iM_i\Gamma_iS_i^2$ | Convexity scaled by underlying level | Gamma budget and stress risk |
| Vega dollars | $\sum_i w_iM_i\nu_i/100$ | P&L for one vol-point move | Volatility exposure budget |
| Theta dollars | $\sum_i w_iM_i\Theta_i/365$ | Daily time carry | Carry budget and decay tolerance |
| Rho dollars | $\sum_i w_iM_i\rho_i/10000$ | P&L for one bp rate move | Rate risk budget |
| Margin usage | $\sum_i \mathcal{M}_i(w_i)$ | Capital required by broker/clearing | Leverage and liquidity constraint |
| Liquidity usage | $|w_i|/\text{ADV}_i$ or $|w_i|/\text{OI}_i$ | Position size relative to tradability | Capacity and exit constraint |

A useful gamma-dollar definition is:

$$
\text{GammaDollar}_i = w_iM_i\Gamma_iS_i^2.
$$

The approximate gamma P&L for a small return $r_i=\Delta S_i/S_i$ is:

$$
\text{Gamma P\&L}_i\approx \frac{1}{2}w_iM_i\Gamma_iS_i^2r_i^2
=\frac{1}{2}\text{GammaDollar}_i r_i^2.
$$

This scaling makes gamma comparable across underlyings with different price levels.

## 7.4 Netting and Aggregation Across Risk Buckets

Aggregate portfolio Greeks can hide concentrated risks. A portfolio with near-zero total vega may be long short-dated single-name vega and short long-dated index vega. A portfolio with near-zero total delta may be long high-beta technology delta and short low-beta defensive delta. A portfolio with small total gamma may still have dangerous short gamma around one crowded strike.

Therefore Greek exposures should be bucketed.

Let $b$ represent a risk bucket. Examples include:

- underlying ticker;
- sector;
- country;
- currency;
- maturity bucket;
- delta bucket;
- moneyness bucket;
- volatility tenor;
- event status;
- liquidity tier;
- strategy sleeve.

The bucketed Greek exposure is:

$$
G_{p,b}^{(m)}=\sum_{i=1}^{N}w_iM_iG_i^{(m)}\mathbf{1}\{i\in b\},
$$

where $\mathbf{1}\{i\in b\}$ equals one if instrument $i$ belongs to bucket $b$ and zero otherwise.

For multiple bucket dimensions, define bucket tuple $\mathbf{b}=(b_1,b_2,\ldots,b_L)$. Then:

$$
G_{p,\mathbf{b}}^{(m)}=\sum_{i=1}^{N}w_iM_iG_i^{(m)}\mathbf{1}\{i\in\mathbf{b}\}.
$$

For example, one can compute:

$$
\nu_{p,\text{Technology},\,30\text{d},\,25\Delta\text{ put}}
$$

as total vega exposure in technology-sector options, around 30-day maturity, in the 25-delta put bucket.

## 7.5 Core Portfolio Greek Aggregation Equations

## 7.5.1 Delta Aggregation

Per-underlying delta exposure is:

$$
\Delta_{p,j}=\sum_{i:u(i)=j}w_iM_i\Delta_i,
$$

where $u(i)=j$ means option $i$ references underlying $j$.

Dollar delta is:

$$
\text{DollarDelta}_{p,j}=S_j\Delta_{p,j}.
$$

Portfolio dollar delta is:

$$
\text{DollarDelta}_{p}=\sum_{j=1}^{J}S_j\Delta_{p,j}.
$$

If $\beta_j$ is the market beta of underlying $j$, beta-adjusted dollar delta is:

$$
\text{BetaAdjDelta}_{p}=\sum_{j=1}^{J}\beta_jS_j\Delta_{p,j}.
$$

This matters for equity portfolios because $1$ dollar of delta in a high-beta stock is not equivalent to $1$ dollar of delta in a low-beta stock.

## 7.5.2 Gamma Aggregation

Per-underlying gamma-dollar exposure is:

$$
\text{GammaDollar}_{p,j}=\sum_{i:u(i)=j}w_iM_i\Gamma_iS_j^2.
$$

Portfolio gamma-dollar exposure is:

$$
\text{GammaDollar}_{p}=\sum_{j=1}^{J}\text{GammaDollar}_{p,j}.
$$

For a small return vector $\mathbf{r}$, the gamma P&L approximation is:

$$
\text{Gamma P\&L}_p\approx \frac{1}{2}\sum_{j=1}^{J}\text{GammaDollar}_{p,j}r_j^2.
$$

Gamma aggregation is nonlinear in spot changes because P&L depends on squared returns. Netting gamma across underlyings is imperfect because different stocks do not move identically. Short gamma in one stock is not fully offset by long gamma in another stock unless the return paths, volatilities, correlations, and hedge rules align.

## 7.5.3 Vega Aggregation

Total vega is:

$$
\nu_p=\sum_{i=1}^{N}w_iM_i\nu_i.
$$

Vega per one volatility point is:

$$
\nu_p^{\text{1 vol point}}=\frac{1}{100}\sum_{i=1}^{N}w_iM_i\nu_i.
$$

Bucketed vega by maturity bucket $m$ and moneyness bucket $d$ is:

$$
\nu_{p,m,d}=\sum_{i\in\mathcal{B}(m,d)}w_iM_i\nu_i.
$$

Surface-aware vega should be represented as a vector:

$$
\boldsymbol{\nu}_p=\begin{bmatrix}
\nu_{1m,ATM} \\
\nu_{1m,25\Delta put} \\
\nu_{3m,ATM} \\
\nu_{3m,25\Delta put} \\
\nu_{6m,ATM} \\
\nu_{1y,ATM}
\end{bmatrix}.
$$

This vector representation is more informative than one total vega number.

## 7.5.4 Theta Aggregation

Annual theta is:

$$
\Theta_p=\sum_{i=1}^{N}w_iM_i\Theta_i.
$$

Daily theta using a calendar-day convention is:

$$
\Theta_p^{\text{daily}}=\frac{1}{365}\sum_{i=1}^{N}w_iM_i\Theta_i.
$$

Theta can be interpreted as carry only under a carefully specified assumption: spot, implied volatility, rates, dividends, and surface shape remain unchanged except for the passage of time. In reality, theta is earned or paid together with gamma, vega, skew, financing, and transaction costs.

## 7.5.5 Rho Aggregation

Rho per basis point is:

$$
\rho_p^{\text{bp}}=\frac{1}{10000}\sum_{i=1}^{N}w_iM_i\rho_i.
$$

For short-dated equity options, rho may be small. For long-dated options, FX options, rates options, and macro portfolios, rho can be material. Rate shocks can also interact with equity volatility through discount-rate channels and macro regimes.

## 7.5.6 Vanna and Volga Aggregation

Vanna exposure is:

$$
\text{Vanna}_p=\sum_{i=1}^{N}w_iM_i\text{Vanna}_i.
$$

Volga exposure is:

$$
\text{Volga}_p=\sum_{i=1}^{N}w_iM_i\text{Volga}_i.
$$

These are important because a portfolio can be delta-neutral and vega-neutral but still have large exposure to spot-volatility co-movement and volatility convexity.

A local spot-volatility P&L approximation is:

$$
\Delta V_p\approx
\Delta_p\Delta S+
\nu_p\Delta\sigma+
\frac{1}{2}\Gamma_p(\Delta S)^2+
\text{Vanna}_p\Delta S\Delta\sigma+
\frac{1}{2}\text{Volga}_p(\Delta\sigma)^2.
$$

For multi-underlying portfolios, this approximation must be applied by underlying and volatility bucket.

## 7.6 Greek Exposure Matrix Representation

A portfolio can be represented using an exposure matrix. Let:

- $N$ be the number of candidate instruments;
- $M$ be the number of risk factors or Greeks;
- $\mathbf{w}\in\mathbb{R}^{N}$ be the vector of position weights;
- $\mathbf{A}\in\mathbb{R}^{M\times N}$ be the exposure matrix;
- $A_{m,i}$ be the exposure of instrument $i$ to risk factor $m$.

Then portfolio exposures are:

$$
\mathbf{g}_p=\mathbf{A}\mathbf{w},
$$

where:

$$
\mathbf{g}_p=
\begin{bmatrix}
\Delta_p \\
\text{GammaDollar}_p \\
\nu_p^{1\text{ vol point}} \\
\Theta_p^{daily} \\
\text{Vanna}_p \\
\text{Volga}_p \\
\text{SkewExposure}_p \\
\text{Margin}_p
\end{bmatrix}.
$$

This matrix representation enables optimization with linear Greek constraints. Nonlinear quantities such as margin, expected shortfall, drawdown, and transaction costs may require approximations, iterative optimization, or nonlinear solvers.

## 7.7 Factor Mapping for Option Exposures

Options inherit factor exposures from their underlyings and add nonlinear exposures through Greeks. A single-stock option on stock $j$ has exposure to equity factors through delta and gamma.

Suppose underlying return $R_j$ follows a factor model:

$$
R_j=\alpha_j+\boldsymbol{\beta}_j^{\top}\mathbf{F}+\varepsilon_j,
$$

where:

- $\mathbf{F}\in\mathbb{R}^{K}$ is a vector of factor returns;
- $\boldsymbol{\beta}_j\in\mathbb{R}^{K}$ is the factor beta vector for stock $j$;
- $\varepsilon_j$ is idiosyncratic return.

The option's first-order factor exposure through delta is approximately:

$$
\mathbf{b}_{i}^{\Delta}=w_iM_i\Delta_iS_j\boldsymbol{\beta}_j.
$$

Portfolio factor delta exposure is:

$$
\mathbf{b}_{p}^{\Delta}=\sum_{i=1}^{N}w_iM_i\Delta_iS_{u(i)}\boldsymbol{\beta}_{u(i)}.
$$

Gamma creates nonlinear exposure to factor moves. If stock $j$ return is $R_j\approx\boldsymbol{\beta}_j^{\top}\mathbf{F}+\varepsilon_j$, gamma P&L is approximately:

$$
\text{Gamma P\&L}_i\approx\frac{1}{2}w_iM_i\Gamma_iS_j^2\left(\boldsymbol{\beta}_j^{\top}\mathbf{F}+\varepsilon_j\right)^2.
$$

Expanding the factor component:

$$
\left(\boldsymbol{\beta}_j^{\top}\mathbf{F}\right)^2
=\mathbf{F}^{\top}\boldsymbol{\beta}_j\boldsymbol{\beta}_j^{\top}\mathbf{F}.
$$

Thus gamma exposure can be mapped to quadratic factor exposure:

$$
\mathbf{Q}_{p}^{\Gamma}=\sum_{i=1}^{N}\frac{1}{2}w_iM_i\Gamma_iS_{u(i)}^2\boldsymbol{\beta}_{u(i)}\boldsymbol{\beta}_{u(i)}^{\top}.
$$

This matrix $\mathbf{Q}_{p}^{\Gamma}$ describes how portfolio gamma responds to squared factor moves and factor interactions.

## 7.8 Sector-Level and Macro-Factor Aggregation

For equity options, sector aggregation is essential. Let $\mathcal{S}_c$ be the set of underlyings in sector $c$. Sector dollar delta is:

$$
\text{SectorDelta}_{c}=\sum_{j\in\mathcal{S}_c}\sum_{i:u(i)=j}w_iM_i\Delta_iS_j.
$$

Sector gamma dollars are:

$$
\text{SectorGamma}_{c}=\sum_{j\in\mathcal{S}_c}\sum_{i:u(i)=j}w_iM_i\Gamma_iS_j^2.
$$

Sector vega is:

$$
\text{SectorVega}_{c}=\sum_{j\in\mathcal{S}_c}\sum_{i:u(i)=j}w_iM_i\nu_i.
$$

Macro-factor aggregation may use beta mappings to factors such as:

- equity market;
- size;
- value;
- momentum;
- quality;
- low volatility;
- rates sensitivity;
- credit sensitivity;
- commodity sensitivity;
- currency sensitivity;
- inflation sensitivity.

For macro factor $k$, delta-equivalent exposure is:

$$
\text{MacroDelta}_{k}=\sum_{j=1}^{J}\left(\sum_{i:u(i)=j}w_iM_i\Delta_iS_j\right)\beta_{j,k}.
$$

A portfolio can be market-delta neutral but still have large factor exposure if long-delta positions are concentrated in high-beta or high-momentum stocks and short-delta positions are concentrated elsewhere.

## 7.9 Multi-Asset Options Portfolio Construction

A multi-asset options portfolio can include:

- equity index options;
- ETF options;
- single-stock options;
- futures options;
- FX options;
- rates options;
- commodity options;
- volatility derivatives;
- variance swaps or variance-like exposures.

Each asset class has distinct Greek conventions and risk drivers.

| Asset Class | Key Underlying Risk | Important Option Risk | Special Implementation Issue |
|---|---|---|---|
| Equity index | Market beta and correlation | Skew, crash risk, variance premium | Index dividend assumptions and correlation shocks |
| Single stock | Idiosyncratic and factor risk | Earnings gaps, borrow, corporate actions | American exercise and hard-to-borrow constraints |
| ETF | Basket and tracking risk | ETF liquidity and creation/redemption dynamics | Underlying basket liquidity may differ from ETF liquidity |
| Futures option | Futures curve and roll | Commodity/rates curve optionality | Contract expiry and futures basis |
| FX option | Currency pair and rates differential | Delta convention, premium adjustment, smile | Domestic/foreign rates and settlement |
| Rates option | Yield curve and volatility | Rho, curve gamma, smile | Model choice and curve construction |
| Commodity option | Spot/futures curve, storage | Term structure, seasonality, jumps | Delivery, inventory, geopolitical shocks |

Cross-asset aggregation must avoid false netting. Equity vega should not be automatically netted against FX vega. Rate gamma is not the same as equity gamma. Cross-asset covariance and stress behavior determine whether offsets are reliable.

## 7.10 Applying the Framework to Individual Stock Options

Single-stock options require special care because idiosyncratic events can dominate continuous-diffusion Greeks.

## 7.10.1 Earnings Gaps

Earnings create discrete jump risk. A delta-hedged option cannot be continuously hedged through an overnight earnings gap. If stock price jumps from $S_-$ to $S_+$ after earnings, the option repricing P&L is:

$$
\Delta V^{\text{earnings}}=V(S_+,\sigma_+,t_+)-V(S_-,\sigma_-,t_-).
$$

A local approximation using delta and gamma may be inaccurate if the jump is large and implied volatility collapses.

A portfolio constraint may limit event exposure:

$$
\sum_{i\in\mathcal{E}(D)}|w_i|M_i\text{EventVega}_i \le L_{\text{event}},
$$

where $\mathcal{E}(D)$ is the set of options whose underlying has earnings within $D$ days.

## 7.10.2 Takeover Risk

Takeover risk can create upside gaps. Short calls can lose substantially if a stock gaps upward due to acquisition news. Upside skew can become expensive in names with credible takeover speculation.

A takeover-risk control can penalize short call exposure in flagged names:

$$
\sum_{i\in\mathcal{T}}\max(0,-w_i)M_i\text{CallTailExposure}_i\le L_{\text{takeover}},
$$

where $\mathcal{T}$ is the set of takeover-sensitive underlyings.

## 7.10.3 Borrow Costs and Hard-to-Borrow Constraints

Borrow costs affect hedging, put-call parity, synthetic forwards, and short-option economics. If a delta hedge requires short stock, borrow cost matters:

$$
\text{BorrowCost}_{j,t}\approx |h_{j,t}^{-}|S_{j,t}b_{j,t}\Delta t,
$$

where:

- $h_{j,t}^{-}=\min(h_{j,t},0)$ is the short stock hedge;
- $b_{j,t}$ is annualized borrow cost.

A hard-to-borrow constraint may be:

$$
|h_{j,t}^{-}|\le \text{LocateAvailable}_{j,t}.
$$

If borrow is unavailable, a theoretically delta-hedged strategy may be impossible to implement.

## 7.10.4 Liquidity and Crowding

Single-name option liquidity is uneven. A realistic portfolio must constrain position size relative to open interest, volume, and spread:

$$
|w_i|\le \lambda_{OI}\cdot OI_i,
$$

$$
|w_i|\le \lambda_{Vol}\cdot \text{Volume}_{i}^{(L)},
$$

$$
\text{BidAskPct}_i\le s_{\max}.
$$

Crowding risk can be approximated using option volume, open interest changes, skew richness, retail-flow proxies, short interest, and abnormal call-put activity. Crowding should reduce capacity and increase stress costs.

## 7.10.5 Idiosyncratic Jumps and Corporate Actions

Single-name options are exposed to:

- earnings surprises;
- product announcements;
- litigation;
- regulatory decisions;
- credit events;
- mergers and acquisitions;
- special dividends;
- spin-offs;
- stock splits;
- index inclusion or deletion;
- management changes.

A portfolio construction process should maintain separate limits for idiosyncratic jump exposure. A stylized jump-risk budget is:

$$
\sum_{j=1}^{J}\text{JumpLoss}_{j}^{\alpha}(\mathbf{w})\le L_{\text{jump}},
$$

where $\text{JumpLoss}_{j}^{\alpha}$ is a scenario loss for underlying $j$ under an $\alpha$-severity jump scenario.

## 7.11 Single-Stock Option Risk Table

| Risk | Why It Matters | Affected Strategies | Control |
|---|---|---|---|
| Earnings gap | Price jumps cannot be continuously hedged | Short straddles, short strangles, calendars | Event filters, event variance limits |
| Volatility crush | IV falls after event | Long pre-earnings options | Event P&L scenarios |
| Takeover risk | Upside gap hurts short calls | Covered calls, call overwriting, short call spreads | M&A flags and short-call caps |
| Borrow squeeze | Short hedge becomes expensive or unavailable | Delta-hedged long calls, synthetic shorts | Borrow and locate constraints |
| Hard-to-borrow parity distortion | Option prices reflect stock loan market | Puts, conversions, reversals | Borrow-adjusted pricing |
| Liquidity | Wide spreads can erase edge | All single-name option strategies | Spread, volume, OI filters |
| Crowding | Exit pressure and one-sided hedging | Short vol and retail-heavy names | Crowding penalty and capacity cuts |
| Corporate actions | Contract terms can change | All listed options | Corporate-action processing |
| Idiosyncratic jump | Company-specific discontinuity | Short gamma and short skew | Jump scenarios and name caps |
| Factor concentration | Many names share hidden factor | Cross-sectional option books | Sector and factor constraints |

## 7.12 Portfolio Construction Constraint Table

| Constraint Type | Mathematical Form | Purpose |
|---|---:|---|
| Delta neutrality | $L_{\Delta}\le\mathbf{a}_{\Delta}^{\top}\mathbf{w}\le U_{\Delta}$ | Control directional risk |
| Beta-adjusted delta | $|\mathbf{a}_{\beta\Delta}^{\top}\mathbf{w}|\le U_{\beta\Delta}$ | Control market beta exposure |
| Gamma budget | $L_{\Gamma}\le\mathbf{a}_{\Gamma}^{\top}\mathbf{w}\le U_{\Gamma}$ | Limit convexity exposure |
| Vega budget | $L_{\nu}\le\mathbf{a}_{\nu}^{\top}\mathbf{w}\le U_{\nu}$ | Control volatility exposure |
| Theta carry | $L_{\Theta}\le\mathbf{a}_{\Theta}^{\top}\mathbf{w}\le U_{\Theta}$ | Limit time decay or short-convexity carry |
| Vanna budget | $|\mathbf{a}_{\text{Vanna}}^{\top}\mathbf{w}|\le U_{\text{Vanna}}$ | Control spot-vol co-movement |
| Volga budget | $|\mathbf{a}_{\text{Volga}}^{\top}\mathbf{w}|\le U_{\text{Volga}}$ | Control volatility convexity |
| Sector concentration | $|\mathbf{a}_{c}^{\top}\mathbf{w}|\le U_c$ | Avoid sector crowding |
| Maturity bucket | $L_m\le\mathbf{a}_m^{\top}\mathbf{w}\le U_m$ | Control tenor concentration |
| Liquidity | $|w_i|\le\lambda OI_i$ | Avoid oversized positions |
| Margin | $\mathcal{M}(\mathbf{w})\le M_{\max}$ | Control capital usage |
| Turnover | $\sum_i |w_i-w_i^{old}|\le T_{\max}$ | Control trading cost |
| Transaction cost | $\text{TC}(\mathbf{w},\mathbf{w}^{old})\le C_{\max}$ | Preserve net alpha |
| Event exposure | $\sum_{i\in\mathcal{E}}|w_i|E_i\le E_{\max}$ | Limit earnings and jump risk |

## 7.13 Expected Return Model for Option Positions

Let $\boldsymbol{\mu}\in\mathbb{R}^{N}$ be expected net return or expected P&L per unit position. A Greek-aware expected return model can combine alpha signals and carry components:

$$
\mu_i=
\mu_i^{\text{VRP}}+
\mu_i^{\text{skew}}+
\mu_i^{\text{term}}+
\mu_i^{\text{jump}}+
\mu_i^{\text{liquidity}}+
\mu_i^{\text{hedging}}
-C_i^{\text{entry}}-C_i^{\text{exit}}-C_i^{\text{financing}}-C_i^{\text{borrow}}.
$$

Variables:

- $\mu_i^{\text{VRP}}$ is expected compensation from volatility risk premium;
- $\mu_i^{\text{skew}}$ is expected compensation from skew risk premium;
- $\mu_i^{\text{term}}$ is expected roll-down or term-structure return;
- $\mu_i^{\text{jump}}$ is expected compensation or cost for event jump exposure;
- $\mu_i^{\text{liquidity}}$ is liquidity premium or liquidity cost;
- $\mu_i^{\text{hedging}}$ is expected gamma-scalping or hedging benefit;
- $C_i$ terms are costs.

This decomposition is conceptual. In production, expected return should be estimated conservatively and validated through walk-forward tests.

## 7.14 Covariance Model for Option Strategy Returns

Let $\boldsymbol{\Sigma}\in\mathbb{R}^{N\times N}$ be the covariance matrix of position returns or P&L. For options, covariance must include more than underlying returns. A factor representation may be:

$$
\mathbf{r}^{\text{opt}}_t=\mathbf{B}\mathbf{f}_t+\boldsymbol{\epsilon}_t,
$$

where:

- $\mathbf{r}^{\text{opt}}_t$ is vector of option or strategy returns;
- $\mathbf{B}$ is factor exposure matrix;
- $\mathbf{f}_t$ includes equity returns, volatility changes, skew changes, term-structure changes, rates, credit spreads, liquidity shocks, and factor returns;
- $\boldsymbol{\epsilon}_t$ is residual return.

The covariance is:

$$
\boldsymbol{\Sigma}=\mathbf{B}\boldsymbol{\Sigma}_f\mathbf{B}^{\top}+\boldsymbol{\Sigma}_{\epsilon},
$$

where:

- $\boldsymbol{\Sigma}_f$ is factor covariance;
- $\boldsymbol{\Sigma}_{\epsilon}$ is residual covariance.

For options, factor covariance should include co-movement among:

- underlying returns;
- implied volatility changes;
- skew changes;
- term-structure changes;
- correlation shocks;
- liquidity shocks;
- margin shocks.

## 7.15 Mean-Variance Optimization with Greek Constraints

A basic Greek-constrained mean-variance optimization is:

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
\mathcal{M}(\mathbf{w})\le M_{\max},
$$

$$
\sum_{i=1}^{N}|w_i-w_i^{old}|\le T_{\max}.
$$

Variables:

- $\boldsymbol{\mu}$ is expected return vector;
- $\boldsymbol{\Sigma}$ is covariance matrix;
- $\lambda$ is risk-aversion parameter;
- $\text{TC}(\cdot)$ is transaction-cost function;
- $\mathbf{A}$ is Greek exposure matrix;
- $\mathbf{L}_g$ and $\mathbf{U}_g$ are lower and upper Greek limits;
- $\mathbf{l}$ and $\mathbf{u}$ are position bounds;
- $\mathcal{M}(\mathbf{w})$ is margin usage;
- $M_{\max}$ is maximum margin budget;
- $T_{\max}$ is turnover budget.

This framework is useful but incomplete if returns are highly non-normal or dominated by jumps. Therefore expected shortfall and stress constraints should be added.

## 7.16 Risk-Budgeting Objective

A risk-budgeting approach allocates risk contributions rather than maximizing expected return directly. Let portfolio volatility be:

$$
\sigma_p=\sqrt{\mathbf{w}^{\top}\boldsymbol{\Sigma}\mathbf{w}}.
$$

The marginal risk contribution of position $i$ is:

$$
\text{MRC}_i=\frac{(\boldsymbol{\Sigma}\mathbf{w})_i}{\sigma_p}.
$$

The total risk contribution is:

$$
\text{RC}_i=w_i\text{MRC}_i.
$$

A risk-budgeting objective minimizes deviation from target risk budgets $b_i$:

$$
\min_{\mathbf{w}}\quad \sum_{i=1}^{N}\left(\text{RC}_i-b_i\sigma_p\right)^2
$$

subject to Greek, liquidity, margin, and position constraints.

For options, risk budgets can be assigned by strategy sleeve, Greek exposure, or stress scenario rather than by instrument alone.

## 7.17 Expected Shortfall Optimization

Expected shortfall is often more relevant than variance for options because P&L distributions can be skewed and fat-tailed.

Let $L(\mathbf{w},\omega)$ be portfolio loss in scenario $\omega$. The expected shortfall at confidence level $\alpha$ is:

$$
ES_{\alpha}(\mathbf{w})=\mathbb{E}\left[L(\mathbf{w},\omega)\mid L(\mathbf{w},\omega)\ge VaR_{\alpha}(\mathbf{w})\right].
$$

A scenario-based optimization can be written as:

$$
\max_{\mathbf{w}}\quad \boldsymbol{\mu}^{\top}\mathbf{w}-\lambda ES_{\alpha}(\mathbf{w})-\text{TC}(\mathbf{w},\mathbf{w}^{old})
$$

subject to:

$$
\mathbf{L}_g\le\mathbf{A}\mathbf{w}\le\mathbf{U}_g,
$$

$$
\mathcal{M}(\mathbf{w})\le M_{\max},
$$

$$
\text{StressLoss}_s(\mathbf{w})\le L_s^{\max},\quad s=1,\ldots,S.
$$

This is often more appropriate for short-volatility and short-skew portfolios because variance can understate crash exposure.

## 7.18 Drawdown-Aware Optimization

A drawdown-aware framework penalizes path-dependent losses. Let $W_t(\mathbf{w})$ be simulated portfolio wealth, and let running maximum wealth be:

$$
H_t(\mathbf{w})=\max_{u\le t}W_u(\mathbf{w}).
$$

Drawdown is:

$$
D_t(\mathbf{w})=\frac{W_t(\mathbf{w})}{H_t(\mathbf{w})}-1.
$$

Maximum drawdown is:

$$
MDD(\mathbf{w})=\min_t D_t(\mathbf{w}).
$$

A drawdown-aware objective may be:

$$
\max_{\mathbf{w}}\quad
\boldsymbol{\mu}^{\top}\mathbf{w}
-\lambda_1\mathbf{w}^{\top}\boldsymbol{\Sigma}\mathbf{w}
-\lambda_2|MDD(\mathbf{w})|
-\lambda_3\text{TC}(\mathbf{w},\mathbf{w}^{old}).
$$

Options strategies with positive average returns but severe episodic losses should be evaluated using drawdown-aware metrics.

## 7.19 Utility-Based Optimization with Margin and Transaction Costs

A utility-based objective can incorporate risk aversion, margin, and transaction costs:

$$
\max_{\mathbf{w}}\quad
\mathbb{E}\left[U\left(W_0+\Delta W(\mathbf{w})\right)\right]
-\lambda_c\text{TC}(\mathbf{w},\mathbf{w}^{old})
-\lambda_m\mathcal{M}(\mathbf{w}),
$$

where $U(W)$ may be constant relative risk aversion utility:

$$
U(W)=\frac{W^{1-\gamma}}{1-\gamma},\quad \gamma\ne 1,
$$

or logarithmic utility:

$$
U(W)=\log(W).
$$

Variables:

- $W_0$ is initial wealth or capital;
- $\Delta W(\mathbf{w})$ is scenario-dependent P&L;
- $\gamma$ is risk-aversion coefficient;
- $\lambda_c$ penalizes transaction costs;
- $\lambda_m$ penalizes margin usage.

Utility-based methods are theoretically appealing but require realistic scenario distributions. If the scenario generator underestimates jumps or liquidity stress, utility optimization can still allocate too aggressively to short-volatility trades.

## 7.20 Margin Constraints

Margin is nonlinear and broker-specific. A simplified approximation is:

$$
\mathcal{M}(\mathbf{w})=\sum_{i=1}^{N}m_i|w_i|+\sum_{s=1}^{S}\max\left(0,\text{StressLoss}_{s}(\mathbf{w})\right)h_s,
$$

where:

- $m_i$ is base margin per unit of instrument $i$;
- $\text{StressLoss}_{s}(\mathbf{w})$ is loss under scenario $s$;
- $h_s$ is a stress margin multiplier.

A margin constraint is:

$$
\mathcal{M}(\mathbf{w})\le M_{\max}.
$$

Margin should also be stressed dynamically. During volatility spikes, margin may increase when P&L is already negative:

$$
\mathcal{M}_{t}^{\text{stress}}=\mathcal{M}(\mathbf{w};\sigma_t+\Delta\sigma, S_t+\Delta S, \text{LiquidityStress}_t).
$$

A portfolio that is optimal under normal margin can be infeasible under stress margin.

## 7.21 Transaction Cost Model

A practical transaction-cost model includes spread, slippage, and impact:

$$
\text{TC}(\mathbf{w},\mathbf{w}^{old})=
\sum_{i=1}^{N}\left[
\frac{1}{2}\text{Spread}_i|\Delta w_i|M_i
+\eta_i\left(\frac{|\Delta w_i|}{ADV_i}\right)^{\alpha_i}|\Delta w_i|S_i
+\text{Commission}_i|\Delta w_i|
\right],
$$

where:

- $\Delta w_i=w_i-w_i^{old}$;
- $\text{Spread}_i$ is bid-ask spread in option premium terms;
- $ADV_i$ is average daily volume or an analogous liquidity measure;
- $\eta_i$ is impact coefficient;
- $\alpha_i$ controls nonlinear impact;
- $M_i$ is contract multiplier.

For options, cost models should be regime-dependent because spreads widen during stress. A stress-adjusted spread can be:

$$
\text{Spread}_{i,t}^{\text{stress}}=\text{Spread}_{i,t}\left(1+a_1\text{VolStress}_t+a_2\text{LiquidityStress}_t+a_3\text{EventRisk}_{i,t}\right).
$$

## 7.22 Turnover and Rebalancing

Options portfolios face turnover from:

- signal changes;
- delta hedging;
- option expiry and rolling;
- Greek drift;
- regime probability changes;
- liquidity changes;
- risk-limit breaches.

Turnover can be defined as:

$$
\text{Turnover}_t=\sum_{i=1}^{N}|w_{i,t}-w_{i,t}^{old}|.
$$

A notional turnover measure is:

$$
\text{NotionalTurnover}_t=\sum_{i=1}^{N}|w_{i,t}-w_{i,t}^{old}|M_iP_{i,t},
$$

where $P_{i,t}$ is option premium. For hedging, underlying hedge turnover should be measured separately:

$$
\text{HedgeTurnover}_t=\sum_{j=1}^{J}|h_{j,t}-h_{j,t}^{old}|S_{j,t}.
$$

A strategy can have attractive gross alpha but poor net alpha if hedge turnover and roll costs are too high.

## 7.23 Full Repricing Versus Greek Approximation in Portfolio Construction

Optimization often uses linear Greek approximations because they are tractable. Risk management should supplement them with full repricing.

A Greek approximation under scenario $s$ is:

$$
\Delta V_{p,s}^{\text{Greek}}
=\sum_{i=1}^{N}w_iM_i\left[
\Delta_i\Delta S_{i,s}
+\frac{1}{2}\Gamma_i(\Delta S_{i,s})^2
+\nu_i\Delta\sigma_{i,s}
+\text{Vanna}_i\Delta S_{i,s}\Delta\sigma_{i,s}
+\frac{1}{2}\text{Volga}_i(\Delta\sigma_{i,s})^2
\right].
$$

A full repricing scenario is:

$$
\Delta V_{p,s}^{\text{Full}}=\sum_{i=1}^{N}w_iM_i\left[V_i(\mathbf{x}_{i,s})-V_i(\mathbf{x}_{i,0})\right],
$$

where $\mathbf{x}_{i,s}$ is the shocked state vector for option $i$.

For large shocks, full repricing should dominate. Greek approximations are best used for local attribution, constraints, and optimization approximations.

## 7.24 Python Pseudocode: Greek-Aware Portfolio Exposure Aggregation

The following code illustrates a practical aggregation structure. It assumes a DataFrame of option positions with precomputed Greeks and metadata.

```python
import numpy as np
import pandas as pd


def validate_position_frame(df: pd.DataFrame) -> None:
    required = [
        "position", "multiplier", "underlying", "sector", "spot",
        "delta", "gamma", "vega", "theta", "rho", "vanna", "volga",
        "maturity_bucket", "delta_bucket", "bid_ask_pct", "open_interest", "volume"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if (df["multiplier"] <= 0).any():
        raise ValueError("multipliers must be positive")
    if (df["spot"] <= 0).any():
        raise ValueError("spot prices must be positive")


def add_scaled_greeks(df: pd.DataFrame) -> pd.DataFrame:
    """Add position-scaled Greek exposures.

    Vega is assumed to be per 1.00 volatility unit and is converted to
    one-vol-point vega. Theta is assumed annual and converted to daily theta.
    """
    validate_position_frame(df)
    out = df.copy()
    scale = out["position"] * out["multiplier"]

    out["share_delta"] = scale * out["delta"]
    out["dollar_delta"] = out["share_delta"] * out["spot"]
    out["gamma_dollar"] = scale * out["gamma"] * out["spot"] ** 2
    out["vega_1vol"] = scale * out["vega"] / 100.0
    out["theta_daily"] = scale * out["theta"] / 365.0
    out["rho_1bp"] = scale * out["rho"] / 10_000.0
    out["vanna_1vol"] = scale * out["vanna"] / 100.0
    out["volga_vol_point_sq"] = scale * out["volga"] / 10_000.0
    return out


def aggregate_exposures(df: pd.DataFrame, group_cols: list[str] | None = None) -> pd.DataFrame:
    """Aggregate scaled Greeks overall or by specified groups."""
    scaled = add_scaled_greeks(df)
    exposure_cols = [
        "share_delta", "dollar_delta", "gamma_dollar", "vega_1vol",
        "theta_daily", "rho_1bp", "vanna_1vol", "volga_vol_point_sq"
    ]
    if group_cols is None:
        return scaled[exposure_cols].sum().to_frame("portfolio_total")
    return scaled.groupby(group_cols, dropna=False)[exposure_cols].sum().reset_index()


# Example usage:
# total_exposure = aggregate_exposures(positions)
# sector_exposure = aggregate_exposures(positions, ["sector"])
# maturity_delta_exposure = aggregate_exposures(positions, ["maturity_bucket", "delta_bucket"])
```

## 7.25 Python Pseudocode: Factor Mapping of Delta Exposure

```python
def map_delta_to_factors(
    positions: pd.DataFrame,
    factor_betas: pd.DataFrame,
    underlying_col: str = "underlying",
) -> pd.Series:
    """Map option dollar delta to factor exposures.

    Parameters
    ----------
    positions:
        Position-level DataFrame with underlying, position, multiplier,
        delta, and spot columns.
    factor_betas:
        DataFrame indexed by underlying with factor beta columns.

    Returns
    -------
    Series of portfolio factor exposures in dollar-delta units.
    """
    scaled = add_scaled_greeks(positions)
    merged = scaled[[underlying_col, "dollar_delta"]].merge(
        factor_betas,
        left_on=underlying_col,
        right_index=True,
        how="left",
    )
    factor_cols = [c for c in factor_betas.columns]
    if merged[factor_cols].isna().any().any():
        raise ValueError("Missing factor betas for at least one underlying")

    factor_exposure = merged[factor_cols].multiply(merged["dollar_delta"], axis=0).sum()
    return factor_exposure
```

## 7.26 Python Pseudocode: Greek-Constrained Portfolio Optimizer

The following implementation uses `scipy.optimize.minimize` for a simplified Greek-constrained mean-variance problem. It is executable in principle but should be extended for production with robust covariance estimation, integer contract handling, nonlinear margin, full repricing stress constraints, and transaction-cost calibration.

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize, LinearConstraint, Bounds


def solve_greek_constrained_optimizer(
    expected_returns: pd.Series,
    covariance: pd.DataFrame,
    exposure_matrix: pd.DataFrame,
    lower_greek_bounds: pd.Series,
    upper_greek_bounds: pd.Series,
    lower_position_bounds: pd.Series,
    upper_position_bounds: pd.Series,
    old_weights: pd.Series | None = None,
    risk_aversion: float = 5.0,
    turnover_penalty: float = 0.001,
) -> pd.Series:
    """Solve a simplified Greek-constrained mean-variance optimizer.

    Parameters
    ----------
    expected_returns:
        Expected net return or expected P&L per unit position. Index = instruments.
    covariance:
        Covariance matrix indexed and columned by instruments.
    exposure_matrix:
        Matrix with rows = Greeks/risk factors and columns = instruments.
    lower_greek_bounds, upper_greek_bounds:
        Bounds for portfolio Greek exposures.
    lower_position_bounds, upper_position_bounds:
        Instrument-level position bounds.
    old_weights:
        Previous weights for turnover penalty. If None, zeros are used.
    risk_aversion:
        Penalty on portfolio variance.
    turnover_penalty:
        Quadratic turnover penalty coefficient.

    Returns
    -------
    Optimized weights as a pandas Series.
    """
    instruments = expected_returns.index
    if not covariance.index.equals(instruments) or not covariance.columns.equals(instruments):
        raise ValueError("covariance must align with expected_returns index")
    if not exposure_matrix.columns.equals(instruments):
        raise ValueError("exposure_matrix columns must align with expected_returns index")
    if old_weights is None:
        old_weights = pd.Series(0.0, index=instruments)
    old_weights = old_weights.reindex(instruments).fillna(0.0)

    mu = expected_returns.to_numpy(dtype=float)
    sigma = covariance.to_numpy(dtype=float)
    a = exposure_matrix.to_numpy(dtype=float)
    w_old = old_weights.to_numpy(dtype=float)

    # Symmetrize covariance for numerical stability.
    sigma = 0.5 * (sigma + sigma.T)
    ridge = 1e-8 * np.eye(len(instruments))
    sigma = sigma + ridge

    def objective(w: np.ndarray) -> float:
        expected = mu @ w
        variance = w @ sigma @ w
        turnover = np.sum((w - w_old) ** 2)
        return -(expected - 0.5 * risk_aversion * variance - turnover_penalty * turnover)

    linear_constraint = LinearConstraint(
        a,
        lb=lower_greek_bounds.reindex(exposure_matrix.index).to_numpy(dtype=float),
        ub=upper_greek_bounds.reindex(exposure_matrix.index).to_numpy(dtype=float),
    )

    bounds = Bounds(
        lb=lower_position_bounds.reindex(instruments).to_numpy(dtype=float),
        ub=upper_position_bounds.reindex(instruments).to_numpy(dtype=float),
    )

    x0 = np.clip(w_old, bounds.lb, bounds.ub)
    result = minimize(
        objective,
        x0=x0,
        method="SLSQP",
        bounds=bounds,
        constraints=[linear_constraint],
        options={"maxiter": 1000, "ftol": 1e-9},
    )
    if not result.success:
        raise RuntimeError(f"Optimization failed: {result.message}")

    return pd.Series(result.x, index=instruments, name="optimized_weight")
```

## 7.27 Python Pseudocode: Scenario-Based Expected Shortfall Optimizer

The following pseudocode uses scenarios of instrument P&L. This is often more suitable for options than relying only on covariance.

```python
def expected_shortfall(losses: np.ndarray, alpha: float = 0.95) -> float:
    """Compute empirical expected shortfall from a vector of losses."""
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    losses = np.asarray(losses, dtype=float)
    var = np.quantile(losses, alpha)
    tail = losses[losses >= var]
    return float(tail.mean()) if len(tail) else float(var)


def solve_es_optimizer(
    expected_returns: pd.Series,
    scenario_pnl: pd.DataFrame,
    exposure_matrix: pd.DataFrame,
    lower_greek_bounds: pd.Series,
    upper_greek_bounds: pd.Series,
    lower_position_bounds: pd.Series,
    upper_position_bounds: pd.Series,
    alpha: float = 0.95,
    es_penalty: float = 1.0,
) -> pd.Series:
    """Simplified expected-shortfall optimizer using scenario P&L.

    scenario_pnl rows are scenarios and columns are instruments. Positive values
    are gains. Loss is negative portfolio P&L.
    """
    instruments = expected_returns.index
    pnl = scenario_pnl[instruments].to_numpy(dtype=float)
    mu = expected_returns.to_numpy(dtype=float)
    a = exposure_matrix[instruments].to_numpy(dtype=float)

    def objective(w: np.ndarray) -> float:
        portfolio_pnl = pnl @ w
        losses = -portfolio_pnl
        es = expected_shortfall(losses, alpha=alpha)
        return -(mu @ w - es_penalty * es)

    linear_constraint = LinearConstraint(
        a,
        lb=lower_greek_bounds.reindex(exposure_matrix.index).to_numpy(dtype=float),
        ub=upper_greek_bounds.reindex(exposure_matrix.index).to_numpy(dtype=float),
    )
    bounds = Bounds(
        lower_position_bounds.reindex(instruments).to_numpy(dtype=float),
        upper_position_bounds.reindex(instruments).to_numpy(dtype=float),
    )
    x0 = np.zeros(len(instruments))
    result = minimize(
        objective,
        x0=x0,
        method="SLSQP",
        bounds=bounds,
        constraints=[linear_constraint],
        options={"maxiter": 1000, "ftol": 1e-8},
    )
    if not result.success:
        raise RuntimeError(f"ES optimization failed: {result.message}")
    return pd.Series(result.x, index=instruments, name="optimized_weight")
```

## 7.28 Practical Workflow for Building a Greek-Aware Portfolio

A practical process can be organized as follows.

| Step | Action | Output |
|---|---|---|
| 1 | Define universe and filters | Tradable options universe |
| 2 | Clean quotes and compute implied vols | Valid option chain |
| 3 | Compute analytical and surface-aware Greeks | Position-level risk features |
| 4 | Build alpha and carry signals | Expected return estimates |
| 5 | Build covariance and scenario model | Risk model and stress matrix |
| 6 | Aggregate current exposures | Portfolio Greek dashboard |
| 7 | Define constraints | Greek, liquidity, margin, sector, event limits |
| 8 | Optimize candidate portfolio | Proposed trades and target weights |
| 9 | Full reprice stress scenarios | Loss, margin, and liquidity diagnostics |
| 10 | Apply execution model | Cost-adjusted implementation plan |
| 11 | Monitor post-trade | Greeks, P&L attribution, residuals, limit usage |
| 12 | Rebalance or de-risk | Updated portfolio and audit trail |

## 7.29 Production Readiness Checklist for Portfolio Construction

| Area | Required Control |
|---|---|
| Data | Point-in-time option chains, rates, dividends, borrow, corporate actions, earnings |
| Models | Versioned pricing, surface, Greek, and margin models |
| Greeks | Core, higher-order, bucketed, and surface-aware exposures |
| Single-name risk | Earnings, takeover, borrow, liquidity, crowding, and corporate-action flags |
| Optimization | Greek constraints, risk model, transaction costs, margin, turnover, and stress limits |
| Stress testing | Spot, volatility, skew, term, rate, liquidity, jump, and correlation shocks |
| Execution | Spread, slippage, impact, order-size, and capacity assumptions |
| Governance | Audit trail for data, signals, optimizer inputs, and overrides |
| Monitoring | Intraday or daily exposure, P&L attribution, residuals, and limit breaches |
| De-risking | Kill-switches, drawdown controls, margin controls, and liquidity reserves |

## 7.30 Common Portfolio Construction Errors

| Error | Why It Is Dangerous | Better Practice |
|---|---|---|
| Optimizing on premium yield only | Selects hidden jump and distress risk | Use risk-adjusted expected return and stress losses |
| Netting Greeks too broadly | Hides bucket concentration | Aggregate by underlying, sector, tenor, moneyness, and event state |
| Ignoring single-stock events | Earnings gaps dominate Greeks | Separate event variance and event limits |
| Ignoring borrow | Hedge may be impossible or costly | Include borrow and locate constraints |
| Using covariance only | Understates nonlinear tail risk | Add scenario and expected shortfall constraints |
| Ignoring margin procyclicality | Forced deleveraging in stress | Stress margin jointly with P&L |
| Assuming liquidity is constant | Exit costs rise in losses | Use regime-dependent costs and capacity limits |
| Treating vega as one number | Misses skew and term basis | Bucket vega by surface node |
| Ignoring vanna and volga | Vega neutrality can break after shocks | Include higher-order Greek budgets |
| Overfitting optimizer inputs | Produces unstable weights | Use shrinkage, robust constraints, and turnover penalties |

## 7.31 Summary of Part 7

Part 7 developed a Greek-aware portfolio construction framework for multi-asset and single-stock option portfolios.

Key points:

1. Greeks should be treated as portfolio risk factors, not merely trade-level diagnostics.
2. Portfolio-level exposures require consistent scaling by position size, contract multiplier, underlying price, volatility unit, and time convention.
3. Aggregate Greeks can hide risk; exposures must be bucketed by underlying, sector, maturity, delta, moneyness, currency, country, strategy sleeve, and event state.
4. Delta can be mapped to dollar delta, beta-adjusted delta, sector delta, and macro-factor delta.
5. Gamma should be scaled by $S^2$ to compare convexity across underlyings.
6. Vega should be represented as a surface-bucket vector, not only one total number.
7. Single-stock options require explicit treatment of earnings gaps, takeover risk, borrow costs, hard-to-borrow constraints, liquidity, crowding, idiosyncratic jumps, and corporate actions.
8. Sector-level and factor-level aggregation prevent hidden concentration.
9. A Greek exposure matrix enables constrained optimization.
10. Mean-variance optimization is useful but insufficient for nonlinear option tails.
11. Expected shortfall, stress constraints, margin constraints, drawdown controls, and full repricing scenarios are essential for short-volatility and skew-sensitive portfolios.
12. Transaction costs, slippage, market impact, hedge turnover, and roll costs must be included before evaluating net alpha.
13. Margin is nonlinear and procyclical; stress margin can dominate normal-time position sizing.
14. Production readiness requires point-in-time data, model versioning, exposure monitoring, scenario testing, execution modeling, governance, and de-risking rules.

The next installment will cover Part 8: Covariance Estimation, Random Matrix Theory, and Risk Stabilization, including unstable covariance estimation in option portfolios, covariance across Greek factor shocks, Marchenko-Pastur cleaning, shrinkage, factor covariance, regime-conditioned covariance, and portfolio risk examples before and after cleaning.
