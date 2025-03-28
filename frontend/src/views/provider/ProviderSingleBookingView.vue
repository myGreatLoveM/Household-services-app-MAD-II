<script setup>
</script>


<template>
  <div class="bg-white shadow-lg rounded-lg p-8 mb-8 max-w-4xl mx-auto border border-gray-200">
  <!-- Booking Header -->
  <div class="flex items-center justify-between mb-6">
    <div class="space-y-1">
      <h2 class="text-3xl font-semibold text-gray-800">Booking #12345</h2>
      <h5 class="text-sm text-gray-600">2025-03-26 10:30 AM</h5>
    </div>
    <span class="text-sm text-gray-500">Status: <span class="font-semibold text-green-500">Confirmed</span></span>
  </div>

  <!-- Customer and Service Info -->
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-8 mb-8">
    <!-- Customer Info -->
    <div class="bg-gray-50 p-6 rounded-lg shadow-sm space-y-2">
      <h3 class="text-lg font-medium text-gray-700 mb-4">Customer Information</h3>
      <p class="text-gray-600">Name: <span class="font-semibold">John Doe</span></p>
      <p class="text-gray-600">Location: <span class="font-semibold">Mumbai, India</span></p>
      <p class="text-gray-600">Email: <span class="font-semibold">johndoe@example.com</span></p>
      <p class="text-gray-600">Contact: <span class="font-semibold">+91 9876543210</span></p>
    </div>

    <!-- Service Info -->
    <div class="bg-gray-50 p-6 rounded-lg shadow-sm space-y-2">
      <h3 class="text-lg font-medium text-gray-700 mb-4">Service Details</h3>
      <p class="text-gray-600">Service Title: <span class="font-semibold">Plumbing Repair</span></p>
      <p class="text-gray-600">Category: <span class="font-semibold">Plumbing</span></p>
      <p class="text-gray-600">Price: <span class="font-semibold text-blue-500">500 ₹/hr</span></p>
      <p class="text-gray-600">Time Required: <span class="font-semibold">2 hrs</span></p>
    </div>
  </div>

  <!-- Booking and Payment Details -->
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-8 mb-8">
    <!-- Booking Info -->
    <div class="bg-gray-50 p-6 rounded-lg shadow-sm space-y-3">
      <div class="space-y-2">
        <h3 class="text-lg font-medium text-gray-700 mb-4">Booking Information</h3>
        <p class="text-gray-600">Date Booked from: <span class="font-semibold">2025-03-25 09:00 AM -- 2025-03-26 12:00 PM</span></p>
        <p class="text-gray-600">Remark: <span class="font-semibold">Fix leaking faucet</span></p>
      </div>
      <div class="space-y-2">
        <p class="text-gray-600">Confirmed on: <span class="font-semibold">2025-03-25 10:00 AM</span></p>
        <p class="text-gray-600">Completed on: <span class="font-semibold">2025-03-26 02:00 PM</span></p>
        <p class="text-gray-600">Closed on: <span class="font-semibold">2025-03-26 04:00 PM</span></p>
      </div>
    </div>

    <!-- Payment Info -->
    <div class="bg-gray-50 p-6 rounded-lg shadow-sm space-y-2">
      <h3 class="text-lg font-medium text-gray-700 mb-4">Payment Information</h3>
      <p class="text-gray-600">Payment Status: <span class="font-semibold text-green-500">Paid</span></p>
      <p class="text-gray-600">Original amount: <span class="font-semibold">1000 ₹</span></p>
      <p class="text-gray-600">Service fee: <span class="font-semibold">50 ₹</span></p>
      <p class="text-gray-600">Final amount: <span class="font-semibold text-blue-400">950 ₹</span></p>
      <p class="text-gray-600">Payment Date: <span class="font-semibold">2025-03-26 03:00 PM</span></p>
    </div>
  </div>

  <!-- Review & Ratings -->
  <div class="mt-4">
    <h4 class="text-md font-semibold text-gray-700 mb-2">Review & Ratings</h4>
    <div class="space-y-4">
      <div class="bg-gray-100 p-4 rounded-lg">
        <div class="flex justify-between items-center">
          <p class="text-sm text-gray-600">2025-03-26 05:00 PM</p>
          <div class="flex items-center">
            <svg class="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.283 3.953a1 1 0 00.95.691h4.17c.969 0 1.371 1.24.588 1.81l-3.383 2.457a1 1 0 00-.364 1.118l1.283 3.953c.3.921-.755 1.688-1.54 1.118l-3.383-2.457a1 1 0 00-1.175 0l-3.383 2.457c-.785.57-1.839-.197-1.54-1.118l1.283-3.953a1 1 0 00-.364-1.118L2.268 9.381c-.783-.57-.381-1.81.588-1.81h4.17a1 1 0 00.95-.691l1.283-3.953z"></path>
            </svg>
            <svg class="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.283 3.953a1 1 0 00.95.691h4.17c.969 0 1.371 1.24.588 1.81l-3.383 2.457a1 1 0 00-.364 1.118l1.283 3.953c.3.921-.755 1.688-1.54 1.118l-3.383-2.457a1 1 0 00-1.175 0l-3.383 2.457c-.785.57-1.839-.197-1.54-1.118l1.283-3.953a1 1 0 00-.364-1.118L2.268 9.381c-.783-.57-.381-1.81.588-1.81h4.17a1 1 0 00.95-.691l1.283-3.953z"></path>
            </svg>
          </div>
        </div>
        <p class="text-sm text-gray-600 mt-2">Great service, fixed the issue quickly!</p>
      </div>
    </div>
  </div>

  <!-- Action Buttons -->
  <div class="flex justify-end gap-6 mt-6">
    <button class="px-5 py-2 bg-green-600 text-white font-semibold rounded shadow-md hover:bg-green-700 transition duration-200 ease-in-out transform hover:scale-105 focus:outline-none">
      Confirm
    </button>
    <button class="px-5 py-2 bg-red-600 text-white font-semibold rounded shadow-md hover:bg-red-700 transition duration-200 ease-in-out transform hover:scale-105 focus:outline-none">
      Reject
    </button>
  </div>
</div>

</template>