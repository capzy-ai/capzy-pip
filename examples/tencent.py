"""Solve Tencent Captcha.

Run with:
    pip install capzy
    python tencent.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="TencentTaskProxyLess",
    website_url="https://example.com",
    app_id="2003319081",        # aid from the captcha widget
)

print("ticket (proxyless): ", solution["ticket"])
print("randstr (proxyless):", solution["randstr"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="TencentTask",
    website_url="https://example.com",
    app_id="2003319081",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("ticket (via proxy):", solution["ticket"])
