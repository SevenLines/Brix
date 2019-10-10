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


            <template v-for="(m, module_id) in modules" v-slot:[`cell(module_${module_id})`]="data">
                <modules-editor-table-module-item
                        data="data"
                        @clicked="moduleItemClicked"
                        @hours-changed="onHoursChanged(module_id, data)"
                />
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
    import {Kontkurs, Module, Raspnagr, Teacher} from '@/types'
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
        private modules: Dictionary<Module> = {};
        private modulesToRaspnagr: Dictionary<any> = {};
        private isLoading = false;

        get tableData(): any {
            let result: any = {
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
                ],
                items: _(this.nagruzka).groupBy(i => `${i.discipline}_${i.nt}`).map((items, key) => {
                        let discipline = items[0].discipline;
                        let nt = items[0].nt;
                        let raspnagr_id = items[0].raspnagr_ids[0];

                        let teachers = items.map(i => {
                            let teacher = this.teachers ? this.teachers[i.teacher] || {} : {};
                            return {
                                ...i,
                                'teacher': teacher,
                            }
                        });

                        let hours: any = _(items).map("hours").max();

                        let out: any = {
                            discipline,
                            teachers,
                            hours,
                            raspnagr_ids: _(items).map(i => i.raspnagr_ids).flat().values(),
                            nt_title: this.NORMTYPES[nt].title,
                            nt_class: this.NORMTYPES[nt].klass,
                        };

                        _(this.modules).map(i => i).forEach((m: Module) => {
                            out[`module_${m.id}`] = _.get(
                                this.modulesToRaspnagr,
                                `${raspnagr_id}.${m.id}`,
                                {
                                    'hours': 0,
                                },
                            );
                        });

                        return out
                    }
                ).value()
            };

            // bind modules
            _(this.modules).map(i => i).orderBy("title").forEach((m: Module) => {
                result.fields.push({
                    key: `module_${m.id}`,
                    label: m.title,
                },)
            });

            return result;
        }

        async loadModules() {
            let r = await axios.get("/api/brix-modules/get-for-kont", {
                params: {
                    kont_id: this.kont.id
                }
            });

            this.modules = r.data;
        }

        async loadModulesForRaspnagr() {
            let r = await axios.get("/api/brix-modules/get-hours-for-kont", {
                params: {
                    kont_id: this.kont.id
                }
            });

            this.modulesToRaspnagr = r.data;
        }

        async loadNagruzka() {
            let r = await axios.get("/api/brix/nagruzka", {
                params: {
                    kont_id: this.kont.id
                }
            });

            this.nagruzka = r.data;
        }

        @Watch("kont", {immediate: true})
        async onKontChange() {
            if (this.kont) {
                this.isLoading = true;

                await Promise.all([
                    this.loadNagruzka(),
                    this.loadModules(),
                    this.loadModulesForRaspnagr(),
                ]);

                this.isLoading = false;
            }
        }

        moduleItemClicked(e: any) {
        }

        onHoursChanged(module_id: number, data: any) {
            console.log(data)
        }

    }
</script>

<style scoped lang="scss">

</style>