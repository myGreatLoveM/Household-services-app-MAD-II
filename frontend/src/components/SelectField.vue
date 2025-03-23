<script setup>

defineProps({
  id: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    required: true,
  },
  modelValue: {
    type: String,
    required: true,
  },
  choices: {
    type: Array,
    required: true
  },
  error: String,
  placeholder: String,
})

defineEmits(['update:modelValue'])
</script>

<template>
  <div>
    <label :for="id" class="text-base font-medium text-gray-900">{{ label }}</label>
    <div class="mt-2">
      <select
        :id="id"
        :value="modelValue"
        @input="(e) => $emit('update:modelValue', e.target.value)"
        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 "
      >
        <option value="" disabled>{{ placeholder }}</option>
        <option v-for="choice, i in choices" :value="choice.value" :key="i">{{ choice.label }}</option>
      </select>
    </div>
    <p :class="error ? 'block' : 'hidden'" class="text-red-500">{{ error }}</p>
  </div>
</template>
