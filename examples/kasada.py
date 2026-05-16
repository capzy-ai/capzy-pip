"""Solve a Kasada (KPSDK) challenge.

Returns the x-kpsdk-* headers you should replay on subsequent requests.

Run with:
    pip install capzy
    python kasada.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="KasadaCaptchaTaskProxyLess",
    website_url="https://example.com",
)

print("x-kpsdk-ct (proxyless):", solution.get("x-kpsdk-ct"))
print("x-kpsdk-cd (proxyless):", solution.get("x-kpsdk-cd"))


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="KasadaCaptchaTask",
    website_url="https://example.com",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("x-kpsdk-ct (via proxy):", solution.get("x-kpsdk-ct"))
