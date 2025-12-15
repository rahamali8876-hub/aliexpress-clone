// import { storeToRefs } from "pinia"
// import { useCartStore } from "~/stores/modules/cart/cartStore"

// export function useCart() {
//     const cartStore = useCartStore()
//     const { cart, loading, error } = storeToRefs(cartStore)

//     async function addToCart(payload: {
//         product_variant_id: string
//         quantity?: number
//     }) {
//         if (!payload.product_variant_id) {
//             throw new Error("product_variant_id is required")
//         }
//         return await cartStore.addItem(payload)
//     }

//     return {
//         cart,
//         loading,
//         error,
//         loadCart: cartStore.loadCart,
//         addToCart,
//     }
// }


import { storeToRefs } from "pinia"
import { useCartStore } from "~/stores/modules/cart/cartStore"
import { useToastStore } from "~/stores/modules/ui/useToastStore"

export function useCart() {
    const cartStore = useCartStore()
    const toastStore = useToastStore()

    // reactive refs from store
    const { cart, loading, error } = storeToRefs(cartStore)

    /**
     * Add item to cart
     */
    async function addToCart(payload: {
        product_variant_id: string
        quantity?: number
    }) {
        if (!payload.product_variant_id) {
            const msg = "product_variant_id is required"
            toastStore.show(msg, "error")
            throw new Error(msg)
        }

        try {
            await cartStore.addItem({
                product_variant_id: payload.product_variant_id,
                quantity: payload.quantity ?? 1
            })

            toastStore.show("Added to cart successfully", "success")
        } catch (e: any) {
            toastStore.show(
                e?.message || "Failed to add item to cart",
                "error"
            )
            throw e
        }
    }

    return {
        // state
        cart,
        loading,
        error,

        // actions
        loadCart: cartStore.loadCart,
        addToCart
    }
}
