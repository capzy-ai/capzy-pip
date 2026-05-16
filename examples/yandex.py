"""Solve Yandex SmartCaptcha.

Run with:
    pip install capzy
    python yandex.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="YandexSmartCaptchaTaskProxyLess",
    website_url="https://example.com",
    website_key="ysc1_xxxxxxxxxxxxxxxxxxxxxxxx",
)

print("token (proxyless):", solution["token"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="YandexSmartCaptchaTask",
    website_url="https://example.com",
    website_key="ysc1_xxxxxxxxxxxxxxxxxxxxxxxx",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("token (via proxy):", solution["token"])
