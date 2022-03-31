"use strict";
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
var cors_proxy = __importStar(require("cors-anywhere"));
var ProxyService = /** @class */ (function () {
    function ProxyService() {
    }
    ProxyService.loadProxy = function () {
        var host = process.env.HOST || '0.0.0.0';
        var port = process.env.PORT || 8081;
        cors_proxy
            .createServer({
            originWhitelist: [],
            requireHeader: [],
            removeHeaders: ['cookie', 'cookie2'],
        })
            .listen(port, host, function () {
            console.log('Running CORS Anywhere on ' + host + ':' + port);
        });
    };
    return ProxyService;
}());
exports.default = ProxyService;
//# sourceMappingURL=proxy.js.map