# Proxies

You generally **don't need to send a proxy** — every `*ProxyLess` task
type runs against our own upstream network. We charge the same price
either way.

You **do** need to supply one when the target site binds the token /
cookie to the egress IP. Anti-bot platforms (DataDome, PerimeterX,
Imperva, Akamai BMP) do this by design.

## Supported types

| `proxy_type` | Notes |
|---|---|
| `http` | Most common. |
| `https` | TLS to the proxy itself. |
| `socks4` | |
| `socks5` | |

## Format

Switch the task `type` from the `…TaskProxyLess` variant to the plain
`…Task` variant and add the `proxy_*` fields:

```python
from capzy import CapzyClient

capzy = CapzyClient("capzy_xxx")
capzy.solve(
    type="AntiTurnstileTask",        # was "AntiTurnstileTaskProxyLess"
    website_url="https://example.com",
    website_key="0x4AAA...",
    proxy_type="http",
    proxy_address="123.45.67.89",    # IPv4, IPv6, or hostname
    proxy_port=8080,
    proxy_login="user",              # optional
    proxy_password="pass",           # optional
)
```

## Which task types require a proxy?

| Task | Proxy required? |
|---|---|
| `AntiCloudflareTask` (full JS challenge) | Yes |
| `DataDomeSliderTask` | Yes |
| `AntiPerimeterXTask` | Strongly recommended |
| `AntiImpervaTask` | Strongly recommended |
| `AntiAkamaiBMPTask` | Strongly recommended |
| Everything else | No |

## Picking a proxy

Whatever proxy you pass on `createTask` must be the **same** proxy you
then use to replay the resulting cookie / header on the target site. The
fingerprint is bound to the IP — using a different exit IP afterwards
will reset you.

For DataDome / PerimeterX / Imperva, also keep the same `user-agent`
across the solve and the replay request.

## Configuring the SDK to fetch through a proxy too

If you want the SDK's own HTTP calls to `api.capzy.ai` to go through a
proxy (corporate egress, etc.), inject a configured `requests.Session`:

```python
import requests
from capzy import CapzyClient

session = requests.Session()
session.proxies = {
    "http":  "http://user:pass@proxy.example:8080",
    "https": "http://user:pass@proxy.example:8080",
}

client = CapzyClient("capzy_xxx", session=session)
```

This is independent of any proxy you might pass *inside* a task body —
the session proxy only routes traffic to Capzy itself.

---

Next: [FAQ →](./faq.md)
