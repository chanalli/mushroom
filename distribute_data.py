from ucimlrepo import fetch_ucirepo
import pandas as pd
import numpy as np
import json
import hashlib
import requests

#fetch dataset
mushroom = fetch_ucirepo(id=73)

#data (as pandas dataframes)
x = mushroom.data.features
y = mushroom.data.targets
df = pd.merge(y, x, left_index=True, right_index=True)

df.fillna('?', inplace=True)

DATABASE_URLS = {
    0: "https://dsci551-project-af6fd-db0.firebaseio.com/",
    1: "https://dsci551-project-af6fd-db1.firebaseio.com/",
    2: "https://dsci551-project-af6fd-db2.firebaseio.com/",
    3: "https://dsci551-project-af6fd-db3.firebaseio.com/",
    4: "https://dsci551-project-af6fd-db4.firebaseio.com/",
    5: "https://dsci551-project-af6fd-db5.firebaseio.com/",
    6: "https://dsci551-project-af6fd-db6.firebaseio.com/",
    7: "https://dsci551-project-af6fd-db7.firebaseio.com/",
}

def gen_hash(gillcolor, capcolor, habitat):
  """
  Returns integer value that corresponds to predefined databases based
  on hash number that is generated from mushroom dataset features of
  gill color, cap color, and habitat.
  """
  new_string = f"{gillcolor}{capcolor}{habitat}"
  hash_obj = hashlib.sha256(new_string.encode())
  hash_num = int(hash_obj.hexdigest(), 16)
  return hash_num % len(DATABASE_URLS)

def populate_dbs(row, index, db_links):
  data_json = row.to_json()
  db_id = gen_hash(row['gill-color'], row['cap-color'], row['habitat'])
  target_db = db_links[db_id]
  url = f"{target_db}/{index}.json"
  
  response = requests.put(url, data=data_json)
  if response.status_code != 200:
    print(f"Failed to upload data to {url}. Status code: {response.status_code}")

for index, row in df.iterrows():
    populate_dbs(row, index, DATABASE_URLS)
