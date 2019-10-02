<template>
    <div v-if="kont">
        <b-table striped hover small responsive
                 sticky-header="70vh"
                 :fields="tableData.fields"
                 :items="tableData.items"
                 :busy="isLoading"
        >
            <template v-slot:thead-top="data">
                <b-tr>
                    <b-th colspan="4" variant="light">Нагрузка</b-th>
                    <b-th colspan="4" variant="info">Модули</b-th>
                </b-tr>
            </template>

            <template v-slot:cell(discipline)="data">
                <small> {{data.value}}</small>
            </template>

            <template v-slot:cell(module_1)="data">
                <modules-editor-table-module-item data="data" @click="moduleItemClicked"/>
            </template>
            <template v-slot:cell(module_2)="data">
                <modules-editor-table-module-item data="data" @click="moduleItemClicked"/>
            </template>
            <template v-slot:cell(module_3)="data">
                <modules-editor-table-module-item data="data" @click="moduleItemClicked"/>
            </template>
            <template v-slot:cell(module_4)="data">
                <modules-editor-table-module-item data="data" @click="moduleItemClicked"/>
            </template>

            <template v-slot:cell(teachers)="data">
                <div v-for="i in data.item.teachers">
                    <b-badge variant="light">
                        {{i.groups_title}} <span v-if="i.teacher">{{i.teacher.short_name}}</span>
                    </b-badge>
                </div>
            </template>

            <template v-slot:table-busy>
                <div class="text-center text-danger my-2">
                    <b-spinner class="align-middle"></b-spinner>
                    <strong> Гружу...</strong>
                </div>
            </template>
        </b-table>

    </div>
</template>

<script lang="ts">
    import {State, Action, Getter} from 'vuex-class'
    import {Component, Prop, Vue, Watch} from 'vue-property-decorator'
    import {Dictionary} from 'vuex'
    import {Kontkurs, Raspnagr, Teacher} from '@/types'
    import axios from 'axios';
    import _ from 'lodash';
    import ModulesEditorTableModuleItem from "@/components/ModulesEditorTableModuleItem.vue";

    const namespace: string = 'brix_module';
    @Component({
        components: {ModulesEditorTableModuleItem}
    })
    export default class ModulesEditorTable extends Vue {
        @State('konts', {namespace}) konts?: Dictionary<Kontkurs>;
        @State('teachers', {namespace}) teachers?: Dictionary<Teacher>;
        @Prop() private kont!: Kontkurs;

        private NORMTYPES: Dictionary<{ title: string, klass: string }> = {
            1: {title: "лекция", klass: ""},
            2: {title: "практика", klass: ""},
            3: {title: "лаба", klass: ""},
        }

        private nagruzka: Array<Raspnagr> = [];
        private isLoading = false;

        get tableData(): any {
            return {
                fields: [
                    {
                        key: 'discipline',
                        label: 'Предмет',
                        sortable: true,
                    },
                    {
                        key: 'nt_title',
                        label: 'Тип',
                        sortable: true,
                    },
                    {
                        key: 'teachers',
                        label: 'Преподаватель',
                        sortable: false,
                        formatter(items: any) {
                            let result = _(items).map(i => {
                                return `${i.groups_title} ${i.teacher.short_name}`
                            }).join("<br>");
                            return result
                        },
                    },
                    {
                        key: 'hours',
                        label: 'Часы',
                    },
                    {
                        key: 'module_1',
                        label: '1',
                        thStyle: "text-align: center",
                    },
                    {
                        key: 'module_2',
                        label: '2',
                        thStyle: "text-align: center",
                    },
                    {
                        key: 'module_3',
                        label: '3',
                        thStyle: "text-align: center",
                    },
                    {
                        key: 'module_4',
                        label: '4',
                        thStyle: "text-align: center",
                    },
                ],
                items: _(this.nagruzka).groupBy(i => `${i.discipline}_${i.nt}`).map((items, key) => {
                        let discipline = items[0].discipline;
                        let nt = items[0].nt;
                        let teachers = items.map(i => {
                            let teacher = this.teachers ? this.teachers[i.teacher] || {} : {};
                            return {
                                ...i,
                                'teacher': teacher,
                            }
                        });

                        let hours: any = _(items).map("hours").max();
                        return {
                            discipline,
                            teachers,
                            hours,
                            nt_title: this.NORMTYPES[nt].title,
                            nt_class: this.NORMTYPES[nt].klass,
                        }
                    }
                ).value()
            }
        }

        @Watch("kont", {immediate: true})
        async onKontChange() {
            if (this.kont) {
                this.isLoading = true;
                let r = await axios.get("/api/brix/nagruzka", {
                    params: {
                        kont_id: this.kont.id
                    }
                });
                this.isLoading = false;
                this.nagruzka = r.data;
            }
        }

        moduleItemClicked(e: any) {
            console.log(e);
        }

    }
</script>

<style scoped lang="scss">

</style>