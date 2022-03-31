<template>
  <div style="width:100%; height: 100%">
    <div id="map" style="width:100%; height: 100%"></div>
    <MapSearchField/>
    <MapTimeSkip 
        :currentLayer="selectedLayer"
        v-bind:map="map"></MapTimeSkip>
    <MapLegend v-bind:class="{ hidden: !isShownLegend }" v-bind:sideOpen="isDataSidebarOpen"></MapLegend>
    <LayerControlSidebar 
        v-bind:overlays="overlays"
        v-bind:map="map"
        v-on:change-layer="onChangeLayer($event)"
        @changeLayerVisible="onChangeLayerVisible()"
    >
    </LayerControlSidebar>
    <PointViewSidebar 
        @close="close"
        v-bind:isOpen="isDataSidebarOpen" 
    />
  </div>
</template>

<script>
import 'leaflet';
import { MercatorLeafletUtils } from '@/utils/MercatorLeafletUtils.ts';
import LayerControlSidebar from '@/components/LayerControlSidebar';
import MapSearchField from '@/components/MapSearchField';
import DataVisualizationSidebar from '@/components/DataVisualizationSidebar';
import MapTimeSkip from '@/components/MapTimeSkip';
import MapLegend from '@/components/MapLegend';
import PointViewSidebar from '@/components/PointViewSidebar';
import { mapGetters } from 'vuex';

import {
    TMPT_LOADER,
    TMPT_MENU,
    TMPT_TIMECONTROL,
    TMPT_USERPOINT,
} from '@/utils/MapTemplates.ts';
import { getShapeFile, getIndexPlatforms, getGeoJSONPrSc } from '@/providers/layers.service';
import FeatureInfo from '@/providers/feature-info.service';

export default {
    name: 'CentralMap',
    components: {
        LayerControlSidebar,
        MapSearchField,
        DataVisualizationSidebar,
        MapTimeSkip,
        MapLegend,
        PointViewSidebar,
    },
    computed: {
        ...mapGetters([
            'getAllLayers',
            'getSelectedLayer',
            'getLayers',
            'getTimeData',
            'getPopupConfig',
            'getMapModel',
            'getLayerVisibility',
        ]),
    },
    mounted() {
        const map = L.map('map', {
            zoom: 5,
            minZoom: 2,
            preferCanvas: true,
            center: L.latLng(-25.4284, -49.2733)
        });

        const basemaps = MercatorLeafletUtils.getBaseLayers()
            .map((baseLayer) => {
                const basemap = L.tileLayer(baseLayer.url, baseLayer);
                basemap.addTo(map);
                return { name: baseLayer.name, basemap };
            })
            .reduce(
                (p, c) => Object.assign({}, p, { [c.name]: c.basemap }),
                {},
            );

        const date = new Date().toISOString();

        const baseLayers = [...this.getAllLayers()];

        const indexPlatformAsLayer = getIndexPlatforms();
        const indexPlatformLayer = L.tileLayer.wms(indexPlatformAsLayer.path, indexPlatformAsLayer.opts);
        map.on('click', async (e) => {
            if (!map.hasLayer(indexPlatformLayer)) {
                return;
            }

            const getInfo = new FeatureInfo(this.map);
            this.spinControl.addTo(this.map);
            const res = await getInfo.getFeatureInfo(indexPlatformLayer.wmsParams, e);
            this.map.removeControl(this.spinControl);
            if (res.numberReturned >= 1) {
                this.isDataSidebarOpen = true;
                this.dataMessage = res;
                return;
            } else {
                alert(this.$t('map.message.notFound'))
            }

            this.isDataSidebarOpen = false;
        });

        this.overlays = [
            {
                name: 'map.layerControl.overlays.sensor',
                layer: indexPlatformLayer,
                tag: 'sl',
                selected: false,
            },
        ];

        map.on('layerremove', (eventLayer) => {
            this.popup._close();
        });

        map.on('layeradd', (eventLayer) => {
            this.bindLoad(eventLayer);
        });

        this.map = map;
        if (this.getPopupConfig()) {
            this.bindMapEvents();
        }
        this.createSpinner();
        this.$store.subscribe((mutation, state) => {
            if (mutation.type === 'SET_CENTER') {
                this.map.setView(new L.LatLng(...mutation.payload), 6);
            }

            if (mutation.type === 'SET_METADATA') {
                this.layersMetadata = state.layersMetadata;
                this.metadata = this.layersMetadata.find(
                    (value) => value.name === 'mercator:water_speed',
                ) || { dates: [] };
                this.$store.dispatch('setSelectedLayer', this.metadata);              
            }
        });

        this.layersMetadata = this.getTimeData();
        if (!this.layersMetadata.length) {
            this.$store.dispatch('setLayersMetadata');
        }
    },
    data() {
        return {
            isDataSidebarOpen: false,
            isShownLegend: true,
            logoUrl: '/img/logo_white.png',
            latlngControl: L.control(),
            spinControl: L.control({
                position: 'topleft',
            }),
            callNavControl: L.control({
                position: 'topleft',
            }),
            velocityLayer: null,
            map: null,
            popup: L.popup({
                autoPan: false,
            }),
            userSelectionPoint: L.popup({
                autoPan: false,
            }),
            layersMetadata: [],
            metadata: {
                dates: [],
            },
            selectedLayer: null,
            overlays: [],
            satelliteLayers: [],
            forecastLayers: [],
            clicked: false,
            dataMessage: null,
        };
    },
    methods: {
        onChangeLayerVisible() {
            this.isShownLegend = !this.isShownLegend;
        },
        onChangeLayer(layer) {
            this.metadata = this.layersMetadata.find(
                (value) => value.name === layer,
            ) || { dates: [] };
            this.$store.dispatch('setSelectedLayer', this.metadata);
        },
        bindLoad(obj) {
            if (!obj.layer.wmsParams) {
                return;
            }

            obj.layer.on('loading', (evt) => {
                this.spinControl.addTo(this.map);
            });
            const windValues = [
                'mercator:water_vectorial_forecast_daily',
                'regional_model:water_vectorial_hydrodinamic_babitonga_hourly',
                'regional_model:water_vectorial_hydrodinamic_cep_hourly',
                'regional_model:water_vectorial_hydrodinamic_hourly',
                'regional_model:water_vectorial_hydrodinamic_prsc_hourly'
            ];
            obj.layer.on('load', (evt) => {
                if(windValues.includes(obj.layer.options.layers)){
                    return;
                }
                this.selectedLayer = obj.layer;
                this.map.removeControl(this.spinControl);
            });
        },
        createSpinner() {
            this.spinControl.onAdd = (map) => {
                const div = L.DomUtil.create('div');
                div.innerHTML = TMPT_LOADER;
                return div;
            };

            this.spinControl.addTo(this.map);
            return this;
        },

        bindMapEvents() {
            const getDataFromInfo = (res) => {
                 let value = 0;
                if (res.features[0]) {
                    const keys = Object.keys(res.features[0].properties);
                    const data = res.features[0].properties; 
                    value = data[keys[0]];
                }

                return value;
            }

            this.map.on('click', async (e) => {
                // this.isDataSidebarOpen = true;
                if (this.clicked) {
                    this.clicked = false;
                    return;
                }
                if (this.getMapModel() !== 'global' || !this.getLayerVisibility() || localStorage.getItem('regional-clicked')) {
                    localStorage.removeItem('regional-clicked');
                    return;
                }

                this.clicked = true;
                const point = new L.popup({
                    autoClose: false,
                    keepInView: true,
                    closeOnClick: true,
                });

                const getInfo = new FeatureInfo(this.map);
                const res = await getInfo.getFeatureInfo(this.selectedLayer.wmsParams, e);
                
               const value = getDataFromInfo(res);

                point
                    .setLatLng(e.latlng)
                    .setContent(TMPT_USERPOINT(e.latlng, this.$t('analyze'), value))
                    .addTo(this.map);                

                setTimeout(() => {
                    document.getElementById(`infowindow-${e.latlng.lat + '' + e.latlng.lng}`)
                        .addEventListener('mousedown', async (evt) => {                            
                            const getInfo = new FeatureInfo(this.map);
                            const res = await Promise.all(this.metadata.dates.map(date => {
                                return getInfo.getFeatureInfo(
                                    this.selectedLayer.wmsParams, 
                                    e,
                                    date
                                )
                            }));
                            const data = res.map((info, index) => ({
                                value: getDataFromInfo(info).toFixed(3),
                                date: this.metadata.dates[index]
                            }));
                            this.$store.dispatch('setPointView', data);
                            this.isDataSidebarOpen = true;
                        });
                }, 300);
                // this.map.addLayer(point);
            });
        },

        close() {
            this.isDataSidebarOpen = false;
        },
    },
};
</script>

<style lang="scss">
@import '~leaflet/dist/leaflet.css';

.leaflet-control-timecontrol.timecontrol-date.utc {
    width: 14vw;
}

.timecontrol-dateslider > .slider {
    width: 50vw;
}

.mercator-legend {
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: rgba(230, 230, 230, 0.8);
    padding: 1rem;
    border-radius: 5px;
    max-width: 8vw;

    &--title {
        margin-bottom: 1rem;
    }

    h3 {
        background-color: #fffffa;
    }

    span {
        font-size: 1.3em;
        width: 100%;
        text-align: center;
    }
}

.leaflet-range-slider {
    height: 6rem;
    background: transparent;
    padding: 3rem 7rem 5rem 23rem;
    width: 100%;
    overflow: hidden;
    border-radius: 5px;
}

.hidden {
    visibility: hidden;
}

@mixin rangeThumb {
    width: 18px;
    height: 18px;
    margin: -8px 0 0;
    border-radius: 50%;
    background: #4e76ed;
    cursor: pointer;
    border: 0 !important;
}

@mixin rangeTrack {
    width: 100%;
    height: 2px;
    cursor: pointer;
    background: #fffffa;
}

.range {
    position: relative;
    width: 550px;
    height: 5px;
    transform: translateY(1rem);
}

.range input {
    width: 100%;
    position: absolute;
    top: 2px;
    height: 0;
    -webkit-appearance: none;

    // Thumb
    &::-webkit-slider-thumb {
        -webkit-appearance: none; // needed again for Chrome & Safari
        @include rangeThumb;
    }

    &::-moz-range-thumb {
        @include rangeThumb;
    }

    &::-ms-thumb {
        @include rangeThumb;
    }

    // Track
    &::-webkit-slider-runnable-track {
        @include rangeTrack;
    }

    &::-moz-range-track {
        @include rangeTrack;
    }

    &::-ms-track {
        @include rangeTrack;
    }

    &:focus {
        // override outline/background on focus
        background: none;
        outline: none;
    }

    &::-ms-track {
        // A little somethin' somethin' for IE
        width: 100%;
        cursor: pointer;
        background: transparent;
        border-color: transparent;
        color: transparent;
    }
}

// Labels below slider
.range-labels {
    margin: 18px -41px 0;
    padding: 0;
    list-style: none;
    transform: translateY(1rem);

    li {
        position: relative;
        float: left;
        width: 90.25px;
        text-align: center;
        color: #fffffa;
        font-size: 14px;
        cursor: pointer;

        &::before {
            position: absolute;
            top: -25px;
            right: 0;
            left: 0;
            content: '';
            margin: 0 auto;
            width: 9px;
            height: 9px;
            background: #fffffa;
            border-radius: 50%;
        }
    }

    .active {
        color: #fffffa;
        background: #4e76ed;
        border-radius: 10px;
    }

    .selected::before {
        background: #4e76ed;
    }

    .active.selected::before {
        display: none;
    }
}

.current-latlng {
    background: rgba(230, 230, 230, 0.6);
    padding: 1rem;
    display: flex;
    flex-direction: column;
    border-radius: 5px;
    margin-top: 6rem !important;

    span {
        font-size: 1.3em;
        font-weight: bold;
    }
}

.leaflet-control-velocity.leaflet-control {
    display: none;
}

.mercator-color {
    background-color: #4e76ed !important;
    border-color: #4e76ed !important;
    color: #fffffa !important;
    &--text {
        caret-color: #4e76ed !important;
        color: #4e76ed !important;
    }
}

.leaflet-control-layers.leaflet-control,
.leaflet-control-zoom.leaflet-control a {
    border-radius: 5px;
    background: #4e76ed;
    color: #fffffa;
    span {
        color: #fffffa;
    }
}

.position-absolute {
    position: absolute !important;
}
.img-brand {
    width: 120px !important;
    margin-top: 1rem;
}
</style>
