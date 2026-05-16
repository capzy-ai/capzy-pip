"""Solve GeeTest v3.

gt + challenge are issued by the target site and rotate on each load.
Grab them from the page (or your own fetch) just before solving.

Run with:
    pip install capzy
    python geetest_v3.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="GeeTestV3TaskProxyLess",
    website_url="https://example.com",
    gt="022397c99c9f646f6477822485f30404",
    challenge="b6e7caefb2533fd5b1fb05c1a3aebd6e",
    # geetest_api_server_subdomain="api.geetest.com",   # optional
)

print("challenge (proxyless):", solution["challenge"])
print("validate (proxyless):", solution["validate"])
print("seccode (proxyless):", solution["seccode"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="GeeTestV3Task",
    website_url="https://example.com",
    gt="022397c99c9f646f6477822485f30404",
    challenge="b6e7caefb2533fd5b1fb05c1a3aebd6e",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("validate (via proxy):", solution["validate"])
