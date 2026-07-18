# -*- coding: utf-8 -*-
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

from flask import Flask, render_template, jsonify, request
import sys, os, asyncio
import requests as req_lib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tiktok.auth    import get_cookie
from tiktok.mobile  import video_feed, resolve_uid, feed_v2, search, search_video, search_music, search_live, search_photo, search_place, register_device
from tiktok.webcast import (
    COUNTRY_DATA, detect_country_ip,
    fetch_live_rooms, get_webcast_cookies,
)

try:
    import aiohttp
    LIVE_DEPS_OK = True
except ImportError:
    LIVE_DEPS_OK = False

app      = Flask(__name__)
_session = req_lib.Session()

# ── ROUTES ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/cookie')
def api_cookie():
    """Cookie'nin yüklü ve geçerli olup olmadığını kontrol et."""
    return jsonify({'ok': bool(get_cookie())})


@app.route('/api/countries')
def api_countries():
    """Desteklenen 54 ülkenin kod + isim listesini döndür."""
    names = {
        "TR": "🇹🇷 Türkiye",  "US": "🇺🇸 ABD",          "DE": "🇩🇪 Almanya",      "GB": "🇬🇧 İngiltere",
        "FR": "🇫🇷 Fransa",   "IT": "🇮🇹 İtalya",        "ES": "🇪🇸 İspanya",      "PT": "🇵🇹 Portekiz",
        "BR": "🇧🇷 Brezilya", "MX": "🇲🇽 Meksika",       "AR": "🇦🇷 Arjantin",     "CO": "🇨🇴 Kolombiya",
        "CL": "🇨🇱 Şili",     "PE": "🇵🇪 Peru",           "CA": "🇨🇦 Kanada",       "AU": "🇦🇺 Avustralya",
        "NZ": "🇳🇿 Yeni Zelanda", "JP": "🇯🇵 Japonya",   "KR": "🇰🇷 Güney Kore",  "CN": "🇨🇳 Çin",
        "TW": "🇹🇼 Tayvan",   "HK": "🇭🇰 Hong Kong",     "TH": "🇹🇭 Tayland",      "VN": "🇻🇳 Vietnam",
        "ID": "🇮🇩 Endonezya","MY": "🇲🇾 Malezya",       "PH": "🇵🇭 Filipinler",   "SG": "🇸🇬 Singapur",
        "IN": "🇮🇳 Hindistan","PK": "🇵🇰 Pakistan",      "BD": "🇧🇩 Bangladeş",    "RU": "🇷🇺 Rusya",
        "UA": "🇺🇦 Ukrayna",  "PL": "🇵🇱 Polonya",       "NL": "🇳🇱 Hollanda",     "BE": "🇧🇪 Belçika",
        "SE": "🇸🇪 İsveç",    "NO": "🇳🇴 Norveç",        "DK": "🇩🇰 Danimarka",    "FI": "🇫🇮 Finlandiya",
        "CH": "🇨🇭 İsviçre",  "AT": "🇦🇹 Avusturya",     "CZ": "🇨🇿 Çekya",        "HU": "🇭🇺 Macaristan",
        "RO": "🇷🇴 Romanya",  "GR": "🇬🇷 Yunanistan",    "SA": "🇸🇦 S. Arabistan", "AE": "🇦🇪 BAE",
        "EG": "🇪🇬 Mısır",    "NG": "🇳🇬 Nijerya",       "ZA": "🇿🇦 G. Afrika",    "KE": "🇰🇪 Kenya",
        "IL": "🇮🇱 İsrail",   "IR": "🇮🇷 İran",
    }
    return jsonify([{"code": k, "name": v} for k, v in names.items()])


@app.route('/api/resolve', methods=['POST'])
def api_resolve():
    """TikTok @kullanıcı adını sayısal UID'ye çevir."""
    u = (request.json or {}).get('username', '').strip().lstrip('@')
    if not u:
        return jsonify({'error': 'username gerekli'})
    uid = resolve_uid(u)
    return jsonify({'uid': uid} if uid else {'error': f'Bulunamadı: {u}'})


@app.route('/api/search', methods=['POST'])
def api_search():
    """Genel arama (video/kullanici/hashtag).

    Body: { keyword, type=0, count=10, cursor=0 }
    type: 0=video, 1=kullanici, 2=hashtag
    """
    body    = request.json or {}
    keyword = body.get('keyword', '').strip()
    if not keyword:
        return jsonify({'error': 'keyword gerekli'})
    type     = int(body.get('type', 0))
    count    = min(int(body.get('count', 10)), 20)
    cursor   = int(body.get('cursor', 0))
    return jsonify(search(keyword, type=type, count=count, cursor=cursor))


@app.route('/api/search/user', methods=['POST'])
def api_search_user():
    """Kullanici arama (discover/search type=1).

    Body: { keyword, count=10, cursor=0 }
    """
    body    = request.json or {}
    keyword = body.get('keyword', '').strip().lstrip('@')
    if not keyword:
        return jsonify({'error': 'keyword gerekli'})
    count  = min(int(body.get('count', 10)), 20)
    cursor = int(body.get('cursor', 0))
    return jsonify(search(keyword, type="1", count=count, cursor=cursor))


@app.route('/api/search/video', methods=['POST'])
def api_search_video():
    """Video arama (search/item).

    Body: { keyword, count=10, cursor=0, sort_type=0, publish_time=0 }
    """
    body    = request.json or {}
    keyword = body.get('keyword', '').strip()
    if not keyword:
        return jsonify({'error': 'keyword gerekli'})
    count  = min(int(body.get('count', 10)), 20)
    cursor = int(body.get('cursor', 0))
    st     = int(body.get('sort_type', 0))
    pt     = int(body.get('publish_time', 0))
    return jsonify(search_video(keyword, count=count, cursor=cursor, sort_type=st, publish_time=pt))


@app.route('/api/search/music', methods=['POST'])
def api_search_music():
    """Müzik arama (music/search).

    Body: { keyword, count=10, cursor=0, sort_type=0, filter_by=0 }
    """
    body    = request.json or {}
    keyword = body.get('keyword', '').strip()
    if not keyword:
        return jsonify({'error': 'keyword gerekli'})
    count  = min(int(body.get('count', 10)), 20)
    cursor = int(body.get('cursor', 0))
    st     = int(body.get('sort_type', 0))
    fb     = int(body.get('filter_by', 0))
    return jsonify(search_music(keyword, count=count, cursor=cursor, sort_type=st, filter_by=fb))


@app.route('/api/search/live', methods=['POST'])
def api_search_live():
    """Canlı yayın arama (live/search).

    Body: { keyword, count=10, cursor=0 }
    """
    body    = request.json or {}
    keyword = body.get('keyword', '').strip()
    if not keyword:
        return jsonify({'error': 'keyword gerekli'})
    count  = min(int(body.get('count', 10)), 20)
    cursor = int(body.get('cursor', 0))
    return jsonify(search_live(keyword, count=count, cursor=cursor))


@app.route('/api/search/photo', methods=['POST'])
def api_search_photo():
    """Fotoğraf arama (search/photo).

    Body: { keyword, count=10, cursor=0, sort_type=0, publish_time=0 }
    """
    body    = request.json or {}
    keyword = body.get('keyword', '').strip()
    if not keyword:
        return jsonify({'error': 'keyword gerekli'})
    count  = min(int(body.get('count', 10)), 20)
    cursor = int(body.get('cursor', 0))
    st     = int(body.get('sort_type', 0))
    pt     = int(body.get('publish_time', 0))
    return jsonify(search_photo(keyword, count=count, cursor=cursor, sort_type=st, publish_time=pt))


@app.route('/api/device/register', methods=['POST'])
def api_device_register():
    """Yeni cihaz kaydet (device_register API). Her çağrıda yeni device_id + install_id üretir."""
    return jsonify(register_device())


@app.route('/api/search/place', methods=['POST'])
def api_search_place():
    """Yer/mekan arama (search/place).

    Body: { keyword, count=10, cursor=0 }
    """
    body    = request.json or {}
    keyword = body.get('keyword', '').strip()
    if not keyword:
        return jsonify({'error': 'keyword gerekli'})
    count  = min(int(body.get('count', 10)), 20)
    cursor = int(body.get('cursor', 0))
    return jsonify(search_place(keyword, count=count, cursor=cursor))


@app.route('/api/feed/v2', methods=['POST'])
def api_feed_v2():
    """aweme/v2/feed/ — protobuf tabanlı video akışı, full JSON çıktı.

    Body: { feed_type=0, count=6, cursor=0 }
    - feed_type: 0=Sana Özel, 6=Takip Edilen
    - cursor: son yanıttaki "3" (max_cursor) değeri ile sayfala
    """
    body      = request.json or {}
    feed_type = int(body.get('feed_type', 0))
    count     = min(int(body.get('count', 6)), 20)
    cursor    = int(body.get('cursor', 0))
    data = feed_v2(feed_type=feed_type, count=count, cursor=cursor)
    return jsonify(data)





@app.route('/api/feed', methods=['POST'])
def api_feed():
    """Genel video akışını döndür (aweme/v1/feed).

    Body: { cursor=0, count=20 }
    """
    body   = request.json or {}
    cursor = int(body.get('cursor', 0))
    count  = min(int(body.get('count', 20)), 50)
    return jsonify(video_feed(_session, cursor=cursor, count=count))


@app.route('/api/live', methods=['POST'])
def api_live():
    """Belirtilen ülkedeki canlı yayın odalarını döndür (webcast/feed).

    Body: { country='AUTO' }
    """
    if not LIVE_DEPS_OK:
        return jsonify({'error': 'aiohttp kurulu değil — pip install aiohttp'}), 500

    body    = request.json or {}
    country = body.get('country', 'AUTO').upper()

    if country == 'AUTO':
        detected = detect_country_ip()
        country  = detected if detected in COUNTRY_DATA else 'TR'
    if country not in COUNTRY_DATA:
        country = 'TR'

    country_info = COUNTRY_DATA[country]
    cookies = get_webcast_cookies()

    async def _fetch():
        connector = aiohttp.TCPConnector(limit=10)
        async with aiohttp.ClientSession(connector=connector) as session:
            return await fetch_live_rooms(session, cookies, country_info)

    rooms = asyncio.run(_fetch())
    return jsonify({'country': country, 'count': len(rooms), 'rooms': rooms})


# ── ENTRYPOINT ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    get_cookie()
    print('\n  ** TikTok API **  http://127.0.0.1:5000\n')
    app.run(debug=False, host='127.0.0.1', port=5000, threaded=True)
