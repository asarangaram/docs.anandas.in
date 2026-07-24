---
tags:
  - http
  - networking
  - debugging
---

# "Server disconnected without sending a response" — a keep-alive race

An HTTP client that **polls** or otherwise makes repeated requests with idle gaps
sometimes fails, intermittently, with something like:

- Python / **httpx**: `httpx.RemoteProtocolError: Server disconnected without sending a response.`
- Dart / **package:http**: `ClientException: Connection closed before full header was received`

The request never reaches the server. It fails at the transport layer, and it's
**timing-dependent** — the same call works most of the time.

## Cause (not your code, not a server bug)

HTTP clients keep a **connection pool** and reuse **keep-alive** connections.
Servers close idle keep-alive connections after a timeout (uvicorn defaults to
~5s). If your next request happens to **reuse a connection the server just
closed**, the send fails. Polling loops with backoff are the classic trigger:
the gap between polls grows past the server's keep-alive timeout, so the pooled
connection is dead by the time you reuse it.

Nothing is actually wrong — it's inherent to keep-alive + connection pooling.

## Fix: retry idempotent requests on transient transport errors

A retry simply opens a **fresh** connection and succeeds. Retry only the
transport-level failures; never swallow real HTTP status errors (4xx/5xx).

Python (httpx) — note `httpx.HTTPStatusError` is **not** a `TransportError`, so
it still propagates:

```python
for attempt in range(3):
    try:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()
    except httpx.TransportError:          # RemoteProtocolError, ConnectError, …
        if attempt == 2:
            raise
        await asyncio.sleep(0.5 * (attempt + 1))
```

Dart (package:http):

```dart
// retry on http.ClientException / SocketException / TimeoutException
```

!!! note
    httpx's built-in `AsyncHTTPTransport(retries=N)` only retries **connection**
    errors (`ConnectError`), **not** a `RemoteProtocolError` on an already-open
    reused connection — so you need the explicit retry above. Dart's
    `package:http` doesn't retry by default either; wrap it yourself.
