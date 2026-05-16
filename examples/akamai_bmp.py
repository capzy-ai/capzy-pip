"""Generate an Akamai Bot Manager (BMP) sensor payload for mobile flows.

The mobile (app) variant — for native iOS/Android clients hitting an
Akamai-protected API.

Run with:
    pip install capzy
    python akamai_bmp.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

solution = capzy.solve(
    type="AntiAkamaiBMPTaskProxyLess",
    package_name="com.example.app",
    version="3.3.5",
    # device_id="...", device_name="iPhone15,2",
)

print("sensor_data (proxyless):", solution["sensor_data"][:80], "...")


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="AntiAkamaiBMPTask",
    package_name="com.example.app",
    version="3.3.5",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("sensor_data (via proxy):", solution["sensor_data"][:80], "...")
