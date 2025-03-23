<script setup>
import { onMounted, ref, watch } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { useToast } from "vue-toastification";
import { useRoute } from "vue-router";
import PaginationBar from "@/components/PaginationBar.vue";
import LoadingState from "@/components/LoadingState.vue";
import ErrorState from "@/components/ErrorState.vue";
import { getAllProvidersForAdminDashboard } from "@/services/adminService.js";
import { formatDate } from "@/utils.js";
import { UserStatus } from "@/constants.js";

const toast = useToast();
const route = useRoute();

const isEnabled = ref(false);
const page = ref(route.query.page ? parseInt(route.query.page) : 1);


const { data, isPending, refetch, isError } = useQuery({
  queryKey: () => ["admin", "providers", page.value, UserStatus.NOT_APPROVED],
  queryFn: async () => await getAllProvidersForAdminDashboard(UserStatus.NOT_APPROVED, page.value),
  keepPreviousData: true,
  enabled: isEnabled.value,
  onError: (error) => {
    console.log(error)
    toast.error(error);
  },
});

onMounted(() => {
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
</script>


<template>
<section class="mx-auto w-full max-w-7xl px-4 py-4">
  <div class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
    <div>
      <h2 class="text-lg font-semibold">All newly joined Providers</h2>
      <p class="mt-1 text-sm text-gray-700">
        This is a list of all verified providers.
      </p>
    </div>
  </div>

  <LoadingState v-if="isPending" />
  <ErrorState v-else-if="isError" />

  <div v-else class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
    <table class="min-w-full bg-white text-sm">
      <thead class="text-left bg-gray-50 uppercase">
        <tr class="text-center">
          <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Username</th>
          <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Category</th>
          <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Experience</th>
          <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Location</th>
          <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Status</th>
          <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Joined</th>
          <th scope="col"  class="px-4 py-2">Action</th>
        </tr>
      </thead>

      <tbody class="divide-y divide-gray-200">
        <tr class="odd:bg-white even:bg-gray-50 text-center" v-for="(prov, i) in data.providers" :key="i">
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">{{ prov.user.username }}</td>
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-700">{{ prov.category.toUpperCase() }} </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ prov.experience }} yr</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ prov.location }} </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              <span v-if="!prov.is_approved && prov.is_blocked" class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700 bg-red-100">
                blocked
              </span>
              <span v-else-if="!prov.is_approved && !prov.is_blocked" class="whitespace-nowrap rounded-full border border-yellow-500 px-2.5 py-0.5 text-sm text-yellow-700 bg-yellow-100">
                pending
              </span>
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ formatDate(prov.created_at) }}</td>
            <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
              <button
                v-if="!prov.is_approved && !prov.is_blocked"
                class="inline-block rounded bg-green-600 px-4 py-2 text-xs font-medium text-white hover:bg-green-700"
              >
                Approve
              </button>
              <button
                v-if="!prov.is_approved && !prov.is_blocked"
                class="inline-block rounded bg-red-600 px-4 py-2 text-xs font-medium text-white hover:bg-red-700"
              >
                Block
              </button>
              <button
                v-if="!prov.is_approved && prov.is_blocked"
                class="inline-block rounded bg-teal-600 px-4 py-2 text-xs font-medium text-white hover:bg-teal-700"
              >
                Unblock
              </button>
            </td>
        </tr>
      </tbody>
    </table>
  </div>

  <PaginationBar
    v-if="!isPending && !isError"
    :total="data?.no_of_providers"
    :pages="data?.no_of_pages"
    :currentPage="page"
    :perPage="data?.per_page"
    :path="{ name: route.name, query: { page } }"
  />
</section>
</template>
