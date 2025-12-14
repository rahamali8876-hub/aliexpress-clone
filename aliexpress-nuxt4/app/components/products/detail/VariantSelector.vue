<template>
  <div class="variant-selector-root">
    <div v-if="loading" class="loader">Loading options...</div>
    <div v-else-if="error" class="error">Failed to load variants</div>

    <div v-else>
      <div v-if="attributeGroups.length === 0" class="no-attrs">
        No variants or attributes available
      </div>

      <div v-else>
        <!-- Attribute groups -->
        <div v-for="group in attributeGroups" :key="group.id" class="group">
          <div class="group-title">{{ group.name }}</div>

          <!-- color swatches -->
          <div v-if="group.isColor" class="swatches">
            <button
              v-for="val in group.values"
              :key="val.id"
              class="swatch-btn"
              :class="{
                selected: selectedAttrs[group.id] === val.id,
                disabled: isDisabled(group.id, val.id)
              }"
              :disabled="isDisabled(group.id, val.id)"
              @click="onSelectValue(group.id, val.id)"
              :aria-pressed="selectedAttrs[group.id] === val.id"
              :title="valueLabel(val)"
            >
              <span
                class="swatch-circle"
                :style="swatchStyle(val)"
              ></span>
              <span v-if="!isHex(val.value)" class="swatch-label">{{ valueLabel(val) }}</span>
            </button>
          </div>

          <!-- normal option buttons -->
          <div v-else class="option-buttons">
            <button
              v-for="val in group.values"
              :key="val.id"
              class="opt-btn"
              :class="{ selected: selectedAttrs[group.id] === val.id, disabled: isDisabled(group.id, val.id) }"
              :disabled="isDisabled(group.id, val.id)"
              @click="onSelectValue(group.id, val.id)"
            >
              {{ valueLabel(val) }}
            </button>
          </div>
        </div>

        <!-- preview / selected summary -->
        <div v-if="previewVariant" class="preview">
          <div class="preview-grid">
            <img :src="previewVariant.image" alt="variant image" class="preview-img" />
            <div>
              <div class="price">
                {{ previewVariant.currency }} {{ previewVariant.discount_price }}
                <span class="old-price">{{ previewVariant.currency }} {{ previewVariant.price }}</span>
              </div>
              <div class="sku">SKU: {{ previewVariant.sku }}</div>
              <div :class="previewVariant.stock > 0 ? 'in-stock' : 'out-stock'">
                {{ previewVariant.stock > 0 ? 'In stock' : 'Out of stock' }}
              </div>
            </div>
          </div>
        </div>

        <!-- controls -->
        <div class="controls">
          <button @click="resetSelection" class="reset-btn">Reset</button>
          <button @click="addToCart" :disabled="!finalVariant || finalVariant.stock <= 0" class="add-cart">
            Add to cart
          </button>
        </div>

        <div v-if="availabilityWarning" class="warning">{{ availabilityWarning }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-unused-vars */
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useVariantStore } from '~/stores/modules/product/variantStore'

// ------------------------------
// Props & Emits
// ------------------------------
const props = defineProps({
  productId: { type: String, required: true }
})
const emit = defineEmits(['select', 'update-image', 'update-price', 'update-stock'])

// ------------------------------
// Store & local reactive state
// ------------------------------
const variantStore = useVariantStore()

const loading = ref(true)
const error = ref(null)

const selectedAttrs = ref({})    // { attribute_id: value_id }
const previewVariant = ref(null) // preview for partial or full match
const availabilityWarning = ref(null)

// router (URL sync)
const router = useRouter()
const route = useRoute()

// store accessors
const storeVariants = computed(() => variantStore.variants || [])
const storeAvailableAttributes = computed(() => variantStore.available_attributes || {})
const storeCombinationMap = computed(() => variantStore.combination_map || {})
const storeSelectedVariant = computed(() => variantStore.selectedVariant || null)

// ------------------------------
// Utility helpers
// ------------------------------
function isHex(v) {
  return /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test((v || '').toString().trim())
}
function valueLabel(v) {
  return v?.value ?? v?.name ?? String(v)
}
function swatchStyle(val) {
  const color = isHex(val.value) ? val.value : '#fff'
  const border = isHex(val.value) ? '1px solid rgba(0,0,0,0.12)' : '1px solid #e5e7eb'
  return { background: color, border }
}
function isColorGroup(name, sampleValue) {
  if (!name && !sampleValue) return false
  const n = (name || '').toLowerCase()
  if (['color', 'colour', 'shade'].some(x => n.includes(x))) return true
  return isHex(sampleValue)
}
function buildKey(map) {
  return Object.keys(map)
    .filter(k => map[k] != null)
    .map(k => `${k}:${map[k]}`)
    .sort()
    .join('|')
}

// ------------------------------
// Derived data (attribute groups)
// ------------------------------
const attributeGroups = computed(() => {
  const aa = storeAvailableAttributes.value || {}
  return Object.keys(aa).map(id => {
    const group = aa[id]
    const sample = (group.values && group.values[0] && group.values[0].value) || null
    return {
      id,
      name: group.name,
      values: group.values || [],
      isColor: isColorGroup(group.name, sample)
    }
  })
})

// ------------------------------
// Variant lookup helpers
// ------------------------------
const variantLookup = computed(() => {
  // Build a map key -> variant object for O(1) exact lookups
  const map = {}
  for (const v of storeVariants.value || []) {
    const key = (v.attributes || []).map(a => `${a.attribute_id}:${a.value_id}`).sort().join('|')
    map[key] = v
  }
  return map
})

function findMatchingVariants(attrsMap) {
  if (!storeVariants.value?.length) return []
  // Return variants that match all selected keys in attrsMap
  return storeVariants.value.filter(v => {
    const vm = {}
    for (const a of v.attributes || []) vm[a.attribute_id] = a.value_id
    for (const k of Object.keys(attrsMap)) {
      if (attrsMap[k] == null) continue
      if (vm[k] !== attrsMap[k]) return false
    }
    return true
  })
}

// is option available given current partial selection
function isAvailable(attrId, valId) {
  const trial = { ...selectedAttrs.value, [attrId]: valId }
  const matches = findMatchingVariants(trial)
  return matches.length > 0
}
function isDisabled(attrId, valId) { return !isAvailable(attrId, valId) }

// ------------------------------
// Selection logic
// ------------------------------
function selectAttrsFromVariant(variant) {
  const map = {}
  for (const a of variant.attributes || []) {
    if (a.attribute_id && a.value_id) map[a.attribute_id] = a.value_id
  }
  selectedAttrs.value = map
}

function applyFinalVariant(variant) {
  previewVariant.value = variant
  variantStore.setSelectedVariant(variant)
  emit('select', variant)
  if (variant.image) emit('update-image', variant.image)
  if (variant.discount_price) emit('update-price', variant.discount_price)
  if (variant.stock !== undefined) emit('update-stock', variant.stock)
}

// User clicks an option
function onSelectValue(attrId, valId) {
  // toggle selection
  if (selectedAttrs.value[attrId] === valId) {
    selectedAttrs.value = { ...selectedAttrs.value, [attrId]: null }
  } else {
    selectedAttrs.value = { ...selectedAttrs.value, [attrId]: valId }
  }
  availabilityWarning.value = null

  // find matches for current partial selection
  const matches = findMatchingVariants(selectedAttrs.value)

  if (matches.length === 1) {
    applyFinalVariant(matches[0])
  } else if (matches.length > 1) {
    // preview first match
    previewVariant.value = matches[0]
    if (previewVariant.value?.image) emit('update-image', previewVariant.value.image)
  } else {
    previewVariant.value = null
    availabilityWarning.value = 'This combination is not available.'
  }

  // update URL query param if exact key maps to variant id (combination_map preferred)
  const key = buildKey(selectedAttrs.value)
  const mappedId = storeCombinationMap.value?.[key] || null
  if (mappedId) {
    router.replace({ query: { ...route.query, variant: mappedId } }).catch(() => {})
  } else {
    const q = { ...route.query }; delete q.variant
    router.replace({ query: q }).catch(() => {})
  }
}

// reset selection
function resetSelection() {
  selectedAttrs.value = {}
  previewVariant.value = variantStore.selectedVariant || null
  availabilityWarning.value = null
  const q = { ...route.query }; delete q.variant
  router.replace({ query: q }).catch(() => {})
}

// Add to cart (emit selected preview / final)
function addToCart() {
  const target = previewVariant.value || variantStore.selectedVariant
  if (!target) return
  emit('select', target)
}

// computed finalVariant if selection matches exactly
const finalVariant = computed(() => {
  const key = buildKey(selectedAttrs.value)
  const id = storeCombinationMap.value?.[key]
  if (!id) return null
  return storeVariants.value.find(v => v.id === id) || (variantLookup.value && variantLookup.value[key]) || null
})

// ------------------------------
// Load & init
// ------------------------------
async function load() {
  try {
    loading.value = true
    error.value = null

    const res = await variantStore.fetchVariants(props.productId)

    if (!res || res.success === false) {
      throw res || new Error('Failed to load variants')
    }

    // URL variant override
    const urlVariantId = route.query.variant
    if (urlVariantId) {
      const found = storeVariants.value.find(v => v.id === urlVariantId)
      if (found) {
        selectAttrsFromVariant(found)
        applyFinalVariant(found)
        return
      }
    }

    // default: use storeSelectedVariant (store auto-selected one)
    if (storeSelectedVariant.value) {
      selectAttrsFromVariant(storeSelectedVariant.value)
      previewVariant.value = storeSelectedVariant.value
      if (previewVariant.value?.image) emit('update-image', previewVariant.value.image)
      emit('select', storeSelectedVariant.value)
    } else if (storeVariants.value.length) {
      // fallback pick first or first in-stock
      const pick = storeVariants.value.find(v => v.stock > 0) || storeVariants.value[0]
      if (pick) {
        selectAttrsFromVariant(pick)
        applyFinalVariant(pick)
      }
    }
  } catch (e) {
    error.value = e
  } finally {
    loading.value = false
  }
}

onMounted(load)

// react to external store selectedVariant changes
watch(storeSelectedVariant, (nv) => {
  if (!nv) return
  selectAttrsFromVariant(nv)
  previewVariant.value = nv
  emit('select', nv)
  if (nv.image) emit('update-image', nv.image)
})
</script>

<style scoped>
.variant-selector-root { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; }
.loader { color: #6b7280; }
.error { color: #dc2626; }
.no-attrs { color: #6b7280; }

.group { margin-bottom: 0.75rem; }
.group-title { font-weight: 600; margin-bottom: 0.5rem; color:#111827; }

.swatches { display:flex; gap:0.5rem; flex-wrap:wrap; align-items:center; }
.swatch-btn { display:flex; align-items:center; gap:0.5rem; padding:6px 8px; border-radius:8px; background:transparent; border: none; cursor:pointer; }
.swatch-btn.disabled { opacity:0.4; cursor:not-allowed; }
.swatch-circle { width:32px; height:32px; border-radius:50%; display:inline-block; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }
.swatch-label { font-size:0.85rem; color:#374151; margin-left:4px; }

.option-buttons { display:flex; gap:0.5rem; flex-wrap:wrap; }
.opt-btn { padding:6px 10px; border-radius:8px; border:1px solid #e5e7eb; background:#f9fafb; cursor:pointer; }
.opt-btn.selected { background:#111827; color:#fff; border-color:transparent; }
.opt-btn.disabled { opacity:0.45; cursor:not-allowed; }

.swatch-btn.selected .swatch-circle { outline: 2px solid #10b981; transform: scale(1.03); }

.preview { background:#fff; margin-top:10px; border:1px solid #eee; padding:12px; border-radius:8px; }
.preview-grid { display:flex; gap:1rem; align-items:center; }
.preview-img { width:96px; height:96px; object-fit:cover; border-radius:6px; }

.controls { display:flex; gap:10px; margin-top:10px; }
.reset-btn { background:#fff; padding:8px 12px; border:1px solid #e5e7eb; border-radius:6px; cursor:pointer; }
.add-cart { background:#111827; color:#fff; padding:8px 12px; border-radius:6px; border:none; cursor:pointer; }
.warning { color:#b45309; margin-top:8px; }
.in-stock { color:#059669; margin-top:6px; }
.out-stock { color:#dc2626; margin-top:6px; }
</style>
