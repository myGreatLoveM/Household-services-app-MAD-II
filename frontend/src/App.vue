<script setup>
import { RouterView } from 'vue-router'
import { VueQueryDevtools } from '@tanstack/vue-query-devtools'
// import { useAuthStore } from '@/stores/authStore.js'

// const authStore = useAuthStore()

// // Call hydrate when the app starts to restore authentication state from localStorage
// authStore.hydrate()

</script>


<template>
  <RouterView />
  <VueQueryDevtools />
</template>
