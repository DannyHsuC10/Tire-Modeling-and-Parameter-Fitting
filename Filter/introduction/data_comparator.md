---
layout: base
---

# Data Comparator User Guide

## Source Location

See the [source file](../Data_comparator.py).
The tool **compares raw tire test data with preprocessed data**.

```
magic_formula/
├─ filter/
│  └─ Data_comparator.py
├─ data/
│  └─ csv/
│     ├─ raw_data.csv
├─ data/
│  └─ Filtered_data/
│     ├─ data_processed.csv
```

---

## Features

The `DataComparator` class does the following.

* Read the raw CSV.
* Read the cleaned or filtered CSV.
* Identify **columns shared by both files**.
* Plot the data for each shared column in two panels.

  * Left panel for raw data.
  * Right panel for cleaned data.
* Choose one of the following output modes.

  * Show the plots immediately.
  * Save the comparison plots.

---

## Class Reference

### `DataComparator`

### Constructor Parameters

```python
DataComparator(
    raw_filename: str,
    cleaned_filename: str,
    save_fig: bool = False,
    fig_dir: str = "figures"
)
```

| Parameter | Description |
| ------------------ | --------------------------------- |
| `raw_filename` | Raw data file name in `data/csv/` |
| `cleaned_filename` | Cleaned data file name in `data/Filtered_data/` |
| `save_fig` | Save plots if enabled. The default, False, displays them. |
| `fig_dir` | Directory name for saved plots |

---

## Comparison Logic

1. Read the two CSV files.
2. Identify the shared columns.
3. For each shared column, create a comparison figure.

   * Create a 1×2 subplot layout.
   * Left panel holds the raw data.
   * Right panel holds the cleaned data.
4. Apply the `save_fig` setting.

   * `False` displays the plot.
   * `True` saves the plot as a PNG.

---

## Usage

Run the following example directly.

```python
if __name__ == "__main__":

    comparator = DataComparator(
        raw_filename="data_name.csv",
        cleaned_filename="data_name_processed1.csv",
        save_fig=False
    )
    comparator.compare_columns()
```

---

## Output

The tool creates one side-by-side plot per column with a shared y-axis. Use the plots to check the following.

* The effect of filtering.
* Whether outliers were removed.
* Whether the signal was smoothed.
* Whether valid data was removed by mistake.

---

## Use Cases

* Validate preprocessing for the Magic Formula tire model.
* Inspect the effects of filtering.
* Check Boolean mask cleaning.
* Verify unit conversions.
* Check data quality.

---

## 📁 Saving Plots

With the following setting,

```python
save_fig=True
```

the tool creates this directory

```
magic_formula/figures/
```

and saves the plots here.

```
ColumnName_comparison.png
```

## Notes

* Both CSV files must exist in their expected directories.
* The tool compares columns with matching names.
* The two files can contain different numbers of samples. The sample index is used on the x-axis.
