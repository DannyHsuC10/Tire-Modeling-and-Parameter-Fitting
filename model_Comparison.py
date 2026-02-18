'''
模型比較
'''
import model
import MF_tester
import matlab.engine
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
from Fitter import MF_fitter

# 檔案與路徑設定
base_dir = Path(__file__).resolve().parent  # magic_formula/

#mf_file = base_dir / "data/tir" / "D2704_mf612.tir"# 原本的tir
mf_file = base_dir / "data/tir" /"tir_Fitting_results.tir" # 我fit的檔案
#tir_params = MF_tester.load_tir("D2704_mf612.tir")# 參考文件
tir_params = MF_tester.load_tir("tir_Fitting_results.tir")# 我的檔案

matlab_path = base_dir / "model_matlab"# 啟動matlab引擎
eng = matlab.engine.start_matlab()
eng.cd(str(matlab_path), nargout=0)

def compare_models(output, FZ, SA, SL, IA, P, printout = False):# 單次比較器
    """
    檔案與路徑設定是全域變數
    output : FX,FY,MX,MZ
    """
    
    F_matlab = eng.MF_api(output, FZ, SA, SL, IA, P, str(mf_file))

    MF = model.CalculationInput(
        FZ=FZ,
        SA=SA,
        SL=SL,
        IA=IA,
        pressure=P,
        tir_params=tir_params)

    F_python = MF_fitter.MF_Universal_solver(output, MF)

    if printout == True:# 選擇印出
        print("(matlab 模型)================")
        print("F:", F_matlab, "N")

        print("(python 模型)================")
        print("F:", F_python, "N")

    return float(F_matlab), F_python



# 固定輸入
SA = 0.0
IA = 0.0
P  = 84080.0
# 掃過
SL_range = np.linspace(-1, 1, 40)
FZ_range = np.linspace(500, 2000, 40)

#==================================================================================================
#　建立曲面
SL_grid, FZ_grid = np.meshgrid(SL_range, FZ_range)

F_matlab = np.zeros_like(SL_grid)
F_python = np.zeros_like(SL_grid)

# 迴圈
for i in range(SL_grid.shape[0]):
    for j in range(SL_grid.shape[1]):

        FZ = float(FZ_grid[i, j])
        SL = float(SL_grid[i, j])

        F_matlab[i, j], F_python[i, j] = compare_models('FX', FZ, SA, SL, IA, P)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# MATLAB surface
surf = ax.plot_surface(
    SL_grid,
    FZ_grid,
    F_matlab,
    color='blue',
    alpha=0.5
)

# Python wireframe (紅色)
wire = ax.plot_wireframe(
    SL_grid,
    FZ_grid,
    F_python,
    color='red',
    linewidth=0.8
)
# 出圖
ax.set_xlabel("Slip Ratio (SL)")
ax.set_ylabel("Vertical Load (FZ)")
ax.set_zlabel("Fx")

plt.title("MATLAB vs Python MF612 Fx Comparison")
plt.show()

Fx_error = F_python - F_matlab

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(SL_grid, FZ_grid, Fx_error)

ax.set_xlabel("Slip Ratio")
ax.set_ylabel("FZ")
ax.set_zlabel("Fx Error")

plt.title("Python - MATLAB Fx Error Surface")
plt.show()

eng.quit()# 一定要加不可以刪，不然結束後會一直占用資源