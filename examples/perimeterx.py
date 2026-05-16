"""Solve a PerimeterX (Human Security) challenge.

Run with:
    pip install capzy
    python perimeterx.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="AntiPerimeterXTaskProxyLess",
    website_url="https://example.com",
    # website_key="PX...",     # if the site sets a public app id
)

print("cookies (proxyless):", solution.get("cookies"))


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="AntiPerimeterXTask",
    website_url="https://example.com",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("cookies (via proxy):", solution.get("cookies"))
