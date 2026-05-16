# Getting started

In 60 seconds you'll have a real, working integration.

## 1. Sign up + grab your free credits

Create an account at **[capzy.ai/auth/register](https://capzy.ai/auth/register)** — every new account starts with **$0.10 of free credits** posted as a real `bonus` transaction. That's enough to fire 50–100 test solves in production before you pay a cent.

## 2. Create an API key

Visit **[capzy.ai/dashboard](https://capzy.ai/dashboard) → API keys → New key**. Copy it now — keys are shown once.

The key looks like `capzy_xxxxxxxxxxxxxxxxxxxxxxxx`.

## 3. Solve a captcha

```python
from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")

solution = capzy.solve(
    type="AntiTurnstileTaskProxyLess",
    website_url="https://example.com/login",
    website_key="0x4AAAAAAA000000000000000000",
)
print(solution["token"])
```

Run it:

```bash
python my_solve.py
```

That's the entire SDK surface for the common case.

## What just happened

```
your script ──▶ capzy.solve(type="...", **params)
                       │
                       ├──▶ POST /createTask     {clientKey, task}
                       │     ◀── {taskId, timeout}
                       │
                       └─▶ POST /getTaskResult   {clientKey, taskId}   (every 2s)
                             ◀── {status: "processing"}                (until ready)
                             ◀── {status: "ready", solution: {...}}
                       │
return ─◀ solution dict (e.g. {"token": "..."})
```

`solve()` raises:

- `ApiError` — `createTask` returned an `errorId != 0` (bad key, wrong task type, insufficient funds, rate-limited).
- `TaskFailedError` — `getTaskResult` returned `status: "failed"`. **Auto-refunded.**
- `TaskTimeoutError` — `max_wait` elapsed before `status` reached `"ready"` or `"failed"`. **Auto-refunded.**

See [Error handling](./error-handling.md) for the full matrix.

## Lower-level: drive the API yourself

If you need to do something exotic (custom polling backoff, batching, etc.), the same `CapzyClient` exposes the raw verbs:

```python
created = capzy.create_task(
    type="AntiTurnstileTaskProxyLess",
    website_url="https://example.com",
    website_key="0x4AAA...",
)
task_id = created["taskId"]

import time
while True:
    time.sleep(1.5)
    result = capzy.get_task_result(task_id)
    if result["status"] == "ready":
        print(result["solution"])
        break
    if result["status"] == "failed":
        raise RuntimeError(result["errorDescription"])
```

`solve()` is just a thin wrapper around exactly this pattern.

## Parameter naming

Pass either snake_case (`website_url`) or camelCase (`websiteURL`) — they're equivalent. The SDK normalises snake_case to the camelCase the API expects on the wire.

## Where to next

- [Task type reference](./task-types.md) — every supported captcha and how to call it
- [Error handling](./error-handling.md) — every exception, every `errorCode`
- [Proxies](./proxies.md) — when and how to use a proxy
- [examples/](../examples/) — copy-paste-able scripts per service
