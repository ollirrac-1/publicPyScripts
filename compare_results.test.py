import pandas as pd
import numpy as np
from refactored_ab_test import AB_Test as AB_0
from ab_refactor_label_swap import AB_Test as AB_1

df_raw = pd.read_csv('.../cookie_cats.csv')
""" REPLACE ABOVE WITH PATH TO LOCAL COPY OF: https://www.kaggle.com/datasets/yufengsui/mobile-games-ab-testing/cookie_cats.csv """

df_clean = df_raw[df_raw.sum_gamerounds < 10000].reset_index() # removes one outlier
df_rel = df_clean[df_clean.sum_gamerounds > 29] # the relevant frame for the AB test
df_check = df_clean[df_clean.sum_gamerounds < 30] # checks that samples are representative: verifies no impact through level 29

# A/B Testing Function - Quick Solution
def AB_Test(dataframe, group, target):
    # Packages
    from scipy.stats import shapiro
    import scipy.stats as stats

    # Split A/B
    groupA = dataframe[dataframe[group] == "gate_30"][target]
    groupB = dataframe[dataframe[group] == "gate_40"][target]

    # Assumption: Normality
    ntA = shapiro(groupA)[1] < 0.05
    ntB = shapiro(groupB)[1] < 0.05
    # H0: Distribution is Normal! - False
    # H1: Distribution is not Normal! - True

    if (ntA == False) & (ntB == False):  # "H0: Normal Distribution"
        # Parametric Test
        # Assumption: Homogeneity of variances
        leveneTest = stats.levene(groupA, groupB)[1] < 0.05
        # H0: Homogeneity: False
        # H1: Heterogeneous: True

        if leveneTest == False:
            # Homogeneity
            ttest = stats.ttest_ind(groupA, groupB, equal_var=True)[1]
            # H0: M1 == M2 - False
            # H1: M1 != M2 - True
        else:
            # Heterogeneous
            ttest = stats.ttest_ind(groupA, groupB, equal_var=False)[1]
            # H0: M1 == M2 - False
            # H1: M1 != M2 - True
    else:
        # Non-Parametric Test
        ttest = stats.mannwhitneyu(groupA, groupB, alternative='two-sided')[1]
        # H0: M1 == M2 - False
        # H1: M1 != M2 - True

    # Result
    temp = pd.DataFrame({
        "AB Hypothesis": [ttest < 0.05],
        "p-value": [ttest]
    })
    temp["Test Type"] = np.where((ntA == False) & (ntB == False), "Parametric", "Non-Parametric")
    temp["AB Hypothesis"] = np.where(temp["AB Hypothesis"] == False, "Fail to Reject H0", "Reject H0")
    temp["Comment"] = np.where(temp["AB Hypothesis"] == "Fail to Reject H0", "A/B groups are similar!",
                               "A/B groups are not similar!")

    # Columns
    if (ntA == False) & (ntB == False):
        temp["Homogeneity"] = np.where(leveneTest == False, "Yes", "No")
        temp = temp[["Test Type", "Homogeneity", "AB Hypothesis", "p-value", "Comment"]]
    else:
        temp = temp[["Test Type", "AB Hypothesis", "p-value", "Comment"]]

    # Print Hypothesis
    print("# A/B Testing Hypothesis")
    print("H0: A == B")
    print("H1: A != B", "\n")

    return temp


# Apply A/B Testing: Compare outputs

print('ORIGINAL MANN-WHITNEY FORM:')
print(AB_Test(dataframe=df_clean, group="version", target="sum_gamerounds"))  # non-parametric --> mann-whitney

# non-parametric --> brunner-munzel
print('\nINITIAL REFACTOR:')
print(AB_0(df_clean, "version", "sum_gamerounds", "gate_30", "gate_40"))
print('\nLABEL SWAP REFACTOR:')
print(AB_1(df_clean, "version", "sum_gamerounds", "gate_30", "gate_40"))
