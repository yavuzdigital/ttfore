# TikTok API - Sunucu Kurulumu

## Gereksinimler
- Python 3.10+
- Ubuntu/Debian (önerilen)

## 1. Bağımlılıklar

```bash
apt update && apt install -y python3 python3-pip
pip3 install -r requirements.txt --break-system-packages
```

## 2. Proje Dosyaları

Projeyi sunucuya yükle (örn: `/var/www/tapi/`). Gerekli dosyalar:

- `web.py`
- `tiktok/` (klasör)
- `lib/` (klasör)
- `templates/` (klasör)
- `data/` (klasör - devices.txt, models.txt)
- `www.tiktok.com_cookies.txt`
- `requirements.txt`

## 3. Cookie

`www.tiktok.com_cookies.txt` içinde geçerli `sessionid` olmalı.

## 4. API Key (Opsiyonel)

`web.py` içinde `API_KEY` değişkenine bir anahtar belirle:

```python
API_KEY = "gizli-anahtar-buraya"
```

Dışarıdan çağırırken header'a ekle: `X-API-Key: gizli-anahtar-buraya`

## 5. Systemd Servisi

```bash
nano /etc/systemd/system/tiktok-api.service
```

```ini
[Unit]
Description=TikTok API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/tapi
Environment=PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ExecStart=/usr/bin/python3 /var/www/tapi/web.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable tiktok-api
systemctl start tiktok-api
```

## 6. Test

```bash
# Cookie
curl http://127.0.0.1:3131/api/cookie

# API Key'li istek
curl http://127.0.0.1:3131/api/search/user \
  -H "Content-Type: application/json" \
  -H "X-API-Key: gizli-anahtar-buraya" \
  -d '{"keyword":"hadise","count":3}'
```

## 7. Endpoint'ler

| Endpoint | Açıklama |
|----------|----------|
| `GET /api/cookie` | Cookie durumu |
| `GET /api/countries` | Ülke listesi |
| `POST /api/resolve` | Username → UID |
| `POST /api/search` | Genel arama (type=0 video, 1 kullanıcı, 2 hashtag) |
| `POST /api/search/user` | Kullanıcı arama |
| `POST /api/search/video` | Video arama |
| `POST /api/search/music` | Müzik arama |
| `POST /api/search/live` | Canlı yayın arama |
| `POST /api/search/photo` | Fotoğraf arama |
| `POST /api/search/place` | Mekan arama |
| `POST /api/feed` | Video akışı (v1) |
| `POST /api/feed/v2` | Video akışı (v2, protobuf) |
| `POST /api/live` | Canlı yayın odaları |

## 8. PHP Kullanımı

```php
function tikTokAra($keyword) {
    $ch = curl_init('http://127.0.0.1:3131/api/search/user');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'X-API-Key: gizli-anahtar-buraya'
        ],
        CURLOPT_POSTFIELDS => json_encode(['keyword' => $keyword, 'count' => 10]),
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 15,
    ]);
    $res = curl_exec($ch);
    curl_close($ch);
    return json_decode($res, true);
}
```

## 9. Port

Varsayılan port: **3131** (`web.py` içinden değiştirebilirsin)

```python
app.run(debug=False, host='0.0.0.0', port=3131, threaded=True)
```

Güvenlik duvarı:
```bash
ufw allow 3131
```
