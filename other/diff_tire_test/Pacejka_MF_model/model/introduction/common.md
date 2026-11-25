# Magic Formula Base Class
[Base class source file](../_common.py)
## Normalizing Normal Load with `_normalize_load`

- **Equation**  
  $$F_{z0}' = LFZO \cdot FNOMIN$$
  $$dfz = \frac{F_z - F_{z0}'}{F_{z0}' + \epsilon}$$

- **Physical meaning**  
  - $F_{z0}'$ is the reference normal force, typically the nominal load.  
  - $dfz$ is the deviation of the actual normal load relative to the reference load. Normalization keeps the model consistent across load conditions.

---

## Normalizing Inflation Pressure with `_normalize_pressure`

- **Equation**  
  $$dpi = \frac{p - PIO}{PIO}$$
  $$dpi^2 = dpi^2$$

- **Physical meaning**  
  - $dpi$ is the fractional deviation of inflation pressure from the reference pressure $PIO$.  
  - $dpi^2$ captures second-order effects of pressure variation on stiffness and friction.

---

## Normalizing Angles with `_normalize_angles`

- **Equation**  
  $$SA_{rad} = \text{radians}(SA)$$
  $$IA_{rad} = \text{radians}(IA)$$
  $$a_{mi} = \tan(SA_{rad})$$
  $$ia_{Mi} = \sin(IA_{rad})$$
  $$ia_{Mi}^2 = (\sin(IA_{rad}))^2$$

- **Physical meaning**  
  - $a_{mi}$ is the tangent of the slip angle and captures its effect on lateral force.  
  - $ia_{Mi}$ is the sine of the camber angle and captures the effect of tire inclination on moments and lateral force.  
  - $ia_{Mi}^2$ captures nonlinear camber effects.  
