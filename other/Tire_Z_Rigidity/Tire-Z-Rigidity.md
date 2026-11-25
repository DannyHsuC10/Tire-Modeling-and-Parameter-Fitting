# Vertical Tire Stiffness Calculation and Comparison
* [Final results](result.md)

## Main Script
This tool estimates vertical tire stiffness independently of the spring rates provided by TTC. Data processing and filtering use the same modules as the tire modeling workflow, so the same usage guidance and improvement plans apply.

The main script performs these steps. 
> 1. Apply the data filter.
> 2. Fit a linear regression.
> 3. Plot the results and generate a [report](result.md).

## 1. Data Processing
* [MAT to CSV and Excel](data/introduction/mat_to_excel_csv.md) converts MATLAB data to CSV and Excel.

## 2. Data Filtering

1. The [JSON configuration](Filter/introduction/json.md) defines the data-cleaning criteria.
1. The [filter](Filter/introduction/Filter.md) cleans and organizes the data. Update it if file names or paths change.

* [Data comparison plots](Figures/data_comparison.md) can be regenerated with the [data comparator](Filter/introduction/data_comparator.md). Configure the plots as needed. Figures based on private data are generated locally when you run the script.
## 3. Linear Regression
* Use [linear regression](Fitter/introduction/linear_regression.md) to estimate linear tire stiffness from the measured data.

## Further Work
1. Real tire stiffness may be nonlinear. Try exponential or polynomial fits and compare residuals.
1. Use the tool to analyze other stiffness relationships for the same tire.