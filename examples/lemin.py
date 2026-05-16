"""Solve Lemin Cropped Captcha.

Run with:
    pip install capzy
    python lemin.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="LeminTaskProxyLess",
    website_url="https://example.com",
    website_key="CROPPED_xxxxxxxxxxxxxxxxxxxx",
)

print("answer (proxyless):      ", solution["answer"])
print("challenge_id (proxyless):", solution["challenge_id"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="LeminTask",
    website_url="https://example.com",
    website_key="CROPPED_xxxxxxxxxxxxxxxxxxxx",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("answer (via proxy):", solution["answer"])
