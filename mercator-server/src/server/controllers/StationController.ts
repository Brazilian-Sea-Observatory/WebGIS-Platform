import { IRouteController } from '../modules/route';
import { ServerHttp2Stream } from 'http2';
import { ServerResponse } from 'http';
import { Client } from 'pg';

let memoizer: Map<string, any> = new Map();
const queryData = (code: Number, variable: Number) => {
    const initialDate = new Date();
    initialDate.setMonth(initialDate.getMonth() - 1)
    
    return `
        select
            d.id,
            d.code,
            d.time,
            d.value,
            d.variable_id,
            v.name as variable,
            ST_X(d.geom) as lon,
            ST_Y(d.geom) as lat
        from
            data d,
            variable v
        where
            d.code = '${code}'  
        and
            d.type = 'DB'
        and
            d.variable_id = ${variable}  
        and
            v.id = d.variable_id
        and
            d.time > '${initialDate.toISOString()}'
        and
            d.time < '${new Date().toISOString()}'
        ORDER BY d.time ASC
    `;
}

const queryGetAllToday = () => `
    SELECT DISTINCT ON (d.code)
        d.code,
        d.time,
        ST_X(d.geom) as lon,
        ST_Y(d.geom) as lat
    from
        data d 
    WHERE d.time >= NOW() - interval '48 hours' ORDER BY d.code, d.time DESC;
`;

export class StationController implements IRouteController {
    private getDataFromCode(code: Number, variable: Number) {
        const key = `code:${code}:${variable}:${new Date().toLocaleDateString()}`;
        const client = new Client({
            user: 'docker',
            host: 'localhost',
            database: 'gis',
            password: 'docker',
            port: 25434,
        });
        client.connect();
        return new Promise((resolve, reject) => {
            if (memoizer.get(key)) {
                resolve(memoizer.get(key));
                client.end();
                return;
            }
	    const q = queryData(code, variable);
	    console.log(q);
            client.query(
                q,
                (err, res) => {
                    if (err) {
                        reject(err.stack);
		    }
		   console.log(res);
		    if (!res){
		    	resolve([]);
			client.end();
		    	return; 
		    }
                    memoizer.set(key, res.rows);
                    resolve(res.rows);
                    client.end();
                },
            );
        });
    }

    private getLastPoints() {
        const key = `points:${new Date().toLocaleDateString()}`
        const client = new Client({
            user: 'docker',
            host: 'localhost',
            database: 'gis',
            password: 'docker',
            port: 25434,
        });
        client.connect();
        return new Promise((resolve, reject) => {
            if (memoizer.get(key)) {
                resolve(memoizer.get(key));
                client.end();
                return;
            }

            client.query(
                queryGetAllToday(),
                (err, res) => {
                    if (err) {
                        reject(err.stack);
                    }

                    memoizer.set(key, res.rows);
                    resolve(res.rows);                    
                    client.end();
                },
            );
        });
    }

    async send(stream?: ServerHttp2Stream | ServerResponse, query?: any) {
        if (!stream) {
            throw new Error('No stream assigned to controller');
        }
        console.log(`[${new Date().toISOString()}] -`,query);
        let data: any = {};
        if (query && query.code) {
            data = await this.getDataFromCode(query.code, query.variable || 2);
        } else {
            data = await this.getLastPoints();
        }  
        
        return stream.end(JSON.stringify(data));
        
    }
}
