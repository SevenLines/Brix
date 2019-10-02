import {Dictionary} from "vuex";

export interface BrixModule {
    id: number,
    title: string,
    date_start: Date,
    date_end: Date,
    kont_id: number
}

export interface BrixRaspnagrToModule {
    id: number
    raspnagr_id: number
    module_id: number
    hours: number
}

export interface Raspnagr {
    id: number
    discipline: string
    teacher: number
    groups_title: string,
    hours: number,
    nt: number,
}

export interface Teacher {
    id: number,
    full_name: string,
    short_name: string,
}

export interface Kontkurs {
    id: number
    title: string
    depth?: number
    kont?: number,
    groups?: Dictionary<Kontkurs>
}

export interface RootState {

}

export interface BrixModuleState {
    konts: Dictionary<Kontkurs>,
    teachers: Dictionary<Teacher>
}