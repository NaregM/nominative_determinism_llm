import numpy as np
import pandas as pd

import argparse
from helpers import run_nd_analysis
from permutation import permutation_test, binary_score

from pprint import pprint

# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------

if __name__ == "__main__":
    
    p = argparse.ArgumentParser()
    p.add_argument("--input_csv", required=True, help="path to input CSV")
    p.add_argument("--output_csv", required=False, help="path to write results CSV")
    p.add_argument("--N", required=False, help="Sample size", type=int)
    p.add_argument("--M", required=False, help="Permutation Size", type=int)

    args = p.parse_args()
    pprint(permutation_test(args.input_csv, binary_score, args.N, args.M))
    #run_nd_analysis(args.input_csv, args.output_csv)