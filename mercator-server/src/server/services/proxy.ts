import * as cors_proxy from 'cors-anywhere';

export default class ProxyService {
    public static loadProxy() {
        const host = process.env.HOST || '0.0.0.0';
        const port = process.env.PORT || 8081;

        cors_proxy
            .createServer({
                originWhitelist: [], // Allow all origins
                requireHeader: [], //['origin', 'x-requested-with'],
                removeHeaders: ['cookie', 'cookie2']
            })
            .listen(port, host, function() {
                console.log('Running CORS Anywhere on ' + host + ':' + port);
            });
    }
}
