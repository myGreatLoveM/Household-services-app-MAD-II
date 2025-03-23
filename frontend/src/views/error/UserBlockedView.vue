<script setup>
</script>


<template>
  <div class="w-full h-full min-h-screen flex justify-center items-center">
    <div class="bg-white shadow-md rounded-lg p-8 max-w-lg text-center">

        <h1 class="text-3xl font-bold text-red-600 mb-4">
          Temporary Block
        </h1>

        <p class="text-gray-700 mb-6">
          You have been blocked from accessing platform. Please check back later or contact support for more information.
        </p>

        <div class="flex flex-col gap-2 items-center">
          <RouterLink
            :to="{ name: 'home' }"
            class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
          >
            Home
          </RouterLink>
          <RouterLink
            :to="{ name: 'logout' }"
            class="bg-amber-500 hover:bg-amber-500 text-white font-bold py-2 px-4 rounded"
          >
            Logout
          </RouterLink>
        </div>
    </div>
  </div>
</template>
