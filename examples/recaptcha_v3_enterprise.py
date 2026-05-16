"""Solve reCAPTCHA v3 Enterprise.

Run with:
    pip install capzy
    python recaptcha_v3_enterprise.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="ReCaptchaV3EnterpriseTaskProxyLess",
    website_url="https://example.com",
    website_key="6Lc_aCMTAAAAAB...",
    page_action="checkout",
    min_score=0.7,
    # api_domain="recaptcha.net",   # for .net deployments
)

print("token (proxyless):", solution["gRecaptchaResponse"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="ReCaptchaV3EnterpriseTask",
    website_url="https://example.com",
    website_key="6Lc_aCMTAAAAAB...",
    page_action="checkout",
    min_score=0.7,
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("token (via proxy):", solution["gRecaptchaResponse"])
