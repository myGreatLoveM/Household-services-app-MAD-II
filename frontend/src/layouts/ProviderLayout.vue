<script setup>
import { ref } from 'vue'
import SideBar from '@/components/SideBar.vue'

const isModalOpen = ref(false)

function handleModal() {
  isModalOpen.value = !isModalOpen.value
}


const provDashboardPathName = "provider-dashboard"

const provDashboardOtherPaths = [
  { name: 'Services', pathName: 'provider-services' },
  { name: 'Bookings', pathName: 'provider-bookings' },
  { name: 'Payments', pathName: 'provider-payments' },
  { name: 'Profile', pathName: 'provider-profile' },
  { name: 'Logout', pathName: 'logout' },
]
</script>

<template>
  <div class="w-full h-full min-h-screen flex overflow-y-auto">
    <SideBar :dashboard-path="provDashboardPathName" :other-paths="provDashboardOtherPaths" :is-modal-open="isModalOpen" />
    <div class="w-full h-full min-h-screen max-h-screen py-8 overflow-y-auto">
      <RouterView @service-modal-open="handleModal" @service-modal-close="handleModal" />
    </div>
  </div>
</template>
