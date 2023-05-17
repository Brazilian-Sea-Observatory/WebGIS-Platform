<template>
    <div id="content" class="hide-sm" v-bind:class="{ open: isOpen || opened }">
        <header>
            <h1>{{ $t("map.dataSidebar.title") }}</h1>
            <span @click="close">
                <v-icon medium color="white">close</v-icon>
            </span>
        </header>
        <main>
            <v-card flat tile>
                <v-card-text style="padding: 0">
                    <div style="height: 22rem; width:30vw" id="chart-renderer"></div>
                </v-card-text>
            </v-card>
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
export default class PointViewSidebar extends Vue {
    @Prop(Boolean) public isOpen!: boolean;
    public opened = false;
    public metadata: any = {};
    public title = '';
    public symbol = '';

    public genChart(data: any) {
        const options = {
            year: 'numeric', month: 'numeric', day: 'numeric'
        } as const;
        const formatter = new Intl.DateTimeFormat('pt-BR', options);
        const date = data.map((value: { date: string, value: number}) =>
            formatter.format(new Date(value.date))
        );
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
                text: this.title,
            },
            xAxis: {
                type: 'category',                
                data: date,
                min: "dataMin",
                max: "dataMax"
            },
            yAxis: {
                name: this.symbol,
                type: 'value',
                min: "dataMin",
                max: "dataMax",
                boundaryGap: [0, '100%'],
                axisLabel: {
                    formatter: `{value}`
                }
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
                    name: this.symbol,
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

        const chart = echarts.init(document.getElementById('chart-renderer') as HTMLDivElement);
        /* eslint-disable */
        chart.setOption(option as any);
    }

    @Emit('close')
    public close() {
        this.opened = false;
    }

    public mounted() {
        this.$store.subscribe((mutation, state) => {
            if (mutation.type === 'SET_POINT_VIEW') {
                this.opened = true;
                this.metadata = {};
                setTimeout(() => {                    
                    this.genChart(state.pointData);
                }, 1000);
            }
            if (mutation.type === 'SET_SELECTED_LAYER' || mutation.type === 'SET_LAYERS') {
                if (!state.selectedLayer) {
                    return;
                }
                const layer = state.layers.find((e: any) => {
                    return state.selectedLayer.name === e.layers;
                });
                if (!layer) {
                    return;
                }
                
                this.title = this.$t(layer.name).toString();
                this.symbol = `(${state.selectedLayer.symbol})`;
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
}

@media (max-width: 768px) {
    .hide-sm {
        display: none !important;
    }
}
</style>
