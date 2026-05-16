"""Solve Friendly Captcha (a proof-of-work captcha).

Run with:
    pip install capzy
    python friendly_captcha.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="FriendlyCaptchaTaskProxyLess",
    website_url="https://example.com",
    website_key="FCMST6...",    # data-sitekey on the widget
)

print("solution (proxyless):", solution["token"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="FriendlyCaptchaTask",
    website_url="https://example.com",
    website_key="FCMST6...",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("solution (via proxy):", solution["token"])
