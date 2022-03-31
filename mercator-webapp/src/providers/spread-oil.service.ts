import IOilType from './IOilType';
const ITEMS_KEY = 'oil:items';
export default class SpreadOilService {
    public static getInstance() {
        return this.instance;
    }

    private static readonly instance = new SpreadOilService();

    public getAll(lat: number, lon: number, date: string): Promise<IOilType> {
        // const lastTimestamp = localStorage.getItem('oil:timestamp');
        // if (
        //     lastTimestamp &&
        //     Date.now() - parseInt(lastTimestamp, 10) < 120000
        // ) {
        //     return Promise.resolve(JSON.parse(localStorage.getItem(
        //         ITEMS_KEY,
        //     ) as string) as IOilType);
        // }

        return fetch(`${process.env.VUE_APP_OIL_URL}?lat=${lat.toFixed(3)}&lon=${lon.toFixed(3)}&date=${date}`)
            .then((res: Response) => res.json())
            .then((res: { data: IOilType }) => {
                localStorage.setItem('oil:timestamp', Date.now().toString());
                localStorage.setItem(ITEMS_KEY, JSON.stringify(res.data));
                return res.data;
            });
    }
}
