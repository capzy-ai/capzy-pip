"""Solve a 'what is 7 + 3?' style math captcha image.

Returns synchronously from createTask — no polling.

Run with:
    pip install capzy
    python math_captcha.py path/to/captcha.png
"""

import base64
import sys

from capzy import CapzyClient

if len(sys.argv) < 2:
    sys.stderr.write("usage: python math_captcha.py path/to/captcha.png\n")
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    body_b64 = base64.b64encode(f.read()).decode()

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")

solution = capzy.solve(type="MathCaptchaTask", body=body_b64)

print("answer:", solution["text"])
