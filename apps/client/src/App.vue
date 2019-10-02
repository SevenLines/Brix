<template>
    <b-container>
        <b-navbar toggleable="lg">
            <b-navbar-brand to="/">БИ БРИКС</b-navbar-brand>
            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav>
                    <b-nav-item to="/modules" active-class="active">
                        Настройка модулей
                    </b-nav-item>
                </b-navbar-nav>
            </b-collapse>
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
