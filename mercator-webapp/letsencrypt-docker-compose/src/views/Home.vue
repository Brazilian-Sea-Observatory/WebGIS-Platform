<template>
  <div class="home">
    <Settings/>
    <CentralMap />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import * as L from 'leaflet';
import { tileLayer } from 'leaflet';
import CentralMap from '@/components/CentralMap.vue'; // @ is an alias to /src
import Settings from '@/components/Settings.vue';
import { getAllLayers } from '@/providers/layers.service';

const basePath = `${process.env.VUE_APP_BASE_URL}/ows?`;

@Component({
    components: {
        CentralMap,
        Settings,
    },
})
export default class Home extends Vue {

  public mounted() {
    getAllLayers().then((res: any) => {
      const layers = res.map((layer: any) => {
          layer.layer = tileLayer.wms(layer.layer.path, layer.layer.opts);
          return layer;
      });

      this.$store.dispatch('setLayers', layers);
    });    
  }
}
</script>

<style lang="scss" scoped>
.home {
    width: 100%;
    height: 100%;
}
</style>
