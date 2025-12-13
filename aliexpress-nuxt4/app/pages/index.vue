<!-- <template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Homepage  ************** </h1>
    <UBanner icon="i-lucide-info" title="This is a banner with an icon." />

    <div v-if="loading" class="text-center py-10">Loading homepage...</div>
    <div v-else-if="error" class="text-center text-red-500 py-10">
      {{ error.message || "Something went wrong" }}
    </div>

    <div v-else>
      <strong>Hero Section</strong>
      <LazyHomeHero v-if="heroSection" :data="heroSection.data" />
      <br>

      <strong>Banner Section</strong>
      <LazyHomeBanner v-if="bannerSection" :data="bannerSection.data" />

      <strong>Featured Products</strong>

      <!-- {{ featuredProductsSection }}</h1> --
      <LazyHomeFeaturedProducts v-if="featuredProductsSection" :data="featuredProductsSection.data" />

      <h1>Categoires Data </h1>
      <!-- {{ categoriesSection.data }} --
      <LazyHomeCategories v-if="categoriesSection" :data="categoriesSection.data" />

      <!-- <h1>Promotions - {{ promotions }}</h1> --
      <LazyHomePromoSection v-if="promotions" :data="promotions.data" />
      <div v-else>No promotions data</div>

      <strong>For Feauture Plan</strong>
      <LazyHomeTestimonials v-if="testimonialsSection" :data="testimonialsSection.data" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from "vue"
import { storeToRefs } from "pinia"
import { useHomepageStore } from "~/stores/modules/homepage/homepageStore"

const homeStore = useHomepageStore()
const { sections, loading, error } = storeToRefs(homeStore)
console.log('sectins in index.vue ', sections);
const { fetchHomepageData } = homeStore

onMounted(() => {
  fetchHomepageData()
})

const heroSection = computed(() => sections.value.find(s => s.type === "hero"))
const bannerSection = computed(() => sections.value.find(s => s.type === "banner"))
const featuredProductsSection = computed(() => sections.value.find(s => s.type === "products"))
const categoriesSection = computed(() => sections.value.find(s => s.type === "categories"))
const promotions = computed(() => {
  return sections.value.find(s => s.type === "promo");
});
// for future 
const testimonialsSection = computed(() => sections.value.find(s => s.type === "testimonials"))

</script>

<style scoop></style> -->


<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Homepage</h1>

    <div v-if="loading" class="py-20 text-center">
      Loading homepage...
    </div>

    <div v-else-if="error" class="text-red-500 py-20 text-center">
      {{ error.message }}
    </div>

    <div v-else>
      <LazyHomeHero
        v-if="hero"
        :data="hero"
      />

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
