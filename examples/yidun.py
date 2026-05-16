"""Solve a NetEase Yidun slider captcha.

Run with:
    pip install capzy
    python yidun.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="YidunSliderTaskProxyLess",
    website_url="https://example.com",
    captcha_id="9a371b56b9474958b59569f47df03555",
)

print("validate (proxyless):", solution["validate"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="YidunSliderTask",
    website_url="https://example.com",
    captcha_id="9a371b56b9474958b59569f47df03555",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("validate (via proxy):", solution["validate"])
