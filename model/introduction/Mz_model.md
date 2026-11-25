---
layout: base
---

# Magic Formula Mz
[Mz source file](../Mz_models.py)

Calculate the required input force first using [Fx](Fx_model.md).

Calculate the required input force first using [Fy](Fy_model.md).
## Initial Calculations
### Equation Factors
- Stiffness factor  
$$B_t = (QBZ1 + QBZ2 \cdot dfz + QBZ3 \cdot dfz^2)(1 + QBZ5 \cdot |ia_{Mi}| + QBZ4 \cdot ia_{Mi}) \cdot LYKA$$

- Shape factor  
$$C_t = QCZ1$$

- Peak moment $D_r$  
$$D_r = F_z \cdot R_o \cdot \Big( (QDZ6 + QDZ7 \cdot dfz) \cdot LMP \cdot \zeta_2 
+ (QDZ8 + QDZ9 \cdot dfz)(1 + PPZ2 \cdot dfz) \cdot |ia_{Mi}| \cdot ia_{Mi} \cdot LKYC \cdot \zeta_0 \Big) \cdot LMUY \cdot \zeta_4 \cdot \cos(V) + \zeta_8 - 1$$

- Initial trail  
$$D_{t0} = \frac{F_z \cdot R_o}{F_{z0}' + \epsilon} \cdot (QDZ1 + QDZ2 \cdot dfz)(1 - PPZ1 \cdot dpi) \cdot vsign \cdot LRES$$

- Adjusted trail  
$$D_t = D_{t0}(1 + QDZ3 \cdot |ia_{Mi}| + QDZ4 \cdot ia_{Mi}^2) \cdot \zeta_5$$

- Curvature  
$$E_t = (QEZ1 + QEZ2 \cdot dfz + QEZ3 \cdot dfz^2)(1 + (QEZ4 + QEZ5 \cdot ia_{Mi}) \cdot \tfrac{2}{\pi} \cdot \arctan(B_t \cdot \alpha_{mi}))$$

- Adjusted angle  
$$a_t = \alpha_{mi} + QHZ1 + QHZ2 \cdot dfz + (QHZ3 + QHZ4 \cdot dfz) \cdot ia_{Mi}$$

- Pneumatic trail：  

$$t_0 = D_t \cdot \cos\Big(C_t \cdot \arctan(B_t \cdot a_t - E_t(B_t \cdot a_t - \arctan(B_t \cdot a_t)))\Big) \cdot \cos(V)$$

### Stiffness and Friction
- Cornering stiffness  
$$K_{ya} = PKY1 \cdot F_{z0}'(1 + PPY1 \cdot dpi)(1 - PKY3 \cdot |ia_{Mi}|)\sin(PKY4 \cdot \arctan(term)) \cdot LYKA \cdot \zeta_3$$
where  
$$term = \frac{F_z / F_{z0}'}{(PKY2 + PKY5 \cdot ia_{Mi})(1 + PPY2 \cdot dpi)}$$

- Friction coefficient  
$$\mu_y = (PDY1 + PDY2 \cdot dfz)(1 + PPY3 \cdot dpi + PPY4 \cdot dpi^2)(1 - PDY3 \cdot ia_{Mi}) \cdot LMUY$$

- Stiffness factor  
$$B_y = \frac{K_{ya}}{C_y \cdot D_y + \epsilon_y}, \quad C_y = PCY1 \cdot LCY, \quad D_y = \mu_y \cdot F_z \cdot \zeta_2$$

- Aligning moment stiffness  
$$B_r = (QBZ9 \cdot LKZC / LMUY + QBZ10 \cdot B_y \cdot C_y) \cdot \zeta_6$$

### Initial Aligning Moment
- Trail contribution  
$$M_{zo}' = -t_0 \cdot F_{y0}$$

- Stiffness contribution  
$$M_{zr0} = D_r \cdot \cos(C_r \cdot \arctan(B_r)), \quad C_r = \zeta_7$$

- Pure lateral slip aligning moment  
$$Mz0 = M_{zo}' + M_{zr0}$$

---

## Combined-Slip Aligning Moment $Mz$

### Adjusted Slip Angle
$$\alpha^* = \tan(\text{radians}(SA))$$
$$\cos(\alpha^*) = \frac{1}{\sqrt{1 + (\alpha^*)^2}}$$

### Stiffness Calculation
- Longitudinal stiffness  
$$
K_{xk} = F_z(PKX1 + PKX2 \cdot dfz)e^{PKX3 \cdot dfz}(1 + PPX1 \cdot dpi + PPX2 \cdot dpi^2) \cdot LKX
$$

- Cornering stiffness  
Use the $K_{ya}$ calculation above.  

### Correction Terms
- Trail correction  
$$s = R_o(SSZ1 + SSZ2 \cdot \tfrac{F_y}{F_{z0}'} + (SSZ3 + SSZ4 \cdot dfz) \cdot ia_{Mi}) \cdot LS$$

- Adjusted stiffness  
$$K_{ya}' = K_{ya} + \epsilon_K$$

- Longitudinal-to-lateral stiffness ratio  
$$\left(\frac{K_{xk}}{K_{ya}'}\right)^2$$

- Equivalent angle  
$$\alpha_{tEq} = \sqrt{(\text{radians}(SA))^2 + SL^2 \cdot \left(\frac{K_{xk}}{K_{ya}'}\right)^2} \cdot \text{sign}(\text{radians}(SA))$$

- Adjusted aligning moment  
$$M_{zr} = D_r \cdot \cos(C_r \cdot \arctan(B_r \cdot \alpha_{tEq}))$$

### Final Aligning Moment
- Base correction  
$$Mz_{Fybase} = \cos(\alpha^*) \cdot \frac{F_y}{F_{y0} + \epsilon}$$

- Final equation  
$$Mz = Mz0 \cdot Mz_{Fybase} + M_{zr} + F_x \cdot s^2$$