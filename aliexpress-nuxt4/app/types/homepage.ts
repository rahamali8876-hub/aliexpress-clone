// ~/types/homepage.ts

export type HomepageSectionType =
    | "hero"
    | "banner"
    | "categories"
    | "products"
    | "promo"
    | "testimonials"

export interface HomepageSection<T = any> {
    type: HomepageSectionType
    data: T
}

/* =====================
   API RESPONSE TYPES
===================== */

export interface Banner {
    id: string
    title: string
    image: string
    alt_text: string
    sort_order: number
    is_active: boolean
}

export interface Category {
    id: string
    name: string
    slug: string
    description: string
}

export interface Product {
    id: string
    title: string
    slug: string
    price: string
    discount_price: string | null
    description: string
    image: string
    stock: number
    is_active: boolean
}

export interface Promotion {
    id: string
    title: string
    image: string
    sort_order: number
}
