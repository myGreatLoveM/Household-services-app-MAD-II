<script setup>
import { reactive, watch, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { useMutation, useQueryClient } from '@tanstack/vue-query';
import ModalCloseButton from '@/components/ModalCloseButton.vue';
import InputField from '@/components/InputField.vue'
import { validateCategoryForm } from '@/validations/categoryFormValidation.js';
import { createNewCategoryForAdminDashboard } from '@/services/adminService.js'
import { parseNumericFields, trimObjectStringValues } from '@/utils';

const props = defineProps({
  closeCategoryModal: {type: Function}
})

const queryClient = useQueryClient()
const toast = useToast()

const addCategoryFormFields = {
  name: '',
  basePrice: '',
  minTime: '',
  serviceRate: '',
  bookingRate: '',
  transactionRate: '',
  description: ''
}

const addCategoryForm = reactive({ ...addCategoryFormFields })
const addCategoryFormErrors = reactive({ ...addCategoryFormFields })

const isSubmitButtonDisabled = computed(() => {
  return Object.values(addCategoryFormErrors).some((err) => err !== '') || Object.values(addCategoryForm).some((f) => f === '')
})

watch(
  () => ({...addCategoryForm}),
  () => {
    validateCategoryForm(addCategoryForm, addCategoryFormErrors)
  },
  { deep: true },
)


const {isPending, isError, error, isSuccess, mutate} = useMutation({
  mutationFn: (data) => createNewCategoryForAdminDashboard(data)
})

watch([isError, error], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || "Failed to created category");
  }
});

watch(isSuccess, () => {
  queryClient.invalidateQueries({
    predicate: (query) => {
      return Array.isArray(query.queryKey) &&
        query.queryKey[0] === 'admin' &&
        query.queryKey[1] === 'categories';
    }
  });
  toast.success('new category created successfully')
  emit('create-category')
  props.closeCategoryModal()
})

function handleCreateCategory() {
  const isCategoryFormInvalid = validateCategoryForm(addCategoryForm, addCategoryFormErrors)

  if (isCategoryFormInvalid || isSubmitButtonDisabled.value) {
    return toast.error('Category Form is invalid!!!')
  }

  mutate(trimObjectStringValues(parseNumericFields({...addCategoryForm})))
}

const emit = defineEmits(['create-category'])
</script>

<template>
<div class="overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 flex justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
  <div class="relative p-4 w-full max-w-md max-h-full">
    <div class="relative bg-emerald-700 rounded-lg shadow">
      <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
        <h3 class="text-lg font-semibold text-white">
          Add New Category
        </h3>
        <ModalCloseButton @click="closeCategoryModal" />
      </div>

      <div class="p-4 md:p-5">
        <div class="grid gap-4 mb-4 grid-cols-2">
          <div class="col-span-2">
            <InputField
              id="name"
              label="Name"
              type="text"
              placeholder="Enter name for category"
              v-model="addCategoryForm.name"
              :error="addCategoryFormErrors.name"
              classForLabel="block mb-2 text-sm font-medium text-white"
              classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
            />
          </div>
          <div class="col-span-2">
            <InputField
              id="basePrice"
              label="Base Price"
              labelInfo="(in INR)"
              type="number"
              placeholder="Enter base price "
              v-model="addCategoryForm.basePrice"
              :error="addCategoryFormErrors.basePrice"
              classForLabel="block mb-2 text-sm font-medium text-white"
              classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
            />
          </div>
          <div class="col-span-2">
            <InputField
              id="minTime"
              label="Min time"
              labelInfo="(in hr)"
              type="number"
              placeholder="Enter minimum time required for a service"
              v-model="addCategoryForm.minTime"
              :error="addCategoryFormErrors.minTime"
              classForLabel="block mb-2 text-sm font-medium text-white"
              classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
            />
          </div>
          <div class="col-span-2">
            <InputField
              id="serviceRate"
              label="Service Rate"
              labelInfo="(% charge levy on the service listing)"
              type="number"
              placeholder="Enter minimum time required for a service"
              v-model="addCategoryForm.serviceRate"
              :error="addCategoryFormErrors.serviceRate"
              classForLabel="block mb-2 text-sm font-medium text-white"
              classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
            />
          </div>
          <div class="col-span-2">
            <InputField
              id="bookingRate"
              label="Booking Rate"
              labelInfo="(% charge levy on the booking of the service)"
              type="number"
              placeholder="Enter minimum time required for a service"
              v-model="addCategoryForm.bookingRate"
              :error="addCategoryFormErrors.bookingRate"
              classForLabel="block mb-2 text-sm font-medium text-white"
              classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
            />
          </div>
          <div class="col-span-2">
            <InputField
              id="transactionRate"
              label="Transaction Rate"
              labelInfo="(% commission for payment handling for the  booking)"
              type="number"
              placeholder="Enter minimum time required for a service"
              v-model="addCategoryForm.transactionRate"
              :error="addCategoryFormErrors.transactionRate"
              classForLabel="block mb-2 text-sm font-medium text-white"
              classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
            />
          </div>
          <div class="col-span-2">
            <InputField
              id="description"
              label="Description"
              type="text"
              placeholder="Enter description about the category ...."
              v-model="addCategoryForm.description"
              :error="addCategoryFormErrors.description"
              classForLabel="block mb-2 text-sm font-medium text-white"
              classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
            />
          </div>
        </div>
        <button
          @click="handleCreateCategory"
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
