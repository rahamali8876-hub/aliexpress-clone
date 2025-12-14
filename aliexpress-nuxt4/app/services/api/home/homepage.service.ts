// ~/services/api/homepage.service.ts

import { useNuxtApp } from "#app"

const BASE = "/homepage/"

export async function getHomepageData() {
    const { $api } = useNuxtApp()

    try {
        const res = await $api.get(BASE)
        console.log('is data or not SERVICE ----------->>>>>>>>>>', res);
        console.log('data ', res.data);
        console.log('data banner ', res.data.banners[0].title);
        console.log('data.data', res.data.data);
        return {
            success: true,
            data: res.data
        }
    } catch (error: any) {
        return {
            success: false,
            error
        }
    }
}
