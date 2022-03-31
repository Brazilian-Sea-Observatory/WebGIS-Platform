const tileUrl = 'https://server.arcgisonline.com/ArcGIS/rest/services/';
const oneDay = 86400000;

export class MercatorLeafletUtils {
    public static overlaysDefaultValues = {
        FORMAT: 'image/png',
        NUMCOLORBANDS: 20,
        // TIME: date,
        COLORSCALERANGE: '-50,50', // "-2.029481,1.6440321",
        srs: 'EPSG:4326',
        styles: 'boxfill/rainbow',
        TRANSPARENT: true,
        ABOVEMAXCOLOR: '0x000000',
        BELOWMINCOLOR: '0x000000',
        attribution: 'Numerical Models: MERCATOR CMEMS GLOBAL OCEAN 1/12°',
        LOGSCALE: false,
    };

    public static getBaseLayers() {
        return [
            // {
            //     name: 'World Gray Canvas',
            //     // tslint:disable-next-line:max-line-length
            //     url: 'https://server.arcgisonline.com/ArcGIS/rest/
            // services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
            //     attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
            // },
            {
                name: 'World Imagery',
                visible: true,
                attribution:
                // tslint:disable-next-line:max-line-length
                'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
                url: `${tileUrl}World_Imagery/MapServer/tile/{z}/{y}/{x}`,
            },
            {
                name: 'World Imagery with labels',
                visible: true,
                attribution:
                    // tslint:disable-next-line:max-line-length
                    'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
                url: `${tileUrl}/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}`,
            },
        ];
    }

    public static getInterval() {
        const referenceDate = new Date();
        const startDate = new Date(+referenceDate - (referenceDate.getDay() + 6) * oneDay);
        const endDate = new Date();
        const addZero = (num: number) => (num < 10 ? `0${num}` : num);

        // tslint:disable-next-line:max-line-length
        const format = (date: Date) => `${date.getFullYear()}-${addZero(date.getUTCMonth() + 1)}-${addZero(date.getUTCDate())}`;
        return `${format(startDate)}T11:30:00.000Z/${format(endDate)}T11:30:00.000Z`;
    }

    public static getDates(): Date[] {
        const start = new Date(this.getInterval().split('/')[1]);
        const values = [];
        for (let i = 0; i < 7; i++) {
            values.push(new Date(start.getTime() - (oneDay * i)));
        }
        return values.reverse();
    }

    public static toLocaleString(date: Date) {
        // const months = [
        //     'Janeiro',
        //     'Fevereiro',
        //     'Março',
        //     'Abril',
        //     'Maio',
        //     'Junho',
        //     'Julho',
        //     'Agosto',
        //     'Setembro',
        //     'Outubro',
        //     'Novembro',
        //     'Dezembro',
        // ]

        const months = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December',
        ];

        return `${months[date.getMonth()]} ${date.getUTCDate()}, ${date.getFullYear()}`;
    }

    public static getDaysOfTheWeek() {
        const days = [
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
        ];

        return this.getDates().map((e: Date) => days[e.getDay()]);
    }
}
