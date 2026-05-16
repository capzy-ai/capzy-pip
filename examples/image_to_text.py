"""OCR a generic image captcha.

ImageToText returns its solution synchronously from createTask — solve()
returns immediately, no polling.

Run with:
    pip install capzy
    python image_to_text.py path/to/captcha.png
"""

import base64
import sys

from capzy import CapzyClient

if len(sys.argv) < 2:
    sys.stderr.write("usage: python image_to_text.py path/to/captcha.png\n")
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    body_b64 = base64.b64encode(f.read()).decode()

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")

solution = capzy.solve(
    type="ImageToTextTask",
    body=body_b64,
    # case="mixed",          # mixed | upper | lower | numbers | letters | alphanumeric
    # comment="Lowercase letters and digits only",
    # min_length=4,
    # max_length=8,
)

print("text:", solution["text"])
