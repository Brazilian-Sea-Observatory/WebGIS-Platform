import IPointType from './IPointType';

export default interface IOilType {
    title: string;
    name: string;
    latitude: number | string;
    longitude: number | string;
    volume: number | string;
    beginTime: number | string;
    points: IPointType[][];
}
