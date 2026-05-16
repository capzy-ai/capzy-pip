# Task type reference

Every currently-sold task type, its parameters, and the shape of the
`solution` dict it returns.

> **Parameter naming.** Snake_case (`website_url`, `page_action`) and
> camelCase (`websiteURL`, `pageAction`) are equivalent — the SDK
> normalises to the wire format the API expects.

Every task type has a **proxy variant**: drop the `ProxyLess` suffix
from the type name and add the proxy fields:

```python
proxy_type="http",        # http | https | socks4 | socks5
proxy_address="1.2.3.4",
proxy_port=8080,
proxy_login="user",       # optional
proxy_password="pass",    # optional
```

See [Proxies](./proxies.md) for when you actually need one.

Currently in **active development** but not yet sold: **hCaptcha** and
**hCaptcha Enterprise**. Submitting their types now returns
`ERROR_TASK_TYPE_DISABLED`; the SDK still ships the wire-level
identifiers so your code is forward-compatible.

---

## Cloudflare Turnstile

```python
capzy.solve(
    type="AntiTurnstileTaskProxyLess",
    website_url="https://example.com",
    website_key="0x4AAA...",
    action="login",     # optional, must match data-action
    cdata="user-123",   # optional, must match data-cdata
)
```

Returns: `{"token": "..."}` — submit as `cf-turnstile-response`.

## Cloudflare Challenge (JS interstitial)

```python
capzy.solve(
    type="AntiCloudflareTask",
    website_url="https://example.com",
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)
```

Returns: `{"cookies": {...}, "userAgent": "..."}` — replay both on subsequent requests.

The proxyless variant is **deprecated** and disabled — a proxy is required.

## CaptchaFox

```python
capzy.solve(
    type="CaptchaFoxTaskProxyLess",
    website_url="https://example.com",
    website_key="sk_...",
)
```

Returns: `{"token": "..."}`.

## reCAPTCHA v2

```python
capzy.solve(
    type="ReCaptchaV2TaskProxyLess",
    website_url="https://example.com",
    website_key="6Lc_...",
    is_invisible=False,
    data_s=None,         # optional, only for Google's own properties
)
```

Returns: `{"gRecaptchaResponse": "..."}` — submit as `g-recaptcha-response`.

## reCAPTCHA v2 Enterprise

```python
capzy.solve(
    type="ReCaptchaV2EnterpriseTaskProxyLess",
    website_url="https://example.com",
    website_key="6Lc_...",
    enterprise_payload={"s": "..."},   # optional
    api_domain="recaptcha.net",         # optional, only for .net deployments
)
```

Returns: `{"gRecaptchaResponse": "..."}`.

## reCAPTCHA v3 / v3 Enterprise

```python
capzy.solve(
    type="ReCaptchaV3TaskProxyLess",
    website_url="https://example.com",
    website_key="6Lc_...",
    page_action="checkout",
    min_score=0.7,
    is_enterprise=False,
    api_domain=None,
)
```

Returns: `{"gRecaptchaResponse": "..."}`.

> **Reporting the score back boosts your dashboard analytics** and helps us
> auto-route your traffic. After Google `siteverify` returns its score, call
> `capzy.report_score(task_id, score=..., action=..., hostname=...)`.

Enterprise variant: `type="ReCaptchaV3EnterpriseTaskProxyLess"`
(no `is_enterprise` flag needed).

## FunCaptcha

```python
capzy.solve(
    type="FunCaptchaTaskProxyLess",
    website_url="https://example.com",
    website_public_key="476068BF-9607-4799-B53D-966BE98E2B81",
    funcaptcha_api_js_subdomain="client-api.arkoselabs.com",  # optional
    data='{"blob": "..."}',                                   # optional
)
```

Returns: `{"token": "..."}`.

## GeeTest v4

```python
capzy.solve(
    type="GeeTestV4TaskProxyLess",
    website_url="https://example.com",
    captcha_id="b6e7caefb2533fd5b1fb05c1a3aebd6e",
)
```

Returns:

```python
{
  "captcha_id":     "...",
  "lot_number":     "...",
  "pass_token":     "...",
  "gen_time":       "1715000000",
  "captcha_output": "...",
}
```

> `type="GeeTestTaskProxyLess"` is an alias of v4 — kept for legacy compatibility.

## GeeTest v3

```python
capzy.solve(
    type="GeeTestV3TaskProxyLess",
    website_url="https://example.com",
    gt="022397c99c9f646f6477822485f30404",
    challenge="b6e7caefb2533fd5b1fb05c1a3aebd6e",
    geetest_api_server_subdomain="api.geetest.com",  # optional
)
```

Returns: `{"challenge": "...", "validate": "...", "seccode": "..."}`.

## Image-to-Text

```python
capzy.solve(
    type="ImageToTextTask",
    body="<base64-encoded PNG/JPG>",
    case="mixed",       # mixed | upper | lower | numbers | letters | alphanumeric
    phrase=False,
    numeric=0,          # 0 = anything, 1 = digits only, 2 = letters only
    min_length=4,
    max_length=8,
    comment="Lowercase letters and digits",
)
```

Returns: `{"text": "abc12"}`. Solution returned **synchronously** from `createTask` — no polling.

## Math Captcha

```python
capzy.solve(type="MathCaptchaTask", body="<base64 image>")
```

Returns: `{"text": "10"}`.

## DataDome Slider

```python
capzy.solve(
    type="DataDomeSliderTask",
    website_url="https://example.com",
    captcha_url="https://geo.captcha-delivery.com/captcha/?initialCid=...",
    user_agent="Mozilla/5.0 ...",
    proxy_type="http", proxy_address="...", proxy_port=8080,
)
```

Returns: `{"cookie": "datadome=..."}` — set as the `datadome` cookie on subsequent requests.

## AWS WAF

```python
capzy.solve(
    type="AntiAwsWafTaskProxyLess",
    website_url="https://example.com",
    # Optional context — scraped from the challenge page:
    aws_key=None, aws_iv=None, aws_context=None, aws_challenge_js=None,
)
```

Returns: `{"token": "..."}` — replay as `aws-waf-token`.

```python
capzy.solve(
    type="AwsWafClassification",
    images=["<base64>", "<base64>", "..."],
    question="Pick all tiles containing a car",
)
```

Returns: `{"indices": [0, 2]}` — only the image-pick step.

## Binance bCAPTCHA2

```python
capzy.solve(
    type="BinanceCaptchaTask",
    website_url="https://www.binance.com",
    website_key="login",
)
```

Returns: `{"validate": "..."}`.

## PerimeterX

```python
capzy.solve(type="AntiPerimeterXTaskProxyLess", website_url="https://example.com")
```

Returns: `{"cookies": {...}}`.

## Alibaba

```python
capzy.solve(
    type="AntiAlibabaCaptchaTaskProxyLess",
    website_url="https://example.com",
    website_key="X82Y...",
)
```

Returns: `{"token": "..."}`.

## Temu

```python
capzy.solve(type="TemuCaptchaTaskProxyLess", website_url="https://www.temu.com")
```

Returns: `{"cookies": {...}}`.

## Friendly Captcha

```python
capzy.solve(
    type="FriendlyCaptchaTaskProxyLess",
    website_url="https://example.com",
    website_key="FCMST6...",
)
```

Returns: `{"token": "..."}`.

## MTCaptcha

```python
capzy.solve(
    type="MtCaptchaTaskProxyLess",
    website_url="https://example.com",
    website_key="MTPublic-...",
)
```

Returns: `{"token": "..."}`.

## ALTCHA

```python
capzy.solve(type="AltchaTaskProxyLess", website_url="https://example.com")
```

Returns: `{"payload": "..."}` — set as the `altcha` form field.

## Lemin

```python
capzy.solve(
    type="LeminTaskProxyLess",
    website_url="https://example.com",
    website_key="CROPPED_...",
)
```

Returns: `{"answer": "...", "challenge_id": "..."}`.

## Shopee

```python
capzy.solve(type="ShopeeSliderTaskProxyLess", website_url="https://shopee.com/buyer/login")
capzy.solve(type="ShopeeCurveTaskProxyLess",  website_url="https://shopee.com/buyer/login")
```

Returns: `{"cookies": {...}}`.

## Tencent

```python
capzy.solve(
    type="TencentTaskProxyLess",
    website_url="https://example.com",
    app_id="2003319081",
)
```

Returns: `{"ticket": "...", "randstr": "..."}`.

## Yandex SmartCaptcha

```python
capzy.solve(
    type="YandexSmartCaptchaTaskProxyLess",
    website_url="https://example.com",
    website_key="ysc1_...",
)
```

Returns: `{"token": "..."}`.

## Kasada

```python
capzy.solve(type="KasadaCaptchaTaskProxyLess", website_url="https://example.com")
```

Returns: `{"x-kpsdk-ct": "...", "x-kpsdk-cd": "..."}` — replay as the matching request headers.

## Imperva Incapsula

```python
capzy.solve(
    type="AntiImpervaTaskProxyLess",
    website_url="https://example.com",
    user_agent="Mozilla/5.0 ...",
)
```

Returns: `{"cookies": {...}}`.

## Akamai BMP (mobile)

```python
capzy.solve(
    type="AntiAkamaiBMPTaskProxyLess",
    package_name="com.example.app",
    version="3.3.5",
)
```

Returns: `{"sensor_data": "..."}` — replay in the `X-Acf-Sensor-Data` header.

## Capy

```python
capzy.solve(
    type="CapyTaskProxyLess",
    website_url="https://example.com",
    website_key="PUZZLE_...",
)
```

Returns: `{"captchakey": "...", "challengekey": "...", "answer": "..."}`.

## Coordinates Click

```python
capzy.solve(
    type="CoordinatesTask",
    body="<base64>",
    comment="Click all images with a cat",
)
```

Returns: `{"coordinates": [{"x": 120, "y": 88}, ...]}` — image-pixel space.

## Rotate

```python
capzy.solve(type="RotateTask", body="<base64>")
```

Returns: `{"angle": 73}` — degrees clockwise needed to upright.

## NetEase Yidun

```python
capzy.solve(
    type="YidunSliderTaskProxyLess",
    website_url="https://example.com",
    captcha_id="9a371b56...",
)
```

Returns: `{"validate": "..."}`.

---

Next: [Error handling →](./error-handling.md)
