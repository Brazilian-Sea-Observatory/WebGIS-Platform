import { VesselType } from './VesselType';

const VESSELS_ITEMS = 'vessels:items';
export default class VesselsService {
    public static getInstance() {
        return this.instance;
    }

    private static readonly instance = new VesselsService();

    public getAll(): Promise<VesselType[]> {
        const lastTimestamp = sessionStorage.getItem('vessel:timestamp');
        if (
            lastTimestamp &&
            Date.now() - parseInt(lastTimestamp, 10) < 120000
        ) {
            return Promise.resolve(JSON.parse(sessionStorage.getItem(
                VESSELS_ITEMS,
            ) as string) as VesselType[]);
        }

        sessionStorage.setItem('vessel:timestamp', Date.now().toString());
        return fetch(process.env.VUE_APP_VESSELS_URL)
            .then((res: Response) => res.json())
            .then((res: any) => {
                const { data } = res;
                const response = this.processReqBody(data).map((vessel: Element) =>
                    this.parser(vessel),
                );
                sessionStorage.setItem(VESSELS_ITEMS, JSON.stringify(response));
                return response;
            })
            .catch(() => {
                const customPayload = `
                    <?xml version="1.0" encoding="iso-8859-1"?>
                    <VESSELS>
                        <vessel
                            MMSI="264162572"
                            TIME="2011-04-12 10:50:11 GMT"
                            LONGITUDE="-48.068053"
                            LATITUDE="-25.843775"
                            COG="237.4"
                            SOG="6.6"
                            HEADING="511"
                            NAVSTAT="5"
                            IMO="0"
                            NAME="SULINA1"
                            CALLSIGN="YP2572"
                            TYPE="70"
                            A="68"  B="12"  C="6"  D="2"
                            DRAUGHT="2.4"  DEST="ROTTERDAM"  ETA="03-15 10:00" />
                        <vessel
                            MMSI="244670509"
                            TIME="2011-04-12 10:44:54 GMT"
                            LONGITUDE="-48.353573"
                            LATITUDE="-26.238613"
                            COG="117"  SOG="5.6"
                            HEADING="511"  NAVSTAT="15"
                            IMO="0"
                            NAME="VALENCIA"
                            CALLSIGN="PD2667"
                            TYPE="79"
                            A="74"  B="11"  C="0"  D="10"
                            DRAUGHT="1.4"
                            DEST=""
                            ETA="01-16 13:10" />
                        <vessel
                            MMSI="366993070"
                            TIME="2011-04-12 10:50:27 GMT"
                            LONGITUDE="-26.828360
                            LATITUDE="-44.201759"
                            COG="353.5"  SOG="0"
                            HEADING="511"  NAVSTAT="0"
                            IMO="0"
                            NAME="KOOLCAT"
                            CALLSIGN="WDC2431"
                            TYPE="31"
                            A="3"  B="24"  C="5"  D="2"
                            DRAUGHT="15.5"  DEST="WORKING GNOTS FLEET"  ETA="09-01 00:00" />
                        <vessel
                            MMSI="211177720"
                            TIME="2011-04-12 10:50:26 GMT"
                            LONGITUDE="-26.140029"
                            LATITUDE="-45.498376"
                            COG="0"  SOG="0"
                            HEADING="511"  NAVSTAT="0"
                            IMO="0"
                            NAME="DETTMER TANK 83"
                            CALLSIGN="DB4027"
                            TYPE="80"
                            A="64"  B="16"  C="6"  D="3"
                            DRAUGHT="0"  DEST="" ETA="00-00 24:60" />
                        <vessel
                            MMSI="246538000"
                            TIME="2011-04-12 10:50:24 GMT"
                            LONGITUDE="-41.413249"
                            LATITUDE="-29.386363"
                            COG="263.2"  SOG="0"
                            HEADING="511"  NAVSTAT="0"
                            IMO="7700180"
                            NAME="SIRIUS"
                            CALLSIGN="PBRW"
                            TYPE="52"
                            A="6"  B="20"  C="3"  D="5"
                            DRAUGHT="4.8"  DEST="IJMUIDEN"  ETA="12-31 00:00" />
                        <vessel
                            MMSI="211506060"
                            TIME="2011-04-12 10:50:00 GMT"
                            LONGITUDE="-40.622128"
                            LATITUDE="-23.930406"
                            COG="296.2"  SOG="7"
                            HEADING="511"  NAVSTAT="5"
                            IMO="0"
                            NAME="BERLENA"
                            CALLSIGN="DA4565"
                            TYPE="79"
                            A="70"  B="15"  C="3"  D="7"
                            DRAUGHT="0"  DEST="ROTTERDAM"  ETA="00-00 24:60" />
                    </VESSELS>
                `;
                const response = this.processReqBody(customPayload).map(
                    (vessel: Element) => this.parser(vessel),
                );
                sessionStorage.setItem(VESSELS_ITEMS, JSON.stringify(response));
                return response;
            });
    }

    private processReqBody(payload: string): Element[] {
        const div = document.createElement('div');
        div.innerHTML = payload;
        return [...div.querySelectorAll('vessel')];
    }

    private parser(data: Element): VesselType {
        const latitude = parseFloat(data.getAttribute('LATITUDE') as string);
        const longitude = parseFloat(data.getAttribute('LONGITUDE') as string);
        const rotation = parseInt(data.getAttribute('COG') as string, 10);
        const name = data.getAttribute('NAME') as string;
        const time = data.getAttribute('TIME') as string;
        const destination = data.getAttribute('DEST') as string;
        const callsign = data.getAttribute('CALLSIGN') as string;

        return new VesselType(
            latitude,
            longitude,
            rotation,
            name,
            destination,
            callsign,
            time,
        );
    }
}
