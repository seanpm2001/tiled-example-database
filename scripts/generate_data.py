#!/usr/env/bin python

# Usage: generate_sample_data.py DATABASE_URI

import sys
from tiled.catalog import from_uri
from tiled.client import Context, from_context
from tiled.server.app import build_app
import pandas as pd
import glob

uri = sys.argv[1]
catalog = from_uri(uri, writable_storage="temp")
with Context.from_app(build_app(catalog)) as context:
    client = from_context(context)
    # Write data generated test data
    for i in range(10000):
        client.write_array(
            [i],
            metadata={
                "number": i,
                "number_as_string": str(i),
                "nested": {"number": i, "number_as_string": str(i), "bool": bool(i)},
                "bool": bool(i),
            },
        )
    # Write in captured PandAblocks data
    jsonl_files = glob.glob('./data/panda_output/*.jsonl')
    for file in jsonl_files:
        pandas_data = pd.read_json(file, lines=True)
        for index, row in pandas_data.iterrows():
            client.write_array([0], metadata=row.to_dict())
