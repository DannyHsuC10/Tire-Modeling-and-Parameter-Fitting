---
layout: base
---

# Data Filter JSON Configuration
> The [example JSON file](../Filtering_Limits_stage_example.json) contains randomly generated values because the test data is private. Replace them with values appropriate for your dataset.
## 📌 Purpose

This JSON file controls how the tire data filter selects samples.

It defines the following constraints.

* Value ranges for each data channel (`min` and `max`).
* Minimum number of consecutive samples (`n`).
* Positive and negative segment limits (`pos_range` and `neg_range`).
* Slope limits (`slope_min` and `slope_max`).
* Data grouping by fitting stage.

Edit this file to **control which operating conditions and data enter Magic Formula fitting**.

---

# 📂 JSON Structure

```json
{
  "category_name": {
    "variable_name": {
      "subcategory_name": {
        "min": value,
        "max": value,
        "n":   consecutive_samples
      }
    }
  }
}
```

---

# 🧩 Level 1. Fitting Stages

Example uses

```json
"57_1"
"23_234"
```

These entries represent the following.

* Test runs.
* fitting stage
* Different stages of model development.

To add a fitting stage, use the following structure.

```json
"new_stage_name": {
  ...
}
```

---

# 📊 Level 2. Physical Variables

Common variables

| Variable | Description |
| -- | --- |
| FZ | Normal force |
| IA | Camber angle |
| P | Inflation pressure |
| SA | Slip angle |
| SL | Slip ratio |

Use the following pattern to constrain another variable such as `V`.

```json
"V": {
  "V_40": {"min": 90, "max": 91, "n": 50}
}
```

---

# 🔢 Level 3. Value Limits (min, max, and n)

Examples

```json
"FZ_10": {
  "min": -1200,
  "max": -700,
  "n": 30
}
```

### Parameters

| Parameter | Function |
| --- | ------------ |
| min | Lower bound |
| max | Upper bound |
| n | Number of consecutive samples that must meet the condition |

# 🔁 Positive and Negative Segment Limits (pos_range and neg_range)

Use separate ranges for positive and negative values of variables such as SA and SL.

Examples

```json
"SA": {
  "pos_range": {"min": 10, "max": 20},
  "neg_range": {"min": -20, "max": -10}
}
```

### Uses

* Retain only operating conditions with a fixed slip angle.
* Keep data symmetric across left and right turns.
* Select steady-state cornering segments.

---

# 📈 Slope Limits (slope_min and slope_max)

Examples

```json
"slope_min": -0.05,
"slope_max": -0.00
```

### Uses

* Retain segments where the variable changes at a steady rate.
* Exclude transitions between operating conditions.
* Exclude ramp-up and ramp-down events.
