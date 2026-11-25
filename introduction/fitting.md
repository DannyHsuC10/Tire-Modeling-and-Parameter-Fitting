---
layout: base
---

# Main Script for Staged Magic Formula Fitting

This script controls parameter fitting for the **Magic Formula (MF)** tire model.

[Source file](../fitting.py)

* Read preprocessed tire measurement data.
* Load and manage fitting parameters and their bounds.
* Optimize the active parameters for each stage.
* Compute error metrics (RMS and COST).
* Update the parameter files.
* Export the results as a `.tir` file.

This script coordinates the full MF fitting workflow.

---

# 📦 Workflow Overview

```
Raw data → filter → tir_tester → Staged fitting → Update the CSV → Export TIR
```

Main dependencies

* [filter](../Filter/introduction/Filter.md) preprocesses the test data. Run data cleaning before running this script.
* [tir_tester](tir_tester.md) reads MF test data.
* [MF_Fitter](../Fitter/introduction/MF_fitter.md) optimizes the parameters.
* [csv_to_tir](csv_to_tir.md) converts the final CSV to a TIR file.

---

# 📁 Directory Structure

```
magic_formula/
│
├── data/
│   └── Fitting_data/
│       ├── Fitting_process.csv   # Fitting parameters
│       └── Fitting_Limits.csv    # Template file
│
├── Fitter/
├── model/
├── filter.py
├── tir_tester.py
└── main_fitting_script.py  ← Main script
```

---

# 🔧 Main Functions

---

## 1️⃣ Loading Fitting Parameters

```python
load_fit_parameters(filename)
```

What it does

* Load the fitting parameters from `data/Fitting_data/`.
* Read `.csv` or `.xlsx` files.
* Copy the template automatically if the parameter file is missing.

Return format

```python
{
  "PCX1": {"x0": initial_value, "lb": lower_bound, "ub": upper_bound},
  ...
}
```

---

## 2️⃣ Building the Initial MF Parameters

```python
build_mf_params(fit_params)
```

What it does

* Use the `x0` values as the initial MF parameters.
* Build a dictionary that can be passed directly to the MF calculations.

---

## 3️⃣ Selecting Parameters by Stage

```python
build_fit_params_for_stages(full_fit_params, STAGES, stages)
```

The function selects and returns the parameters for a fitting stage.

* Select the parameters fitted in the current stage.
* Return the following.

  * The stage-specific fit_params.
  * active_keys, the order of parameters passed to the optimizer.

---

# 🧩 Fitting Stage Design

The script fits the model in multiple stages.

---

## FX Fitting Stages

```
Stage 1 → Basic shape, stiffness, and peak force
Stage 2 → Load and camber variation
Stage 3 → Curvature correction under driving conditions
Stage 4 → Load-dependent correction
Stage 5 → Combined-slip parameters
```

---

## FY Fitting Stages

These stages cover the following parameters.

* Primary lateral force parameters.
* Load corrections.
* Higher-order corrections.
* Combined slip

---

# 🚀 Running the Converter

---

## Step 1. Read the Data

```python
F_data_1 = tir_tester.load_mf_data(...)
```

The input data must contain the following fields.

```
FZ
SL
SA
IA
P
FX or FY
```

---

## Step 2. Select the Fitting Type

```python
Fit_type = "FX"  # or "FY"
selected_stages = [1,2,3,4,5]
```

---

## Step 3. Fit the Parameters Stage by Stage

Fitting loop

```python
for stage_num in selected_stages:
```

For each stage, do the following.

1. Select the relevant data.
2. Create MF_inputs.
3. Initialize the Fitter.
4. Get the active parameters.
5. Call the optimizer.

```python
result = fitter.fit(...)
```

---

# 📊 Error Metrics

Each stage reports the following metrics.

```
N used by optimizer
RMS
MAX
COST
RMS %
```

Definitions

$$RMS = \sqrt{\sum(\Delta x²)}$$

$$MAX = \max{(\Delta x)}$$

$$cost = \sum(\Delta x)$$

$$RMS\% = RMS/\max{(x)}$$
---

# 💾 Safely Updating Parameter Files

```python
update_x0(mf_params_current, SAVE_DIR/"Fitting_process.csv")
```

The update follows this sequence.

* Write to a `.tmp` file first.
* Replace the original file with the temporary file.
* This protects the original file if a write is interrupted.

---

# 🔄 Final Output

```python
import csv_to_tir
```

Convert the updated CSV to a `.tir` file.
The TIR file can be used for the following.


---

# ⚙ Customization

You can change the following settings.

```python
Fit_type
selected_stages
F_data_list
```

Adjust these settings to switch between fitting strategies.

---

# 🏁 Full Workflow

```
Read the data
→ Load the parameters
→ Staged fitting
→ Compute the error
→ Update the CSV
→ Export TIR
→ Done
```
