
<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Homepage</h1>

    <div v-if="loading" class="py-20 text-center">
      Loading homepage...
    </div>

    <!-- <div v-else-if="error" class="text-red-500 py-20 text-center">
      {{ error.message }}
    </div> -->
    <div v-else-if="error" class="text-red-500 py-20 text-center">
    {{ error.message }}
  </div>


    <div v-else>
      <!-- <LazyHomeHero
        v-if="hero"
        :data="hero"
      /> -->

      <LazyHomeBanner
        v-if="banners?.length"
        :data="banners"
      />

      <LazyHomeCategories
        v-if="categories?.length"
        :data="categories"
      />

      <LazyHomeFeaturedProducts
        v-if="products?.length"
        :data="products"
      />

      <LazyHomePromoSection
        v-if="promotions?.length"
        :data="promotions"
      />

      <LazyHomeTestimonials
        v-if="testimonials?.length"
        :data="testimonials"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia"
import { useHomepageStore } from "~/stores/modules/homepage/homepage.store"

const store = useHomepageStore()
const { loading, error } = storeToRefs(store)

/* =====================
   SSR + SEO SAFE FETCH
===================== */
await store.fetchHomepage()

/* =====================
   SECTION ACCESS
===================== */
const hero = store.getSection("hero")
const banners = store.getSection("banner")
const categories = store.getSection("categories")
const products = store.getSection("products")
const promotions = store.getSection("promo")
const testimonials = store.getSection("testimonials")
</script>
