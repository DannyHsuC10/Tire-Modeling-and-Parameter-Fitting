---
layout: base
---

# CSV → TIR 轉換工具說明
[檔案位置](../csv_to_tir.py)

本模組負責將 **Magic Formula 擬合完成之 CSV 參數檔**
轉換為可供車輛模型使用的 `.tir` 檔案。

用途：

* 將擬合完成的 MF 參數
* 自動寫回 TIR 模板
* 產出最終可供模擬軟體使用的輪胎模型檔

---

# 🎯 設計目的

在完整擬合流程中：

```
擬合完成 → 更新 CSV → 轉換成 TIR → 模型使用
```

本腳本負責最後一步：

> 將 `Fitting_process.csv` 的 x0 參數
> 覆寫到 TIR 模板中
> 產生最終輪胎模型檔

---

# 📂 模組結構

```
magic_formula/
│
├── data/
│   ├── Fitting_data/
│   │   └── Fitting_process.csv
│   │
│   ├── TIR_template.tir
│   │
│   └── tir/
│       └── tir_Fitting_results.tir
│
└── csv_to_tir.py  ← 本檔
```

---

# 🔧 主要功能

---

## 1️⃣ 讀取 TIR 檔

```python
load_tir(tir_path)
```

功能：

* 讀取 `.tir` 檔案
* 解析為：

  * 原始文字列表
  * 結構化字典

回傳格式：

```python
lines  # 原始文字 list
tir_dict = {
  "SECTION": {
    "PARAM": value,
    ...
  }
}
```

---

### 解析邏輯說明

* `[SECTION]` → 建立新的區段
* `key = value` → 解析為參數
* 忽略 `$` 開頭的註解
* 嘗試轉為 float，失敗則保留字串

此功能可用於：

* 參數檢查
* Debug
* 比對模板內容

---

## 2️⃣ CSV 轉換為 TIR

```python
csv_to_tir(csv_path, tir_path, tir_template)
```

---

### 📌 輸入

* `csv_path`
  擬合完成的 CSV 檔

* `tir_path`
  輸出 TIR 路徑

* `tir_template`
  TIR 模板檔

---

### 📌 CSV 格式要求

CSV 必須包含欄位：

```
name,x0
```

範例：

```
PCX1,1.65
PDX1,1.12
PKX1,22.5
```

---

### 📌 轉換流程

1. 讀取 CSV
2. 建立參數 dict：

```python
csv_params = {
  "PCX1": 1.65,
  ...
}
```

3. 逐行讀取 TIR 模板
4. 若發現：

```
KEY = value
```

且 KEY 存在於 CSV：

→ 替換成：

```
KEY = CSV_value
```

5. 寫出新 TIR 檔

---

### 📌 範例替換輸出

```
替換 PCX1 >>> 1.65
替換 PDX1 >>> 1.12
```

---

# 📄 TIR 模板需求

模板必須：

* 使用標準 TIR 格式
* 參數名稱與 CSV 完全一致
* 使用：

```
PARAM = value
```

# 🚀 執行流程

```python
tir_lines, tir_data = load_tir(BASE_PATH/"data"/"TIR_template.tir")

tir_template = BASE_PATH/"data"/"TIR_template.tir"
tir_path = BASE_PATH/"data"/"tir"/"tir_Fitting_results.tir"
csv_path = BASE_PATH/"data"/"Fitting_data"/"Fitting_process.csv"

csv_to_tir(
    csv_path=csv_path,
    tir_path=tir_path,
    tir_template=tir_template
)
```

輸出：

```
TIR 已生成: ...tir_Fitting_results.tir
```

此模組為：

> 分段擬合系統的最終輸出端

完整流程：

```
資料預處理
→ 分段擬合
→ 更新 CSV
→ CSV → TIR
→ 模型模擬
```
