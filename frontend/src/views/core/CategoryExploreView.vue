<script setup>

</script>

<template>
  <div class="w-full h-full px-8 py-6  ">
    <div class="w-full max-w-7xl mx-auto px-4">
      <div class="flex justify-between items-center mx-auto mb-6">
        <div>
            <h1 class="text-3xl font-bold text-gray-900">category.name</h1>
        </div>

        <div class="flex items-center gap-10">
          <div class="text-right">
              <p class="text-lg text-gray-900 font-semibold">Starting from category.base_price ₹</p>
              <p class="text-sm text-gray-500">per hr</p>
          </div>

          <button class="inline-flex items-center justify-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-md transition-all duration-300 mt-3 text-sm">
              Explore Services
              <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14m-7-7l7 7-7 7"></path>
              </svg>
          </button>
        </div>
      </div>

      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Description and Details</h2>
        <p class="text-gray-600 mb-4">
            category.long_description
        </p>
        <ul class="list-disc ml-6 text-gray-600">
            <li>Lorem ipsum dolor sit amet.</li>
            <li>Lorem ipsum dolor sit amet consectetur adipisicing elit. Iusto, rerum.</li>
            <li>Magni ea, deleniti qui officiis adipisci </li>
            <li>iusto ipsa consequuntur? Nisi error quod provident suscipit.</li>
        </ul>
      </div>
    </div>
  </div>
</template>


