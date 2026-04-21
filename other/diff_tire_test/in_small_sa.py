import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from Pacejka_MF_model.model.api import load_tir,MF_Universal_solver,CalculationInput
import pandas as pd

# 固定輸入
SL = 0.0
IA = 0.0
P  = 84080.0
output = "FY" # FX,FY,MX,MZ
SA_SET = 1.5
# 掃過
SA_range = np.linspace(-SA_SET,SA_SET, 50)
SA_range = np.array(SA_range)
border_scale = (len(SA_range)-5)/len(SA_range)# 避免邊界效應

FZ_range = np.linspace(0, 2000, 50)
D2704_mf612 = load_tir("D2704_mf612.tir")# 紅心13吋
tir_params_fit = load_tir("FSAE_43075R20.tir")# 新的擬合結果

base_dir = Path(__file__).resolve().parent  # magic_formula/
# ==================================================================================================(2D圖形建立)

FZ_target = 882.9  # 固定正向力

MF = CalculationInput(
FZ=FZ_target,
SA=SA_range,
SL=SL,
IA=IA,
pressure=P,
tir_params=D2704_mf612)

MF2 = CalculationInput(
FZ=FZ_target,
SA=SA_range,
SL=SL,
IA=IA,
pressure=P,
tir_params=tir_params_fit)

F_1_fixed = MF_Universal_solver(output, MF)
F_2_fixed = MF_Universal_solver(output, MF2)
F_1_fixed = np.array(F_1_fixed)
F_2_fixed = np.array(F_2_fixed)
# 畫誤差圖
plt.figure(figsize=(7,5))
plt.plot(SA_range, F_1_fixed, color='purple', label='Original Model')
plt.plot(SA_range, F_2_fixed, color='blue', linestyle='--', label='Fitted Model')
plt.plot(SA_range, F_1_fixed-F_2_fixed, color='red', linestyle=':', label='delta')
plt.xlabel("Slip angle (SA)")
plt.ylabel("FY (N)")
plt.title(f"FY vs SA at FZ = {FZ_target} N")
plt.legend()
plt.grid(True)
plt.savefig(base_dir / "Figures" / f"Fy_compar_fixload", dpi=300, bbox_inches='tight')
plt.show()

# ==================================================================================================(斜率誤差分析)

# 已知數據
# SA_range, F_1_fixed, F_2_fixed 已存在
# 確保是 numpy array
SA_range = np.array(SA_range)
F_1_fixed = np.array(F_1_fixed)
F_2_fixed = np.array(F_2_fixed)

# 1️⃣ 計算斜率（一次微分）
dF1_dSA = np.gradient(F_1_fixed, SA_range)
dF2_dSA = np.gradient(F_2_fixed, SA_range)

# 2️⃣ 計算斜率變化率（二次微分）
d2F1_dSA2 = np.gradient(dF1_dSA, SA_range)
d2F2_dSA2 = np.gradient(dF2_dSA, SA_range)

# 3️⃣ 計算誤差
slope_error = dF1_dSA - dF2_dSA           # 斜率差
slope_rate_error = d2F1_dSA2 - d2F2_dSA2 # 斜率變化率差

# --------------------------
# 畫圖

plt.figure(figsize=(12,8))

plt.subplot(2,2,1)
plt.plot(SA_range, dF1_dSA, color='red', label='Original dF/dSA')
plt.plot(SA_range, dF2_dSA, color='blue', linestyle='--', label='Fitted dF/dSA')
plt.xlabel("SA")
plt.ylabel("Slope (dF/dSA)")
plt.title("Slope vs Slip Angle")
plt.legend()
plt.xlim(-SA_SET*border_scale, SA_SET*border_scale)
plt.grid(True)

plt.subplot(2,2,2)
plt.plot(SA_range, slope_error, color='purple')
plt.xlabel("SA")
plt.ylabel("Slope Error (dF1-dF2)")
plt.title("Slope Difference")
plt.xlim(-SA_SET*border_scale, SA_SET*border_scale)
plt.grid(True)

plt.subplot(2,2,3)
plt.plot(SA_range, d2F1_dSA2, color='red', label='Original d²F/dSA²')
plt.plot(SA_range, d2F2_dSA2, color='blue', linestyle='--', label='Fitted d²F/dSA²')
plt.xlabel("SA")
plt.ylabel("Slope Rate (d²F/dSA²)")
plt.title("Slope Rate vs Slip Angle")
plt.legend()
plt.xlim(-SA_SET*border_scale, SA_SET*border_scale)
plt.grid(True)

plt.subplot(2,2,4)
plt.plot(SA_range, slope_rate_error, color='purple')
plt.xlabel("SA")
plt.ylabel("Slope Rate Error")
plt.title("Slope Rate Difference")
plt.xlim(-SA_SET*border_scale, SA_SET*border_scale)

plt.grid(True)
plt.tight_layout()
plt.savefig(base_dir / "Figures" / f"Fy_Slope_compar", dpi=300, bbox_inches='tight')
plt.show()

print(SA_SET*border_scale)