"""Smart bulb wrapper"""

import asyncio
from collections import Counter
from kasa import Discover, smartdevice

from common import EXPECTED_BULB_NAMES
from common.decs import retry

class ExpectedBulbsNotFoundException(Exception):
    """When the bulbs we want just aren't there :("""
    pass

@retry(ExpectedBulbsNotFoundException)
def get_bulbs(expected_bulbs=None):
    """Finds all the bulbs and returns the connection objects"""
    if not expected_bulbs:
        expected_bulbs = EXPECTED_BULB_NAMES

    bulbs = {}
    devices = asyncio.run(Discover.discover())
    for device in devices.values():
        if hasattr(device, "device_type"):
            if device.device_type == smartdevice.DeviceType.Bulb:
                bulbs[device.alias] = device

    if Counter(list(bulbs.keys())) != Counter(expected_bulbs):
        raise ExpectedBulbsNotFoundException(f"Not all expected bulbs found. Found bulbs: {bulbs}")

    return bulbs

def async_run(obj):
    """Run the supplied object/command via asyncio"""
    return asyncio.run(obj)
