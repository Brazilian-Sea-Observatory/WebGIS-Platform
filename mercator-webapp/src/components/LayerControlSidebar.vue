<template>
    <section>
        <v-btn
            class="map-control"
            color="primary"
            fab
            light
            @click="isOpen = true"
            v-if="isLayersVisible"
        >
            <v-icon>layers</v-icon>
        </v-btn>
        <div v-bind:class="{ open: isOpen }" class="panel">
            <header>
                <span @click="isOpen = false">
                    <v-icon medium color="white">close</v-icon>
                </span>
            </header>
            <main>
                <h2>Modelo</h2>
                <section>
                    <v-select
                        v-model="layerModel"
                        :items="layerModels"
                        item-text="text"
                        item-value="value"
                        label="Selecione um modelo"
                        solo
                        v-on:change="onChangeModel()"
                    ></v-select>
                </section>

                <h2>{{ $t('map.layerControl.layer') }}</h2>
                <section>
                    <v-select
                        v-model="layer"
                        :items="layersFiltered"
                        :item-text="item => $t(item.name)"
                        item-value="name"
                        label="Select a layer"
                        solo
                        v-on:change="setGlobalLayer()"
                    ></v-select>
                </section>

                <section v-if="isRegionalLayer">
                    <v-btn @click="setGlobalLayer()" flat color="error">
                        <small>
                            <b>x</b>
                        </small>
                        &nbsp;&nbsp;
                        {{ $t('map.layerControl.disableRegional') }}
                    </v-btn>
                </section>

                <section v-if="mapModel === 'coast'">
                    <v-btn @click="setGlobalLayer()" flat color="error">
                        <small>
                            <b>x</b>
                        </small>
                        &nbsp;&nbsp; {{ $t('map.layerControl.disableCoast') }}
                    </v-btn>
                </section>

                <section v-if="mapModel === 'cep'">
                    <v-btn @click="setGlobalLayer()" flat color="error">
                        <small>
                            <b>x</b>
                        </small>
                        &nbsp;&nbsp; {{ $t('map.layerControl.disableCEP') }}
                    </v-btn>
                </section>

                <section v-if="mapModel === 'babitonga'">
                    <v-btn @click="setGlobalLayer()" flat color="error">
                        <small>
                            <b>x</b>
                        </small>
                        &nbsp;&nbsp;
                        {{ $t('map.layerControl.disableBabitonga') }}
                    </v-btn>
                </section>
            </main>
        </div>

        <div
            style="position: fixed;bottom: 26.2rem;left: 1rem;z-index: 999; padding: 0 1rem; display: flex; align-items: center; flex-direction: row;"
        >
            <input
                v-model="isLayersVisible"
                class="wind-toggle-cb"
                type="checkbox"
                name="is-layer-visible-toggle"
                id="is-layer-visible-toggle"
                @change="toggleBaseLayer()"
                hidden
            />
            <label
                for="is-layer-visible-toggle"
                class="wind-toggle"
                :value="$t('map.layerControl.disableLayer')"
                v-if="isLayersVisible"
            >
                <v-icon>visibility_off</v-icon>
            </label>
            <label
                for="is-layer-visible-toggle"
                class="wind-toggle"
                :value="$t('map.layerControl.enableLayer')"
                v-if="!isLayersVisible"
            >
                <v-icon>remove_red_eye</v-icon>
            </label>
        </div>

        <div
            style="position: fixed;bottom: 22.2rem;left: 1rem;z-index: 999; padding: 0 1rem; display: flex; align-items: center; flex-direction: row;"
        >
            <input
                v-model="spreadOilToggler"
                class="wind-toggle-cb"
                type="checkbox"
                name="spreadOil-toggle"
                id="spreadOil-toggle"
                @change="toggleArea()"
                hidden
            />
            <label
                for="spreadOil-toggle"
                class="wind-toggle"
                :value="$t('map.layerControl.oilSpill')"
            >
                <v-icon>invert_colors</v-icon>
            </label>
            <select
                v-if="spreadOilToggler && oilSpilDateShown"
                class="v-btn v-btn--small theme--light mercator-color"
                style="border-radius: 10px"
                name="spread-oil-date"
                id="spread-oil-date"
                v-model="spreadOilSelectedDateFormatted"
                disabled
            >
                <option
                    v-for="item in spreadOilDates"
                    :key="item"
                    :value="item"
                    >{{ item }}</option
                >
            </select>
        </div>

        <div
            style="position: fixed;bottom: 18.2rem;left: 1rem;z-index: 999; padding: 0 1rem; display: flex; align-items: center; flex-direction: row;"
        >
            <input
                type="checkbox"
                v-model="stationsToggler"
                :label="$t('map.layerControl.overlays.sensor')"
                @change="onChangeMonitorStation()"
                name="station-toggle"
                class="wind-toggle-cb"
                id="station-toggle"
                hidden
            />
            <label
                for="station-toggle"
                class="wind-toggle"
                :value="$t('map.layerControl.monitorStation')"
            >
                <v-icon>room</v-icon>
            </label>
        </div>

        <div
            style="position: fixed;bottom: 14.2rem;left: 1rem;z-index: 999; padding: 0 1rem; display: flex; align-items: center; flex-direction: row;"
        >
            <input
                v-model="vesselToggler"
                class="wind-toggle-cb"
                type="checkbox"
                name="vessel-toggle"
                id="vessel-toggle"
                @change="toggleVesselLayer()"
                hidden
            />
            <label
                for="vessel-toggle"
                class="wind-toggle"
                alt="Posição dos Navios"
                :value="$t('map.layerControl.vesselLocation')"
            >
                <v-icon>directions_boat</v-icon>
            </label>
        </div>

        <div
            style="position: fixed;bottom: 10.2rem;left: 1rem;z-index: 999; padding: 0 1rem; display: flex; align-items: center; flex-direction: row;"
        >
            <input
                class="wind-toggle-cb"
                v-model="windToggler"
                @change="toggleVelocityLayer()"
                type="checkbox"
                name="wind-toggle"
                id="wind-toggle"
                hidden
            />
            <label
                for="wind-toggle"
                class="wind-toggle"
                :value="$t('map.layerControl.layers.water_speed')"
            >
                <v-icon>waves</v-icon>
            </label>
            <select
                v-if="windToggler && windType === 'streams'"
                class="v-btn v-btn--small theme--light mercator-color"
                style="border-radius: 10px; display: none !important;"
                name="wind-date"
                id="wind-date"
                @change="onChangeDateSelection($event.target.value)"
            >
                <option v-for="item in windDates" :key="item" :value="item">{{
                    formatDate(item)
                }}</option>
            </select>
            <select
                v-if="windToggler"
                class="v-btn v-btn--small theme--light mercator-color"
                style="border-radius: 10px"
                name="wind-type"
                id="wind-type"
                v-model="windType"
                @change="onChangeWindType()"
            >
                <option value="vectors">{{
                    $t('map.layerControl.water_control.vectors')
                }}</option>
                <option value="streams">{{
                    $t('map.layerControl.water_control.streams')
                }}</option>                
            </select>
        </div>

        <select
            class="v-btn v-btn--left v-btn--small theme--light mercator-color"
            style="position: fixed;bottom: 7.2rem;left: 1rem;z-index: 999; border-radius: 10px; padding: 0 1rem;"
            id="map-models"
            name="map-models"
            v-if="isLayersVisible"
            v-model="mapModel"
            @change="store.dispatch('setMapModel', mapModel)"
            disabled
        >
            <option value="global">{{
                $t('map.layerControl.scope.global')
            }}</option>
            <option value="regional">{{
                $t('map.layerControl.scope.regional')
            }}</option>
            <option value="coast">{{
                $t('map.layerControl.scope.coast')
            }}</option>
            <option value="babitonga">{{
                $t('map.layerControl.scope.babitonga')
            }}</option>
            <option value="cep">{{ $t('map.layerControl.scope.cep') }}</option>
        </select>

        <DataVisualizationSidebar
            @close="close"
            v-bind:isOpen="isSidebarOpen"
            v-bind:vessel="selectedVessel"
        ></DataVisualizationSidebar>

        <v-dialog v-model="dialog" max-width="500">
            <v-card>
                <v-card-title class="headline">{{
                    $t('dialogTitle')
                }}</v-card-title>

                <v-card-text>
                    <div style="
                        width: 100%;
                        display: flex;
                        flex-direction: column;
                        justify-content: flex-start;
                    ">
                         <input
                            v-model="oilSpillDate"
                            type="date"
                            name="date"
                            id="date"
                            style="
                                width:80%;
                                padding: .5rem;
                                height: 3rem;
                            "
                        />
                        <b style="width:80%; padding: .5rem;"> {{ $t('endDateSimulation') }}: {{ oilSpillEndDate }}</b>
                    </div>                   
                </v-card-text>               

                <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn
                        color="red darken-1"
                        style="color: white;"
                        text
                        @click="dialog = false"
                    >
                        {{ $t('cancel') }}
                    </v-btn>

                    <v-btn
                        color="v-btn theme--light mercator-color"
                        text
                        @click="startSimulation()"
                    >
                        {{ $t('simulate') }}
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </section>
</template>

<script lang="ts">
import { Component, Vue, Prop, Emit, Watch } from 'vue-property-decorator';
import * as L from 'leaflet';
import 'leaflet-velocity';
import FeatureInfo from '../providers/feature-info.service';
import {
    getShapeFile,
    getGeoJSONPrSc,
    getGeoJSONcep,
    getGeoJSONBabitonga,
    getOceanVectors,
    getGeoJSONBrazil,
} from '../providers/layers.service';
import WindService from '../providers/wind.service';
import DataVisualizationSidebar from '@/components/DataVisualizationSidebar.vue';
import VesselsService from '../providers/vessels.service';
import { VesselType } from '../providers/VesselType';
import SpreadOilService from '../providers/spread-oil.service';
import IOilType from '../providers/IOilType';
import IPointType from '../providers/IPointType';
import { TMPT_LOADER, TMPT_LOADER_MESSAGE } from '../utils/MapTemplates';

const baseURI = process.env.VUE_APP_BASE_URL;
const basePath = `${baseURI}/ows?`;
const oceanVectorsOptions = getOceanVectors();

@Component({
    components: {
        DataVisualizationSidebar,
    },
})
export default class LayerControlSidebar extends Vue {
    @Prop() public overlays!: any[];
    @Prop() public map!: any;

    public layerModel = 'forecast';

    public isRegionalLayer = false;
    public isCoastLayer = false;
    public isCepLayer = false;
    public isBabitongaLayer = false;

    public mapModel = 'global';

    public isOpen = false;
    public overlay = true;
    public layer = '';
    public satelliteLayers: any[] = [];
    public forecastLayers: any[] = [];
    public regionalLayer: any[] = [];

    public layers: any[] = [];
    public layerId = 0;

    public velocityLayer: any;
    public vectorsLayer: any;

    public stationsToggler = false;
    public stationsLayer: any;

    public windType = 'vectors';
    public windToggler = false;
    public windDates = [];

    public vesselLayer: any;
    public oilLayer: any;
    public vesselToggler = false;
    public selectedVessel: VesselType = new VesselType(0, 0, 0, '', '', '', '');
    public isSidebarOpen = false;

    public spreadOilToggler = false;
    public spreadOilDates: any[] = [];
    public spreadOilSelectedDate = [];

    public oilSpillTimeouts: any[] = [];
    public oilToolclickableArea: any;
    public oilSpilDateShown = false;
    public isLayersVisible = true;
    public dialog = false;
    public oilSpillDate = new Date(
        new Date().setHours(new Date().getHours() - 3),
    )
        .toISOString()
        .substr(0, 10);
    public oilSpillSelectedPoint: any = null;

    private getInfo: FeatureInfo = {} as FeatureInfo;
    private mapEvent: any;
    private shapeFileLayer: any;
    private geoJSONPrScLayer: any;
    private babitongaLayer: any;
    private cepLayer: any;

    public get layerMetadata() {
        const layer = this.layers.find((e: any) => e.name === this.layer);
        this.layerId = layer.id;
        const data = layer.layer.wmsParams.layers;
        return data;
    }

    public get selectedLayer() {
        return this.layer;
    }

    public get oilSpillEndDate() {
        try {
            const date = new Date(this.oilSpillDate + 'T00:00');
            date.setDate(date.getDate() + 2);
            return new Intl.DateTimeFormat('pt-BR').format(date);
        } catch (err) {
            return '-';
        }
    }

    public get spreadOilSelectedDateFormatted() {
        return this.spreadOilSelectedDate;
    }

    public get layersFiltered() {
        const layers = this.layers
            .filter((e: any) => !e.isRegional)
            .filter((e: any) => e.category === this.layerModel);
        return layers;
    }

    private get oldIndex() {
        return this.layers.findIndex((e: any) => e.id === this.layerId);
    }

    public close() {
        this.isSidebarOpen = false;
    }

    public addLoader(value: string) {
        const spinControl = new L.Control({
            position: 'topleft',
        });

        spinControl.onAdd = map => {
            const div = L.DomUtil.create('div');
            div.innerHTML = TMPT_LOADER_MESSAGE(value);
            return div;
        };
        spinControl.addTo(this.map);
        return () => {
            this.map.removeControl(spinControl);
        };
    }

    public onChangeMonitorStation() {
        if (this.stationsLayer) {
            this.map.removeLayer(this.stationsLayer);
            this.stationsLayer = null;
            return;
        }

        const finishLoader = this.addLoader(this.$t(
            'loadMonitorStation',
        ) as string);
        const getValuesFromStation = (code: any) => (variable: any) =>
            fetch(
                `${
                    process.env.VUE_APP_STATIONS_URL
                }?code=${code}&variable=${variable}`,
            ).then((res: Response) => res.json());

        fetch(process.env.VUE_APP_STATIONS_URL)
            .then((res: Response) => res.json())
            .then((res: any) => {
                this.stationsLayer = L.layerGroup(
                    res.map(
                        (station: {
                            code: string;
                            time: string;
                            lat: number;
                            lon: number;
                        }) =>
                            L.marker([station.lat, station.lon], {
                                icon: L.icon({
                                    iconUrl: '/img/marker-red.png',
                                    iconSize: [24, 24],
                                }),
                            }).on('click', (evt: any) => {
                                const finishLoader2 = this.addLoader(this.$t(
                                    'loading',
                                ) as string);
                                const getter = getValuesFromStation(
                                    station.code,
                                );
                                Promise.all([
                                    getter(2),
                                    getter(1),
                                    getter(109),
                                ]).then(([temperature, depth, salinity]) => {
                                    // this.$store.dispatch('setStationData', { metadata: station, values: res.filter((data: any) => data.variable === 'TEMP') });
                                    this.$store.dispatch('setStationData', {
                                        metadata: station,
                                        values: {
                                            temperature,
                                            depth,
                                            salinity,
                                        },
                                    });
                                    finishLoader2();
                                });
                            }),
                    ),
                ).addTo(this.map);
                finishLoader();
            });
    }

    public toggleVesselLayer() {
        const getRandomColor = () => {
            const letters = '0123456789ABCDEF';
            let color = '#';
            for (let i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        };

        if (this.vesselLayer) {
            this.map.removeLayer(this.vesselLayer);
            this.vesselLayer = null;
            return;
        }
        VesselsService.getInstance()
            .getAll()
            .then((res: VesselType[]) => {
                this.vesselLayer = L.layerGroup(
                    res
                        .filter(
                            (vessel: VesselType) =>
                                !isNaN(vessel.latitude) &&
                                !isNaN(vessel.longitude),
                        )
                        .map((vessel: VesselType) =>
                            L.marker([vessel.latitude, vessel.longitude], {
                                icon: L.divIcon({
                                    html: `
                                        <img style="width: 40px;transform: rotate(${
                                            vessel.rotation
                                        }deg);" src="/img/navigation-3.png" />
                                    `,
                                    popupAnchor: [15, 20],
                                    // icon: L.divIcon({
                                    //     html: `
                                    //     <div style="color: ${getRandomColor()}; transform: rotate(${vessel.rotation}deg);">
                                    //         <svg style="fill:currentColor;" aria-hidden="true">
                                    //             <use xlink:href="#vessel-icon"></use>
                                    //         </svg>
                                    //     </div>
                                    // `,
                                    // iconSize: [16, 16],
                                    // iconAnchor: [16, 46],
                                    // popupAnchor: [0, 16],
                                }),
                            })
                                .on('click', (evt: any) => {
                                    this.selectedVessel = vessel;
                                    this.isSidebarOpen = true;
                                    this.$store.dispatch('setVesselView');
                                })
                                .bindPopup(vessel.name || '-'),
                        ),
                ).addTo(this.map);
            });
    }

    public cleanOilSimulation() {
        this.oilSpillTimeouts.forEach(timeout => clearTimeout(timeout));
        if (this.oilLayer) {
            this.map.removeLayer(this.oilLayer);
            this.oilLayer = null;
        }
    }

    public toggleArea() {
        if (this.spreadOilToggler) {
            this.map.addLayer(this.oilToolclickableArea);
            return;
        }

        this.map.removeLayer(this.oilToolclickableArea);
        this.cleanOilSimulation();
    }

    public toggleSpreadOilLayer(latlng: any) {
        this.cleanOilSimulation();

        const spinControl = new L.Control({
            position: 'topleft',
        });

        spinControl.onAdd = map => {
            const div = L.DomUtil.create('div');
            div.innerHTML = TMPT_LOADER_MESSAGE(this.$t(
                'loadSimulation',
            ) as string);
            return div;
        };
        spinControl.addTo(this.map);
        SpreadOilService.getInstance()
            .getAll(
                latlng.lat as number,
                latlng.lng as number,
                this.oilSpillDate,
            )
            .then((data: IOilType) => {
                this.map.removeControl(spinControl);
                this.oilSpilDateShown = true;
                this.oilLayer = L.layerGroup().addTo(this.map);

                const beginTime = +new Date(data.beginTime) as number;
                const options = {
                    year: 'numeric',
                    month: 'numeric',
                    day: 'numeric',
                    hour: 'numeric',
                    minute: 'numeric',
                    second: 'numeric',
                    hour12: false,
                    timeZone: 'America/Sao_Paulo',
                } as const;
                const formatter = new Intl.DateTimeFormat('pt-BR', options);
                this.spreadOilDates = data.points.map(
                    (point: IPointType[], index: number) => {
                        const date = new Date(beginTime);
                        date.setHours(date.getHours() + index);
                        return formatter.format(date);
                    },
                );
                this.spreadOilSelectedDate = this.spreadOilDates[0];

                data.points.forEach((point: IPointType[], offset: number) => {
                    const circles = point
                        .filter(
                            (point: IPointType) => !!point.lat && !!point.lon,
                        )
                        .map((point: IPointType) =>
                            L.circle(
                                [point.lat as number, point.lon as number],
                                {
                                    color: `#5e5e5e`,
                                    fillColor: `#5e5e5e`,
                                    fillOpacity: 0.5,
                                    radius: 500,
                                },
                            ),
                        );
                    const timeout = setTimeout(() => {
                        this.map.removeLayer(this.oilLayer);
                        this.oilLayer = L.layerGroup().addTo(this.map);
                        this.spreadOilSelectedDate = this.spreadOilDates[
                            offset
                        ];
                        circles.map((circle: L.Circle, index: number) => {
                            this.oilLayer.addLayer(circle);
                        });
                    }, 300 * offset);

                    this.oilSpillTimeouts.push(timeout);
                });
            });
    }

    public toggleVelocityLayer() {
        if (!this.vectorsLayer) {
            this.windType = 'vectors';
            const options = {
                year: 'numeric',
                month: 'numeric',
                day: 'numeric',
            } as const;
            const formatter = new Intl.DateTimeFormat('pt-BR', options);
            this.vectorsLayer = L.tileLayer.wms(
                oceanVectorsOptions.get(this.mapModel).path,
                oceanVectorsOptions.get(this.mapModel).opts,
            );
            this.map.addLayer(this.vectorsLayer);
            this.onChangeDateSelection(formatter.format(new Date()));

            return;
        }

        if (this.velocityLayer) {
            this.map.removeLayer(this.velocityLayer);
            this.velocityLayer = null;
        }

        if (this.vectorsLayer) {
            this.map.removeLayer(this.vectorsLayer);
            this.vectorsLayer = null;
        }
    }

    public onChangeDateSelection(date: string, hour?: any) {
        const [day, month, year] = date
            .split('/')
            .map((e: string) => parseInt(e, 10));
        if (this.windType === 'vectors') {
            if (!this.vectorsLayer) {
                return;
            }
            this.map.removeLayer(this.vectorsLayer);
            this.vectorsLayer = L.tileLayer.wms(
                oceanVectorsOptions.get(this.mapModel).path,
                oceanVectorsOptions.get(this.mapModel).opts,
            );
            this.map.addLayer(this.vectorsLayer);

            if (!hour) {
                this.vectorsLayer.setParams({
                    time: new Date(year, month - 1, day, 9, 0, 0).toISOString(),
                });
            } else {
                const [hh, mm] = hour
                    .split(':')
                    .map((e: string) => parseInt(e, 10));
                this.vectorsLayer.setParams({
                    time: new Date(
                        year,
                        month - 1,
                        day,
                        hh,
                        mm,
                        0,
                    ).toISOString(),
                });
            }
            this.vectorsLayer.bringToFront();
            return;
        }
        const addZero = (num: number) => (num < 10 ? `0${num}` : num);
        WindService.getVelocityLayerMetadata(
            `${year}-${addZero(month)}-${addZero(day)}`,
            this.mapModel,
        ).then((data: any) => {
            try {
                if (this.velocityLayer) {
                    this.map.removeLayer(this.velocityLayer);
                }

                this.velocityLayer = (L as any).velocityLayer(data);
                this.map.addLayer(this.velocityLayer);
            } catch (err) {
                console.warn(
                    'could not animate velocity layer. Reason: Date not Found',
                );
            }
        });
    }

    public get layerModels() {
        return [
            { text: this.$t('map.layerControl.forecast'), value: 'forecast' },
            { text: this.$t('map.layerControl.satellite'), value: 'satellite' },
        ];
    }

    public formatDate(date: string) {
        const [year, month, day] = date.split('-');
        return `${day}/${month}/${year}`;
    }

    public setGlobalLayer() {
        if (this.windToggler) {
            this.toggleVelocityLayer();
            this.windToggler = false;
        }

        switch (this.mapModel) {
            case 'cep':
                setTimeout(() => {
                    this.createCepBabitongaEvent('cep')(null);
                }, 100);
            case 'babitonga':
                setTimeout(() => {
                    this.createCepBabitongaEvent('babitonga')(null);
                }, 200);
            case 'coast':
                setTimeout(() => {
                    this.createCoastEvent()(null);
                }, 300);
            case 'regional':
                setTimeout(() => {
                    this.createEvent()(null);
                }, 400);
            default:
                setTimeout(() => {
                    this.onChangeLayer();
                    const center = { lat: -26.6116, lon: -47.2741 };
                    this.map.setView(new L.LatLng(center.lat, center.lon), 4);
                }, 700);
                break;
        }
    }

    public onChangeModel() {
        this.setGlobalLayer();
        const layer = this.layers.find(
            (e: any) => e.category === this.layerModel,
        );
        if (!layer) {
            return;
        }
        this.layer = layer.name;
        this.layerId = layer.id;

        this.$emit('change-layer', this.layerMetadata);

        this.toggleShapefile();
        this.map.removeLayer(this.geoJSONPrScLayer);
        this.map.removeLayer(this.cepLayer);
        this.map.removeLayer(this.babitongaLayer);
        this.isRegionalLayer = false;
        this.mapModel = 'global';
    }

    public onChangeLayer() {
        this.$emit('change-layer', this.layerMetadata);
        this.toggleShapefile();
        this.map.removeLayer(this.geoJSONPrScLayer);
        this.isRegionalLayer = false;
    }

    public onChangeWindType() {
        if (this.windType === 'streams') {
            if (this.vectorsLayer) {
                this.map.removeLayer(this.vectorsLayer);
            }

            const options = {
                year: 'numeric',
                month: 'numeric',
                day: 'numeric',
            } as const;
            const formatter = new Intl.DateTimeFormat('pt-BR', options);

            this.onChangeDateSelection(formatter.format(new Date()));
            return;
        }

        if (this.velocityLayer) {
            this.map.removeLayer(this.velocityLayer);
        }

        this.vectorsLayer = L.tileLayer.wms(
            oceanVectorsOptions.get(this.mapModel).path,
            oceanVectorsOptions.get(this.mapModel).opts,
        );
        this.map.addLayer(this.vectorsLayer);
    }

    public createEvent() {
        return (evt: any) => {
            localStorage.setItem('regional-clicked', 'true');
            if (evt) {
                evt.originalEvent.preventDefault();
                evt.originalEvent.stopPropagation();
            }
            if (this.isCoastLayer) {
                return this.createCoastEvent()(evt);
            }
            let index = -1;
            if (this.mapModel === 'regional') {
                index = this.setLayerArea(
                    'global',
                    (e: any) => e.id === this.layers[this.oldIndex].parent.id,
                    5,
                );
            } else {
                index = this.setLayerArea(
                    'regional',
                    (e: any) => e.id === this.layers[this.oldIndex].child[0].id,
                    6,
                );
            }

            setTimeout(() => {
                this.map.closePopup();
                this.overlays.forEach((overlay: any) => {
                    overlay.selected = false;
                    this.map.removeLayer(overlay.layer);
                });
            }, 300);
        };
    }

    public createCoastEvent() {
        return (evt: any) => {
            let index = -1;

            if (this.mapModel === 'coast') {
                this.map.addLayer(this.shapeFileLayer);
                index = this.setLayerArea(
                    'regional',
                    (e: any) => e.id === this.layers[this.oldIndex].parent.id,
                    6,
                );
            } else {
                index = this.setLayerArea(
                    'coast',
                    (e: any) => e.id === this.layers[this.oldIndex].child[0].id,
                    8,
                );
            }

            setTimeout(() => {
                this.map.closePopup();
                this.overlays.forEach((overlay: any) => {
                    overlay.selected = false;
                    this.map.removeLayer(overlay.layer);
                });
            }, 300);
        };
    }

    public createCepBabitongaEvent(type: string) {
        return (evt: any) => {
            let index = -1;
            if (this.mapModel === 'cep' || this.mapModel === 'babitonga') {
                this.map.addLayer(this.geoJSONPrScLayer);
                index = this.setLayerArea(
                    'coast',
                    (e: any) => e.id === this.layers[this.oldIndex].parent.id,
                    8,
                );
            } else {
                index = this.setLayerArea(
                    type,
                    (e: any) =>
                        e.id ===
                        this.layers[this.oldIndex].child.find((el: any) =>
                            el.layers.includes(type),
                        ).id,
                    11,
                    { lat: evt.latlng.lat, lon: evt.latlng.lng },
                );
            }

            setTimeout(() => {
                this.map.closePopup();
                this.overlays.forEach((overlay: any) => {
                    overlay.selected = false;
                    this.map.removeLayer(overlay.layer);
                });
            }, 300);
        };
    }

    @Emit('changeLayerVisible')
    public toggleBaseLayer() {
        if (!this.isLayersVisible) {
            this.map.removeLayer(this.shapeFileLayer);
            this.map.removeLayer(this.babitongaLayer);
            this.map.removeLayer(this.cepLayer);
            this.map.removeLayer(this.geoJSONPrScLayer);
            const index = this.layers.findIndex(
                (e: any) => e.id === this.layerId,
            );
            this.$store.getters.getAllLayers()[index].layer.setOpacity(0);
            this.$store.dispatch('isLayerVisible', false);
            return;
        }

        this.setGlobalLayer();
        this.map.addLayer(this.shapeFileLayer);
        const index = this.layers.findIndex((e: any) => e.id === this.layerId);
        this.$store.getters.getAllLayers()[index].layer.setOpacity(1);
        this.$store.dispatch('isLayerVisible', true);
    }

    public startSimulation() {
        this.dialog = false;
        this.toggleSpreadOilLayer(this.oilSpillSelectedPoint);
    }

    public mounted() {
       getGeoJSONBrazil().then(shapefileAsGeoJSON => {
            this.oilToolclickableArea = L.geoJSON(shapefileAsGeoJSON, {
                style: (feature: any) => {
                    return {
                        fillColor: 'rgba(0,0,0,0.2)',
                    };
                },
                onEachFeature: (feature, layer) => {
                    layer.on({
                        click: (evt: any) => {
                            this.dialog = true;
                            this.oilSpillSelectedPoint = evt.latlng;
                        },
                    });
                },
            });
        });
        

        this.vectorsLayer = null;

        this.$store.getters.getWindDates().then((res: any) => {
            this.windDates = res;
        });

        this.$store.subscribe(async (mutation, state) => {
            if (mutation.type === 'SET_LAYER_DATE') {
                this.onChangeDateSelection(
                    state.selectedDate,
                    state.selectedHour,
                );
                return;
            }
            if (mutation.type === 'UPDATE_CACHED_LAYERS') {
                this.layers = state.layers;
                return;
            }

            if (mutation.type === 'SET_LAYERS') {
                this.layers = state.layers;
                if (!state.layers[0]) {
                    return;
                }
                this.layer = state.layers[0].name;
                this.layerId = state.layers[0].id;

                const shapefileAsGeoJSON = await getShapeFile();
                const geoJSONPrSc = await getGeoJSONPrSc();
                const babitongaAsGeoJSON = await getGeoJSONBabitonga();
                const cepAsGeoJSON = await getGeoJSONcep();

                setTimeout(() => {
                    this.shapeFileLayer = L.geoJSON(shapefileAsGeoJSON, {
                        style: (feature: any) => {
                            return {
                                fillColor: 'rgba(0,0,0,0)',
                            };
                        },
                        onEachFeature: (feature, layer) => {
                            layer.on({
                                click: this.createEvent(),
                            });
                        },
                    });

                    this.geoJSONPrScLayer = L.geoJSON(geoJSONPrSc, {
                        style: (feature: any) => {
                            return {
                                fillColor: 'rgba(0,0,0,0)',
                                color: '#ff0000',
                            };
                        },
                        onEachFeature: (feature, layer) => {
                            layer.on({
                                click: this.createCoastEvent(),
                            });
                        },
                    });

                    this.babitongaLayer = L.geoJSON(babitongaAsGeoJSON, {
                        style: (feature: any) => {
                            return {
                                fillColor: 'rgba(0,0,0,0)',
                                color: '#ffff00',
                            };
                        },
                        onEachFeature: (feature, layer) => {
                            layer.on({
                                click: this.createCepBabitongaEvent(
                                    'babitonga',
                                ),
                            });
                        },
                    });

                    this.cepLayer = L.geoJSON(cepAsGeoJSON, {
                        style: (feature: any) => {
                            return {
                                fillColor: 'rgba(0,0,0,0)',
                                color: '#00ff00',
                            };
                        },
                        onEachFeature: (feature, layer) => {
                            layer.on({
                                click: this.createCepBabitongaEvent('cep'),
                            });
                        },
                    });

                    this.map.addLayer(this.shapeFileLayer);
                }, 3000);
            }
        });
    }

    private toggleShapefile() {
        if (!!this.shapeFileLayer) {
            const layer = this.layers.find((l: any) => this.layerId === l.id);
            if (
                !layer ||
                !(layer.child || { length: 0 }).length ||
                this.layerModel === 'satellite'
            ) {
                this.map.removeLayer(this.shapeFileLayer);
                return;
            }

            this.map.addLayer(this.shapeFileLayer);
        }
    }

    private setLayerArea(model: string, rule: any, zoom: number, point?: any) {
        const center = point || { lat: -26.6116, lon: -47.2741 };
        let index = -1;
        this.map.setView(new L.LatLng(center.lat, center.lon), zoom);

        index = this.layers.findIndex(rule);
        if (this.windToggler) {
            this.toggleVelocityLayer();
            this.windToggler = false;
        }
        switch (model) {
            case 'global':
                this.isRegionalLayer = false;
                this.isCoastLayer = false;
                this.map.removeLayer(this.babitongaLayer);
                this.map.removeLayer(this.cepLayer);
                this.map.removeLayer(this.geoJSONPrScLayer);
                break;
            case 'regional':
                this.isRegionalLayer = true;
                this.isCoastLayer = false;
                if (
                    this.layers[index].isRegional &&
                    !!this.layers[index].child[0]
                ) {
                    this.map.removeLayer(this.geoJSONPrScLayer);
                    this.map.addLayer(this.geoJSONPrScLayer);
                }
                this.map.removeLayer(this.babitongaLayer);
                this.map.removeLayer(this.cepLayer);
                break;
            case 'coast':
                this.isRegionalLayer = false;
                this.isCoastLayer = true;
                const finder = (type: string) =>
                    this.layers[index].child.find((el: any) =>
                        el.layers.includes(type),
                    );
                if (finder('babitonga')) {
                    this.map.removeLayer(this.babitongaLayer);
                    this.map.addLayer(this.babitongaLayer);
                }

                if (finder('cep')) {
                    this.map.removeLayer(this.cepLayer);
                    this.map.addLayer(this.cepLayer);
                }

                this.map.removeLayer(this.shapeFileLayer);
                break;
            case 'cep':
                this.isRegionalLayer = false;
                this.isCoastLayer = false;
                this.isBabitongaLayer = false;
                this.isCepLayer = true;
                this.map.removeLayer(this.babitongaLayer);
                this.map.removeLayer(this.geoJSONPrScLayer);
                break;
            case 'babitonga':
                this.isRegionalLayer = false;
                this.isCoastLayer = false;
                this.isBabitongaLayer = true;
                this.isCepLayer = false;
                this.map.removeLayer(this.cepLayer);
                this.map.removeLayer(this.geoJSONPrScLayer);
                break;
            default:
                break;
        }

        this.mapModel = model;

        this.layerId = this.layers[index].id;
        const meta = this.layers[index].layer.wmsParams.layers;
        this.$emit('change-layer', meta);
        this.changeLayerVisible(this.oldIndex, index);

        return index;
    }

    private searchFunction(name: string): string {
        return name.includes('_wp_regional') || this.isRegionalLayer
            ? name.replace('_wp_regional', '')
            : name + '_wp_regional';
    }

    private changeLayerVisible(oldIndex: number, index: number) {
        if (!!this.$store.getters.getAllLayers()[oldIndex]) {
            if (this.$store.getters.getAllLayers()[oldIndex].cachedLayers) {
                this.$store.getters
                    .getAllLayers()
                    [oldIndex].cachedLayers.forEach((layer: any) => {
                        this.map.removeLayer(layer);
                    });
            }
            this.map.removeLayer(
                this.$store.getters.getAllLayers()[oldIndex].layer,
            );
        }

        this.$store.getters.getAllLayers()[index].layer.setOpacity(1);
        this.map.addLayer(this.$store.getters.getAllLayers()[index].layer);
        this.layerId = this.$store.getters.getAllLayers()[index].id;
    }

    private debounceFunction(fct: any) {
        let timeout: any = 0;

        return (params: any) => {
            if (!!timeout) {
                clearTimeout(timeout);
            }

            timeout = setTimeout(() => {
                fct(params);
            }, 300);
        };
    }

    @Watch('layerId')
    private onLayerChange(value: any, oldValue: any): void {
        setTimeout(() => {
            window.requestAnimationFrame(() => {
                if (!this.map) {
                    this.onLayerChange(value, oldValue);
                    return;
                }
                this.map.eachLayer((layer: any) => {
                    if (layer.options.name === 'World Imagery with labels') {
                        layer.bringToFront();
                    }
                });
                const oldIndex = this.layers.findIndex((e: any) => e.id === oldValue);
                const index = this.layers.findIndex((e: any) => e.id === value);

                if (!this.layers) {
                    this.onLayerChange(value, oldValue);
                    return;
                }

                if (!!this.layers[index]) {
                    this.changeLayerVisible(oldIndex, index);
                }
            });
        }, 1000);        
    }

    private createPopup(value: number, latlng: [number, number]) {
        L.popup({ maxWidth: 800, closeButton: false, className: 'info-value' })
            .setLatLng(latlng)
            // <h2>${ this.$t(this.layers[index].name)}</h2>
            .setContent(
                `
                <h2>${(value as number).toFixed(
                    3,
                )} ${this.$store.getters.getSelectedLayer().symbol || ''}</h2>
            `,
            )
            .openOn(this.map);
    }

    private onChangeOverlay(overlay: any) {
        if (!overlay.selected) {
            this.map.removeLayer(overlay.layer);
            return;
        }

        this.map.addLayer(overlay.layer);
    }
}
</script>

<style lang="scss" scoped>
div.panel {
    position: absolute;
    top: 14vh;
    left: 0;
    z-index: 9999;
    background: white;
    transition: 0.3s ease-in-out;
    width: 30vw;
    padding: 3rem 1rem 2rem 1rem;
    height: auto;
    border-radius: 5px;
    transform: translateX(-110%);
    overflow: auto;
    max-height: 70vh;

    @media (max-width: 768px) {
        top: 0;
        width: 100vw;
        height: 100vh;
        max-height: 70vh;
        z-index: 99999;
    }
}

header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;

    span {
        background: #4e76ed;
        border-radius: 100%;
        width: 3rem;
        height: 3rem;
        padding: 0.5rem 0 0 0.5rem;
        cursor: pointer;
        position: absolute;
        right: 1rem;
        top: 1rem;
    }
}

div.panel.open {
    transform: translateX(0);
}

.map-control {
    position: absolute;
    z-index: 99999;
    top: 5rem;
    left: 2rem;
    margin: 0;
    margin-top: 1rem;
}

.info-value .leaflet-popup-content-wrapper,
.info-value .leaflet-popup-tip {
    background: rgba(0, 0, 0, 0);
    color: #333;
    box-shadow: none;
}

.wind-toggle-cb:checked + .wind-toggle {
    background-color: white;
    color: #4e76ed;
    .v-icon {
        color: #4e76ed;
    }
    &:hover:after,
    &:hover::after {
        background-color: white;
        color: #4e76ed;
    }
}

.wind-toggle {
    padding: 1rem;
    border-radius: 100%;
    margin-right: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    background: #4e76ed;
    color: white;
    font-weight: 600;
    -webkit-box-shadow: 0 3px 1px -2px rgba(0, 0, 0, 0.2),
        0 2px 2px 0 rgba(0, 0, 0, 0.14), 0 1px 5px 0 rgba(0, 0, 0, 0.12);
    box-shadow: 0 3px 1px -2px rgba(0, 0, 0, 0.2),
        0 2px 2px 0 rgba(0, 0, 0, 0.14), 0 1px 5px 0 rgba(0, 0, 0, 0.12);
    will-change: box-shadow;

    .v-icon {
        color: white;
    }

    &:hover:after,
    &:hover::after {
        content: attr(value);
        position: absolute;
        background: #4e76ed;
        padding: 0.5rem;
        width: max-content;
        left: 5rem;
        border-radius: 5px;
        z-index: 999999;
    }

    @media screen and (orientation: landscape) and (max-width: 1024px) {
        display: none;
    }
}
</style>
