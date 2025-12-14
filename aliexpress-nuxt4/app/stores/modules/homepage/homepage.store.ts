// // ~/stores/homepage.store.ts

// import { defineStore } from "pinia"
// import { getHomepageData } from "~/services/api/home/homepage.service"
// import type { HomepageSection } from "~/types/homepage"

// export const useHomepageStore = defineStore("homepage", () => {
//     const sections = ref<HomepageSection[]>([])
//     const loading = ref(false)

//     // ✅ POJO ONLY
//     const error = ref<{ message: string } | null>(null)

//     async function fetchHomepage() {
//         loading.value = true
//         error.value = null

//         try {
//             const res = await getHomepageData()
//             console.log('is data or not STORE ----------->>>>>>>>>>', res);

//             if (!res.success) {
//                 throw new Error("Failed to load homepage")
//             }

//             const data = res.data


//             sections.value = [
//                 { type: "hero", data: data.hero ?? null },
//                 { type: "banner", data: data.banners ?? [] },
//                 { type: "categories", data: data.categories ?? [] },
//                 { type: "products", data: data.featured_products ?? [] },
//                 { type: "promo", data: data.promotions ?? [] },
//                 { type: "testimonials", data: data.testimonials ?? [] }
//             ]
//         } catch (e: any) {
//             // ✅ SERIALIZABLE ERROR
//             error.value = {
//                 message: e?.message || "Unknown error"
//             }
//         } finally {
//             loading.value = false
//         }
//     }

//     const getSection = (type: HomepageSection["type"]) =>
//         computed(() => sections.value.find(s => s.type === type)?.data ?? null)

//     return {
//         sections,
//         loading,
//         error,
//         fetchHomepage,
//         getSection
//     }
// })




import { defineStore } from "pinia"
import { getHomepageData } from "~/services/api/home/homepage.service"
import type { HomepageSection } from "~/types/homepage"

export const useHomepageStore = defineStore("homepage", () => {
    const sections = ref<HomepageSection[]>([])
    const loading = ref(false)
    const error = ref<{ message: string } | null>(null)

    /**
     * Fetch homepage data (SSR/CSR safe)
     */
    async function fetchHomepage() {
        loading.value = true
        error.value = null

        try {
            const res = await getHomepageData()

            if (!res.success || !res.data) {
                throw new Error(res.message || "Failed to load homepage")
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
            error.value = { message: e.message || "Unknown error" }
        } finally {
            loading.value = false
        }
    }

    /**
     * Section selector
     */
    function getSection(type: HomepageSection["type"]) {
        return computed(
            () => sections.value.find(s => s.type === type)?.data ?? null
        )
    }

    return {
        sections,
        loading,
        error,
        fetchHomepage,
        getSection
    }
})
