<script setup>
import { reactive, watch, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { useMutation, useQueryClient } from '@tanstack/vue-query';
import ModalCloseButton from '@/components/ModalCloseButton.vue';
import InputField from '@/components/InputField.vue'
import { createServiceForProvider } from '@/services/providerService.js'

import { parseNumericFields, trimObjectStringValues } from '@/utils';
import { validateServiceForm } from '@/validations/serviceFormValidation';
import { useAuthUserStore } from '@/stores/authUserStore';


const props = defineProps({
  closeServiceModal: {type: Function}
})

const authUserStore = useAuthUserStore()
const queryClient = useQueryClient()
const toast = useToast()

const provId = parseInt(authUserStore.provider.id)

const serviceFormFields = {
  name: '',
  price: '',
  time: '',
  description: ''
}

const serviceForm = reactive({ ...serviceFormFields })
const serviceFormErrors = reactive({ ...serviceFormFields })

const isSubmitButtonDisabled = computed(() => {
  return Object.values(serviceFormErrors).some((err) => err !== '') || Object.values(serviceForm).some((f) => f === '')
})

watch(
  () => ({...serviceForm}),
  () => {
    validateServiceForm(serviceForm, serviceFormErrors)
  },
  { deep: true },
)

const {isPending, isError, error, isSuccess, mutate} = useMutation({
  mutationFn: ({provId, serviceData}) => createServiceForProvider(provId, serviceData)
})

watch([isError, error], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || "Failed to created service!!");
  }
});

watch(isSuccess, () => {
  queryClient.invalidateQueries({
    predicate: (query) => {
      return Array.isArray(query.queryKey) &&
        query.queryKey[0] === 'providers' &&
        query.queryKey[1] === provId &&
        query.queryKey[2] === 'services';
    }
  });
  toast.success('New service created successfully')
  emit('create-service')
  props.closeServiceModal()
})

function handleCreateService() {
  const isServiceFormInvalid = validateServiceForm(serviceForm, serviceFormErrors)

  if (isServiceFormInvalid || isSubmitButtonDisabled.value) {
    return toast.error('Service Form is invalid!!!')
  }

  const serviceData = trimObjectStringValues(parseNumericFields({...serviceForm}))

  mutate({provId, serviceData})
}

const emit = defineEmits(['create-service'])

</script>


<template>
<div class="overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 flex justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
  <div class="relative p-4 w-full max-w-md max-h-full">
    <div class="relative bg-emerald-700 rounded-lg shadow">
      <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
        <h3 class="text-lg font-semibold text-white">
          List Service
        </h3>
        <ModalCloseButton @click="closeServiceModal" />
      </div>

      <div class="p-4 md:p-5">
        <div class="grid gap-4 mb-4 grid-cols-2">
          <div class="col-span-2">
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
          </div>
          <div class="col-span-2">
            <InputField
              id="price"
              label="Price"
              labelInfo="(in INR)"
              type="number"
              placeholder="Enter price to list a service"
              v-model="serviceForm.price"
              :error="serviceFormErrors.price"
              classForLabel="block mb-2 text-sm font-medium text-white"
              classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
            />
          </div>
          <div class="col-span-2">
            <InputField
              id="time"
              label="Time required"
              labelInfo="(in hr)"
              type="number"
              placeholder="Enter minimum time required for a service"
              v-model="serviceForm.time"
              :error="serviceFormErrors.time"
              classForLabel="block mb-2 text-sm font-medium text-white"
              classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
            />
          </div>
          <div class="col-span-2">
            <InputField
              id="description"
              label="Description"
              type="text"
              placeholder="Enter description about the service ...."
              v-model="serviceForm.description"
              :error="serviceFormErrors.description"
              classForLabel="block mb-2 text-sm font-medium text-white"
              classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
            />
          </div>
        </div>
        <button
          @click="handleCreateService"
          :disabled="isSubmitButtonDisabled  || isPending"
          :class="isSubmitButtonDisabled || isPending ? 'bg-blue-500  cursor-none' : 'bg-blue-700 hover:bg-blue-800'"
          class="text-white inline-flex items-center   font-medium rounded-lg text-sm px-5 py-2.5 text-center"
        >
          {{ isPending ? 'Creating...' : 'Create' }}
        </button>
      </div>
    </div>
  </div>
</div>
</template>
