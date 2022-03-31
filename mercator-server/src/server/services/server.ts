import http2, {
    Http2SecureServer,
    ServerHttp2Stream,
    Http2Server,
} from 'http2';
import http, { Server } from 'http';
import fs from 'fs';
import path from 'path';
import mime from 'mime-types';
import Router from '../modules/route';
import WindController, {
    AvailableDatesController,
} from '../controllers/WindController';
import { Route } from '../modules/route/Route';
import { parse } from 'url';
import SpreadOilController from '../controllers/SpreadOilController';
import VesselsController from '../controllers/VesselsController';
import { StationController } from '../controllers/StationController';

const {
    HTTP2_HEADER_PATH,
    HTTP2_HEADER_METHOD,
    HTTP_STATUS_NOT_FOUND,
    HTTP_STATUS_INTERNAL_SERVER_ERROR,
} = http2.constants;

const options = {
    key: fs.readFileSync(path.resolve(__dirname, '../../../key.pem')),
    cert: fs.readFileSync(path.resolve(__dirname, '../../../cert.pem')),
    allowHTTP1: true,
    agent: false,
    rejectUnauthorized: false,
};

const serverRoot =
    process.env.STATIC_PATH ||
    path.join(__dirname, '../../../../mercator-webapp/dist');

export default class ServerService {
    private server: Http2SecureServer;
    private router = new Router();
    private port = process.env.SERVER_PORT || 8443;

    private unsercureServer: Server;
    private unsecurePort = process.env.UNSECURE_PORT || 3000;

    constructor() {
        this.server = http2.createSecureServer(options);
        this.unsercureServer = http.createServer();
    }

    public start() {
        this.bindRoutes();
        this.onStart(this.server);
        this.onStartUnsecure(this.unsercureServer);

        this.unsercureServer.listen(this.unsecurePort);
        this.server.listen(this.port);

        console.log(`Running HTTP/2 Server at: 0.0.0.0:${this.unsecurePort}`);
        console.log(`Running HTTP/2 Secure Server at: 0.0.0.0:${this.port}`);
    }

    private onStartUnsecure(server: Server) {
        server.on('request', (request, response) => {
            const { url, method } = request;
            response.setHeader('Access-Control-Allow-Origin', '*');
            response.setHeader(
                'Access-Control-Allow-Methods',
                'POST, GET, PUT, DELETE, OPTIONS',
            );
            response.setHeader('Access-Control-Allow-Credentials', 'false');
            response.setHeader('Access-Control-Max-Age', '86400');
            response.setHeader('Access-Control-Allow-Headers', '*');
            if (method === 'OPTIONS') {                
                response.statusCode = 200;
                return response.end();
            }

            const parsedUrl = parse(url, true);
            response.setHeader('content-type', 'application/json');
            const route = this.router.find(
                method,
                parsedUrl.pathname as string,
            );

            if (!!route) {
                return route.controller.send(response, parsedUrl.query);
            }

            response.statusCode = 404;
            response.end(JSON.stringify({ error: 'No data' }));
        });
    }

    private onStart(server: Http2SecureServer | Http2Server) {
        server.on('stream', (stream: ServerHttp2Stream, headers) => {
            const reqPath = headers[HTTP2_HEADER_PATH] as string;
            const reqMethod = <string>headers[HTTP2_HEADER_METHOD];
            if (reqMethod === 'OPTIONS') {
                const headers = {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods':
                        'POST, GET, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Credentials': 'false',
                    'Access-Control-Max-Age': '86400', // 24 hour,
                    // 'Access-Control-Allow-Headers': 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept',
                    'Access-Control-Allow-Headers': '*',
                    ':status': 200,
                };

                stream.respond(headers);
                return stream.end();
            }

            const currentPath = parse(reqPath, true);
            if (this.router.find(reqMethod, currentPath.pathname as string)) {
                return this.router.dispatch(
                    stream,
                    reqMethod,
                    currentPath.pathname as string,
                    currentPath.query,
                );
            }

            const fullPath = path.join(serverRoot, reqPath);
            const responseMimeType = mime.lookup(fullPath) as any;

            stream.respondWithFile(
                fullPath,
                {
                    'content-type': responseMimeType,
                },
                {
                    onError: err => this.respondToStreamError(err, stream),
                },
            );
        });
    }

    private bindRoutes() {
        const routes = [
            new Route('GET', '/api/wind', new WindController()),
            new Route(
                'GET',
                '/api/wind/available-dates',
                new AvailableDatesController(),
            ),
            new Route('GET', '/api/vessels', new VesselsController()),
            new Route('GET', '/api/spread-oil', new SpreadOilController()),
            new Route('GET', '/api/stations', new StationController())
        ];
        routes.forEach((route: Route) => {
            this.router.addRoute(route);
        });
    }

    private respondToStreamError(
        err: NodeJS.ErrnoException,
        stream: http2.ServerHttp2Stream,
    ) {
        console.log(err);
        if (err.code === 'ENOENT') {
            stream.respond({ ':status': HTTP_STATUS_NOT_FOUND });
        } else {
            stream.respond({ ':status': HTTP_STATUS_INTERNAL_SERVER_ERROR });
        }
        stream.end();
    }
}
