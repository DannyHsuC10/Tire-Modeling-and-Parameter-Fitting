---
layout: base
---

# MATLAB Parameter Update Workflow

This script **shares fitted parameters with other MATLAB models**. It reads parameter values from a CSV file, applies them to the original `.mat` data, and writes a new `.mat` file for repeatable tests.

[MATLAB bridge script](../Test_bridge.m)

## Workflow

### 1. Load the Original `.mat` File
```matlab
orig_file = 'MF612_parameter_new.mat';
load(orig_file);
```
- Load the original parameter file as the base configuration.
- The original data is private.
---

### 2. Load the CSV File
- Read the parameter names and initial values from `Fitting_process.csv`.
- Store the CSV data in the `params` struct.

---

### 3. Group the Parameters
```matlab
Px = [...];   % Longitudinal parameters
Rx = [...];   % Longitudinal correction parameters
Py = [...];   % Lateral parameters
Ry = [...];   % Lateral correction parameters
```
- Group the parameters by purpose.
  - **Px and Rx** contain the longitudinal model parameters.
  - **Py and Ry** contain the lateral model parameters.

---

### 4. Save the New `.mat` File
- Save the updated parameters to a new `.mat` file.
- Other MATLAB models can load the updated parameters directly.

---

## Capabilities
- **Parameter sharing.** Update the `.mat` file with CSV values for cross-model tests.
- **Automation.** The script reads and updates the values automatically.
- **Repeatable testing.** Load the same output `.mat` file into other models to repeat a test.
