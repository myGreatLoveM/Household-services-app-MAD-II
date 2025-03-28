<script setup>
</script>


<template>
<section class="mx-auto w-full h-full max-w-7xl px-4 py-4">
    <div class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
        <div>
            <h2 class="text-lg font-semibold">Pending Payments</h2>
            <p class="mt-1 text-sm text-gray-700">
                This is a list of all pending payments for confirmed bookings.
            </p>
        </div>
    </div>

    <div class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
        <table class="min-w-full divide-gray-200 bg-white text-sm">
            <thead class="text-left bg-gray-50 uppercase">
                <tr class="text-center">
                    <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Booking ID</th>
                    <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Service</th>
                    <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Provider</th>
                    <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Price</th>
                    <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Booked</th>
                    <th scope="col" class="px-4 py-2">Action</th>
                </tr>
            </thead>

            <tbody class="divide-y divide-gray-200">
                <!-- Replace with dynamically generated rows -->
                <tr class="odd:bg-white even:bg-gray-50 text-center">
                    <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">1</td>
                    <td class="whitespace-nowrap px-4 py-2 text-gray-700">Service Name</td>
                    <td class="whitespace-nowrap px-4 py-2 text-gray-700">Provider Name</td>
                    <td class="whitespace-nowrap px-4 py-2 text-gray-700">500 ₹</td>
                    <td class="whitespace-nowrap px-4 py-2 text-gray-700">2025-03-20</td>
                    <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
                        <a href="/payment/1" class="inline-block rounded bg-blue-600 px-4 py-2 text-xs font-medium text-white hover:bg-blue-700">
                            Pay
                        </a>
                        <a href="#" class="inline-block rounded bg-red-600 px-4 py-2 text-xs font-medium text-white hover:bg-red-700">
                            Cancel
                        </a>
                    </td>
                </tr>
                <!-- Repeat similar rows for other pending payments -->
            </tbody>
        </table>
    </div>
</section>

</template>