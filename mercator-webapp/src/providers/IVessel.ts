export interface IVessel {
    latitude: number;
    longitude: number;
    rotation: number;
    name: string;
    callsign: string;
    destination: string;
    time: Date | number | string;
}
