/**
 * Base API response normalizer
 * ----------------------------
 * Ensures frontend always receives
 * a predictable response shape
 */

export interface NormalizedResponse<T> {
    success: boolean
    code: number | null
    message: string | null
    data: T | null
}

export function normalizeResponse<T>(payload: any): NormalizedResponse<T> {
    return {
        success: Boolean(payload?.success),
        code: payload?.code ?? null,
        message: payload?.message ?? null,
        data: payload?.data ?? null
    }
}

export function handleApiError(error: any): NormalizedResponse<null> {
    return {
        success: false,
        code: error?.response?.status ?? 500,
        message: error?.message ?? "Unknown error occurred",
        data: null
    }
}
