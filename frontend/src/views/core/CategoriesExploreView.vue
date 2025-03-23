<script setup>
import { onMounted, ref, watch } from 'vue';
import { useQuery } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification';
import { RouterLink, useRoute } from 'vue-router'
import { getAllCategoriesDetails } from '@/services/coreServices.js'
import PaginationBar from "@/components/PaginationBar.vue";
import LoadingState from "@/components/LoadingState.vue";
import ErrorState from "@/components/ErrorState.vue";


const toast = useToast()
const route = useRoute()

const isEnabled = ref(false);
const page = ref(route.query.page ? parseInt(route.query.page) : 1);


const { data, isPending, refetch, isError } = useQuery({
  queryKey: () => ['categories', page.value],
  queryFn: async() => await getAllCategoriesDetails(page.value),
  enabled: isEnabled.value,
  onError: (error) => {
    toast.error(error.message)
  }
})

onMounted(() => {
  isEnabled.value = true
  refetch()
})

watch(
  () => route.query.page,
  (newPage) => {
    page.value = newPage ? parseInt(newPage) : 1;
    refetch();
  }
);

</script>


<template>
  <div class="w-full h-full mx-auto py-6 flex flex-col items-center">
    <div class="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <LoadingState v-if="isPending" />
      <ErrorState v-else-if="isError" />
      <div v-else v-for="(cat, i) in data.categories" :key="i" class="max-w-sm rounded-lg overflow-hidden shadow-lg bg-white border border-gray-200">
        <div class="p-6 h-full flex flex-col justify-between">
          <h5 class="text-2xl font-bold mb-2 text-gray-900">
            <a href="#">{{ cat.name }}</a>
          </h5>

          <p class="text-gray-700 text-base mb-4">
            {{ cat.short_description }}
          </p>

          <div class="mb-4">
            <span class="font-semibold text-lg text-green-600">Starting at:</span>
            <span class="text-lg font-bold text-green-700"> {{ cat.base_price }} ₹ <span class="text-sm text-gray-500">/hr</span></span>
          </div>

          <div class="flex items-center mb-4">
            <svg class="w-5 h-5 text-gray-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12l7 7 7-7M5 12l7-7 7 7"></path>
            </svg>
            <span class="text-gray-600"> {{ cat.active_providers }} Active Providers</span>
          </div>

          <div class="flex items-center mb-4">
            <svg class="w-5 h-5 text-gray-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12l7 7 7-7M5 12l7-7 7 7"></path>
            </svg>
            <span class="text-gray-600"> {{ cat.active_services }} Active Services</span>
          </div>

          <RouterLink :to="'#'" class="inline-flex items-center justify-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-md transition-all duration-300 mt-3 text-sm">
            Explore Services
            <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14m-7-7l7 7-7 7"></path>
            </svg>
          </RouterLink>
        </div>
      </div>
    </div>

    <PaginationBar
      v-if="!isPending && !isError"
      :total="data?.no_of_categories"
      :pages="data?.no_of_pages"
      :currentPage="page"
      :perPage="data?.per_page"
      :path="{ name: route.name, query: { page } }"
    />
  </div>



</template>
