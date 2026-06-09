<div align="center">

<img src="https://capzy.ai/capzy-logo.svg" alt="Capzy" width="220" />

# `capzy` — official Python SDK

**Solve every major captcha with a single line of Python.**

[![PyPI version](https://img.shields.io/pypi/v/capzy.svg?color=%23ff5d2a)](https://pypi.org/project/capzy/)
[![Python](https://img.shields.io/pypi/pyversions/capzy.svg?color=%23ff5d2a)](https://pypi.org/project/capzy/)
[![License: MIT](https://img.shields.io/badge/license-MIT-%23ff5d2a.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-capzy.ai-%23ff5d2a)](https://capzy.ai/docs)
[![Status](https://img.shields.io/badge/uptime-99.9%25-%2322c55e)](https://capzy.ai)

[Website](https://capzy.ai) · [Dashboard](https://capzy.ai/dashboard) · [Docs](https://capzy.ai/docs) · [Pricing](https://capzy.ai/pricing) · [Get free credits](https://capzy.ai/auth/register)

</div>

---

## Why Capzy

> Built by people who were tired of paying half a cent to get back `errorCode: ERROR_NO_AVAILABLE_WORKERS`.

- ⚡️ **Fast.** Median solve <5s for Turnstile / reCAPTCHA v2 / GeeTest.
- 💸 **Cheap.** Token-bound captchas start at **$0.40 per 1,000 solves**.
- 🧠 **Solves what others don't.** Native support for **Temu**, **Shopee** (slider + curve), **Binance bCAPTCHA2**, **CaptchaFox**, **MTCaptcha**, **Lemin**, **ALTCHA**, **Yidun**, **Capy** — not just the obvious ones.
- 🧩 **Drop-in compatible.** Uses the same `createTask` / `getTaskResult` shape your existing scripts already speak. Migration is a one-line `base_url` change.
- 🆓 **Free credits on sign-up.** Every new account gets **$0.10** in real credits to test in production. No card required.
- 🔓 **No retainer, no minimum.** Pay-as-you-go. Top up when you want.
- 📊 **Real dashboard.** Per-key analytics, score quality charts for v3, full payment audit log.

> [**Create a free account →**](https://capzy.ai/auth/register)
> Get **$0.10 in free credits** the moment you sign up — enough to verify integration end-to-end on roughly **80 reCAPTCHA v3** or **80 Turnstile** solves before you pay a cent.

---

## Install

```bash
pip install capzy
```

Requires Python ≥ 3.9 and `requests`. That's it.

Bleeding-edge (straight from `main`):

```bash
pip install "git+https://github.com/capzy-ai/capzy-pip.git"
```

---

## 60-second quickstart

```python
from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")   # from capzy.ai/dashboard

solution = capzy.solve(
    type="AntiTurnstileTaskProxyLess",
    website_url="https://example.com/login",
    website_key="0x4AAAAAAA...",
)
print(solution["token"])     # paste into the cf-turnstile-response field
```

That's the whole pattern. `solve()` does `createTask` → polls `getTaskResult` → hands you the solution dict.

Need to route the solve through your own proxy? Switch to the `…Task` (non-`ProxyLess`) type and add the proxy params:

```python
solution = capzy.solve(
    type="AntiTurnstileTask",
    website_url="https://example.com/login",
    website_key="0x4AAAAAAA...",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)
```

Need lower-level control? Use the raw verbs:

```python
created = capzy.create_task(
    type="AntiTurnstileTaskProxyLess",
    website_url="https://example.com/login",
    website_key="0x4AAAAAAA...",
)
task_id = created["taskId"]

# Poll on your own schedule:
status = capzy.get_task_result(task_id)
```

> **Param naming.** Pass either `website_url=` / `website_key=` (Python style) or
> `websiteURL=` / `websiteKey=` (wire style). They're equivalent — the SDK
> normalises snake_case to the camelCase the API expects.

---

## How it works

```
┌──────────────┐  createTask   ┌──────────┐    enqueue    ┌──────────┐
│ your script  │ ────────────▶ │  Capzy   │ ────────────▶ │ solver   │
│  (capzy SDK) │ ◀──────────── │   API    │ ◀──────────── │  cluster │
└──────────────┘ getTaskResult └──────────┘   solution    └──────────┘
                          (polls until "ready")
```

Submit → poll → done. No webhooks to set up, no SDK runtime required on the solver side, no captive browser to manage.

---

## Supported captchas

Every captcha below is supported as a **proxyless** task (we handle the upstream routing) and a **proxy** task (you supply the upstream IP). All prices are USD per solve.

### Token-based — the workhorses

| Captcha | Task type | Price | Notes |
|---|---|---|---|
| Cloudflare Turnstile | `AntiTurnstileTaskProxyLess` | **$0.0012** | Including invisible variant |
| Cloudflare Challenge | `AntiCloudflareTask` | $0.005 | Full JS-challenge page |
| reCAPTCHA v2 | `ReCaptchaV2TaskProxyLess` | **$0.002** | Checkbox + invisible |
| reCAPTCHA v2 Enterprise | `ReCaptchaV2EnterpriseTaskProxyLess` | $0.004 | |
| reCAPTCHA v3 | `ReCaptchaV3TaskProxyLess` | **$0.0015** | Action + min-score |
| reCAPTCHA v3 Enterprise | `ReCaptchaV3EnterpriseTaskProxyLess` | $0.005 | |
| FunCaptcha (Arkose) | `FunCaptchaTaskProxyLess` | $0.004 | Including Roblox flow |
| GeeTest v4 | `GeeTestTaskProxyLess` | **$0.003** | captchaId-based |
| GeeTest v3 | `GeeTestV3TaskProxyLess` | $0.0035 | gt + challenge |
| CaptchaFox | `CaptchaFoxTaskProxyLess` | **$0.0012** | |
| MTCaptcha | `MtCaptchaTaskProxyLess` | $0.002 | |
| Friendly Captcha | `FriendlyCaptchaTaskProxyLess` | $0.002 | |
| ALTCHA | `AltchaTaskProxyLess` | $0.001 | Pure proof-of-work |
| Lemin | `LeminTaskProxyLess` | $0.0015 | |
| Capy Puzzle | `CapyTaskProxyLess` | $0.002 | |
| NetEase Yidun | `YidunSliderTaskProxyLess` | $0.003 | |
| Yandex SmartCaptcha | `YandexSmartCaptchaTaskProxyLess` | $0.025 | |
| Binance bCAPTCHA2 | `BinanceCaptchaTask` | $0.003 | |
| Tencent | `TencentTaskProxyLess` | $0.002 | |
| Shopee Slider | `ShopeeSliderTaskProxyLess` | $0.002 | |
| Shopee Curve Slider | `ShopeeCurveTaskProxyLess` | $0.003 | |
| Temu | `TemuCaptchaTaskProxyLess` | $0.002 | |
| Alibaba | `AntiAlibabaCaptchaTaskProxyLess` | $0.003 | |

### Anti-bot platforms

| Platform | Task type | Price | Notes |
|---|---|---|---|
| AWS WAF (full challenge) | `AntiAwsWafTaskProxyLess` | $0.012 | |
| AWS WAF (image classify) | `AwsWafClassification` | **$0.0008** | Just the image piece |
| DataDome Slider | `DataDomeSliderTask` | $0.04 | Proxy required |
| PerimeterX | `AntiPerimeterXTask` | $0.04 | Proxy required (IP-bound) |
| Imperva Incapsula | `AntiImpervaTaskProxyLess` | $0.04 | |
| Akamai Bot Manager | `AntiAkamaiBMPTaskProxyLess` | $0.05 | Mobile (BMP) |
| Kasada | `KasadaCaptchaTaskProxyLess` | $0.005 | |

### Image-based

| Type | Task type | Price | Use case |
|---|---|---|---|
| Image-to-Text | `ImageToTextTask` | **$0.001** | Generic OCR captchas |
| Math Captcha | `MathCaptchaTask` | $0.001 | "What is 7 + 3?" |
| Coordinates Click | `CoordinatesTask` | $0.001 | "Click the cat" |
| Rotate | `RotateTask` | $0.001 | Rotate-to-upright |

Full live pricing at **[capzy.ai/pricing](https://capzy.ai/pricing)** — these tables are scraped from the same source-of-truth.

---

## Examples per service

### Cloudflare Turnstile

```python
from capzy import CapzyClient

capzy = CapzyClient("capzy_xxx")
sol = capzy.solve(
    type="AntiTurnstileTaskProxyLess",
    website_url="https://example.com",
    website_key="0x4AAAAAAA...",
    action="login",      # optional — must match data-action
    cdata="user-123",    # optional — server-issued cdata
)
print(sol["token"])
```

### reCAPTCHA v2

```python
from capzy import CapzyClient

capzy = CapzyClient("capzy_xxx")
sol = capzy.solve(
    type="ReCaptchaV2TaskProxyLess",
    website_url="https://example.com",
    website_key="6Lc_aCMTAAAAAB...",
    is_invisible=False,
)
print(sol["gRecaptchaResponse"])
```

### reCAPTCHA v3 (score-based)

```python
from capzy import CapzyClient

capzy = CapzyClient("capzy_xxx")
created = capzy.create_task(
    type="ReCaptchaV3TaskProxyLess",
    website_url="https://example.com",
    website_key="6Lc_aCMTAAAAAB...",
    page_action="checkout",
    min_score=0.7,
)
task_id = created["taskId"]

# After you call Google siteverify with your secret, report the score back —
# it lights up your v3 quality dashboard and helps us auto-route your traffic.
capzy.report_score(task_id, score=0.9, action="checkout", hostname="example.com")
```

### GeeTest v4

```python
from capzy import CapzyClient

capzy = CapzyClient("capzy_xxx")
sol = capzy.solve(
    type="GeeTestV4TaskProxyLess",
    website_url="https://example.com",
    captcha_id="abc123...",
)
# sol contains captcha_id, lot_number, pass_token, gen_time, captcha_output
```

### Image-to-Text (sync solve — no polling)

```python
import base64
from capzy import CapzyClient

capzy = CapzyClient("capzy_xxx")
with open("captcha.png", "rb") as f:
    body = base64.b64encode(f.read()).decode()

sol = capzy.solve(type="ImageToTextTask", body=body, case="lower")
print(sol["text"])
```

More copy-pasteable runners in [`examples/`](./examples).

---

## Free credits & getting an API key

1. Create an account at **[capzy.ai/auth/register](https://capzy.ai/auth/register)**.
2. We post a **$0.10 welcome bonus** as a real credit transaction on your dashboard. (Audit it like any other payment.)
3. Generate an API key on **[capzy.ai/dashboard](https://capzy.ai/dashboard)** and drop it into `CapzyClient("capzy_…")`.

The $0.10 is plenty to verify end-to-end:

| Captcha | Solves you can run on $0.10 |
|---|---|
| reCAPTCHA v3 | ~66 |
| Turnstile | ~83 |
| reCAPTCHA v2 | ~50 |
| Image-to-Text | ~100 |
| GeeTest v4 | ~33 |

When you run out, top up with **Stripe** (card / Apple Pay / Google Pay) or **MixPay** (USDT / BTC / 30+ coins). No subscription, no minimum.

---

## Handling errors

```python
from capzy import CapzyClient, ApiError, TaskFailedError, TaskTimeoutError

capzy = CapzyClient("capzy_xxx")
try:
    sol = capzy.solve(
        type="AntiTurnstileTaskProxyLess",
        website_url="https://example.com",
        website_key="0x4AAAAAAA...",
    )
except ApiError as e:
    # createTask was rejected — bad key, wrong task type, insufficient funds, etc.
    print("API rejected the task:", e.error_code, e.error_description)
    if e.recommended_task_type:
        print("Hint — submit as:", e.recommended_task_type)
except TaskFailedError as e:
    # Task ran but couldn't be solved. Refunded automatically.
    print("Solver failed:", e.error_code, e.error_description)
except TaskTimeoutError as e:
    # We didn't get an answer within max_wait. Refunded automatically.
    print(f"No answer after {e.waited:.0f}s")
```

**You are never charged for failed or timed-out tasks.** Refunds post as real credit transactions, visible in your dashboard.

---

## Configuration

```python
capzy = CapzyClient(
    api_key="capzy_xxx",
    base_url="https://api.capzy.ai",   # override for on-prem / staging
    timeout=30.0,                       # per HTTP-request timeout
)

# Tune the polling behaviour per .solve() call:
capzy.solve(type="AntiTurnstileTaskProxyLess", website_url=..., website_key=...,
            poll_interval=1.0, max_wait=90.0)
```

Need a proxy on the SDK's own egress, retries, or custom TLS? Pass your own `requests.Session`:

```python
import requests
from capzy import CapzyClient

session = requests.Session()
session.proxies = {"https": "http://user:pass@proxy.example:8080"}
capzy = CapzyClient("capzy_xxx", session=session)
```

---

## API reference

`CapzyClient` is a thin wrapper around the Capzy HTTP API:

| Method | Endpoint | Returns |
|---|---|---|
| `capzy.solve(type=..., **params)` | `POST /createTask` + polls `POST /getTaskResult` | the `solution` dict |
| `capzy.create_task(type=..., **params)` | `POST /createTask` | `{taskId, status?, solution?, timeout?}` |
| `capzy.get_task_result(task_id)` | `POST /getTaskResult` | `{status, solution?, cost?, ip?, …}` |
| `capzy.report_score(task_id, score, action=None, hostname=None)` | `POST /reportScore` | `None` |
| `capzy.get_balance()` | `POST /getBalance` | `float` USD |

All task parameters travel as kwargs. Snake_case (`website_url`, `proxy_address`, `min_score`) and camelCase (`websiteURL`, `proxyAddress`, `minScore`) are equivalent — the SDK normalises to the wire format.

---

## FAQ

**Do you need to supply a proxy?**
No — every `*ProxyLess` task type runs against our own network. Bring your own only when the target binds the token to your egress IP (some anti-bot platforms do).

**Do you support async?**
Not in v0.0.1. The sync client is intentionally tiny — pair it with a thread pool, `anyio.to_thread`, or `asyncio.to_thread` if you need fan-out today. A native `AsyncCapzyClient` is on the roadmap.

**What happens if a task fails?**
The credit is automatically refunded as a `refund` transaction. The SDK raises `TaskFailedError` so you can retry with a different task type or proxy.

**Can I run this in a long-running service?**
Yes. Re-use one `CapzyClient` across threads — the underlying `requests.Session` is thread-safe for our usage pattern.

**Where do I find my API key?**
[capzy.ai/dashboard](https://capzy.ai/dashboard) → API keys → New key.

**Do you have rate limits?**
Per-key concurrency limits exist (visible on your dashboard). When you hit them, `createTask` returns `ERROR_RATE_LIMIT` and the SDK raises `ApiError(error_code="ERROR_RATE_LIMIT")` so you can back off.

**Where do solutions need to be submitted?**
- Turnstile → `cf-turnstile-response` form field
- reCAPTCHA v2 / Enterprise → `g-recaptcha-response`
- Others → service-specific; see the per-service guides at [capzy.ai/docs](https://capzy.ai/docs)

---

## Roadmap

- **Native `AsyncCapzyClient`** — `asyncio`-native client, same API surface.
- **Streaming `solveMany()`** — fan out N tasks, yield as they finish.

Want something prioritised? Open a [GitHub issue](https://github.com/capzy-ai/capzy-pip/issues) or email **support@capzy.ai**.

---

## Links

- 🌐 **Website:** https://capzy.ai
- 📚 **Documentation:** https://capzy.ai/docs
- 💵 **Pricing:** https://capzy.ai/pricing
- 🔑 **Dashboard / API keys:** https://capzy.ai/dashboard
- 🆓 **Free credits on sign-up:** https://capzy.ai/auth/register
- 📜 **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- 🐛 **Issues:** https://github.com/capzy-ai/capzy-pip/issues
- 💬 **Support:** support@capzy.ai

---

## License

MIT — see [LICENSE](LICENSE). Use it in proprietary software, redistribute it, fork it. Just don't blame us if your bot finds love.

<div align="center">
<sub>Built with care by the Capzy team — <a href="https://capzy.ai">capzy.ai</a></sub>
</div>
