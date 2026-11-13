// SafeBunk service worker — app shell cache (offline ke liye).
const CACHE = "safebunk-v2-9-2";
const SHELL = ["./", "index.html", "manifest.json", "firebase-config.js",
  "icon-192.png", "icon-512.png", "fonts/poppins-400.woff2", "fonts/poppins-600.woff2", "fonts/poppins-700.woff2", "fonts/poppins-800.woff2"];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(
    ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  if (url.origin === location.origin) {
    // same-origin: cache-first, phir network se refresh
    e.respondWith(caches.match(e.request).then(hit => {
      const net = fetch(e.request).then(r => {
        if (r.ok) caches.open(CACHE).then(c => c.put(e.request, r.clone()));
        return r;
      }).catch(() => hit);
      return hit || net;
    }));
  }
  // cross-origin (Firebase CDN): browser ki normal cache chalegi
});
