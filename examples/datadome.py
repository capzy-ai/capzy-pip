"""Solve a DataDome slider challenge.

A proxy is required. Use the same proxy + user-agent on the replay
request — DataDome cookies are bound to the egress IP + UA fingerprint.

Run with:
    pip install capzy
    python datadome.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")

solution = capzy.solve(
    type="DataDomeSliderTask",
    website_url="https://example.com",
    captcha_url="https://geo.captcha-delivery.com/captcha/?initialCid=...",
    user_agent=(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    proxy_type="http",          # http | https | socks4 | socks5
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("cookie:", solution["cookie"])   # set this as `datadome` on subsequent requests
