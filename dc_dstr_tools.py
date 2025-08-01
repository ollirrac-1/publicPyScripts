import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing_extensions import Literal
import seaborn as sns
import plotly.express as px


def analyze_decile_distribution(df, column, title=None, figsize=(12, 6)):
    """Create a decile binning visualization showing value counts for each decile.
    Returns: dict"""

    # Remove missing values
    data = df[column].dropna()

    if len(data) == 0:
        print(f"No valid data found in column '{column}'")
        return None

    # Calculate decile boundaries
    deciles = np.percentile(data, np.arange(0, 101, 10))

    # Create decile bins
    bins = pd.cut(data, bins=deciles, include_lowest=True, duplicates='drop')

    # Count values in each decile
    decile_counts = bins.value_counts().sort_index()

    # Create the visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Plot 1: Decile counts
    decile_labels = [f"D{i + 1}" for i in range(len(decile_counts))]
    bars = ax1.bar(decile_labels, decile_counts.values,
                   color='skyblue', edgecolor='navy', alpha=0.7)

    # Add value labels on bars
    for bar, count in zip(bars, decile_counts.values):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(decile_counts) * 0.01,
                 f'{count}', ha='center', va='bottom', fontsize=9)

    ax1.set_xlabel('Deciles')
    ax1.set_ylabel('Count')
    ax1.set_title(f'Value Counts by Decile: {column}' if not title else title)
    ax1.grid(axis='y', alpha=0.3)

    # Plot 2: Decile ranges (for reference)
    decile_ranges = [(deciles[i], deciles[i + 1]) for i in range(len(deciles) - 1)]
    range_widths = [r[1] - r[0] for r in decile_ranges]

    bars2 = ax2.bar(decile_labels, range_widths,
                    color='lightcoral', edgecolor='darkred', alpha=0.7)

    ax2.set_xlabel('Deciles')
    ax2.set_ylabel('Range Width')
    ax2.set_title(f'Decile Range Widths: {column}')
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Print summary statistics
    print(f"\nDecile Analysis for '{column}':")
    print(f"Total observations: {len(data)}")
    print(f"Data range: {data.min():.3f} to {data.max():.3f}")
    print("\nDecile Boundaries:")
    for i, (lower, upper) in enumerate(decile_ranges):
        print(f"  D{i + 1}: [{lower:.3f}, {upper:.3f}] -> {decile_counts.iloc[i]} values")

    # Return analysis results
    return {
        'decile_counts': decile_counts,
        'decile_boundaries': deciles,
        'decile_ranges': decile_ranges,
        'total_observations': len(data),
        'data_range': (data.min(), data.max())
    }


def compare_decile_distributions(df, columns, figsize=(15, 8)):
    """Compare decile distributions across multiple columns."""
    n_cols = len(columns)
    fig, axes = plt.subplots(1, n_cols, figsize=figsize, sharey=True)

    if n_cols == 1:
        axes = [axes]

    for i, column in enumerate(columns):
        data = df[column].dropna()

        if len(data) == 0:
            axes[i].text(0.5, 0.5, f"No data\nfor {column}",
                         ha='center', va='center', transform=axes[i].transAxes)
            continue

        # Calculate deciles and counts
        deciles = np.percentile(data, np.arange(0, 101, 10))
        bins = pd.cut(data, bins=deciles, include_lowest=True, duplicates='drop')
        decile_counts = bins.value_counts().sort_index()

        # Plot
        decile_labels = [f"D{j + 1}" for j in range(len(decile_counts))]
        axes[i].bar(decile_labels, decile_counts.values,
                    color=plt.cm.Set3(i), alpha=0.7)

        axes[i].set_xlabel('Deciles')
        axes[i].set_title(f'{column}')
        axes[i].grid(axis='y', alpha=0.3)

        if i == 0:
            axes[i].set_ylabel('Count')

    plt.suptitle('Decile Distribution Comparison', fontsize=16)
    plt.tight_layout()
    plt.show()


# aligns percentiles with the normal distribution for the describe function
def normal_percentiles(df, column):
    print(df[column].describe([0.001, 0.022, 0.158, 0.50, 0.841, 0.977, 0.998, 0.999]))


# partially resolves disappearing histogram issues for skewed data
def std_bins_hist(df, column, viz: Literal["plt", "sns", "px"] = "plt"):
    df_col = df[column]
    sigma = df_col.std(axis=0)
    max_rounds = df_col.max(axis=0)
    min_rounds = df_col.min(axis=0)
    b = int(np.rint([(1 + max_rounds - min_rounds) / sigma])[0])
    w = max_rounds / b
    print('Number of bins: ' + str(b))
    print('Bin width: ' + str(w))
    if viz == "sns":
        sns.histplot(df_col, bins=b)
        plt.show()
    elif viz == "px":
        px.histogram(df_col, nbins=b).show()
    else:
        plt.hist(df_col, bins=b)
        plt.show()



# Example usage:
# result = analyze_decile_distribution(df, 'your_column_name')
# compare_decile_distributions(df, ['column1', 'column2', 'column3'])

# Example runs and results:
# df_raw = pd.read_csv('.../cookie_cats.csv')
""" TO DO: Repoint df_raw to https://www.kaggle.com/datasets/yufengsui/mobile-games-ab-testing/cookie_cats.csv """
# normal_percentiles(df_raw, 'sum_gamerounds')
# analyze_decile_distribution(df_raw, 'sum_gamerounds')
