# Magic Formula Mz
[Mz source file](../Mz_models.py)

Calculate the required input force first using [Fy](Fy_model.md).

Calculate the required input force first using [Fx](Fx_model.md).

## Aligning Moment from Lateral Force $Mzt$

### Equivalent Slip Angle
$$
\alpha_t^{eq} = \sqrt{\alpha^2 + \kappa^2 \left(\frac{K_{x\kappa}}{K_{y\alpha}'}\right)^2} \cdot \text{sign}(\alpha)
$$

**Physical meaning**  
Combines longitudinal slip $\kappa$ and slip angle $\alpha$ into an equivalent angle to account for **combined slip**.

---

### Adjusted Cornering Stiffness
$$
K_{y\alpha}' = K_{y\alpha} + \epsilon_K
$$

**Physical meaning**  
Prevents a zero denominator and adjusts stiffness at low load.

---

### Pneumatic Trail Shift
$$
S_{ht} = QHZ1 + QHZ2 \cdot dfz + (QHZ3 + QHZ4 \cdot dfz)\cdot ia
$$

$$
\alpha_t = \alpha_m + S_{ht}
$$

**Physical meaning**  
Represents a shift in the center of pressure within the contact patch, which moves the aligning moment curve horizontally.

---

### Stiffness Factor $B_t$
$$
B_t = (QBZ1 + QBZ2 \cdot dfz + QBZ3 \cdot dfz^2)
\cdot (1 + QBZ5|ia| + QBZ4 ia)
\cdot \frac{\lambda_{y\alpha}}{\lambda_{\mu y}}
$$

**Physical meaning**  
Controls the sensitivity of pneumatic trail to slip angle.

---

### Shape Factor
$$
C_t = QCZ1
$$

**Physical meaning**  
Controls the overall shape of the curve.

---

### Curvature Factor
$$
E_t = (QEZ1 + QEZ2 \cdot dfz + QEZ3 \cdot dfz^2)
\cdot \left[1 + (QEZ4 + QEZ5 ia)\frac{2}{\pi}\arctan(B_t C_t \alpha_t)\right]
$$

**Physical meaning**  
Controls saturation and nonlinearity of pneumatic trail at large slip angles.

---

### Peak Trail
$$
D_t = D_{t0} \cdot (1 + QDZ3 |ia| + QDZ4 ia^2)\cdot \zeta_5
$$

where
$$
D_{t0} = F_z \cdot \frac{R_0}{F_{z0}'} \cdot (QDZ1 + QDZ2 dfz)
\cdot (1 - PPZ1 \cdot dpi)\cdot \lambda_{MP} \cdot \text{sign}(V_x)
$$

**Physical meaning**  
The maximum pneumatic trail depends on load, inflation pressure, and tire radius.

---

### Pneumatic trail
$$
t = D_t \cdot \cos\left(C_t \cdot \arctan\left(B_t \alpha_t^{eq} - E_t(B_t \alpha_t^{eq} - \arctan(B_t \alpha_t^{eq}))\right)\right)
$$

**Physical meaning**  
Measures how far the contact force acts from the center of the tire.

---

### Aligning Moment from Lateral Force
$$
M_{zt} = -t \cdot F_y
$$

**Physical meaning**  
The aligning moment is the lateral force times its moment arm, the pneumatic trail.  
The negative sign indicates that the moment tends to straighten the wheel.

---

## Pure Lateral Slip Aligning Moment $Mz$

### Equivalent Slip Angle
$$
\alpha_r^{eq} = \sqrt{\alpha_r^2 + \kappa^2 \left(\frac{K_{x\kappa}}{K_{y\alpha}'}\right)^2} \cdot \text{sign}(\alpha_r)
$$

**Physical meaning**  
As with $Mzt$, use an equivalent angle that accounts for longitudinal and lateral slip coupling.

---

### Shift Correction
$$
S_{hf} = S_{hy} + \frac{S_{vy}}{K_{y\alpha}'}
$$

$$
\alpha_r = \alpha_m + S_{hf}
$$

**Physical meaning**  
Accounts for how a lateral force shift affects the aligning moment.

---

### Stiffness Factor
$$
B_r = (QBZ9 \cdot \frac{\lambda_{y\alpha}}{\lambda_{\mu y}} + QBZ10 \cdot B_y C_y)\cdot \zeta_6
$$

**Physical meaning**  
Controls how sensitive the residual aligning moment is to slip angle.

---

### Shape Factor
$$
C_r = \zeta_7
$$

**Physical meaning**  
Controls the shape of the residual aligning moment curve.

---

### Amplitude
$$
D_r = F_z R_0 \cdot \Big[
(QDZ6 + QDZ7 dfz)\lambda_{RES}\zeta_2
+ ((QDZ8 + QDZ9 dfz)(1 + PPZ2 dpi)
+ (QDZ10 + QDZ11 dfz)|ia|)
\cdot ia \cdot \lambda_{KZC}\zeta_0
\Big]
\cdot \lambda_{\mu y} \cdot \cos(\alpha')
$$

**Physical meaning**  
The magnitude of the residual aligning moment depends on
- Tire deformation.
- Camber effects.
- Asymmetry in the contact patch.

---

### Residual Aligning Moment
$$
M_{zr} = D_r \cdot \cos\left(C_r \cdot \arctan(B_r \alpha_r^{eq})\right)
$$

**Physical meaning**  
This moment remains at high slip after pneumatic trail falls to zero.

---

### Moment Offset Term
$$
s = R_0 \cdot (SSZ1 + SSZ2 \frac{F_y}{F_{z0}'} + (SSZ3 + SSZ4 dfz) ia)\cdot \lambda_S
$$

$$
M_{z,offset} = s \cdot F_x
$$

**Physical meaning**  
Longitudinal force $F_x$ acts through an offset and produces an additional aligning moment.

---

## Total Aligning Moment
$$
M_z = M_{zt} + M_{zr} + s \cdot F_x
$$

**Physical meaning**  
The total aligning moment has three components.
1. **$M_{zt}$** is lateral force times pneumatic trail, the main contribution.
2. **$M_{zr}$** is the residual aligning moment that persists at high slip.
3. **$sF_x$** is the additional moment from longitudinal force.
