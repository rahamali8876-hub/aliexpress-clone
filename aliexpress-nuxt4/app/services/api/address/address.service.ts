import { useNuxtApp } from "#app"
import { normalizeResponse, handleApiError } from "~/utils/api/base"

const ENDPOINT = "/address/"

export async function fetchAddresses() {
    const { $api } = useNuxtApp()
    try {
        const res = await $api.get(ENDPOINT)
        return normalizeResponse<any[]>(res)
    } catch (e) {
        return handleApiError(e)
    }
}

export async function createAddress(payload: any) {
    const { $api } = useNuxtApp()
    try {
        const res = await $api.post(ENDPOINT, payload)
        return normalizeResponse<any>(res)
    } catch (e) {
        return handleApiError(e)
    }
}
