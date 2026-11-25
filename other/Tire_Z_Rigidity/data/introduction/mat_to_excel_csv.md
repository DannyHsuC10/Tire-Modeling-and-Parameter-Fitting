# Batch Conversion of `.mat` Files to Excel and CSV
[MATLAB source file](../data/mat_to_csv_excel.m)
## Overview
This MATLAB script **batch-processes `.mat` files** in a directory and converts their variables to **Excel (`.xlsx`) and CSV (`.csv`)** for further analysis.

---

## Workflow

1. **Initialize and set paths.**
   - Find the directory containing the script.
   - Set `mat` as the input directory and `csv` and `excel` as the output directories.
   - Create the output directories if they do not exist.

2. **Read `.mat` files.**
   - Use `dir` to find all `.mat` files in the `mat` directory.
   - Raise an error if the directory contains no matching files.

3. **Process the files.**
   - Read each `.mat` file in turn.
   - Load its variables and convert them to MATLAB tables.
   - Try to combine the variables into a single table.
     - Skip variables with a different number of rows.
     - Generate unique names for duplicate columns.

4. **Write the results.**
   - Export the combined table in two formats.
     - Save `.csv` files in `csv`.
     - Save `.xlsx` files in `excel`.

5. **Convert values with `convertToTable`.**
   - Convert supported MATLAB types to `table`.
     - Use an existing `table` directly.
     - Convert `numeric` values to columns or vectors.
     - Convert a `struct` with `struct2table`.
     - Convert a `cell` with `cell2table`.
     - Raise an error for other types.

---

## Use Cases
- MATLAB often stores calculations and experimental data in `.mat` files, which other tools may have difficulty reading directly.  
- Convert to `.csv` or `.xlsx` for further analysis in **Excel, Python, or R**.  
- Use this script for **batch data cleaning, cross-platform sharing, and preprocessing**.

---

## Example Usage
1. Place all `.mat` files in the `mat` directory.  
2. Run the script from MATLAB.  
3. Find the converted files in the `csv` and `excel` directories.  
