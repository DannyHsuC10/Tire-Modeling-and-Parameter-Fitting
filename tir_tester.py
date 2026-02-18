import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
import model
import MF_tester
import pandas as pd
from Fitter.MF_fitter import MF_Universal_solver

def load_mf_data(filename):# 載入數據
    """
    讀取 Magic Formula 擬合用資料(CSV 或 Excel)
    回傳 dict[str, np.ndarray]
    """
    base_dir = Path(__file__).resolve().parent  # magic_formula/
    filepath = base_dir /"data"/"Filtered_data"/filename
    if filepath.suffix == ".csv":
        df = pd.read_csv(filepath)
    elif filepath.suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(filepath)
    else:
        raise ValueError("Unsupported file format")

    # 轉成 dict of numpy array
    data = {col: df[col].to_numpy() for col in df.columns}

    return data

def plot_data(df,tir_params1, tir_params2,Fit_type):
    tir_params_list = [tir_params1,tir_params2]
    
    F_lists  = []

    for j in range(len(tir_params_list)):

        MF = model.CalculationInput(
            FZ=df["FZ"],
            SA=df["SA"],
            SL=df["SL"],
            IA=df["IA"],
            pressure=df["P"],
            tir_params=tir_params_list[j],  # 傳完整參數
        )
        F_array = MF_Universal_solver(Fit_type,MF)
        F_lists.append(F_array)

    Fy_m = df[Fit_type]

    # 實際測量值
    F1 = np.array(F_lists[0])
    F2  = np.array(F_lists[1])
    F_meas   = np.array(Fy_m)

    # 畫圖
    plt.figure(figsize=(12, 6))
    plt.plot(F_meas, label="Measured F", color="black", linewidth=1)
    plt.plot(F1, label="Predicted F (1)", linestyle="--")
    plt.plot(F2, label="Predicted F (2)", linestyle="-.")
    plt.xlabel("Data Point Index")
    plt.ylabel("F[N]")
    plt.legend()
    plt.grid(True)
    plt.show()
if __name__ == "__main__":
    # load data
    df = load_mf_data("B2356run57_processed5.csv")# 輸入與輸出結果
    tir_params1 = MF_tester.load_tir("data/tir/D2704_mf612.tir")# 紅心
    tir_params2 = MF_tester.load_tir("data/tir/tir_Fitting_results.tir")# 我
    # plot
    plot_data(df,tir_params1, tir_params2, "FY")