"""Solve an Imperva Incapsula challenge.

Run with:
    pip install capzy
    python imperva.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="AntiImpervaTaskProxyLess",
    website_url="https://example.com",
    user_agent=UA,
)

print("cookies (proxyless):", solution.get("cookies"))


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="AntiImpervaTask",
    website_url="https://example.com",
    user_agent=UA,
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("cookies (via proxy):", solution.get("cookies"))
