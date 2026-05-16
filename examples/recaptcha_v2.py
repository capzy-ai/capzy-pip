"""Solve reCAPTCHA v2 (checkbox or invisible).

Submit the returned `gRecaptchaResponse` as the `g-recaptcha-response`
form field, or pass it into the widget's JS callback.

Run with:
    pip install capzy
    python recaptcha_v2.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="ReCaptchaV2TaskProxyLess",
    website_url="https://example.com",
    website_key="6Lc_aCMTAAAAAB...",
    is_invisible=False,
)

print("g-recaptcha-response (proxyless):", solution["gRecaptchaResponse"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="ReCaptchaV2Task",
    website_url="https://example.com",
    website_key="6Lc_aCMTAAAAAB...",
    is_invisible=False,
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("g-recaptcha-response (via proxy):", solution["gRecaptchaResponse"])
