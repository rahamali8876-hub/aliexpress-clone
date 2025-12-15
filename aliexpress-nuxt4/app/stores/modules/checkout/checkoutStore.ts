
// import { defineStore } from "pinia"
// import { ref } from "vue"
// import { createCheckout } from "~/services/api/checkout/checkout.service"

// export const useCheckoutStore = defineStore("checkout", () => {
//     const checkout = ref<any>(null)
//     const loading = ref(false)
//     const error = ref<string | null>(null)

//     /**
//      * Start checkout from cart
//      * ------------------------
//      * - Requires cart items
//      * - Backend validates cart
//      */
//     async function startCheckout() {
//         loading.value = true
//         error.value = null

//         try {
//             const res = await createCheckout()

//             if (!res.success || !res.data) {
//                 throw new Error(res.message || "Checkout failed")
//             }

//             checkout.value = res.data
//             return res.data
//         } catch (e: any) {
//             error.value =
//                 e?.errors?.[0]?.message ||
//                 e?.message ||
//                 "Checkout failed"

//             // 🔥 IMPORTANT: do NOT throw raw axios error to Vue
//             throw new Error(error.value)
//         } finally {
//             loading.value = false
//         }
//     }

//     function resetCheckout() {
//         checkout.value = null
//         error.value = null
//     }

//     return {
//         checkout,
//         loading,
//         error,
//         startCheckout,
//         resetCheckout
//     }
// })


import { defineStore } from "pinia"
import { ref } from "vue"
import { createCheckout } from "~/services/api/checkout/checkout.service"

export const useCheckoutStore = defineStore("checkout", () => {
    const checkout = ref<any>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function startCheckout() {
        loading.value = true
        error.value = null

        try {
            const res = await createCheckout()

            if (!res.success) {
                throw new Error(res.message || "Checkout failed")
            }

            checkout.value = res.data
            return res.data
        } catch (e: any) {
            error.value = e.message
            throw e
        } finally {
            loading.value = false
        }
    }

    return {
        checkout,
        loading,
        error,
        startCheckout
    }
})
