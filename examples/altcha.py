"""Solve ALTCHA (pure proof-of-work).

Run with:
    pip install capzy
    python altcha.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="AltchaTaskProxyLess",
    website_url="https://example.com",
    # website_key="...",       # only if the page binds challenges to a key
)

print("payload (proxyless):", solution["payload"])    # paste into `altcha` form field


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="AltchaTask",
    website_url="https://example.com",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("payload (via proxy):", solution["payload"])
