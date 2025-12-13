// ~/services/api/homepage.service.ts

import { useNuxtApp } from "#app"

const BASE = "/homepage/"

export async function getHomepageData() {
    const { $api } = useNuxtApp()

    try {
        const res = await $api.get(BASE)
        return {
            success: true,
            data: res.data.data
        }
    } catch (error: any) {
        return {
            success: false,
            error
        }
    }
}
