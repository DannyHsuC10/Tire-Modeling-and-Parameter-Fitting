---
layout: base
---

# Magic Formula 模型比較與結果視覺化工具

[本模組](../tir_tester.py)用於：

* 載入已過濾之輪胎量測資料
* 載入兩組 `.tir` 輪胎模型參數
* 計算 Magic Formula 輸出
* 與實測數據比較
* 視覺化模型差異

此工具主要用於：

> ✔ 擬合前後模型比較
> ✔ 不同版本 TIR 對比
> ✔ 驗證 MF 參數修正效果

# 📦 依賴模組

* `model.CalculationInput`
* `MF_Universal_solver`
* `MF_tester.load_tir`
* `numpy`
* `matplotlib`
* `pandas`

---

# 🔧 功能說明

## 1️⃣ 載入 MF 資料

```python
load_mf_data(filename)
```

功能：

* 從 `data/Filtered_data/` 讀取資料
* 支援 `.csv` / `.xlsx`
* 回傳：

```python
{
  "FZ": np.ndarray,
  "SA": np.ndarray,
  "SL": np.ndarray,
  "IA": np.ndarray,
  "P": np.ndarray,
  "FX" 或 "FY": np.ndarray
}
```

---

### 📌 資料需求

資料需包含：

```
FZ      垂直載重
SA      Slip Angle
SL      Slip Ratio
IA      Camber
P       Inflation Pressure
FX/FY   量測力
```

---

## 2️⃣ 模型計算流程

```python
MF = model.CalculationInput(...)
F_array = MF_Universal_solver(Fit_type, MF)
```

流程：

1. 將資料包裝成 `CalculationInput`
2. 呼叫 `MF_Universal_solver`
3. 計算對應輸出力

支援：

* `"FX"` → 縱向力
* `"FY"` → 側向力

---

## 3️⃣ 比較函式

```python
plot_data(df, tir_params1, tir_params2, Fit_type)
```

---

### 📌 設計目的

比較：

```
Measured Force
vs
Model 1 Prediction
vs
Model 2 Prediction
```

---

### 📌 計算步驟

對兩組 TIR：

```python
tir_params_list = [tir_params1, tir_params2]
```

逐一：

* 建立 MF 輸入物件
* 計算預測值
* 存入 F_lists

---

### 📌 視覺化內容

* 黑色實線 → 實測值
* 虛線 → 模型 1
* 點虛線 → 模型 2

X 軸：

```
資料索引
```

Y 軸：

```
Force [N]
```

---

# 🚀 執行方式

```python
if __name__ == "__main__":
```

---

## Step 1：讀取資料

```python
df = load_mf_data("B2356run57_processed5.csv")
```

---

## Step 2：讀取兩組 TIR

```python
tir_params1 = MF_tester.load_tir("data/tir/D2704_mf612.tir")
tir_params2 = MF_tester.load_tir("data/tir/tir_Fitting_results.tir")
```

常見用途：

* `tir_params1` → 原始 TTC / 官方模型
* `tir_params2` → 自己擬合結果

---

## Step 3：畫圖比較

```python
plot_data(df, tir_params1, tir_params2, "FY")
```