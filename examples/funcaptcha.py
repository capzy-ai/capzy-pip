"""Solve FunCaptcha (Arkose Labs).

Run with:
    pip install capzy
    python funcaptcha.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="FunCaptchaTaskProxyLess",
    website_url="https://example.com",
    website_public_key="476068BF-9607-4799-B53D-966BE98E2B81",
    # funcaptcha_api_js_subdomain="client-api.arkoselabs.com",
    # data='{"blob": "..."}',
)

print("token (proxyless):", solution["token"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="FunCaptchaTask",
    website_url="https://example.com",
    website_public_key="476068BF-9607-4799-B53D-966BE98E2B81",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("token (via proxy):", solution["token"])
