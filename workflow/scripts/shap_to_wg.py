import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--shap", required=True)
parser.add_argument("--out", required=True)
args = parser.parse_args()

df = pd.read_csv(args.shap, sep="\t")
out = pd.DataFrame()

out['variant'] = df['feature']
out['af'] = 0.5
out['lrt-pvalue'] = 1.0
out['filter-pvalue'] = 1.0

if 'mean_abs_shap' in df.columns:
    out['beta'] = df['mean_abs_shap']
elif 'mean_shap_value' in df.columns:
    out['beta'] = df['mean_shap_value']
else:
    out['beta'] = 1.0

out.to_csv(args.out, sep="\t", index=False)
