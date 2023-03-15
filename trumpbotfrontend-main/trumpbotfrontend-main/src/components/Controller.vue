<script setup>
import { ref } from "vue";
const message = ref("");

const clearInput = () => {
  message.value = "";
};
</script>

<template>
  <div class="w-full flex flex-row">
    <input
      type="text"
      placeholder="Type in a topic ..."
      class="w-5/6 px-3"
      v-model="message"
      @keypress.enter="$emit('sendQuestion', message, clearInput)"
    />
    <button
      class="w-1/6 bg-green-600 p-2 text-white cursor-pointer hover:bg-green-700"
      @click="$emit('sendQuestion', message, clearInput)"
    >
      Send
    </button>
  </div>
</template>

<style scoped></style>
