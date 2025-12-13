// ~/stores/homepage.store.ts

import { defineStore } from "pinia"
import { getHomepageData } from "~/services/api/home/homepage.service"
import type {
    HomepageSection,
    Banner,
    Category,
    Product,
    Promotion
} from "~/types/homepage"

export const useHomepageStore = defineStore("homepage", () => {
    const sections = ref<HomepageSection[]>([])
    const loading = ref(false)
    const error = ref<Error | null>(null)

    async function fetchHomepage() {
        loading.value = true
        error.value = null

        try {
            const res = await getHomepageData()

            if (!res.success) {
                throw new Error("Failed to load homepage")
            }

            const data = res.data

            sections.value = [
                { type: "hero", data: data.hero ?? null },
                { type: "banner", data: data.banners ?? [] },
                { type: "categories", data: data.categories ?? [] },
                { type: "products", data: data.featured_products ?? [] },
                { type: "promo", data: data.promotions ?? [] },
                { type: "testimonials", data: data.testimonials ?? [] }
            ]
        } catch (e: any) {
            error.value = e
        } finally {
            loading.value = false
        }
    }

    /* =====================
       SECTION SELECTORS
    ===================== */

    const getSection = <T>(type: HomepageSection["type"]) =>
        computed(() =>
            sections.value.find(s => s.type === type)?.data as T | null
        )

    return {
        sections,
        loading,
        error,
        fetchHomepage,
        getSection
    }
})
