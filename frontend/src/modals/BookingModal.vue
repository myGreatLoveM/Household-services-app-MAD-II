<script setup>
import { ref } from 'vue';
import { useToast } from 'vue-toastification';
import { useRoute } from 'vue-router';
import { useAuthUserStore } from '@/stores/authUserStore';
import InputField from '@/components/InputField.vue';
import ModalCloseButton from '@/components/ModalCloseButton.vue';

const props = defineProps({
  closeBookingModal: {type: Function}
})

const authUserStore = useAuthUserStore()
const route = useRoute()
const toast = useToast()

const serviceId = route.params.serviceId
const custId = parseInt(authUserStore.customer.id)


const bookingFormFields = {
  bookDate: '',
  fullfillmentDate: '',
  remark: ''
}

const serviceForm = reactive({ ...serviceFormFields })
const serviceFormErrors = reactive({ ...serviceFormFields })
</script>

<template>
<div class="overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 flex justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
  <div class="relative p-4 w-full max-w-md max-h-full">
    <div class="relative bg-emerald-700 rounded-lg shadow">
      <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
        <h3 class="text-lg font-semibold text-white">
          Book Service
        </h3>
        <ModalCloseButton @click="closeBookingModal" />
      </div>

      <div class="p-4 md:p-5">
        <div class="grid gap-4 mb-6 grid-cols-1 md:grid-cols-2 items-center">
          <label for="start-date" class="text-white font-medium">Booking Date:</label>
          <input
            type="date"
            id="start-date"
            name="start-date"
            class="border rounded-lg px-4 py-2 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
        </div>

        <div class="grid gap-4 mb-6 grid-cols-1 md:grid-cols-2 items-center">
          <label for="end-date" class="text-white font-medium">Fullfillment Date:</label>
          <input
            type="date"
            id="end-date"
            name="end-date"
            class="border rounded-lg px-4 py-2 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
        </div>

        <InputField
          id="name"
          label="Name"
          type="text"
          placeholder="Enter name for service"
          v-model="serviceForm.name"
          :error="serviceFormErrors.name"
          classForLabel="block mb-2 text-sm font-medium text-white"
          classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
        />

        <button
          class="bg-blue-700 text-white font-medium rounded-lg text-sm px-5 py-2.5 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Book
        </button>
      </div>

    </div>
  </div>
</div>
</template>