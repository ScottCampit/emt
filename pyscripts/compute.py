"""
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr


def log2FoldChange(df):
    """
    """
    control = df[["Intensity CTRL1", "Intensity CTRL2"]].mean(axis=1)
    treatment = df[["Intensity TREATED1", "Intensity TREATED2"]].mean(axis=1)

    foldChange = treatment.div(control)
    maxFC = foldChange.loc[[foldChange != np.inf]].max()
    foldChange = foldChange.replace(np.inf, maxFC, inplace=True)

    log2FoldChange = foldChange.apply(np.log2)

    df["log2 FC"] = log2FoldChange
    return df


def computeZScore(df):
    """
    """
    mean = df["log2 FC"].mean()
    stddev = df["log2 FC"].std()
    diff = df["log2 FC"] - mean
    df["Zscore"] = diff.div(stddev)
    return df


def computeColumnZ(array):
    """
    """
    RcoefMat = np.zeros(array.shape)
    PvalMat = np.zeros(array.shape)

    for col in range(RcoefMat.shape[1]):
        for row in range(RcoefMat.shape[0]):
            pearson_product = pearsonr(array[row, col], array[:, col])

            RcoefMat[row, col] = pearson_product[0]
            PvalMat[row, col] = pearson_product[1]

    return RcoefMat, PvalMat
