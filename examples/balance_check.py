"""Print the current account balance — handy for billing health checks.

Run with:
    pip install capzy
    python balance_check.py
"""

from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")

print(f"balance: ${capzy.get_balance():.4f}")
