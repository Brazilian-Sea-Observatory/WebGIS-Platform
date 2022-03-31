import { ServerHttp2Stream } from 'http2';
import { Route } from './Route';
import { ServerResponse } from 'http';

export interface IRouteController {
    send(stream?: ServerHttp2Stream | ServerResponse, query?: any): void;
}

export interface IRoute {
    method: string;
    path: string;
    controller: IRouteController;
    key: string;
}

export default class Router {
    routes: Map<string, IRoute> = new Map();

    constructor() {}

    find(method: string, path: string) {
        return this.routes.get(Route.genKey(method, path));
    }

    addRoute(route: Route) {
        this.routes.set(route.key, route);
    }

    private processError(
        stream: ServerHttp2Stream,
        code: number,
        message?: string,
    ) {
        stream.respond({
            'content-type': 'application/json',
            ':status': code,
        });

        return stream.end({ message });
    }

    dispatch(
        stream: ServerHttp2Stream,
        method: string,
        path: string,
        query: any,
    ) {
        const route = this.routes.get(Route.genKey(method, path));
        if (!route) {
            return this.processError(stream, 404, 'Não encontrado');
        }

        stream.respond({
            'content-type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS, POST, GET',
            'Access-Control-Max-Age': 2592000, // 30 days
            ':status': 200,
        });

        if (Object.keys(query).length > 0) {
            return route.controller.send(stream, query);
        }

        route.controller.send(stream);
    }
}
