import Vue from 'vue'
import Vuex, {StoreOptions} from 'vuex'
import {RootState} from "@/types";
import {brix_module} from "./brix_module"

Vue.use(Vuex);

const store: StoreOptions<RootState> = {
    modules: {
        brix_module
    }
};

export default new Vuex.Store(store)