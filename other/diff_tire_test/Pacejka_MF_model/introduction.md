# Pacejka_MF_model
## Introduction
Pacejka_MF_model predicts tire forces and moments. You can call it using the API in the following example.
* [Demo source file](Demo.py)
```python
from model import api  # Import the model API

tir_params = api.load_tir("D2704_mf612.tir")  # Load the tire parameter file

MF = api.CalculationInput(  # Set the Magic Formula inputs
            FZ=800,
            SA=1,
            SL=0.25,
            IA=0.0,
            V = 10,
            pressure=80000,
            tir_params=tir_params
        )
# MF_Universal_solver returns FX, FY, MX, RRT, or MZ. Pass the output code and the MF input object.
Fx = api.MF_Universal_solver("FX", MF)  # Calculate longitudinal force
Fy = api.MF_Universal_solver("FY", MF)  # Calculate lateral force

print("Fx:", Fx)  # Print the result
print("Fy:", Fy)

```
## Supporting Tools
This package contains a subset of the tools from the full Magic Formula fitting project.

1. The [plotting tester](/Pacejka_MF_model/introduction/MF_tester.md) provides a quick way to analyze tire performance.
2. The [example plots](/Pacejka_MF_model/Figures/MF_plt.md) are updated when you run the plotting tester.
3. The [tire model documentation](/Pacejka_MF_model/introduction/magic_formula_model.md) explains how the model works.