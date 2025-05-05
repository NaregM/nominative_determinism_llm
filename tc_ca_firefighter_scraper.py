"""
Source of data: https://transparentcalifornia.com/agencies/salaries/
"""
import numpy as np
import pandas as pd
import requests

import time
from datetime import date

from bs4 import BeautifulSoup
from tqdm import tqdm
import geonamescache

# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
UA   = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36")

def scrape_name_title(city: str, year: int = 2022, sleep_s=0.6):
    """
    """
    sess = requests.Session()
    sess.headers.update({"User-Agent": UA})
    out  = []

    page = 1
    while True:
        url  = f"https://transparentcalifornia.com/salaries/{year}/{city}/?page={page}"
        resp = sess.get(url, timeout=30)
        if resp.status_code != 200:
            break                                     

        soup  = BeautifulSoup(resp.text, "html.parser")
        table = soup.find("table", class_="table")
        if not table:
            break                                    

        rows = table.tbody.find_all("tr")
        for k in range(0, len(rows), 2):               # 0,2,4 … → name/job rows
            tds  = rows[k].find_all("td")
            if len(tds) < 2:
                continue
            name = tds[0].get_text(strip=True)
            job  = tds[1].get_text(strip=True)
            out.append({"name": name, "job_title": job})

        page += 1
        time.sleep(sleep_s)            

    return pd.DataFrame(out)



if __name__ == "__main__":
    
    today = date.today()
    
    # Get all CA city names and reformat so usable with url
    gc   = geonamescache.GeonamesCache()
    ca   = [c['name'] for c in gc.get_cities().values() if c['admin1code']=='CA']
    ca_cities = [x.lower().strip().replace(' ', '-') for x in ca]
    
    names_jobtitles = []

    for city in tqdm(ca_cities[:]):

        df_tmp = scrape_name_title(city)
        res.append(df_tmp)
        time.sleep(1)

    df_tot = pd.concat(res)
    df_tot.to_csv(f'ca_all_cities_name_title_{today}.csv', index = False)
    print('Done!')