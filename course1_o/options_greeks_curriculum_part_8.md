# Institutional Options Greeks, Systematic Strategy, and Regime-Aware Portfolio Construction Curriculum

## Completed Installment

This installment contains:

- Part 8: Covariance Estimation, Random Matrix Theory, and Risk Stabilization.

The document is educational and research-oriented. It is not personalized investment advice, a live trading recommendation, or a claim that any option strategy produces guaranteed alpha.

---

# Part 8: Covariance Estimation, Random Matrix Theory, and Risk Stabilization

**Level:** Expert

## 8.1 Purpose of Part 8

Parts 1 through 7 developed the foundations of option pricing, Greeks, volatility surfaces, systematic alpha signals, regime-aware strategy selection, and Greek-aware portfolio construction. Part 8 addresses one of the most important implementation problems in institutional options portfolios: risk estimates are unstable.

Options portfolios are exposed to many interacting sources of uncertainty:

- underlying returns;
- implied-volatility changes;
- volatility skew changes;
- volatility term-structure changes;
- correlation shocks;
- jump shocks;
- liquidity shocks;
- margin shocks;
- Greek factor shocks such as delta, gamma, vega, vanna, and volga changes.

A portfolio optimizer or risk-budgeting engine needs covariance estimates for these risk drivers. However, covariance estimation is difficult because option portfolios are high-dimensional, nonlinear, non-stationary, fat-tailed, and regime-dependent. A naive sample covariance matrix can be noisy, unstable, nearly singular, and highly sensitive to the estimation window. The result can be excessive leverage, unstable weights, hidden concentration, false diversification, and high turnover.

The purpose of this part is to build a rigorous framework for covariance estimation and risk stabilization in options portfolios. The key principle is:

$$
\text{In options portfolios, covariance cleaning is not cosmetic. It is a core risk-control process.}
$$

Covariance cleaning does not create true information from noise. It attempts to reduce estimation error so that portfolio construction is less dominated by sampling artifacts.

## 8.2 Why Covariance Estimation Is Unstable in Option Portfolios

Let $\mathbf{r}_t\in\mathbb{R}^{N}$ denote a vector of returns, P&L changes, or factor shocks for $N$ instruments or risk factors at time $t$. The sample covariance matrix using $T$ observations is:

$$
\widehat{\boldsymbol{\Sigma}}=\frac{1}{T-1}\sum_{t=1}^{T}(\mathbf{r}_t-\bar{\mathbf{r}})(\mathbf{r}_t-\bar{\mathbf{r}})^{\top},
$$

where:

- $\widehat{\boldsymbol{\Sigma}}\in\mathbb{R}^{N\times N}$ is the sample covariance matrix;
- $\mathbf{r}_t$ is the return or shock vector at time $t$;
- $\bar{\mathbf{r}}=T^{-1}\sum_{t=1}^{T}\mathbf{r}_t$ is the sample mean vector;
- $N$ is the number of assets, strategies, instruments, or risk factors;
- $T$ is the number of observations.

If $N$ is large relative to $T$, the sample covariance matrix contains substantial estimation noise. If $N>T$, the sample covariance matrix is singular and cannot be inverted without regularization. This is a serious issue because mean-variance optimization, risk attribution, hedging, and factor neutralization often require inverse covariance matrices or stable eigenstructure.

Options portfolios make the problem harder than ordinary equity portfolios because:

1. **Nonlinear P&L:** option returns are not linear functions of underlying returns.
2. **Changing Greeks:** exposures change as spot, volatility, time, and surface shape change.
3. **Volatility clustering:** quiet periods and stress periods have very different covariance structures.
4. **Fat tails:** extreme moves are more common than Gaussian assumptions imply.
5. **Regime shifts:** correlations and volatilities change across macro and volatility regimes.
6. **Small samples:** many options have short histories, changing strikes, and limited observations.
7. **Stale quotes:** illiquid options can show artificial autocorrelation and understated volatility.
8. **Overlapping signals:** option strategies often share common short-volatility, short-skew, or liquidity exposures.
9. **Event risk:** earnings, policy meetings, and corporate actions generate discontinuities.
10. **Surface risk:** covariance across volatility level, skew, and term structure is not captured by underlying returns alone.

A covariance matrix estimated from calm regimes can underestimate stress risk. A covariance matrix estimated from a crisis can overstate normal-time risk and reduce capital efficiency. A robust system must recognize this trade-off.

## 8.3 What Covariance Means for Options

In a linear equity portfolio, covariance usually refers to covariance among asset returns. In an options portfolio, covariance can refer to several different objects.

## 8.3.1 Covariance of Option Returns

Let $R_{i,t}^{\text{opt}}$ be the return of option or strategy $i$. The option-return covariance is:

$$
\Sigma_{ij}^{\text{opt}}=\text{Cov}(R_{i,t}^{\text{opt}},R_{j,t}^{\text{opt}}).
$$

This is useful for strategy-level allocation but can be unstable because option returns are affected by changing moneyness, maturity decay, implied-volatility changes, and roll rules.

## 8.3.2 Covariance of P&L

For dollar-risk management, P&L covariance may be more relevant:

$$
\Sigma_{ij}^{\text{P\&L}}=\text{Cov}(\Delta V_{i,t},\Delta V_{j,t}).
$$

P&L covariance depends on position sizing and contract multipliers. It is suitable for portfolio risk and expected shortfall but less comparable across instruments unless normalized.

## 8.3.3 Covariance of Underlying Returns

For delta and gamma exposures, underlying return covariance matters:

$$
\Sigma_{ij}^{S}=\text{Cov}(R_{i,t}^{S},R_{j,t}^{S}).
$$

This is the familiar equity covariance matrix. It supports delta-equivalent and gamma-factor risk, but it does not capture implied-volatility, skew, or term-structure risk.

## 8.3.4 Covariance of Implied-Volatility Changes

For vega exposures, covariance among implied-volatility changes matters:

$$
\Sigma_{ij}^{\sigma}=\text{Cov}(\Delta\sigma_{i,t}^{\text{imp}},\Delta\sigma_{j,t}^{\text{imp}}).
$$

This covariance should often be bucketed by underlying, maturity, and moneyness. A one-month at-the-money volatility shock is not the same as a one-year downside-skew shock.

## 8.3.5 Covariance of Skew and Term-Structure Changes

Let $\kappa_t$ denote a skew feature, such as 25-delta put volatility minus at-the-money volatility. Let $\ell_t$ denote a term-structure feature, such as 3-month ATM volatility minus 1-month ATM volatility. Then:

$$
\Sigma^{\text{skew}}=\text{Cov}(\Delta\kappa_t),
$$

$$
\Sigma^{\text{term}}=\text{Cov}(\Delta\ell_t).
$$

In practice, these are often included inside a factor covariance matrix rather than as separate matrices.

## 8.3.6 Covariance of Greek Factor Shocks

A useful options risk representation is based on Greek P&L factors. For instrument $i$:

$$
\Delta V_i \approx
\Delta_i\Delta S_i+\frac{1}{2}\Gamma_i(\Delta S_i)^2
+\nu_i\Delta\sigma_i+\text{Vanna}_i\Delta S_i\Delta\sigma_i
+\frac{1}{2}\text{Volga}_i(\Delta\sigma_i)^2+\cdots.
$$

The covariance of P&L depends on the covariance of these shock terms:

$$
\text{Cov}(\Delta V_i,\Delta V_j)
\approx
\text{Cov}\left(
\Delta_i\Delta S_i+\nu_i\Delta\sigma_i+\cdots,
\Delta_j\Delta S_j+\nu_j\Delta\sigma_j+\cdots
\right).
$$

This is why a Greek-aware covariance model should include not only underlying return covariance but also cross-covariance between spot returns and implied-volatility changes:

$$
\text{Cov}(\Delta S_i,\Delta\sigma_j),
$$

as well as covariance among volatility shocks:

$$
\text{Cov}(\Delta\sigma_i,\Delta\sigma_j).
$$

Equity stress often involves negative spot-volatility co-movement: spot falls while implied volatility rises. Ignoring this cross-covariance can materially understate risk for portfolios with vanna exposure.

## 8.4 A Factor Covariance Representation for Options

A practical institutional approach is to model option P&L using a factor representation. Let $\mathbf{f}_t\in\mathbb{R}^{K}$ be a vector of risk-factor shocks:

$$
\mathbf{f}_t=
\begin{bmatrix}
\mathbf{r}^{S}_t \\
\Delta\boldsymbol{\sigma}^{ATM}_t \\
\Delta\boldsymbol{\kappa}^{skew}_t \\
\Delta\boldsymbol{\ell}^{term}_t \\
\Delta\boldsymbol{\rho}^{corr}_t \\
\Delta\mathbf{c}^{liq}_t
\end{bmatrix}.
$$

Components include:

- $\mathbf{r}^{S}_t$: underlying returns;
- $\Delta\boldsymbol{\sigma}^{ATM}_t$: changes in ATM implied volatility by underlying or index;
- $\Delta\boldsymbol{\kappa}^{skew}_t$: changes in skew features;
- $\Delta\boldsymbol{\ell}^{term}_t$: changes in volatility term-structure features;
- $\Delta\boldsymbol{\rho}^{corr}_t$: changes in implied or realized correlation;
- $\Delta\mathbf{c}^{liq}_t$: liquidity-cost or spread shocks.

Let $\mathbf{B}\in\mathbb{R}^{N\times K}$ be the exposure matrix mapping factor shocks to option or strategy P&L. Then:

$$
\mathbf{r}^{opt}_t = \mathbf{B}\mathbf{f}_t+\boldsymbol{\epsilon}_t,
$$

where:

- $\mathbf{r}^{opt}_t$ is a vector of option strategy returns or normalized P&L;
- $\boldsymbol{\epsilon}_t$ is residual risk not explained by the factors.

The covariance matrix is:

$$
\boldsymbol{\Sigma}_{opt}=\mathbf{B}\boldsymbol{\Sigma}_{f}\mathbf{B}^{\top}+\boldsymbol{\Sigma}_{\epsilon},
$$

where:

- $\boldsymbol{\Sigma}_{f}=\text{Cov}(\mathbf{f}_t)$ is factor covariance;
- $\boldsymbol{\Sigma}_{\epsilon}=\text{Cov}(\boldsymbol{\epsilon}_t)$ is residual covariance.

This representation is valuable because $K$ can be much smaller than $N$. It also improves interpretability: risk is decomposed into underlying, volatility, skew, term, correlation, and liquidity shocks.

## 8.5 Sample Covariance

The sample covariance matrix is the simplest estimator:

$$
\widehat{\boldsymbol{\Sigma}}_{sample}=\frac{1}{T-1}\mathbf{X}^{\top}\mathbf{X},
$$

where $\mathbf{X}\in\mathbb{R}^{T\times N}$ is the demeaned data matrix.

Strengths:

- easy to compute;
- transparent;
- unbiased under classical assumptions;
- useful as a baseline.

Weaknesses:

- unstable when $N/T$ is high;
- singular when $N>T$;
- highly sensitive to outliers;
- assumes stationarity over the estimation window;
- produces noisy eigenvalues and eigenvectors;
- leads to unstable optimizer weights.

In options portfolios, sample covariance is rarely sufficient on its own.

## 8.6 Exponentially Weighted Moving Average Covariance

An EWMA covariance estimator gives more weight to recent observations:

$$
\widehat{\boldsymbol{\Sigma}}_{t}^{EWMA}
=(1-\lambda)\sum_{j=0}^{\infty}\lambda^j \mathbf{x}_{t-j}\mathbf{x}_{t-j}^{\top},
$$

where:

- $\lambda\in(0,1)$ is the decay parameter;
- $\mathbf{x}_{t}$ is the demeaned return or shock vector at time $t$.

The recursive form is:

$$
\widehat{\boldsymbol{\Sigma}}_{t}^{EWMA}
=\lambda\widehat{\boldsymbol{\Sigma}}_{t-1}^{EWMA}+(1-\lambda)\mathbf{x}_{t}\mathbf{x}_{t}^{\top}.
$$

Strengths:

- adapts more quickly to changing volatility;
- simple and computationally efficient;
- useful for daily risk monitoring.

Weaknesses:

- still noisy in high dimensions;
- sensitive to decay parameter;
- can overreact to recent shocks;
- does not by itself solve rank deficiency when $N$ is large;
- may overweight crisis observations immediately after a shock.

EWMA is often useful as an input to shrinkage or factor models rather than a final standalone estimator.

## 8.7 Ledoit-Wolf Shrinkage and Linear Shrinkage

Shrinkage estimators combine the sample covariance matrix with a structured target. A generic linear shrinkage estimator is:

$$
\widehat{\boldsymbol{\Sigma}}_{shrink}
=\delta\mathbf{F}+(1-\delta)\widehat{\boldsymbol{\Sigma}}_{sample},
$$

where:

- $\mathbf{F}$ is a shrinkage target;
- $\delta\in[0,1]$ is the shrinkage intensity;
- $\widehat{\boldsymbol{\Sigma}}_{sample}$ is the sample covariance.

Common targets include:

1. **Identity target:**

$$
\mathbf{F}=\bar{\sigma}^2\mathbf{I},
$$

where $\bar{\sigma}^2$ is average variance.

2. **Constant-correlation target:**

$$
F_{ij}=\begin{cases}
\widehat{\sigma}_i^2, & i=j, \\
\bar{\rho}\widehat{\sigma}_i\widehat{\sigma}_j, & i\ne j,
\end{cases}
$$

where $\bar{\rho}$ is average pairwise correlation.

3. **Factor-model target:**

$$
\mathbf{F}=\mathbf{B}\widehat{\boldsymbol{\Sigma}}_f\mathbf{B}^{\top}+\widehat{\boldsymbol{\Sigma}}_{\epsilon}.
$$

Shrinkage stabilizes covariance estimates by pulling noisy sample estimates toward a structured prior. The trade-off is bias: too much shrinkage can suppress real relationships.

## 8.8 Random Matrix Theory and Marchenko-Pastur Cleaning

Random Matrix Theory provides a framework for distinguishing signal from noise in high-dimensional covariance matrices. The Marchenko-Pastur result describes the distribution of eigenvalues of a sample covariance matrix when the true covariance is identity and returns are independent Gaussian noise.

## 8.8.1 Setup

Let $\mathbf{X}\in\mathbb{R}^{T\times N}$ be a standardized data matrix with zero mean and unit variance columns. The sample correlation matrix is:

$$
\mathbf{C}=\frac{1}{T}\mathbf{X}^{\top}\mathbf{X}.
$$

Define the aspect ratio:

$$
q=\frac{N}{T}.
$$

Some texts use $Q=T/N$. This curriculum uses $q=N/T$.

If the true population correlation matrix is identity and $T,N\rightarrow\infty$ with $q=N/T$ fixed, then the eigenvalues of $\mathbf{C}$ are mostly contained in the Marchenko-Pastur interval:

$$
\lambda_{-}=(1-\sqrt{q})^2,
$$

$$
\lambda_{+}=(1+\sqrt{q})^2,
$$

when $0<q\le 1$. If $q>1$, the sample covariance has $N-T$ zero eigenvalues and is singular.

More generally, if the noise variance is $\sigma_{\epsilon}^2$, the bounds are:

$$
\lambda_{-}=\sigma_{\epsilon}^2(1-\sqrt{q})^2,
$$

$$
\lambda_{+}=\sigma_{\epsilon}^2(1+\sqrt{q})^2.
$$

Interpretation:

- eigenvalues below or within the Marchenko-Pastur noise band may be dominated by sampling noise;
- eigenvalues above $\lambda_+$ may contain common factor information;
- this is a statistical heuristic, not a proof that every large eigenvalue is true signal.

## 8.8.2 Eigenvalue Decomposition

For a sample correlation matrix $\mathbf{C}$, the eigenvalue decomposition is:

$$
\mathbf{C}=\mathbf{V}\boldsymbol{\Lambda}\mathbf{V}^{\top},
$$

where:

- $\mathbf{V}$ is the matrix of eigenvectors;
- $\boldsymbol{\Lambda}=\text{diag}(\lambda_1,\ldots,\lambda_N)$ is the diagonal matrix of eigenvalues;
- eigenvalues are often sorted from largest to smallest.

Noisy small eigenvalues can cause unstable inverse covariance matrices. Optimizers may exploit these small eigenvalues by taking large offsetting long-short positions that appear low-risk in sample but are not robust out of sample.

## 8.8.3 Eigenvalue Clipping

Eigenvalue clipping replaces noisy eigenvalues with a common value while preserving the trace of the correlation matrix. Let $\mathcal{N}$ be the set of eigenvalues considered noise, often those satisfying:

$$
\lambda_i\le\lambda_+.
$$

The clipped value is:

$$
\bar{\lambda}_{\mathcal{N}}=\frac{1}{|\mathcal{N}|}\sum_{i\in\mathcal{N}}\lambda_i.
$$

The cleaned eigenvalues are:

$$
\tilde{\lambda}_i=
\begin{cases}
\lambda_i, & \lambda_i>\lambda_+, \\
\bar{\lambda}_{\mathcal{N}}, & \lambda_i\le\lambda_+.
\end{cases}
$$

The cleaned correlation matrix is:

$$
\tilde{\mathbf{C}}=\mathbf{V}\tilde{\boldsymbol{\Lambda}}\mathbf{V}^{\top}.
$$

Finally, the matrix is normalized back to a valid correlation matrix with unit diagonal:

$$
\tilde{C}_{ij}^{corr}=\frac{\tilde{C}_{ij}}{\sqrt{\tilde{C}_{ii}\tilde{C}_{jj}}}.
$$

Then the cleaned covariance matrix is reconstructed using the original or separately estimated volatilities:

$$
\tilde{\boldsymbol{\Sigma}}=\mathbf{D}\tilde{\mathbf{C}}^{corr}\mathbf{D},
$$

where:

$$
\mathbf{D}=\text{diag}(\widehat{\sigma}_1,\ldots,\widehat{\sigma}_N).
$$

## 8.8.4 Covariance Cleaning Algorithm

A practical Marchenko-Pastur cleaning algorithm is:

1. Start with a return, P&L, or factor-shock matrix $\mathbf{R}\in\mathbb{R}^{T\times N}$.
2. Clean missing values and remove bad observations.
3. Standardize each column to zero mean and unit variance.
4. Compute the sample correlation matrix $\mathbf{C}$.
5. Compute eigenvalues and eigenvectors of $\mathbf{C}$.
6. Compute $q=N/T$ and Marchenko-Pastur upper bound $\lambda_+=(1+\sqrt{q})^2$.
7. Identify eigenvalues inside the noise band.
8. Replace noisy eigenvalues with their average or apply a shrinkage rule.
9. Reconstruct the cleaned correlation matrix.
10. Renormalize the diagonal to one.
11. Reconstruct covariance using volatility estimates.
12. Check positive semidefiniteness and numerical stability.

This process stabilizes the eigenstructure of the covariance matrix and can reduce optimizer instability.

## 8.9 Rotationally Invariant Estimators

Eigenvalue clipping keeps sample eigenvectors and adjusts eigenvalues. Rotationally invariant estimators, or RIEs, also operate in the eigenbasis but use more sophisticated nonlinear shrinkage of eigenvalues.

A general RIE form is:

$$
\widehat{\boldsymbol{\Sigma}}_{RIE}=\mathbf{V}\widehat{\boldsymbol{\Lambda}}_{RIE}\mathbf{V}^{\top},
$$

where:

- $\mathbf{V}$ contains sample eigenvectors;
- $\widehat{\boldsymbol{\Lambda}}_{RIE}$ contains cleaned eigenvalues derived from random matrix theory or nonlinear shrinkage.

RIE methods can outperform simple clipping when assumptions are closer to the theoretical setting and when implemented carefully. However, they are more complex and can be harder to explain to stakeholders.

Practical caveats:

- RIE still relies on sample eigenvectors;
- performance depends on sample size and stationarity;
- fat tails and autocorrelation can weaken theoretical assumptions;
- implementation errors are harder to detect than with simple shrinkage.

## 8.10 Hierarchical Clustering and Hierarchical Risk Models

Hierarchical methods stabilize covariance by recognizing clustered structure. In equity and options portfolios, instruments often cluster by:

- sector;
- country;
- underlying;
- maturity;
- strategy type;
- volatility surface bucket;
- factor exposure.

A hierarchical clustering process may:

1. Convert correlations to distances:

$$
d_{ij}=\sqrt{\frac{1-\rho_{ij}}{2}}.
$$

2. Build a hierarchical tree using single, complete, average, or Ward linkage.
3. Reorder the covariance matrix by cluster.
4. Allocate risk using hierarchical risk parity or cluster-based risk budgets.

Hierarchical methods can reduce optimizer sensitivity by avoiding direct inversion of a noisy covariance matrix. They are especially useful when expected returns are uncertain and when risk diversification is the main objective.

Limitations:

- clustering can be unstable across windows;
- distance metrics may not capture nonlinear option tail dependence;
- clusters can break down during stress;
- hierarchical methods do not eliminate the need for scenario testing.

## 8.11 Factor-Model Alternatives

A factor covariance model reduces dimensionality by representing returns through common factors. For options, factors should reflect both underlying and volatility risks.

Let:

$$
\mathbf{r}_t=\mathbf{B}\mathbf{f}_t+\boldsymbol{\epsilon}_t.
$$

Then:

$$
\boldsymbol{\Sigma}=\mathbf{B}\boldsymbol{\Sigma}_f\mathbf{B}^{\top}+\boldsymbol{\Sigma}_{\epsilon}.
$$

A Greek-aware factor model may include:

| Factor Group | Examples | Relevant Greeks |
|---|---|---|
| Equity market | index return, sector returns, style factors | delta, gamma |
| Volatility level | ATM IV changes by tenor | vega |
| Skew | 25-delta put minus ATM IV | skew exposure, vanna |
| Term structure | 3m IV minus 1m IV | term vega, calendars |
| Correlation | implied correlation, realized correlation | dispersion |
| Liquidity | bid-ask spread changes, volume shocks | execution and liquidation risk |
| Rates | yield changes, curve shifts | rho and macro-vol interaction |
| Credit | HY/IG spread changes, CDS proxies | downside skew and single-name jump |

Factor models are interpretable and scalable. Their weakness is omitted-factor risk. If the factor model excludes a risk driver that matters in stress, it can understate portfolio risk.

## 8.12 Regime-Conditioned Covariance

A single covariance matrix may be inappropriate if the market alternates between calm and stress regimes. A regime-conditioned covariance model estimates different covariance matrices for different states.

Let $z_t\in\{1,\ldots,K\}$ be the regime state. The conditional covariance is:

$$
\boldsymbol{\Sigma}_k=\text{Cov}(\mathbf{r}_t\mid z_t=k).
$$

Given regime probabilities $p_{k,t}$, a probability-weighted covariance estimate is:

$$
\widehat{\boldsymbol{\Sigma}}_t=\sum_{k=1}^{K}p_{k,t}\boldsymbol{\Sigma}_k.
$$

If regime means differ, the full mixture covariance is:

$$
\widehat{\boldsymbol{\Sigma}}_t
=\sum_{k=1}^{K}p_{k,t}\left[\boldsymbol{\Sigma}_k+(\boldsymbol{\mu}_k-\widehat{\boldsymbol{\mu}})(\boldsymbol{\mu}_k-\widehat{\boldsymbol{\mu}})^{\top}\right],
$$

where:

$$
\widehat{\boldsymbol{\mu}}=\sum_{k=1}^{K}p_{k,t}\boldsymbol{\mu}_k.
$$

Variables:

- $\boldsymbol{\Sigma}_k$ is covariance in regime $k$;
- $\boldsymbol{\mu}_k$ is mean return or shock vector in regime $k$;
- $p_{k,t}$ is the current probability of regime $k$.

Regime-conditioned covariance is valuable for options because correlations, volatilities, skew behavior, and liquidity costs can change abruptly during stress. However, estimating separate covariance matrices reduces sample size per regime, increasing estimation error. Shrinkage and factor structure are usually required.

## 8.13 How Covariance Cleaning Affects Portfolio Construction

Covariance cleaning changes portfolio construction through several channels.

## 8.13.1 Risk Budgeting

Risk contribution for position $i$ is:

$$
RC_i=w_i\frac{(\boldsymbol{\Sigma}\mathbf{w})_i}{\sqrt{\mathbf{w}^{\top}\boldsymbol{\Sigma}\mathbf{w}}}.
$$

If $\boldsymbol{\Sigma}$ is noisy, risk contributions are noisy. A cleaned covariance matrix stabilizes marginal risk contributions and prevents the optimizer from overallocating to positions that appear diversifying only because of sampling error.

## 8.13.2 Optimization Stability

Mean-variance optimal weights are proportional to the inverse covariance matrix:

$$
\mathbf{w}^{*}\propto\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu},
$$

subject to constraints. If $\boldsymbol{\Sigma}$ has very small noisy eigenvalues, the inverse covariance matrix contains very large values along those directions. This creates unstable long-short portfolios. Cleaning eigenvalues reduces this instability.

## 8.13.3 Leverage

Noisy covariance can understate risk in certain directions, allowing excessive leverage. Cleaning raises artificially low eigenvalues and can reduce leverage in fragile long-short trades.

## 8.13.4 Concentration

If covariance estimates incorrectly suggest that several positions diversify each other, the optimizer may concentrate in a hidden common risk factor. Cleaning and factor modeling can reduce false diversification.

## 8.13.5 Turnover

Small changes in noisy covariance estimates can cause large changes in optimized weights. Cleaning stabilizes covariance and can reduce turnover. Lower turnover is especially valuable for options because bid-ask spreads, slippage, and hedge costs can be large.

## 8.14 Limitations of Marchenko-Pastur Cleaning

Marchenko-Pastur cleaning is useful, but it has serious limitations.

## 8.14.1 Fat Tails

The classical Marchenko-Pastur result assumes finite-variance independent Gaussian-like observations. Financial returns and option P&L are fat-tailed. Extreme observations can distort eigenvalues and eigenvectors. Robust covariance estimators may be needed before or instead of RMT cleaning.

## 8.14.2 Non-Stationarity

The true covariance matrix changes through time. Marchenko-Pastur cleaning assumes a stable population covariance over the sample. If the sample mixes multiple regimes, cleaning may average incompatible states.

## 8.14.3 Autocorrelation and Stale Prices

Option marks can be stale. Stale marks create artificial autocorrelation and understated volatility. RMT cleaning does not fix bad input data.

## 8.14.4 Volatility Clustering

Returns are conditionally heteroskedastic. A calm period and a volatile period should not necessarily receive equal treatment. EWMA, GARCH-like scaling, or regime-conditioned covariance may be needed.

## 8.14.5 Regime Shifts

During crisis regimes, correlations can rise abruptly. A covariance matrix cleaned using a long calm history may still understate stress correlation.

## 8.14.6 Small Sample Sizes

When $T$ is very small, eigenstructure is unreliable. Cleaning can reduce noise but cannot create information. In small samples, factor models and stronger priors are often preferable.

## 8.14.7 Cross-Sectional Dependence and True Factors

Large eigenvalues above the MP bound may correspond to true factors, but they can also reflect temporary crowding, stale data, or common data errors. Eigenvalue significance should be interpreted with domain knowledge.

## 8.15 Covariance Estimation Method Comparison Table

| Method | Strengths | Weaknesses | Best Use |
|---|---|---|---|
| Sample covariance | Simple and transparent | Noisy, unstable, singular when $N>T$ | Baseline and diagnostics |
| EWMA covariance | Adapts to recent volatility | Still noisy; parameter-sensitive | Daily risk monitoring |
| Ledoit-Wolf shrinkage | Stable and easy to implement | Target may be too simple | General-purpose covariance stabilization |
| Constant-correlation shrinkage | Reduces pairwise noise | Can miss sector and factor structure | Broad cross-sectional portfolios |
| Factor covariance | Interpretable and scalable | Omitted-factor risk | Greek-aware risk decomposition |
| RMT eigenvalue clipping | Stabilizes noisy eigenvalues | Assumption-sensitive; keeps sample eigenvectors | High-dimensional correlation cleaning |
| Nonlinear shrinkage / RIE | More refined eigenvalue cleaning | More complex and less transparent | Advanced institutional risk systems |
| Hierarchical clustering | Avoids direct inversion; intuitive clusters | Cluster instability and tail-dependence limits | Risk budgeting and allocation |
| Regime-conditioned covariance | Captures state-dependent risk | Fewer observations per regime | Options strategies with regime-sensitive risk |
| Scenario covariance | Captures designed stress behavior | Depends on scenario design | Stress-aware portfolio construction |

## 8.16 Python Code: Marchenko-Pastur Covariance Cleaner

The following code implements a practical covariance cleaner using Marchenko-Pastur eigenvalue clipping. It is designed for research and education. A production version should include stronger data validation, robust outlier handling, missing-data policies, diagnostics, and governance.

```python
import numpy as np
import pandas as pd


def _validate_returns_frame(returns: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean a return or factor-shock DataFrame."""
    if not isinstance(returns, pd.DataFrame):
        raise TypeError("returns must be a pandas DataFrame")
    if returns.shape[0] < 5 or returns.shape[1] < 2:
        raise ValueError("returns must have at least 5 rows and 2 columns")
    x = returns.astype(float).replace([np.inf, -np.inf], np.nan).dropna(axis=0, how="any")
    if x.shape[0] < 5:
        raise ValueError("not enough complete observations after dropping missing values")
    if (x.std(axis=0) <= 0).any():
        raise ValueError("all columns must have positive standard deviation")
    return x


def correlation_from_returns(returns: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Return sample correlation and sample standard deviations."""
    x = _validate_returns_frame(returns)
    std = x.std(axis=0, ddof=1)
    corr = x.corr()
    return corr, std


def nearest_positive_semidefinite(matrix: np.ndarray, epsilon: float = 1e-10) -> np.ndarray:
    """Project a symmetric matrix to positive semidefinite by flooring eigenvalues."""
    sym = 0.5 * (matrix + matrix.T)
    eigvals, eigvecs = np.linalg.eigh(sym)
    eigvals = np.maximum(eigvals, epsilon)
    psd = eigvecs @ np.diag(eigvals) @ eigvecs.T
    return 0.5 * (psd + psd.T)


def marchenko_pastur_bounds(n_assets: int, n_obs: int, noise_variance: float = 1.0) -> tuple[float, float]:
    """Compute Marchenko-Pastur eigenvalue bounds using q = N / T.

    Parameters
    ----------
    n_assets:
        Number of variables N.
    n_obs:
        Number of observations T.
    noise_variance:
        Assumed noise variance. For correlation matrices, usually 1.0.
    """
    if n_assets <= 0 or n_obs <= 0:
        raise ValueError("n_assets and n_obs must be positive")
    q = n_assets / n_obs
    lambda_min = noise_variance * (1.0 - np.sqrt(q)) ** 2
    lambda_max = noise_variance * (1.0 + np.sqrt(q)) ** 2
    return float(lambda_min), float(lambda_max)


def rmt_clean_correlation(corr: pd.DataFrame, n_obs: int) -> pd.DataFrame:
    """Clean a correlation matrix using Marchenko-Pastur eigenvalue clipping.

    Steps
    -----
    1. Eigendecompose the sample correlation matrix.
    2. Identify eigenvalues inside the MP noise band.
    3. Replace noisy eigenvalues with their average.
    4. Reconstruct and renormalize to unit diagonal.
    """
    if corr.shape[0] != corr.shape[1]:
        raise ValueError("corr must be square")
    cols = corr.columns
    c = corr.to_numpy(dtype=float)
    c = 0.5 * (c + c.T)

    eigvals, eigvecs = np.linalg.eigh(c)
    # np.linalg.eigh returns ascending eigenvalues.
    lambda_min, lambda_max = marchenko_pastur_bounds(corr.shape[0], n_obs, noise_variance=1.0)

    noisy = eigvals <= lambda_max
    cleaned_eigvals = eigvals.copy()
    if noisy.any():
        cleaned_eigvals[noisy] = eigvals[noisy].mean()

    cleaned = eigvecs @ np.diag(cleaned_eigvals) @ eigvecs.T
    cleaned = nearest_positive_semidefinite(cleaned)

    # Renormalize to correlation.
    diag = np.sqrt(np.diag(cleaned))
    cleaned_corr = cleaned / np.outer(diag, diag)
    cleaned_corr = np.clip(cleaned_corr, -1.0, 1.0)
    np.fill_diagonal(cleaned_corr, 1.0)

    return pd.DataFrame(cleaned_corr, index=cols, columns=cols)


def covariance_from_correlation(corr: pd.DataFrame, std: pd.Series) -> pd.DataFrame:
    """Reconstruct covariance matrix from correlation and standard deviations."""
    std = std.reindex(corr.index)
    d = np.diag(std.to_numpy(dtype=float))
    cov = d @ corr.to_numpy(dtype=float) @ d
    return pd.DataFrame(cov, index=corr.index, columns=corr.columns)


def rmt_clean_covariance(returns: pd.DataFrame) -> dict[str, pd.DataFrame | tuple[float, float]]:
    """Return sample and RMT-cleaned covariance and correlation matrices."""
    x = _validate_returns_frame(returns)
    corr, std = correlation_from_returns(x)
    cleaned_corr = rmt_clean_correlation(corr, n_obs=x.shape[0])
    sample_cov = x.cov()
    cleaned_cov = covariance_from_correlation(cleaned_corr, std)
    bounds = marchenko_pastur_bounds(x.shape[1], x.shape[0])
    return {
        "sample_corr": corr,
        "cleaned_corr": cleaned_corr,
        "sample_cov": sample_cov,
        "cleaned_cov": cleaned_cov,
        "mp_bounds": bounds,
    }
```

## 8.17 Python Code: Portfolio Risk Before and After Covariance Cleaning

The following example simulates noisy correlated data, estimates sample and RMT-cleaned covariance matrices, and compares portfolio risk. The example is synthetic and is not calibrated to any live market.

```python
import numpy as np
import pandas as pd


def simulate_factor_returns(
    n_obs: int = 252,
    n_assets: int = 80,
    n_factors: int = 5,
    seed: int = 42,
) -> pd.DataFrame:
    """Simulate asset returns with a low-rank factor structure plus noise."""
    rng = np.random.default_rng(seed)
    factor_returns = rng.normal(0.0, 0.01, size=(n_obs, n_factors))
    loadings = rng.normal(0.0, 0.6, size=(n_assets, n_factors))
    idio = rng.normal(0.0, 0.015, size=(n_obs, n_assets))
    returns = factor_returns @ loadings.T + idio
    cols = [f"asset_{i:03d}" for i in range(n_assets)]
    return pd.DataFrame(returns, columns=cols)


def random_long_short_weights(n_assets: int, seed: int = 7) -> np.ndarray:
    """Create a random dollar-neutral long-short weight vector."""
    rng = np.random.default_rng(seed)
    w = rng.normal(size=n_assets)
    w = w - w.mean()
    w = w / np.sum(np.abs(w))
    return w


def portfolio_volatility(weights: np.ndarray, covariance: pd.DataFrame, annualization: int = 252) -> float:
    """Compute annualized portfolio volatility."""
    cov = covariance.to_numpy(dtype=float)
    var = float(weights @ cov @ weights)
    return float(np.sqrt(max(var, 0.0) * annualization))


returns = simulate_factor_returns(n_obs=252, n_assets=80, n_factors=5, seed=11)
cleaned = rmt_clean_covariance(returns)
weights = random_long_short_weights(returns.shape[1], seed=9)

sample_vol = portfolio_volatility(weights, cleaned["sample_cov"])
cleaned_vol = portfolio_volatility(weights, cleaned["cleaned_cov"])

print("Marchenko-Pastur bounds:", cleaned["mp_bounds"])
print("Annualized portfolio volatility using sample covariance:", round(sample_vol, 4))
print("Annualized portfolio volatility using cleaned covariance:", round(cleaned_vol, 4))

# Compare eigenvalue dispersion.
sample_eigs = np.linalg.eigvalsh(cleaned["sample_corr"].to_numpy())
cleaned_eigs = np.linalg.eigvalsh(cleaned["cleaned_corr"].to_numpy())
print("Smallest sample eigenvalues:", np.round(sample_eigs[:5], 4))
print("Smallest cleaned eigenvalues:", np.round(cleaned_eigs[:5], 4))
print("Largest sample eigenvalues:", np.round(sample_eigs[-5:], 4))
print("Largest cleaned eigenvalues:", np.round(cleaned_eigs[-5:], 4))
```

Expected interpretation:

- The cleaned covariance matrix usually has less extreme small eigenvalues.
- Portfolio volatility estimates may increase or decrease depending on whether the original weights exploited noisy low-risk directions.
- The largest eigenvalues may be preserved if they are above the Marchenko-Pastur threshold.
- Cleaning should be evaluated out of sample, not merely by in-sample smoothness.

## 8.18 Python Code: Comparing Optimized Weights Under Sample and Cleaned Covariance

The next example shows how covariance cleaning can affect optimization. It uses a simple mean-variance objective with long-short weights and no full option constraints. It is a diagnostic example, not a production optimizer.

```python
from scipy.optimize import minimize


def min_variance_weights(covariance: pd.DataFrame, gross_limit: float = 1.0) -> pd.Series:
    """Solve a simple minimum-variance portfolio with dollar-neutrality and gross limit.

    This is a stylized optimizer. It is used only to illustrate covariance
    sensitivity. Production options optimization requires Greek, margin,
    liquidity, and stress constraints.
    """
    cols = covariance.columns
    cov = covariance.to_numpy(dtype=float)
    n = len(cols)

    def objective(w: np.ndarray) -> float:
        return float(w @ cov @ w)

    constraints = [
        {"type": "eq", "fun": lambda w: np.sum(w)},  # dollar-neutral
        {"type": "ineq", "fun": lambda w: gross_limit - np.sum(np.abs(w))},
    ]
    bounds = [(-0.05, 0.05)] * n
    x0 = np.zeros(n)

    result = minimize(objective, x0=x0, method="SLSQP", bounds=bounds, constraints=constraints)
    if not result.success:
        raise RuntimeError(result.message)
    return pd.Series(result.x, index=cols)


# Add a tiny expected-return tilt to avoid the all-zero minimum if desired.
def mean_variance_weights(
    expected_returns: pd.Series,
    covariance: pd.DataFrame,
    risk_aversion: float = 10.0,
    gross_limit: float = 1.0,
) -> pd.Series:
    """Solve a simple constrained mean-variance problem."""
    cols = expected_returns.index
    cov = covariance.loc[cols, cols].to_numpy(dtype=float)
    mu = expected_returns.to_numpy(dtype=float)
    n = len(cols)

    def objective(w: np.ndarray) -> float:
        return float(-(mu @ w - 0.5 * risk_aversion * w @ cov @ w))

    constraints = [
        {"type": "eq", "fun": lambda w: np.sum(w)},
        {"type": "ineq", "fun": lambda w: gross_limit - np.sum(np.abs(w))},
    ]
    bounds = [(-0.05, 0.05)] * n
    x0 = np.zeros(n)
    result = minimize(objective, x0=x0, method="SLSQP", bounds=bounds, constraints=constraints)
    if not result.success:
        raise RuntimeError(result.message)
    return pd.Series(result.x, index=cols)


rng = np.random.default_rng(123)
expected_returns = pd.Series(rng.normal(0.0, 0.001, size=returns.shape[1]), index=returns.columns)

w_sample = mean_variance_weights(expected_returns, cleaned["sample_cov"], risk_aversion=25.0, gross_limit=1.0)
w_clean = mean_variance_weights(expected_returns, cleaned["cleaned_cov"], risk_aversion=25.0, gross_limit=1.0)

comparison = pd.DataFrame({
    "w_sample_cov": w_sample,
    "w_cleaned_cov": w_clean,
    "abs_difference": (w_sample - w_clean).abs(),
})

print("Gross sample weights:", round(w_sample.abs().sum(), 4))
print("Gross cleaned weights:", round(w_clean.abs().sum(), 4))
print("Weight turnover between solutions:", round((w_sample - w_clean).abs().sum(), 4))
print(comparison.sort_values("abs_difference", ascending=False).head(10))
```

Expected interpretation:

- Optimized weights can change materially when the covariance matrix is cleaned.
- If a strategy depends on small eigenvalue directions in the sample covariance, it may be fragile.
- Adding Greek, liquidity, turnover, and stress constraints is essential for options portfolios.

## 8.19 Python Code: Greek Factor Covariance Example

This example constructs a stylized factor covariance model for option strategy P&L using delta, vega, skew, and liquidity factors.

```python

def build_greek_factor_covariance(
    factor_returns: pd.DataFrame,
    exposures: pd.DataFrame,
    residual_var: pd.Series,
) -> pd.DataFrame:
    """Build option strategy covariance from factor covariance and exposures.

    Parameters
    ----------
    factor_returns:
        DataFrame of factor shocks, columns are factors.
    exposures:
        DataFrame with rows as strategies/options and columns as factors.
    residual_var:
        Series of residual variances indexed by strategies/options.
    """
    if not exposures.columns.equals(factor_returns.columns):
        raise ValueError("exposure columns must match factor return columns")
    if not residual_var.index.equals(exposures.index):
        raise ValueError("residual_var index must match exposures index")

    factor_cov = factor_returns.cov()
    b = exposures.to_numpy(dtype=float)
    cov = b @ factor_cov.to_numpy(dtype=float) @ b.T + np.diag(residual_var.to_numpy(dtype=float))
    return pd.DataFrame(cov, index=exposures.index, columns=exposures.index)


# Synthetic factor shocks.
rng = np.random.default_rng(202)
factor_shocks = pd.DataFrame(
    rng.normal(size=(500, 5)),
    columns=["equity_return", "atm_vol_change", "skew_change", "term_change", "liquidity_shock"],
)

# Impose stylized correlation: equity down with vol up and liquidity stress up.
factor_shocks["atm_vol_change"] = -0.6 * factor_shocks["equity_return"] + 0.8 * factor_shocks["atm_vol_change"]
factor_shocks["liquidity_shock"] = -0.4 * factor_shocks["equity_return"] + 0.9 * factor_shocks["liquidity_shock"]
factor_shocks = factor_shocks * pd.Series(
    {
        "equity_return": 0.01,
        "atm_vol_change": 0.01,
        "skew_change": 0.005,
        "term_change": 0.004,
        "liquidity_shock": 0.003,
    }
)

strategies = ["long_gamma", "short_vega", "collar", "calendar", "dispersion"]
exposures = pd.DataFrame(
    {
        "equity_return": [0.05, 0.02, 0.20, 0.03, 0.00],
        "atm_vol_change": [0.80, -0.90, 0.10, 0.50, -0.30],
        "skew_change": [0.40, -0.50, 0.35, 0.05, -0.20],
        "term_change": [0.10, -0.10, 0.05, 0.60, 0.20],
        "liquidity_shock": [-0.10, -0.60, -0.20, -0.10, -0.40],
    },
    index=strategies,
)
residual_var = pd.Series(0.0001, index=strategies)

strategy_cov = build_greek_factor_covariance(factor_shocks, exposures, residual_var)
print(strategy_cov.round(6))
```

This factor covariance is more interpretable than a raw strategy-return covariance because it explicitly identifies the drivers of co-movement.

## 8.20 Practical Workflow for Covariance Stabilization

A practical institutional workflow is:

| Step | Action | Output |
|---|---|---|
| 1 | Define risk object: option returns, P&L, or factor shocks | Clear covariance target |
| 2 | Clean input data | Valid return/shock matrix |
| 3 | Winsorize or robustly handle outliers | Reduced outlier dominance |
| 4 | Estimate sample and EWMA covariance | Baseline diagnostics |
| 5 | Estimate shrinkage covariance | Stable general-purpose estimate |
| 6 | Estimate factor covariance | Interpretable risk model |
| 7 | Apply RMT cleaning to correlation matrix | Eigenvalue stabilization |
| 8 | Build regime-conditioned covariance | State-dependent risk |
| 9 | Compare risk forecasts out of sample | Model validation |
| 10 | Test optimizer sensitivity | Stability diagnostics |
| 11 | Add stress scenario constraints | Tail-risk control |
| 12 | Monitor realized P&L residuals | Model failure detection |

## 8.21 Diagnostics for Covariance Models

A covariance model should be evaluated with diagnostics, not accepted because it looks mathematically elegant.

| Diagnostic | Question Answered |
|---|---|
| Eigenvalue spectrum | Are there near-zero or extreme eigenvalues? |
| Condition number | Is the covariance matrix numerically unstable? |
| Out-of-sample risk forecast | Does predicted volatility match realized P&L volatility? |
| Risk contribution stability | Do risk budgets change excessively across windows? |
| Optimizer turnover | Does covariance noise cause unstable trades? |
| Stress correlation | Does the model capture correlation spikes? |
| Residual covariance | Are important factors missing? |
| Regime performance | Does the model work in calm and stress regimes? |
| Tail calibration | Are extreme losses underestimated? |
| Sensitivity to window | Are results robust to lookback choices? |

The condition number is:

$$
\kappa(\boldsymbol{\Sigma})=\frac{\lambda_{\max}}{\lambda_{\min}},
$$

where $\lambda_{\max}$ and $\lambda_{\min}$ are the largest and smallest eigenvalues. A very high condition number indicates numerical instability.

## 8.22 Common Implementation Errors

| Error | Why It Is Dangerous | Better Practice |
|---|---|---|
| Using sample covariance blindly | Optimizer exploits noise | Use shrinkage, RMT, or factor models |
| Mixing return and P&L units | Risk estimates become inconsistent | Define covariance target explicitly |
| Ignoring volatility surface factors | Vega-neutral books can still have skew and term risk | Include vol level, skew, and term factors |
| Estimating covariance from stale option prices | Understates risk and creates autocorrelation | Filter stale quotes and use robust marks |
| Using calm-period covariance for stress risk | Underestimates drawdown | Use regime-conditioned and stressed covariance |
| Over-cleaning covariance | Suppresses real signals | Validate out of sample and compare alternatives |
| Assuming MP theory always applies | Fat tails and non-stationarity violate assumptions | Treat MP as a tool, not truth |
| Ignoring turnover impact | Stable-looking optimizer may trade too much | Add turnover and cost penalties |
| Ignoring jump dependence | Covariance misses discontinuous co-movement | Add jump and scenario stress tests |
| Ignoring margin covariance | Margin rises with losses in stress | Model P&L and margin jointly |

## 8.23 Summary of Part 8

Part 8 developed a covariance estimation and risk stabilization framework for options portfolios.

Key points:

1. Options covariance is more complex than equity return covariance because option P&L depends on spot, volatility, skew, term structure, correlation, liquidity, and changing Greeks.
2. Sample covariance is simple but unstable when the number of instruments or risk factors is large relative to the number of observations.
3. EWMA covariance adapts to recent volatility but remains noisy and parameter-sensitive.
4. Shrinkage estimators stabilize covariance by combining sample covariance with structured targets.
5. A Greek-aware factor covariance model can represent option P&L through underlying returns, implied-volatility changes, skew changes, term-structure changes, correlation shocks, liquidity shocks, and residual risk.
6. Marchenko-Pastur theory provides eigenvalue bounds for distinguishing noisy eigenvalues from potentially informative factors under restrictive assumptions.
7. RMT eigenvalue clipping stabilizes the correlation matrix by replacing noisy eigenvalues with a common value and reconstructing covariance with volatility estimates.
8. Rotationally invariant estimators provide more advanced eigenvalue cleaning but are more complex and still assumption-sensitive.
9. Hierarchical clustering and hierarchical risk models can reduce direct reliance on noisy inverse covariance matrices.
10. Regime-conditioned covariance is essential because option covariance changes across low-volatility, transition, stress, post-shock, and vol-of-vol regimes.
11. Covariance cleaning affects risk budgeting, optimization stability, leverage, concentration, and turnover.
12. Marchenko-Pastur cleaning has limitations under fat tails, non-stationarity, autocorrelation, volatility clustering, regime shifts, and small samples.
13. Covariance models must be validated through out-of-sample risk forecasts, optimizer stability, stress testing, residual analysis, and regime-specific diagnostics.
14. In production, covariance cleaning should be combined with Greek constraints, liquidity controls, margin stress, expected shortfall, and full repricing scenarios.

The next installment will cover Part 9: Risk Management, Stress Testing, and Failure Modes, including Greek limits, drawdown limits, margin limits, liquidity limits, nonlinear risk under large moves, gap risk, vol-of-vol risk, correlation breakdown, crowded unwind, early assignment, full repricing versus Taylor approximation, and portfolio stress-testing code.
