<template>
  <div v-if="addresses.length">
    <div
      v-for="addr in addresses"
      :key="addr.id"
      class="address-card"
      :class="{ active: selected?.id === addr.id }"
      @click="$emit('select', addr)"
    >
      <p>{{ addr.name }}</p>
      <p>{{ addr.line1 }}, {{ addr.city }}</p>
      <p>{{ addr.phone }}</p>
    </div>
  </div>

  <p v-else>No saved addresses</p>
</template>

<script setup>
defineProps({
  addresses: Array,
  selected: Object
})
defineEmits(["select"])
</script>
