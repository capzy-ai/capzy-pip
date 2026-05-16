# Authentication & API keys

## Free credits on every new account

When you sign up at **[capzy.ai/auth/register](https://capzy.ai/auth/register)**, **$0.10 in real credits** is posted to your account as a `bonus` transaction. No credit card required, no email-verification gate, no trial expiry. It behaves exactly like any other balance — you can audit it in your dashboard's payment log.

That's enough to:

| Captcha | Solves you can run |
|---|---|
| Image-to-Text | ~100 |
| Cloudflare Turnstile | ~83 |
| CaptchaFox | ~83 |
| reCAPTCHA v3 | ~66 |
| reCAPTCHA v2 | ~50 |
| GeeTest v4 | ~33 |

When the bonus runs out, top up with **Stripe** (card, Apple Pay, Google Pay) or **MixPay** (USDT, BTC, 30+ coins). No subscription, no minimum, no monthly retainer.

## Creating an API key

1. Sign in at **[capzy.ai/dashboard](https://capzy.ai/dashboard)**.
2. Open the **API keys** tab.
3. Click **New key**. Give it a label (e.g. `prod-scraper-east`) and save.
4. **Copy the key now** — it is shown once. Lost keys can be revoked but not recovered.

A key looks like `capzy_` followed by ~24 random characters.

## Using the key

```python
from capzy import CapzyClient

capzy = CapzyClient("capzy_xxxxxxxxxxxxxxxxxxxxxxxx")
```

Or — recommended for any real deployment — read from the environment:

```python
import os
from capzy import CapzyClient

capzy = CapzyClient(os.environ["CAPZY_API_KEY"])
```

## Multiple keys per account

You can mint as many keys as you want. Each key is independently tracked:

- per-key spend
- per-key task success rate
- per-key concurrency limit
- per-key revocation (kill one without affecting others)

A common setup:

- one key per service / region / environment
- a separate key for CI / staging
- a "kill switch" key with a tight concurrency limit, used for any code path you don't fully trust yet

## Rotating a key

1. Mint a new key.
2. Roll the new key into your deployment.
3. Revoke the old key from the dashboard. In-flight tasks finish; new `createTask` requests on the old key are rejected with `ERROR_KEY_DOES_NOT_EXIST`.

## What happens to balance on key revocation

Nothing. Balance is account-wide, not key-scoped. Revoking a key just blocks that token from making API calls — your dollars are still there for the remaining keys.

## Why not use an `Authorization` header?

The Capzy API follows the `createTask` / `getTaskResult` shape that has become the de-facto industry standard. Tokens travel in the JSON body as `clientKey`. This means any script you already have, written against the same shape, ports to Capzy by changing one constant (`base_url`).

---

Next: [Pricing →](./pricing.md)
