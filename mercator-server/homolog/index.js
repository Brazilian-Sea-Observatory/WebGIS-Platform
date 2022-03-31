"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var proxy_1 = __importDefault(require("./server/services/proxy"));
var server_1 = __importDefault(require("./server/services/server"));
var StartApp = /** @class */ (function () {
    function StartApp() {
    }
    StartApp.prototype.onInit = function () {
        process.stdout.write('Starting Mercator Server \n');
        proxy_1.default.loadProxy();
        process.stdout.write('Starting Mercator WebServer\n');
        var server = new server_1.default();
        server.start();
        process.stdout.write('Mercator WebServer Started\n');
        return true;
    };
    return StartApp;
}());
exports.default = StartApp;
var app = new StartApp;
app.onInit();
//# sourceMappingURL=index.js.map