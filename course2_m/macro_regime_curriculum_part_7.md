# Institutional Macro-Regime Detection, Multi-Asset Signal Identification, and Statistical Validation Curriculum

## Installment 7: Part 7 - Statistical Validation, Inference, and Robustness Testing

**Scope of this installment.** This installment continues the curriculum with **Part 7 only**. It assumes the global assumptions, timestamp conventions, feature engineering framework, return-target definitions, regime-detection concepts, causal-channel framework, and signal-scoring framework established in Installments 1 through 6.

**Educational boundary.** This document is for research education, model design, and institutional portfolio-process development. It is not personalized investment advice, a live trading recommendation, or a guarantee of alpha.

---

# Part 7: Statistical Validation, Inference, and Robustness Testing

## 7.1 Purpose of Statistical Validation

Statistical validation is the discipline that separates a plausible macro signal from a reliable research input. In macro-regime and multi-asset forecasting, false discoveries are common because samples are short, targets overlap, regimes are unstable, and researchers can test many indicators, transformations, assets, horizons, and portfolio rules. Validation therefore asks a stricter question than: "Did the signal work historically?" It asks:

$$
\text{Would this signal, model, or regime process have been useful under realistic information, estimation, cost, and governance constraints?}
$$

Let $Y_{i,t,h}$ be a forward target for asset $i$ at timestamp $t$ and horizon $h$, and let $\hat Y_{i,t,h}$ be a forecast produced using only $\mathcal{F}_t$. A validation framework evaluates the forecast relationship:

$$
Y_{i,t,h}=\hat Y_{i,t,h}+e_{i,t,h},
$$

where $e_{i,t,h}$ is the forecast error. The validation process studies the distribution, dependence, stability, calibration, economic usefulness, and failure modes of $e_{i,t,h}$ and of the investment decisions derived from $\hat Y_{i,t,h}$.

A signal is not validated merely because an in-sample coefficient has a low p-value. For institutional macro research, validation must address:

1. Point-in-time availability.
2. Out-of-sample performance.
3. Walk-forward estimation.
4. Overlapping return inference.
5. Multiple-testing risk.
6. Forecast calibration.
7. Regime and subperiod stability.
8. Economic significance after risk, turnover, costs, and constraints.
9. Model governance and reproducibility.

## 7.2 Validation Philosophy: Evidence Stack Rather Than Single Statistic

No single statistic is sufficient. A model with a strong information coefficient may be untradable because of turnover. A model with a high hit rate may have rare but severe left-tail losses. A model with high in-sample $R^2$ may fail out of sample. A model with good average performance may fail in crisis regimes where risk control matters most.

A robust validation process therefore builds an evidence stack:

| Evidence Layer | Question | Typical Diagnostics |
|---|---|---|
| Data integrity | Was all information available at $t$? | Timestamp audit, vintage check, target tail missingness. |
| Statistical association | Is there predictive relation? | IC, rank IC, regression coefficient, hit rate, spread. |
| Robust inference | Are errors and p-values credible? | Newey-West, block bootstrap, clustered errors. |
| Out-of-sample validation | Did the model work without refitting to the future? | Walk-forward forecasts, OOS $R^2$, live-style backtest. |
| Calibration | Are probabilities and uncertainty estimates reliable? | Brier score, reliability curve, calibration error. |
| Stability | Does evidence persist across contexts? | Subperiod, regime, geography, asset-class, stress tests. |
| Economic significance | Is the signal investable? | Net spread, turnover, drawdown, capacity, cost sensitivity. |
| Multiple-testing control | Could this be data-mined? | FDR, Reality Check, SPA, deflated Sharpe. |
| Governance | Can the research be reproduced and monitored? | Run manifest, model registry, data version, validation report. |

The practical standard is not perfection. Macro signals are noisy. The standard is that evidence should be coherent, realistic, and robust enough to justify the signal's role: research candidate, monitor-only, low-weight input, production input, or retired model.

## 7.3 In-Sample, Out-of-Sample, and Pseudo-Real-Time Testing

### 7.3.1 In-Sample Testing

In-sample testing estimates and evaluates a model on the same historical sample. For a regression model:

$$
Y_{t,h}=\alpha_h+\beta_h^\top X_t+\varepsilon_{t,h},
$$

in-sample testing estimates $\hat\alpha_h$ and $\hat\beta_h$ using all available observations and evaluates fitted values on the same sample. In-sample analysis is useful for exploratory understanding, sign checks, residual analysis, and economic interpretation. It is not sufficient for model approval.

### 7.3.2 Out-of-Sample Testing

Out-of-sample testing estimates the model on a training period and evaluates it on a separate future period. If the training sample ends at $T_0$, then for $t>T_0$:

$$
\hat Y_{t,h}=\hat\alpha_{T_0,h}+\hat\beta_{T_0,h}^{\top}X_t,
$$

where $\hat\alpha_{T_0,h}$ and $\hat\beta_{T_0,h}$ were estimated without observing $Y_{t,h}$ or any future data. This is closer to real investment use.

### 7.3.3 Pseudo-Real-Time Testing

Pseudo-real-time testing recreates the historical forecasting process using only information that would have been available at each timestamp. It requires:

1. Point-in-time macro vintages or conservative publication lags.
2. Expanding or rolling model estimation.
3. Historical-only scaling, feature selection, PCA, and ranking.
4. Realistic universe membership at $t$.
5. Rebalancing and execution conventions.
6. Cost and turnover assumptions where portfolio outputs are evaluated.

Pseudo-real-time validation is usually the minimum standard for a production macro signal.

## 7.4 Expanding-Window and Rolling-Window Validation

### 7.4.1 Expanding Window

An expanding-window estimator uses all historical observations available up to time $t$:

$$
\hat\theta_t^{exp}=\arg\min_{\theta}\sum_{s=t_0}^{t}L(Y_{s,h},f(X_s;\theta)),
$$

where $L(\cdot)$ is a loss function and $f(\cdot)$ is the forecasting model. The forecast for $t+1$ or a forward target beginning after $t$ is then produced using $\hat\theta_t^{exp}$.

**Strength.** Uses the maximum amount of data, which is important for monthly macro samples.

**Weakness.** Old regimes and outdated policy relationships may dominate estimates.

### 7.4.2 Rolling Window

A rolling-window estimator uses only the most recent $W$ observations:

$$
\hat\theta_t^{roll}=\arg\min_{\theta}\sum_{s=t-W+1}^{t}L(Y_{s,h},f(X_s;\theta)).
$$

**Strength.** Adapts to structural change.

**Weakness.** Parameter estimates are noisier because the sample is smaller.

### 7.4.3 Choosing the Window

The window should reflect a trade-off between parameter stability and regime relevance. For monthly data, common minimum windows may range from 60 to 120 months, depending on model complexity. A 20-feature model with 72 observations is usually fragile. A two-feature model with 120 observations may be more defensible.

| Window Type | Best Use | Main Risk |
|---|---|---|
| Expanding | Stable relationships and small samples. | Structural-break contamination. |
| Rolling | Changing relationships and regime shifts. | Noisy estimates and window mining. |
| Hybrid | Expanding baseline with rolling overlay. | Added governance complexity. |
| Bayesian updating | Prior plus new evidence. | Prior sensitivity. |

## 7.5 Walk-Forward Validation

Walk-forward validation simulates repeated real-time model use. At each decision timestamp $t$, the researcher fits all preprocessing and model steps using only training data, generates a forecast, records the realized target later, and then moves forward.

A generic walk-forward algorithm is:

1. Select initial training length $T_{train}$.
2. For each decision timestamp $t=T_{train},\ldots,T-h$:
   1. Build features using only information available at $t$.
   2. Fit scalers, PCA, feature selection, regime models, and predictive models using only data up to $t$.
   3. Generate forecasts $\hat Y_{i,t,h}$.
   4. Store forecasts and metadata.
   5. After the forward window is realized, compare $\hat Y_{i,t,h}$ with $Y_{i,t,h}$.
3. Evaluate performance using forecast, signal, risk, and portfolio metrics.

The key principle is:

$$
\hat Y_{i,t,h}=f_t(X_{i,t}),
\qquad f_t \text{ is estimated without data after } t.
$$

If feature selection, standardization, PCA, hyperparameter tuning, model selection, or regime labeling uses data after $t$, the validation is contaminated.

## 7.6 Time-Series Cross-Validation for Monthly Macro Data

Standard random k-fold cross-validation is usually invalid for macro time series because it mixes future information into training folds and ignores serial dependence. Time-series cross-validation preserves order.

### 7.6.1 Expanding Split

An expanding split uses folds such as:

| Fold | Training Period | Test Period |
|---:|---|---|
| 1 | 2000-2009 | 2010 |
| 2 | 2000-2010 | 2011 |
| 3 | 2000-2011 | 2012 |
| 4 | 2000-2012 | 2013 |

### 7.6.2 Rolling Split

A rolling split uses fixed-length training windows:

| Fold | Training Period | Test Period |
|---:|---|---|
| 1 | 2000-2009 | 2010 |
| 2 | 2001-2010 | 2011 |
| 3 | 2002-2011 | 2012 |
| 4 | 2003-2012 | 2013 |

### 7.6.3 Nested Time-Series Validation

Nested validation is required when hyperparameters are tuned. The outer loop estimates out-of-sample performance. The inner loop selects hyperparameters using only the outer training sample.

$$
\lambda_t^*=\arg\min_{\lambda\in\Lambda}\mathrm{CVLoss}_{train(t)}(\lambda),
$$

where $\lambda$ is a hyperparameter such as ridge penalty, lasso penalty, number of trees, number of regimes, or PCA dimension. The selected $\lambda_t^*$ is then used to fit the model and forecast the outer test period.

## 7.7 Purging and Embargoing for Monthly Horizon Data

When targets overlap, training observations near the test observation may contain future return information that overlaps with the test target. This is especially relevant for $t+3$ and $t+12$ forward returns.

Let the test observation at timestamp $t$ have target window:

$$
\mathcal{T}_{test}(t,h)=\{t+1,t+2,\ldots,t+h\}.
$$

A training observation at timestamp $s$ has target window:

$$
\mathcal{T}_{train}(s,h)=\{s+1,s+2,\ldots,s+h\}.
$$

The observation $s$ should be purged from the training set if:

$$
\mathcal{T}_{train}(s,h)\cap\mathcal{T}_{test}(t,h)\neq\emptyset.
$$

An embargo removes observations immediately after the test period to reduce leakage through serial dependence or delayed labels. If the embargo length is $E$, training observations with timestamps in:

$$
\{t+1,t+2,\ldots,t+h+E\}
$$

are excluded when relevant to the validation design.

For simple chronological walk-forward forecasting, purging is often naturally satisfied because training data ends at or before $t$. For cross-validation folds that test blocks within history, purging and embargoing are important.

## 7.8 Overlapping Returns and Dependence

For horizon $h>1$, forward returns overlap. The $t+12$ return and the $(t+1)+12$ return share 11 monthly returns. This induces serial correlation in targets, residuals, signal spreads, and performance metrics.

If a regression is:

$$
Y_{t,h}=\alpha_h+\beta_h x_t+\varepsilon_{t,h},
$$

then for overlapping $Y_{t,h}$, the residuals $\varepsilon_{t,h}$ are generally autocorrelated. Naive OLS standard errors assume:

$$
\mathrm{Cov}(\varepsilon_t,\varepsilon_{t-k})=0 \quad \text{for } k\neq 0,
$$

which is often false. The consequence is that naive t-statistics may be overstated.

A practical minimum is to use heteroskedasticity-and-autocorrelation-consistent standard errors such as Newey-West with lag at least $h-1$:

$$
L_{NW}\geq h-1.
$$

This is a rule of thumb. Longer lags may be needed if signal and residual persistence extends beyond the target overlap.

## 7.9 Newey-West Adjusted t-Statistic

Let $\hat\beta$ be an estimated coefficient from a predictive regression. The Newey-West adjusted t-statistic is:

$$
t_{NW}=\frac{\hat\beta}{\sqrt{\widehat{\mathrm{Var}}_{NW}(\hat\beta)}}.
$$

For a sample moment $g_t$, the Newey-West long-run variance estimator is:

$$
\hat\Omega_{NW}=\hat\Gamma_0+\sum_{\ell=1}^{L}w_\ell(\hat\Gamma_\ell+\hat\Gamma_\ell^\top),
$$

where $L$ is the lag truncation parameter, $w_\ell=1-\ell/(L+1)$ is the Bartlett kernel weight, and $\hat\Gamma_\ell$ is the lag-$\ell$ autocovariance of the moment condition. In regression form, this produces a HAC covariance matrix for coefficients.

**Interpretation.** Newey-West does not fix a bad model or make overlapping returns independent. It adjusts standard errors to reflect heteroskedasticity and autocorrelation under assumptions.

## 7.10 Block Bootstrap and Stationary Bootstrap

Bootstrap methods estimate uncertainty by resampling blocks of observations rather than individual months. This preserves some serial dependence.

### 7.10.1 Moving Block Bootstrap

Given a time series $z_1,\ldots,z_T$, define overlapping blocks of length $b$:

$$
B_j=(z_j,z_{j+1},\ldots,z_{j+b-1}),
\qquad j=1,\ldots,T-b+1.
$$

A bootstrap sample is created by sampling blocks with replacement and concatenating them until length $T$ is reached. For statistic $\hat\theta$, repeat $B$ times to obtain bootstrap estimates:

$$
\hat\theta^{*(1)},\ldots,\hat\theta^{*(B)}.
$$

A percentile confidence interval is:

$$
CI_{1-\alpha}=\left[Q_{\alpha/2}(\hat\theta^*),Q_{1-\alpha/2}(\hat\theta^*)\right],
$$

where $Q_p$ is the $p$-quantile of the bootstrap distribution.

### 7.10.2 Stationary Bootstrap

The stationary bootstrap samples blocks with random lengths. A new block begins with probability $p$, so the expected block length is:

$$
\mathbb{E}[b]=\frac{1}{p}.
$$

This avoids fixed block boundaries and can better mimic stationary dependent data.

**Practical guidance.** For monthly overlapping returns, block length should reflect the horizon and the persistence of the signal. A $t+12$ target generally requires longer blocks than a $t+1$ target.

## 7.11 t-Statistics, p-Values, Confidence Intervals, and Economic Significance

A statistical test often begins with:

$$
H_0:\theta=0,
\qquad H_A:\theta\neq 0,
$$

where $\theta$ may be a regression coefficient, mean IC, mean spread, or forecast improvement. The p-value is:

$$
p=\Pr(|T|\geq |t_{obs}|\mid H_0),
$$

where $T$ is the test statistic under the null and $t_{obs}$ is the observed statistic.

A confidence interval for $\theta$ is:

$$
\hat\theta\pm c_{1-\alpha/2}\cdot \widehat{SE}(\hat\theta),
$$

where $c_{1-\alpha/2}$ is a critical value and $\widehat{SE}$ is a standard error estimator. With autocorrelation or non-normality, bootstrap intervals may be more appropriate.

### 7.11.1 Statistical Versus Economic Significance

A signal can be statistically significant but economically irrelevant if:

1. The predicted return is too small relative to transaction costs.
2. The signal requires high turnover.
3. The capacity is low.
4. The drawdown profile is unacceptable.
5. The signal loads on unwanted beta, duration, FX, or liquidity exposure.
6. The signal only works in periods that are hard to identify in real time.

Economic significance should be measured using net performance, risk contribution, drawdown behavior, turnover, cost sensitivity, capital usage, and marginal contribution to portfolio objectives.

## 7.12 Bayesian Credible Intervals

In Bayesian validation, parameters are random variables with posterior distributions. If $\theta$ is a signal coefficient, the posterior is:

$$
p(\theta\mid\mathcal{D})\propto p(\mathcal{D}\mid\theta)p(\theta),
$$

where $p(\mathcal{D}\mid\theta)$ is the likelihood and $p(\theta)$ is the prior. A $(1-\alpha)$ credible interval $[a,b]$ satisfies:

$$
\Pr(a\leq \theta \leq b\mid\mathcal{D})=1-\alpha.
$$

Unlike a frequentist confidence interval, a credible interval directly represents posterior probability under the chosen prior and likelihood. It is useful for communicating parameter uncertainty, but it depends on the model specification and prior assumptions.

## 7.13 Forecast Accuracy and Out-of-Sample R-Squared

For point forecasts, define forecast error:

$$
e_{t,h}=Y_{t,h}-\hat Y_{t,h}.
$$

Mean squared error is:

$$
MSE_h=\frac{1}{T}\sum_{t=1}^{T}(Y_{t,h}-\hat Y_{t,h})^2.
$$

Mean absolute error is:

$$
MAE_h=\frac{1}{T}\sum_{t=1}^{T}|Y_{t,h}-\hat Y_{t,h}|.
$$

Out-of-sample $R^2$ relative to benchmark forecast $\hat Y^0_{t,h}$ is:

$$
R^2_{OOS,h}=1-
\frac{\sum_{t}(Y_{t,h}-\hat Y_{t,h})^2}
{\sum_{t}(Y_{t,h}-\hat Y^0_{t,h})^2}.
$$

A positive $R^2_{OOS}$ means the model reduces squared forecast error relative to the benchmark. A negative value means the benchmark forecast is better.

**Important caution.** For asset returns, $R^2_{OOS}$ may be small even for economically useful signals. A signal can have low forecast $R^2$ but still improve ranking, risk control, or portfolio tilts.

## 7.14 Information Coefficient Inference

For cross-sectional ranking, the rank information coefficient at date $t$ is:

$$
RIC_{t,h}=\mathrm{corr}_{Spearman}(s_{i,t},Y_{i,t,h})_{i\in\mathcal{U}_t}.
$$

The mean rank IC is:

$$
\overline{RIC}_h=\frac{1}{T}\sum_{t=1}^{T}RIC_{t,h}.
$$

A naive t-statistic is:

$$
t_{RIC}=\frac{\overline{RIC}_h}{\hat\sigma(RIC)/\sqrt{T}},
$$

where $\hat\sigma(RIC)$ is the sample standard deviation of the IC series. If $RIC_{t,h}$ is autocorrelated because of overlapping returns or persistent signals, the standard error should be HAC or bootstrap-adjusted.

For time-series IC on one asset:

$$
IC_{i,h}=\mathrm{corr}(s_{i,t},Y_{i,t,h})_{t=1}^{T}.
$$

For a panel of assets, inference must consider both time-series dependence and cross-sectional dependence.

## 7.15 Hit Rate, Long-Short Spread, and Directional Validation

### 7.15.1 Hit Rate

For forecast $\hat Y_{i,t,h}$ and realized target $Y_{i,t,h}$, the hit indicator is:

$$
H_{i,t,h}=\mathbf{1}\{\mathrm{sign}(\hat Y_{i,t,h})=\mathrm{sign}(Y_{i,t,h})\}.
$$

The hit rate is:

$$
\mathrm{HitRate}_h=\frac{1}{N}\sum_{i,t}H_{i,t,h}.
$$

A binomial test can compare hit rate to 50%, but independence assumptions are often violated in macro data. Block bootstrap is usually more realistic.

### 7.15.2 Long-Short Spread

For a cross-sectional signal, define top and bottom groups $Q_t^{Top}$ and $Q_t^{Bottom}$. The long-short spread is:

$$
LS_{t,h}=\frac{1}{|Q_t^{Top}|}\sum_{i\in Q_t^{Top}}Y_{i,t,h}
-
\frac{1}{|Q_t^{Bottom}|}\sum_{i\in Q_t^{Bottom}}Y_{i,t,h}.
$$

The average spread is:

$$
\overline{LS}_h=\frac{1}{T}\sum_{t=1}^{T}LS_{t,h}.
$$

The t-statistic should account for serial dependence:

$$
t_{LS,NW}=\frac{\overline{LS}_h}{\widehat{SE}_{NW}(\overline{LS}_h)}.
$$

A long-short spread is closer to an implementable signal test than an IC, but it is still not a complete portfolio backtest unless it includes turnover, costs, financing, shorting constraints, leverage, capacity, and risk controls.

## 7.16 Diebold-Mariano Forecast Comparison

The Diebold-Mariano test compares predictive accuracy of two forecasts. Let $e_{1,t}$ and $e_{2,t}$ be forecast errors from models 1 and 2. Define loss differential:

$$
d_t=L(e_{1,t})-L(e_{2,t}),
$$

where $L(e)=e^2$ for squared-error loss or $L(e)=|e|$ for absolute-error loss. The null hypothesis is equal predictive accuracy:

$$
H_0:\mathbb{E}[d_t]=0.
$$

The Diebold-Mariano statistic is:

$$
DM=\frac{\bar d}{\sqrt{\widehat{\mathrm{LRV}}(d_t)/T}},
$$

where $\bar d$ is the sample mean loss differential and $\widehat{\mathrm{LRV}}(d_t)$ is a long-run variance estimate, often Newey-West adjusted.

**Interpretation.** If $DM<0$ under squared-error loss defined as model loss minus benchmark loss, model 1 has lower average loss than model 2. The sign convention must be stated.

## 7.17 Probability Forecast Calibration

For probability forecasts, accuracy is not only about ranking. A model that predicts 70% probability should realize the event approximately 70% of the time among comparable observations.

Let $\hat p_t$ be the forecast probability of event $D_t=1$. The Brier score is:

$$
\mathrm{Brier}=\frac{1}{T}\sum_{t=1}^{T}(D_t-\hat p_t)^2.
$$

Calibration error can be estimated by grouping predictions into $B$ bins. Let $\mathcal{B}_b$ be bin $b$. The expected calibration error is:

$$
ECE=\sum_{b=1}^{B}\frac{|\mathcal{B}_b|}{T}
\left|
\frac{1}{|\mathcal{B}_b|}\sum_{t\in\mathcal{B}_b}D_t
-
\frac{1}{|\mathcal{B}_b|}\sum_{t\in\mathcal{B}_b}\hat p_t
\right|.
$$

The log loss is:

$$
\mathrm{LogLoss}= -\frac{1}{T}\sum_{t=1}^{T}
\left[D_t\log(\hat p_t)+(1-D_t)\log(1-\hat p_t)\right].
$$

Probability models for macro returns should be evaluated with both discrimination and calibration metrics. A model can rank high-risk months correctly but still produce probabilities that are too extreme.

## 7.18 Multiple Testing and False Discovery Risk

Macro signal research creates a large multiple-testing problem. Suppose a researcher tests:

$$
N_{tests}=N_{features}\times N_{transformations}\times N_{assets}\times N_{horizons}\times N_{model\ choices}.
$$

Even if every signal has no true predictive power, some will look significant by chance. If 1,000 independent null hypotheses are tested at the 5% level, about 50 false positives are expected.

### 7.18.1 Bonferroni Correction

The Bonferroni method tests each p-value against:

$$
\alpha^*=\frac{\alpha}{M},
$$

where $M$ is the number of tests. It controls family-wise error rate but can be overly conservative when tests are correlated.

### 7.18.2 False Discovery Rate

The Benjamini-Hochberg false discovery rate procedure sorts p-values:

$$
p_{(1)}\leq p_{(2)}\leq \cdots \leq p_{(M)}.
$$

Find the largest $k$ such that:

$$
p_{(k)}\leq \frac{k}{M}q,
$$

where $q$ is the desired false discovery rate. Reject hypotheses $1,\ldots,k$.

FDR control is often more appropriate than Bonferroni for exploratory signal libraries, but it still requires honest accounting of tested hypotheses.

## 7.19 White's Reality Check and Superior Predictive Ability Test

White's Reality Check addresses data snooping when selecting the best model from many candidates. Let $f_{m,t}$ be the performance differential of model $m$ versus a benchmark at time $t$. The null is that no candidate model has positive expected performance:

$$
H_0:\max_{m=1,\ldots,M}\mathbb{E}[f_{m,t}]\leq 0.
$$

The test statistic is:

$$
T_{RC}=\max_m \sqrt{T}\,\bar f_m,
$$

where $\bar f_m$ is the average performance differential. Bootstrap methods approximate the distribution of $T_{RC}$ under the null.

The Superior Predictive Ability, or SPA, test refines this idea by reducing the influence of clearly poor models. It tests whether the best model is significantly better than the benchmark after accounting for the search over candidate models.

**Practical interpretation.** These tests are useful when a research process has selected the best signal from many alternatives. They are not a substitute for economic rationale and out-of-sample validation.

## 7.20 Deflated Sharpe Ratio

The deflated Sharpe ratio adjusts a Sharpe ratio for non-normal returns and multiple trials. Let $\widehat{SR}$ be the observed Sharpe ratio, $SR^*$ be a benchmark Sharpe threshold that accounts for selection across trials, $T$ be sample size, $\hat\gamma_3$ be skewness, and $\hat\gamma_4$ be kurtosis. A stylized deflated Sharpe statistic is:

$$
DSR=\Phi\left(
\frac{(\widehat{SR}-SR^*)\sqrt{T-1}}
{\sqrt{1-\hat\gamma_3\widehat{SR}+\frac{\hat\gamma_4-1}{4}\widehat{SR}^2}}
\right),
$$

where $\Phi$ is the standard normal CDF. The threshold $SR^*$ increases with the number of trials and the distribution of candidate Sharpe ratios.

**Interpretation.** A high raw Sharpe ratio is less impressive when many variants were tried, returns are negatively skewed, or returns have fat tails. This is especially relevant for carry, short-volatility, credit, and levered alternative risk premia.

## 7.21 Regime-Stratified and Stress-Period Validation

A macro signal should be evaluated across regimes. Let $\pi_{k,t}$ be the probability of regime $k$. A regime-weighted mean spread is:

$$
\overline{LS}_{k,h}=\frac{\sum_t \pi_{k,t}LS_{t,h}}{\sum_t \pi_{k,t}}.
$$

A regime-weighted IC can be similarly computed:

$$
\overline{IC}_{k,h}=\frac{\sum_t \pi_{k,t}IC_{t,h}}{\sum_t \pi_{k,t}}.
$$

Stress-period validation asks whether the signal behaves acceptably during crisis periods, inflation shocks, liquidity shocks, volatility spikes, policy pivots, credit stress, and currency crises. A signal does not need to work in every regime, but its failure modes must be known and managed.

## 7.22 Stability Across Subperiods, Asset Classes, Geographies, and Horizons

Validation should report stability slices:

| Slice | Question | Example Diagnostic |
|---|---|---|
| Subperiod | Does the signal work across decades or cycles? | IC by decade, pre/post crisis. |
| Regime | Does efficacy depend on state? | IC by macro regime probability. |
| Asset class | Is it broad or concentrated? | Equity, rates, credit, FX, commodity IC. |
| Geography | Does it work across regions? | US, Europe, Japan, EM. |
| Horizon | Does it decay logically? | $t+1$, $t+3$, $t+12$ IC table. |
| Stress | Does it fail in critical periods? | Crisis drawdown and tail loss. |
| Implementation | Does cost erase value? | Net spread after turnover and costs. |

A signal that works only in one asset class and one historical regime may still be useful, but its role should be narrow and its confidence score should reflect that concentration.

## 7.23 Portfolio Backtest Validation

Signal validation and portfolio validation are related but different. A signal can rank assets well but still produce poor portfolio performance because of covariance, constraints, turnover, or cost.

A portfolio return is:

$$
R_{p,t+1}=w_t^\top r_{t+1}-\mathrm{TC}(w_t,w_{t-1}),
$$

where $w_t$ is the vector of weights selected at $t$, $r_{t+1}$ is next-month asset return, and $\mathrm{TC}$ is transaction cost.

Portfolio validation should include:

1. Gross and net returns.
2. Volatility and drawdown.
3. Turnover and cost sensitivity.
4. Exposure decomposition by beta, duration, FX, credit, commodity, volatility, and liquidity.
5. Regime-conditional performance.
6. Tail behavior and expected shortfall.
7. Capacity and liquidity assumptions.
8. Benchmark-relative active risk.

A backtest is not a validation endpoint unless it is point-in-time, cost-aware, and benchmarked against simple alternatives.

## 7.24 Validation Report Structure

An institutional validation report should be standardized.

| Section | Required Content |
|---|---|
| Model description | Signal, features, target, horizon, universe, rationale. |
| Data audit | Sources, timestamps, lags, vintages, universe rules. |
| Methodology | Transformations, model, estimation, validation design. |
| In-sample diagnostics | Coefficients, IC, spreads, residuals, monotonicity. |
| Out-of-sample diagnostics | Walk-forward performance and benchmark comparisons. |
| Inference | Newey-West, bootstrap, clustered errors, p-values, intervals. |
| Multiple testing | Number of variants, FDR, Reality Check or DSR if applicable. |
| Stability | Subperiod, regime, geography, asset-class, stress diagnostics. |
| Economic significance | Net performance, costs, turnover, drawdown, capacity. |
| Failure modes | Known weaknesses and risk controls. |
| Recommendation | Research, monitor, low-weight, production, or retire. |
| Monitoring plan | Live decay, data anomalies, model drift, review frequency. |

## 7.25 Python: Robust Validation Toolkit

The following code provides reusable functions for forecast validation, Newey-West inference, block bootstrap confidence intervals, Diebold-Mariano comparison, FDR adjustment, and probability calibration. The code is designed for monthly macro and multi-asset research and assumes the data have already been aligned without look-ahead bias.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Sequence

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn.metrics import brier_score_loss, log_loss, mean_absolute_error, mean_squared_error


@dataclass(frozen=True)
class ValidationConfig:
    """Configuration for monthly validation diagnostics."""

    horizon: int = 1
    nw_lags: int | None = None
    min_obs: int = 36
    bootstrap_samples: int = 2000
    block_length: int | None = None
    random_state: int = 42

    def resolved_nw_lags(self) -> int:
        if self.nw_lags is not None:
            return self.nw_lags
        return max(0, self.horizon - 1)

    def resolved_block_length(self) -> int:
        if self.block_length is not None:
            return self.block_length
        return max(3, self.horizon)


def clean_xy(y: pd.Series, x: pd.DataFrame | pd.Series) -> tuple[pd.Series, pd.DataFrame]:
    """Align and clean target and features."""
    if isinstance(x, pd.Series):
        x = x.to_frame("x")
    df = pd.concat([y.rename("target"), x], axis=1)
    df = df.replace([np.inf, -np.inf], np.nan).dropna().astype(float)
    return df["target"], df.drop(columns="target")


def hac_regression(y: pd.Series, x: pd.DataFrame | pd.Series, config: ValidationConfig):
    """Fit OLS with Newey-West/HAC covariance."""
    y_clean, x_clean = clean_xy(y, x)
    if len(y_clean) < config.min_obs:
        raise ValueError("Insufficient observations for HAC regression.")
    X = sm.add_constant(x_clean, has_constant="add")
    model = sm.OLS(y_clean, X).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": config.resolved_nw_lags()},
    )
    return model


def mean_with_hac_tstat(series: pd.Series, config: ValidationConfig) -> dict[str, float]:
    """Estimate mean and HAC-adjusted t-statistic for a time series."""
    s = series.replace([np.inf, -np.inf], np.nan).dropna().astype(float)
    if len(s) < config.min_obs:
        return {"mean": np.nan, "se_hac": np.nan, "t_hac": np.nan, "nobs": len(s)}
    y = s
    X = pd.DataFrame({"intercept_only": np.ones(len(y))}, index=y.index)
    model = sm.OLS(y, X).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": config.resolved_nw_lags()},
    )
    return {
        "mean": float(model.params["intercept_only"]),
        "se_hac": float(model.bse["intercept_only"]),
        "t_hac": float(model.tvalues["intercept_only"]),
        "p_value": float(model.pvalues["intercept_only"]),
        "nobs": int(model.nobs),
    }
```

## 7.26 Python: Block Bootstrap Inference for IC or Spread

```python
def moving_block_bootstrap_indices(
    n: int,
    block_length: int,
    n_samples: int,
    rng: np.random.Generator,
) -> list[np.ndarray]:
    """Generate moving-block bootstrap index arrays."""
    if n <= 1:
        raise ValueError("n must be greater than 1.")
    if not 1 <= block_length <= n:
        raise ValueError("block_length must be between 1 and n.")

    starts = np.arange(0, n - block_length + 1)
    out = []
    for _ in range(n_samples):
        pieces = []
        while sum(len(p) for p in pieces) < n:
            start = rng.choice(starts)
            pieces.append(np.arange(start, start + block_length))
        idx = np.concatenate(pieces)[:n]
        out.append(idx)
    return out


def block_bootstrap_ci(
    series: pd.Series,
    statistic: Callable[[np.ndarray], float] = np.mean,
    config: ValidationConfig = ValidationConfig(),
    alpha: float = 0.05,
) -> dict[str, float]:
    """Compute moving-block bootstrap confidence interval for a statistic."""
    s = series.replace([np.inf, -np.inf], np.nan).dropna().astype(float).to_numpy()
    if len(s) < config.min_obs:
        return {"estimate": np.nan, "ci_low": np.nan, "ci_high": np.nan, "nobs": len(s)}

    rng = np.random.default_rng(config.random_state)
    idxs = moving_block_bootstrap_indices(
        n=len(s),
        block_length=config.resolved_block_length(),
        n_samples=config.bootstrap_samples,
        rng=rng,
    )
    boot = np.array([statistic(s[idx]) for idx in idxs], dtype=float)
    return {
        "estimate": float(statistic(s)),
        "ci_low": float(np.nanquantile(boot, alpha / 2)),
        "ci_high": float(np.nanquantile(boot, 1 - alpha / 2)),
        "bootstrap_std": float(np.nanstd(boot, ddof=1)),
        "nobs": int(len(s)),
    }
```

## 7.27 Python: Forecast Accuracy and Diebold-Mariano Test

```python
def forecast_accuracy_report(
    actual: pd.Series,
    forecast: pd.Series,
    benchmark: pd.Series | float = 0.0,
) -> dict[str, float]:
    """Compute point forecast accuracy metrics."""
    df = pd.concat([actual.rename("actual"), forecast.rename("forecast")], axis=1)
    if isinstance(benchmark, pd.Series):
        df["benchmark"] = benchmark
    else:
        df["benchmark"] = float(benchmark)
    df = df.replace([np.inf, -np.inf], np.nan).dropna().astype(float)
    if df.empty:
        raise ValueError("No valid observations.")

    mse_model = mean_squared_error(df["actual"], df["forecast"])
    mse_bench = mean_squared_error(df["actual"], df["benchmark"])
    return {
        "mse": float(mse_model),
        "mae": float(mean_absolute_error(df["actual"], df["forecast"])),
        "rmse": float(np.sqrt(mse_model)),
        "oos_r2": float(1.0 - mse_model / mse_bench) if mse_bench > 0 else np.nan,
        "corr": float(df["actual"].corr(df["forecast"])),
        "sign_hit_rate": float((np.sign(df["actual"]) == np.sign(df["forecast"])).mean()),
        "nobs": int(len(df)),
    }


def diebold_mariano_test(
    actual: pd.Series,
    forecast_1: pd.Series,
    forecast_2: pd.Series,
    horizon: int = 1,
    loss: str = "squared",
) -> dict[str, float]:
    """Diebold-Mariano test using HAC variance for loss differential.

    The loss differential is loss(model 1) - loss(model 2). A negative mean
    means model 1 has lower average loss.
    """
    df = pd.concat(
        [actual.rename("actual"), forecast_1.rename("f1"), forecast_2.rename("f2")],
        axis=1,
    ).replace([np.inf, -np.inf], np.nan).dropna().astype(float)
    if len(df) < max(24, horizon + 5):
        raise ValueError("Insufficient observations for Diebold-Mariano test.")

    e1 = df["actual"] - df["f1"]
    e2 = df["actual"] - df["f2"]
    if loss == "squared":
        d = e1**2 - e2**2
    elif loss == "absolute":
        d = e1.abs() - e2.abs()
    else:
        raise ValueError("loss must be 'squared' or 'absolute'.")

    cfg = ValidationConfig(horizon=horizon, nw_lags=max(horizon - 1, 0), min_obs=24)
    stats_mean = mean_with_hac_tstat(d, cfg)
    return {
        "mean_loss_diff_f1_minus_f2": stats_mean["mean"],
        "dm_stat": stats_mean["t_hac"],
        "p_value": stats_mean["p_value"],
        "nobs": stats_mean["nobs"],
    }
```

## 7.28 Python: FDR, Calibration, and Reliability Diagnostics

```python
def benjamini_hochberg_fdr(pvalues: pd.Series, q: float = 0.10) -> pd.DataFrame:
    """Apply Benjamini-Hochberg false discovery rate control."""
    if not 0 < q < 1:
        raise ValueError("q must lie between 0 and 1.")
    p = pvalues.dropna().astype(float).sort_values()
    m = len(p)
    if m == 0:
        return pd.DataFrame(columns=["p_value", "threshold", "reject"])
    ranks = np.arange(1, m + 1)
    thresholds = ranks / m * q
    reject = p.to_numpy() <= thresholds
    if reject.any():
        kmax = np.where(reject)[0].max()
        reject_final = np.arange(m) <= kmax
    else:
        reject_final = np.zeros(m, dtype=bool)
    return pd.DataFrame({"p_value": p, "threshold": thresholds, "reject": reject_final}, index=p.index)


def probability_calibration_report(
    event: pd.Series,
    probability: pd.Series,
    n_bins: int = 10,
) -> dict[str, object]:
    """Evaluate probability forecast calibration."""
    df = pd.concat([event.rename("event"), probability.rename("prob")], axis=1)
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    df["event"] = df["event"].astype(int)
    df["prob"] = df["prob"].astype(float).clip(1e-6, 1 - 1e-6)
    if df["event"].nunique() < 2:
        raise ValueError("Event series must contain both classes.")

    df["bin"] = pd.cut(df["prob"], bins=np.linspace(0, 1, n_bins + 1), include_lowest=True)
    by_bin = df.groupby("bin", observed=False).agg(
        n=("event", "size"),
        avg_probability=("prob", "mean"),
        realized_frequency=("event", "mean"),
    )
    by_bin["abs_calibration_error"] = (by_bin["realized_frequency"] - by_bin["avg_probability"]).abs()
    ece = (by_bin["n"] / by_bin["n"].sum() * by_bin["abs_calibration_error"]).sum()

    return {
        "brier_score": float(brier_score_loss(df["event"], df["prob"])),
        "log_loss": float(log_loss(df["event"], df["prob"])),
        "expected_calibration_error": float(ece),
        "avg_probability": float(df["prob"].mean()),
        "realized_frequency": float(df["event"].mean()),
        "nobs": int(len(df)),
        "reliability_table": by_bin,
    }
```

## 7.29 Python: Walk-Forward Validation Engine

The following engine is intentionally generic. It receives a model factory so the same function can validate linear models, regularized models, classifiers, or simple custom forecasting functions. Any scaling or feature selection must be inside the model pipeline to avoid leakage.

```python
from sklearn.base import clone


def walk_forward_predictions(
    data: pd.DataFrame,
    feature_cols: list[str],
    target_col: str,
    model,
    min_train: int = 72,
    rolling_window: int | None = None,
) -> pd.DataFrame:
    """Generate walk-forward predictions for a sklearn-style model.

    The model must implement fit(X, y) and predict(X). If preprocessing is
    required, pass a sklearn Pipeline so preprocessing is fit only on training
    data within each walk-forward step.
    """
    required = feature_cols + [target_col]
    missing = set(required) - set(data.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")

    clean = data[required].replace([np.inf, -np.inf], np.nan).dropna().astype(float)
    if len(clean) <= min_train:
        raise ValueError("Not enough observations for walk-forward validation.")

    rows = []
    for loc in range(min_train, len(clean)):
        start = 0 if rolling_window is None else max(0, loc - rolling_window)
        train = clean.iloc[start:loc]
        test = clean.iloc[[loc]]
        if len(train) < min_train:
            continue
        fitted = clone(model)
        fitted.fit(train[feature_cols], train[target_col])
        pred = float(fitted.predict(test[feature_cols])[0])
        rows.append({
            "date": test.index[0],
            "forecast": pred,
            "actual": float(test[target_col].iloc[0]),
            "train_start": train.index[0],
            "train_end": train.index[-1],
            "n_train": len(train),
        })
    return pd.DataFrame(rows).set_index("date")
```

## 7.30 Python: Cross-Sectional IC, Spread, and Regime-Stratified Validation

```python
from scipy.stats import spearmanr


def cross_sectional_ic_by_date(
    panel: pd.DataFrame,
    signal_col: str,
    target_col: str,
    min_assets: int = 5,
) -> pd.Series:
    """Compute Spearman rank IC by date for a MultiIndex(date, asset) panel."""
    if not isinstance(panel.index, pd.MultiIndex):
        raise TypeError("panel must have MultiIndex(date, asset).")
    out = {}
    for date, group in panel[[signal_col, target_col]].dropna().groupby(level=0):
        if len(group) < min_assets:
            out[date] = np.nan
        else:
            out[date] = float(spearmanr(group[signal_col], group[target_col])[0])
    return pd.Series(out, name="rank_ic")


def long_short_spread_by_date(
    panel: pd.DataFrame,
    signal_col: str,
    target_col: str,
    top_q: float = 0.8,
    bottom_q: float = 0.2,
    min_assets: int = 10,
) -> pd.Series:
    """Compute top-minus-bottom forward target spread by date."""
    if not 0 < bottom_q < top_q < 1:
        raise ValueError("Require 0 < bottom_q < top_q < 1.")
    out = {}
    for date, group in panel[[signal_col, target_col]].dropna().groupby(level=0):
        if len(group) < min_assets:
            out[date] = np.nan
            continue
        lo = group[signal_col].quantile(bottom_q)
        hi = group[signal_col].quantile(top_q)
        top = group.loc[group[signal_col] >= hi, target_col]
        bottom = group.loc[group[signal_col] <= lo, target_col]
        out[date] = float(top.mean() - bottom.mean())
    return pd.Series(out, name="long_short_spread")


def regime_weighted_metric(metric: pd.Series, regime_prob: pd.Series) -> float:
    """Compute a probability-weighted average metric for one regime."""
    df = pd.concat([metric.rename("metric"), regime_prob.rename("prob")], axis=1)
    df = df.replace([np.inf, -np.inf], np.nan).dropna().astype(float)
    if df.empty or df["prob"].sum() <= 0:
        return np.nan
    return float((df["metric"] * df["prob"]).sum() / df["prob"].sum())


def regime_stratified_report(metric: pd.Series, regime_probs: pd.DataFrame) -> pd.Series:
    """Compute regime-weighted metric for each regime probability column."""
    return pd.Series(
        {col: regime_weighted_metric(metric, regime_probs[col]) for col in regime_probs.columns},
        name=f"regime_weighted_{metric.name}",
    )
```

## 7.31 Python: Visualization Code for Validation Diagnostics

```python
import matplotlib.pyplot as plt


def plot_forecast_errors(results: pd.DataFrame, title: str = "Forecast Errors") -> None:
    """Plot realized target, forecast, and error."""
    required = {"actual", "forecast"}
    if not required.issubset(results.columns):
        raise KeyError("results must include actual and forecast columns.")
    fig, ax = plt.subplots(figsize=(10, 4))
    results[["actual", "forecast"]].plot(ax=ax)
    ax.axhline(0.0, linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Target / forecast")
    plt.tight_layout()
    plt.show()


def plot_rolling_metric(series: pd.Series, window: int = 24, title: str = "Rolling Metric") -> None:
    """Plot a metric and its rolling average."""
    clean = series.dropna()
    fig, ax = plt.subplots(figsize=(10, 4))
    clean.plot(ax=ax, label="Metric")
    clean.rolling(window, min_periods=max(3, window // 3)).mean().plot(ax=ax, label=f"Rolling {window}m mean")
    ax.axhline(0.0, linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_reliability_table(reliability_table: pd.DataFrame) -> None:
    """Plot probability calibration by bin."""
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(reliability_table["avg_probability"], reliability_table["realized_frequency"])
    ax.plot([0, 1], [0, 1], linewidth=1)
    ax.set_xlabel("Average predicted probability")
    ax.set_ylabel("Realized frequency")
    ax.set_title("Probability Reliability Plot")
    plt.tight_layout()
    plt.show()


def plot_drawdown(return_series: pd.Series, title: str = "Drawdown") -> None:
    """Plot cumulative drawdown from a return series."""
    r = return_series.dropna().astype(float)
    wealth = (1.0 + r).cumprod()
    peak = wealth.cummax()
    dd = wealth / peak - 1.0
    fig, ax = plt.subplots(figsize=(10, 4))
    dd.plot(ax=ax)
    ax.axhline(0.0, linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    plt.tight_layout()
    plt.show()
```

## 7.32 Python: Synthetic End-to-End Validation Example

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

# Synthetic example only. Replace with point-in-time features and aligned targets.
rng = np.random.default_rng(123)
dates = pd.date_range("2000-01-31", periods=240, freq="M")

features = pd.DataFrame(
    {
        "growth_score": rng.normal(size=len(dates)).cumsum() / 10,
        "credit_stress": rng.normal(size=len(dates)).cumsum() / 8,
        "inflation_score": rng.normal(size=len(dates)).cumsum() / 12,
    },
    index=dates,
)

# Historical-only standardization for the synthetic example.
features_z = (features - features.shift(1).expanding(60).mean()) / features.shift(1).expanding(60).std()

target = (
    0.010 * features_z["growth_score"].fillna(0)
    - 0.012 * features_z["credit_stress"].fillna(0)
    - 0.006 * features_z["inflation_score"].fillna(0)
    + rng.normal(0, 0.04, len(dates))
)
target = target.rename("target")

data = features_z.join(target).dropna()
model = Pipeline([("scaler", StandardScaler()), ("ridge", Ridge(alpha=10.0))])

wf = walk_forward_predictions(
    data=data,
    feature_cols=["growth_score", "credit_stress", "inflation_score"],
    target_col="target",
    model=model,
    min_train=84,
)

print(forecast_accuracy_report(wf["actual"], wf["forecast"], benchmark=0.0))

cfg = ValidationConfig(horizon=3, nw_lags=2, min_obs=36, bootstrap_samples=1000, random_state=11)
spread_like = wf["forecast"] * wf["actual"]
print(mean_with_hac_tstat(spread_like, cfg))
print(block_bootstrap_ci(spread_like, config=cfg))

# Probability example: classify positive returns using a simple transformed score.
prob = 1.0 / (1.0 + np.exp(-wf["forecast"] / wf["forecast"].std()))
event = (wf["actual"] > 0).astype(int)
cal = probability_calibration_report(event, prob, n_bins=5)
print({k: v for k, v in cal.items() if k != "reliability_table"})
print(cal["reliability_table"])
```

## 7.33 Interpretation of Validation Results

A validation result should be interpreted using both statistical and economic standards.

| Finding | Interpretation | Action |
|---|---|---|
| Positive OOS $R^2$, stable IC, low turnover | Strong evidence of useful forecast content. | Candidate for portfolio integration. |
| Positive IC but weak spread | Ranking relation exists but may not monetize well. | Re-examine bucket construction and costs. |
| Strong in-sample, poor OOS | Likely overfit or unstable. | Retire, simplify, or restrict to research. |
| Good hit rate, poor payoff | Frequent small wins with large losses. | Add tail-risk controls or avoid. |
| Good average performance, crisis failure | Hidden short-vol or liquidity exposure. | Regime gate, stress overlay, or lower weight. |
| Significant before FDR, insignificant after FDR | Multiple-testing risk. | Treat as research candidate only. |
| Good probability ranking, poor calibration | Discrimination exists but probabilities too extreme. | Calibrate probabilities or use rank-only. |
| Regime-specific efficacy | Signal works only in certain states. | Use regime-conditioned confidence. |

## 7.34 Validation Governance and Model Approval

A signal should move through staged approval.

| Stage | Description | Allowed Use |
|---|---|---|
| Research candidate | Economic rationale and preliminary evidence. | Research only. |
| Watchlist signal | Point-in-time construction and some OOS support. | Monitoring dashboard. |
| Low-weight input | Robust validation but limited breadth or capacity. | Small contribution to composite. |
| Production input | Strong evidence, governance approval, monitoring. | Portfolio process subject to constraints. |
| Retired signal | Evidence decayed or implementation failed. | Archived; no active use. |

Approval should require a frozen specification. If a researcher modifies the lookback, universe, transformation, or threshold after validation, the model should be revalidated.

## 7.35 Common Validation Mistakes

1. **Using full-sample preprocessing.** Scaling, PCA, feature selection, winsorization, and ranking must be fit historically.
2. **Ignoring overlapping returns.** $t+3$ and $t+12$ require robust inference.
3. **Treating in-sample p-values as validation.** Out-of-sample and walk-forward evidence are required.
4. **Not counting failed trials.** Multiple-testing controls require honest inventory of tested variants.
5. **Confusing smoothed regime labels with real-time probabilities.** Smoothed labels use future data.
6. **Evaluating gross performance only.** Costs, turnover, financing, roll, margin, and liquidity matter.
7. **Ignoring stress periods.** A signal that fails in crises may be unacceptable even if average returns are good.
8. **Over-optimizing hyperparameters.** Nested validation is required.
9. **Assuming probability calibration.** Probability forecasts require reliability diagnostics.
10. **Not documenting decisions.** Research without run manifests and versioning cannot be governed.

## 7.36 Part 7 Summary

Part 7 developed the statistical validation, inference, and robustness-testing layer of the macro-regime research process. The main lessons are:

1. Validation must be an evidence stack, not a single p-value or backtest chart.
2. In-sample analysis is useful for exploration, but pseudo-real-time and walk-forward testing are essential for production relevance.
3. Expanding windows use more data, while rolling windows adapt better to structural breaks; both should be tested thoughtfully.
4. Time-series cross-validation must preserve chronological order, and nested validation is required for hyperparameter tuning.
5. Purging and embargoing are important when cross-validation folds contain overlapping forward-return windows.
6. Overlapping $t+3$ and $t+12$ returns require Newey-West, block bootstrap, or other dependence-robust inference.
7. Statistical significance must be separated from economic significance after costs, turnover, liquidity, risk, and constraints.
8. Diebold-Mariano tests compare forecast accuracy against benchmarks, while probability forecasts require calibration diagnostics.
9. Multiple-testing risk is central in macro signal research; FDR, Reality Check, SPA, and deflated Sharpe methods help control false discoveries.
10. Regime-stratified, subperiod, geography, asset-class, horizon, and stress-period validation reveal whether a signal is broad or conditional.
11. Portfolio validation must include gross and net returns, turnover, exposure decomposition, drawdowns, stress behavior, and capacity assumptions.
12. Production approval requires frozen specifications, reproducibility, monitoring, and a clear governance status.

---

# Stop Point

This installment completes:

1. **Part 7: Statistical Validation, Inference, and Robustness Testing.**

Continue next with **Part 8: Machine Learning for Macro-Regime and Signal Models**.
