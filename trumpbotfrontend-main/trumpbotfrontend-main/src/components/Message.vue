<script setup>
import { defineProps } from "vue";
const props = defineProps({
  message: String,
  type: String,
});
</script>

<template>
  <li>
    <div class="flex flex-col py-4 px-7">
      <div class="flex flex-row h-full" v-if="props.type === 'trump'">
        <img class="mr-5 w-10" src="assets/trump.png" alt="trump-avatar" />
        <p class="text-xl self-center">Donald Trump</p>
      </div>
      <div class="flex flex-row h-full" v-else>
        <img class="w-10 mr-5" src="assets/user.png" alt="user-avatar" />
        <p class="text-xl self-center">You</p>
      </div>
      <div class="flex-grow pt-2">
        <p class="text-ellipsis">{{ props.message }}</p>
      </div>
    </div>
  </li>
</template>

<style scoped></style>
