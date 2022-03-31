import ProxyService from "./server/services/proxy";
import ServerService from "./server/services/server";

export default class StartApp {
    constructor () {}

    onInit() {
        process.stdout.write('Starting Mercator Server \n');
        ProxyService.loadProxy();
        process.stdout.write('Starting Mercator WebServer\n');
        const server = new ServerService();
        server.start();
        process.stdout.write('Mercator WebServer Started\n');
        return true;
    }
}

const app = new StartApp();

app.onInit();