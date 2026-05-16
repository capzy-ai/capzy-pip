"""Solve Capy Puzzle Captcha.

Run with:
    pip install capzy
    python capy.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="CapyTaskProxyLess",
    website_url="https://example.com",
    website_key="PUZZLE_CapyKey",
)

print("captchakey (proxyless):  ", solution["captchakey"])
print("challengekey (proxyless):", solution["challengekey"])
print("answer (proxyless):      ", solution["answer"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="CapyTask",
    website_url="https://example.com",
    website_key="PUZZLE_CapyKey",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("answer (via proxy):", solution["answer"])
