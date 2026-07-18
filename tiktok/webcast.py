# -*- coding: utf-8 -*-
"""TikTok webcast (canlı yayın) API — fetch mantığı ve IP tespiti."""
import json
import random
import urllib.request as urllib_req

try:
    import aiohttp
except ImportError:
    aiohttp = None

from .config import (
    COUNTRY_DATA,
    WEBCAST_API_URL     as _API_URL,
    WEBCAST_COOKIES_RAW as _COOKIES_RAW,
    WEBCAST_UA_POOL     as _UA_POOL,
)


def parse_cookies(raw: str) -> dict:
    """Cookie string'ini dict'e çevir."""
    cookies = {}
    for item in raw.split('; '):
        if '=' in item:
            k, v = item.split('=', 1)
            cookies[k.strip()] = v
    return cookies


def get_webcast_cookies() -> dict:
    """Varsayılan webcast cookie'lerini dict olarak döndür."""
    return parse_cookies(_COOKIES_RAW)


def detect_country_ip() -> str:
    """Mevcut IP adresine göre ülke kodunu tespit et, bulamazsa 'TR' döndür."""
    services = [
        ("https://ipapi.co/json/",   lambda d: d.get("country_code")),
        ("https://ip-api.com/json/", lambda d: d.get("countryCode")),
        ("https://ipwho.is/",        lambda d: d.get("country_code")),
    ]
    for url, extractor in services:
        try:
            req = urllib_req.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib_req.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                code = (extractor(data) or "").upper().strip()
                if code and len(code) == 2:
                    return code
        except Exception:
            continue
    return "TR"


async def fetch_live_rooms(session, cookies: dict, country_info: tuple,
                           get_ua=None) -> list:
    """
    webcast.tiktok.com/webcast/feed/ uç noktasından canlı yayın odalarını çek.
    get_ua: User-Agent string'i döndüren callable (opsiyonel).
    """
    region, _lang_short, _lang_full, timezones = country_info
    ua_str = (get_ua() if callable(get_ua) else None) or random.choice(_UA_POOL)

    # Hesap cookie'sindeki ülkeyi istek ülkesiyle ezerek içerik bölgesini yönlendirmeyi dene.
    # "store-country-code-src=ip" → TikTok bu değeri "uid" (hesap) yerine IP'den gelmiş sayar,
    # bu sayede hesabın kök ülkesi yerine istenen region parametresi baskın olur.
    cookies = {
        **cookies,
        "store-country-code":     region.lower(),
        "store-country-code-src": "ip",
    }

    # DevTools'tan alınan gerçek istek analizi:
    # İçerik ülkesi app_language/tz_name'den değil, gerçek IP + region param'dan belirleniyor.
    # Bu yüzden dil parametreleri hesabın diline (TR) sabitlendi; sadece region değişiyor.
    headers = {
        "Accept":          "*/*",
        "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
        "User-Agent":      ua_str,
        "Origin":          "https://www.tiktok.com",
        "Referer":         "https://www.tiktok.com/",
    }
    if "msToken" in cookies:
        headers["msToken"] = cookies["msToken"]

    params = {
        "aid":              "1988",
        "app_language":     "tr-TR",      # Hesap dili — bölgeyle değişmez
        "app_name":         "tiktok_web",
        "browser_language": "tr-TR",      # Hesap dili
        "browser_name":     "Mozilla",
        "browser_online":   "true",
        "browser_platform": "Win32",      # Gerçek istek: Win32 (linux değil)
        "browser_version":  ua_str,
        "channel":          "tiktok_web",
        "channel_id":       "87",         # Gerçek istek: 87
        "cookie_enabled":   "true",
        "cpu_number":       "12",         # Gerçek istek: 12
        "data_collection_enabled": "true",
        "device_id":        str(random.randint(7500000000000000000, 7599999999999999999)),
        "device_platform":  "web_mobile",
        "device_type":      "web_h265",
        "focus_state":      "true",
        "from_page":        "",           # Gerçek istek: boş string
        "history_len":      str(random.randint(2, 10)),
        "is_fullscreen":    "false",
        "is_non_personalized": "0",
        "is_page_visible":  "true",
        "max_time":         "0",          # Gerçek istek: max_time=0
        "os":               "ios",        # Gerçek istek: ios (android değil)
        "priority_region":  region,       # ← Ülke filtresi
        "referer":          "",           # Gerçek istek: boş string
        "region":           region,       # ← Ülke filtresi
        "req_from":         "live_mt_pc_web_rec_tab_refresh",  # Gerçek istek
        "root_referer":     "https://www.google.com/",         # Gerçek istek
        "screen_height":    "932",        # iPhone 15 Pro Max boyutları
        "screen_width":     "430",
        "tz_name":          random.choice(timezones),
        "user_is_login":    "true",
        "webcast_language": "tr-TR",      # Hesap dili
    }

    try:
        async with session.get(
            _API_URL,
            headers=headers,
            cookies=cookies,
            params=params,
            timeout=aiohttp.ClientTimeout(total=6, connect=4, sock_read=5),
        ) as resp:
            if not resp.ok:
                return []
            data = json.loads(await resp.text())
            return data.get("data", [])
    except Exception:
        return []
