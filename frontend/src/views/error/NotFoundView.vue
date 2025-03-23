<script setup>

</script>

<template>
    <div class="flex flex-col items-center justify-center px-4 py-10 sm:px-6 sm:py-16 lg:px-8 lg:py-24 ">
        <RouterLink
          :to="{ name: 'home' }"
          class="underline text-xl font-semibold text-blue-400 mb-4"
        >
          Home
        </RouterLink>
        <h1 class="text-3xl font-semibold mb-3">Oops. Page Not Found (404)</h1>
    </div>
</template>

