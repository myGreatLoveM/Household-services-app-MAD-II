<script setup>
</script>


<template>
  <section class="mx-auto w-full max-w-7xl px-4">
  <div class="max-w-full bg-white border border-gray-200 rounded-lg shadow-lg p-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Category Name</h2>
        <p class="text-sm">Created At: Feb 20, 2025</p>
      </div>
      <p class="text-lg font-semibold text-gray-900">Base Price: 500 ₹/hr</p>
    </div>

    <p class="text-gray-600 text-base mt-5">
      This is a placeholder for the category's long description. Replace with actual data.
    </p>

    <hr class="my-4 border-gray-300">

    <div class="grid grid-cols-4 gap-4">
      <!-- Total Providers -->
      <div class="bg-blue-100 p-4 rounded-lg text-center">
        <h5 class="text-xl font-bold text-blue-700">15</h5>
        <p class="text-sm text-blue-600">Service Providers</p>
      </div>
      <!-- Total Services -->
      <div class="bg-purple-100 p-4 rounded-lg text-center">
        <h5 class="text-xl font-bold text-purple-700">35</h5>
        <p class="text-sm text-purple-600">Services Listed</p>
      </div>
      <!-- Total Bookings -->
      <div class="bg-yellow-100 p-4 rounded-lg text-center">
        <h5 class="text-xl font-bold text-yellow-700">100</h5>
        <p class="text-sm text-yellow-600">Total Bookings</p>
      </div>
      <!-- Total Revenue -->
      <div class="bg-green-100 p-4 rounded-lg text-center">
        <h5 class="text-xl font-bold text-green-700">50,000 ₹</h5>
        <p class="text-sm text-green-600">Total Revenue</p>
      </div>
    </div>

    <!-- Active Services Table -->
    <div class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
      <h3 class="text-lg font-medium text-gray-700 mb-4">Active Services</h3>
      <table class="w-full bg-white text-sm">
        <thead class="text-left bg-gray-50 uppercase">
          <tr class="text-center">
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Service Id</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Title</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Provider</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Price /hr</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Avg rating</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Active Bookings</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Total Bookings</th>
            <th scope="col" class="px-4 py-2">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <!-- Loop through services -->
          <tr class="odd:bg-white even:bg-gray-50 text-center">
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">1</td>
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Service Title</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">Provider Name</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">100 ₹</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">4.5</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">10</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">50</td>
            <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
              <a href="#" class="inline-block rounded bg-indigo-600 px-4 py-2 text-xs font-medium text-white hover:bg-indigo-700">
                View
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Active Providers Table -->
    <div class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
      <h3 class="text-lg font-medium text-gray-700 mb-4">Active Providers</h3>
      <table class="w-full bg-white text-sm">
        <thead class="text-left bg-gray-50 uppercase">
          <tr class="text-center">
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Prov Id</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Name</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Avg rating</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Active Services</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Active Bookings</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Total Bookings</th>
            <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Lifetime Earning</th>
            <th scope="col" class="px-4 py-2">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <!-- Loop through providers -->
          <tr class="odd:bg-white even:bg-gray-50 text-center">
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">1</td>
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Provider Name</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">4.5</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">3</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">15</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">50</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">5000 ₹</td>
            <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
              <a href="#" class="inline-block rounded bg-indigo-600 px-4 py-2 text-xs font-medium text-white hover:bg-indigo-700">
                View
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Other Category Info -->
    <div class="mt-3 grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <div class="bg-gray-50 p-4 rounded-lg space-y-1 text-gray-500">
          <p><span class="font-medium">Service Listing Rate:</span> 10%</p>
          <p><span class="font-medium">Service Booking Rate:</span> 5%</p>
          <p><span class="font-medium">Transaction Rate:</span> 2%</p>
        </div>
      </div>
    </div>
  </div>
</section>

</template>
