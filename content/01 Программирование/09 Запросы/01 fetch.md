### What `window.fetch` is

`window.fetch` is a **browser API used by JavaScript in a page to send HTTP requests**.

In simple terms:

- The page’s script calls `fetch()`
- The browser sends a request to the server
- JavaScript receives the response (JSON, HTML, etc.)

Typical example:

`fetch("/api/data")`  
  `.then(res => res.json())`  
  `.then(data => console.log(data));`

Here the request goes through:

window.fetch → browser network stack → server

That’s why your hook works:
```

const originalFetch = window.fetch;  
window.fetch = async (...args) => { ... }
```
You are basically **intercepting every request made with `fetch` from the page**.

### Important detail (this is where your situation starts)

`window.fetch` exists only in the **main page context**.

But there are other contexts in a browser:

- Main page (where you injected code)
- Web Worker
- Service Worker
- Extension background scripts
- iframe with different context

Each of them can have **its own `fetch`**, separate from `window.fetch`.