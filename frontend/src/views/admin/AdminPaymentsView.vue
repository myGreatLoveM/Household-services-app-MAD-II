<script setup>
</script>


<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
    <div class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
      <div>
        <h2 class="text-lg font-semibold">All Payments</h2>
        <p class="mt-1 text-sm text-gray-700">
          This is a list of payments for confirmed bookings
        </p>
      </div>
    </div>


<div class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
  <table class="min-w-full bg-white text-sm">
    <thead class="text-left bg-gray-50 uppercase">
      <tr class="text-center">
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Payment Id</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Booking Id</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Service</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Customer</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Total Amount</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Payed on</th>
        <th scope="col" class="px-4 py-2">Action</th>
      </tr>
    </thead>

    <tbody class="divide-y divide-gray-200">
        <tr class="odd:bg-white even:bg-gray-50 text-center">
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">payment.id</td>
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">payment.booking.id</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">payment.booking.service.title </td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">payment.booking.customer.full_nam</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">payment.total_amount ₹</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">payment.created_at.strftime("%b, %d-%Y")</td>
            <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
              <a href="#" class="inline-block rounded bg-indigo-600 px-4 py-2 text-xs font-medium text-white hover:bg-indigo-700">
                  View
              </a>
            </td>
        </tr>
    </tbody>
  </table>
</div>
</section>
</template>
