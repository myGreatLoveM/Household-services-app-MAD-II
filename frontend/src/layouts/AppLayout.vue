<script setup>
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

const isModalOpen = ref(false)

function handleModal() {
  isModalOpen.value = !isModalOpen.value
}
</script>

<template>
  <div class="w-full h-full max-w-screen min-h-screen flex flex-col">
    <NavBar :isModalOpen="isModalOpen" />
    <RouterView @booking-modal-open="handleModal" @booking-modal-close="handleModal" />
  </div>
</template>
