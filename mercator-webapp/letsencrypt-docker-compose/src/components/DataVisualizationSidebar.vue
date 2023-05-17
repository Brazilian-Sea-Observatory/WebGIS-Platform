<template>
    <div id="content" class="hide-sm" v-bind:class="{ open: isOpen || opened }">
        <header>
            <h1>{{ $t("map.dataSidebar.title") }}</h1>
            <span @click="close">
                <v-icon medium color="white">close</v-icon>
            </span>
        </header>
        <main v-if="!!vessel && !isStation">
            <ul>
                <li>
                    <b>{{$t('vessel.name')}}: </b>
                    {{vessel.name || '-'}}
                </li>
                <li>
                    <b>{{$t('vessel.destination')}}: </b>
                    {{vessel.destination || '-'}}
                </li>
                <li>
                    <b>{{$t('vessel.time')}}: </b>
                    {{vessel.time.toLocaleString()}}
                </li>
                <li>
                    <b>{{$t('vessel.latitude')}}: </b>
                    {{vessel.latitude}}
                </li>
                <li>
                    <b>{{$t('vessel.longitude')}}: </b>
                    {{vessel.longitude}}
                </li>
                <li>
                    <b>{{$t('vessel.rotation')}}: </b>
                    {{vessel.rotation}} {{$t('vessel.rotationUnit')}}
                </li>
            </ul>
        </main>
        <main v-if="!!isStation">
            <ul v-if="!!isStation">
                <li>
                    <b>{{ $t('map.layerControl.overlays.sensorData.platform') }}</b>
                    {{metadata.platform}}
                </li>
                <li>
                    <b>{{ $t('map.layerControl.overlays.sensorData.last_date_') }}</b>
                    {{metadata.date}}
                </li>
                <li>
                    <b>{{ $t('map.layerControl.overlays.sensorData.last_latit') }}</b>
                    {{metadata.latitude}}
                </li>
                <li>
                    <b>{{ $t('map.layerControl.overlays.sensorData.last_longi') }}</b>
                    {{metadata.longitude}}
                </li>
            </ul>
            <v-tabs
                v-model="tab1"
                v-if="tempShow"
                style="margin-top: 1rem;"
                background-color="cyan"
                :centered="true"
                :grow="true"
            >
                <v-tabs-slider></v-tabs-slider>
                <v-tab href="#tab-temperature">{{ $t('map.layerControl.layers.temperature_satellite') }}</v-tab>

                <v-tab-item id="tab-temperature">
                    <v-card flat tile>
                        <v-card-text>
                            <div style="height: 22rem; width:28vw" id="temp-chart-renderer"></div>
                        </v-card-text>
                    </v-card>
                </v-tab-item>                
            </v-tabs>
            <v-tabs
                v-model="tab2"
                v-if="depthShow"
                style="margin-top: 1rem;"
                background-color="cyan"
                :centered="true"
                :grow="true"
            >
                <v-tabs-slider></v-tabs-slider>
                <v-tab href="#tab-depth">{{ $t('map.layerControl.layers.depth') }}</v-tab>

                <v-tab-item id="tab-depth">
                    <v-card flat tile>
                        <v-card-text>
                            <div style="height: 22rem; width:28vw" id="depth-chart-renderer"></div>
                        </v-card-text>
                    </v-card>
                </v-tab-item>                
            </v-tabs>
            <v-tabs
                v-model="tab3"
                v-if="salinityShow"
                style="margin-top: 1rem;"
                background-color="cyan"
                :centered="true"
                :grow="true"
            >
                <v-tabs-slider></v-tabs-slider>
                <v-tab href="#tab-salinity">{{ $t('map.layerControl.layers.salinity') }}</v-tab>

                <v-tab-item id="tab-salinity">
                    <v-card flat tile>
                        <v-card-text>
                            <div style="height: 22rem; width:28vw" id="salinity-chart-renderer"></div>
                        </v-card-text>
                    </v-card>
                </v-tab-item>                
            </v-tabs>
        </main>
    </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Emit, Watch } from 'vue-property-decorator';
import * as echarts from 'echarts';
import { VesselType } from '../providers/VesselType';

@Component({
    components: {},
})
export default class DataVisualizationSidebar extends Vue {
    @Prop(Object) public message!: any;
    @Prop(VesselType) public vessel!: string;
    @Prop(Boolean) public isOpen!: boolean;
    public opened = false;
    public metadata: any = {};
    public tab1 = 'tab-temperature';
    public tab2 = 'tab-depth';
    public tab3 = 'tab-salinity';
    public isStation = false;
    public tempShow = false;
    public depthShow = false;
    public salinityShow = false;

    public genChart(data: any, id: string) {
        const options = {
            year: 'numeric', month: 'numeric', day: 'numeric'
        } as const;
        const formatter = new Intl.DateTimeFormat('pt-BR', options);
        const date = data.map((value: { date: string, value: number}) => {
            const dateObject = new Date(value.date);
            if (isNaN(+dateObject)) {
                console.warn('Could not parse date');
                return value.date;
            }

            return formatter.format(dateObject);
        });
        const values = data.map((value: { date: string, value: number}) => value.value);
        const option = {
            tooltip: {
                trigger: 'axis',
                position: function(pt: any) {
                    return [pt[0], '10%'];
                },
            },
            textStyle: {
              dataView: {
                show : false,
                title : '',
                readOnly: false,
                lang: ['Visualizar', 'atualizar', 'fechar']
              }
            },
            title: {
                left: 'center',
                text: '',
            },
            xAxis: {
                type: 'category',                
                data: date,
                min: "dataMin",
                max: "dataMax"
            },
            yAxis: {
                type: 'value',
                min: "dataMin",
                max: "dataMax",
                boundaryGap: [0, '100%'],
            },
            dataZoom: [
                {
                    type: 'inside',
                },
                {
                    handleIcon:
                        'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                    handleSize: '80%',
                    handleStyle: {
                        color: '#fff',
                        shadowBlur: 3,
                        shadowColor: 'rgba(0, 0, 0, 0.6)',
                        shadowOffsetX: 2,
                        shadowOffsetY: 2,
                    },
                },
            ],
            series: [
                {
                    name: '',
                    type: 'line',
                    smooth: true,
                    symbol: 'none',
                    sampling: 'average',
                    itemStyle: {
                        color: 'rgb(255, 70, 131)',
                    },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            {
                                offset: 0,
                                color: 'rgb(255, 158, 68)',
                            },
                            {
                                offset: 1,
                                color: 'rgb(255, 70, 131)',
                            },
                        ]),
                    },
                    data: values,
                },
            ],
        };

        const chart = echarts.init(document.getElementById(id) as HTMLDivElement);
            /* eslint-disable */
            chart.setOption(option as any);
    }

    @Emit('close')
    public close() {
        this.opened = false;
        this.isStation = false;
        this.tempShow = false;
        this.depthShow = false;
        this.salinityShow = false;
    }

    // @Watch('isOpen')
    // private onOpenChange(value: string, oldValue: string) {
    //     this.opened = true;
    //     if (!!this.message) {
    //         const data = this.message.features
    //             .sort((a: any, b: any) => +new Date(a.properties.time) - +new Date(b.properties.time))
    //             .filter((e: any) => e.properties.variable === 'TEMP');

    //         const lastData = data[data.length - 1];
    //         this.metadata = {
    //             platform: lastData.properties.code,
    //             date: new Date(lastData.properties.time).toLocaleString(),
    //             latitude: lastData.geometry.coordinates[0].toFixed(4),
    //             longitude: lastData.geometry.coordinates[1].toFixed(4),
    //         }

    //         setTimeout(() => {
    //             this.genChart(
    //                 data.map((e: any) => ({
    //                     date: new Date(e.properties.time).toLocaleString(),
    //                     value: parseFloat(e.properties.value.toFixed(2))
    //                 })),
    //             );
    //         }, 500);            
    //     }        
    // }

    public mounted() {
        const options = {
            year: 'numeric', month: 'numeric', day: 'numeric',
            hour: 'numeric', minute: 'numeric', second: 'numeric',
            hour12: false,
            timeZone: 'America/Sao_Paulo' 
        } as const;
        const formatter = new Intl.DateTimeFormat('pt-BR', options);
        this.$store.subscribe((mutation, state) => {
            if (mutation.type === 'SET_STATION_VIEW') {
                this.opened = true;
                this.isStation = true;
                this.metadata = {
                    platform: state.stationData.metadata.code,
                    date: formatter.format(new Date(state.stationData.metadata.time)),
                    latitude: state.stationData.metadata.lat.toFixed(4),
                    longitude: state.stationData.metadata.lon.toFixed(4),
                };            
                if (state.stationData.values.temperature.length > 0) {
                    this.tempShow = true;
                }
                
                if (state.stationData.values.depth.length > 0) {
                    this.depthShow = true;
                }
                
                if (state.stationData.values.salinity.length > 0) {
                    this.salinityShow = true;
                }
                setTimeout(() => {                
                    if (state.stationData.values.temperature.length > 0) {
                        this.tempShow = true;
                        this.genChart(state.stationData.values.temperature, 'temp-chart-renderer');
                    }
                    
                    if (state.stationData.values.depth.length > 0) {
                        this.depthShow = true;
                        this.genChart(state.stationData.values.depth, 'depth-chart-renderer');
                    }
                    
                    if (state.stationData.values.salinity.length > 0) {
                        this.salinityShow = true;
                        this.genChart(state.stationData.values.salinity, 'salinity-chart-renderer');
                    }
                }, 1000);
            }

            if (mutation.type === 'SET_VESSEL_VIEW') {
                this.isStation = false;
            }
        });
    }
}
</script>

<style lang="scss" scoped>
#content {
    position: absolute;
    top: 0;
    right: 0;
    z-index: 9999999;
    background: white;
    transition: 0.3s ease-in-out;
    width: 30vw;
    padding: 2rem 1rem;
    height: 100%;
    transform: translateX(100%);
}

header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    border-bottom: 1px solid rgba(50, 50, 50, 0.4);
    margin-bottom: 1rem;
    padding-bottom: 1rem;

    span {
        background: #4e76ed;
        border-radius: 100%;
        width: 3rem;
        height: 3rem;
        padding: 0.5rem 0 0 0.5rem;
        cursor: pointer;
    }
}

ul {
    list-style: none;
    padding: 0;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    border-bottom: 1px solid rgba(50, 50, 50, 0.4);

    li {
        width: 50%;
        display: flex;
        flex-direction: column;
        margin-bottom: 1rem;

        b {
            color: #4e76ed;
        }
        &.w-100 {
            width: 100%;
        }
    }
}

#content.open {
    transform: translateX(0);
    max-height: 100%;
    overflow: auto;
}

@media (max-width: 768px) {
    .hide-sm {
        display: none !important;
    }
}
</style>
