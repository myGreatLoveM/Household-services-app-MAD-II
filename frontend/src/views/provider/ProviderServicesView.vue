<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import { useRoute } from 'vue-router'
import ServiceListModal from '@/modals/ServiceListModal.vue'
import PaginationBar from '@/components/PaginationBar.vue'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import { formatDate } from '@/utils.js'
import {
  getAllServicesForProviderDashboard,
  continueServiceForProviderDashboard,
  discontinueServiceForProviderDashboard,
} from '@/services/providerService'
import { useAuthUserStore } from '@/stores/authUserStore'

const queryClient = useQueryClient()
const authUserStore = useAuthUserStore()
const toast = useToast()
const route = useRoute()

const isEnabled = ref(false)
const page = ref(route.query.page ? parseInt(route.query.page) : 1)
const isServiceModalOpen = ref(false)
const provId = parseInt(authUserStore.provider.id)

const {
  data: serviceData,
  isPending: isServiceDataPending,
  refetch: refetchServices,
  isError: isServiceDataError,
  error: serviceDataError,
} = useQuery({
  queryKey: () => ['providers', provId, 'services', page.value],
  queryFn: () => getAllServicesForProviderDashboard(provId, page.value),
  enabled: isEnabled.value,
  keepPreviousData: true,
})

const {
  data: discontinueServiceData,
  isPending: isDiscontinuePending,
  isSuccess: isDiscontinueSuccess,
  mutate: discontinueServiceMutate,
  error: discontinueError,
  isError: isDiscontinueError,
} = useMutation({
  mutationFn: ({ serviceId, serviceName }) =>
    discontinueServiceForProviderDashboard(provId, { serviceId, serviceName }),
})

const {
  data: continueServiceData,
  isPending: isContinuePending,
  isSuccess: isContinueSuccess,
  mutate: continueServiceMutate,
  error: continueError,
  isError: isContinueError,
} = useMutation({
  mutationFn: ({ serviceId, serviceName }) =>
    continueServiceForProviderDashboard(provId, { serviceId, serviceName }),
})

onMounted(async () => {
  isEnabled.value = true
  refetchServices()
})

watch([isServiceDataError, serviceDataError], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || 'Failed to fetch service data')
  }
})

watch(discontinueError, (errorVal) => {
  if (isDiscontinueError.value && errorVal) {
    toast.error(`Failed to discontinue service ${discontinueServiceData.value.serviceName}!!`)
  }
})

watch(continueError, (errorVal) => {
  if (isContinueError.value && errorVal) {
    toast.error(`Failed to continue service ${continueServiceData.value.serviceName}!!`)
  }
})

watch(isDiscontinueSuccess, (isDiscontinueSuccessVal) => {
  if (isDiscontinueSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'providers' &&
          query.queryKey[2] === 'services'
        )
      },
    })
    toast.success(`Service ${discontinueServiceData.value.serviceName} discontinued..`)
    refetchServices()
  }
})

watch(isContinueSuccess, (isContinueSuccessVal) => {
  if (isContinueSuccessVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'providers' &&
          query.queryKey[2] === 'services'
        )
      },
    })
    toast.success(`Service ${continueServiceData.value.serviceName} continued..`)
    refetchServices()
  }
})

watch(
  () => route.query.page,
  (newPage) => {
    page.value = newPage ? parseInt(newPage) : 1
    refetchServices()
  },
)

const openServiceModal = () => {
  isServiceModalOpen.value = true
  emit('serviceModalOpen')
}

const closeServiceModal = () => {
  isServiceModalOpen.value = false
  emit('serviceModalClose')
}

const isActionButtonsDisabled = computed(
  () => isDiscontinuePending.value || isContinuePending.value,
)

const handleDiscontinueService = async (serviceId, serviceName) => {
  discontinueServiceMutate({ serviceId, serviceName })
}

const handleContinueService = async (serviceId, serviceName) => {
  continueServiceMutate({ serviceId, serviceName })
}

const emit = defineEmits(['serviceModalOpen', 'serviceModalClose'])
</script>

<template>
  <section :class="isServiceModalOpen && 'opacity-50'" class="mx-auto w-full max-w-7xl px-4 py-4">
    <div
      class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0"
    >
      <div>
        <h2 class="text-lg font-semibold">All Services</h2>
        <p class="mt-1 text-sm text-gray-700">This is a list of all services.</p>
      </div>

      <div class="flex items-center gap-10">
        <button
          @click="openServiceModal"
          class="rounded-md bg-black px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
        >
          List Service
        </button>
      </div>
    </div>

    <LoadingState v-if="isServiceDataPending" />
    <ErrorState v-else-if="isServiceDataError" />
    <div
      class="text-xl font-medium w-full text-center mt-10"
      v-else-if="serviceData.services.length === 0"
    >
      No Services Listed
    </div>

    <div v-else class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
      <table class="w-full bg-white text-sm">
        <thead class="text-left bg-gray-50 uppercase">
          <tr class="text-center">
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Service ID
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Name</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Price /hr
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Status
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Avg Rating
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Total Bookings
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Lifetime Earning
            </th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">
              Listed On
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
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ service.price }} ₹</td>
            <td class="whitespace-nowrap px-4 py-2">
              <span
                v-if="!service.is_approved"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
              >
                pending
              </span>
              <span
                v-else-if="service.is_blocked"
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
              >
                blocked
              </span>
              <span
                v-else-if="service.is_active"
                class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700"
              >
                active
              </span>
              <span
                v-else
                class="whitespace-nowrap rounded-full border border-yellow-500 px-2.5 py-0.5 text-sm text-yellow-700"
              >
                discontinue
              </span>
            </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ service.avg_rating }}</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">{{ service.active_bookings }}</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">10,000 ₹</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
              {{ formatDate(service.created_at) }}
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
                @click="() => handleDiscontinueService(service.id, service.name)"
                :class="
                  isActionButtonsDisabled ? 'bg-red-300 cursor-none' : 'bg-red-600 hover:bg-red-700'
                "
                class="inline-block rounded px-4 py-2 text-xs font-medium text-white"
              >
                Discontinue
              </button>
              <button
                v-if="service.is_approved && !service.is_blocked && !service.is_active"
                :disabled="isActionButtonsDisabled"
                @click="() => handleContinueService(service.id, service.name)"
                :class="
                  isActionButtonsDisabled
                    ? 'bg-teal-300 cursor-none'
                    : 'bg-teal-600 hover:bg-teal-700'
                "
                class="inline-block rounded px-4 py-2 text-xs font-medium text-white"
              >
                Continue
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <PaginationBar
      v-if="!isServiceDataPending && !isServiceDataError"
      :total="serviceData?.no_of_services"
      :pages="serviceData?.no_of_pages"
      :currentPage="page"
      :perPage="serviceData?.per_page"
      :path="{ name: route.name, query: { page } }"
    />
  </section>

  <ServiceListModal
    v-if="isServiceModalOpen"
    :close-service-modal="closeServiceModal"
    @create-service="refetchServices"
  />
</template>
