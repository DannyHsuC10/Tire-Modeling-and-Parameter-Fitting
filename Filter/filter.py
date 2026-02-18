# 資料過濾器
"""
處理程序:
1. 清掉頭尾資料
2. 建立布林遮罩
3. 套用遮罩並刪掉 NaN
4. 低通濾波（可選）
5. 資料轉換
"""
import pandas as pd
from pathlib import Path
import numpy as np
import json
from scipy.signal import butter, filtfilt, welch

# filter.py 所在資料夾
FILTER_DIR = Path(__file__).resolve().parent
# 專案根目錄 project/
PROJECT_DIR = FILTER_DIR.parent

# ===========================================(載入)
def load_tire_data(file_path):# 載入資料
    file_path = Path(file_path)

    if file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path)
    elif file_path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

    return df

# ===========================================(資料清洗)
def trim_dataframe_edges(df: pd.DataFrame, n_head: int = 0, n_tail: int = 0, fill_value=np.nan) -> pd.DataFrame:# 頭尾清洗
    """
    清掉 DataFrame 開頭與結尾的資料

    df: pandas DataFrame
    n_head: 要清掉的開頭列數
    n_tail: 要清掉的結尾列數
    fill_value: 清掉後填入的值，預設 NaN

    返回新的 DataFrame
    """
    df_clean = df.copy()

    if n_head > 0:
        df_clean.iloc[:n_head, :] = fill_value

    if n_tail > 0:
        df_clean.iloc[-n_tail:, :] = fill_value

    return df_clean

# ===========================================(布林遮罩)
class MaskBuilder:
    def __init__(self, json_path: str):
        """
        json_path: Filtering_Limits.json 路徑
        """
        with open(json_path, "r") as f:
            self.limits = json.load(f)

    # =========================
    # 基本工具
    # =========================
    @staticmethod
    def enforce_min_segment_length(mask: np.ndarray, min_len: int) -> np.ndarray:
        """將 mask 中連續 True 長度 < min_len 的區段清除"""
        mask = mask.copy()
        count = 0
        start = 0

        for i, val in enumerate(mask):
            if val:
                if count == 0:
                    start = i
                count += 1
            if (not val or i == len(mask) - 1) and count > 0:
                if count < min_len:
                    mask[start:start + count] = False
                count = 0
        return mask

    def build_mask_from_range(
        self,
        data: np.ndarray,
        min_val: float,
        max_val: float,
        min_len: int
    ) -> np.ndarray:
        """一般 min / max 範圍遮罩"""
        mask = (data >= min_val) & (data <= max_val)
        return self.enforce_min_segment_length(mask, min_len)

    # =========================
    # slope 特殊遮罩
    # =========================
    @staticmethod
    def build_slope_mask(
        data: np.ndarray,
        pos_range,
        neg_range,
        slope_min,
        slope_max,
        min_len: int = 5
    ) -> np.ndarray:
        """
        建立 data 斜率遮罩（防 NaN / 防短段 / 防退化）
        - 全常數段也會被直接通過
        """
        data = np.asarray(data, dtype=float)

        in_pos = (data >= pos_range["min"]) & (data <= pos_range["max"])
        in_neg = (data >= neg_range["min"]) & (data <= neg_range["max"])
        merged = in_pos | in_neg

        mask = np.zeros_like(data, dtype=bool)

        # 如果全部都符合 merged，直接全通過
        if np.all(merged):
            mask[:] = True
            return mask

        zero_idx = np.where(~merged)[0]

        breaks = np.where(np.diff(zero_idx) > 1)[0]
        starts = zero_idx[np.r_[0, breaks + 1]]
        ends   = zero_idx[np.r_[breaks, len(zero_idx) - 1]]

        for s, e in zip(starts, ends):
            seg = data[s:e + 1]

            # ❶ 長度檢查
            if len(seg) < min_len:
                continue

            # ❷ NaN / Inf 檢查
            if not np.all(np.isfinite(seg)):
                continue

            # ❸ 退化檢查（全常數）
            if np.std(seg) < 1e-6:
                mask[s:e+1] = True  # 全常數直接通過
                continue

            # ❹ 斜率計算（防爆）
            try:
                x = np.arange(len(seg))
                slope = np.polyfit(x, seg, 1)[0]
            except np.linalg.LinAlgError:
                continue

            if slope_min <= slope <= slope_max:
                mask[s:e + 1] = True

        return mask

    # =========================
    # 對外主介面
    # =========================
    def build_masks(
        self,
        df: pd.DataFrame,
        mask_type: str = "FX"
    ) -> dict:
        """
        df: pandas DataFrame
        mask_type: "FX" or "FY"
        
        邏輯：
        - 每個欄位內子遮罩用 OR 合併
        - 不同欄位之間用 AND 合併
        """
        limits = self.limits[mask_type]
        masks = {}
        total_mask = np.ones(len(df), dtype=bool)

        for col, col_limits in limits.items():
            if "slope_min" in col_limits:
                # SL 特殊處理
                slope_data = df[col].to_numpy(dtype=float)      # 轉成 float，非數字會變 NaN
                numeric_slope = np.nan_to_num(slope_data, nan=0.0) # NaN 視為 0

                if np.all(numeric_slope == 0):
                    sl_mask = np.ones(len(numeric_slope), dtype=bool)
                else:
                    sl_mask = self.build_slope_mask(
                        numeric_slope,
                        col_limits["pos_range"],
                        col_limits["neg_range"],
                        col_limits["slope_min"],
                        col_limits["slope_max"]
                    )

                masks[col] = sl_mask
                total_mask &= sl_mask
            else:
                data = df[col].to_numpy()
                # 對欄位內所有子遮罩做 OR
                col_mask = np.zeros(len(df), dtype=bool)
                for name, params in col_limits.items():
                    mask = self.build_mask_from_range(
                        data,
                        params["min"],
                        params["max"],
                        params["n"]
                    )
                    col_mask |= mask  # OR
                    masks[name] = mask  # 保留原本各子遮罩

                total_mask &= col_mask  # AND 不同欄位

        # 將 total_mask 也回傳
        masks["total_mask"] = total_mask
        return masks

# ===========================================(濾波器)
def auto_lowpass_filter(# 傅立葉低通率波
    df: pd.DataFrame,
    fs: float = 1000.0,
    energy_ratio: float = 0.9,
    order: int = 5,
    min_cutoff: float = 0.001
) -> pd.DataFrame:
    """
    自動低通濾波（安全版）
    透過 Welch PSD 累積能量決定 cutoff frequency，
    並加入完整保護機制，避免 cutoff = 0 或數值爆炸。

    df: pandas DataFrame
    fs: 取樣頻率 (Hz)
    energy_ratio: 保留的訊號能量比例 (建議 < 1，例如 0.95~0.99)
    order: Butterworth 濾波器階數
    min_cutoff: 最小 cutoff frequency (Hz)，避免 0 Hz
    """

    df_filtered = df.copy()

    # energy_ratio 保護（FFT 永遠不要用 1）
    energy_ratio = min(max(energy_ratio, 0.0), 0.999)

    nyquist = fs / 2.0

    for col in df.columns:
        data = df[col].to_numpy()

        # ---- 1️⃣ NaN / 無效資料保護 ----
        if np.all(np.isnan(data)):
            continue

        valid = ~np.isnan(data)
        if valid.sum() < 10:
            # 資料太短，直接略過
            continue

        x = data[valid]

        # ---- 2️⃣ 常數訊號（FFT 只剩 DC） ----
        if np.std(x) < 1e-8:
            df_filtered[col] = data
            continue

        # ---- 3️⃣ Welch PSD ----
        nperseg = min(1024, len(x))
        f, Pxx = welch(x, fs=fs, nperseg=nperseg)

        cumulative_energy = np.cumsum(Pxx)
        total_energy = cumulative_energy[-1]

        if total_energy <= 0:
            continue

        # ---- 4️⃣ 找 cutoff ----
        cutoff_idx = np.searchsorted(
            cumulative_energy,
            energy_ratio * total_energy
        )
        cutoff_idx = min(cutoff_idx, len(f) - 1)
        cutoff_freq = f[cutoff_idx]

        # ---- 5️⃣ cutoff 安全保護 ----
        cutoff_freq = np.clip(
            cutoff_freq,
            min_cutoff,
            0.45 * fs   # 留 margin，避免貼 Nyquist
        )

        Wn = cutoff_freq / nyquist
        if not (0 < Wn < 1):
            continue

        # ---- 6️⃣ 濾波 ----
        b, a = butter(order, Wn, btype="low")
        filtered = np.full_like(data, np.nan, dtype=float)
        filtered[valid] = filtfilt(b, a, x)

        df_filtered[col] = filtered

    return df_filtered

# ===========================================(轉換器)
def data_converter(df): # 轉換資料只留下需要用的，未來如果raw data 有變更可能需要修改
    """
    處理工作
    1. 只留下需要的資料
    2. 進行正負號調換
    """
    # === 1. Columns used in current fitting stage ===
    # 原資料 AMBTMP,ET,FX,FY,FZ,IA,MX,MZ,N,NFX,NFY,P,RE,RL,RST,RUN,SA,SL,SR,TSTC,TSTI,TSTO,V
    cols_keep = ['FX', 'FY', 'FZ', 'MX', 'MZ', 'IA', 'P', 'SA', 'SL', 'V']# 配合MF62模型
    df_fit = df[cols_keep].copy()

    # === 2. Sign convention (集中管理轉換邏輯) ===
    sign_flip = {
        'FX': -1,
        'FY': -1,
        'FZ': -1,   # load -> positive
        'SA': -1,   # align SA-FY direction
        'SL': -1,
        'MX': -1,
        'MZ': -1,
        'V': 0.28,
        'P' : 1000}  # MZ,MX 其實也需要轉換但先不保留 之後加入
        

    for col, s in sign_flip.items():
        df_fit[col] *= s

    return df_fit

# ===========================================(全部處理)
def preprocess_tire_data(
    df: pd.DataFrame,
    mask_builder,                # 👈 傳入 MaskBuilder instance
    mask_type: str = "FX",
    n_head: int = 5,
    n_tail: int = 5,
    fs: float = 1000,
    energy_ratio: float = 0.9,
    order: int = 8
) -> pd.DataFrame:
    """
    完整的輪胎資料清洗流程：
    1. 清掉頭尾資料
    2. 建立布林遮罩
    3. 套用遮罩並刪掉 NaN
    4. 低通濾波（可選）
    5. 資料轉換
    """

    # 頭尾清洗
    df_cleaned = trim_dataframe_edges(
        df,
        n_head=n_head,
        n_tail=n_tail,
        fill_value=np.nan
    )
    print(f"[Step 1] 頭尾清洗後有效列數: {df_cleaned.dropna(how='all').shape[0]} / {len(df_cleaned)}")

    # 建立布林遮罩（由 class 處理）
    masks = mask_builder.build_masks(df_cleaned, mask_type=mask_type)
    for k, v in masks.items():
        print(f"[Mask] {k} 符合條件列數: {np.sum(v)} / {len(v)}")

    # 套用總遮罩（MaskBuilder 已經幫你計算 total_mask）
    total_mask = masks.pop("total_mask")  # 取出總遮罩，其它子遮罩仍保留在字典中
    df_cleaned.loc[~total_mask, :] = np.nan

    # 刪掉整列都是 NaN 的資料
    df_cleaned = df_cleaned.dropna(how='all').reset_index(drop=True)
    print(f"[Step 3] 套用總遮罩並刪 NaN 後有效列數: {len(df_cleaned)} / {len(df)}")
    
    # 低通濾波（只對數值欄位，可選）
    df_filtered = auto_lowpass_filter(
        df_cleaned,
        fs=fs,
        energy_ratio=energy_ratio,
        order=order
    )
    print(f"[Step 4] 濾波後有效列數: {df_filtered.dropna(how='all').shape[0]} / {len(df_filtered)}")

    # 最後進行資料轉換(轉換單位、刪不要的項目)
    print("[Step 5] 進行資料轉換")
    return data_converter(df_cleaned) # 關掉濾波器
    return data_converter(df_filtered)

# ===========================================(執行區域)
"""
檔案資料結構
magic_formula/
├─ filter/
│  └─ filter.py   ← 這個檔案
│  └─ Filtering_Limits.json← json
├─ data/
│  └─ csv/B2356run23.csv← 要載入的資料
│  └─ csv/B2356run57.csv← 要載入的資料
├─ data/
│  └─ Filtered_data/B2356run23_processed.csv← 存檔資料
│  └─ Filtered_data/B2356run23_processed.csv← 存檔資料
"""
# 建立遮罩
mask_builder = MaskBuilder(FILTER_DIR / "Filtering_Limits_stage.json")

"""
將單位轉換後的 F_data_processed 拆成累積對應 STAGES 的資料
Stage 1 → IA=0, SL=0
Stage 2 → Stage1 + IA!=0, SL=0
Stage 3~4 → Stage1~2
Stage 5 → Stage3 + SL!=0 (all data)
"""


data_23 = load_tire_data(PROJECT_DIR / "data/csv/B2356run23.csv")
data_57 = load_tire_data(PROJECT_DIR / "data/csv/B2356run57.csv")

print("========處理23========")
data_23_out = preprocess_tire_data(data_23,mask_builder = mask_builder,mask_type = "23_1")
data_23_out.to_csv(PROJECT_DIR / "data/Filtered_data/B2356run23_processed1.csv", index=False)
data_23_out = preprocess_tire_data(data_23,mask_builder = mask_builder,mask_type = "23_234")
data_23_out.to_csv(PROJECT_DIR / "data/Filtered_data/B2356run23_processed234.csv", index=False)

print("========處理57========")
data_57_out = preprocess_tire_data(data_57,mask_builder = mask_builder,mask_type = "57_1")
data_57_out.to_csv(PROJECT_DIR / "data/Filtered_data/B2356run57_processed1.csv", index=False)
data_57_out = preprocess_tire_data(data_57,mask_builder = mask_builder,mask_type = "57_234")
data_57_out.to_csv(PROJECT_DIR / "data/Filtered_data/B2356run57_processed234.csv", index=False)
data_57_out = preprocess_tire_data(data_57,mask_builder = mask_builder,mask_type = "57_5")
data_57_out.to_csv(PROJECT_DIR / "data/Filtered_data/B2356run57_processed5.csv", index=False)

print("✅ 資料已成功存成 CSV！")
