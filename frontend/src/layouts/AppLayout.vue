<script setup>
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue';
</script>


<template>
  <div class="w-full h-full max-w-screen min-h-screen flex flex-col">
    <NavBar />
    <RouterView />
  </div>
</template>
