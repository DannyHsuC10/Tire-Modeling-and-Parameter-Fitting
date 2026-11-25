# Magic Formula Fy
[Fy source file](../Fy_models.py)
## Pure Lateral Slip Force $Fy0$
### Friction and Stiffness
- **Friction coefficient $\mu_y$ (4.E23)**  
  $$\mu_y = (PDY1 + PDY2 \cdot dfz) \cdot (1 + PPY3 \cdot dpi + PPY4 \cdot dpi^2) \cdot (1 - PDY3 \cdot \sin^2 \gamma) \cdot \lambda_{\mu_yMi}$$
  **Physical meaning.** The lateral friction coefficient determines the peak lateral force at slip and depends on load, inflation pressure, and camber.

- **Cornering stiffness $K_{y\alpha}$ (4.E25)**  
  $$K_{y\alpha} = PKY1 \cdot F_{z0}' \cdot (1 + PPY1 \cdot dpi) \cdot (1 - PKY3 \cdot |\sin \gamma|) \cdot \sin(PKY4 \cdot \arctan(term)) \cdot \lambda_{Kyia} \cdot \zeta_3$$
  where  
  $$term = \frac{F_z / F_{z0}'}{(PKY2 + PKY5 \cdot \sin^2 \gamma) \cdot (1 + PPY2 \cdot dpi)}$$
  **Physical meaning.** The rate at which lateral force rises at small slip angles.

- **Camber stiffness $K_{y\gamma0}$ (4.E30)**  
  $$K_{y\gamma0} = F_z \cdot (PKY6 + PKY7 \cdot dfz) \cdot (1 + PPY5 \cdot dpi) \cdot \lambda_{Kyia}$$
  **Physical meaning.** Describes how camber affects lateral force.
### Curve Shifts
- **Vertical shift $Sv_{\gamma\alpha}$ (4.E28)**  
  $$Sv_{\gamma\alpha} = F_z \cdot (PVY3 + PVY4 \cdot dfz) \cdot \sin \gamma \cdot \lambda_{Kyia} \cdot \lambda_{\mu_y'} \cdot \zeta_2$$
  **Physical meaning.** The camber-induced shift in lateral force.

- **Horizontal shift $Shy$ (4.E27)**  
  $$Shy = (PHY1 + PHY2 \cdot dfz) \cdot \lambda_{Hy} + \frac{(K_{y\gamma0} \cdot \sin \gamma - Sv_{\gamma\alpha}) \cdot \zeta_0}{K_{y\alpha} + \epsilon_y} + \zeta_4 - 1$$
  **Physical meaning.** The slip-angle shift accounts for load and camber.

- **Adjusted slip angle $a_y$ (4.E20)**  
  $$a_y = \alpha^* + Shy$$
  **Physical meaning.** The effective slip angle after applying the shift.

- **Vertical shift $Svy$ (4.E29)**  
  $$Svy = F_z \cdot (PVY1 + PVY2 \cdot dfz) \cdot \lambda_{Vy} \cdot \lambda_{\mu_y'} \cdot \zeta_2 + Sv_{\gamma\alpha}$$
  **Physical meaning.** The lateral force offset accounts for camber and load.
### Main Factors
- **Shape factor $C_y$ (4.E21)**  
  $$C_y = PCY1 \cdot \lambda_{Cy}$$
  **Physical meaning.** Controls the shape of the lateral force curve.

- **Curvature $E_y$ (4.E24)**  
  $$E_y = (PEY1 + PEY2 \cdot dfz) \cdot (1 + PEY4 \cdot \sin^2 \gamma - (PEY3 + PEY5 \cdot \sin \gamma) \cdot \text{sign}(a_y)) \cdot \lambda_{Ey}$$
  **Physical meaning.** Controls how strongly the lateral force curve bends at large slip angles.

- **Peak force $D_y$ (4.E22)**  
  $$D_y = \mu_y \cdot F_z \cdot \zeta_2$$
  **Physical meaning.** The peak lateral force is proportional to the friction coefficient and normal load.

- **Stiffness factor $B_y$ (4.E26)**  
  $$B_y = \frac{K_{y\alpha}}{C_y \cdot D_y + \epsilon_y}$$
  **Physical meaning.** Determines the initial slope of the curve and depends on stiffness and peak force.
### Main Equation
- **Main Magic Formula equation (4.E19)**  
  $$Fy0 = D_y \cdot \sin \Big( C_y \cdot \arctan(B_y \cdot a_y - E_y \cdot (B_y \cdot a_y - \arctan(B_y \cdot a_y))) \Big) + Svy$$
  **Physical meaning.** Describes the nonlinear relationship between slip angle and lateral force.

---

## Combined-Slip Lateral Force $Fy$

Under combined slip, longitudinal slip influences lateral force.
### Scaling Factors
- **Horizontal shift $SH_\kappa$ (4.E64)**  
  $$SH_\kappa = RHY1 + RHY2 \cdot dfz$$
  $$\kappa_S = SL + SH_\kappa$$
  **Physical meaning.** Adjusts the longitudinal slip ratio for load.

- **Stiffness factor $B_{y\kappa}$ (4.E63)**  
  $$B_{y\kappa} = (RBY1 + RBY4 \cdot \sin^2 \gamma) \cdot \cos(\arctan(RBY2 \cdot (\alpha^* - RBY3))) \cdot \lambda_{Yk}$$
  **Physical meaning.** Adjusts stiffness for the interaction between longitudinal slip and slip angle.

- **Shape factor $C_{y\kappa}$ (4.E65)**  
  $$C_{y\kappa} = RCY1$$
  **Physical meaning.** Controls the shape of the lateral force curve under combined slip.

- **Curvature $E_{y\kappa}$ (4.E65)**  
  $$E_{y\kappa} = REY1 + REY2 \cdot dfz$$
  **Physical meaning.** Controls how strongly the lateral force curve bends under combined slip.

- **Weighting function $G_{y\kappa}$**  
  $$G_{y\kappa}(x) = \cos \Big( C_{y\kappa} \cdot \arctan(B_{y\kappa} \cdot x - E_{y\kappa} \cdot (B_{y\kappa} \cdot x - \arctan(B_{y\kappa} \cdot x))) \Big)$$
  $$G_{y\kappa0} = G_{y\kappa}(SH_\kappa)$$
  $$G_{y\kappa} = \frac{G_{y\kappa}(\kappa_S)}{G_{y\kappa0} + \epsilon_y}$$
  **Physical meaning.** Describes how longitudinal slip reduces lateral force.
### Shift Terms
- **Friction coefficient $\mu_y$ (for DVκ)**  
  $$\mu_y = (PDY1 + PDY2 \cdot dfz) \cdot (1 + PPY3 \cdot dpi + PPY4 \cdot dpi^2) \cdot (1 - PDY3 \cdot \sin^2 \gamma) \cdot \lambda_{\mu_y}$$
  
  **Physical meaning.** The lateral friction coefficient under combined slip.

- **Peak correction $DV_\kappa$ (4.E66)**  
  $$D_{V\kappa} = \mu_y \cdot F_z \cdot (RVY1 + RVY2 \cdot dfz + RVY3 \cdot \sin \gamma) \cdot \cos(RVY4 \cdot \alpha^*)$$
  **Physical meaning.** Adjusts the peak for the interaction between longitudinal slip and slip angle.

- **Shift $SV_\kappa$ (4.E67)**  
  $$S_{V\kappa }=D_{V\kappa }\cdot \sin (RVY5\cdot \arctan (RVY6\cdot SL))\cdot \lambda_{Vyk}$$

  **Physical meaning.** Represents the lateral force offset introduced by longitudinal slip.
### Combined-Slip Force
- **Combined-slip lateral force**  
  $$Fy = Fy0 \cdot G_{y\kappa} + SV_\kappa$$
  **Physical meaning.** Combines the pure lateral slip force, longitudinal-slip weighting, and force shift to account for the interaction between longitudinal slip and slip angle.

