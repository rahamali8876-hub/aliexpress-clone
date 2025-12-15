<template>
  <div class="checkout-summary">
    <h3>Order Summary</h3>

    <div v-for="item in checkout.items" :key="item.id">
      <span>{{ item.product.name }}</span>
      <span>{{ item.quantity }} × {{ item.price }}</span>
    </div>

    <hr />

    <div class="total">
      Total: {{ checkout.total_price }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  checkout: Object
})
</script>
