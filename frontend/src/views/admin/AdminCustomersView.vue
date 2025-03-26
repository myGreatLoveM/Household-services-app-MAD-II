<script setup>
</script>



<template>
<section class="mx-auto w-full max-w-7xl px-4 py-4">
<div class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
    <div>
      <h2 class="text-lg font-semibold">All Customers</h2>
      <p class="mt-1 text-sm text-gray-700">
        This is a list of customers
      </p>
    </div>
</div>


<div class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
  <table class="min-w-full bg-white text-sm">
    <thead class="text-left bg-gray-50 uppercase">
      <tr class="text-center">
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Cust Id</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Name</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Location</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Active Bookings</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Total Bookings</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Lifetime Spent</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Status</th>

        <th scope="col" class="px-4 py-2">Action</th>
      </tr>
    </thead>

    <tbody class="divide-y divide-gray-200">
        <tr class="odd:bg-white even:bg-gray-50 text-center">
          <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">customer.id</td>
          <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">customer.full_name</td>
          <td class="whitespace-nowrap px-4 py-2 ">customer.user.profile.location</td>
          <td class="whitespace-nowrap px-4 py-2 text-gray-700">total_active_bookings</td>
          <td class="whitespace-nowrap px-4 py-2 text-gray-700">total_bookings</td>
          <td class="whitespace-nowrap px-4 py-2 text-gray-700">lifetime_spent ₹</td>
          <td class="whitespace-nowrap px-4 py-2 text-gray-700">
            <span class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700 bg-red-100">
                blocked
            </span>
            <span class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700 bg-green-100">
                active
            </span>
          </td>
          <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
            <a
              href="#"
              class="inline-block rounded bg-indigo-600 px-4 py-2 text-xs font-medium text-white hover:bg-indigo-700"
            >
              View
            </a>
            <a
              href="#"
              class="inline-block rounded bg-red-600 px-4 py-2 text-xs font-medium text-white hover:bg-red-700"
            >
              Block
            </a>
            <a
              href="#"
              class="inline-block rounded bg-teal-600 px-4 py-2 text-xs font-medium text-white hover:bg-teal-700"
            >
              Unblock
            </a>
          </td>
        </tr>
    </tbody>
  </table>
</div>
</section>

</template>
