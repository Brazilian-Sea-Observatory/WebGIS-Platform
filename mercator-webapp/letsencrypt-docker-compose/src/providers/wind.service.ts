const windLayerOptions = (data: any) => ({
    displayValues: true,
    displayOptions: {
        velocityType: 'Wind Velocity',
        position: 'bottomleft',
        emptyString: 'No data',
        angleConvention: 'bearingCW',
        displayPosition: 'bottomleft',
        displayEmptyString: 'No data',
    },
    visible: false,
    data,
    minVelocity: 0.01, // used to align color scale
    maxVelocity: 0.9, // used to align color scale
    velocityScale: 0.2, // modifier for particle animations, arbitrarily defaults to 0.005
});

const windMap = new Map();

export default abstract class WindService {
    public static getVelocityLayerMetadata(date?: string, model?: string) {
        const key = `wind-data-${model}:${date}`;
        const values = windMap.get(key);
        if (values) {
            return Promise.resolve(windLayerOptions(values));
        }

        const paths = new Map([
            ['regional', 'regional'],
            ['coast', 'pr_sc'],
            ['cep', 'cep'],
            ['babitonga', 'babitonga'],
        ]);
        // const path = model === 'global' ? '' : `&path=${paths.get(model || 'regional')}`;
        const path = '';

        return fetch(
            `${process.env.VUE_APP_SERVER_URL}/api/wind?date=${date || new Date().toISOString().substr(0, 10)}${path}`,
        {
            mode: 'cors',
            headers: {
                'Access-Control-Allow-Origin': '*',
            },
        })
            .then((res: Response) => res.json())
            .then((data: any) => {
                windMap.set(key, data.data);
                return windLayerOptions(data.data);
            });
    }

    public static async getAvailableDates() {
        // const values = sessionStorage.getItem('wind-dates');
        // if (values) {
        //     return JSON.parse(values);
        // }

        const res = await fetch(`${process.env.VUE_APP_SERVER_URL}/api/wind/available-dates`,
            {
                mode: 'cors',
                headers: {
                    'Access-Control-Allow-Origin': '*',
                },
            },
        );

        const data = await res.json();
        const today = new Date();
        today.setDate(today.getDate() - 1);
        const response = data.data.filter((date: any) => +new Date(date) >= +today);

        sessionStorage.setItem('wind-dates', JSON.stringify(response));
        return response;
    }
}
