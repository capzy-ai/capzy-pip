"""Solve Binance bCAPTCHA2.

Run with:
    pip install capzy
    python binance.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")

solution = capzy.solve(
    type="BinanceCaptchaTask",
    website_url="https://www.binance.com",
    website_key="login",        # the bCAPTCHA scene id
    # validate_id="...",        # if pre-supplied by your flow
)

print("validate:", solution["validate"])
