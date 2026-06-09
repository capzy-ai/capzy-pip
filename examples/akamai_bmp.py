"""Mint Akamai BMP (Mobile) sensors — X-acf-sensor-data for native
mobile apps protected by Akamai Bot Manager Premier (BMP).

This is the MOBILE variant — the native iOS / Android SDK that emits
the `X-acf-sensor-data` HTTP header on every request from a protected
mobile app. Sub-second per sensor, pure-API, no browser.

For the DESKTOP / Web variant (`_abck` cookie via the bmak JS bundle),
see akamai_web.py — different task type, different shape, different price.

Capzy's BMP shape matches CapSolver's AntiAkamaiBMPTask contract
verbatim — if you already integrate with CapSolver for Akamai BMP, you
can point at Capzy with zero code changes.

Run with:
    pip install capzy
    python akamai_bmp.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Mint a single sensor ─────────────────────────────────────────────

solution = capzy.solve(
    type="AntiAkamaiBMPTaskProxyLess",
    package_name="com.ihg.apps.android",   # the protected app's bundle ID
    version="3.3.4",                        # Akamai BMP SDK version baked into the app
    platform="android",                     # iOS not yet supported
    pow_url="https://m.ihg.com",            # URL the app POSTs to (optional)
)

# Response shape (CapSolver-canonical):
#   sensors[]  — array of base64 strings, one per requested `count`
#   useragent  — Dalvik UA matching the device fingerprint
#   deviceId   — stable device identifier
#   version    — echo of the BMP SDK version
print("sensors[0]:", solution["sensors"][0][:80], "...")
print("useragent:", solution["useragent"])
print("deviceId:", solution["deviceId"])


# ── 2. Mint multiple sensors in one task (saves round-trips) ────────────
# Real mobile apps often need several sequential sensor posts per
# session. Pass count=N to get N sensors in one task instead of N
# separate tasks. Each sensor uses a different randomly-picked device
# fingerprint.

bulk = capzy.solve(
    type="AntiAkamaiBMPTaskProxyLess",
    package_name="com.starbucks.mobilecard",
    version="4.2.1",
    count=5,
)
print(f"got {len(bulk['sensors'])} sensors in one task")


# ── 3. Use a sensor on your own HTTP client ─────────────────────────────
# Akamai validates that the User-Agent matches the device fingerprint
# embedded in the sensor. ALWAYS send the returned useragent on the
# same request as the sensor — pasting in your own UA will fail.

import requests  # noqa: E402

resp = requests.post(
    "https://api.example.com/v1/orders",
    headers={
        "X-acf-sensor-data": solution["sensors"][0],
        "User-Agent": solution["useragent"],
        "Content-Type": "application/json",
    },
    json={"item": "..."},
)
print("akamai-protected request status:", resp.status_code)
