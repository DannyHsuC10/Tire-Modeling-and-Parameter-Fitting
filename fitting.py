from Filter import filter # 沒有要用這裡面的函式，但需要先資料預處理
from model._common import CalculationInput
import MF_tester
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from Fitter.MF_fitter import MF_Fitter,MF_Universal_solver
import shutil
import tir_tester

# filter.py 所在資料夾
FILTER_DIR = Path(__file__).resolve().parent
# 設定資料夾
SAVE_DIR = FILTER_DIR / "data" / "Fitting_data"
SAVE_DIR.mkdir(exist_ok=True)

# 資料處理
def load_fit_parameters(filename):# 載入擬合資料
    """
    從「與此 .py 檔案同一資料夾」載入擬合參數檔
    """
    base_dir = Path(__file__).resolve().parent  # magic_formula/
    filepath = base_dir / "data" / "Fitting_data" / filename

    if not filepath.exists():
        print("找不到已擬合檔!!採用模板資料!!")
        shutil.copy(base_dir / "data/Fitting_data/Fitting_Limits.csv", filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

    if filepath.suffix == ".csv":
        df = pd.read_csv(filepath)
    elif filepath.suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(filepath)
    else:
        raise ValueError("Unsupported file format")

    params = {}

    for _, row in df.iterrows():
        name = row["name"]

        def _to_value(v):
            return None if pd.isna(v) else float(v)

        params[name] = {
            "x0": _to_value(row["x0"]),
            "lb": _to_value(row.get("lb")),
            "ub": _to_value(row.get("ub"))
        }

    return params

def build_mf_params(fit_params):# 建擬合用MF
    """
    產生一開始給MF的參數
    """
    mf_params = {}

    for name, info in fit_params.items():
        if info["x0"] is None:
            continue

        mf_params[name] = float(info["x0"])

    return mf_params

def update_x0(params, file_path): # 擬合過程中的檔案修改
    file_path = Path(file_path)
    temp_path = file_path.with_suffix(".tmp")

    df = pd.read_csv(file_path)

    for k, v in params.items():
        if k not in df["name"].values:
            print(f"Warning: {k} not found in CSV")
        else:
            df.loc[df["name"] == k, "x0"] = v

    # 先寫到暫存檔
    df.to_csv(temp_path, index=False)

    # 再取代原檔
    temp_path.replace(file_path)

    print("Safe update completed.")

def build_fit_params_for_stages(full_fit_params, STAGES, stages=None):
    """
    full_fit_params:
        dict, 完整 MF 參數資訊，每個參數含 x0, lb, ub
    STAGES:
        dict, 每個 stage 對應的 active parameter 名稱
    stages:
        list[int] 或 None
        - list[int]: 指定要回傳哪些 stage 的參數，例如 [1,2,3,4]
        - None: 回傳所有 stage

    return:
        merged_fit_params: dict, 合併後的 fit_params，只包含指定 stages 的參數
        active_keys: list, 所有要擬合的參數名稱，順序依 stages 中順序排列
    """
    if stages is None:
        stages = list(STAGES.keys())

    merged_fit_params = {}
    active_keys = []

    for s in stages:
        if s not in STAGES:
            print(f"⚠️ Stage {s} 不存在於 STAGES，忽略")
            continue
        keys = STAGES[s]
        for k in keys:
            if k in full_fit_params:
                if k not in merged_fit_params:
                    merged_fit_params[k] = full_fit_params[k]
                    active_keys.append(k)  # 按順序加入 active_keys

    if len(merged_fit_params) == 0:
        print("⚠️ 沒有任何參數被選中，請檢查 stages 與 full_fit_params")

    return merged_fit_params, active_keys

# 分段結構定義
STAGES_FY = {# 分段定義 Fy
    1: [
        "PCY1", "PDY1", "PDY2", "PDY3",
        "PEY1", "PEY2", "PEY3", "PEY4",
        "PKY1", "PKY2", "PKY3",
        "PHY1", "PVY1",
    ],
    2: [
        "PHY2", "PVY2",
        "PKY4", "PKY5",
    ],
    3: [
        "PEY5",
        "PKY6", "PKY7",
    ],
    4: [
        "PPY1", "PPY2", "PPY3", "PPY4", "PPY5","PVY3", "PVY4",
    ],
    5: [
        "RBY1", "RBY2", "RBY3", "RBY4",
        "RCY1",
        "REY1", "REY2",
        "RHY1", "RHY2",
        "RVY1", "RVY2", "RVY3", "RVY4", "RVY5", "RVY6",
    ],}

STAGES_FX = {# 分段定義 Fx
    1: [
        "PCX1",                     # Shape factor
        "PDX1", "PDX2",             # Friction (Peak) vs Load
        "PKX1", "PKX2", "PKX3",     # Slip stiffness vs Load
        "PEX1", "PEX2", "PEX3",     # Curvature vs Load
        "PHX1", "PVX1",             # Basic Shifts
    ],
    2: [
        "PHX2", "PVX2",             # Variation of shifts with load
        "PDX3",                     # Variation of friction with camber
    ],
    3: [
        "PEX4",                     # Factor in curvature while driving
    ],
    4: [
        "PPX1", "PPX2",             # Influence on stiffness
        "PPX3", "PPX4",             # Influence on peak friction
    ],
    5: [
        "RBX1", "RBX2", "RBX3",     # Slope factors for combined
        "RCX1",                     # Shape factor for combined
        "REX1", "REX2",             # Curvature for combined
        "RHX1",                     # Shift for combined
    ],
}

# 導入檔案需求
#F_data_1 = tir_tester.load_mf_data("B2356run23_processed1.csv")# 輸入與輸出結果
#F_data_234 = tir_tester.load_mf_data("B2356run23_processed234.csv")# 輸入與輸出結果

F_data_1 = tir_tester.load_mf_data("B2356run57_processed1.csv")# 輸入與輸出結果
F_data_234 = tir_tester.load_mf_data("B2356run57_processed234.csv")# 輸入與輸出結果
F_data_5 = tir_tester.load_mf_data("B2356run57_processed5.csv")# 輸入與輸出結果

fit_lim = load_fit_parameters("Fitting_process.csv")# 你和數據與上下限
mf_params = build_mf_params(fit_lim)

Fit_type = "FX"# fitting項目
selected_stages = [1,2,3,4,5]  # 可自行調整
F_data_list = [F_data_1,F_data_234,F_data_234,F_data_234,F_data_5]# 選用資料

if  Fit_type == "FY":
    STAGES = STAGES_FY
elif Fit_type == "FX":
    STAGES = STAGES_FX

# ===========================================================================(分段擬合)
for stage_num in selected_stages:

    # 選擇要擬合的 stage
    F_sub = F_data_list[stage_num-1] # 全資料擬和
    MF_inputs = {
        "FZ": F_sub["FZ"],
        "SL": F_sub["SL"],
        "IA": F_sub["IA"],
        "pressure": F_sub["P"],
        "SA": F_sub["SA"]
    }
    F_meas=F_sub[Fit_type]

    # 建立 fitter
    mf_params_current = mf_params.copy()  # 初始參數
    mf_params.copy()  # 初始參數
    fitter = MF_Fitter(out = Fit_type,fit_params = None)  # 先建立空的，後面會傳入每次的 fit_params

    print(f"\n=== Stage {stage_num} 擬合開始 ===")
    stage_params_before = mf_params_current.copy()# 這裡不該重新用原始參數
    # 取得該 stage 的 active parameters
    fit_params_stage, active_keys_stage = build_fit_params_for_stages(fit_lim, STAGES, [stage_num])
    
    # 更新 fitter
    fitter.fit_params = fit_params_stage
    
    # 執行擬合
    result = fitter.fit(
        F_meas=F_meas,
        stage_params=mf_params_current,  # 使用上一 stage 結果作為初值
        active_keys=active_keys_stage,
        MF_inputs=MF_inputs)
    
    # 更新參數
    stage_params_after = mf_params_current.copy()# 這邊紀錄fit後參數用來畫圖
    
    # 結果輸出
    res = result.fun
    RMS = np.sqrt(np.mean(res**2))
    print("N used by optimizer:", len(res))
    print("RMS :", RMS)
    print("MAX :", np.max(np.abs(res)))
    print("COST:", result.cost)
    print("RMS %:", RMS / np.max(np.abs(F_meas)) * 100)
    print(result)

    
    print("最佳參數：")
    for k in active_keys_stage:
        print(f" {k} = {mf_params_current[k]}")
    
    # 可視化(依需求加入)
    #tir_tester.plot_data(F_sub,stage_params_before, stage_params_after,Fit_type)


# 存 CSV
update_x0(mf_params_current, SAVE_DIR/"Fitting_process.csv")
print("暫時存檔案到",SAVE_DIR/"Fitting_process.csv")
print("擬和完成")

import csv_to_tir# 這部分在執行轉檔
