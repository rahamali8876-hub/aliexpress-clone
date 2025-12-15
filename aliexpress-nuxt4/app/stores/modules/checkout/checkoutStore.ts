import { defineStore } from "pinia"
import { ref } from "vue"
import { createCheckout } from "~/services/api/checkout/checkout.service"

export const useCheckoutStore = defineStore("checkout", () => {
    const checkout = ref<any | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function startCheckout(payload: {
        product_variant_id: string
        quantity: number
    }) {
        loading.value = true
        error.value = null

        try {
            const res = await createCheckout(payload)

            if (!res.success || !res.data) {
                throw new Error(res.message || "Checkout failed")
            }

            checkout.value = res.data
            return res.data
        } catch (e: any) {
            error.value = e.message || "Checkout error"
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
