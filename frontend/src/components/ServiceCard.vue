<script setup>
import RatingStar from '@/components/RatingStar.vue'

defineProps({
  id: Number,
  name: String,
  price: Number,
  time: Number,
  category: String,
  provider: String,
  provExperience: Number,
  avgRating: Number,
  totalReviews: Number,
  totalBookings: Number,
})
</script>


<template>
  <div
    class="max-w-sm bg-white shadow-lg border rounded-xl overflow-hidden transform transition duration-500 hover:scale-105 hover:shadow-xl"
  >
    <div class="p-6">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ name }}</h2>
      <p class="text-gray-600 mb-4">
        This service offers a complete solution for your needs, providing high-quality results with
        experienced professionals.
      </p>

      <div class="flex justify-between items-center mb-4">
        <div>
          <span class="text-sm text-gray-500">⏱ {{ time }} hr</span>
          <p class="text-sm text-gray-500">Rate: <span class="text-blue-600">{{ price }} ₹ /hr</span></p>
        </div>
        <span class="bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded-full"
          >{{ category }}</span
        >
      </div>

      <div class="flex items-center mb-4">
        <div>
          <p class="font-medium text-lg text-indigo-900">@{{ provider }}</p>
          <p class="text-xs text-gray-500">{{ provExperience }} yr experience</p>
        </div>
      </div>

      <div class="flex justify-between items-center mb-4">
        <div class="flex items-center">
          <RatingStar />
          <p class="text-sm text-gray-600 ml-2">{{ avgRating }} ({{ totalReviews }} reviews)</p>
        </div>
        <p class="text-sm text-gray-600">{{ totalBookings }} Total bookings</p>
      </div>

      <div class="flex justify-between items-center">
        <RouterLink :to="{ name: 'explore-service' , params: { serviceId: id } }">
          <button
            class="bg-gray-100 text-gray-600 text-sm font-semibold px-4 py-2 rounded-lg hover:bg-gray-200"
          >
            More Info
          </button>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
