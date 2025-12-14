<template>
  <div class="cart-icon">
    🛒
    <span v-if="totalItems > 0" class="badge">
      {{ totalItems }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { useCartStore } from "~/stores/modules/cart/useCartStore"

const cart = useCartStore()
const { totalItems } = storeToRefs(cart)
</script>

<style scoped>
.cart-icon {
  position: relative;
  font-size: 20px;
}

.badge {
  position: absolute;
  top: -6px;
  right: -10px;
  background: red;
  color: white;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 999px;
}
</style>
