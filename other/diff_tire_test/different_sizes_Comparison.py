import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
from Pacejka_MF_model.model.api import MF_Universal_solver,load_tir,CalculationInput
import pandas as pd

# 固定輸入
SL = 0.0
IA = 0.0
P  = 84080.0
output = "FY" # FX,FY,MX,MZ
# 掃過
SA_range = np.linspace(-15, 15, 50)
FZ_range = np.linspace(0, 2000, 50)
D2704_mf612 = load_tir("D2704_mf612.tir")# 紅心13吋
tir_params_fit = load_tir("FSAE_43075R20.tir")# 新的擬合結果
base_dir = Path(__file__).resolve().parent  # magic_formula/
#==================================================================================================
#　建立曲面
SA_grid, FZ_grid = np.meshgrid(SA_range, FZ_range)

F_1 = np.zeros_like(SA_grid)
F_2 = np.zeros_like(SA_grid)

# 迴圈
for i in range(SA_grid.shape[0]):
    for j in range(SA_grid.shape[1]):

        FZ = float(FZ_grid[i, j])
        SA = float(SA_grid[i, j])

        MF = CalculationInput(
        FZ=FZ,
        SA=SA,
        SL=SL,
        IA=IA,
        pressure=P,
        tir_params=D2704_mf612)

        MF2 = CalculationInput(
        FZ=FZ,
        SA=SA,
        SL=SL,
        IA=IA,
        pressure=P,
        tir_params=tir_params_fit)

        F_1[i, j] = MF_Universal_solver(output, MF)
        F_2[i, j] = MF_Universal_solver(output, MF2)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(
    SA_grid,
    FZ_grid,
    F_2,
    color='blue',
    alpha=0.5
)

wire = ax.plot_wireframe(
    SA_grid,
    FZ_grid,
    F_1,
    color='red',
    linewidth=0.8
)

Fx_error = F_1 - F_2
#ax.plot_surface(SA_grid, FZ_grid, Fx_error)
# 出圖
ax.set_xlabel("Slip angle (SA)")
ax.set_ylabel("Vertical Load (FZ)")
ax.set_zlabel("FY")
fig.savefig(base_dir / "Figures" / f"Fy_compar", dpi=300, bbox_inches='tight')
ax.view_init(elev=0, azim=0)# 俯視圖
plt.show()

Fx_error = (F_1 - F_2)/F_1 * 100

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(SA_grid, FZ_grid, Fx_error)

ax.set_xlabel("Slip angle (SA)")
ax.set_ylabel("FZ")
ax.set_zlabel("FY Error (%)")
fig.savefig(base_dir / "Figures" / f"Fy_delta", dpi=300, bbox_inches='tight')
ax.view_init(elev=0, azim=90)# 俯視圖
ax.set_zlim(-50, 50)
plt.show()