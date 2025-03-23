<script setup>

</script>



<template>

  <div class="min-h-screen py-6">
    <div class="max-w-7xl mx-auto">
        <form method="POST" action="#" class="relative max-w-xl ml-auto flex items-center gap-5">
            <input
                type="text"
                name="search_by"
                class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-blue-200"
                placeholder="Search services by provider name, location, or category"
                id="search-input">
            <button type="submit" class="px-6 bg-fuchsia-500 text-white font-bold py-2 rounded-lg hover:bg-fuchsia-700">Search</button>
        </form>
        <div class="flex mt-5">
            <div class="w-1/4 bg-white p-6 border rounded-lg shadow-md mr-6 h-fit">
                <h2 class="text-xl font-semibold mb-4">Filter Services</h2>

               <form method="POST" action="#">
                    <div class="mb-6">
                        <h3 class="text-md font-medium text-gray-700 mb-2">Category</h3>
                        <ul class="space-y-2">
                            <li>
                                <label class="flex items-center">
                                    <input type="checkbox" name="category" value="Category Name" class="form-checkbox h-4 w-4 text-blue-600">
                                    <span class="ml-2 text-gray-700">Category Name</span>
                                </label>
                            </li>
                        </ul>
                    </div>

                    <!-- Price Range -->
                    <div class="mb-6">
                        <h3 class="text-md font-medium text-gray-700 mb-2">Price Range</h3>
                        <div class="flex gap-2 mb-2">
                            <input type="number" name="min_price" min=0 placeholder="₹ Min" class="w-1/2 px-3 py-2 bg-gray-100 rounded-lg border">
                            <input type="number" name="max_price" min=0 placeholder="₹ Max" class="w-1/2 px-3 py-2 bg-gray-100 rounded-lg border">
                        </div>
                    </div>

                    <button type="submit" class="w-full mt-5 bg-teal-600 text-white font-bold py-2 rounded-lg hover:bg-teal-700">Apply</button>
                </form>
            </div>

            <!-- Main Content: Service Cards Grid -->
            <div class="flex-grow">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                    <!-- Service Cards Example -->
                    <div class="max-w-sm bg-white shadow-lg border rounded-xl overflow-hidden transform transition duration-500 hover:scale-105 hover:shadow-xl">
                        <!-- Card Content -->
                        <div class="p-6">
                            <!-- Service Title -->
                            <h2 class="text-2xl font-bold text-gray-900 mb-2">Service Title</h2>

                            <!-- Service Description -->
                            <p class="text-gray-600 mb-4">This service offers a complete solution for your needs, providing high-quality results with experienced professionals.</p>

                            <!-- Time, Rate, and Verified Badge -->
                            <div class="flex justify-between items-center mb-4">
                                <div>
                                    <span class="text-sm text-gray-500">⏱ 60 mins</span>
                                    <p class="text-sm text-gray-500">Base rate: <span class="text-blue-600">₹ Price</span></p>
                                </div>
                                <span class="bg-green-100 text-green-800 text-xs font-semibold px-2 py-1 rounded-full">Category Name</span>
                            </div>

                            <!-- Provider Information -->
                            <div class="flex items-center mb-4">
                                <img class="w-12 h-12 rounded-full border-2 border-blue-500 mr-4" src="#" alt="Provider Avatar">
                                <div>
                                    <p class="text-sm font-medium text-gray-900">Provider Name</p>
                                    <p class="text-xs text-gray-500">X yr experience</p>
                                </div>
                            </div>

                            <!-- Ratings and Bookings -->
                            <div class="flex justify-between items-center mb-4">
                                <div class="flex items-center">
                                    <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.367 4.204a1 1 0 00.95.69h4.473c.967 0 1.371 1.24.588 1.81l-3.632 2.64a1 1 0 00-.364 1.118l1.368 4.205c.3.921-.755 1.688-1.54 1.118L10 15.917l-3.631 2.64c-.785.57-1.841-.197-1.54-1.118l1.368-4.205a1 1 0 00-.364-1.118l-3.632-2.64c-.783-.57-.379-1.81.588-1.81h4.473a1 1 0 00.95-.69l1.367-4.204z"/>
                                    </svg>
                                    <p class="text-sm text-gray-600 ml-2">4.5 (25 reviews)</p>
                                </div>
                                <p class="text-sm text-gray-600">
                                    100 Total bookings
                                </p>
                            </div>

                            <!-- Call to Action Buttons -->
                            <div class="flex justify-between items-center">
                                <button class="bg-gray-100 text-gray-600 text-sm font-semibold px-4 py-2 rounded-lg hover:bg-gray-200">
                                    <a href="#">More Info</a>
                                </button>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</div>

</template>
