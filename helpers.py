import pandas as pd
from chains import make_nd_chain_gpt
from schemas import NDResult

# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------

def run_nd_analysis(input_csv: str, output_csv: str) -> None:
    """
    Load name/job CSV, run the ND chain, and write out a CSV annotated
    with nom_det_tag and nom_det_explain.
    """
    df = pd.read_csv(input_csv)
    chain = make_nd_chain_gpt()

    results = []
    for _, row in df.iterrows():
        nd: NDResult = chain.invoke({
            "name": row["name"],
            "job_title": row["job_title"]
        })
        results.append(nd.dict())

    out = pd.concat([df, pd.DataFrame(results)], axis=1)
    out.to_csv(output_csv, index=False)
