---
layout: base
---

# Magic Formula Mx

[Mx source file](../Mx_models.py)

Calculate the required input force first using [Fy](Fy_model.md).
## Basic Transformations
- **Lateral force ratio**  
  $$F_{y_{ratio}} = \frac{F_y}{F_{z0}' + \epsilon}$$
  **Physical meaning.** Normalizes lateral force to remove the effect of load magnitude when comparing moments across operating conditions.

- **Normal force ratio**  
  $$F_{z_{ratio}} = \frac{F_z}{F_{z0}' + \epsilon}$$
  **Physical meaning.** Expresses the tire normal force relative to the reference load.

---

## Overturning Moment Equation

- **First term $Q_1$**  
  $$Q_1 = QSX1 \cdot \lambda_{VMX} - QSX2 \cdot \iota_a \cdot (1 + PPMX1 \cdot dpi)$$
  **Physical meaning.** Combines a baseline term with a correction for camber.

- **Second term $Q_2$**  
  $$Q_2 = QSX3 \cdot F_{y_{ratio}} + QSX4 \cdot \cos(QSX5 \cdot \arctan(QSX6 \cdot F_{z_{ratio}})^2)$$
  **Physical meaning.** Accounts for the interaction between the lateral and normal force ratios.

- **Third term $Q_3$**  
  $$Q_3 = QSX7 \cdot \iota_a + QSX8 \cdot \arctan(QSX9 \cdot F_{y_{ratio}})$$
  **Physical meaning.** Accounts for the interaction between camber and the lateral force ratio.

- **Fourth term $Q_4$**  
  $$Q_4 = QSX10 \cdot \arctan(QSX11 \cdot F_{z_{ratio}}) \cdot \iota_a$$
  **Physical meaning.** Accounts for the interaction between the normal force ratio and camber.

- **Combined term $Q$**  
  $$Q = Q_1 + Q_2 \cdot \sin(Q_3) + Q_4$$
  **Physical meaning.** Combines the baseline, lateral force, normal force, and camber contributions to the moment coefficient.

- **Final overturning moment**  
  $$M_x = R_o \cdot F_z \cdot Q \cdot \lambda_{MX}$$
  **Physical meaning.** The overturning moment is proportional to tire radius $R_o$, normal load $F_z$, and correction factor $Q$.
