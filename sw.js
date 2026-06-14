const CACHE_NAME = 'daily-v5';
const ASSETS = [
  './',
  './index.html',
  './app.js',
  './prayers.js',
  './finance.js',
  './finance-corporate.js',
  './finance-gaap.js',
  './finance-nonprofit.js',
  './finance-investing.js',
  './finance-corporate-2.js',
  './finance-gaap-2.js',
  './finance-nonprofit-2.js',
  './finance-investing-2.js',
  './finance-corporate-3.js',
  './finance-gaap-3.js',
  './finance-nonprofit-3.js',
  './finance-investing-3.js',
  './finance-corporate-4.js',
  './finance-gaap-4.js',
  './finance-nonprofit-4.js',
  './finance-investing-4.js',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-512-maskable.png',
  './icons/apple-touch-icon.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
          return response;
        })
        .catch(() => cached);
    })
  );
});
