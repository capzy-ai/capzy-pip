# Changelog

All notable changes to `capzy` are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
follows [Semantic Versioning](https://semver.org/).

## [0.0.1] — Unreleased

Pre-PyPI publish snapshot. Pinned at `0.0.1` until the listing is
approved; the first published version on PyPI will bump to `0.1.0`.

### Added

- `CapzyClient` — sync HTTP client with `solve`, `create_task`,
  `get_task_result`, `report_score`, `get_balance`.
- `solve(type=..., **params)` — submits + polls. Single-call solve for
  every supported captcha; takes the wire-level task `type` as a string
  and the task params as kwargs.
- Auto camelCase conversion of snake_case task params
  (`website_url` → `websiteURL`, `proxy_address` → `proxyAddress`, etc.)
  so you can write Python-style names without thinking about the wire
  format. CamelCase passes through untouched.
- `ApiError`, `TaskFailedError`, `TaskTimeoutError` for structured error
  handling; refunded tasks raise rather than silently succeed.
- Per-call polling tunables (`poll_interval`, `max_wait`).
- Session injection for proxies / retries / custom TLS.
- Examples for every currently-supported captcha service
  (Cloudflare Turnstile / Challenge, reCAPTCHA v2/v3 and Enterprise,
  FunCaptcha, GeeTest v3 / v4, CaptchaFox, MTCaptcha, Friendly Captcha,
  ALTCHA, Lemin, Capy, NetEase Yidun, Yandex SmartCaptcha, Binance
  bCAPTCHA2, Tencent, Shopee Slider, Shopee Curve, Temu, Alibaba,
  AWS WAF, DataDome, PerimeterX, Imperva, Akamai BMP, Kasada,
  Image-to-Text, Math, Coordinates, Rotate).
- Documentation set under [docs/](./docs).
