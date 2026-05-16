"""Solve a Cloudflare JS challenge page (the interstitial, not Turnstile).

Returns the cookies + user-agent you should replay on subsequent
requests. A proxy is required — the challenge token is bound to the
egress IP, so the IP you solve from must match the IP you use after.

Run with:
    pip install capzy
    python cloudflare_challenge.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")

solution = capzy.solve(
    type="AntiCloudflareTask",
    website_url="https://example.com",
    proxy_type="http",          # http | https | socks4 | socks5
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",         # optional
    proxy_password="pass",      # optional
)

print("cookies:   ", solution.get("cookies"))
print("user-agent:", solution.get("userAgent"))
