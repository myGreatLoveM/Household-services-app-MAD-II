<script setup>
import { ref } from 'vue'
import SideBar from '@/components/SideBar.vue'

const isModalOpen = ref(false)

function handleModal() {
  isModalOpen.value = !isModalOpen.value
}


const custDashboardPathName = "customer-dashboard"

const custDashboardOtherPaths = [
  { name: 'Bookings', pathName: 'customer-bookings' },
  { name: 'Payments', pathName: 'customer-payments' },
  { name: 'Profile', pathName: 'customer-profile' },
  { name: 'Logout', pathName: 'logout' },
]
</script>


<template>
  <div class="w-full h-full min-h-screen flex overflow-y-auto">
    <SideBar :dashboard-path="custDashboardPathName" :other-paths="custDashboardOtherPaths" :is-modal-open="isModalOpen" />
    <div class="w-full h-full min-h-screen max-h-screen py-8 overflow-y-auto">
      <RouterView @review-modal-open="handleModal" @review-modal-close="handleModal"  />
    </div>
  </div>
</template>
