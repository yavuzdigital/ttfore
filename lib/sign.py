from hashlib import md5
from time import time

from .XGorgon import XGorgon
from .XLadon import Ladon
from .XArgus import Argus


def Sign(
    params: str,
    headers: dict = {},
    sec_device_id: str = "",
    aid: int = 1233,
    license_id: int = 1611921764,
    sdk_version_str: str = "v05.00.03-ov-android",
    sdk_version: int = 167773760,
    platform: int = 0,
    unix: int = None,
):
    x_ss_stub = None
    payload = None
    if "x-ss-stub" in headers:
        x_ss_stub = headers["x-ss-stub"]
        payload = x_ss_stub
    if not unix:
        unix = int(time())

    gorgon = XGorgon(params, unix, data=payload, cookies=headers.get("cookie")).get_value()

    return {
        **headers,
        **gorgon,
        "X-Ladon": Ladon.encrypt(unix, license_id, aid),
        "X-Argus": Argus.get_sign(
            params,
            x_ss_stub,
            unix,
            platform=platform,
            aid=aid,
            license_id=license_id,
            sec_device_id=sec_device_id,
            sdk_version=sdk_version_str,
            sdk_version_int=sdk_version,
        ),
    }
