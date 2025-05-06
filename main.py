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
    #p.add_argument("--output_csv", required=True, help="path to write results CSV")

    args = p.parse_args()
    pprint(permutation_test(args.input_csv, binary_score))
    #run_nd_analysis(args.input_csv, args.output_csv)