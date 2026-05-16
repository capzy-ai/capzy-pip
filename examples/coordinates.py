"""Click-coordinate captcha — 'Click the cat' style image puzzles.

Returns one or more (x, y) pairs in image-pixel space. Translate to the
on-page widget's coordinate system before submitting.

Run with:
    pip install capzy
    python coordinates.py path/to/image.png 'Click the cat'
"""

import base64
import sys

from capzy import CapzyClient

if len(sys.argv) < 3:
    sys.stderr.write("usage: python coordinates.py path/to/image.png 'Click the cat'\n")
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    body_b64 = base64.b64encode(f.read()).decode()

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")

solution = capzy.solve(
    type="CoordinatesTask",
    body=body_b64,
    comment=sys.argv[2],
)

for pt in solution.get("coordinates", []):
    print(pt["x"], pt["y"])
