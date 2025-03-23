<script setup>
import SideBar from '@/components/SideBar.vue'


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
    <SideBar :dashboard-path="provDashboardPathName" :other-paths="provDashboardOtherPaths" />
    <div class="w-full h-full min-h-screen max-h-screen py-8 overflow-y-auto">
      <RouterView />
    </div>
  </div>
</template>
