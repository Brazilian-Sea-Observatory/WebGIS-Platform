'use strict';
const VERSION = 4;
const CURRENT_CACHES = {
  files: `cache-${VERSION}`
}

self.addEventListener('activate', function (event) {
  const expectedCacheNames = Object.values(CURRENT_CACHES);

  event.waitUntil(
    caches.keys().then(function (cacheNames) {
      return Promise.all(
        cacheNames.map(function (cacheName) {
          if (!expectedCacheNames.includes(cacheName)) {
            console.log('Deleting out of date cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});


self.addEventListener('fetch', function (event) {
  event.respondWith(
    caches.open(CURRENT_CACHES.models).then(cache => {
      return cache.match(event.request).then(function (response) {
        if (response) {
          return response; //Arquivo encontrado no Cache
        }

        return fetch(event.request.clone()).then(function (response) {
          if (response.status < 400 && event.request.url.includes('geoserver')) {
            //Adicionando/Atualizando Cache
            cache.put(event.request, response.clone());
          } 

          return response;
        });
      }).catch(function (error) {
        console.error('Error in fetch handler:', error);
        throw error;
      });
    })
  );
});