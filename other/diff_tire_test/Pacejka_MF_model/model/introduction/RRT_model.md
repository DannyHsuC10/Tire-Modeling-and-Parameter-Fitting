# Magic Formula Calculations for Rolling Resistance Moment $RRT$
[RRT source file](../RRT_models.py)

Calculate the required input force first using [Fx](Fx_model.md).
## Magic Formula Model

- **Rolling resistance coefficient $f_{rr}$**  
  $$
  f_{rr} = QSY1
  + QSY2 \cdot \frac{F_x}{F_{z0}' + \epsilon}
  + QSY3 \cdot V
  + QSY4 \cdot V^4
  + QSY5 \cdot \gamma^2
  + QSY6 \cdot \gamma^2 \cdot \frac{F_z}{F_{z0}' + \epsilon}
  $$
  **Physical meaning.** Represents energy lost to tire deformation and friction during rolling, accounting for longitudinal force, speed, camber, and load.

- **Correction terms**  
  $$f_{rr} \leftarrow f_{rr} \cdot (1 + QSY7 \cdot dfz + QSY8 \cdot dpi)$$
  **Physical meaning.** Adjust the rolling resistance coefficient for changes in load ($dfz$) and inflation pressure ($dpi$).

- **Rolling resistance moment**  
  $$PPT = -R_o \cdot F_z \cdot f_{rr}$$
  **Physical meaning.** The moment is proportional to tire radius $R_o$, normal load $F_z$, and the rolling resistance coefficient. The negative sign indicates opposition to forward motion.

---

## SAE Model

- **Individual terms**  
  $$R1 = \frac{K'}{c1}, \quad R2 = c2$$
  $$R3 = \frac{c3 + c4 \cdot F_z}{p}, \quad R4 = \frac{c5 + c6 \cdot F_z}{p} \cdot v^2$$
  **Physical meaning.** The terms represent different contributions to rolling resistance.  
  - $R1$ is the baseline scale factor.  
  - $R2$ is the constant term.  
  - $R3$ accounts for load and inflation pressure.  
  - $R4$ accounts for the speed-squared contribution, including interaction with rolling fluctuations.

- **Rolling resistance coefficient**  
  $$C_{rr} = R1 \cdot (R2 + R3 + R4)$$
  **Physical meaning.** Combines the contributions to rolling resistance.

- **Rolling resistance**  
  $$F_r = C_{rr} \cdot F_z$$
  **Physical meaning.** The resulting force is proportional to normal load and represents energy consumed as the tire rolls.