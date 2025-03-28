<script setup>

</script>


<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
    <div class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
        <div>
            <h2 class="text-lg font-semibold">All Payments</h2>
            <p class="mt-1 text-sm text-gray-700">This is a list of all payments</p>
        </div>

        <div class="flex items-center gap-10">
            <button
                type="button"
                class="rounded-md bg-zinc-600 hover:bg-zinc-700 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black">
                <a href="/pending-payments">Pending Payments</a>
            </button>
        </div>
    </div>

    <div class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
        <table class="min-w-full divide-gray-200 bg-white text-sm">
            <thead class="text-left bg-gray-50 uppercase">
                <tr class="text-center">
                    <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Payment Id</th>
                    <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Booking Id</th>
                    <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Service</th>
                    <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Provider</th>
                    <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Total amount</th>
                    <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Book on</th>
                    <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Paid on</th>
                    <th scope="col" class="px-4 py-2">Action</th>
                </tr>
            </thead>

            <tbody class="divide-y divide-gray-200">
                <tr class="odd:bg-white even:bg-gray-50 text-center">
                    <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">1</td>
                    <td class="whitespace-nowrap px-4 py-2 text-gray-700">123</td>
                    <td class="whitespace-nowrap px-4 py-2 text-gray-700">Service Name</td>
                    <td class="whitespace-nowrap px-4 py-2 text-gray-700">Provider Name</td>
                    <td class="whitespace-nowrap px-4 py-2 text-gray-700">1000 ₹</td>
                    <td class="whitespace-nowrap px-4 py-2 text-gray-700">2025-03-20</td>
                    <td class="whitespace-nowrap px-4 py-2 text-gray-700">2025-03-25</td>
                    <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
                        <a href="/booking/123" class="inline-block rounded bg-indigo-600 px-4 py-2 text-xs font-medium text-white hover:bg-indigo-700">
                            Detail
                        </a>
                    </td>
                </tr>
                <!-- Repeat similar rows for other payments -->
            </tbody>
        </table>
    </div>
</section>

</template>