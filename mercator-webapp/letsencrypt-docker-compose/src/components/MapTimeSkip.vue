<template>
  <div class="time-skip" v-if="isShown && layerVisibility">
    <button
      id="time-skip--rewind"
      type="button"
      class="v-btn v-btn--floating v-btn--left v-btn--small theme--light mercator-color"
      @click="onRewind()"
    >
      <div class="v-btn__content">
        <i aria-hidden="true" class="v-icon material-icons theme--light">fast_rewind</i>
      </div>
    </button>
    <button
      id="time-skip--play"
      type="button"
      class="v-btn v-btn--floating v-btn--left v-btn--small theme--light mercator-color"
    >
      <div class="v-btn__content">
        <i aria-hidden="true" v-if="!isPlaying" class="v-icon material-icons theme--light" @click="onPlay()">play_arrow</i>
        <i aria-hidden="true" v-if="isPlaying" class="v-icon material-icons theme--light" @click="onStop()">pause</i>
      </div>
    </button>

    <select
      class="v-btn v-btn--left v-btn--small theme--light mercator-color"
      style="transform: translateY(.5rem);font-weight: bold; border-radius:10px;"
      list="daysEnabled" 
      id="hourlyDays" 
      name="hourlyDays"
      v-model="selectedHourlyDay"
      @change="changeHourlyDay($event)"
    >
      <option v-for="(item) in hourlyDays" :key="item" :value="item">{{ item }}</option>
    </select>

    <select
      v-if="isHourly"
      class="v-btn v-btn--left v-btn--small theme--light mercator-color"
      style="transform: translateY(.5rem);font-weight: bold; border-radius:10px;"
      list="hoursEnabled" 
      id="hours" 
      name="hours"
      v-model="selectedHour"
      @change="changeHour($event)"
    >
      <option v-for="(item) in hours" :key="item" :value="item">{{ item }} UTC+0</option>
    </select>

    <select
      v-if="isHourly"
      class="v-btn v-btn--left v-btn--small theme--light mercator-color"
      style="transform: translateY(.5rem);font-weight: bold; border-radius:10px;"
      id="intervals" 
      name="intervals"
      v-model="selectedInterval"
    >
      <option v-for="(item) in intervals" :key="item.value" :value="item.value">{{ item.text }} {{ $t('hour') }}{{ item.sufix }}</option>
    </select>

    <button
      id="time-skip--forward"
      type="button"
      class="v-btn v-btn--floating v-btn--small theme--light mercator-color"
      style="margin-left: 1.5rem;"
      @click="onForward()"
    >
      <div class="v-btn__content">
        <i aria-hidden="true" class="v-icon material-icons theme--light">fast_forward</i>
      </div>
    </button>
    <div v-if="isLoading" class="position--fixed centering overlay">
        <v-progress-circular  
          :rotate="-90"
          :size="100"
          :width="15"
          :value="loaderValue"
          color="primary"
        >
        {{ loaderValue }} %
        </v-progress-circular>
      <!-- <h3 class="loader--text">Baixando...</h3> -->
    </div>
    
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { tileLayer, map } from 'leaflet';

@Component({
    components: {},
})
export default class MapTimeSkip extends Vue {
  public isPlaying = false;
  public selectedDay = '1';
  public selectedDate = new Date().toISOString().substr(0, 10);
  public pickerIsVisible = false;
  public days: any = { dates: [], name: '' };
  public selectedHourlyDay: any = '';
  public oldValue = '';
  public selectedHour = '00:00';
  public hourOldValue = '';
  public loaderValue = 0;
  public isLoading = false;
  public isNew = true;
  public layerVisibility = true;
  public intervals: any[] = [];

  public selectedInterval = 1;

  @Prop() public currentLayer: any;
  @Prop() public map!: any;

  private lastLayerSelectedIndex = 0;
  private interval: any = -1;
  private cachedLayers: any[] = [];

  public onPlay() {
    this.isPlaying = true;
    let isFirst = true;
    this.loaderValue = 0;
    const increaseValue = Math.floor(100 / (this.days.dates.length / this.selectedInterval ));
    this.isLoading = true;
    this.interval = setInterval(() => {
      this.onForward();
      if (!isFirst) {
        return;
      }

      if ((this.loaderValue + increaseValue) >= 100) {
        isFirst = false;
        this.isLoading = false;
        this.loaderValue = 0;
        return;
      }
      this.loaderValue += increaseValue;
    }, 3000);
  }

  public onStop() {
    this.isPlaying = false;
    this.isLoading = false;
    clearInterval(this.interval);
  }

  public onForward() {
    let day = (parseInt(this.selectedDay, 10) + this.selectedInterval);

    if (day > this.days.dates.length) {
      day = 0;
    }

    this.selectedDay =  day + '';
    // this.map.timeDimension.nextTime();
    this.setLayerDate();
  }

  public onRewind() {
    let day = (parseInt(this.selectedDay, 10) - this.selectedInterval);

    if (day <= 0) {
      day = this.days.dates.length;
    }

    this.selectedDay =  day + '';
    // this.map.timeDimension.previousTime();
    this.setLayerDate();
  }

  public get isHourly() {
    const dates = this.days.dates;
    if (!dates[0] || !dates[1]) {
      return false;
    }
    return 86400000 > ((+new Date(dates[1])) - (+new Date(dates[0])));
  }

  public get isShown() {
    return this.hourlyDays.length > 1 && this.layerVisibility;
  }

  public get hourlyDays() {
    return Array.from(new Set(this.days.dates.map((e: any) => this.formatDate(new Date(e)))));
  }

  public get hours() {
    return this.days.dates
      .filter((e: any) => this.formatDate(e) === this.selectedHourlyDay)
      .map((item: any) => this.formatHour(new Date(item)))
      .sort();
  }

  public changeHourlyDay($event: any) {
    this.oldValue = this.selectedHourlyDay;
    const [day, month, year] = this.selectedHourlyDay.split('/');
    this.selectedDate = (new Date(`${year}-${month}-${day}T00:00`)).toISOString().substr(0, 10);
    this.onDateChange();
    setTimeout(() => {
      $event.target.blur();
      this.selectedHour = this.hours[0];
    }, 300);
  }

  public changeHour($event: any) {
    this.hourOldValue = this.selectedHour;
    const [day, month, year] = this.selectedHourlyDay.split('/').map(parseInt);
    const [hour, minutes] = this.selectedHour.split(':').map(parseInt);
    this.selectedDate = (new Date(year, month - 1, day, hour, minutes)).toISOString();
    this.onDateChange();
    setTimeout(() => {
      $event.target.blur();
    }, 300);
  }

  public setDay(index: number, $event?: any) {
    this.selectedDay = `${index + 1}`;
    this.setLayerDate($event);
  }

  public formatDate(date: string|Date, plus?: number) {
    const insertZero = (n: number) => n < 10 ? '0' + n : n;
    const dateObject = new Date(date);
    dateObject.setDate(dateObject.getDate() + (plus || 0));
     const options = {
          year: 'numeric', month: 'numeric', day: 'numeric'
      } as const;
      const formatter = new Intl.DateTimeFormat('pt-BR', options);
    return formatter.format(dateObject);
  }

  public formatHour(date: string|Date) {
    const dateObject = new Date(date);
    const insertZero = (n: number) => n < 10 ? '0' + n : n;
    return `${insertZero(dateObject.getUTCHours())}:${insertZero(dateObject.getUTCMinutes())}`;
  }

  public setLayerDate($event?: any) {
    if (!this.currentLayer) {
      return;
    }

    const index = parseInt(this.selectedDay, 10);
    const date = new Date(this.days.dates[index]);
    if (isNaN(date.getTime())) {
      return;
    }
    this.selectedDate = this.isHourly ? date.toISOString() : date.toISOString().substr(0, 10);
    // this.currentLayer.setParams({  time: this.selectedDate  }, false);
    this.changeLayerVisible(this.lastLayerSelectedIndex, index, {  time: date.toISOString() });
    this.lastLayerSelectedIndex = index;

    if (!this.isHourly) {
      this.selectedHourlyDay = this.formatDate(date);
      this.$store.dispatch('setLayerHour', { date: this.selectedHourlyDay, hour: null });        
    } else {
      this.selectedHourlyDay = this.formatDate(date, 1);
      this.selectedHour = this.formatHour(date);
      this.$store.dispatch('setLayerHour', { date: this.selectedHourlyDay, hour: this.selectedHour });      
    }
    this.onDateChange();
    this.$store.dispatch('setLayerDate', this.selectedHourlyDay);

    if (!!$event) {
      $event.target.scrollIntoView();
    }
  }

  public isDateAllowed(date: string) {
    return !!this.days.dates.find((day: string) => new Date(day).toISOString().substr(0, 10) === date);
  }

  public onDateChange() {
    const day = this.days.dates
      .findIndex((date: string) => {
        const value = new Date(date);
        return (this.isHourly ? value.toISOString() : value.toISOString().substr(0, 10)) === this.selectedDate;
      });
    this.selectedDay =  day + '';
    this.pickerIsVisible = false;
  }

  public mounted() {
    this.$store.subscribe(({ type }, state) => {
      if (type === 'SET_SELECTED_LAYER') {
        this.days = state.selectedLayer;
        this.selectedHourlyDay = this.hourlyDays[0];
        const today = new Date();
        const todayFormatted = this.formatDate(today);
        if (this.hourlyDays.includes(todayFormatted)) {
          this.selectedHourlyDay = todayFormatted;
          this.selectedDate = this.isHourly ? `${today.toISOString().substr(0, 10)}T00:00:00.000Z`: today.toISOString().substr(0, 10);
          const day = this.days.dates
            .findIndex((date: string) => {
              return date.includes(this.selectedDate);
            });
          this.lastLayerSelectedIndex = day;
          this.selectedDay =  day + '';
        }
        
        this.isNew = true;
        if (!!this.interval) {
          clearInterval(this.interval);
        }

        this.isPlaying = false;
        this.isLoading = false;
      }

      if (type === 'SET_LAYER_VISIBILITY') {
        this.layerVisibility = state.layerVisibility;
      }
    });

    this.setLayerDate();

    this.intervals = [
      {
        text: `1`,
        sufix: '',
        value: 1,
      },
      {
        text: `3`,
        sufix: 's',
        value: 3,
      },
      {
        text: `6`,
        sufix: 's',
        value: 6,
      },
      {
        text: `12`,
        sufix: 's',
        value: 12,
      },
      {
        text: `24`,
        sufix: 's',
        value: 24,
      }
    ];
  }

  private changeLayerVisible(oldIndex: number, index: number, date: any) {
    if (!!this.cachedLayers[oldIndex]) {
        this.cachedLayers[oldIndex].setOpacity(0);
    }

    if (this.map.hasLayer(this.cachedLayers[index])) {
        this.cachedLayers[index].setOpacity(1);
        return;
    }
    this.currentLayer.setOpacity(0);
    const layer = tileLayer.wms(this.currentLayer._url, Object.assign({}, this.currentLayer.options));
    layer.setParams(date, false);
    this.map.addLayer(layer);
    this.cachedLayers[index] = layer;
    this.currentLayer.setOpacity(1);
    this.$store.dispatch('setCachedLayers', { layers: this.cachedLayers, name: this.days.name });
  }
}
</script>

<style lang="scss" scoped>
.date-selection {
    display: block;
    width: 100%;
    overflow-x: auto;
    overflow-y: hidden;
    min-height: 7rem;
}

.time-skip{
  position: fixed;
  bottom: 5vh;
  z-index: 99999;
  left: 0;
  width: 98vw;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

.position--fixed {
  position: fixed;
  z-index: 9999999;
  margin: 0 auto;
  top: 40vh;
  bottom: 40vh;
  left: 40vw;
  right: 40vw;
}

.centering {
  justify-content: center;
  align-items: center;
  display: flex;
  flex-direction: column;
}

.overlay {
  // background: rgba(255, 255, 255, 0.92);
  border-radius: 5px;
}

.loader--text {
  text-transform: uppercase;
  color: #4e76ed;
 }

@media (max-width: 768px) {
  .range, .range-labels { display: none; }
  #date-selector { 
    width: 90vw; 
    transform: translateY(-4rem) !important;
    margin-left: 0 !important;
    padding: 1rem 0;
    height: 3rem;
  }
}
</style>
