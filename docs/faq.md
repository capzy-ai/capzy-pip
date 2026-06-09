# FAQ

### Do you have an async client?

Not yet. The sync client is intentionally tiny — pair it with
`anyio.to_thread.run_sync`, `asyncio.to_thread`, or a thread pool if you
need fan-out today. A native `AsyncCapzyClient` is on the roadmap (same
API surface, `async def` everywhere).

### How concurrent can I be?

The default per-key concurrency cap is enough for most users — check
your dashboard for the exact number on each key. Hitting the cap surfaces
as `ApiError(error_code="ERROR_RATE_LIMIT")`; back off and retry. Higher
caps for enterprise users — email `support@capzy.ai`.

### How do I know if I picked the wrong task type?

The API tries to tell you. When `createTask` rejects with
`ERROR_WRONG_TASK_TYPE`, the response includes `recommendedTaskType` —
the SDK surfaces it as `ApiError.recommended_task_type`. Resubmit with
that and you're done.

### Can I use the SDK in long-running services?

Yes. Re-use one `CapzyClient` across threads — the underlying
`requests.Session` is thread-safe for the way we use it (one request at
a time per thread, no shared mutable state in the client).

### Does the SDK retry automatically?

No. We intentionally don't auto-retry — retries against the wrong error
mode can charge you extra (e.g. retrying a soft-failed v3 task is fine;
retrying an `ERROR_KEY_DOES_NOT_EXIST` is pointless). The
[error handling](./error-handling.md) page has a recommended retry
pattern you can drop in.

### What happens to a task if my script crashes mid-solve?

The task runs to completion on the backend regardless. Your account is
charged on success and refunded on failure exactly as if you had been
polling. If you saved the `taskId`, you can pick up the result later
with `capzy.get_task_result(task_id)`.

### Do you log my task data?

We store the task body and solution long enough to fulfil the request,
power dashboards (per-task latency, score quality, refunds), and meet
compliance requirements. We do **not** sell or share task data. Full
policy at [capzy.ai/legal/privacy](https://capzy.ai/legal/privacy).

### Is there a free trial?

Yes — every new account is credited **$0.10** at sign-up, with no card
required. That's enough to run 50–100 real solves end-to-end. See
[Authentication & API keys](./authentication.md) for the per-captcha
math.

### How do I cancel?

There's nothing to cancel. We're pay-as-you-go — no subscription, no
auto-renewal. Stop using the API and you stop being charged. Your
remaining balance stays in your account; refunds on unused balance are
available on request.

### Why are some images / cookies returned as opaque blobs?

Anti-bot platforms (Akamai, Kasada, etc.) encode their tokens
opaquely — we return them verbatim because that's what the target site
expects. Don't try to decode them; replay them as-is.

### Where do I get support?

- 📧 `support@capzy.ai` — fastest for account / billing questions.
- 🐛 [github.com/capzy-ai/capzy-pip/issues](https://github.com/capzy-ai/capzy-pip/issues) — bugs in this SDK.
- 💬 Live chat on the [dashboard](https://capzy.ai/dashboard) — same humans, same response time.

---

Back to [docs index](./README.md).
