---
layout: base
---

# Magic Formula Model Comparison and Visualization

[This module](../tir_tester.py) performs the following tasks.

* Load filtered tire measurement data.
* Load two `.tir` parameter sets.
* Evaluate the Magic Formula models.
* Compare predictions against measured data.
* Visualize differences between models.

Typical uses

> ✔ Compare models before and after fitting.
> ✔ Compare different TIR versions.
> ✔ Verify the effect of changes to MF parameters.

# 📦 Dependencies

* `model.CalculationInput`
* `MF_Universal_solver`
* `MF_tester.load_tir`
* `numpy`
* `matplotlib`
* `pandas`

---

# 🔧 Features

## 1️⃣ Loading MF Data

```python
load_mf_data(filename)
```

What it does

* Read data from `data/Filtered_data/`.
* Read `.csv` or `.xlsx` files.
* Return the following.

```python
{
  "FZ": np.ndarray,
  "SA": np.ndarray,
  "SL": np.ndarray,
  "IA": np.ndarray,
  "P": np.ndarray,
  "FX" or "FY": np.ndarray
}
```

---

### 📌 Required Data

The input data must contain the following fields.

```
FZ      Vertical load
SA      Slip Angle
SL      Slip Ratio
IA      Camber
P       Inflation Pressure
FX/FY   Measured force
```

---

## 2️⃣ Evaluating the Models

```python
MF = model.CalculationInput(...)
F_array = MF_Universal_solver(Fit_type, MF)
```

Calculation steps

1. Wrap the data in a `CalculationInput` object.
2. Call `MF_Universal_solver`.
3. Calculate the corresponding output force.

Supported outputs

* `"FX"` produces longitudinal force.
* `"FY"` produces lateral force.

---

## 3️⃣ Comparison Function

```python
plot_data(df, tir_params1, tir_params2, Fit_type)
```

---

### 📌 Purpose

Compare the following series.

```
Measured Force
vs
Model 1 Prediction
vs
Model 2 Prediction
```

---

### 📌 Calculation Steps

Collect the two TIR parameter sets.

```python
tir_params_list = [tir_params1, tir_params2]
```

For each parameter set, follow these steps.

* Build the MF input object.
* Compute the predicted values.
* Store the results in F_lists.

---

### 📌 Plot Contents

* Black solid line for measured values.
* Dashed line for Model 1.
* Dash-dot line for Model 2.

X-axis

```
Data point index
```

Y-axis

```
Force [N]
```

---

# 🚀 Usage

```python
if __name__ == "__main__":
```

---

## Step 1. Read the Data

```python
df = load_mf_data("B2356run57_processed5.csv")
```

---

## Step 2. Load Two TIR Parameter Sets

```python
tir_params1 = MF_tester.load_tir("data/tir/D2704_mf612.tir")
tir_params2 = MF_tester.load_tir("data/tir/tir_Fitting_results.tir")
```

Typical inputs

* `tir_params1` contains the original TTC or manufacturer model.
* `tir_params2` contains the fitted parameters.

---

## Step 3. Plot the Comparison

```python
plot_data(df, tir_params1, tir_params2, "FY")
```
