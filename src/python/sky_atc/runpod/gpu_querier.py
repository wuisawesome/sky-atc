"""
Create or append all runpod pricing/availability information for all gpus to a csv file.

A directory must be provided. The directory will be organized by date. All dates and times in GMT.

TODO: This script probably doesn't belong here just because it's runpod related.
"""
import os
from pathlib import Path
import runpod
import runpod.api.ctl_commands
import sys
import time
import pandas as pd

def get_all_gpu_details() -> pd.DataFrame:
    all_gpu_details = {
        'id': [], # str
        'timestamp': [], # float
        'communityCloud': [], # bool
        'communityPrice': [], # float
        'communitySpotPrice': [], #float
        'maxGpuCount': [], # int
        'memoryInGb': [], # int
        'secureCloud': [], # bool
        'securePrice': [], #float
        'secureSpotPrice': [], # float
        'oneWeekPrice': [], # float
        'oneMonthPrice': [], # float
        'threeMonthPrice': [], #float
    }

    gpus = runpod.api.ctl_commands.get_gpus()
    for gpu in gpus:
        id = gpu["id"]
        gpu_details = runpod.api.ctl_commands.get_gpu(id)
        gpu_details["timestamp"] = time.time()

        for key in all_gpu_details:
            all_gpu_details[key].append(gpu_details[key])

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
    runpod.api_key = os.environ["RUNPOD_API_KEY"]

    assert len(sys.argv) == 2, "Usage: python -m sky_atc.runpod.gpu_querier <output-dir>"

    dir = Path(sys.argv[1])
    day = int(time.time()) // (24 * 60 * 60)
    filename = dir / f"{day}.csv"

    print(f"Inferring file name should be {filename}")

    df = get_all_gpu_details()
    df = create_or_append_csv(filename, df)
