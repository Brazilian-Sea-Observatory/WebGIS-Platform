import * as L from 'leaflet';

const baseURI = process.env.VUE_APP_BASE_URL;
const basePath = `${baseURI}/ows?`;
const baseLayer = {
    layers: 'mercator:height_test',
    styles: 'height_surface_normalize',
    transparent: true,
    format: 'image/png',
    crs: L.CRS.EPSG4326,
    uppercase: true,
    crossOrigin: true,
    tiled: true,
    attribution: '',
};

const partialShapeFileURL =
    // tslint:disable-next-line:max-line-length
    'regional_model/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=regional_model%3Ashp-file-regional&maxFeatures=50&outputFormat=application%2Fjson';
export async function getShapeFile() {
    if (!!localStorage.geoJSONData) {
        return Promise.resolve(JSON.parse(localStorage.geoJSONData));
    }

    const res = await fetch(`${baseURI}/${partialShapeFileURL}`);
    const json = await res.json();
    localStorage.setItem('geoJSONData', JSON.stringify(json));
    return json;
}

const modelPrScURL =
    // tslint:disable-next-line:max-line-length
    'regional_model/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=regional_model%3Ashp-file-regional-prsc&outputFormat=application%2Fjson';

export async function getGeoJSONPrSc() {
    if (!!localStorage.geoJSONPrSc) {
        return Promise.resolve(JSON.parse(localStorage.geoJSONPrSc));
    }

    const res = await fetch(`${baseURI}/${modelPrScURL}`);
    const json = await res.json();
    localStorage.setItem('geoJSONPrSc', JSON.stringify(json));
    return json;
}

export function getIndexPlatforms() {
    const date = new Date();
    date.setHours(date.getHours() - 3);
    date.setMinutes(0);
    date.setSeconds(0);
    return {
        path: basePath,
        opts: Object.assign({}, baseLayer, {
            // layers: 'mercator:bouy_info',
            layers: 'mercator:last_position_station',
            styles: '',
        }),
    };
}

export function getOceanVectors() {
    const vectors = new Map();
    vectors.set('global', {
        path: basePath,
        opts: Object.assign({}, baseLayer, {
            layers: 'mercator:water_vectorial_forecast_daily',
            tiled: 'False',
            format: 'image/png',
            styles: 'water_vectorial_directions_global',
        }),
    });

    vectors.set('babitonga', {
        path: basePath,
        opts: Object.assign({}, baseLayer, {
            layers: 'regional_model:water_vectorial_hydrodinamic_babitonga_hourly',
            tiled: 'False',
            format: 'image/png',
            styles: 'water_vectorial_directions_babitonga_cep',
        }),
    });

    vectors.set('cep', {
        path: basePath,
        opts: Object.assign({}, baseLayer, {
            layers: 'regional_model:water_vectorial_hydrodinamic_cep_hourly',
            tiled: 'False',
            format: 'image/png',
            styles: 'water_vectorial_directions_babitonga_cep',
        }),
    });

    vectors.set('regional', {
        path: basePath,
        opts: Object.assign({}, baseLayer, {
            layers: 'regional_model:water_vectorial_hydrodinamic_hourly',
            tiled: 'False',
            format: 'image/png',
            styles: 'water_vectorial_directions_regional',
        }),
    });

    vectors.set('coast', {
        path: basePath,
        opts: Object.assign({}, baseLayer, {
            layers: 'regional_model:water_vectorial_hydrodinamic_prsc_hourly',
            tiled: 'False',
            format: 'image/png',
            styles: 'water_vectorial_directions_prsc',
        }),
    });

    return vectors;
}

const babitongaUrl =
    // tslint:disable-next-line:max-line-length
    'regional_model/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=regional_model%3Ashp-file-regional-babitonga&maxFeatures=50&outputFormat=application%2Fjson';

export async function getGeoJSONBabitonga() {
    if (!!localStorage.babitongaGeoJSON) {
        return Promise.resolve(JSON.parse(localStorage.babitongaGeoJSON));
    }

    const res = await fetch(`${baseURI}/${babitongaUrl}`);
    const json = await res.json();
    localStorage.setItem('babitongaGeoJSON', JSON.stringify(json));
    return json;
}

const cepUrl =
    // tslint:disable-next-line:max-line-length
    'regional_model/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=regional_model%3Ashp-file-regional-cep&maxFeatures=50&outputFormat=application%2Fjson';

export async function getGeoJSONcep() {
    if (!!localStorage.cepGeoJSON) {
        return Promise.resolve(JSON.parse(localStorage.cepGeoJSON));
    }

    const res = await fetch(`${baseURI}/${cepUrl}`);
    const json = await res.json();
    localStorage.setItem('cepGeoJSON', JSON.stringify(json));
    return json;
}

const brazilURL =
    // tslint:disable-next-line:max-line-length
    'mercator/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=mercator%3Ashp-file-brazil&maxFeatures=50&outputFormat=application%2Fjson';

export async function getGeoJSONBrazil() {
    if (!!localStorage.brazilGeoJSON) {
        return Promise.resolve(JSON.parse(localStorage.brazilGeoJSON));
    }

    const res = await fetch(`${baseURI}/${brazilURL}`);
    const json = await res.json();
    localStorage.setItem('brazilGeoJSON', JSON.stringify(json));
    return json;
}

export async function getAllLayers() {
    const res = await fetch(`${process.env.VUE_APP_BACKEND_URL}/layers`);
    const data = await res.json();
    return data
        .filter((layer: any) => layer.isenable)
        .sort((a: any, b: any) => parseInt(a.tag, 10) - parseInt(b.tag, 10))
        .map((layer: any) => {
            const { layers, styles, attribution } = layer;
            layer.layer = {
                path: basePath,
                opts: Object.assign({}, baseLayer, {
                    layers,
                    styles,
                    attribution,
                }),
            };
            return layer;
        });
}
