<template>
  <div class="legend-container" v-bind:class="{ 'side-open': !!sideOpen, 'hidden': !title }">
    <h1>{{ $t(title) }}</h1>
    <h1>{{ symbol }}</h1>
    <img v-bind:src="url" alt="Legend not found">
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

const basePath = `${process.env.VUE_APP_BASE_URL}`;
const baseUrl = (layer: string) =>
    `${basePath}/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=30&HEIGHT=10&LAYER=${layer}`;

@Component({
    components: {},
})
export default class MapLegend extends Vue {
    public url = '';
    public title = '';
    public symbol = '';

    @Prop(Boolean) public sideOpen!: boolean;

    public mounted() {
        this.$store.subscribe((mutation, state) => {
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
                this.url = baseUrl(state.selectedLayer.name);
                this.title = layer.name;
                this.symbol = `(${state.selectedLayer.symbol})`;
            }
        });
    }
}
</script>

<style lang="scss" scoped>
    .hidden { display: none; }    
    .legend-container {
        position: absolute;
        z-index: 9999;
        right: 2rem;
        bottom: 2vh;
        overflow: hidden;
        padding: 2rem;
        max-width: 10rem;
        background: white;
        border-radius: 5px;
        margin-bottom: 2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;        
        align-items: center;    
        will-change: transform;
        transition: 0.3s ease-in-out;

        h1 {
            font-size: 1em;
            text-align: center;
        }

        @media (max-width: 768px) {
            display: none;
        }
    }

    .side-open { transform: translateX(-30vw); }
</style>
