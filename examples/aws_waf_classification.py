"""Classify the AWS WAF image puzzle without a full solve.

Useful when you have your own session pipeline and only need the
image-pick step. Returns the indices of the matching tiles.

Run with:
    pip install capzy
    python aws_waf_classification.py
"""

import base64

from capzy import CapzyClient


def load_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")

solution = capzy.solve(
    type="AwsWafClassification",
    images=[load_b64("tile_1.png"), load_b64("tile_2.png"), load_b64("tile_3.png")],
    question="Pick all tiles containing a car",
)

print("matching tile indices:", solution["indices"])
