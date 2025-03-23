<script setup>
import SideBar from '@/components/SideBar.vue'


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
    <SideBar :dashboard-path="custDashboardPathName" :other-paths="custDashboardOtherPaths" />
    <div class="w-full h-full min-h-screen max-h-screen py-8 overflow-y-auto">
      <RouterView />
    </div>
  </div>
</template>
