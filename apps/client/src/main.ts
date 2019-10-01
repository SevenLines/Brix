import Vue from 'vue'
import App from './App.vue'
import store from './store'
import VueRouter from 'vue-router'
import ModulesEditor from './components/ModulesEditor.vue';
import BootstrapVue from 'bootstrap-vue'


Vue.use(BootstrapVue)
Vue.use(VueRouter);

Vue.config.productionTip = false;

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/modules',
      component: ModulesEditor,
    }
  ]
});

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app');
