---
layout: base
---

# Magic Formula Model

## Model Scope
Magic Formula (MF) describes a tire's **longitudinal force, lateral force, aligning moment, overturning moment, and rolling resistance moment** across operating conditions.  
Version **6.1.2** implements the full equations for engineering use under pure and combined slip.

---

## Module Structure

### 1. **[Magic Formula Base Class](common.md)**

- **CalculationInput** groups operating inputs such as normal load, slip angle, longitudinal slip ratio, inflation pressure, speed, and camber.  
- The **MF612 base class** provides the following normalization methods.
  - `_normalize_load()` normalizes load.  
  - `_normalize_pressure()` normalizes inflation pressure.  
  - `_normalize_angles()` normalizes angles.  

**Physical meaning.** These steps express operating conditions as dimensionless quantities relative to reference values, keeping model behavior consistent across loads, pressures, and angles.

---

### 2. **[Magic Formula Fx](Fx_model.md)**
- **Fx0** is the longitudinal force under pure longitudinal slip.  
- **Fx** is the longitudinal force under combined slip, including the effect of slip angle.

**Physical meaning.** Describes the nonlinear relationship between slip ratio and longitudinal force during acceleration or braking, with slip-angle effects under combined slip.

---

### 3. **[Magic Formula Fy](Fy_model.md)**
- **Fy0** is the lateral force under pure lateral slip.  
- **Fy** is the lateral force under combined slip, including the effect of longitudinal slip.

**Physical meaning.** Describes how slip angle generates lateral force and how longitudinal slip affects it under combined slip.

---

### 4. **[Magic Formula Mz](Mz_model.md)**
- **Mz0** is the aligning moment under pure lateral slip.  
- **Mz** is the aligning moment under combined slip.

**Physical meaning.** Describes the aligning moment generated at a slip angle, including **pneumatic trail** and **scrub radius** effects and a longitudinal-slip correction under combined slip.

---

### 5. **[Magic Formula Mx](Mx_model.md)**
- **Mx** is the overturning moment.

**Physical meaning.** Describes tire overturning due to camber and lateral force. It depends on normal load, the lateral force ratio, and camber.

---

### 6. **[Magic Formula RRT](RRT_model.md)**
- **RRT MF** uses Magic Formula to calculate the rolling resistance moment.  
- **RRT SAE** uses the empirical SAE equation to calculate the rolling resistance moment.

**Physical meaning.** Describes tire energy loss during rolling as a function of load, inflation pressure, speed, and camber.

---

### 7. **[Unified API](../api.py)**
Convenience functions
- `calculate_fx()` evaluates combined-slip longitudinal force.  
- `calculate_fy()` evaluates combined-slip lateral force.  
- `calculate_mz()` evaluates combined-slip aligning moment.  
- `calculate_mx()` evaluates overturning moment.  
- `calculate_rrt()` evaluates rolling resistance moment.  

Create a `CalculationInput` object and pass it to the corresponding calculation function.

---

### 8. **[Package Initialization](../__init__.py)**
- Import the models and API functions in one place.  
- Define `__all__` to expose the main classes and functions.  
- Provide a quick-start example.  

Use `import model` to access these features.

---

## Usage Workflow

1. **Import the package and create the inputs.**  
Use one TIR parameter file per evaluation. The other inputs can be arrays for efficient batch evaluation. Supported input combinations include the following.

   * Scalar evaluation uses scalars for all inputs.
   * A single-vector evaluation uses a vector for **one** input and scalars for the rest.
   * Matrix evaluation uses equally sized arrays. This is the most efficient option and is recommended for fitting.

   ```python
   import model  # Import the model package

   MF = model.CalculationInput(  # Set the parameters for the test case
   FZ=800,
   SA=0.6,      
   SL=0.2,
   IA=0.0,
   pressure=80000,
   V = tir_params["LONGVL"],  # Replace with the required value
   Ro = tir_params["UNLOADED_RADIUS"],  # Replace with the required value
   tir_params=tir_params  # Parameters from the TIR file
   )
   ```

2. **Calculate forces and moments.**  
   ```python
   Fx = model.MF612_Fx.calculate(MF)   # Longitudinal force
   Fy = model.MF612_Fy.calculate(MF)   # Lateral force
   Mz = model.MF612_Mz.calculate(MF)   # Aligning moment
   Mx = model.MF612_Mx.calculate(MF)   # Overturning moment
   RRT = model.MF612_RRT_MF.calculate(MF) # Rolling resistance moment
   ```

3. **Read the results.**  
   - $Fx$ is the longitudinal force.  
   - $Fy$ is the lateral force.  
   - $Mz$ is the aligning moment.  
   - $Mx$ is the overturning moment.  
   - $RRT$ is the rolling resistance moment.  
