import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
from dc_dstr_tools import normal_percentiles, analyze_decile_distribution, std_bins_hist
import scipy.stats as stats

df_raw = pd.read_csv('.../cookie_cats.csv')
""" REPLACE ABOVE WITH PATH TO LOCAL COPY OF: https://www.kaggle.com/datasets/yufengsui/mobile-games-ab-testing/cookie_cats.csv """
# print(df_raw.shape) ## (90189, 5)
# print(df_raw.columns)
##  Output -> Index(['userid', 'version', 'sum_gamerounds', 'retention_1', 'retention_7'], dtype='object')
# print(df_raw.head())
# print(df_raw.describe())
## It would be good to verify that there is exactly 1 record per unique user_id

## generally a check for missing values would be good here
    ## skipping because I know there are none

## check for outliers and test for normality vs skew etc
print('df_raw description:')
normal_percentiles(df_raw, 'sum_gamerounds')

## df with target column only ##
df_rounds = df_raw['sum_gamerounds']

## Plot Index against values
df_rounds.plot(legend=False, figsize = (20,5))
plt.suptitle("All Values Against Index", fontsize = 20)
plt.show()

## Examine outlier values past 99.9 percentile
df_rounds[df_rounds > 1073].plot(legend=False, figsize = (20,5))
plt.suptitle("Outliers", fontsize = 20)
plt.show()

## Check extreme value set
print('EXTREME VALUES:')
print(df_rounds[df_rounds > 10000].count())

## Remove the extreme value
df_rounds[df_rounds < 10000].plot(legend=False, figsize = (20,5))
plt.suptitle("After Removing The Extreme Value", fontsize = 20)
plt.show()

df_rounds2 = df_rounds[df_rounds < 10000].reset_index()

print('df_clean description:')
normal_percentiles(df_rounds2, 'sum_gamerounds')

## PLOT1 - Histogram ##
std_bins_hist(df_rounds2, 'sum_gamerounds')

## PLOT2 - Bar Chart ##
# df_clean.value_counts().plot(kind='bar')
# plt.show()

## PLOT3 - Box plot ##
sns.boxplot(data=df_rounds2, y = 'sum_gamerounds')
plt.show()

## PLOT4 - Violin plot ##
sns.violinplot(data=df_rounds2, y = 'sum_gamerounds')
plt.show()

## PLOT5 - Deciles analysis
analyze_decile_distribution(df_rounds2, 'sum_gamerounds')

""" TODO: Add a QQ-plot """

## THE DATA IS STILL HEAVILY SKEWED
##      If we were making a model then...
# df_refined = df_clean[df_clean < 1072].reset_index()

## Users by Round ##
df_clean = df_raw[df_raw.sum_gamerounds < 10000].reset_index()
df_clean.groupby("sum_gamerounds").userid.count().plot()
plt.show()

print(df_clean.groupby("version").sum_gamerounds.agg(["count", "min", "median", "max", "mean", "std"]))
