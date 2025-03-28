<script setup>
import { onMounted, ref, watch } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { useToast } from "vue-toastification";
import { useRoute, useRouter } from "vue-router";
import { getActiveService } from "@/services/coreServices"; 
import BookingModal from "@/modals/BookingModal.vue";
import LoadingState from "@/components/LoadingState.vue";
import ErrorState from "@/components/ErrorState.vue";
import { useAuthUserStore } from '@/stores/authUserStore';


const authUserStore = useAuthUserStore()
const toast = useToast();
const route = useRoute();
const router = useRouter()

const isEnabled = ref(false);
const isBookingModelOpen = ref(false);
const serviceId = route.params.serviceId


const { data, isPending, refetch, isError, error } = useQuery({
  queryKey: () => ['active-services', ],
  queryFn: async () => await getActiveService(serviceId),
  enabled: isEnabled.value,
  keepPreviousData: true,
});


onMounted(async () => {
  isEnabled.value = true;
  refetch();
});


watch([isError, error], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || "Failed to fetch data");
  }
});

const openBookingModal = () => {
  if (authUserStore.isCustomer && !authUserStore.isCustomerBlocked) {
    isBookingModelOpen.value = true;
    emit('booking-modal-open')
  } else {
    router.push({ name: 'login' })
  }
};

const closeBookingModal = () => {
  isBookingModelOpen.value = false;
  emit('booking-modal-close')
};

const emit = defineEmits(['booking-modal-open', 'booking-modal-close'])

</script>

<template>
  <LoadingState v-if="isPending" />
  <ErrorState v-else-if="isError" />

  <div v-else :class="isBookingModelOpen && 'opacity-50'"  class="container min-h-screen max-w-7xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">{{ data.service.name }}</h1>

        <div class="flex items-center mt-2">
          <div>
            <a >
              <p class="text-lg font-medium text-indigo-900">@{{ data.service.provider.user.username }}</p>
            </a>
          </div>
        </div>
      </div>

      <div class="flex items-center gap-10">
        <div class="text-right">
          <p class="text-lg text-gray-900 font-semibold">
            Starting from Service Price <span class="text-green-500 text-xl font-medium">{{ data.service.price }} ₹/hr</span> 
          </p>
          <p class="text-md text-gray-900 font-semibold">
            Time Required <span class="text-purple-500 text-lg font-medium">{{ data.service.time_required_hr }} hr</span> 
          </p>
        </div>

        <button
          @click="openBookingModal"
          class="bg-blue-500 text-white text-normal font-semibold px-5 py-2 rounded-lg hover:bg-blue-600"
        >
          Book Now
        </button>
      </div>
    </div>

    <div class="mb-8">
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">Description and Details</h2>
      <p class="text-gray-700 text-lg mb-4">{{ data.service.description }}</p>
      <ul class="list-disc ml-6 text-gray-600">
        <li>Lorem ipsum dolor sit amet.</li>
        <li>Lorem ipsum dolor sit amet consectetur adipisicing elit. Iusto, rerum.</li>
        <li>Magni ea, deleniti qui officiis adipisci.</li>
        <li>Iusto ipsa consequuntur? Nisi error quod provident suscipit.</li>
      </ul>
    </div>
  </div>

  <BookingModal v-if="isBookingModelOpen" :close-booking-modal="closeBookingModal" />
</template>
