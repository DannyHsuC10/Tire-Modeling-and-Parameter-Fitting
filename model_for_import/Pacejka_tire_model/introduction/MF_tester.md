# Magic Formula (MF) Tester and Surface Visualization

This module provides the following capabilities.

* Plot **Magic Formula tire model surfaces**.
* Compare how different TIR parameter sets affect predicted tire forces.
* Evaluate **Fx, Fy, Mx, Mz, and RRT**.
* Generate surfaces or curves for **α–Fz, κ–Fz, Fx–Fy–κ, and Fx–Fy–Fz**.

# 📂 Module Structure

```
MF_tester.py
├─ TIR file loader
├─ MF calculation input builder
├─ Surface plotting functions (plot_tire_surface / plot_tire_surfaces)
├─ Friction circles and surfaces or curves for varying κ or Fz
├─ __main__ example
```

---

# 🔧 Features and Main Functions

---

## 1️⃣ Loading TIR Parameters

```python
load_tir(filename: str) -> dict
```

What it does

* Read the `.tir` file.
* Convert each parameter to a float, int, or string.
* Return a **flat dictionary** `{param_name: value}` suitable for direct input to the MF model.

```python
tir_params["PCX1"] = 1.9
tir_params["UNLOADED_RADIUS"] = 0.259
```

---

## 2️⃣ Building MF Calculation Inputs

```python
MF_set(i, j, X, Y, fix, tir_params, pressure=82319, IA=0.0)
```

What it does

* Select the sweep dimension (`alpha`, `kappa`, or `Fz`).
* Create a `CalculationInput` object.
* Assign **fixed and varying inputs** to the appropriate axes for surface plotting.

Examples

* With fix = `"alpha"`, hold α fixed and vary the slip ratio and Fz.
* With fix = `"kappa"`, hold κ fixed and vary α and Fz.
* With fix = `"Fz"`, hold Fz fixed and vary α and κ.

---

## 3️⃣ Setting Surface Ranges

```python
fig_set(fix, out)
```

What it does

* Set the x, y, and z axes based on the sweep dimension `fix`.
* Return `(xlabel, ylabel, zlabel, x_range, y_range)`.
* Use these settings in all surface plotting functions.

---

## 4️⃣ Plotting Surfaces

### Single Model

```python
plot_tire_surface(out, fix, tir_params=None)
```

* Output a three-dimensional surface plot.
* Use one TIR model.
* Use **MF_Universal_solver** to evaluate the force at each grid point.

### Comparing Multiple Models

```python
plot_tire_surfaces(out, fix, tir_params_list, labels=None)
```

* Plot multiple TIR models together.
* Distinguish surfaces by color and opacity.
* Generate a legend automatically.
* Compare model behavior **before and after fitting**.

---

## 5️⃣ Friction Circle and Slip Ratio Surfaces

### Fx-Fy vs κ

```python
plot_friction_circle_vs_kappa_surface(Fz, pressure, alpha_lim, kappa_lim, tir_params, IA)
plot_friction_circle_vs_kappa_curves(Fz, pressure, alpha_lim, kappa_lim, tir_params, IA)
```

What it does

* The z-axis represents slip ratio κ.
* Show how κ changes the forces in the Fx–Fy plane.
* Choose a surface or stacked curves.
* Use the plot for friction circle analysis and model validation.

---

### Fx-Fy vs Fz

```python
plot_friction_circle_vs_Fz_surface(kappa, pressure, alpha_lim, Fz_max, tir_params, IA)
plot_friction_circle_vs_Fz_curves(kappa, alpha_lim, Fz_max, pressure, tir_params, IA)
```

What it does

* The z-axis represents vertical load Fz.
* Analyze how Fz affects the Fx–Fy distribution.
* Generate a smooth surface or stacked curves from an α sweep.

---

## 6️⃣ Visualization Features

* Plot **3D surfaces and curves**.
* Use a colormap to distinguish models or encode values.
* Adjust opacity to overlay several model surfaces.
* Generate legends and axis labels automatically.

---

# 🧠 Design

1. **Object-Based Plotting**

   * Pass objects to simplify the workflow.
   * Reuse the same plotting methods for different inputs.

2. **Flexible Sweep Dimensions**

   * Hold α, κ, or Fz constant to generate different surfaces.
   * Analyze friction circles and changes in vertical load.

3. **Model Comparison**

   * Compare results before and after fitting or across TIR parameter sets.
   * Assess fitting accuracy quickly.

4. **Extensibility**

   * Plot Fx, Fy, Mx, Mz, or RRT.
   * Extend the analysis with RMS error, percentage error, or 3D surface heatmaps.

---

# 🚀 Running the Examples

```python
if __name__ == "__main__":
    tir_params = load_tir("D2704_mf612.tir")
    tir_params_fit = load_tir("tir_Fitting_results.tir")
    
    outputs = ['FY']
    fix_cases = ['alpha', 'kappa', 'Fz']
    tir_params_list = [tir_params_fit, tir_params]
    
    for out in outputs:
        for fix in fix_cases:
            plot_tire_surfaces(out, fix, tir_params_list)
```

* Sweep α, κ, and Fz separately for the **FY** force output.
* Compare the surfaces before fitting (`D2704_mf612.tir`) and after fitting (`tir_Fitting_results.tir`).


# 🏁 Summary

The tester provides the following capabilities.

* Generate MF model surfaces quickly.
* Compare and visualize multiple models.
* Analyze friction circles and the effects of κ and Fz.
* Evaluate Fx, Fy, Mx, Mz, and RRT.
* Compare how different inputs affect model outputs.
* Extend the tester or integrate it into the full tire fitting workflow.
