# TikTok API - Sunucu Kurulumu

## Gereksinimler

- Python 3.10+
- Nginx
- (Opsiyonel) systemd veya supervisord

## 1. Python & Bagimliliklar

```bash
# Debian/Ubuntu
apt update && apt install -y python3 python3-pip python3-venv nginx

# Proje dizini
mkdir -p /var/www/tiktok-api
cd /var/www/tiktok-api

# Virtualenv (önerilen)
python3 -m venv venv
source venv/bin/activate

# Bagimliliklari yukle
pip install -r requirements.txt
```

## 2. Proje Dosyalari

```bash
# Projeyi kopyala (/var/www/tiktok-api/ altina)
# Gerekli dosyalar:
#   - web.py
#   - tiktok/ (klasör)
#   - lib/ (klasör)
#   - templates/ (klasör)
#   - www.tiktok.com_cookies.txt
#   - data/devices.txt
#   - data/models.txt
#   - requirements.txt
```

## 3. Cookie Dosyasi

`www.tiktok.com_cookies.txt` dosyasina gecerli TikTok session cookie'si eklenmeli:

```
.tiktok.com	TRUE	/	TRUE	1785540564	sessionid	<session_id_buraya>
```

Cookie alm icin tarayicida `www.tiktok.com`'a girip F12 → Application → Cookies → sessionid degerini kopyala.

## 4. Systemd Servisi

```ini
# /etc/systemd/system/tiktok-api.service
[Unit]
Description=TikTok API Flask
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/tiktok-api
Environment=PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ExecStart=/var/www/tiktok-api/venv/bin/python /var/www/tiktok-api/web.py
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

## 5. Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/tiktok-api
server {
    listen 80;
    server_name api.ornek.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 30s;
    }
}
```

```bash
ln -s /etc/nginx/sites-available/tiktok-api /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

## 6. SSL (HTTPS) - Certbot ile

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d api.ornek.com
```

## 7. Test

```bash
curl http://127.0.0.1:5000/api/cookie
# {"ok":true}

curl -X POST http://127.0.0.1:5000/api/search/user \
  -H "Content-Type: application/json" \
  -d '{"keyword":"hadise","count":3}'
```

## 8. Sorun Giderme

| Sorun | Cozum |
|-------|-------|
| `{"ok":false}` | Cookie gecersiz. Yenile. |
| Flask 500 hatasi | `journalctl -u tiktok-api -f` ile log kontrol |
| Nginx 502 Bad Gateway | Flask servisi calisiyor mu? `systemctl status tiktok-api` |
| `SC` hatasi | X-Gorgon/X-Argus gecersiz. Cookie + device ID'leri guncelle. |

## Dosya Yapisi

```
/var/www/tiktok-api/
├── web.py
├── tiktok/
│   ├── __init__.py
│   ├── auth.py
│   ├── client.py
│   ├── config.py
│   ├── mobile.py
│   └── webcast.py
├── lib/
│   ├── __init__.py
│   ├── XArgus.py
│   ├── XGorgon.py
│   ├── XLadon.py
│   ├── sign.py
│   ├── protobuf.py
│   ├── Sm3.py
│   ├── Simon.py
│   ├── pkcs7_padding.py
│   ├── utils.py
│   ├── ByteBuf.py
│   ├── aweme_v2_pb2.py
│   └── ...
├── templates/
│   └── index.html
├── app/
├── data/
│   ├── devices.txt
│   └── models.txt
├── www.tiktok.com_cookies.txt
├── requirements.txt
└── KURULUM.md
```
