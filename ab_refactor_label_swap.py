def AB_Test(dataframe, group, target, value_A, value_B, alpha=0.05, alternative='two-sided'):
    # Packages
    import pandas as pd
    import numpy as np
    from scipy.stats import shapiro, skew
    import scipy.stats as stats
    from scipy.stats import brunnermunzel

    # Split A/B
    groupA = dataframe[dataframe[group] == value_A][target]
    groupB = dataframe[dataframe[group] == value_B][target]

    # Determine sample sizes
    n_A = len(groupA)
    n_B = len(groupB)

    # Sample size based test selection with skewness check
    from scipy.stats import skew
    skewness_A = abs(np.asarray(skew(groupA)).item())
    skewness_B = abs(np.asarray(skew(groupB)).item())
    max_skewness = max(skewness_A, skewness_B)

    if max_skewness > 2:
        # Highly skewed data: assume normality is violated, use non-parametric test
        normalA = False  # Not normal
        normalB = False  # Not normal
    elif n_A >= 100 and n_B >= 100:
        # Large samples with moderate skewness: CLT applies, skip normality testing
        normalA = True  # Assume normal
        normalB = True  # Assume normal
    else:
        # Small/medium samples with moderate skewness: use Shapiro-Wilk
        _, p_value_A = shapiro(groupA)
        _, p_value_B = shapiro(groupB)
        # Note: Signs flipped for readability - True = normal, False = not normal
        normalA = p_value_A >= alpha  # True if normal
        normalB = p_value_B >= alpha  # True if normal
    # H0: Distribution is Normal! - True
    # H1: Distribution is not Normal! - False

    if normalA and normalB:  # Both groups are normal
        # Parametric Test
        # Assumption: Homogeneity of variances
        # Note: Using fixed alpha=0.05 for assumption testing, independent of main test alpha
        leveneTest = stats.levene(groupA, groupB)[1] < 0.05
        # H0: Homogeneity: False
        # H1: Heterogeneous: True

        if leveneTest == False:
            # Homogeneity
            ttest = stats.ttest_ind(groupA, groupB, equal_var=True, alternative=alternative)[1]
            # H0: M1 == M2 - False
            # H1: M1 != M2 - True
        else:
            # Heterogeneous
            ttest = stats.ttest_ind(groupA, groupB, equal_var=False, alternative=alternative)[1]
            # H0: M1 == M2 - False
            # H1: M1 != M2 - True
    else:
        # Non-Parametric Test
        ttest = brunnermunzel(groupA, groupB, alternative=alternative)[1]
        # H0: M1 == M2 - False
        # H1: M1 != M2 - True

    # Result
    temp = pd.DataFrame({
        "AB Hypothesis": [ttest < alpha],
        "p-value": [ttest]
    })
    temp["Test Type"] = np.where(normalA and normalB, "Parametric", "Non-Parametric")
    temp["AB Hypothesis"] = np.where(temp["AB Hypothesis"] == False, "Fail to Reject H0", "Reject H0")
    temp["Comment"] = np.where(temp["AB Hypothesis"] == "Fail to Reject H0", "A/B groups are similar!",
                               "A/B groups are not similar!")

    # Columns
    if normalA and normalB:
        temp["Homogeneity"] = np.where(leveneTest == False, "Yes", "No")
        temp = temp[["Test Type", "Homogeneity", "AB Hypothesis", "p-value", "Comment"]]
    else:
        temp = temp[["Test Type", "AB Hypothesis", "p-value", "Comment"]]

    # Print Hypothesis
    print("# A/B Testing Hypothesis")
    if alternative == 'two-sided':
        print("H0: A == B")
        print("H1: A != B", "\n")
    elif alternative == 'less':
        print("H0: A >= B")
        print("H1: A < B", "\n")
    elif alternative == 'greater':
        print("H0: A <= B")
        print("H1: A > B", "\n")

    return temp
