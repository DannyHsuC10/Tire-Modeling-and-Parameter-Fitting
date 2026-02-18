"""
輸出tir給模型用
"""
import pandas as pd
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent
def load_tir(tir_path):
    """
    讀入 TIR 檔案，返回兩個結果：
    - lines: 原始文字 list
    - tir_dict: { 'SECTION': { 'PARAM': value, ... } }
    """
    tir_path = Path(tir_path)
    lines = tir_path.read_text().splitlines()
    tir_dict = {}
    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1].strip()
            tir_dict[current_section] = {}
        elif '=' in line and current_section is not None:
            # 切分成 key = value
            key, val = line.split('=', 1)
            key = key.strip()
            val = val.strip().split()[0]  # 只取數值部分，忽略註解
            try:
                val = float(val)
            except ValueError:
                pass  # 如果不是數字就保留原字串
            tir_dict[current_section][key] = val

    return lines, tir_dict

def csv_to_tir(csv_path: Path, tir_path: Path, tir_template: str = None):
    """
    將 CSV 參數轉成 TIR 檔
    - csv_path: CSV 路徑
    - tir_path: 輸出 tir 路徑
    - tir_template: 可選字串模板，若 None 就用固定 header
    """
    
    # 1. 讀 CSV
    df = pd.read_csv(csv_path)
    csv_params = dict(zip(df["name"], df["x0"]))
    # 2. 建立 tir 內容
    tir_lines = []

    if tir_template:
        # 使用給定模板，逐行檢查
        with open(tir_template, 'r') as f:
            for line in f:
                stripped = line.strip()
                
                if "=" in stripped and not stripped.startswith("$"):
                    # 可能有參數
                    key = stripped.split("=")[0].strip()
                    
                    if key in csv_params:
                        # 替換成 CSV 的值
                        print("替換",key,">>>",csv_params[key])
                        line = f"{key} = {csv_params[key]}\n"
                tir_lines.append(line)
    else:
        return "沒有模板"
    # 3. 寫出 tir
    with open(tir_path, 'w') as f:
        f.writelines(tir_lines)

    print(f"TIR 已生成: {tir_path}")

#  讀取資料看看(如果需要可以 print 出來觀察)
tir_lines, tir_data = load_tir(BASE_PATH/ "data" / "TIR_template.tir")

print("開始轉換")
tir_template = BASE_PATH/ "data" / "TIR_template.tir"
tir_path = BASE_PATH/ "data" / "tir" / "tir_Fitting_results.tir"
csv_path = BASE_PATH/"data"/ "Fitting_data" / "Fitting_process.csv"
csv_to_tir(csv_path = csv_path, tir_path = tir_path, tir_template = tir_template)