<script setup>
</script>


<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-4">
<div class="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
    <div>
      <h2 class="text-lg font-semibold">All Services</h2>
      <p class="mt-1 text-sm text-gray-700">
        This is a list of all services.
      </p>
    </div>

    <div class="flex items-center gap-10">
        <button
          type="button"
          class="rounded-md bg-zinc-600 hover:bg-zinc-700 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black">
            <a
            href="#">
              New Listed Services
            </a>
        </button>

    </div>
</div>


<div class="relative overflow-x-auto shadow-md sm:rounded-lg mt-10">
  <table class="w-full  bg-white text-sm">
    <thead class="text-left bg-gray-50 uppercase">
      <tr class="text-center">
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Service Id</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Title</th>
        <th scope="col" class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Category</th>
        <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Provider</th>
        <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Price /hr</th>
        <th scope="col"  class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">Status</th>
        <th scope="col"  class="px-4 py-2">Action</th>
      </tr>
    </thead>

    <tbody class="divide-y divide-gray-200">
        <tr class="odd:bg-white even:bg-gray-50 text-center">
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">service.id</td>
            <td class="whitespace-nowrap px-4 py-2 font-medium text-gray-900">service.title</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">provider.category.name</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">provider.username</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">service.price ₹</td>
            <td class="whitespace-nowrap px-4 py-2 text-gray-700">
                <span
                class="whitespace-nowrap rounded-full border border-red-500 px-2.5 py-0.5 text-sm text-red-700"
                >
                blocked
                </span>
                <span
                  class="whitespace-nowrap rounded-full border border-green-500 px-2.5 py-0.5 text-sm text-green-700"
                  >
                  active
                </span>
                <span
                class="whitespace-nowrap rounded-full border border-yellow-500 px-2.5 py-0.5 text-sm text-yellow-700"
                >
                discontinue
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
