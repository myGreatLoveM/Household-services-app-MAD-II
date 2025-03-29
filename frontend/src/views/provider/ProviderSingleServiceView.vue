<script setup>
</script>


<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
    <div class="bg-white rounded-lg shadow-lg p-6 max-w-full">
        <!-- Service Header -->
        <div class="flex justify-between items-center">
            <div>
                <h3 class="text-xl font-bold text-gray-800">Service Title</h3>
                <p class="text-sm text-gray-500">Category: Category Name</p>
            </div>
            <div class="text-right">
                <p class="text-lg font-semibold text-gray-900">1000 ₹ <span class="text-sm font-normal">/hr</span></p>
                <p class="text-sm text-gray-500">Time Required: 2 Hours</p>
            </div>
        </div>

        <!-- Divider -->
        <hr class="my-4">

        <!-- Provider Information -->
        <div class="flex justify-between items-center">
            <div>
                <h4 class="text-md font-semibold text-gray-800">Avg Rating: 4.5</h4>
                <p class="text-sm text-gray-500">No of reviews: 50</p>
            </div>
            <div>
                <p class="text-sm text-green-700 font-semibold">Active Bookings: 10</p>
                <p class="text-sm text-blue-600 font-semibold">Total Bookings: 200</p>
            </div>  
        </div>

        <!-- Booking History (Example Data) -->
        <hr class="my-4">
        <div class="overflow-x-auto">
            <h4 class="text-md font-semibold text-gray-800 mb-2">Booking History</h4>
            <table class="min-w-full divide-gray-200 bg-white text-sm">
                <thead class="text-left bg-gray-50 uppercase">
                    <tr class="text-center">
                        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Booking ID</th>
                        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Customer</th>
                        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Status</th>
                        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Payment Status</th>
                        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Booked On</th>
                        <th scope="col" class="px-4 py-2">Action</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                    <!-- Example Row -->
                    <tr class="odd:bg-white even:bg-gray-50 text-center">
                        <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">12345</td>
                        <td class="whitespace-nowrap px-4 py-2 text-gray-700">John Doe</td>
                        <td class="whitespace-nowrap px-4 py-2 text-gray-700">
                            <span class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700 bg-green-100">active</span>
                        </td>
                        <td class="whitespace-nowrap px-4 py-2 text-gray-700">
                            <span class="whitespace-nowrap rounded-full border border-yellow-500 px-2.5 py-0.5 text-sm text-yellow-700">pending</span>
                        </td>
                        <td class="whitespace-nowrap px-4 py-2 text-gray-700">March 28, 2025</td>
                        <td class="whitespace-nowrap px-4 py-2 flex justify-center gap-3">
                            <a href="#"
                               class="inline-block rounded bg-indigo-600 px-4 py-2 text-xs font-medium text-white hover:bg-indigo-700">Detail</a>
                            <a href="#"
                               class="inline-block rounded bg-zinc-600 px-4 py-2 text-xs font-medium text-white hover:bg-zinc-700">Close</a>
                        </td>
                    </tr>
                    <!-- Add more rows as needed -->
                </tbody>
            </table>
        </div>

        <!-- Divider -->
        <hr class="my-4">

        <!-- Customer Reviews & Ratings (Example) -->
        <div class="mt-4">
            <h4 class="text-md font-semibold text-gray-800 mb-2">Customer Reviews & Ratings</h4>
            <div class="space-y-4">
                <div class="bg-gray-100 p-4 rounded-lg">
                    <div class="flex justify-between">
                        <p class="text-sm font-semibold text-gray-800">Jane Smith</p>
                        <div class="flex items-center">
                            <!-- Example rating: 4 stars -->
                            <svg class="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.283 3.953a1 1 0 00.95.691h4.17c.969 0 1.371 1.24.588 1.81l-3.383 2.457a1 1 0 00-.364 1.118l1.283 3.953c.3.921-.755 1.688-1.54 1.118l-3.383-2.457a1 1 0 00-1.175 0l-3.383 2.457c-.785.57-1.839-.197-1.54-1.118l1.283-3.953a1 1 0 00-.364-1.118L2.268 9.381c-.783-.57-.381-1.81.588-1.81h4.17a1 1 0 00.95-.691l1.283-3.953z"></path>
                            </svg>
                            <!-- Add more stars as needed -->
                        </div>
                    </div>
                    <p class="text-sm text-gray-600 mt-2">Great service, highly recommended!</p>
                </div>
            </div>
        </div>
    </div>
</section>

</template>