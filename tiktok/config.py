# -*- coding: utf-8 -*-
"""Tüm sabit konfigürasyon — cihaz parametreleri, URL'ler, ülke verileri, cookie'ler."""

# ── Mobil API ─────────────────────────────────────────────────────────────────

MOBILE_API_BASE = 'https://api31-normal-alisg.tiktokv.com'

MOBILE_USER_AGENT = (
    'com.zhiliaoapp.musically/2023503040 '
    '(Linux; U; Android 7.1.2; tr_TR; Pixel 4; Build/RQ3A.211001.001)'
)

# Android cihaz sabit parametreleri (rastgele ts/iid/did/oud hariç)
DEVICE: dict = {
    'device_platform':        'android',
    'os':                     'android',
    'ssmix':                  'a',
    'cdid':                   'f0de4bd2-4090-4b00-85ec-71855834b6a8',
    'channel':                'googleplay',
    'aid':                    '1233',
    'app_name':               'musical_ly',
    'version_code':           '430903',
    'version_name':           '43.9.3',
    'manifest_version_code':  '2023503040',
    'update_version_code':    '2023503040',
    'ab_version':             '43.9.3',
    'resolution':             '1080*1776',
    'dpi':                    '480',
    'device_type':            'Pixel+4',
    'device_brand':           'google',
    'language':               'tr',
    'os_api':                 '25',
    'os_version':             '7.1.2',
    'ac':                     'wifi',
    'is_pad':                 '0',
    'current_region':         'TR',
    'app_type':               'normal',
    'sys_region':             'TR',
    'last_install_time':      '1771770962',
    'mcc_mnc':                '28603',
    'timezone_name':          'Europe/Istanbul',
    'carrier_region_v2':      '286',
    'residence':              'TR',
    'build_number':           '43.9.3',
    'uoo':                    '1',
    'carrier_region':         'TR',
    'region':                 'TR',
    'locale':                 'tr-TR',
    'op_region':              'TR',
    'timezone_offset':        '10800',
    'app_language':           'tr',
    'ac2':                    'wifi',
    'host_abi':               'arm64-v8a',
}

# ── Webcast API ───────────────────────────────────────────────────────────────

WEBCAST_API_URL = 'https://webcast.tiktok.com/webcast/feed/'

WEBCAST_UA_POOL: list[str] = [
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.193 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; Redmi Note 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.111 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
]

WEBCAST_COOKIES_RAW = (
    "tta_attr_id_mirror=0.1760894537.7562984450150105104; _ga=GA1.1.1457920418.1760894536; "
    "_ga_ER02CH5NW5=GS1.1.1760894535.1.0.1760894535.0.0.1862329857; "
    "FPID=FPID2.2.143U5jsWvgsgREeMR1sbjrnKxtocNBzvWLJkxpR2SG4%3D.1760894536; "
    "FPAU=1.2.73909050.1760894539; _fbp=fb.1.1760894539423.1400597018; "
    "_tt_enable_cookie=1; _ttp=34LHmk0ENwiBUW0XIeyELLGhcNV.tt.1; "
    "passport_csrf_token=8318f14d3412a4bc3182b92fe731193b; "
    "passport_csrf_token_default=8318f14d3412a4bc3182b92fe731193b; "
    "d_ticket=c4e33dce529674d7acce93726a76e771b21d1; "
    "multi_sids=7576620581141152776%3Adaa8122115232f8a5996ffd9cebc387b; "
    "cmpl_token=AgQYAPOG_hfkTtK5G37hKOfdMfNRUv1Nkz-FDWCjSMI; "
    "sid_guard=daa8122115232f8a5996ffd9cebc387b%7C1764805813%7C15551999%7CMon%2C+01-Jun-2026+23%3A50%3A12+GMT; "
    "uid_tt=4bb091f11b16d979ece201d288ccda676ba26c99eac50c7c5b121222ba2bfbf5; "
    "uid_tt_ss=4bb091f11b16d979ece201d288ccda676ba26c99eac50c7c5b121222ba2bfbf5; "
    "sid_tt=daa8122115232f8a5996ffd9cebc387b; sessionid=daa8122115232f8a5996ffd9cebc387b; "
    "sessionid_ss=daa8122115232f8a5996ffd9cebc387b; "
    "store-idc=alisg; store-country-code=tr; store-country-code-src=uid; "
    "tt-target-idc=alisg; _m4b_theme_=new; "
    "tt_csrf_token=fx21Iarr-86iN7H1gRGWayvbHtbk2nbHLKug; "
    "csrfToken=OTQlDWok-cAaYWpeIFLLrv3NYg1F6jXiQ8Is; "
    "csrf_session_id=5b7e86493f89fe2e596afbacb1561c3a; "
    "odin_tt=297f6e99285551c948442b9709afd93f84b9caa9c9d75ed1b60cea95402ef6c25fe490c2c88df06f5e545b8e232b27aae67774252313f472cff5e90a4cece64d1e1696ce7307841e45a63c0ab4342ff9; "
    "msToken=wa0a75jJLYjR8eOzLJFqs78AKq6-B5amJ_w4POOJrV90zw3gTATnAHzTPKQtc3EdXECpulWNig3QHqAxpO_HeWV3fGSPJvDGM60GgvO9AtChi7AiiNB2J6oS9vQr"
)

# ── Ülke verileri ─────────────────────────────────────────────────────────────
# (ülke_kodu) → (region, kısa_dil, tam_dil, zaman_dilimleri)

COUNTRY_DATA: dict[str, tuple] = {
    "TR": ("TR", "tr",    "tr-TR",  ["Europe/Istanbul"]),
    "US": ("US", "en",    "en-US",  ["America/New_York", "America/Los_Angeles", "America/Chicago", "America/Denver", "America/Phoenix"]),
    "DE": ("DE", "de",    "de-DE",  ["Europe/Berlin"]),
    "GB": ("GB", "en-GB", "en-GB",  ["Europe/London"]),
    "FR": ("FR", "fr",    "fr-FR",  ["Europe/Paris"]),
    "IT": ("IT", "it",    "it-IT",  ["Europe/Rome"]),
    "ES": ("ES", "es",    "es-ES",  ["Europe/Madrid"]),
    "PT": ("PT", "pt",    "pt-PT",  ["Europe/Lisbon"]),
    "BR": ("BR", "pt-BR", "pt-BR",  ["America/Sao_Paulo", "America/Manaus"]),
    "MX": ("MX", "es-MX", "es-MX",  ["America/Mexico_City", "America/Monterrey"]),
    "AR": ("AR", "es-AR", "es-AR",  ["America/Argentina/Buenos_Aires"]),
    "CO": ("CO", "es-CO", "es-CO",  ["America/Bogota"]),
    "CL": ("CL", "es-CL", "es-CL",  ["America/Santiago"]),
    "PE": ("PE", "es-PE", "es-PE",  ["America/Lima"]),
    "CA": ("CA", "en-CA", "en-CA",  ["America/Toronto", "America/Vancouver"]),
    "AU": ("AU", "en-AU", "en-AU",  ["Australia/Sydney", "Australia/Melbourne"]),
    "NZ": ("NZ", "en-NZ", "en-NZ",  ["Pacific/Auckland"]),
    "JP": ("JP", "ja",    "ja-JP",  ["Asia/Tokyo"]),
    "KR": ("KR", "ko",    "ko-KR",  ["Asia/Seoul"]),
    "CN": ("CN", "zh",    "zh-CN",  ["Asia/Shanghai"]),
    "TW": ("TW", "zh-TW", "zh-TW",  ["Asia/Taipei"]),
    "HK": ("HK", "zh-HK", "zh-HK",  ["Asia/Hong_Kong"]),
    "TH": ("TH", "th",    "th-TH",  ["Asia/Bangkok"]),
    "VN": ("VN", "vi",    "vi-VN",  ["Asia/Ho_Chi_Minh"]),
    "ID": ("ID", "id",    "id-ID",  ["Asia/Jakarta", "Asia/Makassar"]),
    "MY": ("MY", "ms",    "ms-MY",  ["Asia/Kuala_Lumpur"]),
    "PH": ("PH", "en-PH", "en-PH",  ["Asia/Manila"]),
    "SG": ("SG", "en-SG", "en-SG",  ["Asia/Singapore"]),
    "IN": ("IN", "hi",    "hi-IN",  ["Asia/Kolkata"]),
    "PK": ("PK", "ur",    "ur-PK",  ["Asia/Karachi"]),
    "BD": ("BD", "bn",    "bn-BD",  ["Asia/Dhaka"]),
    "RU": ("RU", "ru",    "ru-RU",  ["Europe/Moscow", "Asia/Yekaterinburg"]),
    "UA": ("UA", "uk",    "uk-UA",  ["Europe/Kiev"]),
    "PL": ("PL", "pl",    "pl-PL",  ["Europe/Warsaw"]),
    "NL": ("NL", "nl",    "nl-NL",  ["Europe/Amsterdam"]),
    "BE": ("BE", "nl-BE", "nl-BE",  ["Europe/Brussels"]),
    "SE": ("SE", "sv",    "sv-SE",  ["Europe/Stockholm"]),
    "NO": ("NO", "nb",    "nb-NO",  ["Europe/Oslo"]),
    "DK": ("DK", "da",    "da-DK",  ["Europe/Copenhagen"]),
    "FI": ("FI", "fi",    "fi-FI",  ["Europe/Helsinki"]),
    "CH": ("CH", "de-CH", "de-CH",  ["Europe/Zurich"]),
    "AT": ("AT", "de-AT", "de-AT",  ["Europe/Vienna"]),
    "CZ": ("CZ", "cs",    "cs-CZ",  ["Europe/Prague"]),
    "HU": ("HU", "hu",    "hu-HU",  ["Europe/Budapest"]),
    "RO": ("RO", "ro",    "ro-RO",  ["Europe/Bucharest"]),
    "GR": ("GR", "el",    "el-GR",  ["Europe/Athens"]),
    "SA": ("SA", "ar",    "ar-SA",  ["Asia/Riyadh"]),
    "AE": ("AE", "ar-AE", "ar-AE",  ["Asia/Dubai"]),
    "EG": ("EG", "ar-EG", "ar-EG",  ["Africa/Cairo"]),
    "NG": ("NG", "en-NG", "en-NG",  ["Africa/Lagos"]),
    "ZA": ("ZA", "en-ZA", "en-ZA",  ["Africa/Johannesburg"]),
    "KE": ("KE", "en-KE", "en-KE",  ["Africa/Nairobi"]),
    "IL": ("IL", "he",    "he-IL",  ["Asia/Jerusalem"]),
    "IR": ("IR", "fa",    "fa-IR",  ["Asia/Tehran"]),
}
