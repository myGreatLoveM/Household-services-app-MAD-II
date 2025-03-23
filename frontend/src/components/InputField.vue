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
  labelInfo: {type: String},
  classForLabel: {type: String},
  classForInputField: {type: String},
  type: {
    type: String,
    default: 'text',
  },
  modelValue: {
    type: String,
    required: true,
  },
  error: String,
  placeholder: String,
})

defineEmits(['update:modelValue'])
</script>

<template>
  <div>
    <label :for="id" :class="classForLabel ? classForLabel : 'text-base font-medium text-gray-900'">
      {{ label }}
      <span class="text-xs"> {{ labelInfo }}</span>
    </label>
    <div class="mt-2">
      <input
        :type="type"
        :id="id"
        :value="modelValue"
        @input="(e) => $emit('update:modelValue', e.target.value)"
        :placeholder="placeholder"
        :class="classForInputField ? classForInputField : 'flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50'"
        autocomplete="on"
      />
    </div>
    <p :class="error ? 'block' : 'hidden'" class="text-red-500">{{ error }}</p>
  </div>
</template>
