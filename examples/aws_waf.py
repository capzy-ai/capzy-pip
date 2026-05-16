"""Solve a full AWS WAF challenge — returns the aws-waf-token.

Run with:
    pip install capzy
    python aws_waf.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="AntiAwsWafTaskProxyLess",
    website_url="https://example.com",
    # Optional context — if you've already scraped these from the
    # challenge page, including them speeds the solve up:
    # aws_key="...", aws_iv="...", aws_context="...",
)

print("aws-waf-token (proxyless):", solution["token"])


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="AntiAwsWafTask",
    website_url="https://example.com",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("aws-waf-token (via proxy):", solution["token"])
