<template>
  <div class="field-container">
    <img src="/img/logo_white.png" alt="Brazilian Sea Observatory">
    <input
        type="text"
        id="search"
        :placeholder="$t('map.search')"
        name="search"
        v-model="search"
        @keypress="onSearch()"
    >  
    <v-btn @click="onSelect(search.split(',').map(e => parseFloat(e)))" color="primary" fab light>
        <v-icon>search</v-icon>
    </v-btn> 
    <v-list v-if="items.length > 0" two-line>
      <template v-for="(item, index) in items">
        <v-list-tile :key="item.title" avatar ripple @click="onSelect(item.latlon)">
          <v-list-tile-content>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            <v-list-tile-sub-title class="text--primary">{{ item.headline }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-divider v-if="index + 1 < items.length" :key="index"></v-divider>
      </template>
    </v-list>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
    components: {},
})
export default class MapSearchField extends Vue {
    public search = '-25.72841, -48.09987';
    public items = [];

    private lastCall = -1;

    public onSelect(latlon: [number, number]) {
        this.items = [];
        this.$store.dispatch('setCenter', latlon);
    }

    public onSearch() {
        if (!this.search) {
            this.items = [];
            return;
        }

        if (this.lastCall) {
            clearTimeout(this.lastCall);
        }

        this.lastCall = setTimeout(() => {
            fetch(
                `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
                    this.search,
                )}&country=Brasil&format=json`,
            )
                .then((res: Response) => res.json())
                .then((value: any) => {
                    this.items = value.map((element: any) => ({
                        title: element.display_name,
                        headline: `${element.lat},${element.lon}`,
                        subtitle: element.license,
                        latlon: [element.lat, element.lon],
                    }));
                });
        }, 300);
    }
}
</script>

<style lang="scss" scoped>
.field-container {
    position: fixed;
    z-index: 9999;
    top: 1rem;
    left: 4rem;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    img {
        width: 15%;
        background: #4e76ed;
        border-radius: 2em;
        padding: 0.2rem 1rem;
        z-index: 2;
        @media (max-width: 768px) {
            height: 3rem;
            width: auto;
        }
    }
    input {
        border: 0;
        background: #fff;
        font-size: 1.5em;
        height: 1.8em;
        border-radius: 2em;
        border: 1px solid #ccc;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.125);
        margin: 0;
        background: #fff;
        padding-top: 1em;
        padding-bottom: 1em;
        padding-left: 3rem;
        padding-right: 1rem;
        margin-left: -2.5rem;
        z-index: 1;
        width: 40%;
        outline: none;
        position: relative;
    }
}

.v-list.v-list--two-line.theme--light {
    position: absolute;
    top: calc(1.8em + 1rem);
    left: 15%;
    max-width: 35%;
    max-height: 30rem;
    overflow: auto;
}
</style>
