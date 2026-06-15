# Institutional Macro-Regime Detection, Multi-Asset Signal Identification, and Statistical Validation Curriculum

## Installment 4: Part 4 - Statistical and Economic Regime Detection

**Scope of this installment.** This installment continues the curriculum with **Part 4 only**. It assumes the global assumptions, timestamp conventions, monthly feature-engineering rules, and return-target conventions established in Installments 1 through 3.

**Educational boundary.** This document is for research education, model design, and institutional portfolio-process development. It is not personalized investment advice, a live trading recommendation, or a guarantee of alpha.

---

# Part 4: Statistical and Economic Regime Detection

## 4.1 Purpose of Regime Detection

Regime detection is the process of estimating whether the current macro-financial environment resembles a persistent state with distinct return, volatility, correlation, liquidity, or policy characteristics. A regime model does not reveal an objective truth. It constructs a useful state representation from noisy data. The state representation can then be used for signal conditioning, forward-return forecasting, risk management, stress testing, and portfolio construction.

Let $S_t$ denote the latent regime at monthly decision timestamp $t$. Because $S_t$ is not directly observed, a realistic model produces probabilities:

$$
\boldsymbol{\pi}_t=
\left[\Pr(S_t=1\mid\mathcal{F}_t),\ldots,
\Pr(S_t=K\mid\mathcal{F}_t)\right]^\top,
$$

where $K$ is the number of possible regimes and $\mathcal{F}_t$ is the information set available at $t$. These probabilities should be interpreted as model-implied beliefs about latent states, not as directly observed labels.

Regime detection is useful only if it improves at least one of the following tasks:

| Task | Regime Output Used | Practical Use |
|---|---|---|
| Return forecasting | $\Pr(S_t=k\mid\mathcal{F}_t)$ | Estimate regime-conditioned expected returns. |
| Volatility forecasting | Regime-specific volatility state | Scale exposures during unstable environments. |
| Correlation forecasting | Regime-specific covariance state | Anticipate diversification breakdown. |
| Signal conditioning | Signal efficacy by regime | Use signals only where they historically worked. |
| Risk management | Stress or crisis probability | Reduce risk when model uncertainty rises. |
| Scenario design | Transition probabilities | Simulate paths from expansion to slowdown or stress. |
| Portfolio construction | Probability-weighted risk premia | Convert state probabilities into expected-return and risk inputs. |

A regime model should therefore be judged not only by whether its labels sound plausible, but by whether its probabilities are stable, interpretable, timely, out-of-sample useful, and robust to realistic data availability.

## 4.2 Regime Definitions: Macro, Market, Volatility, Liquidity, Inflation, Credit, and Risk Appetite

Different regime models answer different questions. A macro regime, a volatility regime, and a liquidity regime are not the same object.

| Regime Type | State Variable | Typical Inputs | Common Output |
|---|---|---|---|
| Macro regime | Growth-inflation-policy mix | PMI, inflation, labor, policy, curve, credit | Expansion, slowdown, stagflation, reflation. |
| Market regime | Asset return and correlation state | Equity, bond, credit, FX, commodity returns | Risk-on, risk-off, diversification, beta shock. |
| Volatility regime | Level and persistence of uncertainty | Realized vol, implied vol, vol term structure | Low vol, rising vol, crisis vol, mean-reversion. |
| Liquidity regime | Funding and market depth state | Funding spreads, FCI, reserves, cross-currency basis | Easy liquidity, tightening, funding stress. |
| Inflation regime | Inflation level and momentum | CPI, PCE, wages, breakevens, inflation breadth | Disinflation, target-consistent, inflation shock. |
| Credit regime | Default and spread stress state | IG/HY spreads, CDS, lending standards, defaults | Benign credit, widening, distress, recovery. |
| Risk-appetite regime | Investor willingness to hold risk | Equity momentum, credit spreads, VIX curve, flows | Risk-seeking, neutral, de-risking, panic. |

A useful institutional framework often runs several regime detectors simultaneously and then combines them. For example, a portfolio team may use a macro growth-inflation regime for strategic tilts, a liquidity regime for leverage control, a volatility regime for option overlays, and a credit regime for drawdown-risk monitoring.

## 4.3 Regime Identification Versus Regime Prediction

A critical distinction is whether the model is estimating the current state or predicting a future state.

A **filtered current-state probability** is:

$$
\pi_{k,t}^{\mathrm{filter}}=
\Pr(S_t=k\mid\mathcal{F}_t).
$$

It uses information available through $t$ and estimates the regime at $t$.

A **forward regime probability** is:

$$
\pi_{k,t+h\mid t}^{\mathrm{forecast}}=
\Pr(S_{t+h}=k\mid\mathcal{F}_t).
$$

It forecasts the state at $t+h$ using only information available at $t$.

A **smoothed historical probability** is:

$$
\pi_{k,t}^{\mathrm{smooth}}=
\Pr(S_t=k\mid\mathcal{F}_T),
\qquad T>t.
$$

It uses information after $t$ and is therefore not valid for real-time historical trading decisions. Smoothed probabilities can be useful for retrospective interpretation, model diagnostics, and regime labeling, but they should not be used as live signals in a backtest unless the goal is explicitly ex-post analysis.

## 4.4 Desirable Properties of a Regime Model

A regime model should satisfy both statistical and economic requirements.

| Property | Statistical Meaning | Economic Meaning |
|---|---|---|
| Persistence | States do not switch every month without reason. | Regimes reflect durable environments. |
| Separability | States have distinct feature distributions. | Each regime tells a different macro story. |
| Timeliness | Detection delay is not excessive. | State changes are useful before the asset move is fully over. |
| Stability | Similar data revisions do not flip labels constantly. | Portfolio process is not whipsawed by noise. |
| Interpretability | State labels can be explained and monitored. | Investment committee can understand drivers. |
| Out-of-sample utility | Probabilities help forecasts or risk control. | Regime model improves decisions, not only narratives. |
| Robustness | Results survive lookback, feature, and sample changes. | Regime story is not a data-mined artifact. |

A regime detector that creates visually appealing historical labels but fails to improve any forecast, risk-control process, or portfolio input is a descriptive clustering exercise, not a validated investment model.

## 4.5 Rule-Based Macro Regime Classification

Rule-based regimes use pre-specified economic thresholds or composite scores. They are transparent and easy to govern, but they can be brittle if thresholds are poorly calibrated.

Let $G_t$ be a standardized growth score and $I_t$ be a standardized inflation score. A simple four-state growth-inflation model is:

$$
S_t=
\begin{cases}
\mathrm{Disinflationary\ Expansion}, & G_t>0,\ I_t<0,\\
\mathrm{Reflation\ or\ Overheating}, & G_t>0,\ I_t>0,\\
\mathrm{Deflationary\ Slowdown}, & G_t<0,\ I_t<0,\\
\mathrm{Stagflation\ Pressure}, & G_t<0,\ I_t>0.
\end{cases}
$$

This model is interpretable, but the hard boundary at zero can create false precision. A continuous alternative uses soft regime scores:

$$
q_{1,t}=\sigma(aG_t)\sigma(-aI_t),
$$

$$
q_{2,t}=\sigma(aG_t)\sigma(aI_t),
$$

$$
q_{3,t}=\sigma(-aG_t)\sigma(-aI_t),
$$

$$
q_{4,t}=\sigma(-aG_t)\sigma(aI_t),
$$

where $\sigma(u)=1/(1+e^{-u})$ is a logistic function and $a>0$ controls boundary sharpness. The normalized regime probabilities are:

$$
\pi_{k,t}=\frac{q_{k,t}}{\sum_{j=1}^{4}q_{j,t}}.
$$

**Interpretation.** Instead of forcing a hard label, the model assigns higher probability to states consistent with the growth-inflation mix. This is more appropriate when the macro environment is ambiguous.

### 4.5.1 Rule-Based Regime Design Principles

| Design Choice | Good Practice | Failure Mode |
|---|---|---|
| Indicator selection | Use diverse categories such as growth, inflation, credit, and liquidity. | One indicator dominates the narrative. |
| Thresholds | Use economically meaningful and historically validated cutoffs. | Optimized thresholds overfit the sample. |
| Smoothing | Use persistence filters or probability smoothing. | Monthly noise causes excessive switching. |
| Publication lag | Use release calendars or conservative lags. | Reference-month data creates look-ahead bias. |
| Labeling | Label after inspecting drivers, not after inspecting returns. | State names are chosen to explain realized performance. |

## 4.6 Clustering-Based Regime Detection

Clustering estimates regimes by grouping observations with similar feature values. Let $X_t\in\mathbb{R}^M$ be a vector of standardized macro and market features at time $t$. Clustering attempts to partition observations into $K$ groups:

$$
S_t \in \{1,\ldots,K\}.
$$

Clustering is attractive because it can discover structure without pre-defined labels. However, clustering does not know economics. It groups based on distance or likelihood, so the researcher must interpret the clusters carefully and avoid selecting $K$ or features solely to create attractive asset-return patterns.

### 4.6.1 K-Means Clustering

K-means solves:

$$
\min_{\{C_k\}_{k=1}^{K}}\sum_{k=1}^{K}\sum_{t\in C_k}\|X_t-\mu_k\|_2^2,
$$

where $C_k$ is the set of observations assigned to cluster $k$ and $\mu_k$ is the cluster centroid.

**Assumptions and interpretation.** K-means assumes roughly spherical clusters under Euclidean distance after scaling. It is sensitive to feature standardization, outliers, and initialization. It produces hard labels rather than probabilities.

### 4.6.2 Gaussian Mixture Models

A Gaussian mixture model assumes:

$$
p(X_t)=\sum_{k=1}^{K}\omega_k\mathcal{N}(X_t\mid\mu_k,\Sigma_k),
$$

where $\omega_k$ is the mixture weight, $\mu_k$ is the mean vector, and $\Sigma_k$ is the covariance matrix of component $k$. The posterior probability of state $k$ is:

$$
\gamma_{k,t}=\Pr(S_t=k\mid X_t)=
\frac{\omega_k\mathcal{N}(X_t\mid\mu_k,\Sigma_k)}
{\sum_{j=1}^{K}\omega_j\mathcal{N}(X_t\mid\mu_j,\Sigma_j)}.
$$

GMMs provide soft probabilities and allow elliptical clusters, but they can be unstable in small samples when $M$ is large relative to $T$.

### 4.6.3 Hierarchical Clustering

Hierarchical clustering builds nested clusters using a distance metric and linkage rule. Common linkage methods include single, complete, average, and Ward linkage. It is useful for exploratory analysis and understanding cluster structure, but it does not naturally produce time-persistent regimes.

### 4.6.4 Spectral Clustering

Spectral clustering uses the eigenvectors of a similarity graph. It can capture nonlinear cluster shapes. However, it is less transparent for institutional macro research and can be sensitive to similarity-kernel choices. It is best used as an exploratory complement rather than as the primary production regime model.

### 4.6.5 Clustering Method Comparison

| Method | Output | Strength | Weakness | Best Use |
|---|---|---|---|---|
| K-means | Hard labels | Simple and transparent. | Spherical clusters, no probabilities. | Baseline regime grouping. |
| GMM | Soft probabilities | Probabilistic and flexible covariance. | Small-sample instability. | Soft macro-state estimation. |
| Hierarchical | Dendrogram and labels | Exploratory structure. | No natural real-time probability. | Feature grouping and regime exploration. |
| Spectral | Nonlinear labels | Captures complex shapes. | Less interpretable and parameter sensitive. | Research exploration. |

## 4.7 Principal Components and Macro Factor Extraction

Regime models often benefit from reducing many correlated macro features into a smaller number of factors. Principal component analysis finds orthogonal directions that explain variance in $X_t$.

Let $X$ be a $T\times M$ standardized feature matrix. PCA decomposes the covariance matrix:

$$
\hat\Sigma_X=V\Lambda V^\top,
$$

where $V$ contains eigenvectors and $\Lambda$ is a diagonal matrix of eigenvalues. The first $r$ principal component scores are:

$$
F_t = V_r^\top X_t,
$$

where $V_r$ contains the first $r$ eigenvectors.

PCA is useful for reducing redundancy, but the factors are statistical objects. They need economic interpretation. A first component may represent broad risk appetite, a second may represent inflation pressure, and a third may represent liquidity stress, but this must be verified by factor loadings and time-series behavior.

### 4.7.1 PCA in Real-Time

A common leakage error is fitting PCA on the full sample and then using historical component scores. A valid walk-forward PCA feature at time $t$ estimates loadings using only data through $t$ or earlier:

$$
\hat V_{r,t}=\mathrm{PCA}(X_{1:t}),
\qquad
F_t=\hat V_{r,t}^\top X_t.
$$

For prediction, the PCA estimation should be nested inside the training window. In production, PCA loadings should be monitored because factor meanings can drift.

## 4.8 Hidden Markov Models

A hidden Markov model, or HMM, assumes the observed feature vector $X_t$ is generated by an unobserved state $S_t$. The state follows a Markov chain:

$$
\Pr(S_t=j\mid S_{t-1}=i,S_{t-2},\ldots)=\Pr(S_t=j\mid S_{t-1}=i)=p_{ij}.
$$

The transition matrix is:

$$
P=
\begin{bmatrix}
p_{11} & p_{12} & \cdots & p_{1K}\\
p_{21} & p_{22} & \cdots & p_{2K}\\
\vdots & \vdots & \ddots & \vdots\\
p_{K1} & p_{K2} & \cdots & p_{KK}
\end{bmatrix},
\qquad
\sum_{j=1}^{K}p_{ij}=1.
$$

The observation density is usually specified as:

$$
X_t\mid S_t=k \sim \mathcal{N}(\mu_k,\Sigma_k),
$$

though other distributions may be used.

The likelihood for a sequence $X_{1:T}$ is:

$$
\mathcal{L}(\theta)=p(X_{1:T}\mid\theta)=
\sum_{S_1=1}^{K}\cdots\sum_{S_T=1}^{K}
\Pr(S_1)\prod_{t=2}^{T}p_{S_{t-1},S_t}
\prod_{t=1}^{T}f(X_t\mid S_t),
$$

where $\theta$ includes the transition matrix, initial state probabilities, and state-specific observation parameters. Direct summation over all state paths is infeasible for large $T$, so the forward-backward algorithm is used.

## 4.9 HMM Filtering, Smoothing, and Forecasting

### 4.9.1 Filtered Probability

The filtered probability is:

$$
\alpha_t(k)=\Pr(S_t=k\mid X_{1:t}).
$$

A recursive filtering step can be written as:

$$
\tilde\alpha_t(k)=f(X_t\mid S_t=k)
\sum_{j=1}^{K}\alpha_{t-1}(j)p_{jk},
$$

and then normalized:

$$
\alpha_t(k)=\frac{\tilde\alpha_t(k)}{\sum_{\ell=1}^{K}\tilde\alpha_t(\ell)}.
$$

This is the probability valid for a real-time decision at $t$ if all inputs $X_{1:t}$ are available at $t$.

### 4.9.2 Smoothed Probability

The smoothed probability is:

$$
\xi_t(k)=\Pr(S_t=k\mid X_{1:T}).
$$

It uses the full sample and should not be used as a real-time signal. Smoothed probabilities are useful for labeling states after estimation and checking whether the HMM produces economically coherent historical regimes.

### 4.9.3 Forward Regime Forecast

The one-step-ahead state forecast is:

$$
\boldsymbol{\pi}_{t+1\mid t}=P^\top\boldsymbol{\alpha}_t.
$$

The $h$-step-ahead state forecast is:

$$
\boldsymbol{\pi}_{t+h\mid t}=(P^\top)^h\boldsymbol{\alpha}_t.
$$

This equation is useful for forecasting how likely the current state is to persist or transition over the portfolio horizon.

## 4.10 Regime Persistence and Expected Duration

The diagonal element $p_{kk}$ is the probability of remaining in regime $k$ for one more month. A simple expected duration approximation is:

$$
\mathbb{E}[D_k]=\frac{1}{1-p_{kk}},
$$

where $D_k$ is the duration in months of regime $k$ under a geometric duration assumption. If $p_{kk}=0.90$, the expected duration is 10 months. If $p_{kk}=0.50$, the expected duration is 2 months.

This formula is useful but should be interpreted cautiously. Some macro regimes may have duration dependence that is not captured by a first-order Markov chain.

## 4.11 Markov-Switching Regression

A Markov-switching regression allows return dynamics or macro relationships to change by latent state. A simple state-dependent mean model is:

$$
y_t=\mu_{S_t}+\varepsilon_t,
\qquad
\varepsilon_t\mid S_t=k\sim \mathcal{N}(0,\sigma_k^2).
$$

A state-dependent regression is:

$$
y_t=\alpha_{S_t}+\beta_{S_t}^{\top}X_t+\varepsilon_t,
\qquad
\varepsilon_t\mid S_t=k\sim \mathcal{N}(0,\sigma_{S_t}^2).
$$

Here, both the intercept and factor sensitivities can differ across regimes. For example, credit spread widening may have a more negative equity effect in a liquidity-stress regime than in a normal expansion.

A practical restriction is to allow only intercepts or variances to switch when sample size is limited:

$$
y_t=\alpha_{S_t}+\beta^{\top}X_t+\varepsilon_t,
\qquad
\varepsilon_t\mid S_t=k\sim \mathcal{N}(0,\sigma_k^2).
$$

This reduces parameter instability while still capturing regime-dependent expected returns and volatility.

## 4.12 Dynamic Factor Models

Dynamic factor models assume many observed variables are driven by a small number of latent factors. Let $X_t\in\mathbb{R}^{M}$ be a vector of macro and market features. A dynamic factor model is:

$$
X_t=\Lambda F_t+u_t,
$$

$$
F_t=A F_{t-1}+\eta_t,
$$

where $F_t\in\mathbb{R}^{r}$ is a vector of latent factors, $\Lambda$ is the loading matrix, $A$ is the factor transition matrix, $u_t$ is idiosyncratic noise, and $\eta_t$ is factor innovation.

Dynamic factor models are useful when the researcher wants a smoother estimate of latent growth, inflation, liquidity, or risk-appetite states from many noisy indicators. Regimes can then be detected by applying thresholds, clustering, or HMMs to the latent factors.

## 4.13 Bayesian State-Space Models

A Bayesian state-space model represents latent macro conditions and updates beliefs as new data arrive. A generic state-space model is:

$$
X_t = H S_t + e_t,
\qquad e_t\sim\mathcal{N}(0,R),
$$

$$
S_t = A S_{t-1}+u_t,
\qquad u_t\sim\mathcal{N}(0,Q),
$$

where $X_t$ is observed data, $S_t$ is a latent state vector, $H$ is the observation matrix, $A$ is the state transition matrix, and $R$ and $Q$ are covariance matrices.

Bayesian updating follows:

$$
p(S_t\mid X_{1:t})\propto p(X_t\mid S_t)p(S_t\mid X_{1:t-1}).
$$

This equation says the posterior state belief equals the prior state belief updated by the likelihood of the new observation. Bayesian models are powerful because they represent uncertainty explicitly and can combine model-based priors with observed data. They are also harder to govern because results can depend on prior choices and model specification.

## 4.14 Regime Labeling and Economic Interpretation

Statistical regimes must be labeled after examining their feature profiles, not after examining which assets performed best. A disciplined labeling process uses state-conditional feature averages:

$$
\bar X_k=\frac{\sum_{t=1}^{T}\pi_{k,t}X_t}{\sum_{t=1}^{T}\pi_{k,t}},
$$

where $\pi_{k,t}$ is the probability of regime $k$. State-conditional realized return averages can be computed later for interpretation, but labels should be driven primarily by macro and market-state characteristics.

A useful labeling table is:

| Regime | Growth | Inflation | Credit | Liquidity | Volatility | Possible Label |
|---|---:|---:|---:|---:|---:|---|
| 1 | High | Low | Tight | Easy | Low | Disinflationary expansion. |
| 2 | High | High | Neutral | Neutral | Rising | Reflation or overheating. |
| 3 | Low | Low | Wider | Easier policy | Moderate | Growth slowdown. |
| 4 | Low | High | Wider | Tight | High | Stagflation or stress. |

The label should be treated as a communication device. The model output remains the probability vector, not the label.

## 4.15 Regime-Conditioned Return and Risk Estimates

Once regime probabilities are estimated, the researcher can compute regime-conditioned expected returns:

$$
\hat\mu_{i,k,h}=\frac{\sum_{t=1}^{T}\pi_{k,t}R_{i,t,h}}{\sum_{t=1}^{T}\pi_{k,t}},
$$

where $\hat\mu_{i,k,h}$ is the estimated expected forward return for asset $i$ over horizon $h$ conditional on regime $k$. The probability-weighted expected return at time $t$ is:

$$
\hat\mu_{i,t,h}^{\mathrm{regime}}=\sum_{k=1}^{K}\pi_{k,t}\hat\mu_{i,k,h}.
$$

A regime-conditioned covariance matrix is:

$$
\hat\Sigma_{k,h}=\frac{\sum_{t=1}^{T}\pi_{k,t}(R_{t,h}-\hat\mu_{k,h})(R_{t,h}-\hat\mu_{k,h})^\top}{\sum_{t=1}^{T}\pi_{k,t}},
$$

where $R_{t,h}$ is a vector of asset returns. The probability-weighted covariance estimate is:

$$
\hat\Sigma_{t,h}^{\mathrm{regime}}=\sum_{k=1}^{K}\pi_{k,t}\hat\Sigma_{k,h}.
$$

These estimates are intuitive but can be noisy. A state with few effective observations may produce unstable expected returns. Shrinkage toward unconditional estimates is usually necessary.

## 4.16 Regime Probability Smoothing

Monthly regime probabilities can be noisy. A simple exponentially weighted smoothing rule is:

$$
\tilde\pi_{k,t}=\lambda\tilde\pi_{k,t-1}+(1-\lambda)\pi_{k,t},
\qquad 0\leq\lambda<1.
$$

The vector is then normalized:

$$
\tilde\pi_{k,t}^{*}=\frac{\tilde\pi_{k,t}}{\sum_{j=1}^{K}\tilde\pi_{j,t}}.
$$

Smoothing reduces whipsaw but increases detection delay. For portfolio use, smoothing should be validated against objectives such as drawdown reduction, turnover control, and forecast improvement rather than chosen visually.

## 4.17 Choosing the Number of Regimes

There is no universal correct number of regimes. Too few regimes hide important distinctions. Too many regimes overfit noise and create states with too few observations.

| Criterion | Use | Limitation |
|---|---|---|
| Economic interpretability | Each regime has a clear macro meaning. | Subjective. |
| Information criteria | Compare AIC or BIC for likelihood models. | Can prefer overly complex or unstable models. |
| Out-of-sample usefulness | Regimes improve forecasts or risk control. | Requires careful validation. |
| Stability | Similar samples produce similar states. | Hard to measure with structural breaks. |
| Effective observations | Each state has enough data. | Rare crisis states may still matter. |
| Transition plausibility | State transitions are economically coherent. | Markov structure may be too restrictive. |

For monthly macro data, $K=2$ to $K=5$ is often more governable than a large number of states. A two-state model may separate calm and stress. A four-state growth-inflation model may separate expansion, reflation, slowdown, and stagflation. More states require stronger evidence.

## 4.18 Regime Model Comparison Table

| Model | Regime Output | Strength | Weakness | Production Use |
|---|---|---|---|---|
| Rule-based | Hard or soft economic states | Transparent and governable. | Threshold sensitivity. | Baseline and governance overlay. |
| K-means | Hard clusters | Simple and fast. | No persistence or probabilities. | Exploratory grouping. |
| GMM | Soft cluster probabilities | Probabilistic state estimates. | Small-sample covariance instability. | Macro-state probability model. |
| HMM | Filtered and smoothed probabilities | Persistence and transition matrix. | Distributional assumptions and local optima. | Core regime detector. |
| Markov-switching regression | State-dependent return dynamics | Directly links regimes to returns. | High parameter count. | Return and volatility state model. |
| Dynamic factor model | Latent factors | Reduces noisy macro panel. | Factors require interpretation. | Latent growth/liquidity estimation. |
| Bayesian state-space | Posterior state distribution | Explicit uncertainty and priors. | Complex estimation and governance. | Advanced nowcasting and regime updating. |

## 4.19 Python: Clustering-Based Regime Detection

The following code demonstrates leak-aware clustering on monthly macro features. It is written for research use. In production, feature scaling and model fitting should be nested inside walk-forward validation when cluster labels are used predictively.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class RegimeClusteringConfig:
    """Configuration for clustering-based regime detection.

    Parameters
    ----------
    n_regimes : int
        Number of clusters or regimes.
    method : str
        One of {'kmeans', 'gmm', 'hierarchical', 'spectral'}.
    pca_components : int | None
        Optional number of PCA components before clustering.
    random_state : int
        Random seed for reproducibility.
    """

    n_regimes: int = 4
    method: str = "gmm"
    pca_components: int | None = None
    random_state: int = 42


def validate_feature_frame(X: pd.DataFrame) -> None:
    """Validate monthly feature matrix."""
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame.")
    if not isinstance(X.index, pd.DatetimeIndex):
        raise TypeError("X must have a DatetimeIndex.")
    if not X.index.is_monotonic_increasing:
        raise ValueError("X index must be sorted.")
    if X.index.has_duplicates:
        raise ValueError("X index has duplicates.")
    if X.shape[0] < 24:
        raise ValueError("At least 24 monthly observations are recommended.")


def fit_clustering_regimes(
    features: pd.DataFrame,
    config: RegimeClusteringConfig,
) -> dict[str, object]:
    """Fit clustering model and return labels and probabilities when available.

    Missing observations are dropped. The returned labels are in estimation
    order and should be economically relabeled before use in communication.
    """
    validate_feature_frame(features)
    X = features.replace([np.inf, -np.inf], np.nan).dropna().astype(float)
    if len(X) < 24:
        raise ValueError("Not enough complete observations after dropping missing data.")

    steps: list[tuple[str, object]] = [("scaler", StandardScaler())]
    if config.pca_components is not None:
        if not 1 <= config.pca_components <= X.shape[1]:
            raise ValueError("pca_components must be between 1 and number of features.")
        steps.append(("pca", PCA(n_components=config.pca_components)))

    preprocessor = Pipeline(steps)
    Z = preprocessor.fit_transform(X)

    method = config.method.lower()
    if method == "kmeans":
        model = KMeans(
            n_clusters=config.n_regimes,
            n_init=50,
            random_state=config.random_state,
        )
        labels = model.fit_predict(Z)
        probs = pd.get_dummies(labels).reindex(columns=range(config.n_regimes), fill_value=0)
        probs = probs.astype(float).to_numpy()

    elif method == "gmm":
        model = GaussianMixture(
            n_components=config.n_regimes,
            covariance_type="full",
            n_init=20,
            reg_covar=1e-5,
            random_state=config.random_state,
        )
        labels = model.fit_predict(Z)
        probs = model.predict_proba(Z)

    elif method == "hierarchical":
        model = AgglomerativeClustering(n_clusters=config.n_regimes, linkage="ward")
        labels = model.fit_predict(Z)
        probs = pd.get_dummies(labels).reindex(columns=range(config.n_regimes), fill_value=0)
        probs = probs.astype(float).to_numpy()

    elif method == "spectral":
        model = SpectralClustering(
            n_clusters=config.n_regimes,
            affinity="nearest_neighbors",
            random_state=config.random_state,
            assign_labels="kmeans",
        )
        labels = model.fit_predict(Z)
        probs = pd.get_dummies(labels).reindex(columns=range(config.n_regimes), fill_value=0)
        probs = probs.astype(float).to_numpy()

    else:
        raise ValueError("method must be one of kmeans, gmm, hierarchical, spectral.")

    label_series = pd.Series(labels, index=X.index, name="raw_regime")
    prob_df = pd.DataFrame(
        probs,
        index=X.index,
        columns=[f"regime_{k}_prob" for k in range(config.n_regimes)],
    )

    return {
        "features_used": X,
        "preprocessor": preprocessor,
        "model": model,
        "labels": label_series,
        "probabilities": prob_df,
    }
```

## 4.20 Python: Labeling Cluster Regimes by Feature Profiles

```python
def regime_feature_profiles(
    features: pd.DataFrame,
    probabilities: pd.DataFrame,
) -> pd.DataFrame:
    """Compute probability-weighted feature profiles by regime."""
    X = features.loc[probabilities.index].astype(float)
    P = probabilities.astype(float)
    profiles = []

    for col in P.columns:
        w = P[col].clip(lower=0.0)
        denom = w.sum()
        if denom <= 0:
            profile = pd.Series(np.nan, index=X.columns)
        else:
            profile = X.mul(w, axis=0).sum(axis=0) / denom
        profile.name = col.replace("_prob", "")
        profiles.append(profile)

    return pd.DataFrame(profiles)


def simple_economic_labels(profile: pd.DataFrame) -> pd.Series:
    """Assign rough labels from standardized macro profiles.

    This helper expects columns with names that include words such as growth,
    inflation, credit, liquidity, or volatility. It is a starting point only;
    final labels require human economic review.
    """
    labels = {}
    for regime, row in profile.iterrows():
        growth = row[[c for c in row.index if "growth" in c.lower()]].mean()
        inflation = row[[c for c in row.index if "inflation" in c.lower()]].mean()
        stress_cols = [c for c in row.index if any(s in c.lower() for s in ["credit", "liq", "vol"])]
        stress = row[stress_cols].mean() if stress_cols else np.nan

        if pd.notna(stress) and stress > 0.75:
            labels[regime] = "stress_or_liquidity_tightening"
        elif growth > 0 and inflation <= 0:
            labels[regime] = "disinflationary_expansion"
        elif growth > 0 and inflation > 0:
            labels[regime] = "reflation_or_overheating"
        elif growth <= 0 and inflation > 0:
            labels[regime] = "stagflation_pressure"
        else:
            labels[regime] = "growth_slowdown"

    return pd.Series(labels, name="economic_label")


# Example usage with a feature matrix called macro_features:
# cfg = RegimeClusteringConfig(n_regimes=4, method="gmm", pca_components=None)
# result = fit_clustering_regimes(macro_features, cfg)
# profiles = regime_feature_profiles(result["features_used"], result["probabilities"])
# labels = simple_economic_labels(profiles)
# print(profiles)
# print(labels)
```

## 4.21 Python: Hidden Markov Model Classifier

The following code uses `hmmlearn` when available. If it is not installed, the function raises a clear error and the fallback pseudocode that follows explains the required algorithm.

```python
def fit_hmm_regimes(
    features: pd.DataFrame,
    n_regimes: int = 4,
    covariance_type: str = "full",
    n_iter: int = 1000,
    random_state: int = 42,
) -> dict[str, object]:
    """Fit a Gaussian HMM to standardized monthly features.

    The model should be used carefully in forecasting studies. For true
    out-of-sample work, fit the HMM inside each expanding or rolling training
    window rather than on the full sample.
    """
    try:
        from hmmlearn.hmm import GaussianHMM
    except ImportError as exc:
        raise ImportError(
            "hmmlearn is not installed. Install hmmlearn or implement the "
            "forward-backward fallback described below."
        ) from exc

    validate_feature_frame(features)
    X = features.replace([np.inf, -np.inf], np.nan).dropna().astype(float)
    scaler = StandardScaler()
    Z = scaler.fit_transform(X)

    model = GaussianHMM(
        n_components=n_regimes,
        covariance_type=covariance_type,
        n_iter=n_iter,
        random_state=random_state,
    )
    model.fit(Z)

    labels = pd.Series(model.predict(Z), index=X.index, name="hmm_raw_regime")
    filtered_or_posterior = pd.DataFrame(
        model.predict_proba(Z),
        index=X.index,
        columns=[f"regime_{k}_prob" for k in range(n_regimes)],
    )
    transition = pd.DataFrame(
        model.transmat_,
        index=[f"from_{k}" for k in range(n_regimes)],
        columns=[f"to_{k}" for k in range(n_regimes)],
    )

    expected_duration = pd.Series(
        1.0 / np.maximum(1.0 - np.diag(model.transmat_), 1e-6),
        index=[f"regime_{k}" for k in range(n_regimes)],
        name="expected_duration_months",
    )

    return {
        "features_used": X,
        "scaler": scaler,
        "model": model,
        "labels": labels,
        "probabilities": filtered_or_posterior,
        "transition_matrix": transition,
        "expected_duration": expected_duration,
    }
```

### 4.21.1 HMM Fallback Pseudocode

```python
# Fallback outline if hmmlearn is unavailable:
#
# 1. Initialize K state means, covariances, transition matrix, and initial probs.
# 2. E-step:
#    a. Use the forward recursion to compute alpha_t(k).
#    b. Use the backward recursion to compute beta_t(k).
#    c. Compute gamma_t(k) = P(S_t=k | X_1:T).
#    d. Compute xi_t(i,j) = P(S_t=i, S_{t+1}=j | X_1:T).
# 3. M-step:
#    a. Update initial probs with gamma_1(k).
#    b. Update transition p_ij = sum_t xi_t(i,j) / sum_t gamma_t(i).
#    c. Update state means and covariances using gamma_t(k) weights.
# 4. Iterate until log-likelihood convergence.
# 5. For real-time use, retain filtered probabilities alpha_t(k), not only
#    smoothed probabilities gamma_t(k).
```

## 4.22 Python: Transition Matrix and Persistence Diagnostics

```python
def empirical_transition_matrix(labels: pd.Series, n_regimes: int | None = None) -> pd.DataFrame:
    """Compute empirical transition matrix from hard regime labels."""
    s = labels.dropna().astype(int)
    if len(s) < 2:
        raise ValueError("Need at least two labels to compute transitions.")
    if n_regimes is None:
        n_regimes = int(s.max()) + 1

    counts = pd.DataFrame(0, index=range(n_regimes), columns=range(n_regimes), dtype=float)
    for a, b in zip(s.iloc[:-1], s.iloc[1:]):
        counts.loc[a, b] += 1.0

    trans = counts.div(counts.sum(axis=1).replace(0.0, np.nan), axis=0)
    trans.index = [f"from_{i}" for i in range(n_regimes)]
    trans.columns = [f"to_{i}" for i in range(n_regimes)]
    return trans


def expected_durations_from_transition(transition: pd.DataFrame) -> pd.Series:
    """Compute geometric expected duration from transition matrix diagonal."""
    diag = np.diag(transition.astype(float).to_numpy())
    duration = 1.0 / np.maximum(1.0 - diag, 1e-6)
    return pd.Series(duration, index=transition.index, name="expected_duration_months")


def smooth_regime_probabilities(prob: pd.DataFrame, lam: float = 0.75) -> pd.DataFrame:
    """Exponentially smooth regime probabilities and re-normalize rows."""
    if not 0 <= lam < 1:
        raise ValueError("lam must satisfy 0 <= lam < 1.")
    P = prob.astype(float).clip(lower=0.0)
    smoothed = P.copy()
    for i in range(1, len(P)):
        smoothed.iloc[i] = lam * smoothed.iloc[i - 1] + (1 - lam) * P.iloc[i]
    row_sum = smoothed.sum(axis=1).replace(0.0, np.nan)
    return smoothed.div(row_sum, axis=0)
```

## 4.23 Python: Markov-Switching Regression with statsmodels

The following example uses `statsmodels` to estimate a Markov-switching mean and variance model for a return series. This is a diagnostic tool and should be embedded in walk-forward validation before being used for forecasting.

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm


def fit_markov_switching_return_model(
    returns: pd.Series,
    k_regimes: int = 2,
    switching_variance: bool = True,
):
    """Fit a Markov-switching model to a monthly return series.

    Parameters
    ----------
    returns : pd.Series
        Monthly return series, indexed by date.
    k_regimes : int
        Number of latent regimes.
    switching_variance : bool
        Whether variance changes by regime.
    """
    y = returns.dropna().astype(float)
    if len(y) < 60:
        raise ValueError("At least 60 observations are recommended.")

    model = sm.tsa.MarkovRegression(
        y,
        k_regimes=k_regimes,
        trend="c",
        switching_variance=switching_variance,
    )
    result = model.fit(disp=False)
    probs = result.filtered_marginal_probabilities
    probs.columns = [f"regime_{k}_prob" for k in range(k_regimes)]
    return result, probs


# Example usage:
# result, regime_probs = fit_markov_switching_return_model(asset_returns["Global_Equity"])
# print(result.summary())
# print(regime_probs.tail())
```

## 4.24 Python: Regime-Conditioned Expected Returns

```python
def regime_conditioned_expected_returns(
    forward_returns: pd.DataFrame,
    regime_probabilities: pd.DataFrame,
    shrinkage: float = 0.50,
) -> pd.DataFrame:
    """Estimate regime-conditioned expected returns with shrinkage.

    Parameters
    ----------
    forward_returns : pd.DataFrame
        Wide matrix of forward returns. Rows are dates and columns are assets.
    regime_probabilities : pd.DataFrame
        Regime probability matrix aligned by date.
    shrinkage : float
        Weight on unconditional mean. 0 means no shrinkage. 1 means fully
        shrink to unconditional mean.
    """
    if not 0 <= shrinkage <= 1:
        raise ValueError("shrinkage must be between 0 and 1.")

    common = forward_returns.index.intersection(regime_probabilities.index)
    R = forward_returns.loc[common].astype(float)
    P = regime_probabilities.loc[common].astype(float).clip(lower=0.0)
    P = P.div(P.sum(axis=1).replace(0.0, np.nan), axis=0)

    unconditional = R.mean(axis=0)
    rows = []
    for regime in P.columns:
        w = P[regime]
        denom = w.sum()
        if denom <= 0:
            mu = pd.Series(np.nan, index=R.columns)
        else:
            mu = R.mul(w, axis=0).sum(axis=0) / denom
        mu_shrunk = (1 - shrinkage) * mu + shrinkage * unconditional
        mu_shrunk.name = regime.replace("_prob", "")
        rows.append(mu_shrunk)

    return pd.DataFrame(rows)


def probability_weighted_regime_forecast(
    current_probabilities: pd.Series,
    regime_expected_returns: pd.DataFrame,
) -> pd.Series:
    """Convert current regime probabilities into asset expected returns."""
    p = current_probabilities.astype(float).copy()
    p.index = [idx.replace("_prob", "") for idx in p.index]
    common = regime_expected_returns.index.intersection(p.index)
    if common.empty:
        raise ValueError("No overlapping regimes between probabilities and expected returns.")
    p = p.loc[common]
    p = p / p.sum()
    return regime_expected_returns.loc[common].mul(p, axis=0).sum(axis=0)
```

## 4.25 Python: Regime Visualization Diagnostics

```python
import matplotlib.pyplot as plt


def plot_regime_probabilities(prob: pd.DataFrame, title: str = "Regime Probabilities") -> None:
    """Plot regime probability histories."""
    fig, ax = plt.subplots(figsize=(10, 5))
    prob.plot(ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Probability")
    ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.show()


def plot_transition_matrix(transition: pd.DataFrame, title: str = "Transition Matrix") -> None:
    """Plot transition matrix as an image."""
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(transition.astype(float).to_numpy(), aspect="auto")
    ax.set_title(title)
    ax.set_xticks(range(transition.shape[1]))
    ax.set_xticklabels(transition.columns, rotation=45, ha="right")
    ax.set_yticks(range(transition.shape[0]))
    ax.set_yticklabels(transition.index)
    fig.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.show()


def plot_regime_feature_profile(profile: pd.DataFrame) -> None:
    """Plot feature profile by regime as a heatmap-like image."""
    fig, ax = plt.subplots(figsize=(10, max(3, 0.4 * len(profile))))
    im = ax.imshow(profile.astype(float).to_numpy(), aspect="auto")
    ax.set_title("Regime Feature Profiles")
    ax.set_xticks(range(profile.shape[1]))
    ax.set_xticklabels(profile.columns, rotation=45, ha="right")
    ax.set_yticks(range(profile.shape[0]))
    ax.set_yticklabels(profile.index)
    fig.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.show()
```

## 4.26 Walk-Forward Regime Estimation

A regime model used for forecasting should be estimated in a walk-forward manner. At each decision timestamp $t$, the model is fit using only training data through $t$ and then produces probabilities for $t$ or $t+1$. A simplified procedure is:

1. Select an initial training window, such as 120 months.
2. At month $t$, fit the scaler, PCA, clustering model, or HMM using observations through $t$.
3. Compute regime probabilities at $t$ using only available features.
4. Use these probabilities to forecast asset returns over $t+1$, $t+3$, or $t+12$.
5. Move forward one month and repeat.

The practical difficulty is **label switching**. Regime 0 in one training window may correspond to regime 2 in the next. A production system must align regime labels across refits using feature-profile similarity, transition continuity, or pre-specified anchor definitions.

```python
def align_regime_labels_by_profile(
    old_profile: pd.DataFrame,
    new_profile: pd.DataFrame,
) -> dict[str, str]:
    """Map new regime labels to old labels using nearest feature profiles.

    This simple greedy mapping is for demonstration. For production, use an
    assignment algorithm such as scipy.optimize.linear_sum_assignment.
    """
    mapping: dict[str, str] = {}
    remaining_old = set(old_profile.index)

    for new_regime, new_row in new_profile.iterrows():
        distances = {}
        for old_regime in remaining_old:
            old_row = old_profile.loc[old_regime]
            common = old_row.dropna().index.intersection(new_row.dropna().index)
            if len(common) == 0:
                distances[old_regime] = np.inf
            else:
                distances[old_regime] = float(np.linalg.norm(new_row[common] - old_row[common]))
        best_old = min(distances, key=distances.get)
        mapping[new_regime] = best_old
        remaining_old.remove(best_old)
        if not remaining_old:
            break

    return mapping
```

## 4.27 Regime Detection Failure Modes

| Failure Mode | Description | Mitigation |
|---|---|---|
| Look-ahead features | Regime labels use unreleased macro data. | Join by release/vintage timestamp. |
| Full-sample scaling | Z-scores or PCA use future data. | Fit transformations inside training windows. |
| Smoothed-probability leakage | Backtest uses probabilities estimated with future data. | Use filtered probabilities for real-time tests. |
| Label switching | State names change across refits. | Align labels by feature profiles or anchors. |
| Over-fragmentation | Too many regimes with few observations. | Limit $K$, use shrinkage, validate out of sample. |
| Narrative overfitting | Labels chosen after observing returns. | Label using feature profiles first. |
| Excess switching | Model reacts to monthly noise. | Add persistence, smoothing, or transition penalties. |
| Delayed detection | Model identifies crises only after losses. | Include market-implied stress and liquidity variables. |
| Structural breaks | Historical states no longer map to current policy regime. | Rolling validation and model-risk overlays. |
| Asset-use mismatch | Macro states do not improve return forecasts. | Test regime-conditioned signal efficacy. |

## 4.28 Practical Governance Checklist

| Question | Required Evidence |
|---|---|
| What does each regime mean? | Feature-profile table and economic interpretation. |
| Are inputs point-in-time? | Data lineage and release-lag documentation. |
| Are probabilities real-time valid? | Filtered probability construction, not ex-post smoothing. |
| Is the number of regimes justified? | Interpretability, stability, and validation evidence. |
| Are transitions plausible? | Transition matrix and expected duration diagnostics. |
| Does the model improve decisions? | Forecast, risk, or portfolio validation versus baselines. |
| How stable are labels across refits? | Label-alignment and profile-stability reports. |
| What happens during crises? | Stress-period diagnostics and failure-mode review. |
| What are the overrides? | Governance rules for data anomalies and model breakdowns. |
| How is drift monitored? | Live feature, probability, and forecast-drift dashboards. |

## 4.29 Part 4 Summary

Part 4 developed the statistical and economic foundation for regime detection. The main lessons are:

1. Regimes are latent, uncertain, and model-dependent. They should be represented as probabilities rather than deterministic truths.
2. Regime identification estimates the current state, while regime prediction forecasts future state probabilities. Smoothed probabilities are useful for retrospective analysis but are not valid real-time signals.
3. Rule-based regimes are transparent and governable but sensitive to thresholds. Soft probability versions reduce boundary brittleness.
4. Clustering methods can discover historical state groupings, but they require careful economic labeling and point-in-time validation.
5. PCA and dynamic factor models reduce noisy macro panels into latent factors, but factor meanings can drift and must be interpreted.
6. HMMs add persistence and transition matrices, making them useful for monthly macro regimes, but they require careful estimation and validation.
7. Markov-switching regressions connect state dynamics directly to returns or volatility, but the parameter count can become large.
8. Bayesian state-space models provide explicit uncertainty updating but require strong governance around priors and specification.
9. Regime-conditioned expected returns and covariances are useful but noisy; shrinkage and effective-sample diagnostics are essential.
10. Production regime models require data lineage, filtered probabilities, label stability, transition diagnostics, out-of-sample validation, and live monitoring.

---

# Stop Point

This installment completes:

1. **Part 4: Statistical and Economic Regime Detection.**

Continue next with **Part 5: Macro Causal Channels and Cross-Asset Transmission**.
