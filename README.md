# Tire-Modeling-and-Parameter-Fitting

## Tire Model Packages (`model_for_import`)
The `model_for_import` directory contains MATLAB and Python versions of the tire model. Download the corresponding directory and follow the examples to call its API, or adapt the supplied demo.

## Tire Analysis Tools (`other`)
These tools support tire analysis during vehicle design. Review the basics of tire behavior before interpreting the results.

1. Tire performance comparison (`diff_tire_test`) compares peak forces across tires.
1. Tire stiffness fitting (`Tire_Z_Rigidity`) estimates vertical tire stiffness for suspension design. You can also use manufacturer or TTC data from comparable operating conditions.
1. Friction coefficient estimation (`coefficient_of_friction`) estimates grip and force limits for vehicle design.

## Fitting Workflow and Usage
The [main fitting script](/introduction/fitting.md) runs the full workflow. To fit a different dataset, update the data, file names, and paths. The scripts use relative paths. The raw data is private, so consult the documentation for the expected locations.

* Fit either Fx or Fy.
* Process the data, evaluate the tire model, fit the parameters, validate the results, and export a TIR file.

### Repository Overview
The following links point to the relevant code or documentation. The list summarizes the role of each directory.

1. `model_for_import` contains the core tire model packages and is the usual starting point.
1. `other` contains tire analysis tools for early vehicle design.
1. `data` contains datasets. Most data is private. See the [data overview](data/introduction/all_data.md).
1. `Figures` stores PNG figures generated from private data.
1. `Filebkp` holds protected backup files and may be unavailable.
1. `Filter` prepares data for `Fitter`.
1. `Fitter` fits the model to the filtered data and produces fitted parameters.
1. `matlab_bridge` connects the workflow to MATLAB.
1. `model` contains the tire models.
1. `model_matlab` contains the MATLAB tire model, which can be used alongside the Python model.
1. `introduction` contains Markdown documentation.
1. `assets` contains the website styles.
1. `_layouts` contains the HTML templates.

### 1. Data Processing

* [Data overview](data/introduction/all_data.md) describes the dataset structure.

* [MAT to CSV and Excel](data/introduction/mat_to_excel_csv.md) converts MATLAB data to CSV and Excel.

### 2. Data Filtering

> Files you are most likely to edit
>
> 1. The [filter configuration](Filter/introduction/json.md) defines the data-cleaning conditions.
> 1. The [filter](Filter/introduction/Filter.md) cleans and organizes the data. Update it if file names or paths change.

* [Data comparison plots](Figures/data_comparison.md) can be regenerated with the [data comparator](Filter/introduction/data_comparator.md). Configure the plots as needed. Figures based on private data are generated locally when you run the script.

### 3. Tire Modeling

> Files you are most likely to edit
>
> 1. The [Magic Formula tester](/introduction/MF_tester.md) uses modular plotting objects to compare model inputs and outputs across tire parameter sets.

* [Magic Formula plots](/Figures/MF_plt.md) holds plots saved by the tester. Plots based on private data are generated locally when the tester runs.
* The [Python Magic Formula model](model/introduction/magic_formula_model.md) uses NumPy to evaluate arrays in optimized native code. The model relies heavily on trigonometric functions and runs on the CPU. The reported runtime for fitting a large dataset is about 30–60 seconds.

* The [MATLAB Magic Formula model](model_matlab/introduction/magic_formula_matlab.md) is the original MF6.1.2 implementation used as a reference for the model and fitting results. The fitting workflow has no direct integration with its MATLAB API.

### 4. Parameter Fitting

> Files you are most likely to edit
>
> 1. The [parameter fitter](/Fitter/introduction/MF_fitter.md) is called by the main fitting script. Its `MF_Universal_solver` can evaluate the Magic Formula model.

### 5. TIR Export and Validation

* [CSV to TIR](/introduction/csv_to_tir.md) converts fitted CSV parameters into a TIR file for import.
* The [TIR tester](/introduction/tir_tester.md) compares predictions from a TIR model against measured data.
* The [MATLAB bridge](/matlab_bridge/introduction/matlab_bridge.md) exports files for MATLAB tests. Copy the generated files when you need them elsewhere.

## Planned Improvements
### Straightforward

* Consolidate the tire model implementations. The importable package is the most complete and easiest to use.
* Add OR conditions to the slope filter.
* Improve how the MATLAB data converter handles complex data structures.
* Centralize file naming and path configuration so users can update paths without editing source code.

### Advanced
* Optimize the MATLAB model calculations.
* Python can run the MATLAB model through the MathWorks MATLAB Engine. Future compatibility is uncertain, and an interface for calling the optimized Python model from MATLAB still needs to be designed.
* Add a single-command fitting workflow. The current scripts fit each degree of freedom separately.

### Difficult
* Derive the JSON filter settings automatically from the data to speed up processing.
* Derive fitting bounds and initial values dynamically to improve speed and possibly accuracy.

### Long-Term Ideas
* Explore additional fitting methods, including genetic algorithms, spline fitting, and neural networks.
* Explore additional tire models, including Gaussian process and brush models.
