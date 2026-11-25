# Linear Regression
* [Regression source file](../Linear_Regression.py)
Linear regression models the relationship between an independent and a dependent variable. For vertical tire stiffness, it estimates stiffness $k$ and preload $b$.

## Basic Equations

The general linear regression model is shown below.
$$R = k \cdot (R0 - RL) + b$$

To force the fit through the origin, use the following form.
$$R = k \cdot (R0 - RL)$$

The terms are defined below.
- $R$ is the vertical force (FZ).
- $R0$ is the unloaded radius.
- $RL$ is the loaded radius.
- $k$ is the vertical stiffness.
- $b$ is the preload.

## Physical Meaning

- **Vertical stiffness $k$** measures resistance to vertical compression. A larger value indicates a stiffer tire.
- **Preload $b$** is the initial force at zero compression.
- **Displacement $\Delta = R0 - RL$** is the tire's compression under load.

## Linear Regression Steps

1. **Build the design matrix.**  
   Construct the matrix using compression $x = R0 - RL$ and vertical force $y = |FZ|$.
   $$X = \begin{bmatrix} x & 1 \end{bmatrix}$$

2. **Solve by least squares.**  
   Solve for the parameter vector.
   $$\beta = (X^T X)^{-1} X^T y$$
   Here, $\beta = \begin{bmatrix} k \\ b \end{bmatrix}$.

3. **Force the fit through the origin.**  
   With the intercept $b$ fixed at zero, calculate stiffness $k$ as follows.
   $$k = \frac{\sum (x \cdot y)}{\sum (x^2)}$$

## Evaluation Metrics

- **Coefficient of determination $R^2$** measures the proportion of variation explained by the fit.  
  $$R^2 = 1 - \frac{\sum (y - y_{pred})^2}{\sum (y - \bar{y})^2}$$

- **Root mean square error (RMSE)** measures how far predictions differ from observations.  
  $$RMSE = \sqrt{\frac{1}{n} \sum (y - y_{pred})^2}$$
