# Pricing

All prices are USD per successful solve. **Failed and timed-out tasks are automatically refunded** — refunds post as real `refund` transactions visible in your dashboard, so you can audit them.

Live source of truth: **[capzy.ai/pricing](https://capzy.ai/pricing)**. The tables below are reproduced from the same backend config that powers the API.

## Token-based captchas

| Captcha | Task type | Price |
|---|---|---|
| Cloudflare Turnstile | `AntiTurnstileTaskProxyLess` | **$0.0012** |
| Cloudflare Turnstile (proxy) | `AntiTurnstileTask` | $0.0012 |
| Cloudflare Challenge (full JS) | `AntiCloudflareTask` | $0.005 |
| CaptchaFox | `CaptchaFoxTaskProxyLess` | **$0.0012** |
| CaptchaFox (proxy) | `CaptchaFoxTask` | $0.0012 |
| reCAPTCHA v2 | `ReCaptchaV2TaskProxyLess` | **$0.002** |
| reCAPTCHA v2 (proxy) | `ReCaptchaV2Task` | $0.002 |
| reCAPTCHA v2 Enterprise | `ReCaptchaV2EnterpriseTaskProxyLess` | $0.004 |
| reCAPTCHA v3 | `ReCaptchaV3TaskProxyLess` | **$0.0015** |
| reCAPTCHA v3 (proxy) | `ReCaptchaV3Task` | $0.0015 |
| reCAPTCHA v3 Enterprise | `ReCaptchaV3EnterpriseTaskProxyLess` | $0.005 |
| FunCaptcha | `FunCaptchaTaskProxyLess` | $0.004 |
| GeeTest v4 | `GeeTestTaskProxyLess` / `GeeTestV4TaskProxyLess` | **$0.003** |
| GeeTest v3 | `GeeTestV3TaskProxyLess` | $0.0035 |
| Friendly Captcha | `FriendlyCaptchaTaskProxyLess` | $0.002 |
| MTCaptcha | `MtCaptchaTaskProxyLess` | $0.002 |
| ALTCHA | `AltchaTaskProxyLess` | $0.001 |
| Lemin | `LeminTaskProxyLess` | $0.0015 |
| Capy | `CapyTaskProxyLess` | $0.002 |
| NetEase Yidun | `YidunSliderTaskProxyLess` | $0.003 |
| Yandex SmartCaptcha | `YandexSmartCaptchaTaskProxyLess` | $0.025 |
| Binance bCAPTCHA2 | `BinanceCaptchaTask` | $0.003 |
| Tencent | `TencentTaskProxyLess` | $0.002 |
| Shopee Slider | `ShopeeSliderTaskProxyLess` | $0.002 |
| Shopee Curve | `ShopeeCurveTaskProxyLess` | $0.003 |
| Temu | `TemuCaptchaTaskProxyLess` | $0.002 |
| Alibaba | `AntiAlibabaCaptchaTaskProxyLess` | $0.003 |

## Anti-bot platforms

| Platform | Task type | Price |
|---|---|---|
| AWS WAF (full challenge) | `AntiAwsWafTaskProxyLess` | $0.012 |
| AWS WAF (proxy) | `AntiAwsWafTask` | $0.008 |
| AWS WAF image classify only | `AwsWafClassification` | **$0.0008** |
| DataDome Slider | `DataDomeSliderTask` | $0.04 |
| PerimeterX | `AntiPerimeterXTaskProxyLess` | $0.04 |
| PerimeterX (proxy) | `AntiPerimeterXTask` | $0.025 |
| Imperva Incapsula | `AntiImpervaTaskProxyLess` | $0.04 |
| Imperva Incapsula (proxy) | `AntiImpervaTask` | $0.025 |
| Akamai BMP (mobile) | `AntiAkamaiBMPTaskProxyLess` | $0.05 |
| Akamai BMP (mobile, proxy) | `AntiAkamaiBMPTask` | $0.03 |
| Kasada | `KasadaCaptchaTaskProxyLess` | $0.005 |

## Image-based

| Type | Task type | Price |
|---|---|---|
| Image-to-Text | `ImageToTextTask` | **$0.001** |
| Math Captcha | `MathCaptchaTask` | $0.001 |
| Coordinates Click | `CoordinatesTask` | $0.001 |
| Rotate | `RotateTask` | $0.001 |

## Volume

There are no volume tiers. The headline price *is* the price. Big customers send us emails (we have a few) and we work out custom solver routing where it makes sense, but there is no minimum spend and no marketing tier you need to unlock.

## How refunds work

- Failed (`status: "failed"`) → automatic refund, posts as a `refund` transaction.
- Timed out at the server-side hard timeout → automatic refund.
- The Python SDK exposes `e.error_code` on `TaskFailedError` so you can branch on the specific failure mode if you want to retry with a different task type / proxy.

## Top-up methods

- **Stripe** — Visa / Mastercard / Amex / Apple Pay / Google Pay / SEPA / iDEAL.
- **MixPay** — USDT (Tron, BSC, Ethereum, Polygon), BTC, ETH, BNB, SOL, TON, DOGE, and 30+ more.

No subscription, no minimum top-up.

---

Next: [Task type reference →](./task-types.md)
