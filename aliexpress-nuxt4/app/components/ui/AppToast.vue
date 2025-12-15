<template>
  <transition name="toast">
    <div v-if="visible" class="toast" :class="type">
      {{ message }}
    </div>
  </transition>
</template>

<script setup lang="ts">
import { useToastStore } from "~/stores/modules/ui/useToastStore"

const toast = useToastStore()
const { message, type, visible } = storeToRefs(toast)
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 14px 18px;
  border-radius: 6px;
  color: #fff;
  font-weight: 500;
  z-index: 9999;
}

.toast.success { background: #2e7d32 }
.toast.error   { background: #d32f2f }
.toast.info    { background: #1976d2 }

.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
