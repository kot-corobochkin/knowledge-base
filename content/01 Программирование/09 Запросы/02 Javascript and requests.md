


**“Does JavaScript always send requests using `fetch`, or are there other ways?”**

Short answer: **no — `fetch` is just one of several ways.**  
Web apps can send data through different browser mechanisms.

The most common ones are:

1. **`fetch()`** – modern standard way.
2. **`XMLHttpRequest (XHR)`** – older but still widely used.
3. **`navigator.sendBeacon()`** – often used for analytics or background sending.
4. **WebSocket** – persistent connection instead of separate HTTP requests.
5. **Requests inside Web Workers / Service Workers** – they can call their own `fetch`.
6. **Internal browser mechanisms** (for example service worker forwarding requests).

So the network flow can look like:
```
Page JS  
   ↓  
(fetch / XHR / worker / websocket / beacon)  
   ↓  
Browser network layer  
   ↓  
Server
```
In your case, since:

- `window.fetch` is patched
- XHR is not firing
- but requests still appear in Network

…it strongly suggests **a worker or service worker**.