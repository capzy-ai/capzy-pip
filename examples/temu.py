"""Solve the Temu captcha.

Run with:
    pip install capzy
    python temu.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="TemuCaptchaTaskProxyLess",
    website_url="https://www.temu.com",
)

print("cookies (proxyless):", solution.get("cookies"))


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="TemuCaptchaTask",
    website_url="https://www.temu.com",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("cookies (via proxy):", solution.get("cookies"))
