// Service worker: offline use + versioned updates. Bump VERSION on every release.
const VERSION = "1.0.10";
const CACHE = 'lotto-filter-' + VERSION;
const CORE = ["./", "./index.html", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png", "./lib/jsQR.js"];
// install: always download fresh copies (bypass the browser HTTP cache) and take over right away
self.addEventListener('install', e => { self.skipWaiting(); e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE.map(u => new Request(u, { cache: 'reload' }))))); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('message', e => { if (e.data === 'skipWaiting') self.skipWaiting(); });
const fresh = req => fetch(req.url, { cache: 'no-cache', credentials: 'same-origin' }).then(r => { if (r.ok) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); } return r; }).catch(() => caches.match(req, { ignoreSearch: true }));
self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;
  // the page itself, version info and draw data: network first (offline -> cached copy)
  if (req.mode === 'navigate' || /\/(index\.html|version\.json|sw\.js)?$/.test(url.pathname) || url.pathname.endsWith('/data/draws.json')) { e.respondWith(fresh(req)); return; }
  // libraries and icons: cache first, then network (OCR modules are cached the first time they are used)
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => { if (r.ok) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); } return r; })));
});
