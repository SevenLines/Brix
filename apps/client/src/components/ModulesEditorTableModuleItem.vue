<template>
    <div class="module-item">
        <div class="item-button">
            <i class="fa fa-plus" v-if="!hours"></i>
        </div>
    </div>
</template>

<script lang="ts">
    import {State, Action, Getter} from 'vuex-class'
    import {Component, Prop, Vue, Watch} from 'vue-property-decorator'
    import {Dictionary} from 'vuex'
    import {Kontkurs, Raspnagr, Teacher} from '@/types'
    import axios from 'axios';
    import _ from 'lodash';

    const namespace: string = 'brix_module';
    @Component({})
    export default class ModulesEditorTableModuleItem extends Vue {
        @Prop() private hours!: number;

    }
</script>

<style scoped lang="scss">
    .module-item {
        color: silver;
        cursor: pointer;
        border-top: 2px solid silver;

        .item-button {
            width: 40px;
            height: 40px;
            margin: 0 0.25em;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;

            &:hover {
                background-color: silver;
                color: black;
            }
        }
    }
</style>