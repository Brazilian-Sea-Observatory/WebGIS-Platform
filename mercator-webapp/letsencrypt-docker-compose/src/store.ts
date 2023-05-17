import Vue from 'vue';
import Vuex from 'vuex';
import { i18n } from './i18n';
import BucketService from './providers/bucket.service';
import UserService from './providers/user.service';
import WindService from './providers/wind.service';
import * as echarts from 'echarts';

Vue.use(Vuex);

const bucket = new BucketService();
const authService = new UserService();

export default new Vuex.Store({
    state: {
        lang: 'Português',
        isLogged: !!bucket.getValue('accessKey'),
        selectedLayers: new Map([
            ['World Imagery with labels', true],
            ['World Imagery', true],
        ]),
        mapCenter: [],
        bucket,
        isDialogOpen: false,
        user: null,
        layersMetadata: [],
        selectedLayer: null,
        popupConfig: true,
        selectedDate: (echarts as any).format.formatTime('dd/MM/yyyy', new Date()) as string,
        selectedHour: null,
        layers: [],
        stationData: { metadata: {}, values: { temperature: [], salinity: [], depth: [] } },
        pointData: [],
        layerVisibility: true,
        mapModel: 'global',
    },
    mutations: {
        SET_LANG(state, payload) {
            const langs = new Map([
                ['English', 'en'],
                ['Français', 'fr'],
                ['Português', 'pt'],
            ]);
            i18n.locale = langs.get(payload) as string;
            state.lang = payload;
        },
        SET_CENTER(state, payload) {
            state.mapCenter = payload;
        },
        addLayer(state, payload) {
            state.selectedLayers.set(payload, true);
        },
        removeLayer(state, payload) {
            state.selectedLayers.set(payload, false);
        },
        SET_USER_KEYS(state, payload) {
            state.isLogged = true;
            state.user = payload.user;
            state.bucket.save('accessKey', payload.jwt);
            state.bucket.save('refreshKey', payload.jwt);
        },
        CREATE_USER(state, payload) {
            state.isDialogOpen = !payload;
        },
        SET_METADATA(state, payload) {
            state.layersMetadata = payload;
        },
        SET_SELECTED_LAYER(state, payload) {
            state.selectedLayer = payload;
        },
        SET_LAYERS(state, payload) {
            state.layers = payload;
        },
        UPDATE_CACHED_LAYERS(state, payload) {
            const index = state.layers.findIndex((layer: any) => layer.layers === payload.name);
            if (!!state.layers[index]) {
                (state.layers[index] as any).cachedLayers = payload.layers;
            }
        },
        SET_STATION_VIEW(state, { metadata, values }) {
            const transformData = (e: any) => ({
                date: new Date(e.time).toLocaleString(),
                value: parseFloat(e.value.toFixed(3)),
            });
            state.stationData = {
                metadata,
                values: {
                    temperature: values.temperature.map(transformData),
                    salinity: values.salinity.map(transformData),
                    depth: values.depth.map(transformData),
                },
            };
        },
        SET_LAYER_DATE(state, payload: string) {
            state.selectedDate = payload;
        },
        SET_LAYER_HOUR(state, payload: any) {
            state.selectedDate = payload.date;
            state.selectedHour = payload.hour;
        },
        SET_VESSEL_VIEW(state, payload: boolean) {},
        SET_POINT_VIEW(state, payload) {
            state.pointData = payload;
        },
        SET_LAYER_VISIBILITY(state, payload) {
            state.layerVisibility = payload;
        },
        SET_MAP_MODEL(state, payload) {
            state.mapModel = payload;
        },
    },
    actions: {
        setLang(context, payload: string) {
            context.commit('SET_LANG', payload);
        },
        setAccount(context, payload) {
            context.commit('setUserProfile', payload);
        },
        setCenter(context, payload) {
            context.commit('SET_CENTER', payload);
        },
        auth(context, credentials) {
            return authService.signIn(credentials).then((res: any) => {
                context.commit('SET_USER_KEYS', res);
            });
        },
        createUser(context, user) {
            return authService
                .signUp(user)
                .then((res: any) => {
                    context.commit('CREATE_USER', res);
                });
        },
        setLayersMetadata(context) {
            // const promises = ['mercator', 'regional_model'].map((e) =>
            const promises = [''].map((e) =>
                fetch(
                    // tslint:disable-next-line:max-line-length
                    // `${process.env.VUE_APP_BASE_URL}/ows?service=wms&version=1.3.0&request=GetCapabilities&namespace=${e}`,
                    `${process.env.VUE_APP_BASE_URL}/ows?service=wms&version=1.3.0&request=GetCapabilities`,
                ).then((res) => res.text()),
            );

            Promise.all(promises).then((values) => {
                const response = values.map((data) => {
                    const div = document.createElement('div');
                    div.innerHTML = data.replace('<?xml version="1.0" encoding="UTF-8"?>', '');
                    return [...div.querySelectorAll('Layer[queryable]')].map((layer: any) => {
                        return {
                            dates: (layer.querySelector('Dimension[name="time"]') || { innerHTML: '' })
                                .innerHTML.split(',').sort(),
                            name: (layer.querySelector('Name') || { innerHTML: '' }).innerHTML,
                            title: (layer.querySelector('Title') || { innerHTML: '' }).innerHTML,
                            symbol: (layer.querySelector('Abstract') || { innerHTML: '' }).innerHTML,
                            legend: (layer.querySelector('LegendURL OnlineResource') || { getAttribute: () => '' })
                                .getAttribute('xlink:href'),
                        };
                    });
                });
                context.commit('SET_METADATA', response.reduce((p: any[], c: any[]) => [...p, ...c], []));
            });
        },
        setSelectedLayer(context, payload: string) {
            context.commit('SET_SELECTED_LAYER', payload);
        },
        setLayers(context, payload) {
            context.commit('SET_LAYERS', payload);
        },
        setCachedLayers(context, payload) {
            context.commit('UPDATE_CACHED_LAYERS', payload);
        },
        setStationData(context, payload) {
            context.commit('SET_STATION_VIEW', payload);
        },
        setLayerDate(context, payload) {
            context.commit('SET_LAYER_DATE', payload);
        },
        setLayerHour(context, payload) {
            context.commit('SET_LAYER_HOUR', payload);
        },
        setVesselView(context) {
            context.commit('SET_VESSEL_VIEW', false);
        },
        setPointView(context, payload) {
            context.commit('SET_POINT_VIEW', payload);
        },
        isLayerVisible(context, payload) {
            context.commit('SET_LAYER_VISIBILITY', payload);
        },
        setMapModel(context, payload) {
            context.commit('SET_MAP_MODEL', payload);
        },
    },
    getters: {
        getLayers: (state: any) => () => state.selectedLayers,
        isLoggedIn: (state: any) => () => state.isLogged,
        getTimeData: (state: any) => () => state.layersMetadata,
        getSelectedLayer: (state: any) => () => state.selectedLayer,
        getPopupConfig: (state: any) => () => state.popupConfig,
        getAllLayers: (state: any) => () => state.layers,
        getLayerVisibility: (state: any) => () => state.layerVisibility,
        getMapModel: (state: any) => () => state.mapModel,
        getWindDates: () => () => {
            // return null;
            return WindService.getAvailableDates();
        },
    },
});
