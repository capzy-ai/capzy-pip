"""Solve Cloudflare Turnstile and print the token.

Drop the returned `token` into the `cf-turnstile-response` form field
on the target page (or into the JS `data-callback`).

Run with:
    pip install capzy
    python cloudflare_turnstile.py
"""

from capzy import CapzyClient

# Grab your key at https://capzy.ai/dashboard
# New accounts get $0.10 in free credits — ~83 Turnstile solves.
capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="AntiTurnstileTaskProxyLess",
    website_url="https://example.com/login",
    website_key="0x4AAAAAAA000000000000000000",
    # action="login",     # optional — must match the page's data-action
    # cdata="user-123",   # optional — server-issued cdata
)

print("token (proxyless):", solution["token"])


# ── 2. Through your own proxy ────────────────────────────────────────────
#
# Switch the `type` to the non-ProxyLess variant and add the proxy_* fields.
# Use the same proxy IP for the solve AND for the request that replays the
# token afterwards — Turnstile tokens issued against one IP are still valid
# on others, but some integrations bind them, so keep IPs consistent.

solution = capzy.solve(
    type="AntiTurnstileTask",
    website_url="https://example.com/login",
    website_key="0x4AAAAAAA000000000000000000",
    proxy_type="http",          # http | https | socks4 | socks5
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",         # optional
    proxy_password="pass",      # optional
)

print("token (via proxy):", solution["token"])
