<script setup>
import { reactive, watch, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import ModalCloseButton from '@/components/ModalCloseButton.vue'
import InputField from '@/components/InputField.vue'
import { validateCategoryForm } from '@/validations/categoryFormValidation.js'
import {
  createNewCategoryForAdminDashboard,
  updateExistingCategoryForAdminDashboard,
} from '@/services/adminService.js'
import { parseNumericFields, trimObjectStringValues } from '@/utils'



const props = defineProps({
  mode: { type: String, default: 'CREATE' }, // 'CREATE', 'UPDATE'
  closeCategoryModal: { type: Function, required: true },
  categoryData: { type: Object },
})

const queryClient = useQueryClient()
const toast = useToast()

const categoryFormFields = {
  name: props.categoryData?.name || '',
  basePrice: props.categoryData?.base_price || '',
  minTime: props.categoryData?.min_time_hr || '',
  serviceRate: props.categoryData?.commission_rate || '',
  bookingRate: props.categoryData?.booking_rate || '',
  transactionRate: props.categoryData?.transaction_rate || '',
  description: props.categoryData?.short_description || '',
}

const categoryFormErrorFields = {
  name: '',
  basePrice: '',
  minTime: '',
  serviceRate: '',
  bookingRate: '',
  transactionRate: '',
  description: '',
}

const categoryForm = reactive({ ...categoryFormFields })
const categoryFormErrors = reactive({ ...categoryFormErrorFields })

const isSubmitButtonDisabled = computed(() => {
  return (
    Object.values(categoryFormErrors).some((err) => err !== '') ||
    Object.values(categoryForm).some((f) => f === '')
  )
})

watch(
  () => ({ ...categoryForm }),
  () => {
    validateCategoryForm(categoryForm, categoryFormErrors)
  },
  { deep: true },
)

const {
  isPending: isCreatePending,
  isError: isCreateError,
  error: createError,
  isSuccess: isCreateSuccess,
  mutate: createCategoryMutate,
} = useMutation({
  mutationFn: (data) => createNewCategoryForAdminDashboard(data),
})

const {
  isPending: isUpdatePending,
  isError: isUpdateError,
  error: updateError,
  isSuccess: isUpdateSuccess,
  mutate: updateCategoryMutate,
} = useMutation({
  mutationFn: ({catId, catData}) => updateExistingCategoryForAdminDashboard(catId, catData),
})

watch([isCreateError, createError], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || 'Failed to created category')
  }
})

watch([isUpdateError, updateError], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    toast.error(errorVal.message || 'Failed to update category')
  }
})

watch(isCreateSuccess, () => {
  queryClient.invalidateQueries({
    predicate: (query) => {
      return (
        Array.isArray(query.queryKey) &&
        query.queryKey[0] === 'admin' &&
        query.queryKey[1] === 'categories'
      )
    },
  })
  toast.success('new category created successfully')
  emit('create-category')
  props.closeCategoryModal()
})

watch(isUpdateSuccess, () => {
  queryClient.invalidateQueries({
    predicate: (query) => {
      return (
        Array.isArray(query.queryKey) &&
        query.queryKey[0] === 'admin' &&
        query.queryKey[1] === 'categories'
      )
    },
  })
  toast.success('Category updated successfully')
  emit('update-category')
  props.closeCategoryModal()
})

function handleCreateCategory() {
  const isCategoryFormInvalid = validateCategoryForm(categoryForm, categoryFormErrors)

  if (isCategoryFormInvalid || isSubmitButtonDisabled.value) {
    return toast.error('Category Form is invalid!!!')
  }

  createCategoryMutate(trimObjectStringValues(parseNumericFields({ ...categoryForm })))
}

function handleUpdateCategory() {
  const isCategoryFormInvalid = validateCategoryForm(categoryForm, categoryFormErrors)

  if (isCategoryFormInvalid || isSubmitButtonDisabled.value) {
    return toast.error('Category Form is invalid!!!')
  }
  
  updateCategoryMutate({
    catId: props.categoryData.id, 
    catData: trimObjectStringValues(parseNumericFields({ ...categoryForm }))
  })
}

const emit = defineEmits(['create-category', 'update-category'])
</script>

<template>
  <div
    class="overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 flex justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full"
  >
    <div class="relative p-4 w-full max-w-md max-h-full">
      <div class="relative bg-emerald-700 rounded-lg shadow">
        <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t">
          <h3 class="text-lg font-semibold text-white">
            {{ mode === 'CREATE' ? 'Create Category' : 'Edit Category' }}
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
                v-model="categoryForm.name"
                :error="categoryFormErrors.name"
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
                v-model="categoryForm.basePrice"
                :error="categoryFormErrors.basePrice"
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
                v-model="categoryForm.minTime"
                :error="categoryFormErrors.minTime"
                classForLabel="block mb-2 text-sm font-medium text-white"
                classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
              />
            </div>
            <div class="col-span-2">
              <InputField
                id="serviceRate"
                label="Service Rate"
                labelInfo="(% charge commision for booking)"
                type="number"
                placeholder="Enter minimum time required for a service"
                v-model="categoryForm.serviceRate"
                :error="categoryFormErrors.serviceRate"
                classForLabel="block mb-2 text-sm font-medium text-white"
                classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
              />
            </div>
            <div class="col-span-2">
              <InputField
                id="bookingRate"
                label="Booking Rate"
                labelInfo="(% charge platform fee for booking)"
                type="number"
                placeholder="Enter minimum time required for a service"
                v-model="categoryForm.bookingRate"
                :error="categoryFormErrors.bookingRate"
                classForLabel="block mb-2 text-sm font-medium text-white"
                classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
              />
            </div>
            <div class="col-span-2">
              <InputField
                id="transactionRate"
                label="Transaction Rate"
                labelInfo="(% commission for payment handling for the booking)"
                type="number"
                placeholder="Enter minimum time required for a service"
                v-model="categoryForm.transactionRate"
                :error="categoryFormErrors.transactionRate"
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
                v-model="categoryForm.description"
                :error="categoryFormErrors.description"
                classForLabel="block mb-2 text-sm font-medium text-white"
                classForInputField="bg-white border border-gray-300 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
              />
            </div>
          </div>
          <button
            v-if="mode === 'CREATE'"
            @click="handleCreateCategory"
            :disabled="isSubmitButtonDisabled || isCreatePending"
            :class="
              isSubmitButtonDisabled || isCreatePending
                ? 'bg-blue-500  cursor-none'
                : 'bg-blue-700 hover:bg-blue-800'
            "
            class="text-white inline-flex items-center font-medium rounded-lg text-sm px-5 py-2.5 text-center"
          >
            {{ isCreatePending ? 'Creating...' : 'Create' }}
          </button>

          <button
            v-if="mode === 'UPDATE'"
            @click="handleUpdateCategory"
            :disabled="isSubmitButtonDisabled || isUpdatePending"
            :class="
              isSubmitButtonDisabled || isUpdatePending
                ? 'bg-blue-500  cursor-none'
                : 'bg-blue-700 hover:bg-blue-800'
            "
            class="text-white inline-flex items-center font-medium rounded-lg text-sm px-5 py-2.5 text-center"
          >
            {{ isUpdatePending ? 'Updating...' : 'Update' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
