<template>
    <b-container>
        <b-navbar toggleable="lg" >
            <b-navbar-brand to="/" >БИ БРИКС</b-navbar-brand>
            <b-navbar-nav>
                <b-nav pills>
                    <b-nav-item to="/modules" active-class="active">
                        Настройка модулей
                    </b-nav-item>
                </b-nav>
            </b-navbar-nav>
        </b-navbar>
        <div id="app">

            <router-view></router-view>
        </div>
    </b-container>

</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';

    @Component({})
    export default class App extends Vue {
    }
</script>

<style lang="scss">
    @import '~bootstrap/scss/bootstrap';
    @import '~bootstrap-vue/src/index.scss';
</style>
