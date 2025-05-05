import numpy as np
import pandas as pd

import argparse
from helpers import run_nd_analysis

# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------

if __name__ == "__main__":
    
    p = argparse.ArgumentParser()
    p.add_argument("--input_csv", required=True, help="path to input CSV")
    p.add_argument("--output_csv", required=True, help="path to write results CSV")

    args = p.parse_args()
    
    run_nd_analysis(args.input_csv, args.output_csv)