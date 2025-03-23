<script setup>
import { onMounted, ref, watch } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { useToast } from "vue-toastification";
import { useRoute } from "vue-router";
import { useAuthStore } from "@/stores/authStore.js";
import { getAllCategoriesForAdminDashboard } from "@/services/adminService.js";

import PaginationBar from "@/components/PaginationBar.vue";
import LoadingState from "@/components/LoadingState.vue";
import ErrorState from "@/components/ErrorState.vue";
import CategoryAddModal from "@/modals/CategoryAddModal.vue";
import { formatDate } from "@/utils.js";

const authStore = useAuthStore()
const toast = useToast();
const route = useRoute();

const isEnabled = ref(false);
const page = ref(route.query.page ? parseInt(route.query.page) : 1);
const isCategoryModelOpen = ref(false);

const { data, isPending, refetch, isError, error } = useQuery({
  queryKey: () => ["admin", "categories", page.value],
  queryFn: async () => await getAllCategoriesForAdminDashboard(page.value, authStore.authToken),
  enabled: isEnabled.value,
  keepPreviousData: true,
});


onMounted(async () => {
  isEnabled.value = true;
  refetch();
});

watch(
  () => route.query.page,
  (newPage) => {
    page.value = newPage ? parseInt(newPage) : 1;
    refetch();
  }
);

watch([isError, error], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || "Failed to fetch data");
  }
});

const openCategoryModal = () => {
  isCategoryModelOpen.value = true;
  emit('categoryModalOpen')
};

const closeCategoryModal = () => {
  isCategoryModelOpen.value = false;
  emit('categoryModalClose')
};

const emit = defineEmits(['categoryModalOpen', 'categoryModalClose'])

</script>

<template>
<section :class="isCategoryModelOpen && 'opacity-50'" class="mx-auto w-full max-w-7xl px-4 py-4">
  <div class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
    <div>
      <h2 class="text-lg font-semibold">All Categories</h2>
      <p class="mt-1 text-sm text-gray-700">This is a list of all categories.</p>
    </div>

    <div class="flex items-center gap-10">
      <button
        v-if="!isError"
        :disabled="isPending"
        @click="openCategoryModal"
        :class="isPending ? 'bg-black/50 hover:bg-black/50 cursor-none' : 'bg-black hover:bg-black/80'"
        class="rounded-md  px-3 py-2 text-sm font-semibold text-white shadow-sm  "
      >
        Add Category
      </button>
    </div>
  </div>

  <LoadingState v-if="isPending" />
  <ErrorState v-else-if="isError" />

  <div v-else class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10" >
    <table class="min-w-full divide-y-2 divide-gray-200 bg-white text-sm">
      <thead class="text-left bg-gray-50 uppercase">
        <tr class="text-center">
          <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
            Category Id
          </th>
          <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
            Name
          </th>
          <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
            Base price /hr
          </th>
          <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
            Active Providers
          </th>
          <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
            Active Services
          </th>
          <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
            Total Bookings
          </th>
          <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
            Listed
          </th>
          <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
            Action
          </th>
        </tr>
      </thead>

      <tbody class="divide-y divide-gray-200">
        <tr
          class="odd:bg-white even:bg-gray-50 text-center"
          v-for="(category, i) in data.categories"
          :key="i"
        >
          <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
            {{ category.id }}
          </td>
          <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
            {{ category.name.toUpperCase() }}
          </td>
          <td class="whitespace-nowrap px-4 py-2 text-gray-700">
            {{ category.base_price }} ₹
          </td>
          <td class="whitespace-nowrap px-4 py-2 text-gray-700">
            {{ category.active_providers }}
          </td>
          <td class="whitespace-nowrap px-4 py-2 text-gray-700">
            {{ category.active_services }}
          </td>
          <td class="whitespace-nowrap px-4 py-2 text-gray-700">
            {{ category.total_bookings }}
          </td>
          <td class="whitespace-nowrap px-4 py-2 text-gray-700">
            {{ formatDate(category.created_at) }}
          </td>
          <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
            <a
              href="#"
              class="inline-block rounded bg-indigo-600 px-4 py-2 text-xs font-medium text-white hover:bg-indigo-700"
            >
              View
            </a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <PaginationBar
    v-if="!isPending && !isError"
    :total="data?.no_of_categories"
    :pages="data?.no_of_pages"
    :currentPage="page"
    :perPage="data?.per_page"
    :path="{ name: route.name, query: { page } }"
  />

</section>
<CategoryAddModal v-if="isCategoryModelOpen" :closeCategoryModal="closeCategoryModal" />
</template>
