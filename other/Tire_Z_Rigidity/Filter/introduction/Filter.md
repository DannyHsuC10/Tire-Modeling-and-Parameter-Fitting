# Data Filter

The filter processes data in four steps. 

1. Trim the beginning and end of each series.
2. Apply a Boolean mask.
3. Apply an automatic low-pass filter.
4. Convert the data.

[Filter source file](../filter.py)

The filter automatically reads [this JSON configuration](json.md).


## 1. Trimming the Beginning and End

### Purpose

The **beginning and end** of a measurement series, particularly in tire tests and other dynamic measurements, often contain

* Transient conditions before the system stabilizes.
* Readings from sensors outside their normal measurement range.
* Deceleration, stops, or manual disturbances.

Remove these samples before analysis because they do not represent the test conditions.

---

### Mathematical Description

Consider an original time series.

$$
\mathbf{X} = {x_1, x_2, \dots, x_N}
$$

Definitions

* $n_h$ is the number of samples to remove from the beginning.
* $n_t$ is the number of samples to remove from the end.

Define the trimmed series as follows.

$$
\tilde{x}_i =
\begin{cases}
\text{NaN}, & i \le n_h \
\text{NaN}, & i > N - n_t \
x_i, & \text{otherwise}
\end{cases}
$$

This operation does the following.

* **Keeps the length of the series unchanged.**
* Marks the unusable regions explicitly.

This preserves time alignment for subsequent masking and filtering.

---

### Using NaN to Preserve the Time Index

* NaN represents a missing value.
* Masking, filtering, and statistical operations can exclude these values.
* The original time index is preserved, preventing misalignment.

---

## 2. Boolean Masking

### Purpose

The mask has the following purpose.

> **Mark the samples that meet the physical and experimental conditions.**

Each sample has one of two states.

* `True` means the sample is valid and usable.
* `False` means the sample is excluded from subsequent analysis.

---

### 2.1 Range Mask

Define an allowed range for each physical quantity $x(t)$, such as $F_z, \alpha, \kappa$.

$$
x_{\min} \le x(t) \le x_{\max}
$$

Define its Boolean mask as follows.

$$
m(t) = \begin{cases}
\text{True}, & x_{\min} \le x(t) \le x_{\max} \
\text{False}, & \text{otherwise}
\end{cases}
$$

---

### 2.2 Minimum Segment Length

Isolated samples and very short segments may be noise or transients even if they lie within the allowed range.

Use the following constraint.

* $L_{\min}$ is the minimum length of a continuous valid segment.

Given a mask sequence $m(t)$, consider a continuous True segment of length $L$ that meets the following condition.

$$
L < L_{\min}
$$

Set the entire segment to False.

$$
m(t) = \text{False}, \quad \forall t \in \text{segment}
$$

This is equivalent to

* a one-dimensional morphological noise removal operation similar to opening.

---

### 2.3 Slope-Based Mask

Use this mask for signals such as slip ratio and slip angle that **should follow a linear trend**.

---

#### (1) Define Segments

Set the allowed ranges for positive and negative values.

$$
x(t) \in [x^+*{\min}, x^+*{\max}] \cup [x^-*{\min}, x^-*{\max}]
$$

Points outside the allowed ranges mark segment boundaries.

---

#### (2) Calculate the Segment Slope

Fit each continuous segment ${x_1, \dots, x_n}$ by least squares.

$$
x(t) \approx a t + b
$$

The slope $a$ is

$$
a = \frac{\sum (t_i - \bar{t})(x_i - \bar{x})}{\sum (t_i - \bar{t})^2}
$$

---

#### (3) Apply the Slope Criterion

If the slope satisfies the following condition,

$$
a_{\min} \le a \le a_{\max}
$$

the whole segment is valid.

$$
m(t) = \text{True}
$$

---

#### (4) Handle Degenerate Cases and Exceptions

* If the segment is constant ($\sigma_x < \varepsilon$),

  * treat it as steady-state data and **keep it**.
* If it contains NaN or Inf,

  * discard the segment.

---

### 2.4 Combining Masks

* **Multiple conditions on the same column**

$$
m_{\text{col}} = m_1 \lor m_2 \lor \dots
$$

* **Conditions across different columns**

$$
m_{\text{total}} = \bigwedge_k m_k
$$

The final mask $m_{\text{total}}$ determines which samples to keep.

## 3. Set-Theoretic Interpretation of Boolean Masks

### Time Index Set and Data Mapping

Define the discrete set of measurement time indices.

$$
\mathcal{T} = \{ t_1, t_2, \dots, t_N \}
$$

Treat each measured quantity, such as $F_z, \alpha, \kappa, SL$, as a mapping.

$$
x : \mathcal{T} \rightarrow \mathbb{R}
$$

A Boolean mask defines a **physically acceptable subset** of the time index set $\mathcal{T}$.

---

### Subset for a Single Condition

Given a range constraint,

$$
x_{\min} \le x(t) \le x_{\max}
$$

define the corresponding subset of time indices.

$$
\mathcal{A}
=
\{\, t \in \mathcal{T} \mid x_{\min} \le x(t) \le x_{\max} \,\}
$$

The Boolean mask is the indicator function of that set.

$$
m(t) = \mathbf{1}_{\mathcal{A}}(t)
=
\begin{cases}
1, & t \in \mathcal{A} \\
0, & t \notin \mathcal{A}
\end{cases}
$$

---

### Combining Conditions on One Column with Union (OR)

If one physical quantity allows several operating conditions, take the union of their acceptable sets.

$$
\mathcal{A}_{\text{col}}
=
\bigcup_{i=1}^{k} \mathcal{A}_i
$$

The corresponding Boolean operation is

$$
m_{\text{col}}(t)
=
\bigvee_{i=1}^{k} m_i(t)
$$

which has the following interpretation.

> A sample is valid if it belongs to any acceptable operating condition.

---

### Combining Different Physical Quantities with Intersection (AND)

When constraints apply to several physical quantities, intersect their acceptable time sets.

$$
\mathcal{A}_{\text{total}}
=
\bigcap_{j} \mathcal{A}_j
$$

In Boolean form,

$$
m_{\text{total}}(t)
=
\bigwedge_{j} m_j(t)
$$

a time index must **meet every physical and experimental condition**.

---

### Set Interpretation of Minimum Segment Length

Take a continuous time subset of $\mathcal{A}$.

$$
\mathcal{S}_i
=
\{ t_k, t_{k+1}, \dots, t_{k+L_i} \}
$$

If its length meets the following condition,

$$
|\mathcal{S}_i| < L_{\min}
$$

remove that subset.

$$
\mathcal{A} \leftarrow \mathcal{A} \setminus \mathcal{S}_i
$$

This filters out short events that do not represent a stable physical condition.

---

## 4. Automatic Fourier-Based Low-Pass Filtering

### 4.1 Fourier Duality Between Time and Frequency

The frequency-domain representation of the discrete signal $x(t)$ is given below.

$$
X(f)
=
\sum_{t=0}^{N-1}
x(t)\,e^{-j2\pi f t}
$$

High-frequency components often represent measurement noise, structural vibration, or rapid artifacts.

---

### 4.2 Power Spectral Density and Welch's Method

Define the power spectral density (PSD) as follows.

$$
P(f) = |X(f)|^2
$$

Welch's method segments, windows, and averages the signal to estimate the energy distribution reliably.

---

### 4.3 Cumulative Energy and Cutoff Selection

Define the cumulative energy function.

$$
E(f)
=
\int_{0}^{f} P(\nu)\,d\nu
$$

Choose cutoff frequency $f_c$ to satisfy the following condition.

$$
E(f_c)
\ge
r \cdot E(f_{\text{Nyq}})
$$

Here, $r$ is the fraction of energy to retain.

> The frequency range $[0, f_c]$ contains most of the physically meaningful signal energy.

---

### 4.4 Butterworth Low-Pass Filter

An order-$n$ Butterworth low-pass filter has the following magnitude response.

$$
|H(\omega)|^2
=
\frac{1}{1 + (\omega / \omega_c)^{2n}}
$$

Its maximally flat passband avoids introducing artificial oscillations.

---

### 4.5 Zero-Phase Filtering

Forward-backward filtering (`filtfilt`) is equivalent to the following.

$$
y(t) = H(z)\,H(z^{-1})\,x(t)
$$

It cancels phase delay so the filtered signal stays aligned with the original time axis.

---

### 4.6 Numerical Stability Constraints

- Skip filtering constant signals for which $P(f)=0,\ \forall f>0$.  
- $f_c > 0$ avoids reducing the filter to DC only.  
- $f_c < 0.45 f_s$ keeps the digital filter within its stability limit.

## 5. Data Conversion
This step converts the remaining data and removes unused fields.

1. Convert units and adjust signs to match the target coordinate convention.
1. Remove unused fields. Moving these field rules into JSON would reduce future source edits.