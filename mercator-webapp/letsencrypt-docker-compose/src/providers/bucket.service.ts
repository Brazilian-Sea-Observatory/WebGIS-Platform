export default class BucketService {
    private bucket: Map<string, any>;
    private KEY = 'buckets-data';

    constructor() {
        const data = JSON.parse(sessionStorage.getItem(this.KEY) || '{}');
        const keys = Object.keys(data);
        const values = Object.values(data).map((e, index) => [keys[index], e]);
        this.bucket = new Map(values as []);
    }

    public save(key: string, value: any) {
        this.bucket.set(key, value);
        const data = JSON.parse(sessionStorage.getItem(this.KEY) || '{}');
        data[key] = value;
        sessionStorage.setItem(this.KEY, JSON.stringify(data));
    }

    public getValue(key: string) {
        return this.bucket.get(key);
    }

    public clearData() {
        sessionStorage.clear();
        this.bucket = new Map();
    }
}
