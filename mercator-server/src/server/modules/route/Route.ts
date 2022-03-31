import NullController from "./NullController";
import { IRoute, IRouteController } from ".";
export class Route implements IRoute {
    method: string;
    path: string;
    controller: IRouteController;
    constructor(method: string, path: string, controller?: IRouteController) {
        this.path = path;
        this.method = method;
        this.controller = controller || new NullController();
    }
    public static genKey(method: string, path: string): string {
        return `${method}:${path}`;
    }
    get key(): string {
        return Route.genKey(this.method, this.path);
    }
}
