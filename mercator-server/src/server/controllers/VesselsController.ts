import { IRouteController } from '../modules/route';
import { ServerHttp2Stream } from 'http2';
import { ServerResponse, get } from 'http';

let memoizer: Map<string, string> = new Map();
const vesselURL =
    'http://data.aishub.net/ws.php?username=AH_2929_92FA06BA&format=1&output=xml&compress=0&latmin=-40&latmax=10&lonmin=-60&lonmax=-20';
export default class VesselsController implements IRouteController {
    private makeRequest(): Promise<string> {
        return new Promise((resolve, reject) => {
            get(
                vesselURL,
                (res: {
                    statusCode?: any;
                    headers?: any;
                    resume?: any;
                    setEncoding?: any;
                    on?: any;
                }) => {
                    const { statusCode } = res;
                    const contentType = res.headers['content-type'];

                    let error;
                    if (statusCode !== 200) {
                        error = new Error(
                            'Request Failed.\n' + `Status Code: ${statusCode}`,
                        );
                    } else if (!/^text\/xml/.test(contentType)) {
                        error = new Error(
                            'Invalid content-type.\n' +
                                `Expected text/xml but received ${contentType}`,
                        );
                    }
                    if (error) {
                        console.error(error.message);
                        res.resume();
                        return;
                    }

                    res.setEncoding('utf8');
                    let rawData = '';
                    res.on('data', (chunk: string) => {
                        rawData += chunk;
                    });
                    res.on('end', () => {
                        try {
                            console.log(rawData);
                            resolve(rawData);
                        } catch (e) {
                            console.error(e.message);
                            reject(e.message);
                        }
                    });
                },
            ).on('error', (e: { message: any }) => {
                console.error(`Got error: ${e.message}`);
                reject(e.message);
            });
        });
    }

    private readData() {
        const key = new Date().toDateString();
        if (memoizer.get(key)) {
            return Promise.resolve(memoizer.get(key));
        }

        return this.makeRequest().then((data: string) => {
            memoizer.set(key, data);
            return data;
        });
    }

    async send(stream?: ServerHttp2Stream | ServerResponse) {
        if (!stream) {
            throw new Error('No stream assigned to controller');
        }

        const data = await this.readData();
        return stream.end(JSON.stringify({ data: data || {} }));
    }
}
