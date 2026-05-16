"""Solve a Shopee curve-slider captcha (the rotated S-shaped track).

Run with:
    pip install capzy
    python shopee_curve.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="ShopeeCurveTaskProxyLess",
    website_url="https://shopee.com/buyer/login",
)

print("cookies (proxyless):", solution.get("cookies"))


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="ShopeeCurveTask",
    website_url="https://shopee.com/buyer/login",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("cookies (via proxy):", solution.get("cookies"))
