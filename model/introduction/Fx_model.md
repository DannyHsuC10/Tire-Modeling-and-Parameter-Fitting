---
layout: base
---

# Magic Formula Fx
[Fx source file](../Fx_models.py)
## Pure Longitudinal Slip Force $Fx0$
### Curve Shifts
- **Horizontal shift (Shx)**  
  $$Shx = (PHX1 + PHX2 \cdot dfz) \cdot \lambda_{Hx}$$
  $$\kappa_x = \kappa + Shx$$
  **Physical meaning.** Adjusts the slip ratio for shifts caused by changes in load.

- **Vertical shift (Svx)**  
  $$Svx = F_z \cdot (PVX1 + PVX2 \cdot dfz) \cdot \lambda_{Vx} \cdot \lambda_{\mu_x'} \cdot \zeta_1$$
  **Physical meaning.** Offsets longitudinal force to account for inflation pressure and load.

- **Curvature $E_x$**  
  $$E_x = (PEX1 + PEX2 \cdot dfz + PEX3 \cdot dfz^2) \cdot (1 - PEX4 \cdot \text{sign}(\kappa_x)) \cdot \lambda_{Ex}$$
  **Physical meaning.** Controls how strongly the longitudinal force curve bends at high slip ratios.
## Main Factors
- **Shape factor $C_x$**  
  $$C_x = PCX1 \cdot \lambda_{Cx}$$
  **Physical meaning.** Controls the shape of the longitudinal force curve.

- **Stiffness $K_{xk}$**  
  $$K_{xk} = F_z \cdot (PKX1 + PKX2 \cdot dfz) \cdot e^{PKX3 \cdot dfz} \cdot (1 + PPX1 \cdot dpi + PPX2 \cdot dpi^2) \cdot \lambda_{Kxk}$$
  **Physical meaning.** Describes how quickly longitudinal force rises at small slip ratios.

- **Friction coefficient $\mu_x$**  
  $$\mu_x = (PDX1 + PDX2 \cdot dfz) \cdot (1 + PPX3 \cdot dpi + PPX4 \cdot dpi^2) \cdot (1 - PDX3 \cdot ia_{Mi}^2) \cdot \lambda_{\mu_xMi} \cdot \lambda_{Mi}$$
  **Physical meaning.** Represents how inflation pressure, load, and camber affect longitudinal friction.

- **Peak force $D_x$**  
  $$D_x = \mu_x \cdot F_z \cdot \zeta_2$$
  **Physical meaning.** The peak longitudinal force is proportional to the friction coefficient and normal load.

- **Stiffness factor $B_x$**  
  $$B_x = \frac{K_{xk}}{C_x \cdot D_x + \epsilon_x}$$
  **Physical meaning.** Determines the initial slope of the curve and depends on stiffness and peak force.
### Main Equation
- **Main Magic Formula equation**  
  $$Fx0 = D_x \cdot \sin \Big( C_x \cdot \arctan \big( B_x \cdot \kappa_x - E_x \cdot (B_x \cdot \kappa_x - \arctan(B_x \cdot \kappa_x)) \big) \Big) + Svx$$
  **Physical meaning.** Describes the nonlinear relationship between slip ratio and longitudinal force.

---

## Combined-Slip Longitudinal Force $Fx$

Under combined slip, the slip angle influences longitudinal force.

- **Slip angle shift**  
  $$SH_{xa} = RHX1$$
  $$\alpha_S = \alpha_{mi} + SH_{xa}$$
  **Physical meaning.** Adjusts the slip angle for load and geometric offsets.

- **Correction factors $B_{xa}, C_{xa}, E_{xa}$**  
  $$B_{xa} = (RBX1 + RBX3 \cdot ia_{Mi}^2) \cdot \cos(\arctan(RBX2 \cdot \kappa)) \cdot \lambda_{xa}$$
  $$C_{xa} = RCX1$$
  $$E_{xa} = REX1 + REX2 \cdot dfz$$
  **Physical meaning.** Determine how longitudinal force changes with slip angle.

- **Weighting function $G_x$**  
  $$G_x(x) = \cos \Big( C_{xa} \cdot \arctan \big( B_{xa} \cdot x - E_{xa} \cdot (B_{xa} \cdot x - \arctan(B_{xa} \cdot x)) \big) \Big)$$
  **Physical meaning.** Describes the reduction in longitudinal force as slip angle changes.

- **Normalization ratio**  
  $$G_{x0} = G_x(SH_a)$$
  $$G_{xa} = \frac{G_x(\alpha_S)}{G_{x0}}$$
  **Physical meaning.** Normalizes the weighting function for numerical stability.

- **Combined-slip longitudinal force**  
  $$Fx = Fx0 \cdot G_{xa}$$
  **Physical meaning.** The final longitudinal force accounts for the interaction between slip ratio and slip angle.
