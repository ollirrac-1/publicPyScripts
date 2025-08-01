# publicPyScripts

A collection of Python scripts for A/B testing and distribution exploration.

## Overview

This repository contains Python scripts focused on A/B testing analysis and statistical distribution visualization. The scripts include improved A/B testing implementations with enhanced statistical accuracy, distribution visualization tools, and validation testing.

## Files Description

### A/B Testing Scripts

#### `refactored_ab_test.py`
A heavily modified version of an A/B testing script originally shared on Kaggle.com under the Apache 2.0 license. The modifications improve:
- Code flexibility and readability
- Statistical accuracy through revised statistical tests
- Overall functionality and usability

#### `ab_refactor_label_swap.py`
A refactored version of `refactored_ab_test.py` that improves code readability by reversing the labeling convention in one area of the code. This script produces identical results to `refactored_ab_test.py` while maintaining cleaner, more readable code structure.

### Validation and Testing

#### `compare_results.test.py`
A validation script that ensures consistency across the A/B testing implementations. This script:
- Validates that `refactored_ab_test.py` and `ab_refactor_label_swap.py` produce identical output on sample datasets
- Compares results with the original Kaggle source code (results are proximal rather than identical due to using Brunner-Munzel test instead of Mann-Whitney U test)
- Provides quality assurance for the refactored implementations

### Data Analysis and Visualization

#### `cookie_cats_explore.py`
An exploratory data analysis script that analyzes a dataset and produces visualizations and summary statistics. This script utilizes the distribution tools from `dc_distr_tools.py` for its analysis.

#### `dc_distr_tools.py`
A mini-module containing tools for visualizing statistical distributions from CSV input files. This script provides reusable visualization functions that can be imported and used by other analysis scripts.

## Script Relationships

- `dc_distr_tools.py` serves as a utility module used by `cookie_cats_explore.py`
- `refactored_ab_test.py` and `ab_refactor_label_swap.py` are functionally equivalent implementations
- `compare_results.test.py` validates the consistency between all A/B testing implementations

## Getting Started

### Prerequisites
- Python 3.12.4 (developed and tested with this version)
- Required packages are listed in `requirements.txt`

### Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/publicPyScripts.git
   cd publicPyScripts
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Use the distribution tools for data visualization or run exploratory analysis on your datasets
4. Apply the A/B testing scripts to analyze treatment effects in your experiments

## Attribution

The A/B testing scripts are based on work originally shared on Kaggle.com under the Apache 2.0 license:
- Original source: [A/B Testing Step by Step Hypothesis Testing](https://www.kaggle.com/code/ekrembayar/a-b-testing-step-by-step-hypothesis-testing?scriptVersionId=81179299&cellId=33) by ekrembayar

## License

This project is open source and available under the [MIT License](LICENSE).