<script setup>
import { RouterLink } from 'vue-router'
import { computed } from 'vue';

const props = defineProps({
  total: {
    type: Number,
    required: true,
  },
  currentPage: {
    type: Number,
    required: true,
  },
  pages: {
    type: Number,
    required: true,
  },
  perPage: {
    type: Number,
    required: true
  },
  path: {
    type: Object,
    required: true,
    default: () => ({
      name: 'home',
      query: {},
      params: {}
    })
  }
})


const firstItem = computed(() => {
  return ((props.currentPage-1) * props.perPage) + 1
})

const lastItem = computed(() => {
  return (props.currentPage * props.perPage) > props.total ? props.total : (props.currentPage * props.perPage)
})

const hasPrevPage = computed(() => {
  return props.currentPage > 1
})

const hasNextPage = computed(() => {
  return props.currentPage < props.pages
})

</script>


<template>
  <div v-if="total > perPage" class="w-full max-w-7xl  border-t border-gray-300 mt-5">
    <div class="mt-2 flex items-center justify-between">
      <div>
        <p>
          showing <strong>{{ firstItem }}</strong> to <strong>{{ lastItem }}</strong> of <strong>{{ total }}</strong> results
        </p>
      </div>
      <div class="flex gap-5">

        <div v-if="hasPrevPage">
          <RouterLink
            :to="{ name: path?.name, query: { ...path?.query, page: currentPage-1 }, params: { ...path?.params } }"
            class="rounded-md bg-black px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
          >
            ← Previous
          </RouterLink>
        </div>

        <div v-if="hasNextPage">
          <RouterLink
            :to="{ name: path?.name, query: { ...path?.query, page: currentPage+1 }, params: { ...path?.params } }"
            class="rounded-md bg-black px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-black/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black"
          >
            Next →
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>
