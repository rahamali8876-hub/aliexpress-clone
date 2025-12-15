<template>
  <div>
    <h3>Shipping Address</h3>

    <AddressList
      :addresses="addresses"
      :selected="selectedAddress"
      @select="selectedAddress = $event"
    />

    <AddressForm />
  </div>
</template>

<script setup>
import { onMounted } from "vue"
import { useAddress } from "~/composables/address/useAddress"

import AddressList from "./AddressList.vue"
import AddressForm from "./AddressForm.vue"

const {
  addresses,
  selectedAddress,
  loadAddresses
} = useAddress()

onMounted(loadAddresses)
</script>
