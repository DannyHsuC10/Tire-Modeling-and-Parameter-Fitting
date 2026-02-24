import os
import scipy.io
import pandas as pd
import numpy as np

# === 相對路徑設定 ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MAT_DIR = os.path.join(BASE_DIR, "mat")
CSV_DIR = os.path.join(BASE_DIR, "csv")
EXCEL_DIR = os.path.join(BASE_DIR, "excel")

# === 若資料夾不存在則建立 ===
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(EXCEL_DIR, exist_ok=True)


def mat_to_dataframe(mat_data):
    """
    將 .mat 讀出的 dict 轉成 pandas DataFrame
    僅保留 numpy array 且維度 <= 2 的資料
    """

    clean_dict = {}

    for key, value in mat_data.items():
        # 跳過 MATLAB 內建欄位
        if key.startswith("__"):
            continue

        if isinstance(value, np.ndarray):

            # 若是 2D 或 1D array
            if value.ndim == 1:
                clean_dict[key] = value

            elif value.ndim == 2:
                # 若是單欄或單列
                if value.shape[0] == 1 or value.shape[1] == 1:
                    clean_dict[key] = value.flatten()
                else:
                    # 多欄矩陣 → 拆成多欄
                    for i in range(value.shape[1]):
                        clean_dict[f"{key}_{i}"] = value[:, i]

    if not clean_dict:
        return None

    return pd.DataFrame(clean_dict)


def convert_all_mat():
    mat_files = [f for f in os.listdir(MAT_DIR) if f.endswith(".mat")]

    if not mat_files:
        print("⚠ 沒有找到 .mat 檔案")
        return

    for file in mat_files:
        mat_path = os.path.join(MAT_DIR, file)
        filename = os.path.splitext(file)[0]

        print(f"轉換中: {file}")

        try:
            mat_data = scipy.io.loadmat(mat_path)
            df = mat_to_dataframe(mat_data)

            if df is None:
                print(f"⚠ {file} 沒有可轉換資料")
                continue

            # === 輸出 CSV ===
            csv_path = os.path.join(CSV_DIR, f"{filename}.csv")
            df.to_csv(csv_path, index=False)

            # === 輸出 Excel ===
            excel_path = os.path.join(EXCEL_DIR, f"{filename}.xlsx")
            df.to_excel(excel_path, index=False)

            print(f"✔ 完成: {filename}")

        except Exception as e:
            print(f"❌ 轉換失敗 {file} : {e}")


if __name__ == "__main__":
    convert_all_mat()