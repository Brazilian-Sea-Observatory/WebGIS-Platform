import L from 'leaflet';

const url = process.env.VUE_APP_BASE_URL + '/mercator/wms';

export default class FeatureInfo {
    private map: any;

    constructor(map: L.Map | any) {
        this.map = map;
    }

    public getFeatureInfo(params: any, evt: any, time?: any) {
        const infoURL = this.getFeatureInfoUrl(params, evt.latlng, time);
        if (!infoURL) {
            return Promise.reject('info URL not found');
        }

        return fetch(infoURL).then((res) => res.json());
    }

    private getFeatureInfoUrl(
        wmsParams: any,
        latlng: [number, number],
        time?: any,
    ) {
        if (!this.map) {
            return;
        }

        const point = this.map.latLngToContainerPoint(
            latlng,
            this.map.getZoom(),
        );
        const size = this.map.getSize();

        const params: any = {
            request: 'GetFeatureInfo',
            service: 'WMS',
            srs: 'EPSG:4326',
            styles: wmsParams.styles,
            transparent: wmsParams.transparent,
            version: '1.1.1',
            format: wmsParams.format,
            bbox: this.map.getBounds().toBBoxString(),
            height: size.y,
            width: size.x,
            layers: wmsParams.layers,
            query_layers: wmsParams.layers,
            info_format: 'application/json',
            feature_count: 3000000,
            x: point.x,
            y: point.y,
        };

        if (time) {
            params.time = time;
        }

        // params[params.version === '1.3.0' ? 'i' : 'x'] = point.x;
        // params[params.version === '1.3.0' ? 'j' : 'y'] = point.y;

        return url + L.Util.getParamString(params, url, true);
    }
}
