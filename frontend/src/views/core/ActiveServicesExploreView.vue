<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useToast } from 'vue-toastification';
import { useQuery } from '@tanstack/vue-query';
import {getAllActiveServices} from '@/services/coreServices.js'
import ServiceCard from '@/components/ServiceCard.vue';
import PaginationBar from '@/components/PaginationBar.vue';
import LoadingState from '@/components/LoadingState.vue';
import ErrorState from '@/components/ErrorState.vue';


const route = useRoute()
const toast = useToast()
const isEnabled = ref(false)
const page = ref(route.query.page ? parseInt(route.query.page) : 1)

const {data, isPending, isError, error, refetch} = useQuery({
  queryKey: ['active-services', page.value],
  queryFn: () => getAllActiveServices(page.value),
  enabled: isEnabled.value,
})

onMounted(() => {
  isEnabled.value = true
  refetch()
})


watch(error, (newVal) => {
  if(isError.value && newVal) {
    toast.error(newVal.message || 'Failed to fetch services')
  }
})

watch(
  () => route.query.page,
  (newPage) => {
    page.value = newPage ? parseInt(newPage) : 1
    refetch()
  },
)
</script>

<template>
  <section class="min-h-screen py-6">
    <LoadingState v-if="isPending" />
    <ErrorState v-else-if="isError" />
    <div v-else class="max-w-7xl mx-auto">
      <form method="POST" action="#" class="relative max-w-xl ml-auto flex items-center gap-5">
        <input
          type="text"
          name="search_by"
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-blue-200"
          placeholder="Search services by provider name, location, or category"
          id="search-input"
        />
        <button
          type="submit"
          class="px-6 bg-fuchsia-500 text-white font-bold py-2 rounded-lg hover:bg-fuchsia-700"
        >
          Search
        </button>
      </form>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-5">
        <ServiceCard 
          v-for="(service,i) in data.services"
          :key="i"
          :id="service.id"
          :name="service.name"
          :price="service.price"
          :time="service.time_required_hr"
          :provider="service.provider.user.username"
          :provExperience="service.provider.experience"
          :category="service.provider.category.name"
          :avgRating="service.avg_rating"
          :totalReviews="service.toatl_reviews"
          :totalBookings="service.total_bookings"
        />
      </div>
    </div>

    <PaginationBar 
      v-if="!isPending && !isError"
      :total="data.no_of_services"
      :pages="data.no_of_pages"
      :currentPage="data.current_page"
      :perPage="data?.per_page"
      :path="{ name: route.name, query: { page } }"
    />
  </section>
</template>
