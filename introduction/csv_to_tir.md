---
layout: base
---

# CSV-to-TIR Conversion
[Source file](../csv_to_tir.py)

This module converts a **CSV parameter file from Magic Formula fitting**
into a `.tir` file for use in a vehicle model.

The converter performs the following tasks.

* Read the fitted MF parameters.
* Write the parameters into a TIR template.
* Produce a tire model file for simulation software.

---

# 🎯 Purpose

Where this step fits in the workflow

```
Complete fitting → Update the CSV → Convert to TIR → Use the tire model
```

This script handles the final conversion.

> Take the `x0` parameters from `Fitting_process.csv`,
> replace the corresponding values in the TIR template,
> and generate the final tire model file.

---

# 📂 Module Structure

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
└── csv_to_tir.py  ← This script
```

---

# 🔧 Main Functions

---

## 1️⃣ Reading a TIR File

```python
load_tir(tir_path)
```

What it does

* Read the `.tir` file.
* Parse the file into two forms.

  * A list of the original text lines.
  * A structured dictionary.

Return format

```python
lines  # List of original text lines
tir_dict = {
  "SECTION": {
    "PARAM": value,
    ...
  }
}
```

---

### Parsing Rules

* Start a section at `[SECTION]`.
* Parse `key = value` as a parameter.
* Ignore comments beginning with `$`.
* Convert each value to a float when possible, otherwise keep it as a string.

Use the parser to do the following.

* Inspect the parameters.
* Debug
* Compare template contents.

---

## 2️⃣ Converting CSV to TIR

```python
csv_to_tir(csv_path, tir_path, tir_template)
```

---

### 📌 Inputs

* `csv_path`
  is the CSV file containing the fitted parameters.

* `tir_path`
  is the output TIR path.

* `tir_template`
  is the input TIR template file.

---

### 📌 CSV Format

The CSV must contain these columns.

```
name,x0
```

Examples

```
PCX1,1.65
PDX1,1.12
PKX1,22.5
```

---

### 📌 Conversion Steps

1. Read the CSV.
2. Build a parameter dictionary.

```python
csv_params = {
  "PCX1": 1.65,
  ...
}
```

3. Read the TIR template line by line.
4. Look for a parameter assignment.

```
KEY = value
```

If the CSV contains the key, replace its value.

```
KEY = CSV_value
```

5. Write the new TIR file.

---

### 📌 Example Replacement Messages

```
Replace PCX1 >>> 1.65
Replace PDX1 >>> 1.12
```

---

# 📄 TIR Template Requirements

Template requirements

* Use the standard TIR format.
* Match parameter names to the CSV exactly.
* Use the following assignment format.

```
PARAM = value
```

# 🚀 Running the Converter

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

Output

```
TIR generated: ...tir_Fitting_results.tir
```

This module completes the staged fitting workflow by exporting the fitted parameters.

Full workflow

```
Data preprocessing
→ Staged fitting
→ Update the CSV
→ CSV → TIR
→ Run the model in a simulation
```
