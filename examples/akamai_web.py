"""Solve Akamai Bot Manager (Web / desktop variant) and get validated
cookies for replay.

Akamai's web variant guards desktop browsers via an obfuscated `bmak`
JS bundle that POSTs `sensor_data` and validates the session by setting
the `_abck` cookie (must contain `~0~`). Capzy drives a real browser
through the challenge and returns the cookies + matching User-Agent.

The cookies are IP-bound: Akamai correlates every replay against the IP
that earned the cookie. The `ProxyLess` variant uses Capzy's upstream IP
(useful when Capzy will replay on your behalf); the regular variant pins
the solve to a proxy you control so you can replay the cookies yourself.

For the MOBILE BMP variant (X-acf-sensor-data header from native iOS/
Android apps), see akamai_bmp.py — different task type, different shape.

Run with:
    pip install capzy
    python akamai_web.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (Capzy handles the upstream IP) ────────────────────────

solution = capzy.solve(
    type="AntiAkamaiWebTaskProxyLess",
    website_url="https://example.com/protected-path",
)

print("cookies:", [c["name"] for c in solution["cookies"]])
print("user-agent:", solution["userAgent"])


# ── 2. Through your own proxy (cookies bound to YOUR IP) ────────────────

solution = capzy.solve(
    type="AntiAkamaiWebTask",
    website_url="https://example.com/protected-path",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

# Replay: set every cookie on your HTTP client, reuse the userAgent
# verbatim, and route the request through the same proxy. Default
# requests/httpx TLS will be rejected by Akamai's Phase-1 check —
# use curl_cffi with Chrome impersonation, tls-client, or a real
# browser context for the replay.
import requests  # noqa: E402

session = requests.Session()
for c in solution["cookies"]:
    session.cookies.set(c["name"], c["value"], domain=c["domain"], path=c["path"])
session.headers["User-Agent"] = solution["userAgent"]

# resp = session.get("https://example.com/protected", proxies={...})
