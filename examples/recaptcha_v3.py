"""Solve reCAPTCHA v3 and (optionally) report the verified score back.

reCAPTCHA v3 is score-based — Google returns 0.0-1.0 from siteverify.
After verifying server-side, call capzy.report_score() with the result
to light up your v3 quality dashboard and help us auto-tune routing
for your traffic. Reporting is optional but recommended.

Run with:
    pip install capzy
    python recaptcha_v3.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")


# ── 1. Proxyless (recommended — we handle the upstream routing) ─────────

# Use the lower-level verbs so we can capture the taskId for report_score.
created = capzy.create_task(
    type="ReCaptchaV3TaskProxyLess",
    website_url="https://example.com",
    website_key="6Lc_aCMTAAAAAB...",
    page_action="checkout",
    min_score=0.7,
)
task_id = created["taskId"]

import time
result = capzy.get_task_result(task_id)
while result.get("status") == "processing":
    time.sleep(2)
    result = capzy.get_task_result(task_id)

if result.get("status") != "ready":
    raise SystemExit(f"task failed: {result.get('errorDescription')}")

token = result["solution"]["gRecaptchaResponse"]
print("token (proxyless):", token)

# ... your backend now POSTs the token to Google siteverify with your secret.
# Suppose siteverify returns {"score": 0.9, "action": "checkout"} — tell us:
capzy.report_score(task_id, score=0.9, action="checkout", hostname="example.com")


# ── 2. Through your own proxy ────────────────────────────────────────────

solution = capzy.solve(
    type="ReCaptchaV3Task",
    website_url="https://example.com",
    website_key="6Lc_aCMTAAAAAB...",
    page_action="checkout",
    min_score=0.7,
    proxy_type="http",
    proxy_address="123.45.67.89",
    proxy_port=8080,
    proxy_login="user",
    proxy_password="pass",
)

print("token (via proxy):", solution["gRecaptchaResponse"])
