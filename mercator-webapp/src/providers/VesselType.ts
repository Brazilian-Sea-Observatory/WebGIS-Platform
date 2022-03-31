import { IVessel } from './IVessel';

export class VesselType implements IVessel {
    public latitude: number;
    public longitude: number;
    public rotation: number;
    public name: string;
    public destination: string;
    public time: number | Date | string;
    public callsign: string;

    constructor(
        latitude: number,
        longitude: number,
        rotation: number,
        name: string,
        destination: string,
        callsign: string,
        time: string,
    ) {
        this.latitude = latitude;
        this.longitude = longitude;
        this.destination = destination;
        this.rotation = rotation;
        this.name = name;
        this.time = new Date(time);
        this.callsign = callsign;
    }
}
