"""Solve GeeTest v4 — the captchaId-based version.

Run with:
    pip install capzy
    python geetest_v4.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="GeeTestV4TaskProxyLess",
    website_url="https://example.com",
    captcha_id="b6e7caefb2533fd5b1fb05c1a3aebd6e",
)

print("captcha_id:    ", solution["captcha_id"])
print("lot_number:    ", solution["lot_number"])
print("pass_token:    ", solution["pass_token"])
print("gen_time:      ", solution["gen_time"])
print("captcha_output:", solution["captcha_output"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="GeeTestV4Task",
    website_url="https://example.com",
    captcha_id="b6e7caefb2533fd5b1fb05c1a3aebd6e",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("captcha_output (via proxy):", solution["captcha_output"])
