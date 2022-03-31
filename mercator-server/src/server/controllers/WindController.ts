import { IRouteController } from '../modules/route';
import { ServerHttp2Stream } from 'http2';
import { readdirSync } from 'fs';
import { resolve } from 'path';
import { ServerResponse } from 'http';

let memoizer: Map<string, any> = new Map();
const jsonPath =
    process.env.WIND_JSON_PATH || resolve(__dirname, '../../../wind-data');
export default class WindController implements IRouteController {
    private readJSON(date: string, path: string) {
        const key = `${date}:${path}`
        if (!memoizer.get(key)) {
	    const dataPath = `${jsonPath}/${path ? path + '/' : path}`;
	    const data = readdirSync(jsonPath + '/' + path);
            const map = new Map();
            data.filter((e: string) => e.includes('.json')).forEach((e: string) => {
                map.set(`${e.replace('.json', '')}:${path}`, require(dataPath + e));
            });

            memoizer = map;
            setTimeout(() => {
                memoizer =  new Map();
            }, 3600000);
        }

        return memoizer.get(key);
    }

    send(stream?: ServerHttp2Stream | ServerResponse, query?: any) {
        if (!stream) {
            throw new Error('No stream assigned to controller');
        }

        const data = this.readJSON((query || {}).date, (query || { path: '' }).path || '');
        return stream.end(JSON.stringify({ data: data || {} }));
    }
}

export class AvailableDatesController implements IRouteController {
    send(stream?: ServerHttp2Stream | ServerResponse): void {
        if (!stream) {
            throw new Error('No stream assigned to controller');
        }

        const data = readdirSync(jsonPath);
        return stream.end(
            JSON.stringify({
                data: data.map(e => e.replace('.json', '')),
            }),
        );
    }
}
