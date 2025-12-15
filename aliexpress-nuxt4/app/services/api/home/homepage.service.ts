// // ~/services/api/homepage.service.ts

// import { useNuxtApp } from "#app"

// const BASE = "/homepage/"

// export async function getHomepageData() {
//     const { $api } = useNuxtApp()

//     try {
//         const res = await $api.get(BASE)
//         console.log('is data or not SERVICE ----------->>>>>>>>>>', res);
//         console.log('data ', res.data);
//         console.log('data banner ', res.data.banners[0].title);
//         console.log('data.data', res.data.data);
//         return {
//             success: true,
//             data: res.data
//         }
//     } catch (error: any) {
//         return {
//             success: false,
//             error
//         }
//     }
// }


import { useNuxtApp } from "#app"
import { normalizeResponse, handleApiError } from "~/utils/api/base"
import type {
    Banner,
    Category,
    Product,
    Promotion
} from "~/types/homepage"

export interface HomepagePayload {
    hero?: any
    banners: Banner[]
    categories: Category[]
    featured_products: Product[]
    promotions: Promotion[]
    testimonials?: any[]
}

const ENDPOINT = "/homepage/"

/**
 * Fetch homepage aggregated data
 * --------------------------------
 * - Runs on server or client
 * - Always returns normalized response
 */
export async function getHomepageData() {
    const { $api } = useNuxtApp()

    try {
        const res = await $api.get(ENDPOINT)

        return normalizeResponse<HomepagePayload>(res)
    } catch (error) {
        return handleApiError(error)
    }
}
