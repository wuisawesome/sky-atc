"""
Create or append all runpod pricing/availability information for all gpus to a csv file.

A directory must be provided. The directory will be organized by date. All dates and times in GMT.
"""
import json
import os
from pathlib import Path
import requests
import sys
import time
import pandas as pd

def get_all_gpu_details(api_key : str) -> pd.DataFrame:
    all_gpu_details = {
        "name": [], # str
        "memory_gib": [], # float
        "storage_gib": [], # float
        "vcpus": [], # float
        "regions_with_capacity_available": [], # str
        "price_cents_per_hour": [], # float
        "timestamp": [], # float
    }

    result = requests.get("https://cloud.lambdalabs.com/api/v1/instance-types", auth=(api_key, ""))
    assert result.status_code == 200

    data = json.loads(result.text)["data"]

    timestamp = time.time()

    for instance_details in data.values():
        instance_type = instance_details["instance_type"]
        regions_with_capacity_available = instance_details["regions_with_capacity_available"]
        to_append = {
            "name": instance_type["name"],
            "memory_gib": instance_type["specs"]["memory_gib"],
            "storage_gib": instance_type["specs"]["storage_gib"],
            "vcpus": instance_type["specs"]["vcpus"],
            "regions_with_capacity_available": ",".join(regions_with_capacity_available),
            "price_cents_per_hour": instance_type["price_cents_per_hour"],
            "timestamp": timestamp,
        }

        for name in to_append:
            all_gpu_details[name].append(to_append[name])

    return pd.DataFrame(all_gpu_details)


def create_or_append_csv(path: Path, df : pd.DataFrame):
    try:
        print("Appending to existing file...")
        existing_df = pd.read_csv(path)
        df = pd.concat([existing_df, df])
    except Exception:
        print("Creating new file...")
        pass

    df.to_csv(path, index=False)


if __name__ == "__main__":
    api_key = os.environ["LAMBDALABS_API_KEY"]

    assert len(sys.argv) == 2, "Usage: python -m sky_atc.runpod.gpu_querier <output-dir>"

    dir = Path(sys.argv[1])
    day = int(time.time()) // (24 * 60 * 60)
    filename = dir / f"{day}.csv"

    print(f"Inferring file name should be {filename}")

    df = get_all_gpu_details(api_key)
    df = create_or_append_csv(filename, df)
