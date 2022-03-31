"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var http2_1 = __importDefault(require("http2"));
var fs_1 = __importDefault(require("fs"));
var path_1 = __importDefault(require("path"));
var mime_types_1 = __importDefault(require("mime-types"));
var _a = http2_1.default.constants, HTTP2_HEADER_PATH = _a.HTTP2_HEADER_PATH, 
// HTTP2_HEADER_METHOD,
HTTP_STATUS_NOT_FOUND = _a.HTTP_STATUS_NOT_FOUND, HTTP_STATUS_INTERNAL_SERVER_ERROR = _a.HTTP_STATUS_INTERNAL_SERVER_ERROR;
var options = {
    key: fs_1.default.readFileSync(path_1.default.resolve(__dirname, '../../../cert.key')),
    cert: fs_1.default.readFileSync(path_1.default.resolve(__dirname, '../../../cert.crt')),
    allowHTTP1: true
};
var serverRoot = path_1.default.join(__dirname, './static');
var ServerService = /** @class */ (function () {
    function ServerService() {
        this.server = http2_1.default.createSecureServer(options);
    }
    ServerService.prototype.start = function () {
        var _this = this;
        this.server.on('stream', function (stream, headers) {
            var reqPath = headers[HTTP2_HEADER_PATH];
            // const reqMethod = headers[HTTP2_HEADER_METHOD];
            var fullPath = path_1.default.join(serverRoot, reqPath);
            var responseMimeType = mime_types_1.default.lookup(fullPath);
            stream.respondWithFile(fullPath, {
                'content-type': responseMimeType
            }, {
                onError: function (err) { return _this.respondToStreamError(err, stream); }
            });
        });
        this.server.listen(process.env.SERVER_PORT || 8443);
    };
    ServerService.prototype.respondToStreamError = function (err, stream) {
        console.log(err);
        if (err.code === 'ENOENT') {
            stream.respond({ ":status": HTTP_STATUS_NOT_FOUND });
        }
        else {
            stream.respond({ ":status": HTTP_STATUS_INTERNAL_SERVER_ERROR });
        }
        stream.end();
    };
    return ServerService;
}());
exports.default = ServerService;
//# sourceMappingURL=server.js.map