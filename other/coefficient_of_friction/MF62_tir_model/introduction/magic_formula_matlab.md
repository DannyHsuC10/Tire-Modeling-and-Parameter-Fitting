---
layout: base
---

# MATLAB Magic Formula API

## 📌 Model Scope

This module implements **Magic Formula 6.1.2 (MF6.1.2)** in MATLAB and exposes a unified [MF API](../MF_api.m).

```
MF_api(cmd, FZ, SA, SL, IA, P, tir)
```
The design goal for the MATLAB API is to

> wrap the MF6.1.2 equations in a single interface.

To evaluate the model, call the API as shown below.

```
MF_api("FX", ...)
```

The MATLAB and Python models produce nearly identical results. This guide focuses on calling the MATLAB API.

## Magic Formula Equations

### Combined Slip

1. [Fx](../MF612_Fx.m)
1. [Fy](../MF612_Fy.m)
1. [Mx](../MF612_Mx.m)
1. [Mz](../MF612_Mz.m)

### Pure Slip

The API calls the combined-slip routines. The pure-slip routines are rarely called on their own because much of their implementation overlaps.

1. [Fx0](../Base_func/MF612_Fx0.m)
1. [Fy0](../Base_func/MF612_Fy0.m)
1. [Mz0](../Base_func/MF612_Mz0.m)

## 🎯 Core API

### Function Signature

```matlab
function out = MF_api(cmd, FZ, SA, SL, IA, P, tir)
```

---

### 📥 Inputs

| Parameter | Unit | Description |
| --------- | ------ | --------------------- |
| `cmd` | string | Output selector. Use "Fx", "Fy", or "Mz". |
| `FZ` | N | Normal force |
| `SA` | deg | Slip angle |
| `SL` | - | Longitudinal slip ratio |
| `IA` | deg | Camber angle |
| `P` | Pa | Inflation pressure |
| `mf_file` | string | Path to the TIR file |

---

### 📤 Outputs

| cmd | Return value |
| ------ | ---- |
| `"FX"` | Longitudinal force |
| `"FY"` | Lateral force |
| `"MZ"` | Aligning moment |
| `"MX"` | Overturning moment |

## CalculationInput

```matlab
function MF = CalculationInput(FZ,SA,SL,IA,P,tir)
```

What it does

1. Use the separate TIR loader to read the `.tir` file once and avoid reloading it for each calculation.
2. Group the operating inputs.
3. Build the MATLAB struct required by the Magic Formula calculations.

---

### Physical Parameters Set Automatically

| Parameter | Source |
| -------- | --------------- |
| `MF.PIO` | NOMPRES         |
| `MF.FZO` | FNOMIN          |
| `MF.Ro`  | UNLOADED_RADIUS |
| `MF.V`   | LONGVL          |

---

### Lambda Scaling Factors

The model retains the full λ scaling framework.

Example uses

```matlab
MF.lambdaMuyMi = 1;
MF.lambdaKya = 1;
MF.lambdaMuxMi = 1;
```

Use the scaling factors to adjust the model.

* Tune the model.
* Simulate reduced grip, for example with a scaling factor of 0.6.
* Run a sensitivity analysis.
* Calibrate the model against a real vehicle.

---

#### Common Adjustable Parameters

| Parameter | Description |
| ------------- | ------------------- |
| `lambdaMuyMi` | Lateral peak friction coefficient |
| `lambdaMuxMi` | Longitudinal peak friction coefficient |
| `lambdaKya`   | Cornering stiffness |
| `lambdaCy`    | Shape factor        |
| `lambdaEy`    | Curvature factor    |
| `epsilonX/Y` | Numerical stabilization term |

---

## 📂 Loading TIR Parameters for the Tire Model
> **Read the file with load_tir and pass the result to the API's TIR parameter field, as shown below.**

```matlab
tir = load_tir("MF612.tir");
```

### load_tir()

What it does

* Parse the TIR file line by line.
* Skip the following automatically.

  * Comments marked with `$`.
  * Section header `[SECTION]`
* Store the key-value pairs in a struct.

---

### parse_value()

What it does

* Try to parse each value as a number.
* Keep the value as a string if parsing fails.

## 📊 Usage Example

```matlab
Fx = MF_api("FX", 800, 0.0, 0.1, 0.0, 80000, tir);

Fy = MF_api("FY", 800, 3.0, 0.0, 0.0, 80000, tir);

Mz = MF_api("MZ", 800, 3.0, 0.0, 0.0, 80000, tir);
```
