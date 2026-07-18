# -*- coding: utf-8 -*-
"""TikTok oturum cookie'si yükleme ve yönetimi."""
import os

_BASE        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_COOKIE_FILE = os.path.join(_BASE, 'www.tiktok.com_cookies.txt')

_cookie_str: str | None = None


def get_cookie() -> str:
    """Netscape formatındaki cookie dosyasını okuyup tek string olarak döndür."""
    global _cookie_str
    if _cookie_str:
        return _cookie_str
    for path in [_COOKIE_FILE, os.path.join(_BASE, 'cookies.txt')]:
        if not os.path.exists(path):
            continue
        cookies: dict[str, str] = {}
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split('\t')
                if len(parts) >= 7:
                    cookies[parts[5]] = parts[6]
        if cookies:
            _cookie_str = '; '.join(f'{k}={v}' for k, v in cookies.items())
            return _cookie_str
    return ''


def invalidate() -> None:
    """Cookie cache'ini sıfırla (dosya değiştiğinde çağır)."""
    global _cookie_str
    _cookie_str = None
