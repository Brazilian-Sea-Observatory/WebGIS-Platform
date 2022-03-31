import { IRouteController } from '../modules/route';
import { ServerHttp2Stream } from 'http2';
import { resolve } from 'path';
import { ServerResponse } from 'http';
import { execSync } from 'child_process';

let memoizer: Map<string, any> = new Map();
const dataPath =
    process.env.SPREAD_OIL_PATH || resolve(__dirname, '../../../oil-data');

const formatDate = (date: Date) => date.toISOString().substr(0, 10);
export default class SpreadOilController implements IRouteController {
    private runSpillTool(lat: number, lon: number, date: string | Date) {
        // /home/maretec/Lagrangian_Global/BSO/exe\n
        try {
            const tommorowDate = new Date(date);
	    tommorowDate.setDate(tommorowDate.getDate() + 2);
	    console.log(tommorowDate, date)

	    console.info(
                'Executed: ',
                `./SpillTool.py ${formatDate(new Date(date))} ${formatDate(
                    tommorowDate,
                )} Continuous ${lon} ${lat}`,
                'at',
                dataPath,
            );
            return execSync(
                `./SpillTool.py ${formatDate(new Date(date))} ${formatDate(
                    tommorowDate,
                )} Continuous ${lon} ${lat}`,
                { cwd: dataPath, env: process.env, stdio: 'pipe' },
            ).toString();
        } catch (err) {
	        console.error(err);
            console.log(err.message);
	        console.log(err.stdout.toString());
            return null;
        }
    }

    private readFileData(lat: number | null, lon: number | null, date: string | null) {
        const key = `${dataPath}/${lat},${lon}`;

        if (!memoizer.get(key)) {
            const stdout = this.runSpillTool(lat || 0, lon || 0, date || '');
            if (!stdout) {
                return {
                    error: true,
                    message: 'Error running Lagrangian SpillTool',
                };
            }

            const data = (
                stdout.split('/home/maretec/Lagrangian_Global/BSO/exe\n') || []
            ).pop();
            if (!data) {
                return { error: true, message: 'Spill Tool stout Empty' };
            }

            const rows = data
                .replace(/\r/gi, '')
                .split('\n')
                .map(e => e.trim())
                .filter(e => !!e);
            const metadata = rows.splice(0, 7);
            const title = metadata.splice(0, 1)[0];
            const [name, latitude, longitude, volume, beginTime] = metadata.map(
                e => e.split(':').map(value => value.trim())[1],
            );
            const points = [];
            while (rows.length > 0) {
                const size = parseInt(rows[0], 10);
                points.push(
                    rows.splice(0, size + 1).map(row => {
                        const [
                            number,
                            time,
                            lat,
                            lon,
                            i,
                            j,
                            sta,
                            wd,
                            cur,
                            sst,
                            err,
                            depth,
                            volume,
                        ] = row
                            .split(' ')
                            .filter(content => !!content)
                            .map(col => col.trim());

                        return {
                            number,
                            time,
                            lat,
                            lon,
                            i,
                            j,
                            sta,
                            wd,
                            cur,
                            sst,
                            err,
                            depth,
                            volume,
                        };
                    }),
                );
            }
            const response = {
                title,
                name,
                latitude,
                longitude,
                volume,
                beginTime: new Date(...((() => { 
		    const arr = beginTime.split('. ');
		    const year = arr[0];
		    const month = parseInt(arr[1]) - 1;
		    const day = parseInt(arr[2]);
		    return [year, month, day]
		})() as [])),
                points: points,
            };

            memoizer.set(key, response);
            setTimeout(() => {
                memoizer.clear();
            }, 3600000);
        }

        return memoizer.get(key);
    }

    send(stream?: ServerHttp2Stream | ServerResponse, query?: any) {
        if (!stream) {
            throw new Error('No stream assigned to controller');
        }
        console.log(`[${new Date().toISOString()}] -`,query);
        const data = this.readFileData((query || {}).lat, (query || {}).lon, (query || {}).date);
        const response = JSON.stringify({ data: data || {} });
        console.log(`[${new Date().toISOString()}] -`, `Response Body length: ${response.length} Bytes`);
        return stream.end(response);
    }
}
