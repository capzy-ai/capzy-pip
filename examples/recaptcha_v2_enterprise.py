"""Solve reCAPTCHA v2 Enterprise.

Run with:
    pip install capzy
    python recaptcha_v2_enterprise.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="ReCaptchaV2EnterpriseTaskProxyLess",
    website_url="https://example.com",
    website_key="6Lc_aCMTAAAAAB...",
    # enterprise_payload={"s": "..."},   # if the page passes one
    # api_domain="recaptcha.net",        # for .net deployments
)

print("g-recaptcha-response (proxyless):", solution["gRecaptchaResponse"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="ReCaptchaV2EnterpriseTask",
    website_url="https://example.com",
    website_key="6Lc_aCMTAAAAAB...",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("g-recaptcha-response (via proxy):", solution["gRecaptchaResponse"])
