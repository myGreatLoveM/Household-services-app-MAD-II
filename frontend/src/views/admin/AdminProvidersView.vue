<script setup>
import { onMounted, ref, watch, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { useToast } from "vue-toastification";
import { useRoute, RouterLink } from "vue-router";
import { approveOrUnblockProviderForAdminDashboard, blockProviderForAdminDashboard, getAllProvidersForAdminDashboard } from "@/services/adminService.js";

import PaginationBar from "@/components/PaginationBar.vue";
import LoadingState from "@/components/LoadingState.vue";
import ErrorState from "@/components/ErrorState.vue";
import { UserStatus } from "@/constants.js";


const queryClient = useQueryClient()
const toast = useToast();
const route = useRoute();

const isEnabled = ref(false);
const page = ref(route.query.page ? parseInt(route.query.page) : 1);


const { data:provData, isPending:isProvDataPending, refetch: refetchApprovedProvider, isError:isProvDataError, error:provDataError } = useQuery({
  queryKey: () => ["admin", "providers", page.value, UserStatus.APPROVED],
  queryFn: async () => await getAllProvidersForAdminDashboard(page.value, UserStatus.APPROVED),
  keepPreviousData: true,
  enabled: isEnabled.value,
});

const { data:blockedProvData, isPending:isBlockPending, isSuccess:isBlockSuccess, mutate:blockProvider, error:blockError, isError:isBlockError} = useMutation({
  mutationFn: ({provId, provUsername}) => blockProviderForAdminDashboard({provId, provUsername})
})

const { data:unblockedProvData, isPending:isUnblockPending, isSuccess:isUnblockSuccess, mutate:unblockProvider, error:unblockError, isError:isUnblockError} = useMutation({
  mutationFn: ({provId, provUsername}) => approveOrUnblockProviderForAdminDashboard({provId, provUsername})
})

onMounted(() => {
  isEnabled.value = true;
  refetchApprovedProvider();
});

watch(provDataError, (errorVal) => {
  if (isProvDataError.value && errorVal) {
    toast.error("Failed to fetch providers data!!");
  }
});


watch(blockError, (errorVal) => {
  if (isBlockError.value && errorVal) {
    toast.error(`Failed to block provider ${blockedProvData.value.provUsername}!!`);
  }
})

watch(unblockError, (errorVal) => {
  if (isUnblockError.value && errorVal) {
    toast.error(`Failed to unblock provider ${unblockedProvData.value.provUsername}!!`);
  }
})


watch(isBlockSuccess, (isBlockSuccessVal) => {
  if (isBlockSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'admin' &&
          query.queryKey[1] === 'providers' &&
          query.queryKey[3] === UserStatus.APPROVED;
      }
    })
    toast.success(`Provider ${blockedProvData.value.provUsername} blocked..`)
    refetchApprovedProvider()
  }
})

watch(isUnblockSuccess, (isUnblockSuccessVal) => {
  if (isUnblockSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'admin' &&
          query.queryKey[1] === 'providers' &&
          query.queryKey[3] === UserStatus.APPROVED;
      }
    })
    toast.success(`Provider ${unblockedProvData.value.provUsername} unblocked..`)
    refetchApprovedProvider()
  }
})

watch(
  () => route.query.page,
  (newPage) => {
    page.value = newPage ? parseInt(newPage) : 1;
    refetchApprovedProvider();
  }
);

const isActionButtonsDisabled = computed(() => isBlockPending.value || isUnblockPending.value)


const handleBlockProvider = async (provId, provUsername) => {
  blockProvider({provId, provUsername})
}

const handleUnblockProvider = async (provId, provUsername) => {
  unblockProvider({provId, provUsername})
}

</script>



<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
  <div class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
      <div>
        <h2 class="text-lg font-semibold">All Providers</h2>
        <p class="mt-1 text-sm text-gray-700">
          This is a list of all verified providers.
        </p>
      </div>

      <div class="flex items-center gap-10">
        <RouterLink :to="{ name: 'admin-providers-pending' }">
          <button
            :disabled="isActionButtonsDisabled"
            :class="isActionButtonsDisabled ? 'bg-zinc-400' : 'bg-zinc-600 hover:bg-zinc-700'"
            class="rounded-md x px-3 py-2 text-sm font-semibold text-white shadow-sm "
          >
            New Providers
          </button>
        </RouterLink>
      </div>
  </div>

  <LoadingState v-if="isProvDataPending" />
  <ErrorState v-else-if="isProvDataError" />

  <div v-else class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
    <table class="min-w-full bg-white text-sm">
      <thead class="text-left bg-gray-50 uppercase">
        <tr class="text-center">
          <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Prov ID</th>
          <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Username</th>
          <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Category</th>
          <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Active Services</th>
          <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Active Bookings</th>
          <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Status</th>
          <th scope="col"  class="px-4 py-2">Action</th>
        </tr>
      </thead>

      <tbody class="divide-y divide-gray-200">
          <tr class="odd:bg-white even:bg-gray-50 text-center" v-for="(prov, i) in provData.providers" :key="i">
              <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">{{ prov.id }}</td>
              <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">{{ prov.user.username }}</td>
              <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-700">{{ prov.category.toUpperCase() }} </td>
              <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ prov.active_services }} </td>
              <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ prov.active_bookings }} </td>
              <td class="whitespace-nowrap px-4 py-2 text-gray-700">
                <span v-if="prov.is_approved && prov.is_blocked" class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700 bg-red-100">
                    blocked
                </span>
                <span v-else-if="prov.is_approved" class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700 bg-green-100">
                    active
                </span>
              </td>
              <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
                <RouterLink :to="{ name: 'home' }">
                  <button
                    v-if="prov.is_approved"
                    :disabled="isActionButtonsDisabled"
                    :class="isActionButtonsDisabled? 'bg-indigo-300 cursor-none': 'bg-indigo-600 hover:bg-indigo-700'"
                    class="inline-block rounded bg-indigo-600 px-4 py-2 text-xs font-medium text-white hover:bg-indigo-700"
                  >
                    View
                  </button>
                </RouterLink>
                <button
                  v-if="prov.is_approved && !prov.is_blocked"
                  :disabled="isActionButtonsDisabled"
                  @click="() => handleBlockProvider(prov.id, prov.user.username)"
                  :class="isActionButtonsDisabled? 'bg-red-300 cursor-none': 'bg-red-600 hover:bg-red-700'"
                  class="inline-block rounded  px-4 py-2 text-xs font-medium text-white "
                >
                  Block
                </button>
                <button
                  v-if="prov.is_approved && prov.is_blocked"
                  :disabled="isActionButtonsDisabled"
                  @click="() => handleUnblockProvider(prov.id, prov.user.username)"
                  :class="isActionButtonsDisabled? 'bg-teal-300 cursor-none': 'bg-teal-600 hover:bg-teal-700'"
                  class="inline-block rounded px-4 py-2 text-xs font-medium text-white "
                >
                  Unblock
                </button>
              </td>
          </tr>
      </tbody>
    </table>
  </div>

  <PaginationBar
    v-show="!isActionButtonsDisabled"
    v-if="!isProvDataPending && !isProvDataError"
    :total="provData?.no_of_providers"
    :pages="provData?.no_of_pages"
    :currentPage="page"
    :perPage="provData?.per_page"
    :path="{ name: route.name, query: { page } }"
  />

</section>
</template>
