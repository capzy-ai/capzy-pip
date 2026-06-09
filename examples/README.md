# Examples

Standalone, copy-paste-ready scripts — one per supported captcha service.

Every script follows the same shape:

```python
from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")   # from capzy.ai/dashboard

solution = capzy.solve(
    type="...",                # API task type
    website_url="...",
    website_key="...",
)
print(solution)
```

Token-based captchas show both the **proxyless** and **proxy** path on
the same page — the only difference is the `type` value and a few
extra `proxy_*` fields.

## Run one

```bash
pip install capzy
# (edit the file to paste your real API key in)
python cloudflare_turnstile.py
```

Don't have a key yet? Get one at **https://capzy.ai/auth/register** —
every new account starts with **$0.10 in free credits**, enough for
50–100 test solves before you pay a cent.

## Index

| File | What it shows |
|---|---|
| [cloudflare_turnstile.py](./cloudflare_turnstile.py) | Cloudflare Turnstile |
| [cloudflare_challenge.py](./cloudflare_challenge.py) | Cloudflare JS challenge (interstitial) |
| [captchafox.py](./captchafox.py) | CaptchaFox |
| [recaptcha_v2.py](./recaptcha_v2.py) | reCAPTCHA v2 (checkbox + invisible) |
| [recaptcha_v2_enterprise.py](./recaptcha_v2_enterprise.py) | reCAPTCHA v2 Enterprise |
| [recaptcha_v3.py](./recaptcha_v3.py) | reCAPTCHA v3 (with score reporting) |
| [recaptcha_v3_enterprise.py](./recaptcha_v3_enterprise.py) | reCAPTCHA v3 Enterprise |
| [funcaptcha.py](./funcaptcha.py) | FunCaptcha (Arkose) |
| [geetest_v4.py](./geetest_v4.py) | GeeTest v4 |
| [geetest_v3.py](./geetest_v3.py) | GeeTest v3 |
| [image_to_text.py](./image_to_text.py) | Generic OCR captchas |
| [math_captcha.py](./math_captcha.py) | Math image captchas |
| [coordinates.py](./coordinates.py) | "Click the cat" coordinate captchas |
| [rotate.py](./rotate.py) | Rotate-to-upright captchas |
| [datadome.py](./datadome.py) | DataDome slider |
| [aws_waf.py](./aws_waf.py) | AWS WAF full challenge |
| [aws_waf_classification.py](./aws_waf_classification.py) | AWS WAF image-classification only |
| [binance.py](./binance.py) | Binance bCAPTCHA2 |
| [perimeterx.py](./perimeterx.py) | PerimeterX (Human Security) |
| [alibaba.py](./alibaba.py) | Alibaba CAPTCHA |
| [temu.py](./temu.py) | Temu |
| [friendly_captcha.py](./friendly_captcha.py) | Friendly Captcha |
| [mtcaptcha.py](./mtcaptcha.py) | MTCaptcha |
| [altcha.py](./altcha.py) | ALTCHA |
| [lemin.py](./lemin.py) | Lemin Cropped |
| [shopee_slider.py](./shopee_slider.py) | Shopee Slider |
| [shopee_curve.py](./shopee_curve.py) | Shopee Curve Slider |
| [tencent.py](./tencent.py) | Tencent |
| [yandex.py](./yandex.py) | Yandex SmartCaptcha |
| [kasada.py](./kasada.py) | Kasada (KPSDK) |
| [imperva.py](./imperva.py) | Imperva Incapsula |
| [akamai_bmp.py](./akamai_bmp.py) | Akamai Bot Manager (mobile) |
| [capy.py](./capy.py) | Capy Puzzle |
| [yidun.py](./yidun.py) | NetEase Yidun |
| [balance_check.py](./balance_check.py) | Print account balance |
