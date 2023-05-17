<template>
  <v-app>   
    <v-content>
      <router-view/>
    </v-content>   
  </v-app>
</template>

<script>
import CentralMap from './components/CentralMap';
import LayerControlSidebar from './components/LayerControlSidebar';
import Settings from './components/Settings';
import $ from 'jquery';

export default {
  name: 'App',
  components: {
    CentralMap,
    Settings,
    LayerControlSidebar,
  },
  data() {
    return {
      clipped: false,
      drawer: true,
      fixed: false,
      items: [
        {
          icon: 'bubble_chart',
          title: 'Inspire',
        },
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Mercator',
    };
  },
};
</script>
<style lang="scss">
html,
body {
  height: 100%;
}

.leaflet-div-icon {
    background: transparent;
    width: 0;
    height: 0;
    border: none;
}

.v-overlay.v-overlay--active,.v-dialog__content.v-dialog__content--active {
    z-index: 99999 !important;
}
</style>