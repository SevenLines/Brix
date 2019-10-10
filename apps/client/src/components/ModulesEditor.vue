<template>
    <div>
        <div>
            <div class="float-left">
                <b-nav pills align="left">
                    <b-nav-item v-for="kont in konts"
                                :active="activeKont === kont"
                                @click="activeKont = kont"
                    >
                        {{kont.title}}
                    </b-nav-item>
                </b-nav>
            </div>

<!--            <div class="float-right" v-if="activeKont">-->
<!--                <b-btn variant="info" v-b-modal.modal-modules>-->
<!--                    <i class="fa fa-edit"></i> Настроить модули-->
<!--                </b-btn>-->
<!--            </div>-->
        </div>
        <div class="clearfix"></div>

        <p></p>
        <modules-editor-table :kont="activeKont"/>


        <b-modal id="modal-modules" title="BootstrapVue">
            <p class="my-4">Hello from modal!</p>
        </b-modal>
    </div>
</template>

<script lang="ts">
    import {State, Action, Getter} from 'vuex-class'
    import {Component, Vue} from 'vue-property-decorator'
    import {Dictionary} from 'vuex'
    import {Kontkurs} from '@/types'
    import ModulesEditorTable from "@/components/ModulesEditorTable.vue"

    const namespace: string = 'brix_module';
    @Component({
        components: {
            ModulesEditorTable
        }
    })
    export default class ModulesEditor extends Vue {
        @State('konts', {namespace}) konts?: Dictionary<Kontkurs>;
        @Action("fetchKonts", {namespace}) fetchKonts: any;
        @Action("fetchTeachers", {namespace}) fetchTeachers: any;

        private activeKont: Kontkurs | null = null;

        mounted() {
            this.fetchKonts();
            this.fetchTeachers();
        }
    }
</script>

<style scoped>

</style>