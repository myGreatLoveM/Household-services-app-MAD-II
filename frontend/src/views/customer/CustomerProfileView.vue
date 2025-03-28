<script setup>
import { watch, reactive } from 'vue'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { useToast } from 'vue-toastification'
import LoadingState from '@/components/LoadingState.vue'
import ErrorState from '@/components/ErrorState.vue'
import InputField from '@/components/InputField.vue'
import {
  getProfileForCustomerDashboard,
  updateProfileForCustomerDashboard,
} from '@/services/customerService.js'
import { useAuthUserStore } from '@/stores/authUserStore.js'
import { formatDate, trimObjectStringValues } from '@/utils.js'

const queryClient = useQueryClient()
const authUserStore = useAuthUserStore()
const toast = useToast()

const custId = parseInt(authUserStore.customer.id)

const {
  data: custProfileData,
  isPending: isCustProfilePending,
  isError: isCustProfileError,
  error: custProfileError,
} = useQuery({
  queryKey: () => ['customers', custId, 'profile'],
  queryFn: () => getProfileForCustomerDashboard(custId),
})

const {
  isPending: isUpdatePending,
  isSuccess: isUpdateSuccess,
  isError: isUpdateError,
  error: updateError,
  mutate: updateProfileMutate,
} = useMutation({
  mutationFn: ({ custId, profileData }) => updateProfileForCustomerDashboard(custId, profileData),
})

const profileFormFields = {
  firstName: custProfileData.value?.user?.profile?.first_name || '',
  lastName: custProfileData.value?.user?.profile?.last_name || '',
  contact: custProfileData.value?.user?.profile?.contact || '',
  location: custProfileData.value?.user?.profile?.location || '',
  bio: custProfileData.value?.user?.profile?.bio || '',
}

const profileForm = reactive({ ...profileFormFields })

watch([isCustProfileError, custProfileError], ([isErrorVal, errorVal]) => {
  if (isErrorVal && errorVal) {
    console.log(errorVal)
    toast.error(errorVal.message || 'Failed to fetch profile!!')
  }
})

watch(custProfileData, (newData) => {
  const profile = newData?.user?.profile
  profileForm.firstName = profile?.first_name || ''
  profileForm.lastName = profile?.last_name || ''
  profileForm.contact = profile?.contact || ''
  profileForm.location = profile?.location || ''
  profileForm.bio = profile?.bio || ''
})

watch(isUpdateSuccess, (newVal) => {
  if (newVal) {
    queryClient.invalidateQueries({
      predicate: () => (query) => {
        return (
          Array.isArray(query.queryKey) &&
          query.queryKey[0] === 'customers' &&
          query.queryKey[1] === custId &&
          query.queryKey[2] === 'profile'
        )
      },
    })
    toast.success('profile updated')
  }
})

watch(updateError, (newVal) => {
  if (newVal && isUpdateError.value) {
    toast.error('profile update failed')
  }
})

const handleUpdateProfile = () => {
  const profileData = trimObjectStringValues({ ...profileForm })
  updateProfileMutate({ custId, profileData })
}
</script>

<template>
  <div class="container max-w-2xl mx-auto p-6 rounded-lg">
    <LoadingState v-if="isCustProfilePending" />
    <ErrorState v-else-if="isCustProfileError" />

    <div v-else class="bg-white p-6 rounded-lg shadow-md mb-6">
      <div class="mb-5 flex items-center w-full justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-800 mb-1">Profile</h2>
          <h3 class="text-green-600">@{{ custProfileData?.user?.username }}</h3>
        </div>
        <div>
          <h3>Joined on: {{ formatDate(custProfileData?.created_at) }}</h3>
        </div>
      </div>
      <div>
        <div class="flex flex-col gap-6">
          <div>
            <InputField
              id="firstName"
              label="First Name"
              type="text"
              placeholder="Enter your first name"
              v-model="profileForm.firstName"
            />
          </div>
          <div>
            <InputField
              id="lastName"
              label="Last Name"
              type="text"
              placeholder="Enter your last name"
              v-model="profileForm.lastName"
            />
          </div>
          <div>
            <InputField
              id="contact"
              label="Contact"
              type="text"
              placeholder="Enter your contact number"
              v-model="profileForm.contact"
            />
          </div>
          <div>
            <InputField
              id="location"
              label="Location"
              type="text"
              placeholder="Enter your location"
              v-model="profileForm.location"
            />
          </div>
          <div>
            <InputField
              id="bio"
              label="Bio"
              type="text"
              placeholder="Write about yourself"
              v-model="profileForm.bio"
            />
          </div>
        </div>
        <div class="mt-6">
          <button
            @click="handleUpdateProfile"
            :disabled="isUpdatePending"
            :class="isUpdatePending ? 'bg-blue-300' : 'bg-blue-500 hover:bg-blue-600'"
            class="text-white py-2 px-4 rounded-md"
          >
            {{ isUpdatePending ? 'Updating...' : 'Update' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
