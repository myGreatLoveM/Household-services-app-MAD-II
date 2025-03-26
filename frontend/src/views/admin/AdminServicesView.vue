<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import PaginationBar from '@/components/PaginationBar.vue'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { ServiceStatus } from '@/constants.js'
import {
  getAllServicesForAdminDashboard,
  approveOrUnblockServiceForAdminDashboard,
  blockServiceForAdminDashboard,
} from '@/services/adminService.js'

const queryClient = useQueryClient()
const toast = useToast()
const route = useRoute()

const isEnabled = ref(false)
const page = ref(route.query.page ? parseInt(route.query.page) : 1)

const {
  data: serviceData,
  isPending: isServiceDataPending,
  refetch: refetchApprovedServices,
  isError: isServiceDataError,
  error: serviceDataError,
} = useQuery({
  queryKey: () => ['admin', 'services', page.value, ServiceStatus.APPROVED],
  queryFn: async () => await getAllServicesForAdminDashboard(page.value, ServiceStatus.APPROVED),
  keepPreviousData: true,
  enabled: isEnabled.value,
})

const {
  data: blockedServiceData,
  isPending: isBlockPending,
  isSuccess: isBlockSuccess,
  mutate: blockService,
  error: blockError,
  isError: isBlockError,
} = useMutation({
  mutationFn: ({ serviceId, serviceName }) =>
    blockServiceForAdminDashboard({ serviceId, serviceName }),
})

const {
  data: unblockedServiceData,
  isPending: isUnblockPending,
  isSuccess: isUnblockSuccess,
  mutate: unblockService,
  error: unblockError,
  isError: isUnblockError,
} = useMutation({
  mutationFn: ({ serviceId, serviceName }) =>
    approveOrUnblockServiceForAdminDashboard({ serviceId, serviceName }),
})

onMounted(() => {
  isEnabled.value = true
  refetchApprovedServices()
})

watch(serviceDataError, (errorVal) => {
  if (isServiceDataError.value && errorVal) {
    toast.error('Failed to fetch pending services data!!')
  }
})

watch(blockError, (errorVal) => {
  if (isBlockError.value && errorVal) {
    toast.error(`Failed to block service ${blockedServiceData.value.serviceName}!!`)
  }
})

watch(unblockError, (errorVal) => {
  if (isUnblockError.value && errorVal) {
    toast.error(`Failed to unblock service ${unblockedServiceData.value.serviceName}!!`)
  }
})

watch(isBlockSuccess, (isBlockSuccessVal) => {
  if (isBlockSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'admin' &&
          query.queryKey[1] === 'services' &&
          query.queryKey[3] === ServiceStatus.APPROVED
        )
      },
    })
    toast.success(`Service ${blockedServiceData.value.serviceName} blocked..`)
    refetchApprovedServices()
  }
})

watch(isUnblockSuccess, (isUnblockSuccessVal) => {
  if (isUnblockSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'admin' &&
          query.queryKey[1] === 'services' &&
          query.queryKey[3] === ServiceStatus.APPROVED
        )
      },
    })
    toast.success(`Service ${unblockedServiceData.value.serviceName} unblocked..`)
    refetchApprovedServices()
  }
})

watch(
  () => route.query.page,
  (newPage) => {
    page.value = newPage ? parseInt(newPage) : 1
    refetchApprovedServices()
  },
)

const isActionButtonsDisabled = computed(() => isBlockPending.value || isUnblockPending.value)

const handleBlockService = async (serviceId, serviceName) => {
  blockService({ serviceId, serviceName })
}

const handleUnblockService = async (serviceId, serviceName) => {
  unblockService({ serviceId, serviceName })
}
</script>

<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
    <div
      class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0"
    >
      <div>
        <h2 class="text-lg font-semibold">All Services</h2>
        <p class="mt-1 text-sm text-gray-700">This is a list of all verified services.</p>
      </div>

      <div class="flex items-center gap-10">
        <RouterLink
          :to="{ name: 'admin-services-pending' }"
          class="rounded-md bg-zinc-600 hover:bg-zinc-700 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black/80"
        >
          New Listed Services
        </RouterLink>
      </div>
    </div>

    <LoadingState v-if="isServiceDataPending" />
    <ErrorState v-else-if="isServiceDataError" />

    <div v-else class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
      <table class="w-full bg-white text-sm">
        <thead class="text-left bg-gray-50 uppercase">
          <tr class="text-center">
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Service Id
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Name</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Category
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Provider
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Price /hr
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Provider Status
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Status
            </th>
            <th scope="col" class="px-4 py-2">Action</th>
          </tr>
        </thead>

        <tbody class="divide-y divide-gray-200">
          <tr
            class="odd:bg-white even:bg-gray-50 text-center"
            v-for="(service, i) in serviceData.services"
            :key="i"
          >
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">{{ service.id }}</td>
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              {{ service.name }}
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{ service.provider.category.name }}
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{ service.provider.user.username }}
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ service.price }} ₹</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              <span
                v-if="service.provider.is_approved && service.provider.is_blocked"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
              >
                blocked
              </span>
              <span
                v-if="service.provider.is_approved && !service.provider.is_blocked"
                class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700"
              >
                active
              </span>
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              <span
                v-if="service.is_approved && service.is_blocked"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
              >
                blocked
              </span>
              <span
                v-if="service.is_approved && !service.is_blocked && service.is_active"
                class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700"
              >
                active
              </span>
              <span
                v-if="service.is_approved && !service.is_blocked && !service.is_active"
                class="whitespace-nowrap rounded-full border border-yellow-500 px-2.5 py-0.5 text-sm text-yellow-700"
              >
                discontinue
              </span>
            </td>

            <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
              <button
                :disabled="isActionButtonsDisabled"
                :class="isActionButtonsDisabled ? 'bg-indigo-300 cursor-none': 'bg-indigo-600 hover:bg-indigo-700'"
                class="inline-block rounded  px-4 py-2 text-xs font-medium text-white "
              >
                View
              </button>
              <button
                v-if="service.is_approved && !service.is_blocked && service.is_active"
                :disabled="isActionButtonsDisabled"
                @click="() => handleBlockService(service.id, service.name)"
                :class="isActionButtonsDisabled ? 'bg-red-300 cursor-none' : 'bg-red-600 hover:bg-red-700'"
                class="inline-block rounded px-4 py-2 text-xs font-medium text-white"
              >
                Block
              </button>
              <button
                v-if="service.is_approved && service.is_blocked && service.is_active"
                :disabled="isActionButtonsDisabled"
                @click="() => handleUnblockService(service.id, service.name)"
                :class="isActionButtonsDisabled ? 'bg-teal-300 cursor-none' : 'bg-teal-600 hover:bg-teal-700'"
                class="inline-block rounded px-4 py-2 text-xs font-medium text-white"
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
      v-if="!isServiceDataPending && !isServiceDataError"
      :total="serviceData?.no_of_services"
      :pages="serviceData?.no_of_pages"
      :currentPage="page"
      :perPage="serviceData?.per_page"
      :path="{ name: route.name, query: { page } }"
    />
  </section>
</template>
