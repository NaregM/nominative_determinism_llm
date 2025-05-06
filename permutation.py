import numpy as np
from numpy.typing import NDArray
import pandas as pd

from tqdm import tqdm
from typing import List, Tuple, Dict, Callable

from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

from helpers import binary_score

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# ---------------------------------------------------------------

def compute_scores_parallel(pairs: List[Tuple[str,str]], score_func, max_workers: int=8) -> NDArray:
    """
    Given a list of (name, job_title) pairs, compute binary scores in parallel.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        # executor.map preserves input order
        scores = list(exe.map(lambda args: binary_score(*args), pairs))
        
    return np.array(scores, dtype=int)

def permutation_test(
    input_csv: str,
    score_func: Callable,
    N: int = 20,
    M: int = 3,
    seed: int = 42,
    max_workers: int = 8
) -> Dict[str, float]:
    """
    Null hypothesis (H_0):
        There is no association between people’s surnames and their real job titles.
    
    1. Draw an N‐row sample from df.
    2. Compute observed pun‐rate.
    3. Repeat M times:
         - Permute job_title
         - Compute pun‐rate on the shuffled set
    4. Return p_obs, null median, p_value, delta, risk_ratio, null_distribution.
    """
    rng = np.random.default_rng(seed)
    df = pd.read_csv(input_csv)

    # sample N pairs
    sample = df.sample(N, replace=False, random_state=seed).reset_index(drop=True)
    names = sample["name"].tolist()
    jobs  = sample["job_title"].tolist()

    # observed
    pairs_obs = list(zip(names, jobs))
    s_obs = compute_scores_parallel(pairs_obs, max_workers)
    p_obs = s_obs.mean()

    # null distribution based on permutation
    null_rates = []
    for _ in tqdm(range(M)):
        
        permuted_jobs = list(rng.permutation(jobs))
        pairs_null   = list(zip(names, permuted_jobs))
        s_null       = compute_scores_parallel(pairs_null, max_workers)
        null_rates.append(s_null.mean())

    null_arr = np.array(null_rates)
    null_med = np.median(null_arr)

    # 4. statistics
    p_value    = (null_arr >= p_obs).mean()
    delta      = p_obs - null_med
    risk_ratio = p_obs / null_med if null_med > 0 else np.inf

    return {
        "p_obs": p_obs,
        "p_null_median": null_med,
        "p_value": p_value,
        "delta": delta,
        "risk_ratio": risk_ratio,
        "null_distribution": null_arr
    }