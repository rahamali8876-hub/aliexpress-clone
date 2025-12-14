import { useRouter } from "vue-router"
import { useCheckoutStore } from "~/stores/modules/checkout/checkoutStore"
import { useToastStore } from "~/stores/modules/ui/useToastStore"

export function useCheckout() {
    const router = useRouter()
    const checkoutStore = useCheckoutStore()
    const toast = useToastStore()

    async function buyNow(payload: {
        product_variant_id: string
        quantity: number
    }) {
        try {
            const checkout = await checkoutStore.startCheckout(payload)

            toast.show("Redirecting to checkout", "success")

            router.push(`/checkout/${checkout.id}`)
        } catch (e: any) {
            toast.show(e.message || "Unable to start checkout", "error")
            throw e
        }
    }

    return {
        buyNow,
        loading: checkoutStore.loading
    }
}
