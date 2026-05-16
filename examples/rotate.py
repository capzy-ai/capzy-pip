"""Rotate-to-upright captcha — returns the rotation angle in degrees.

Run with:
    pip install capzy
    python rotate.py path/to/tilted.png
"""

import base64
import sys

from capzy import CapzyClient

if len(sys.argv) < 2:
    sys.stderr.write("usage: python rotate.py path/to/tilted.png\n")
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    body_b64 = base64.b64encode(f.read()).decode()

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")

solution = capzy.solve(type="RotateTask", body=body_b64)

print("angle:", solution["angle"])    # degrees clockwise to upright
