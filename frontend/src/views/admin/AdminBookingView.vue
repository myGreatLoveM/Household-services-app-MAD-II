<script setup>
</script>



<template>

<section class="mx-auto w-full max-w-7xl px-4 py-4">
<div class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
    <div>
      <h2 class="text-lg font-semibold">All Bookings</h2>
      <p class="mt-1 text-sm text-gray-700">
        This is a list of all bookings
      </p>
    </div>

</div>


<div class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
  <table class="min-w-full divide-gray-200 bg-white text-sm">
    <thead class="text-center bg-gray-50 uppercase">
      <tr class="">
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Booking Id</th>
        <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Service</th>
        <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Category</th>
        <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Customer</th>
        <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Service Price</th>
        <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Status</th>
        <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Payment Status</th>
        <th scope="col"  class="px-4 py-2">Action</th>
      </tr>
    </thead>

    <tbody class="divide-y divide-gray-200 text-center ">
            <tr class="odd:bg-white even:bg-gray-50">
                <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">booking.id</td>
                <td class="whitespace-nowrap px-4 py-2 text-gray-700">service.title</td>
                <td class="whitespace-nowrap px-4 py-2 text-gray-700">service.category</td>
                <td class="whitespace-nowrap px-4 py-2 text-gray-700">customer.full_name</td>
                <td class="whitespace-nowrap px-4 py-2 text-gray-700">service.price ₹</td>
                <td class="whitespace-nowrap px-4 py-2 text-gray-700">
                  <span
                  class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
                  >
                  rejected
                  </span>
                  <span
                  class="whitespace-nowrap rounded-full border border-purple-500 px-2.5 py-0.5 text-sm text-purple-700 bg-purple-100"
                  >
                  confirmed
                  </span>
                  <span
                  class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700 bg-green-100"
                  >
                  active
                  </span>
                  <span
                  class="whitespace-nowrap rounded-full border border-pink-500 px-2.5 py-0.5 text-sm text-pink-700 bg-pink-100"
                  >
                  completed
                  </span>
                  <span
                  class="whitespace-nowrap rounded-full border border-zinc-500 px-2.5 py-0.5 text-sm text-zinc-700 bg-zinc-100"
                  >
                  closed
                  </span>
                </td>
                <td class="whitespace-nowrap px-4 py-2 text-gray-700">
                    <span
                    class="whitespace-nowrap rounded-full border border-yellow-500 px-2.5 py-0.5 text-sm text-yellow-700"
                    >
                    pending
                    </span>
                    <span
                    class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700"
                    >
                    paid
                    </span>
                </td>
                <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
                    <a
                        href="#"
                        class="inline-block rounded bg-indigo-600 px-4 py-2 text-xs font-medium text-white hover:bg-indigo-700"
                    >
                      View
                    </a>
                </td>
            </tr>
    </tbody>
  </table>
</div>
</section>
</template>

