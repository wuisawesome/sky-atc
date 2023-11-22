import pytest
import os

import sky_atc.runpod
from sky_atc.runpod import RunPodProvider

def test_basic():
    assert "RUNPOD_API_KEY" in os.environ

    provider = RunPodProvider()


