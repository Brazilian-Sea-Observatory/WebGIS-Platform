if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw-cache.js', { scope: './' })
    .then((reg) => {
        if (reg.installing) {
            console.log('Service worker installing');
        } else if (reg.waiting) {
            console.log('Service worker installed');
        } else if (reg.active) {
            console.log('Service worker active');
        }
    }).catch(function(error) {
        console.warn('Registration failed with ' + error);
    });
}