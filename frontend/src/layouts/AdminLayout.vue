<script setup>
import SideBar from '@/components/SideBar.vue'
import { ref } from 'vue'

const isModalOpen = ref(false)

function handleModal() {
  isModalOpen.value = !isModalOpen.value
}

const adminDashboardPathName = "admin-dashboard"

const adminDashboardOtherPaths = [
  { name: 'Categories', pathName: 'admin-categories' },
  { name: 'Services', pathName: 'admin-services' },
  { name: 'Providers', pathName: 'admin-providers' },
  { name: 'Customers', pathName: 'admin-customers' },
  { name: 'Bookings', pathName: 'admin-bookings' },
  { name: 'Payments', pathName: 'admin-payments' },
  { name: 'Logout', pathName: 'logout' }
]
</script>

<template>
  <div class="w-full h-full min-h-screen flex overflow-y-auto">
    <SideBar :dashboard-path="adminDashboardPathName" :other-paths="adminDashboardOtherPaths" :is-modal-open="isModalOpen" />
    <div class="w-full h-full min-h-screen max-h-screen py-8 overflow-y-auto">
      <RouterView @category-modal-open="handleModal" @category-modal-close="handleModal" />
    </div>
  </div>
</template>
