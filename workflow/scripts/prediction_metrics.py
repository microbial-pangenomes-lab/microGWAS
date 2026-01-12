#!/usr/bin/env python

def get_options():
    import argparse

    description = 'Compute prediction metrics for a WG pyseer run'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('predictions',
                        help='Output file from pyseer --save-predictions')

    return parser.parse_args()

if __name__ == "__main__":
    options = get_options()

    import sys
    import numpy as np
    import pandas as pd
    from scipy import stats
    from sklearn import metrics

    p = pd.read_csv(options.predictions, sep='\t')

    if 'true_value' not in p.columns or 'predicted_value' not in p.columns:
        sys.stderr.write('Required columns not found in predictions file\n')
        sys.exit(1)

    y = p['true_value'].values
    y_hat = p['predicted_value'].values

    # make sure we don't have NaNs
    y_both = pd.DataFrame({'y': y, 'y_hat': y_hat}).dropna()
    y = y_both['y'].values
    y_hat = y_both['y_hat'].values

    # identify if phenotype is continuous or binary
    if y[(y != 0) & (y != 1)].size > 0 or y_hat[(y_hat != 0) & (y_hat != 1)].size > 0:
        sys.stderr.write("Detected continuous phenotype\n")
        binary = False
    else:
        sys.stderr.write("Detected binary phenotype\n")
        binary = True

    d = {}
    if binary:
        f1 = metrics.f1_score(y, y_hat)
        d['f1'] = f1

        mcc = metrics.matthews_corrcoef(y, y_hat)
        d['mcc'] = mcc

        acc = metrics.accuracy_score(y, y_hat)
        recall = metrics.recall_score(y, y_hat)
        precision = metrics.precision_score(y, y_hat)
        d['accuracy'] = acc
        d['recall'] = recall
        d['precision'] = precision

        brier = metrics.brier_score_loss(y, y_hat)
        d['brier'] = brier
    else:
        rmse = np.sqrt(metrics.mean_squared_error(y, y_hat))
        d['rmse'] = rmse

        mae = metrics.mean_absolute_error(y, y_hat)
        d['mae'] = mae

        mse = metrics.mean_squared_error(y, y_hat)
        d['mse'] = mse

    r2 = metrics.r2_score(y, y_hat)
    d['r2'] = r2

    pearson = stats.pearsonr(y, y_hat)[0]
    d['pearson'] = pearson

    spearman = stats.spearmanr(y, y_hat)[0]
    d['spearman'] = spearman

    r = pd.DataFrame.from_dict(d, orient='index', columns=['value'])
    r.to_csv(sys.stdout, sep='\t', header=True, index=True)
