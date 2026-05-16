# Error handling

Every error raised by the SDK descends from `capzy.CapzyError`. There
are exactly three you need to catch in normal use.

## The three you'll see in production

### `ApiError`

`createTask` returned `errorId != 0`. The task **was not submitted** — your account was not charged.

```python
from capzy import CapzyClient, ApiError

capzy = CapzyClient("capzy_xxx")
try:
    capzy.solve(
        type="AntiTurnstileTaskProxyLess",
        website_url="https://example.com",
        website_key="0x4AAA...",
    )
except ApiError as e:
    e.error_id              # int
    e.error_code            # str, e.g. "ERROR_NO_SLOT_AVAILABLE"
    e.error_description     # human-readable string
    e.recommended_task_type # str | None — set if API hints you picked the wrong type
    e.raw                   # full decoded JSON body, for logging
```

When to retry vs surface:

| `error_code` | Retry? | What to do |
|---|---|---|
| `ERROR_KEY_DOES_NOT_EXIST` | No | Fix the API key. |
| `ERROR_KEY_DISABLED` | No | Mint a new key in the dashboard. |
| `ERROR_NO_FUNDS` | No | Top up at [capzy.ai/dashboard](https://capzy.ai/dashboard). |
| `ERROR_RATE_LIMIT` | Yes, with backoff | Your account's concurrency cap was hit. Sleep + retry. |
| `ERROR_NO_SLOT_AVAILABLE` | Yes | Solver pool is momentarily full. Retry in 1–5s. |
| `ERROR_WRONG_TASK_TYPE` | Yes, with new type | Use `e.recommended_task_type` to resubmit. |
| `ERROR_INVALID_TASK_DATA` | No | Check required fields for the task type. |
| `ERROR_TASK_TYPE_DISABLED` | No | The captcha type is not currently sold. |

### `TaskFailedError`

`getTaskResult` returned `status: "failed"` — the task ran but couldn't be solved. **Automatically refunded.**

```python
from capzy import TaskFailedError

try:
    capzy.solve(type="...", **params)
except TaskFailedError as e:
    e.task_id
    e.error_code        # e.g. "ERROR_RECAPTCHA_INVALID_SITEKEY"
    e.error_description
```

Typical fixes: re-fetch the sitekey from the page, change the `page_action` to match what the page actually uses, or try the proxy variant if the token needs to be IP-bound.

### `TaskTimeoutError`

The task did not return a `ready` or `failed` status within `max_wait` seconds (default 180s). **Automatically refunded** by the backend if it later times out server-side.

```python
from capzy import TaskTimeoutError

try:
    capzy.solve(type="...", max_wait=60.0, **params)
except TaskTimeoutError as e:
    e.task_id
    e.waited       # seconds
```

You can still `capzy.get_task_result(task_id)` afterwards if you want
to check what happened.

## All exceptions

```
CapzyError                 # base — catch this if you don't care which
├── ApiError               # createTask rejected
├── TaskFailedError        # getTaskResult returned status="failed"
└── TaskTimeoutError       # poll deadline hit before ready/failed
```

Also raised by `CapzyClient.__init__`:

- `ValueError("api_key is required")` if you pass an empty string.

And by the underlying HTTP layer:

- `CapzyError("network error ...")` wrapping any `requests.RequestException`.
- `CapzyError("HTTP 4xx/5xx ...")` if the API returns a non-JSON error body.

## Retry pattern (recommended)

```python
import time, random
from capzy import CapzyClient, ApiError, TaskFailedError, TaskTimeoutError

capzy = CapzyClient("capzy_xxx")

def solve_with_retry(type_, attempts=3, **params):
    for i in range(attempts):
        try:
            return capzy.solve(type=type_, **params)
        except ApiError as e:
            if e.error_code in ("ERROR_RATE_LIMIT", "ERROR_NO_SLOT_AVAILABLE"):
                time.sleep((2 ** i) + random.random())
                continue
            raise              # non-retriable
        except TaskFailedError:
            time.sleep(1.0)    # transient solver miss — let the pool re-roll
            continue
        except TaskTimeoutError:
            continue           # already refunded — try again
    raise RuntimeError(f"solve failed after {attempts} attempts")

solve_with_retry(
    "AntiTurnstileTaskProxyLess",
    website_url="https://example.com",
    website_key="0x4AAA...",
)
```

## Refund audit trail

Every refund posts as a `refund` transaction visible at
[capzy.ai/dashboard](https://capzy.ai/dashboard) → Transactions. The
amount equals the original charge for that task. If you ever suspect a
refund is missing, the task UUID (`e.task_id`) is enough for support to
look it up — email `support@capzy.ai`.

---

Next: [Proxies →](./proxies.md)
