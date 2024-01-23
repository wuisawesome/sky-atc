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
import requests
import math

def num_gpus_configuration(max_gpus : int):
    """Courtesy of chat-gpt."""
    # Calculate the maximum power of 2 that is less than or equal to n
    max_power = math.floor(math.log(max_gpus, 2))
    # Generate all powers of 2 from 2^0 up to the maximum power
    return [2**x for x in range(max_power + 1)]


def get_secure_gpu_stock_status(id : str, gpu_count : int):
    secure_gpus_graphql_request = {
        "operationName":"SecureGpuTypes",
        "variables":{
            "gpuTypesInput":{
                "id": None,
            },
            "lowestPriceInput":
            {
                "dataCenterId":None,
                "gpuCount":gpu_count,
                "secureCloud": True
            }
        },
        "query":
        """query SecureGpuTypes($lowestPriceInput: GpuLowestPriceInput, $gpuTypesInput: GpuTypeFilter) {
  gpuTypes(input: $gpuTypesInput) {
    lowestPrice(input: $lowestPriceInput) {
      minimumBidPrice
      uninterruptablePrice
      minVcpu
      minMemory
      stockStatus
      __typename
    }
    id
    displayName
    memoryInGb
    securePrice
    communityPrice
    oneMonthPrice
    threeMonthPrice
    sixMonthPrice
    secureSpotPrice
    __typename
  }
}"""
    }

    # If we just didn't specify this we would get all the gpus 🤔. Maybe we
    # should do that? For now, we'll do it this way since the website does
    # it this way. Maybe smaller requests are better for their load?
    secure_gpus_graphql_request["variables"]["gpuTypesInput"]["id"] = id
    result = requests.post(
        f"https://api.runpod.io/graphql?api_key={runpod.api_key}",
        json = secure_gpus_graphql_request
    )

    assert result.ok, f"Result not ok {result.status_code=}, {result.text=}"

    gpu_types = result.json()["data"]["gpuTypes"]

    assert len(gpu_types) == 1, f"Multiple gpu types {gpu_types}"

    gpu_details = gpu_types[0]

    assert gpu_details["id"] == id

    return gpu_details["lowestPrice"]["stockStatus"]


def get_community_gpu_stock_status(id: str, gpu_count: int):
    community_gpus_graphql_request = {
        "operationName": "CommunityGpuTypes",
        "variables": {
            "gpuTypesInput": {
                "id": "NVIDIA H100 80GB HBM3"
            },
            "lowestPriceInput": {
                "countryCode": None,
                "gpuCount": gpu_count,
                "secureCloud": False,
                "supportPublicIp": True,
            }
        },
        "query":
        """query CommunityGpuTypes($lowestPriceInput: GpuLowestPriceInput, $gpuTypesInput: GpuTypeFilter) {
  gpuTypes(input: $gpuTypesInput) {
    lowestPrice(input: $lowestPriceInput) {
      minimumBidPrice
      uninterruptablePrice
      minVcpu
      minMemory
      stockStatus
      __typename
    }
    id
    displayName
    memoryInGb
    communityPrice
    communitySpotPrice
    __typename
  }
}"""
    }

    # If we just didn't specify this we would get all the gpus 🤔. Maybe we
    # should do that? For now, we'll do it this way since the website does
    # it this way. Maybe smaller requests are better for their load?
    community_gpus_graphql_request["variables"]["gpuTypesInput"]["id"] = id
    result = requests.post(
        f"https://api.runpod.io/graphql?api_key={runpod.api_key}",
        json = community_gpus_graphql_request
    )

    assert result.ok, f"Result not ok {result.status_code=}, {result.text=}"

    gpu_types = result.json()["data"]["gpuTypes"]

    assert len(gpu_types) == 1, f"Multiple gpu types {gpu_types}"

    gpu_details = gpu_types[0]

    assert gpu_details["id"] == id

    return gpu_details["lowestPrice"]["stockStatus"]


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
        'secureStockStatus': [], #str
        'communityStockStatus': [], # str
        'gpuCount': [], # int
    }

    gpus = runpod.api.ctl_commands.get_gpus()
    for gpu in gpus:
        id = gpu["id"]
        gpu_details = runpod.api.ctl_commands.get_gpu(id)
        for gpu_count in num_gpus_configuration(gpu_details["maxGpuCount"]):
            gpu_details["secureStockStatus"] = get_secure_gpu_stock_status(id, gpu_count)
            gpu_details["communityStockStatus"] = get_community_gpu_stock_status(id, gpu_count)
            gpu_details["timestamp"] = time.time()
            gpu_details["gpuCount"] = gpu_count
            for key in all_gpu_details:
                all_gpu_details[key].append(gpu_details[key])

    return pd.DataFrame(all_gpu_details)


def create_or_append_csv(path: Path, df : pd.DataFrame):
    try:
        existing_df = pd.read_csv(path)

        # TODO: Remove this after backporting this to existing data.
        if "gpuCount" not in existing_df.columns:
            existing_df["gpuCount"] = 1
        print("Appending to existing file...")
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
