"""Solve MTCaptcha.

Run with:
    pip install capzy
    python mtcaptcha.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="MtCaptchaTaskProxyLess",
    website_url="https://example.com",
    website_key="MTPublic-...",
)

print("token (proxyless):", solution["token"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="MtCaptchaTask",
    website_url="https://example.com",
    website_key="MTPublic-...",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("token (via proxy):", solution["token"])
