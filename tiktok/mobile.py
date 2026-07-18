# -*- coding: utf-8 -*-
"""TikTok mobil (aweme/v1) API uç noktaları."""
import json, os, sys, time, uuid, random, urllib.parse, re
import requests

from .client import make_params, signed_headers
from .config import MOBILE_API_BASE as _API_BASE

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.protobuf import ProtoBuf, ProtoField, ProtoFieldType
from lib.utils import md5stub
from lib.sign import Sign


_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEVICES_FILE = os.path.join(_BASE, 'data', 'devices.txt')
_MODELS_FILE = os.path.join(_BASE, 'data', 'models.txt')

_device_pool = []
_model_pool = []


def _load_devices():
    global _device_pool, _model_pool
    if not _device_pool:
        try:
            with open(_DEVICES_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(':')
                        if len(parts) >= 6:
                            _device_pool.append({
                                'iid': parts[0],
                                'device_id': parts[1],
                                'device_type': parts[2],
                                'device_brand': parts[3],
                                'openudid': parts[4],
                                'cdid': parts[5],
                            })
        except FileNotFoundError:
            pass
    if not _model_pool:
        try:
            with open(_MODELS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(':')
                        if len(parts) >= 3:
                            _model_pool.append({
                                'brand': parts[0],
                                'model': parts[1],
                                'resolution': parts[2],
                            })
        except FileNotFoundError:
            pass


def get_random_device() -> dict:
    """Devices.txt'den rastgele bir cihaz profili döndür."""
    _load_devices()
    if not _device_pool:
        return {
            'iid': '7663822013170108181',
            'device_id': '7663820368272147988',
            'device_type': 'G011A',
            'device_brand': 'google',
            'openudid': 'c0a8e4f2b3d1a9c7',
            'cdid': 'f0de4bd2-4090-4b00-85ec-71855834b6a8',
        }
    return random.choice(_device_pool)


def register_device(model: dict = None) -> dict:
    """service/2/device_register/ — yeni cihaz kaydet, device_id + install_id döndür."""
    from .auth import get_cookie as _get_cookie
    from lib.sign import Sign

    _load_devices()
    if not model:
        model = random.choice(_model_pool) if _model_pool else {
            'brand': 'google', 'model': 'G011A', 'resolution': '1600*900'
        }

    ts = int(time.time())
    openudid = uuid.uuid4().hex[:16]
    cdid = str(uuid.uuid4())
    clientudid = str(uuid.uuid4())
    req_id = str(uuid.uuid4())
    iid = str(random.randint(7100000000000000000, 7999999999999999999))
    did = str(random.randint(7100000000000000000, 7999999999999999999))
    google_aid = str(uuid.uuid4())
    res = model['resolution'].replace('*', 'x')

    p = {
        "req_id": req_id, "_rticket": str(ts * 1000),
        "manifest_version_code": "440602", "app_language": "tr",
        "app_type": "normal", "iid": iid,
        "app_package": "com.zhiliaoapp.musically.go",
        "channel": "googleplay", "device_type": model['model'],
        "language": "tr", "host_abi": "x86_64", "locale": "tr-TR",
        "resolution": "900*1600", "openudid": openudid,
        "update_version_code": "440602", "ac2": "wifi",
        "cdid": cdid, "sys_region": "TR",
        "os_api": "28", "timezone_name": "Europe/Istanbul", "dpi": "300",
        "carrier_region": "TR", "ac": "wifi", "os": "android",
        "device_id": did, "os_version": "9",
        "timezone_offset": "10800", "version_code": "440602",
        "app_name": "musically_go", "ab_version": "44.6.2",
        "version_name": "44.6.2", "device_brand": model['brand'],
        "op_region": "TR", "ssmix": "a", "device_platform": "android",
        "build_number": "44.6.2", "region": "TR", "aid": "1340",
        "ts": str(ts),
    }
    enc = urllib.parse.urlencode(p)

    body_json = json.dumps({
        "header": {
            "os": "Android", "os_version": "9", "os_api": 28,
            "device_model": model['model'], "device_brand": model['brand'],
            "device_manufacturer": model['brand'],
            "cpu_abi": "arm64-v8a", "density_dpi": 300,
            "display_density": "mdpi", "resolution": res,
            "display_density_v2": "xhdpi", "resolution_v2": res,
            "access": "wifi", "rom": "rel.cjw.20220518.114133",
            "rom_version": f"{model['brand']}-user 9.0.0 20171130.276299 release-keys",
            "language": "tr", "timezone": 3, "region": "TR",
            "tz_name": "Europe/Istanbul", "tz_offset": 10800,
            "sim_region": "tr", "carrier": "Turkcell", "mcc_mnc": "28601",
            "clientudid": clientudid, "openudid": openudid,
            "channel": "googleplay", "not_request_sender": 1, "aid": 1340,
            "release_build": "e2f78a7_20260713", "ab_version": "44.6.2",
            "google_aid": google_aid, "gaid_limited": 0,
            "custom": {"lite_app_type": 3, "filter_warn": 0, "is_kids_mode": 0},
            "package": "com.zhiliaoapp.musically.go",
            "app_version": "44.6.2", "app_version_minor": "",
            "version_code": 440602, "update_version_code": 440602,
            "manifest_version_code": 440602,
            "app_name": "musically_go", "tweaked_channel": "googleplay",
            "display_name": "TikTok Lite",
            "install_id": iid, "device_id": did,
            "sig_hash": "aea615ab910015038f73c47e45d21466",
            "cdid": cdid, "device_platform": "android",
            "git_hash": "a78e02b", "sdk_version_code": 2051120,
            "sdk_target_version": 30, "req_id": req_id,
            "sdk_version": "2.5.11-alpha.0", "guest_mode": 0,
            "sdk_flavor": "i18nInner",
            "apk_first_install_time": (ts - random.randint(100, 86400)) * 1000,
            "is_system_app": 0,
        },
        "magic_tag": "ss_app_log",
        "_gen_time": ts * 1000 + random.randint(0, 999),
    })

    cookie = _get_cookie() + f'; install_id={iid}'
    hdrs = {
        'User-Agent': 'com.zhiliaoapp.musically.go/440602 (Linux; U; Android 9; tr_TR; ' + model['model'] + '; Build/PI;tt-ok/3.12.13.54.lite-ul)',
        'Accept-Encoding': 'gzip', 'Connection': 'Keep-Alive',
        'cookie': cookie, 'sdk-version': '2', 'passport-sdk-version': '1',
        'Content-Type': 'application/json; charset=utf-8',
        'x-ss-stub': md5stub(body_json),
        'x-ss-dp': '1340', 'x-tt-ultra-lite': '1',
        'x-vc-bdturing-sdk-version': '2.3.15.i18n',
        'x-tt-pba-encode': '0020',
    }
    signed = Sign(enc, headers=hdrs)

    for attempt in range(3):
        if attempt > 0:
            body_obj = json.loads(body_json)
            body_obj["header"]["install_id"] = str(random.randint(7100000000000000000, 7999999999999999999))
            body_obj["header"]["device_id"] = str(random.randint(7100000000000000000, 7999999999999999999))
            body_json = json.dumps(body_obj)
            hdrs['x-ss-stub'] = md5stub(body_json)
            signed = Sign(enc, headers=hdrs)

        r = requests.post(
            f"https://log16-normal-alisg.tiktokv.com/service/2/device_register/?{enc}",
            data=body_json, headers=signed, timeout=15,
        )
        try:
            data = r.json()
            did_r = data.get("device_id_str") or str(data.get("device_id", "0"))
            iid_r = data.get("install_id_str") or str(data.get("install_id", "0"))
            if did_r != "0" and iid_r != "0":
                return {
                    "device_id": did_r, "install_id": iid_r,
                    "iid": iid_r, "device_type": model['model'],
                    "device_brand": model['brand'],
                    "openudid": openudid, "cdid": cdid,
                    "new_user": data.get("new_user", 0),
                }
        except Exception:
            pass

    return {"error": "all attempts failed", "raw": r.text[:300] if r else ""}


def video_feed(session: requests.Session, cursor: int = 0, count: int = 20) -> dict:
    """Genel video akışını döndür (aweme/v1/feed)."""
    p = make_params({
        'max_cursor': str(cursor),
        'min_cursor': '0',
        'count':      str(count),
        'pull_type':  '2',
    })
    enc = urllib.parse.urlencode(p)
    r = session.get(
        f'{_API_BASE}/aweme/v1/feed/?{enc}',
        headers=signed_headers(enc),
        timeout=15,
    )
    try:
        return r.json() if r.content else {}
    except Exception:
        return {}


def _dict_to_proto(data: dict) -> ProtoBuf:
    """Recursively convert a dict to ProtoBuf with correct wire types."""
    pb = ProtoBuf()
    for k, v in data.items():
        idx = int(k)
        if isinstance(v, dict):
            pb.putProtoBuf(idx, _dict_to_proto(v))
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    inner = _dict_to_proto(item)
                    pb.putProtoBuf(idx, inner)
                elif isinstance(item, int):
                    if abs(item) > 0x7FFFFFFF:
                        pb.putInt64(idx, item)
                    else:
                        pb.putVarint(idx, item)
                elif isinstance(item, str):
                    pb.putUtf8(idx, item)
        elif isinstance(v, str):
            pb.putUtf8(idx, v)
        elif isinstance(v, bool):
            pb.putVarint(idx, 1 if v else 0)
        elif isinstance(v, int):
            if abs(v) > 0x7FFFFFFF:
                pb.putInt64(idx, v)
            else:
                pb.putVarint(idx, v)
        elif isinstance(v, float):
            pb.putUtf8(idx, str(v))
    return pb


def feed_v2(feed_type: int = 0, count: int = 6, cursor: int = 0,
            region: str = "US", language: str = "en") -> dict:
    """aweme/v2/feed/ — protobuf tabanlı video akışı."""
    _API_BASE_V2 = "https://api32-core-alisg.tiktokv.com"

    session_id = str(uuid.uuid4())
    now_ms = int(time.time() * 1000)
    now_sec = int(time.time())

    body = _dict_to_proto({
        "1": 0, "2": 0, "3": cursor, "4": feed_type, "5": 0, "7": 0,
        "8": "0.2", "10": 1, "18": 0, "26": "", "27": "", "30": 0,
        "31": 0, "32": 0, "34": 0, "36": 0, "37": "", "38": "", "40": count,
        "43": "", "44": 0, "46": region, "48": 0, "49": 0,
        "50": "enter_auto", "51": 1, "52": session_id + "#1", "53": "0",
        "57": 0, "58": 0, "59": 0, "60": 0, "65": "", "66": 0, "68": 0,
        "69": "", "79": "", "91": "Mozilla/5.0 (Linux; Android 9; G011A Build/PI; wv) AppleWebKit/537.36",
        "110": 0, "133": session_id + "#1", "141": "",
        "143": -1,
        "144": {
            "1": {
                "1": {"1": b"\x00\x00\x00\xa0\x99\x99\xd9\x3f", "2": 0},
                "2": 0, "3": b"\x00\x00\x00\x60\x66\x66\xf2\x3f", "5": "",
                "6": b"\x00\x00\x00\x00\x00\x00\x08\x40",
                "7": b"\x00\x00\x00\x00\x00\x00\x00\x00", "8": 1, "9": 0,
                "10": 0, "11": 1, "12": b"\x00\x00\x00\x60\x9b\xe0\x65\x40",
                "13": b"\x9b\xfa\x10\xd7\x4e\x91\xe0\x3f",
                "15": b"\x00\x00\x00\x00\x00\x00\x3d\x40", "17": "",
                "19": "0", "20": "0", "21": "0", "22": "0.0", "23": "",
                "24": 0, "28": 5, "29": 0,
            },
            "2": {"1": [], "2": 0, "5": "", "6": "", "7": 0, "8": 0,
                  "9": 0, "10": 0, "14": {"1": 0, "2": 0, "3": 0, "4": 0},
                  "16": now_ms},
            "3": "{}",
            "4": {"1": 4000, "2": 4000},
        },
        "145": "96_96", "147": 0, "149": "2024600030", "152": 3,
        "155": 0, "156": 0,
        "159": {
            "1": 1, "2": 1,
            "3": {"1": {"1": "1233", "2": "0", "3": "0", "4": "tr"},
                  "2": {"1": "1233", "2": str(now_sec - 120), "3": "0", "4": "tr"}},
            "4": "", "5": json.dumps([{"duration": 0, "page_id": "JOURNEY_SLOGAN_ID"},
                                       {"duration": 1323, "page_id": "JOURNEY_PUSH_PERMISSION_BACKGROUND"},
                                       {"duration": 2361, "page_id": "JOURNEY_INTERESTS_ID"},
                                       {"duration": 1238, "page_id": "JOURNEY_SWIPE_UP_ID"}]),
            "6": 5, "7": 0,
        },
        "160": -1,
        "161": {"1": 0, "2": 0,
                "3": {"1": 0, "2": 0, "7": now_sec - 120, "8": 1}},
        "162": {"1": {"1": md5stub("").lower()}},
        "163": 1, "167": {"1": 0, "2": 0, "3": 0, "4": 0}, "172": 0,
        "174": "0_0_2,", "175": "", "181": 0, "183": 0,
        "184": {"1": {"1": "feed_component"}}, "185": 0, "187": 0,
        "188": {"1": 0, "2": 0, "3": 0}, "195": 0,
        "196": -1, "197": 0,
        "198": -1, "199": 0,
        "200": 480, "201": 853, "202": "Small screen", "204": 0,
    })

    body_bytes = body.toBuf()
    body_md5 = md5stub(body_bytes)

    p = make_params({
        "effect_sdk_version": "21.8.0",
        "req_from": "enter_auto",
        "pull_type": "0",
        "app_version": "2024600030",
        "is_non_personalized": "0",
        "language":         language,
        "current_region":   region,
        "region":           region,
        "app_language":     language,
        "carrier_region":   region,
        "sys_region":       region,
        "op_region":        region,
        "residence":        region,
        "locale":           f"{language}-{region}",
        "timezone_name":    "America/New_York",
        "timezone_offset":  "-18000",
        "mcc_mnc":          "310410",
    })
    enc = urllib.parse.urlencode(p)
    url = f"{_API_BASE_V2}/aweme/v2/feed/?{enc}"

    from .client import get_headers
    from .auth import get_cookie as _get_cookie
    cookie = _get_cookie()
    hdrs = get_headers()
    hdrs.update({
        "Content-Type": "application/x-protobuf",
        "x-ss-stub": body_md5,
        "cookie": cookie,
    })
    signed = Sign(enc, headers=hdrs)

    r = requests.post(url, data=body_bytes, headers=signed, timeout=30)
    try:
        import os as _os
        _os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
        from lib.aweme_v2_pb2 import AwemeV2FeedResponse
        feed = AwemeV2FeedResponse()
        feed.ParseFromString(r.content)
        from google.protobuf.json_format import MessageToDict
        return MessageToDict(feed, preserving_proto_field_name=True)
    except Exception as e:
        try:
            pb = ProtoBuf(r.content)
            return pb.toJson()
        except Exception:
            return {"error": str(e), "_parse_error": True, "raw": r.text[:500]}


def _search_base(endpoint: str, keyword: str, extra_body: dict = None,
                  count: int = 10, cursor: int = 0) -> dict:
    """Tüm search API'leri için ortak imzalı POST isteği."""
    from .auth import get_cookie as _get_cookie
    from lib.sign import Sign

    dev = get_random_device()
    ts = int(time.time())
    search_id = str(uuid.uuid4()).replace("-", "")

    p = {
        "device_platform": "android", "os": "android", "ssmix": "a",
        "channel": "googleplay", "aid": "1233", "app_name": "musical_ly",
        "version_code": "460003", "version_name": "46.0.3",
        "manifest_version_code": "2024600030", "update_version_code": "2024600030",
        "ab_version": "46.0.3", "resolution": "1600*900", "dpi": "300",
        "device_type": dev["device_type"], "device_brand": dev["device_brand"],
        "language": "tr", "os_api": "28", "os_version": "9",
        "ac": "wifi", "is_pad": "0", "current_region": "TR", "app_type": "normal",
        "sys_region": "TR", "mcc_mnc": "28601", "timezone_name": "Europe/Istanbul",
        "residence": "TR", "app_language": "tr", "carrier_region": "TR",
        "timezone_offset": "10800", "host_abi": "arm64-v8a", "locale": "tr-TR",
        "ac2": "wifi", "uoo": "0", "op_region": "TR", "build_number": "46.0.3",
        "region": "TR", "last_install_time": str(ts - 120),
        "iid": dev["iid"], "device_id": dev["device_id"],
        "openudid": dev["openudid"],
        "ts": str(ts), "_rticket": str(ts * 1000),
    }
    enc = urllib.parse.urlencode(p)

    body_data = {
        "keyword": keyword,
        "count": str(count),
        "cursor": str(cursor),
        "search_id": search_id,
        "search_source": "switch_tab",
        **(extra_body or {}),
    }
    # search_id eklenmemisse uret
    if "search_id" not in body_data:
        body_data["search_id"] = search_id

    body_enc = urllib.parse.urlencode(body_data)

    cookie = _get_cookie() + f'; install_id={dev["iid"]}'
    hdrs = {
        'User-Agent': f'com.zhiliaoapp.musically/2024600030 (Linux; U; Android 9; tr_TR; {dev["device_type"]}; Build/PI;tt-ok/3.12.13.21)',
        'Accept-Encoding': 'gzip', 'Connection': 'Keep-Alive', 'cookie': cookie,
        'sdk-version': '2', 'passport-sdk-version': '1',
        'oec-cs-sdk-version': 'v10.02.10-ov-android_V31', 'oec-cs-si-a': '2',
        'oec-vc-sdk-version': '3.2.3.i18n', 'x-vc-bdturing-sdk-version': '2.4.2.i18n',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-ss-stub': md5stub(body_enc),
    }
    signed = Sign(enc, headers=hdrs)

    r = requests.post(f"https://search32-normal-alisg.tiktokv.com/{endpoint}?{enc}",
                      data=body_enc, headers=signed, timeout=15)
    try:
        return r.json()
    except Exception:
        return {"status_code": -1, "error": "parse failed"}


def search(keyword: str, type: str = "0", count: int = 10, cursor: int = 0) -> dict:
    """Genel arama (discover/search). type: 0=video, 1=kullanici, 2=hashtag, 3=music"""
    return _search_base("aweme/v1/discover/search/", keyword, {
        "type": type, "enter_from": "homepage_hot", "hot_search": "0",
        "is_filter_search": "0", "query_correct_type": "1", "multi_virtual_rs": "1",
    }, count, cursor)


def search_video(keyword: str, count: int = 10, cursor: int = 0,
                 sort_type: int = 0, publish_time: int = 0) -> dict:
    """Video arama (search/item)."""
    return _search_base("aweme/v1/search/item/", keyword, {
        "source": "video_search", "sort_type": str(sort_type),
        "publish_time": str(publish_time), "hot_search": "0",
        "is_filter_search": "0", "query_correct_type": "1",
        "enter_from": "homepage_hot", "search_channel": "",
        "multi_virtual_rs": "1",
    }, count, cursor)


def search_music(keyword: str, count: int = 10, cursor: int = 0,
                 sort_type: int = 0, filter_by: int = 0) -> dict:
    """M\u00fczik arama (music/search)."""
    return _search_base("aweme/v1/music/search/", keyword, {
        "source": "music", "sort_type": str(sort_type),
        "filter_by": str(filter_by), "hot_search": "0",
        "enter_from": "homepage_hot", "is_filter_search": "0",
        "query_correct_type": "1", "multi_virtual_rs": "1",
    }, count, cursor)


def search_live(keyword: str, count: int = 10, cursor: int = 0) -> dict:
    """Canli yayin arama (live/search)."""
    return _search_base("aweme/v1/live/search/", keyword, {
        "source": "live", "enter_from": "normal_search",
        "search_source": "switch_tab",
    }, count, cursor)


def search_photo(keyword: str, count: int = 10, cursor: int = 0,
                 sort_type: int = 0, publish_time: int = 0) -> dict:
    """Foto\u011fraf arama (search/photo)."""
    return _search_base("aweme/v1/search/photo/", keyword, {
        "source": "photos", "sort_type": str(sort_type),
        "publish_time": str(publish_time), "hot_search": "0",
        "is_filter_search": "0", "query_correct_type": "1",
        "enter_from": "homepage_hot", "search_channel": "mt_photo",
        "multi_virtual_rs": "1",
    }, count, cursor)


def search_place(keyword: str, count: int = 10, cursor: int = 0) -> dict:
    """Yer/mekan arama (search/place)."""
    return _search_base("aweme/v1/search/place/", keyword, {
        "search_source": "switch_tab",
    }, count, cursor)


def resolve_uid(username: str) -> str | None:
    """TikTok @kullanıcı adını sayısal UID'ye çevir.

    Arama API'si ile kullanıcı ara.
    """
    target = username.lstrip("@")
    try:
        data = search(target, type=1, count=5)
        if data.get("status_code") == 0:
            for item in data.get("user_list", []):
                user = item.get("user_info", {}) or item.get("user", {})
                if user.get("unique_id", "").lower() == target.lower():
                    return str(user.get("uid") or user.get("id", ""))
    except Exception:
        pass
    return None



