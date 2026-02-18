---
layout: base
---

# Magic Formula 分段擬合主程式說明

本程式為輪胎 **Magic Formula (MF)** 模型擬合主控腳本，負責：

[位置](../fitting.py)

* 讀取已預處理之輪胎量測資料
* 載入與管理擬合參數（含上下限）
* 依 Stage 分段進行參數最佳化
* 計算誤差指標（RMS / COST）
* 更新參數檔案
* 輸出為 `.tir` 格式

此腳本為整個 MF 擬合流程的核心控制器。

---

# 📦 系統架構概念

```
原始資料 → filter → tir_tester → 分段擬合 → 更新 CSV → 轉出 TIR
```

主要依賴模組：

* [filter](../Filter/introduction/Filter.md)：資料預處理（本檔未直接呼叫函式，但需確保資料已清洗）
* [tir_tester](tir_tester.md)：讀取 MF 測試資料
* [MF_Fitter](../Fitter/introduction/MF_fitter.md)：負責參數最佳化
* [csv_to_tir](csv_to_tir.md)：將最終 CSV 轉換為 TIR 檔案

---

# 📁 資料夾結構

```
magic_formula/
│
├── data/
│   └── Fitting_data/
│       ├── Fitting_process.csv   # 擬合參數
│       └── Fitting_Limits.csv    # 模板檔
│
├── Fitter/
├── model/
├── filter.py
├── tir_tester.py
└── main_fitting_script.py  ← 本檔
```

---

# 🔧 主要功能說明

---

## 1️⃣ 載入擬合參數

```python
load_fit_parameters(filename)
```

功能：

* 從 `data/Fitting_data/` 載入擬合參數
* 支援 `.csv` / `.xlsx`
* 若檔案不存在，自動複製模板檔

回傳格式：

```python
{
  "PCX1": {"x0": 初始值, "lb": 下限, "ub": 上限},
  ...
}
```

---

## 2️⃣ 建立 MF 初始參數

```python
build_mf_params(fit_params)
```

功能：

* 只取出 `x0` 作為初始 MF 參數
* 產生可直接餵入 MF 計算之參數 dict

---

## 3️⃣ 分段參數選取

```python
build_fit_params_for_stages(full_fit_params, STAGES, stages)
```

用途：

* 依 Stage 取出該段要擬合的參數
* 回傳：

  * 該 Stage 專用 fit_params
  * active_keys（最佳化用參數順序）

---

# 🧩 Stage 結構設計

本程式採用 **分段擬合策略**。

---

## FX 分段

```
Stage 1 → 基本形狀 + 剛性 + 峰值
Stage 2 → Load 與 Camber 變化
Stage 3 → 駕駛狀態曲率修正
Stage 4 → Load 影響修正
Stage 5 → Combined slip 參數
```

---

## FY 分段

包含：

* 主側向力參數
* 負載修正
* 高階修正
* Combined slip

---

# 🚀 執行流程

---

## Step 1：讀取資料

```python
F_data_1 = tir_tester.load_mf_data(...)
```

資料需包含：

```
FZ
SL
SA
IA
P
FX 或 FY
```

---

## Step 2：選擇擬合類型

```python
Fit_type = "FX"  # 或 "FY"
selected_stages = [1,2,3,4,5]
```

---

## Step 3：分段迭代擬合

核心流程：

```python
for stage_num in selected_stages:
```

每一 Stage：

1. 選擇對應資料
2. 建立 MF_inputs
3. 建立 Fitter
4. 取得 active parameters
5. 呼叫：

```python
result = fitter.fit(...)
```

---

# 📊 誤差指標

每一 Stage 會輸出：

```
N used by optimizer
RMS
MAX
COST
RMS %
```

定義：

$$RMS = \sqrt{\sum(\Delta x²)}$$

$$MAX = \max{(\Delta x)}$$

$$cost = \sum(\Delta x)$$

$$RMS\% = RMS/\max{(x)}$$
---

# 💾 安全更新參數檔

```python
update_x0(mf_params_current, SAVE_DIR/"Fitting_process.csv")
```

設計特點：

* 先寫入 `.tmp`
* 再 replace 原檔
* 避免寫檔中斷造成檔案毀損

---

# 🔄 最終輸出

```python
import csv_to_tir
```

將更新後之 CSV 轉為 `.tir` 檔
供：


---

# ⚙ 可客製化部分

你可以修改：

```python
Fit_type
selected_stages
F_data_list
```

即可快速切換不同擬合策略。

---

# 🏁 完整流程總結

```
讀資料
→ 讀參數
→ 分段擬合
→ 計算誤差
→ 更新CSV
→ 轉TIR
→ 完成
```
