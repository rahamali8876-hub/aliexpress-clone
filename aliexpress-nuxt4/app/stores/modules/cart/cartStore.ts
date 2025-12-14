// import { defineStore } from "pinia"
// import { fetchCart, addItemToCart } from "~/services/api/cart/cartService"

// export const useCartStore = defineStore("cart", {
//     state: () => ({
//         cart: null as any,
//         loading: false,
//         error: null as string | null,
//     }),

//     actions: {
//         async loadCart() {
//             this.loading = true
//             const res = await fetchCart()
//             this.loading = false

//             if (res.success) {
//                 this.cart = res.data
//             } else {
//                 this.error = res.message
//             }

//             return res
//         },

//         async addItem(payload: { product_variant_id: string; quantity?: number }) {
//             this.loading = true
//             const res = await addItemToCart(payload)
//             this.loading = false

//             if (res.success) {
//                 this.cart = res.data
//             } else {
//                 this.error = res.message
//             }

//             return res
//         },
//     },
// })

import { defineStore } from "pinia"
import { fetchCart, addItemToCart } from "~/services/api/cart/cartService"

export const useCartStore = defineStore("cart", () => {
    const cart = ref<any>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)

    /**
     * Load cart
     */
    async function loadCart() {
        loading.value = true
        error.value = null

        const res = await fetchCart()
        loading.value = false

        if (res.success) {
            cart.value = res.data
        } else {
            error.value = res.message
        }

        return res
    }

    /**
     * Add item to cart
     */
    async function addItem(payload: { product_variant_id: string; quantity?: number }) {
        loading.value = true
        error.value = null

        const res = await addItemToCart(payload)
        loading.value = false

        if (res.success) {
            cart.value = res.data
        } else {
            error.value = res.message
        }

        return res
    }

    return {
        cart,
        loading,
        error,
        loadCart,
        addItem
    }
})
