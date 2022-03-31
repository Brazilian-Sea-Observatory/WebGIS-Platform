import { IRouteController } from '.';

export default class NullController implements IRouteController {
    send(): void { }
}
