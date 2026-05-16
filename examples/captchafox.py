"""Solve CaptchaFox and print the token.

Submit the returned `token` to the target's verification endpoint
(usually as `cf-captcha-response` or via the widget's JS callback).

Run with:
    pip install capzy
    python captchafox.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="CaptchaFoxTaskProxyLess",
    website_url="https://example.com",
    website_key="sk_xxxxxxxxxxxxxxxxxxxxxxxx",
)

print("token (proxyless):", solution["token"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="CaptchaFoxTask",
    website_url="https://example.com",
    website_key="sk_xxxxxxxxxxxxxxxxxxxxxxxx",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("token (via proxy):", solution["token"])
