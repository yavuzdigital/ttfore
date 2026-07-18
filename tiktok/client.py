# -*- coding: utf-8 -*-
"""TikTok Android API istemcisi — parametre üretme ve istek imzalama."""
import os, sys, time, uuid, random

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

from lib.sign import Sign
from lib.utils import md5stub
from .auth   import get_cookie
from .config import DEVICE, MOBILE_USER_AGENT


def get_headers() -> dict:
    """TikTok Android uygulaması taklidi HTTP başlıkları."""
    return {
        'User-Agent':      MOBILE_USER_AGENT,
        'Connection':      'keep-alive',
        'Accept':          '*/*',
        'Accept-Encoding': 'gzip, deflate,',
        'cookie':          get_cookie(),
    }


def make_params(extra: dict = None) -> dict:
    """Android cihaz parametrelerini rastgele iid/did/ts ile üret."""
    if extra is None:
        extra = {}
    p = {
        **DEVICE,
        '_rticket': str(int(time.time() * 1000)),
        'ts':       str(int(time.time())),
        'iid':      str(random.randint(7100000000000000000, 7999999999999999999)),
        'device_id':str(random.randint(7100000000000000000, 7999999999999999999)),
        'openudid': uuid.uuid4().hex[:16],
    }
    p.update(extra)
    return p


def signed_headers(params_str: str) -> dict:
    """URL-encode edilmiş parametre string'i için imzalı başlıklar üret."""
    return Sign(params_str, headers={**get_headers(), 'x-ss-stub': md5stub('')})
