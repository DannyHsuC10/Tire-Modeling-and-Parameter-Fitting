---
layout: base
---

# MF_fitter 
[Fitter source file](../MF_fitter.py)
## 1. Fitting Concept
MF_fitter uses **nonlinear least squares** to fit parameters. It minimizes the sum of squared residuals between model predictions and measured values.

$$
\min_{\mathbf{x}} \; \sum_{i=1}^{n} \left( F_{\text{pred},i}(\mathbf{x}) - F_{\text{meas},i} \right)^2
$$

The terms are defined below.
- $F_{\text{pred},i}(\mathbf{x})$ is the model prediction for the $i$th input.  
- $F_{\text{meas},i}$ is the measured value.  
- $\mathbf{x}$ is the parameter vector to fit.  

## 2. Residual Function
Define the residual function as follows.

$$
r_i(\mathbf{x}) = F_{\text{pred},i}(\mathbf{x}) - F_{\text{meas},i}
$$

The residual vector is

$$
\mathbf{r}(\mathbf{x}) = 
\begin{bmatrix}
r_1(\mathbf{x}) \\
r_2(\mathbf{x}) \\
\vdots \\
r_n(\mathbf{x})
\end{bmatrix}
$$

and the minimization problem becomes

$$
\min_{\mathbf{x}} \; \|\mathbf{r}(\mathbf{x})\|^2
$$

## 3. Packing and Unpacking Parameters
The optimizer updates only the parameters active in the current stage.  
- **Pack.** Combine the parameters selected by $active\_keys$ into vector $\mathbf{x}$ and set its lower and upper bounds $lb, ub$.  
- **Unpack.** Write the optimized values in $\mathbf{x}$ back into the full $stage\_params$ dictionary.

## 4. Parameter Bounds
The optimizer uses lower and upper parameter bounds to keep solutions within valid ranges.

$$
lb_j \leq x_j \leq ub_j
$$

The terms are defined below.
- $lb_j$ is the lower bound for the $j$th parameter.  
- $ub_j$ is the upper bound for the $j$th parameter.  

## 5. Optimization Method
MF_fitter uses **scipy.optimize.least_squares** with the following settings.
- Trust Region Reflective (TRF) method.  
- Soft L1 loss to reduce the influence of outliers.  

$$
\text{loss}(r) = 2 \left( \sqrt{1 + \frac{r^2}{2}} - 1 \right)
$$

For large $r$, this loss grows approximately linearly, reducing the influence of outliers.

## 6. Model Inputs and Outputs
The model takes the following inputs.
- $FZ$ is the vertical load.  
- $SA$ is the slip angle.  
- $SL$ is the slip ratio.  
- $IA$ is the inclination angle, or camber.  
- $pressure$ is the tire inflation pressure.  
- $Ro$ is the tire radius.  
- $V$ is the speed.  

The selected $out$ value (Fx, Fy, Mx, Mz, or RRT) determines which force or moment the model returns.

## 7. Fitting Workflow
1. **Initialize.** Choose the parameters to fit and set their bounds.  
2. **Pack.** Assemble the parameters into a vector.  
3. **Calculate residuals.** Compare model predictions with measured values.  
4. **Optimize.** Update parameters using least squares.  
5. **Unpack.** Write the best solution back into the full parameter dictionary.  

The resulting parameter set minimizes the discrepancy between predictions and measurements for the supplied inputs.