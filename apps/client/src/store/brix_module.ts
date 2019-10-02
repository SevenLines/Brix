import {BrixModuleState, Kontkurs, RootState, Teacher} from "@/types";
import {ActionTree, Dictionary, Module, MutationTree} from "vuex";
import axios from 'axios'

export const state: BrixModuleState = {
    konts: {},
    teachers: {}
};


export const mutations: MutationTree<BrixModuleState> = {
    setKonts(state, payload: Dictionary<Kontkurs>) {
        state.konts = payload;
    },
    setTeachers(state, payload: Dictionary<Teacher>) {
        state.teachers = payload;
    },
};

export const actions: ActionTree<BrixModuleState, RootState> = {
    async fetchKonts({commit}) {
        let r = await axios.get('/api/brix/konts');
        commit('setKonts', r.data);
    },
    async fetchTeachers({commit}) {
        let r = await axios.get('/api/common/teachers');
        commit('setTeachers', r.data);
    },
};

export const brix_module: Module<BrixModuleState, RootState> = {
    namespaced: true,
    state,
    mutations,
    actions,
};